#!/usr/bin/env python3
"""wider.py — both theorems claim "any offsets, any window W".  W=1 is only the
first window.  This script attacks W = 2, 3, 4, 5 as well, in both universes,
and chases every UNRESOLVED holdout to a much deeper step budget.

Rule pool at window W: all (a,b,c) with a,b,c in {-W..W}  ->  (2W+1)^3 rules.
The 64-bit frame (PAD=6, max_span=40) is exact for |offset| <= 5.
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import xnomos                                                  # noqa: E402
import fastlib as F                                            # noqa: E402
from census import verify_hits, MAXSTEPS, MAXCARD, MAXSPAN     # noqa: E402

BLOCKS = []


def pool(W):
    o = range(-W, W + 1)
    return [(a, b, c) for a in o for b in o for c in o]


def run(name, scope, box, consts, seeds, mode, deep=8000):
    nc, n, cf = F.pack_consts(consts)
    t = time.time()
    hist, hits = F.census(cf, nc, n, mode, seeds, MAXSTEPS, MAXCARD, MAXSPAN,
                          maxhits=300000, report=("GLIDER", "UNRESOLVED"))
    dt = time.time() - t
    gl = [h for h in hits if h[4] >= 0]
    un = [h for h in hits if h[4] < 0]
    ver = verify_hits(consts, seeds, mode, gl) if gl else []
    # ---- chase every UNRESOLVED holdout to a deep step budget
    deep_hist = {}
    deep_gl = []
    for ci, si, _p, _d, _t in un:
        r = F.classify(F.pack_const(consts[ci][0], consts[ci][1], n), n, mode,
                       seeds[si], deep, MAXCARD, MAXSPAN)
        deep_hist[r["kind"]] = deep_hist.get(r["kind"], 0) + 1
        if r["kind"] == "GLIDER":
            deep_gl.append((ci, si, r["period"], r["disp"], r["t0"]))
    deep_ver = verify_hits(consts, seeds, mode, deep_gl) if deep_gl else []
    rec = dict(name=name, scope=scope, box=box, mode=mode, n=n, nconst=int(nc),
               nseed=int(len(seeds)), runs=int(nc * len(seeds)),
               secs=round(dt, 2), hist=hist, gliders=ver,
               n_unresolved_chased=len(un), deep_budget=deep,
               deep_hist=deep_hist, deep_gliders=deep_ver)
    BLOCKS.append(rec)
    print("%-40s %-9s %-8s C=%-8d S=%-6d runs=%-12d %6.1fs | GLIDER=%-4d "
          "unres=%-6d -> deep(%d): %s"
          % (name, mode, scope, nc, len(seeds), nc * len(seeds), dt,
             hist["GLIDER"], hist["UNRESOLVED"], deep,
             deep_hist if deep_hist else "-"))
    if ver or deep_ver:
        print("   !! GLIDER CANDIDATES:", json.dumps((ver + deep_ver)[:5]))
    return rec


def sample_consts(P, n, targets, count, rng):
    idx = rng.integers(0, len(P), size=(count, n))
    return [([P[i] for i in row], list(targets)) for row in idx]


def main():
    rng = np.random.default_rng(56789)

    # ---------------------------------------------------------------- E2
    print("\n=== WIDER WINDOWS — E2 permutation targeting (Theorem A) ===")
    for W in (2, 3):
        P = pool(W)
        c2 = [(list(r), [1, 0]) for r in itertools.product(P, repeat=2)]
        for mode in ("parity", "or"):
            run("E2 W=%d L=2 [1,0] <=4laws/6cells" % W, "COMPLETE",
                "all %d^2=%d consts x all canonical seeds <=4 laws/6 cells"
                % (len(P), len(P) ** 2), c2, F.all_seeds(2, 6, 4), mode)
        run("E2 W=%d L=2 [1,0] <=6laws/8cells" % W, "COMPLETE",
            "all %d^2=%d consts x all canonical seeds <=6 laws/8 cells"
            % (len(P), len(P) ** 2), c2, F.all_seeds(2, 8, 6), "parity")
        del c2
        for L, tg in ((3, [1, 2, 0]), (4, [1, 2, 3, 0])):
            cs = sample_consts(P, L, tg, 200000, rng)
            run("E2 W=%d L=%d cycle <=3laws/5cells" % (W, L), "SAMPLE",
                "200,000 consts drawn uniformly from %d^%d (numpy PCG64 seed "
                "56789) x all canonical seeds <=3 laws/5 cells" % (len(P), L),
                cs, F.all_seeds(L, 5, 3), "parity")
    for W in (4, 5):
        P = pool(W)
        cs = sample_consts(P, 2, [1, 0], 300000, rng)
        run("E2 W=%d L=2 [1,0] <=4laws/6cells" % W, "SAMPLE",
            "300,000 consts drawn uniformly from %d^2 (PCG64 seed 56789) x all "
            "canonical seeds <=4 laws/6 cells" % len(P),
            cs, F.all_seeds(2, 6, 4), "parity")

    # ------------------------------------------------------- supersession
    print("\n=== WIDER WINDOWS — E1 supersession (Theorem B) ===")
    for W in (2, 3):
        P = pool(W)
        c1 = [(list(r), [0]) for r in itertools.product(P, repeat=1)]
        c2 = [(list(r), [0, 1]) for r in itertools.product(P, repeat=2)]
        for mode in ("super", "super_or"):
            run("SUP W=%d n=1 <=7laws/9cells" % W, "COMPLETE",
                "all %d consts x all canonical seeds <=7 laws/9 cells" % len(P),
                c1, F.all_seeds(1, 9, 7), mode)
            run("SUP W=%d n=2 <=4laws/6cells" % W, "COMPLETE",
                "all %d^2=%d consts x all canonical seeds <=4 laws/6 cells"
                % (len(P), len(P) ** 2), c2, F.all_seeds(2, 6, 4), mode)
        run("SUP W=%d n=2 <=5laws/7cells" % W, "COMPLETE",
            "all %d^2=%d consts x all canonical seeds <=5 laws/7 cells"
            % (len(P), len(P) ** 2), c2, F.all_seeds(2, 7, 5), "super")
        del c1, c2
        for n in (3, 4):
            cs = sample_consts(P, n, list(range(n)), 200000, rng)
            for mode in ("super", "super_or"):
                run("SUP W=%d n=%d <=3laws/5cells" % (W, n), "SAMPLE",
                    "200,000 consts drawn uniformly from %d^%d (PCG64 seed "
                    "56789) x all canonical seeds <=3 laws/5 cells" % (len(P), n),
                    cs, F.all_seeds(n, 5, 3), mode)
    for W in (4, 5):
        P = pool(W)
        cs = sample_consts(P, 2, [0, 1], 300000, rng)
        for mode in ("super", "super_or"):
            run("SUP W=%d n=2 <=4laws/6cells" % W, "SAMPLE",
                "300,000 consts drawn uniformly from %d^2 (PCG64 seed 56789) x "
                "all canonical seeds <=4 laws/6 cells" % len(P),
                cs, F.all_seeds(2, 6, 4), mode)


if __name__ == "__main__":
    t0 = time.time()
    main()
    tot = sum(b["runs"] for b in BLOCKS)
    gl = sum(b["hist"]["GLIDER"] for b in BLOCKS)
    dg = sum(len(b["deep_gliders"]) for b in BLOCKS)
    ch = sum(b["n_unresolved_chased"] for b in BLOCKS)
    print("\nTOTAL: %d blocks, %s runs, %.1f min | GLIDERS=%d, holdouts chased"
          " to depth=%d of which gliders=%d"
          % (len(BLOCKS), f"{tot:,}", (time.time() - t0) / 60, gl, ch, dg))
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    with open(os.path.join(HERE, "data", "wider.json"), "w") as f:
        json.dump(BLOCKS, f, indent=1)
