#!/usr/bin/env python3
"""Post-campaign detail extraction for RESULTS.md:
- find + render a W2 period-3 and period-8 cycle (2-law, complete stratum rescan)
- render a W1 period-4 cycle from stored specimens
- summarize supersession specimen classes; render any glider (with 3-period
  re-verification) or the characteristic pulse fauna
"""
import json, os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nomos_lib import (build_tables, make_step, make_step_supersession,
                       classify, seed_from_slots, gen_canonical, spacetime,
                       verify_glider)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def lawstr(slots, NT, W):
    TY, _, _, _ = build_tables(W)
    return ", ".join(f"{TY[s % NT]}@{s // NT}" for s in slots)

_G = {}
def _init():
    _G["s"] = make_step(2, "parity")

def _scan(args):
    slots = args
    v, t, info = classify(seed_from_slots(slots, 125), _G["s"], max_steps=200)
    if v == "cycle" and info["period"] in (3, 6, 8):
        return (info["period"], slots)
    return None

def main():
    # --- odd/long-period W2 cycles
    found = {}
    jobs = [s for k in (1, 2) for s in gen_canonical(125, 5, k)]
    with Pool(10, initializer=_init) as pool:
        for r in pool.imap_unordered(_scan, jobs, chunksize=500):
            if r and r[0] not in found:
                found[r[0]] = r[1]
            if set(found) >= {3, 6, 8}:
                break
    step2 = make_step(2, "parity")
    for p in sorted(found):
        slots = found[p]
        print(f"\nW2 period-{p} cycle: {lawstr(slots, 125, 2)}  slots={slots}")
        S = seed_from_slots(slots, 125)
        for t, row in enumerate(spacetime(S, step2, p + p + 1, -6, 8)):
            print(f"  t={t:2d} {row}")
    # --- W1 period-4
    d = json.load(open(os.path.join(DATA, "w1_le3_duel.json")))
    p4 = [c for c in d["specimens"]["cycle"] if c["info"]["period"] == 4]
    if p4:
        slots = p4[0]["slots"]
        print(f"\nW1 period-4 cycle: {lawstr(slots, 27, 1)}  slots={slots}")
        S = seed_from_slots(slots, 27)
        for t, row in enumerate(spacetime(S, make_step(1, "parity"), 9, -6, 8)):
            print(f"  t={t:2d} {row}")
    # --- supersession summary + any gliders
    sup = make_step_supersession(1)
    for name in ("super_le3", "super_4law_sample", "super_5law_sample"):
        p = os.path.join(DATA, name + ".json")
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        print(f"\n{name}: tally {d['tally']}  cycles {d['cycle_period_histogram']}")
        for g in d["specimens"].get("glider", []):
            slots = g["slots"]
            print(f"  GLIDER: {lawstr(slots, 27, 1)} info={g['info']}")
            S = seed_from_slots(slots, 27)
            # independent re-verification from scratch
            v, t, info = classify(S, sup, max_steps=2000)
            print(f"  re-classify: {v} {info}")
            for t, row in enumerate(spacetime(S, sup, 14, -8, 14)):
                print(f"  t={t:2d} {row}")

if __name__ == "__main__":
    main()
