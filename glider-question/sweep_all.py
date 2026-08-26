#!/usr/bin/env python3
"""sweep_all.py — Expedition N-A rigorous sweeps.

Phases (run as: python3 sweep_all.py <phase>):
  w1core : COMPLETE <=3 placed laws in a 5-cell window, W=1, parity+OR in
           lockstep duel (every step of every seed asserts parity==OR).
  w2core : COMPLETE <=2 laws / 5 cells at W=2 (duel) + SAMPLED 3-law (1e6
           canonical seeds, rng seed 20260826, duel).
  super  : COMPLETE <=3 laws / 5 cells, supersession variant (cross-kind
           effects) — the sharpness hunt.  + sampled 4-law (5e5).
  w1ext4 : COMPLETE 4-law / 5 cells, W=1 parity (engineered-hunt coverage;
           OR identical by the Collision Lemma, machine-verified in w1core).
  hunt56 : engineered caterpillar regime: sampled 1e6 seeds of 5-6 laws in a
           6-cell window, <=4 distinct kinds, OR engine, W=1.
  verify : anchor-invariant machine check on random trajectories, all engines.

Budgets (as pre-registered): 2000 steps/seed, hash cap 150, growth cutoff 3000
(+ documented sustained-width early-evidence stop, width>320 with 3 strictly
increasing 100-step block-min widths — impossible for any bounded-width
pattern, so no glider can be misfiled).
Certificates: every glider recurrence is re-verified over 3 further periods.
"""
import json, math, os, random, sys, time
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nomos_lib import (build_tables, make_step, make_step_supersession,
                       classify, seed_from_slots, gen_canonical,
                       count_canonical, check_anchor_invariants)

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SPECIMEN_CAP = 300          # per-verdict cap for archived specimens
ALWAYS_KEEP = {"glider", "anomaly", "divergence", "slow-holdout"}

_G = {}

def _init(kind):
    """Pool initializer: build steppers once per worker."""
    if kind == "w1duel":
        _G["step"] = make_step(1, "parity"); _G["step2"] = make_step(1, "or")
        _G["NT"] = 27
    elif kind == "w2duel":
        _G["step"] = make_step(2, "parity"); _G["step2"] = make_step(2, "or")
        _G["NT"] = 125
    elif kind == "w1par":
        _G["step"] = make_step(1, "parity"); _G["step2"] = None
        _G["NT"] = 27
    elif kind == "w1or":
        _G["step"] = make_step(1, "or"); _G["step2"] = None
        _G["NT"] = 27
    elif kind == "w2or":
        _G["step"] = make_step(2, "or"); _G["step2"] = None
        _G["NT"] = 125
    elif kind == "super":
        _G["step"] = make_step_supersession(1); _G["step2"] = None
        _G["NT"] = 27

def _run_seeds(slot_tuples):
    """Classify a list of slot-tuples; return (tally, cycle_hist, specimens, n)."""
    step, step2, NT = _G["step"], _G["step2"], _G["NT"]
    tally = Counter(); cyc = Counter(); onset_max = [0, None]
    spec = {}
    n = 0
    for slots in slot_tuples:
        S = seed_from_slots(slots, NT)
        v, t, info = classify(S, step, step2=step2)
        n += 1
        tally[v] += 1
        if v == "cycle":
            cyc[info["period"]] += 1
            if info["transient"] > onset_max[0]:
                onset_max = [info["transient"], slots]
        if v in ALWAYS_KEEP or (v not in ("extinct", "fixed")
                                and tally[v] <= SPECIMEN_CAP):
            spec.setdefault(v, []).append({"slots": list(slots), "t": t,
                                           "info": info})
    return tally, cyc, spec, n, onset_max

def _merge(agg, res):
    tally, cyc, spec, n, onset = res
    agg["tally"].update(tally); agg["cycles"].update(cyc); agg["n"] += n
    if onset[0] > agg["max_transient"][0]:
        agg["max_transient"] = onset
    for v, lst in spec.items():
        cur = agg["spec"].setdefault(v, [])
        room = 100000 if v in ALWAYS_KEEP else SPECIMEN_CAP
        cur.extend(lst[:max(0, room - len(cur))])

def _new_agg():
    return {"tally": Counter(), "cycles": Counter(), "spec": {}, "n": 0,
            "max_transient": [0, None]}

def _finish(agg, name, meta, t0):
    out = {"name": name, "meta": meta, "n": agg["n"],
           "tally": dict(agg["tally"]),
           "cycle_period_histogram": dict(sorted(agg["cycles"].items())),
           "max_transient": agg["max_transient"],
           "wall_seconds": round(time.time() - t0, 1),
           "specimens": agg["spec"]}
    path = os.path.join(DATA, name + ".json")
    with open(path, "w") as f:
        json.dump(out, f)
    print(f"[{name}] DONE n={agg['n']} tally={dict(agg['tally'])} "
          f"wall={out['wall_seconds']}s -> {path}", flush=True)
    return out

def _chunks(it, size):
    buf = []
    for x in it:
        buf.append(x)
        if len(buf) >= size:
            yield buf; buf = []
    if buf:
        yield buf

