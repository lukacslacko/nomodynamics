#!/usr/bin/env python3
"""Deep re-run of every slow-holdout specimen from the sweeps: 10x budget
(20000 steps, hash cap 400, growth cutoff 20000), parallel.  Also records
edge-pinning evidence over the first 3000 steps (the anchor made visible).
Cryptid triage (N6)."""
import json, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nomos_lib import make_step, make_step_supersession, classify, seed_from_slots

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

ENGINES = {
    "w1_le3_duel":         ("w1duel", 27),
    "w2_le2_duel":         ("w2duel", 125),
    "w2_3law_duel_sample": ("w2duel", 125),
    "super_le3":           ("super", 27),
    "super_4law_sample":   ("super", 27),
    "super_5law_sample":   ("super", 27),
    "w1_4law_parity":      ("w1par", 27),
    "hunt_5law_6cells_or": ("w1or", 27),
    "hunt_6law_6cells_or": ("w1or", 27),
    "hunt_4law_6cells_w2_or": ("w2or", 125),
}

_G = {}
def _init():
    _G["w1duel"] = (make_step(1, "parity"), make_step(1, "or"), 27)
    _G["w2duel"] = (make_step(2, "parity"), make_step(2, "or"), 125)
    _G["super"] = (make_step_supersession(1), None, 27)
    _G["w1par"] = (make_step(1, "parity"), None, 27)
    _G["w1or"] = (make_step(1, "or"), None, 27)
    _G["w2or"] = (make_step(2, "or"), None, 125)

def _one(job):
    ek, slots = job
    step, step2, NT = _G[ek]
    S = seed_from_slots(slots, NT)
    v, t, info = classify(S, step, step2=step2, max_steps=20000,
                          hash_cap=400, growth_cap=20000, width_stop=800)
    T = dict(S); mn0, mx0 = min(T), max(T)
    mn_moved = mx_moved = False
    for _ in range(3000):
        if not T:
            break
        if min(T) != mn0: mn_moved = True
        if max(T) != mx0: mx_moved = True
        T = step(T)
    return {"slots": list(slots), "deep_verdict": v, "t": t, "info": info,
            "left_edge_moved": mn_moved, "right_edge_moved": mx_moved}

def main():
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, os.cpu_count() - 2)
    only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    t0 = time.time()
    out = {}
    if os.path.exists(os.path.join(DATA, "holdouts_resolved.json")):
        with open(os.path.join(DATA, "holdouts_resolved.json")) as f:
            out = json.load(f)
    for name, (ek, NT) in ENGINES.items():
        if only and name not in only:
            continue
        if name in out:
            continue
        path = os.path.join(DATA, name + ".json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            d = json.load(f)
        hos = d["specimens"].get("slow-holdout", [])
        if not hos:
            out[name] = {"n_holdouts": 0, "deep_tally": {}, "resolved": []}
            continue
        jobs = [(ek, tuple(h["slots"])) for h in hos]
        with Pool(procs, initializer=_init) as pool:
            res = pool.map(_one, jobs, chunksize=16)
        tally = {}
        for r in res:
            tally[r["deep_verdict"]] = tally.get(r["deep_verdict"], 0) + 1
        out[name] = {"n_holdouts": len(hos), "deep_tally": tally,
                     "resolved": res}
        print(f"[holdouts] {name}: {len(hos)} -> {tally} "
              f"({round(time.time()-t0)}s)", flush=True)
    with open(os.path.join(DATA, "holdouts_resolved.json"), "w") as f:
        json.dump(out, f)
    print(f"[holdouts] DONE wall={round(time.time()-t0)}s")

if __name__ == "__main__":
    main()
