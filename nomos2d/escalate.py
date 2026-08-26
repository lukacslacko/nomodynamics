#!/usr/bin/env python3
"""Escalate unresolved survey seeds through deeper budgets.
Stage B: 6k steps.  Stage C: 30k steps.  Stage D: 200k on survivors.
Hunts: long cycles, gliders, rotors, glides, bounded-aperiodic holdouts."""
import argparse, json, time
from collections import Counter
from multiprocessing import Pool
from engine2d import classify

PARAMS = {
    "B": dict(max_steps=6000, growth_cap=8000, hash_cap=300, d4_cap=48,
              hw_cap=500),
    "C": dict(max_steps=30000, growth_cap=60000, hash_cap=220, d4_cap=32,
              hw_cap=2000),
    "D": dict(max_steps=250000, growth_cap=200000, hash_cap=200, d4_cap=0,
              hw_cap=None, light_hash=True),
}
def work(args):
    i, spec, stage = args
    v = classify(spec, sem="p", **PARAMS[stage])
    v.pop("sizes", None)
    return i, v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices="BCD")
    ap.add_argument("--infiles", nargs="+", required=True)
    ap.add_argument("--inkey", default="unres-flat")
    ap.add_argument("--procs", type=int, default=10)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    specs = []
    for f in args.infiles:
        d = json.load(open(f))
        if "keep" in d:      # survey file
            for s, v in d["keep"].get(args.inkey, []):
                specs.append(tuple((tuple(p), k) for p, k in s))
        else:                # earlier escalation file
            for s, v in d["survivors"]:
                specs.append(tuple((tuple(p), k) for p, k in s))
    if args.limit:
        specs = specs[:args.limit]
    print(f"stage {args.stage}: {len(specs)} seeds", flush=True)

    t0 = time.time()
    tally = Counter()
    finds = {"glider": [], "rotor": [], "glide": [], "longcycle": []}
    survivors = []
    growthy = []
    results = [None] * len(specs)
    with Pool(args.procs) as pool:
        for i, v in pool.imap_unordered(
                work, ((i, s, args.stage) for i, s in enumerate(specs)),
                chunksize=8):
            results[i] = v
            key = v["v"]
            if key == "cycle":
                key = f"cycle-{v['p']}" if v["p"] <= 8 else "cycle>8"
            if key == "unresolved":
                key = "unres-" + v["trend"]
            tally[key] += 1
            spec = [list(x) for x in specs[i]]
            if v["v"] in ("glider", "rotor", "glide"):
                finds[v["v"]].append((spec, v))
            elif v["v"] == "cycle" and v["p"] > 8:
                finds["longcycle"].append((spec, v))
            elif v["v"] == "unresolved":
                (survivors if v["trend"] == "flat" else growthy).append((spec, v))
            elif v["v"] in ("growth", "sprawl"):
                growthy.append((spec, v))
    dt = time.time() - t0
    print(f"done in {dt:.1f}s")
    print("tally:", dict(sorted(tally.items(), key=lambda kv: -kv[1])))
    for kk, lst in finds.items():
        if lst:
            print(f"{kk}: {len(lst)}; examples:")
            for s, v in lst[:10]:
                print("   ", s, v)
    print(f"survivors (still flat-unresolved): {len(survivors)}")
    for s, v in survivors[:20]:
        print("   ", s, v)
    print(f"growth-like escalations: {len(growthy)}")
    json.dump(dict(stage=args.stage, tally=dict(tally), finds=finds,
                   survivors=survivors, growthy=growthy),
              open(args.out, "w"))
    print("wrote", args.out)

if __name__ == "__main__":
    main()
