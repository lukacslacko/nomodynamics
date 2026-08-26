#!/usr/bin/env python3
"""Task 3: random small-seed survey (2-3 laws in a 3x3 patch) + targeted
symmetry-closed hunts.  Multiprocess.  Writes survey_<mode>.json."""
import argparse, json, random, sys, time
from collections import Counter
from multiprocessing import Pool
from engine2d import classify, TPERM, GID, tname

ROT2 = TPERM[GID[(2, 0)]]   # 180-degree type map
ROT1 = TPERM[GID[(1, 0)]]   # 90-degree ccw
MIR = TPERM[GID[(0, 1)]]    # mirror y->-y

def gen_seeds(mode, n, rng):
    seeds = []
    for _ in range(n):
        if mode == "main":
            nl = rng.choice((2, 2, 3, 3))
            spec = set()
            while len(spec) < nl:
                spec.add(((rng.randint(-1, 1), rng.randint(-1, 1)),
                          rng.randrange(125)))
            seeds.append(sorted(spec))
        elif mode == "rot2":   # {k, R2 k} at 2 positions in 3x3
            k = rng.randrange(1, 125)
            spec = set()
            while len(spec) < 2:
                p = (rng.randint(-1, 1), rng.randint(-1, 1))
                spec = {(p, k)} if not spec else spec | {(p, ROT2[k])}
            seeds.append(sorted(spec))
        elif mode == "mir2":   # {k, M k}
            k = rng.randrange(1, 125)
            spec = set()
            while len(spec) < 2:
                p = (rng.randint(-1, 1), rng.randint(-1, 1))
                spec = {(p, k)} if not spec else spec | {(p, MIR[k])}
            seeds.append(sorted(spec))
        elif mode == "rot4":   # {k,Rk,R2k,R3k} at 4 positions in 5x5
            k = rng.randrange(1, 125)
            ks = [k, ROT1[k], ROT1[ROT1[k]], ROT1[ROT1[ROT1[k]]]]
            spec = set()
            tries = 0
            while len(spec) < 4 and tries < 40:
                p = (rng.randint(-2, 2), rng.randint(-2, 2))
                cand = (p, ks[len(spec)])
                if cand not in spec:
                    spec.add(cand)
                tries += 1
            if len(spec) == 4:
                seeds.append(sorted(spec))
    return seeds

def work(args):
    i, spec = args
    v = classify(spec, sem="p", max_steps=256, growth_cap=1200,
                 hash_cap=240, d4_cap=96)
    v.pop("sizes", None)
    return i, v

def vclass(v):
    if v["v"] == "cycle":
        p = v["p"]
        return "cycle>8" if p > 8 else f"cycle-{p}"
    if v["v"] == "unresolved":
        return "unres-" + v["trend"]
    return v["v"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main")
    ap.add_argument("--n", type=int, default=30000)
    ap.add_argument("--seed", type=int, default=20260826)
    ap.add_argument("--procs", type=int, default=10)
    args = ap.parse_args()
    rng = random.Random(args.seed + sum(ord(c) for c in args.mode))
    seeds = gen_seeds(args.mode, args.n, rng)
    print(f"mode={args.mode}: {len(seeds)} seeds", flush=True)
    t0 = time.time()
    tally = Counter()
    keep = {"glider": [], "rotor": [], "glide": [], "cycle>8": [],
            "growth": [], "unres-flat": [], "unres-grow": [], "cycle-big": []}
    results = [None] * len(seeds)
    with Pool(args.procs) as pool:
        for i, v in pool.imap_unordered(work, enumerate(seeds), chunksize=64):
            results[i] = v
            c = vclass(v)
            tally[c] += 1
            if v["v"] in ("glider", "rotor", "glide"):
                keep[v["v"]].append((seeds[i], v))
            elif v["v"] == "cycle" and v["p"] > 8:
                keep["cycle>8"].append((seeds[i], v))
            elif v["v"] == "growth" and len(keep["growth"]) < 2000:
                keep["growth"].append((seeds[i], v))
            elif v["v"] == "unresolved":
                kk = "unres-" + v["trend"]
                if len(keep[kk]) < 12000:
                    keep[kk].append((seeds[i], v))
    dt = time.time() - t0
    print(f"done in {dt:.1f}s ({len(seeds)/dt:.0f} seeds/s)")
    print("tally:", dict(sorted(tally.items(), key=lambda kv: -kv[1])))
    for kk in ("glider", "rotor", "glide", "cycle>8"):
        print(f"{kk}: {len(keep[kk])}")
        for spec, v in keep[kk][:12]:
            print("   ", spec, {a: b for a, b in v.items() if a != "sizes"})
    out = dict(mode=args.mode, n=len(seeds), tally=dict(tally),
               keep={k: [(s, v) for s, v in lst] for k, lst in keep.items()})
    json.dump(out, open(f"survey_{args.mode}.json", "w"))
    print(f"wrote survey_{args.mode}.json")

if __name__ == "__main__":
    main()
