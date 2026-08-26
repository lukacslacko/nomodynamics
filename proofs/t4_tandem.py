#!/usr/bin/env python3
"""
t4_tandem.py -- TARGET 4 (a): TANDEM-1 is a light-cone-admissible ring rotor.

TANDEM-1:  rules  X:(0,-1,1)  Y:(0,-1,0),  both amending {X,Y}   (out-degree 2)
seed    :  both kinds in a SINGLE cell.

Claim to verify, by an independent code path (t4_ring, cross-checked against
xnomos in t4_ring.crosscheck), on rings m = 3,5,7,9,15,21 and even controls:

    Phi(S) = rot_1(S)  exactly,  p = 1, d = +1,  rot_1(S) != S,
    hence min(d, m-d) = 1 <= p*W = 1  -- light-cone-admissible in the strict
    (glider-speed) sense, and a fortiori in the X-C information sense (<= 2pW).

Also: the same seed on Z is a genuine free glider (p=1, d=+1), certified by
xnomos.classify / xnomos.verify_glider.
"""

from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xnomos
from t4_ring import (Ring, rotor_certificate, verify_rotation_recurrence,
                     verify_via_xnomos, vacant_arc, rep)

RULES = [(0, -1, 1), (0, -1, 0)]
TARGETS = [(0, 1), (0, 1)]
W = 1


def certificate(m, mode="parity", verbose=True):
    R = Ring(RULES, TARGETS, m, mode)
    X0 = (1, 1)                                   # both kinds in cell 0
    cert = rotor_certificate(X0, R)
    assert cert is not None, m
    p, d, sym = cert["p"], cert["d"], cert["sym"]
    ok_ring = verify_rotation_recurrence(X0, R, p, d, laps=3)
    ok_xnom = verify_via_xnomos(X0, R, p, d, laps=3)
    # exhaustive: rot_d(S) != S for every d != 0 (stabiliser is trivial)
    stab = [d2 for d2 in range(1, m) if R.rot_state(X0, d2) == X0]
    # every step of one full lap, explicitly
    frames = []
    X = X0
    for _ in range(min(m, 6) + 1):
        frames.append(R.render(X))
        X = R.step(X)
    g = vacant_arc(R.occ(X0), m)
    lc_strict = min(abs(d), m - abs(d)) <= p * W
    lc_xc = min(abs(d), m - abs(d)) <= 2 * p * W
    if verbose:
        print("m=%-3d p=%d d=%+d  sym=%s stab=%s  vacant arc g=%d (need 2pW=%d)"
              " | ring-check=%s xnomos-check=%s | LC(<=pW)=%s LC(<=2pW)=%s"
              % (m, p, d, sym, stab, g, 2 * p * W, ok_ring, ok_xnom,
                 lc_strict, lc_xc))
    return {"m": m, "p": p, "d": d, "sym": sym, "stab": stab, "g": g,
            "ok_ring": ok_ring, "ok_xnomos": ok_xnom,
            "lc_strict": lc_strict, "lc_xc": lc_xc, "frames": frames}


def zeta():
    """The same seed on Z: a free glider, p=1, d=+1."""
    C = xnomos.Const(RULES, TARGETS)
    S = xnomos.state_of([(0, 0), (0, 1)])
    res = xnomos.classify(S, C)
    ok = xnomos.verify_glider(S, C, 1, 1)
    return res, ok


def out_degree_used(R, X0):
    """Max |targets[k]| over the kinds that actually appear in the orbit."""
    used, X, seen = set(), X0, set()
    while X not in seen:
        seen.add(X)
        for k in range(R.n):
            if X[k]:
                used.add(k)
        X = R.step(X)
    return max(len(R.targets[k]) for k in used), sorted(used)


if __name__ == "__main__":
    print("TANDEM-1  rules=%s  targets=%s  (out-degree 2)\n" % (RULES, TARGETS))
    odd = [3, 5, 7, 9, 15, 21]
    even = [4, 6, 8, 10, 12, 16, 22]
    print("--- odd rings ---")
    for m in odd:
        certificate(m)
    print("--- even rings (contrast) ---")
    for m in even:
        certificate(m)
    print("--- a longer sweep, every m from 3 to 60 ---")
    bad = []
    for m in range(3, 61):
        c = certificate(m, verbose=False)
        if not (c["p"] == 1 and c["d"] == 1 and not c["sym"]
                and c["ok_ring"] and c["ok_xnomos"] and c["lc_strict"]):
            bad.append(m)
    print("m = 3..60 : %d rings, all with (p,d)=(1,+1), failures = %s"
          % (58, bad))
    print("--- also under OR resolution ---")
    for m in (3, 5, 7, 9, 15, 21):
        certificate(m, mode="or")
    print("--- spacetime, Z/7 ---")
    for row in certificate(7, verbose=False)["frames"]:
        print("  " + row)
    print("--- out-degree actually used ---")
    R = Ring(RULES, TARGETS, 7, "parity")
    print("  ", out_degree_used(R, (1, 1)))
    print("--- the same seed released on Z ---")
    res, ok = zeta()
    print("   xnomos.classify:", {k: v for k, v in res.items()
                                  if k != "history"},
          " verify_glider(p=1,d=1):", ok)