def run_complete(name, engine_kind, NT, npos, sizes, procs, chunk=4000):
    t0 = time.time()
    total = sum(count_canonical(NT, npos, k) for k in sizes)
    print(f"[{name}] complete sweep: sizes {sizes}, canonical seeds = {total}",
          flush=True)
    agg = _new_agg()
    def gen_all():
        for k in sizes:
            yield from gen_canonical(NT, npos, k)
    with Pool(procs, initializer=_init, initargs=(engine_kind,)) as pool:
        done = 0
        for res in pool.imap_unordered(_run_seeds, _chunks(gen_all(), chunk)):
            _merge(agg, res)
            done += res[3]
            if done // 200000 != (done - res[3]) // 200000:
                print(f"[{name}] {done}/{total} tally={dict(agg['tally'])} "
                      f"{round(time.time()-t0)}s", flush=True)
    assert agg["n"] == total, (agg["n"], total)
    return _finish(agg, name, {"complete": True, "sizes": list(sizes),
                               "npos": npos, "NT": NT, "total": total}, t0)

def run_sampled(name, engine_kind, NT, npos, k, nsamples, procs, rngseed,
                max_kinds=None, chunk=4000):
    t0 = time.time()
    space = count_canonical(NT, npos, k)
    rng = random.Random(rngseed)
    nslots = npos * NT
    seen = set()
    samples = []
    while len(samples) < nsamples:
        s = tuple(sorted(rng.sample(range(nslots), k)))
        if s[0] >= NT:            # canonical: min position must be 0
            continue
        if max_kinds is not None:
            if len({x % NT for x in s}) > max_kinds:
                continue
        if s in seen:
            continue
        seen.add(s); samples.append(s)
    print(f"[{name}] sampled sweep: k={k}, {nsamples} distinct canonical seeds "
          f"of {space} ({100*nsamples/space:.2f}% of space), rng={rngseed}",
          flush=True)
    agg = _new_agg()
    with Pool(procs, initializer=_init, initargs=(engine_kind,)) as pool:
        done = 0
        for res in pool.imap_unordered(_run_seeds, _chunks(iter(samples), chunk)):
            _merge(agg, res)
            done += res[3]
            if done // 200000 != (done - res[3]) // 200000:
                print(f"[{name}] {done}/{nsamples} tally={dict(agg['tally'])} "
                      f"{round(time.time()-t0)}s", flush=True)
    return _finish(agg, name, {"complete": False, "k": k, "nsamples": nsamples,
                               "space": space, "rngseed": rngseed,
                               "max_kinds": max_kinds, "npos": npos, "NT": NT},
                   t0)

# ------------------------------------------------------------------ verify

def run_verify(procs):
    """Anchor-invariant machine check along random trajectories, all engines."""
    t0 = time.time()
    out = {}
    for W, mode, n in ((1, "parity", 20000), (1, "or", 20000),
                       (2, "parity", 8000), (2, "or", 8000)):
        TYPES, NT, ACTIVE, CLIST = build_tables(W)
        step = make_step(W, mode)
        rng = random.Random(777 + W * 10 + (mode == "or"))
        viol = []
        for trial in range(n):
            k = rng.randint(1, 6)
            slots = sorted(rng.sample(range(5 * NT), k))
            S = seed_from_slots(slots, NT)
            r = check_anchor_invariants(S, step, TYPES, steps=300)
            if r is not None:
                viol.append({"slots": slots, "violation": r})
        out[f"W{W}-{mode}"] = {"trajectories": n, "violations": viol}
        print(f"[verify] W{W}-{mode}: {n} random trajectories x 300 steps, "
              f"violations={len(viol)}", flush=True)
    path = os.path.join(DATA, "verify_anchors.json")
    with open(path, "w") as f:
        json.dump(out, f)
    print(f"[verify] DONE wall={round(time.time()-t0,1)}s -> {path}", flush=True)

# ------------------------------------------------------------------ main

if __name__ == "__main__":
    procs = max(1, os.cpu_count() - 2)
    phase = sys.argv[1]
    if phase == "w1core":
        run_complete("w1_le3_duel", "w1duel", 27, 5, (1, 2, 3), procs)
    elif phase == "w2core":
        run_complete("w2_le2_duel", "w2duel", 125, 5, (1, 2), procs)
        run_sampled("w2_3law_duel_sample", "w2duel", 125, 5, 3, 1000000,
                    procs, rngseed=20260826)
    elif phase == "super":
        run_complete("super_le3", "super", 27, 5, (1, 2, 3), procs)
        run_sampled("super_4law_sample", "super", 27, 5, 4, 500000,
                    procs, rngseed=20260827)
    elif phase == "w1ext4":
        run_complete("w1_4law_parity", "w1par", 27, 5, (4,), procs)
    elif phase == "hunt56":
        run_sampled("hunt_5law_6cells_or", "w1or", 27, 6, 5, 500000,
                    procs, rngseed=20260828, max_kinds=4)
        run_sampled("hunt_6law_6cells_or", "w1or", 27, 6, 6, 500000,
                    procs, rngseed=20260829, max_kinds=4)
    elif phase == "super5":
        run_sampled("super_5law_sample", "super", 27, 6, 5, 500000,
                    procs, rngseed=20260831)
    elif phase == "huntw2":
        run_sampled("hunt_4law_6cells_w2_or", "w2or", 125, 6, 4, 300000,
                    procs, rngseed=20260830, max_kinds=4)
    elif phase == "verify":
        run_verify(procs)
    else:
        raise SystemExit(f"unknown phase {phase}")
