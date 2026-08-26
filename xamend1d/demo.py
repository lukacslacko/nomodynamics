#!/usr/bin/env python3
"""
demo.py — the specimen gallery of Expedition X-A, re-verified from scratch.

    python3 demo.py

Every specimen below is re-run through the shared engine `xnomos.py` and
re-certified by `xnomos.verify_glider` (three full periods) at display time.
Nothing here is quoted from a log.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import xnomos
from xnomos import Const, state_of, verify_glider, classify, spacetime


SPECIMENS = [
    dict(name="TANDEM-1  — the minimal cross-amendment glider",
         blurb="2 placed laws in ONE cell.  A enacts the pair one cell ahead;\n"
               "  B repeals the pair where it stands.  Speed 1 = the maximum.",
         rules=[(0, -1, 1), (0, -1, 0)], targets=[(0, 1), (0, 1)],
         seed=[(1, 0), (1, 1)], p=1, d=1, mode="parity", win=(0, 9), steps=6),
    dict(name="DOUBLET   — the caterpillar, realised",
         blurb="Two adjacent cells.  The leading law enacts the pair one cell on;\n"
               "  its partner repeals the pair at the TRAILING end.  Moves left.",
         rules=[(1, -1, 1), (0, -1, -1)], targets=[(0, 1), (0, 1)],
         seed=[(6, 0), (6, 1), (7, 0), (7, 1)], p=1, d=-1,
         mode="parity", win=(0, 9), steps=6),
    dict(name="TRIPTYCH  — a glider under PARITY that dies under OR",
         blurb="Author multiplicity 2: two kinds toggle the same slot, and the\n"
               "  parity cancellation is load-bearing.  OR diverges at t = 1.",
         rules=[(0, 1, 0), (0, -1, 1), (0, 1, -1)],
         targets=[(0, 1, 2), (0, 1, 2), (0, 1, 2)],
         seed=[(1, k) for k in range(3)] + [(2, k) for k in range(3)]
              + [(4, k) for k in range(3)],
         p=1, d=1, mode="parity", win=(0, 11), steps=5, show_or=True),
    dict(name="SOLO — the smallest glider there is: ONE placed law",
         blurb="Fully cross (no law amends its own kind). The lone kind-0 law enacts\n"
               "  kinds 1 and 2 on its own cell; they re-enact kind 0 one cell right\n"
               "  and clear the pair.  Period 2, displacement 1.",
         rules=[(0, 1, 0), (0, 1, 1), (0, 1, 0)],
         targets=[(1, 2), (0,), (0,)],
         seed=[(1, 0)], p=2, d=1, mode="parity", win=(0, 9), steps=7),
    dict(name="QUADRILLE — a FULLY-CROSS glider (no law amends its own kind)",
         blurb="Kinds 0,1 (c=0) between them toggle all four kinds in place, clearing\n"
               "  the cell; kinds 2,3 (c=-1) between them re-enact all four one cell on.",
         rules=[(0, 1, 0), (0, 1, 0), (0, 1, -1), (0, 1, -1)],
         targets=[(1, 2), (0, 3), (1, 3), (0, 2)],
         seed=[(7, k) for k in range(4)], p=1, d=-1,
         mode="parity", win=(0, 9), steps=6),
    dict(name="DRIFTER-1/3 — a slow, phase-changing glider",
         blurb="Breathes one cell / two cells / one cell, then hops.  Period 3,\n"
               "  displacement 1: no single step is a translation.",
         rules=[(-1, 1, -1), (0, -1, 1), (0, -1, 0)],
         targets=[(0, 2), (0, 1), (1, 2)],
         seed=[(1, 0), (1, 1)], p=3, d=1, mode="parity", win=(0, 9), steps=8),
    dict(name="SPEED-2/3 — a non-unit-numerator speed",
         blurb="Three-phase gait A -> # -> ## -> A, advancing 2 cells per 3 steps.\n"
               "  (Three kinds also suffice for 2/3; this 4-kind one is just the\n"
               "  cleanest gait.  At n=2 only speed 1 exists at all.)",
         rules=[(0, 1, 0), (-1, 1, 1), (0, 1, 1), (-1, 1, -1)],
         targets=[(0, 1, 2, 3), (1, 2, 3), (0, 1, 2, 3), (1, 2, 3)],
         seed=[(1, 0)], p=3, d=2, mode="parity", win=(0, 13), steps=10),
]


def show(sp):
    C = Const(sp["rules"], list(sp["targets"]))
    S = state_of(sp["seed"])
    ok = verify_glider(S, C, sp["p"], sp["d"], sp["mode"])
    cls = classify(S, C, sp["mode"])
    print("\n" + "=" * 72)
    print(sp["name"])
    print("  " + sp["blurb"])
    print("  rules   = %s" % (sp["rules"],))
    print("  targets = %s" % ([list(t) for t in sp["targets"]],))
    print("  seed    = xnomos.state_of(%s)" % (sp["seed"],))
    print("  period p = %d   displacement d = %+d   speed |d|/p = %s"
          % (sp["p"], sp["d"], "%d/%d" % (abs(sp["d"]), sp["p"])))
    lo, hi = sp["win"]
    for t, row in enumerate(spacetime(S, C, sp["steps"], sp["mode"], lo, hi)):
        print("    t=%-2d %s" % (t, row))
    print("  xnomos.classify        : %s (period %s, displacement %s)"
          % (cls["kind"], cls.get("period"), cls.get("displacement")))
    print("  verify_glider (3 periods): %s" % ("PASS" if ok else "FAIL"))
    assert ok, sp["name"]
    if sp.get("show_or"):
        ok2 = verify_glider(S, C, sp["p"], sp["d"], "or")
        print("  under OR-toggle resolution:")
        for t, row in enumerate(spacetime(S, C, sp["steps"], "or", lo, hi)):
            print("    t=%-2d %s" % (t, row))
        print("  verify_glider under OR  : %s  <-- the resolution axis decides"
              % ("PASS" if ok2 else "FAIL"))
        assert not ok2


def lifts():
    print("\n" + "=" * 72)
    print("TANDEM-1 LIFTS")
    for name, v in (("2-D, axis   ", (1, 0)), ("2-D, diagonal", (1, 1)),
                    ("2-D, knight ", (2, 1))):
        C = Const([((0, 0), (-1, 0), v), ((0, 0), (-1, 0), (0, 0))],
                  [(0, 1), (0, 1)], dim=2)
        S = state_of([((0, 0), 0), ((0, 0), 1)])
        print("  %s v=%-7s verify_glider = %s"
              % (name, v, verify_glider(S, C, 1, v)))
    print("  rings (own-kind rotors need EVEN m >= 6; this one needs nothing):")
    for m in range(3, 9):
        C = Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)], modulus=m)
        S = state_of([(0, 0), (0, 1)])
        T = dict(S)
        ok = True
        for t in range(1, 3 * m + 1):
            T = xnomos.step(T, C)
            if T != state_of([(t % m, 0), (t % m, 1)]):
                ok = False
                break
        print("    Z/%-2d rotates one cell per step, 3 laps: %s" % (m, ok))


def puffer():
    """PICKET PUFFER — a moving periodic front laying a periodic wake.

    Not a glider: the population grows and the tail is welded to the origin.
    """
    print("\n" + "=" * 72)
    print("PICKET PUFFER — motion the Phi^p = sigma^d definition does NOT catch")
    C = Const([(0, 1, 1), (0, -1, 1)], [(0, 1), (0, 1)])
    S = state_of([(0, 0), (5, 1)])
    print("  rules   = [(0,1,1), (0,-1,1)]   targets = [{0,1},{0,1}]")
    print("  seed    = two placed laws: %s" % sorted(S.items()))
    T = dict(S)
    for t in range(21):
        if t % 4 == 0:
            print("    t=%-2d |%s|" % (t, xnomos.render(T, None, 0, 30)))
        T = xnomos.step(T, C, "or")
    # independent certification of what it does and does not satisfy
    T, hist = dict(S), []
    for t in range(200):
        hi = max(T)
        hist.append((hi, xnomos.card(T),
                     frozenset((c - hi, m) for c, m in T.items() if c > hi - 28)))
        T = xnomos.step(T, C, "or")
    per = all(hist[t][2] == hist[t + 4][2] for t in range(60, 180))
    adv = all(hist[t + 4][0] - hist[t][0] == 4 for t in range(60, 180))
    glid = any(verify_glider(S, C, p, d, "or")
               for p in range(1, 9) for d in range(-8, 9) if d)
    print("  front window p=4 periodic (t=60..180) : %s" % per)
    print("  front advances +4 per 4 steps (speed 1): %s" % adv)
    print("  population growth                     : %d -> %d laws (t=70 -> 139)"
          % (hist[70][1], hist[139][1]))
    print("  is it a glider (verify_glider, any p<=8,|d|<=8)? %s" % glid)
    assert per and adv and not glid


if __name__ == "__main__":
    for sp in SPECIMENS:
        show(sp)
    puffer()
    lifts()
    print("\n" + "=" * 72)
    print("All specimens re-verified by xnomos.verify_glider over 3 full periods.")
