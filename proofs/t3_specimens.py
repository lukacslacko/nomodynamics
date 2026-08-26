#!/usr/bin/env python3
"""
t3_specimens.py -- every TARGET-3 specimen, re-certified through the reference
engine `xnomos` alone (no expedition code in the certification path).

Each specimen is a SINGLE-FIELD constitution at window W = 1: every kind amends
every kind, so the code is one bit per cell.  For each we check

  * xnomos.verify_glider  : Phi^p(S) = sigma^d(S) over THREE full periods
  * xnomos.classify       : independently reports the MINIMAL period and the
                            displacement per minimal period

The last column is the pair (p0, d0) that generates
G(S) = {(t,x) : Phi^t S = sigma^x S}; the published Single-Field Cap says
|d0| <= 2 (parity) / <= 1 (OR at two kinds).
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import xnomos                                                    # noqa: E402

SPECIMENS = [
    # name, rules, seed cells, p, d, mode, note
    ("CONVEYOR (2 kinds)", [(0, -1, 0), (0, 1, 1)],
     [0, 1, 2, 5, 7, 8], 1, 1, "parity",
     "Phi = sigma EXACTLY, in BOTH resolutions: every finite code is a "
     "glider"),
    ("CONVEYOR under OR", [(0, -1, 0), (0, 1, 1)],
     [0, 1, 2, 5, 7, 8], 1, 1, "or", "the same, OR resolution"),
    ("MIRROR-2/5 (X-E, replicated)", [(0, 1, -1), (0, -1, 1)],
     [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21], 5, 2, "parity",
     "the published two-kind d=2 glider"),
    ("TRIAD-3/3  (3 kinds!)", [(1, -1, 0), (-1, 1, -1), (-1, 1, 1)],
     [0, 1, 2, 3, 4], 4, 4, "parity",
     "three kinds, |d0| = 4 -- twice the published n=3 cap of 2"),
    ("STEP-3/3  (4 kinds)",
     [(-1, 1, -1), (1, -1, 0), (0, 1, 1), (1, -1, 1)], [0, 1], 3, 3, "parity",
     "four kinds, one field, |d0| = 3"),
    ("STEP-3/3-OR (4 kinds)",
     [(-1, 1, 1), (0, -1, 1), (0, 1, -1), (1, -1, 0)], [0, 1], 3, 3, "or",
     "the same refutation under OR resolution"),
    ("QUINT-3/5 (5 kinds, ONE cell)",
     [(0, -1, 0), (0, -1, 1), (0, 1, -1), (0, 1, 0), (0, 1, 1)],
     [0], 5, 3, "parity",
     "speed 3/5, gcd(p,d)=1 so minimality is automatic"),
    ("QUINT-5/5 (5 kinds, ONE cell)",
     [(0, -1, 0), (0, -1, 1), (0, 1, 0), (-1, 1, -1), (-1, 1, 1)],
     [0], 5, 5, "parity", "one cell, minimal period 5, displacement 5"),
    ("SEPTET-7/7 (5 kinds, TWO cells)",
     [(0, -1, 0), (0, -1, 1), (0, 1, -1), (0, 1, 0), (-1, 1, 1)],
     [0, 6], 7, 7, "parity", "two cells, minimal period 7, displacement 7"),
    ("HALFTONE-32 (4 kinds, FOUR cells)",
     [(0, -1, 0), (0, 1, -1), (0, 1, 0), (0, 1, 1)],
     [0, 1, 6, 8], 32, 32, "parity",
     "four kinds, four cells, |d0| = 32"),
    ("ODOMETER-64 (4 kinds, SEVEN cells)",
     [(0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 1, 0)],
     [0, 2, 3, 6, 7, 9, 10], 64, -64, "parity",
     "four kinds, seven cells, |d0| = 64 -- 32x the published cap"),
    ("ODOMETER-128 (4 kinds, 14 cells)",
     [(0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 1, 0)],
     [0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15], 128, -128, "parity",
     "the parity record found here: |d0| = 128 at W = 1"),
    ("OR-ODOMETER-16 (3 kinds!)",
     [(0, -1, -1), (-1, 1, 0), (1, -1, 0)],
     [0, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14], 16, -16, "or",
     "THREE kinds under OR, |d0| = 16 -- 16x the published OR cap"),
]


def const(rules):
    n = len(rules)
    return xnomos.Const(rules, [tuple(range(n))] * n), n


def check(name, rules, cells, p, d, mode, note, show=0):
    C, n = const(rules)
    S = {c: (1 << n) - 1 for c in cells}
    ok = xnomos.verify_glider(dict(S), C, p, d, mode)
    cl = xnomos.classify(dict(S), C, mode, max_steps=6 * abs(p) + 40)
    p0 = cl.get("period")
    d0 = cl.get("displacement")
    good = (ok and cl["kind"] == "GLIDER" and p0 == p and d0 == d)
    print("%-32s n=%d  W=1  %-6s  (p0,d0)=(%3d,%4d)  verify=%s classify=%s %s"
          % (name, n, mode, p, d, ok, cl["kind"], "OK" if good else "***FAIL***"))
    print("      rules %s   seed %s" % (rules, cells))
    print("      %s" % note)
    if show:
        for r in xnomos.spacetime(dict(S), C, show, mode,
                                  lo=min(cells) - 4, hi=max(cells) + 6):
            print("        " + r)
    assert good, name
    return good


def main():
    print("TARGET 3 -- single-field specimens, certified by xnomos alone\n")
    for sp in SPECIMENS:
        check(*sp, show=(6 if sp[0].startswith(("CONVEYOR (", "TRIAD",
                                                "STEP-3/3-OR")) else 0))
        print()

    # the CONVEYOR is a theorem, not a specimen: Phi = sigma on EVERY code
    print("CONVEYOR, the whole theorem: Phi(S) = S+1 for every finite code")
    import random
    rng = random.Random(0)
    C, n = const([(0, -1, 0), (0, 1, 1)])
    bad = 0
    for _ in range(2000):
        cells = {rng.randrange(-12, 13) for _ in range(rng.randrange(1, 12))}
        X = {c: (1 << n) - 1 for c in cells}
        for mode in ("parity", "or"):
            if xnomos.step(X, C, mode) != {c + 1: (1 << n) - 1 for c in cells}:
                bad += 1
    print("   2000 random codes x 2 resolutions, %d exceptions to Phi = "
          "sigma\n" % bad)
    assert bad == 0

    # dilation: the same objects at every window
    print("Dilation: the W=1 record carried to larger windows")
    rules = [(0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 1, 0)]
    cells = [0, 2, 3, 6, 7, 9, 10]
    n = 4
    for r in (2, 3):
        ru = [tuple(r * x for x in c) for c in rules]
        Cr = xnomos.Const(ru, [tuple(range(n))] * n)
        S = {r * c: (1 << n) - 1 for c in cells}
        ok = xnomos.verify_glider(dict(S), Cr, 64, -64 * r, "parity")
        cl = xnomos.classify(dict(S), Cr, "parity", max_steps=420)
        print("   r=%d -> W=%d, single field, (p0,d0)=(64,%d)  verify=%s "
              "classify p=%s d=%s" % (r, r, -64 * r, ok, cl.get("period"),
                                      cl.get("displacement")))
        assert ok and cl["period"] == 64 and cl["displacement"] == -64 * r
    print("\nALL SPECIMENS CERTIFIED")


if __name__ == "__main__":
    main()
