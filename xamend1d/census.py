#!/usr/bin/env python3
"""census.py — Tasks 2 and 3: the brute-force attack on Theorem A (E2 fixed
single targeting by a permutation) and Theorem B (E1 supersession).

Every block states COMPLETE ENUMERATION or SAMPLE with the exact box.
Every GLIDER the fast engine reports is re-verified by xnomos.verify_glider
over three full periods before it is allowed into the report.

Budgets for every run: max_steps=200, max_card=200, max_span=40.  A glider
outside that box (period > 200, or > 200 laws, or spanning > 40 cells) would
be missed here; the wide-frame scan in nearmiss.py is the safety net for the
wide case.
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

OFF = (-1, 0, 1)
RULES1 = [(a, b, c) for a in OFF for b in OFF for c in OFF]     # 27, W=1
MAXSTEPS, MAXCARD, MAXSPAN = 200, 200, 40

BLOCKS = []


def verify_hits(consts, seeds, mode, hits):
    """Re-verify every reported glider with the independent xnomos path."""
    out = []
    for ci, si, p, d, t0 in hits:
        rules, targets = consts[ci]
        C = xnomos.Const(rules, targets)
        S0 = F.unpack_state(seeds[si])
        S = dict(S0)
        for _ in range(t0):
            S = xnomos.step(S, C, mode)
        ok = xnomos.verify_glider(S, C, p, d, mode)
        res = xnomos.classify(S0, C, mode, MAXSTEPS, MAXCARD, MAXSPAN)
        out.append(dict(rules=[list(r) for r in rules], targets=list(targets),
                        mode=mode, seed=sorted(S0.items()), p=int(p), d=int(d),
                        t0=int(t0), verify_glider=bool(ok),
                        xnomos_kind=res["kind"]))
    return out


def block(name, scope, boxdesc, consts, seeds, mode):
    nc, n, cf = F.pack_consts(consts)
    t = time.time()
    hist, hits = F.census(cf, nc, n, mode, seeds, MAXSTEPS, MAXCARD, MAXSPAN)
    dt = time.time() - t
    runs = nc * len(seeds)
    ver = verify_hits(consts, seeds, mode, hits) if len(hits) else []
    rec = dict(name=name, scope=scope, box=boxdesc, mode=mode, n=n,
               nconst=int(nc), nseed=int(len(seeds)), runs=int(runs),
               secs=round(dt, 2), hist=hist,
               nglider_raw=int(len(hits)), gliders=ver)
    BLOCKS.append(rec)
    print("%-34s %-8s %-9s C=%-7d S=%-6d runs=%-12d %6.1fs  "
          "ext%-8d fix%-9d bal%-6d cyc%-9d GLIDER=%-4d grow%-9d unres%d"
          % (name, mode, scope, nc, len(seeds), runs, dt,
             hist["EXTINCT"], hist["FIXED"], hist["BALANCED"], hist["CYCLE"],
             hist["GLIDER"], hist["GROWING"], hist["UNRESOLVED"]))
    if ver:
        print("   !! GLIDER CANDIDATES:", json.dumps(ver[:5]))
    return rec


# ------------------------------------------------------------- constitutions

def e2_consts(L, targets):
    return [(list(r), list(targets)) for r in itertools.product(RULES1, repeat=L)]


def super_consts(n):
    return [(list(r), list(range(n))) for r in itertools.product(RULES1, repeat=n)]


def sample_consts(n, targets, count, rng):
    out = []
    for _ in range(count):
        idx = rng.integers(0, 27, size=n)
        out.append(([RULES1[i] for i in idx], list(targets)))
    return out


# --------------------------------------------------------------------- main

def task2():
    print("\n=== TASK 2 — E2: fixed single targeting by a PERMUTATION "
          "(attack on Theorem A) ===")
    # --- L = 2, targets [1,0] --------------------------------------------
    c2 = e2_consts(2, [1, 0])
    for mode in ("parity", "or"):
        block("E2 L=2 [1,0] <=4laws/6cells", "COMPLETE",
              "all 27^2=729 consts x all canonical seeds, <=4 laws in 6 cells",
              c2, F.all_seeds(2, 6, 4), mode)
        block("E2 L=2 [1,0] <=6laws/8cells", "COMPLETE",
              "all 27^2=729 consts x all canonical seeds, <=6 laws in 8 cells",
              c2, F.all_seeds(2, 8, 6), mode)

    # --- L = 3, targets [1,2,0] -------------------------------------------
    c3 = e2_consts(3, [1, 2, 0])
    for mode in ("parity", "or"):
        block("E2 L=3 [1,2,0] <=3laws/5cells", "COMPLETE",
              "all 27^3=19,683 consts x all canonical seeds, <=3 laws in 5 cells",
              c3, F.all_seeds(3, 5, 3), mode)
        block("E2 L=3 [1,2,0] <=4laws/6cells", "COMPLETE",
              "all 27^3=19,683 consts x all canonical seeds, <=4 laws in 6 cells",
              c3, F.all_seeds(3, 6, 4), mode)
    block("E2 L=3 [1,2,0] <=5laws/7cells", "COMPLETE",
          "all 27^3=19,683 consts x all canonical seeds, <=5 laws in 7 cells",
          c3, F.all_seeds(3, 7, 5), "parity")

    # --- L = 4, targets [1,2,3,0] -----------------------------------------
    c4 = e2_consts(4, [1, 2, 3, 0])
    for mode in ("parity", "or"):
        block("E2 L=4 [1,2,3,0] <=3laws/5cells", "COMPLETE",
              "all 27^4=531,441 consts x all canonical seeds, <=3 laws in 5 cells",
              c4, F.all_seeds(4, 5, 3), mode)
    block("E2 L=4 [1,2,3,0] <=4laws/6cells", "COMPLETE",
          "all 27^4=531,441 consts x all canonical seeds, <=4 laws in 6 cells",
          c4, F.all_seeds(4, 6, 4), "parity")

    # --- two 2-cycles, targets [1,0,3,2] ----------------------------------
    c22 = e2_consts(4, [1, 0, 3, 2])
    for mode in ("parity", "or"):
        block("E2 2+2 [1,0,3,2] <=3laws/5cells", "COMPLETE",
              "all 27^4=531,441 consts x all canonical seeds, <=3 laws in 5 cells",
              c22, F.all_seeds(4, 5, 3), mode)
    block("E2 2+2 [1,0,3,2] <=4laws/6cells", "COMPLETE",
          "all 27^4=531,441 consts x all canonical seeds, <=4 laws in 6 cells",
          c22, F.all_seeds(4, 6, 4), "parity")
    del c4, c22

    # --- L=5 and L=6 cycles, sampled --------------------------------------
    rng = np.random.default_rng(20260826)
    for L in (5, 6):
        cs = sample_consts(L, [(i + 1) % L for i in range(L)], 60000, rng)
        block("E2 L=%d cycle <=4laws/6cells" % L, "SAMPLE",
              "60,000 consts drawn uniformly from 27^%d (numpy PCG64 seed "
              "20260826) x all canonical seeds, <=4 laws in 6 cells" % L,
              cs, F.all_seeds(L, 6, 4), "parity")


def task3():
    print("\n=== TASK 3 — E1 supersession (attack on Theorem B) ===")
    for mode in ("super", "super_or"):
        block("SUP n=1 <=6laws/8cells", "COMPLETE",
              "all 27 consts x all canonical seeds, <=6 laws in 8 cells",
              super_consts(1), F.all_seeds(1, 8, 6), mode)
        block("SUP n=2 <=6laws/8cells", "COMPLETE",
              "all 27^2=729 consts x all canonical seeds, <=6 laws in 8 cells",
              super_consts(2), F.all_seeds(2, 8, 6), mode)
        block("SUP n=2 <=7laws/9cells", "COMPLETE",
              "all 27^2=729 consts x all canonical seeds, <=7 laws in 9 cells",
              super_consts(2), F.all_seeds(2, 9, 7), mode)
    c3 = super_consts(3)
    for mode in ("super", "super_or"):
        block("SUP n=3 <=4laws/6cells", "COMPLETE",
              "all 27^3=19,683 consts x all canonical seeds, <=4 laws in 6 cells",
              c3, F.all_seeds(3, 6, 4), mode)
        block("SUP n=3 <=5laws/7cells", "COMPLETE",
              "all 27^3=19,683 consts x all canonical seeds, <=5 laws in 7 cells",
              c3, F.all_seeds(3, 7, 5), mode)
    del c3
    c4 = super_consts(4)
    for mode in ("super", "super_or"):
        block("SUP n=4 <=4laws/6cells", "COMPLETE",
              "all 27^4=531,441 consts x all canonical seeds, <=4 laws in 6 cells",
              c4, F.all_seeds(4, 6, 4), mode)
    del c4
    rng = np.random.default_rng(11235)
    c4s = sample_consts(4, list(range(4)), 30000, rng)
    for mode in ("super", "super_or"):
        block("SUP n=4 <=5laws/7cells", "SAMPLE",
              "30,000 consts drawn uniformly from 27^4 (numpy PCG64 seed 11235)"
              " x all canonical seeds, <=5 laws in 7 cells",
              c4s, F.all_seeds(4, 7, 5), mode)
    for n in (5, 6):
        cs = sample_consts(n, list(range(n)), 40000, rng)
        for mode in ("super", "super_or"):
            block("SUP n=%d <=4laws/6cells" % n, "SAMPLE",
                  "40,000 consts drawn uniformly from 27^%d (numpy PCG64 seed "
                  "11235, continued) x all canonical seeds, <=4 laws in 6 cells" % n,
                  cs, F.all_seeds(n, 6, 4), mode)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    t0 = time.time()
    if which in ("all", "2"):
        task2()
    if which in ("all", "3"):
        task3()
    tot = sum(b["runs"] for b in BLOCKS)
    gl = sum(b["hist"]["GLIDER"] for b in BLOCKS)
    print("\nTOTAL: %d blocks, %s (constitution x seed) runs, %.1f min, "
          "GLIDERS = %d" % (len(BLOCKS), f"{tot:,}", (time.time() - t0) / 60, gl))
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    with open(os.path.join(HERE, "data", "census_%s.json" % which), "w") as f:
        json.dump(BLOCKS, f, indent=1)
