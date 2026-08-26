#!/usr/bin/env python3
"""
t4_specimens.py -- TARGET 4: the gallery, every frame re-certified.

  TANDEM-1  the light-cone-admissible odd-ring rotor (out-degree 2) that DOES
            lift: Phi(S) = rot_1(S) on every ring m >= 3, and the same code on
            Z is a free glider of period 1 and displacement +1.

  SP-m      THE COUNTEREXAMPLE TO THE NAIVE CONVERSE.  Own-kind -- out-degree
            ONE -- codes on Z/10, Z/18, Z/20, Z/22 that are strictly
            light-cone-admissible rotors.  By the Anchor Theorem (equivalently
            the Out-Degree Law) their constitutions carry no finite Z glider at
            all, so these rotors are not the wrapping of anything.  They are
            exactly the Sunset Parliament's record cycles.

  HOLE      An out-degree-2 light-cone-admissible rotor with vacant arc 1: the
            code is the whole ring minus one cell and the HOLE advances.  Its
            rotation d = +1 is outside the tropical interval [-p, 0] of its own
            amendment digraph, so no Z glider of that constitution can have it.

  O-15      the first odd-ring rotor of Expedition X-C: p = 1, r = 5.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xnomos
from t4_ring import (Ring, rotor_certificate, verify_rotation_recurrence,
                     verify_via_xnomos, vacant_arc)
from t4_lift import lift_report, zconst, o15, dense_family, dense_all_lifts
from t4_analyze import cycle_means

W = 1


def certify(name, rules, targets, m, X, mode="parity", frames=None,
            comment=""):
    R = Ring(rules, targets, m, mode)
    c = rotor_certificate(X, R)
    assert c is not None, name
    p, d = c["p"], c["d"]
    ok1 = verify_rotation_recurrence(X, R, p, d, laps=3)
    ok2 = verify_via_xnomos(X, R, p, d, laps=3)
    g = vacant_arc(R.occ(X), m)
    used = set()
    Y, seen = X, set()
    L = 0
    while Y not in seen:
        seen.add(Y)
        L += 1
        for k in range(R.n):
            if Y[k]:
                used.add(k)
        Y = R.step(Y)
    od = max(len(targets[k]) for k in used)
    lo, hi = cycle_means(rules, targets, used)
    ta = None
    if lo is not None:
        a, b = p * min(lo, 0), p * max(hi, 0)
        ta = any(a <= e <= b for e in (d, d - m, d + m))
    rep = lift_report(R, X, p, d)
    print("\n### %s   %s" % (name, comment))
    print("constitution: %s   targets %s   [%s, ring Z/%d]"
          % (rules, [list(t) for t in targets], mode, m))
    print("Phi^%d(S) = rot_%+d(S)   laws = %d   orbit length %d   "
          "rot_d(S) != S : %s" % (p, d, R.card(X), L, not c["sym"]))
    print("re-certified 3 full periods: ring engine %s, xnomos %s"
          % (ok1, ok2))
    print("light cone |d| <= pW : %s   (2pW = %d %s m = %d, so the "
          "representative is %s)"
          % (abs(d) <= p * W, 2 * p * W, "<" if 2 * p * W < m else ">=", m,
             "unique" if 2 * p * W < m else "NOT unique -- test vacuous"))
    print("tropical interval [%s, %s] contains a representative of d : %s"
          % (p * min(lo, 0) if lo is not None else "-",
             p * max(hi, 0) if lo is not None else "-", ta))
    print("out-degree used = %d   vacant arc g = %d   (Lift Theorem needs "
          "g >= 2pW = %d : %s)" % (od, g, 2 * p * W, g >= 2 * p * W))
    print("cut-lift on Z: correspondence %s, Phi_Z^p(T) = sigma^d(T) : %s, "
          "xnomos classify %s" % (rep.get("correspondence"), rep.get("glides"),
                                  rep["classify"]))
    Y = X
    for t in range((frames or p) + 1):
        print("  t=%-2d %s" % (t, R.render(Y)))
        Y = R.step(Y)
    return c


SP = {
    10: ((0, -1, 1), (0b1010101011,)),
    18: ((0, -1, 1), (0b010101010101010111,)),
    20: ((0, -1, 1), None),
    22: ((0, -1, 1), None),
}


if __name__ == "__main__":
    certify("TANDEM-1 on Z/7", [(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)],
            7, (1, 1), frames=3,
            comment="-- lifts: the SAME code on Z is a free glider (p=1,d=+1)")

    # DUO-6: X at {0}, Y at {1,3,5}
    certify("DUO-6  (THE SMALLEST COUNTEREXAMPLE)", [(0, -1, 1), (0, -1, 0)],
            [(0,), (0,)], 6, (0b000001, 0b101010), frames=3,
            comment="-- 4 laws, out-degree 1, strictly light-cone-admissible; "
                    "the smallest ring that carries one")

    # SP-10: state 683 = 0b1010101011 = cells {0,1,3,5,7,9}
    certify("SP-10  (THE COUNTEREXAMPLE)", [(0, -1, 1)], [(0,)], 10, (683,),
            frames=4,
            comment="-- own-kind, out-degree 1, strictly light-cone-admissible")
    certify("SP-18", [(0, -1, 1)], [(0,)], 18, (87383,), frames=8,
            comment="-- the Sunset Parliament's 63-cycle is a rot_-2 rotor")
    certify("SP-22", [(0, -1, 1)], [(0,)], 22, None or (2796203,), frames=2,
            comment="-- the 341-cycle; 2pW = 62 > 22, light cone vacuous here")

    # X at cells {0,1,2,4,6}; Y at cells {0,2,4,6}   (packed state 21847)
    certify("DUET-8  (THE SHARPEST COUNTEREXAMPLE)",
            [(-1, 1, -1), (0, -1, 1)], [(0,), (0,)], 8, (87, 85), frames=3,
            comment="-- out-degree 1, strictly light-cone-admissible, "
                    "SATURATING its own tropical bound (-1 per step), and "
                    "rotationally aperiodic")
    # a second one, out-degree 1, inside the tropical interval [0,3]
    certify("DUET-8b", [(0, -1, 1), (0, -1, 0)], [(0,), (0,)], 8, (17, 85),
            frames=4,
            comment="-- out-degree 1, LC and tropical, but rot_4-symmetric")

    certify("HOLE-7", [(0, -1, 0), (0, -1, -1)], [(0, 1), (0, 1)], 7,
            ((1 << 7) - 2, (1 << 7) - 2), frames=3,
            comment="-- out-degree 2, g = 1, rotation +1 outside the tropical "
                    "interval")
    print()
    o15()
    print("\n=== the Sunset-Parliament rotor family: L = p * (m/|d|) ===")
    for m, p, d, st in ((10, 3, -2, 683), (18, 7, -2, 87383),
                        (20, 6, -4, None), (22, 31, -2, 2796203)):
        if st is None:
            continue
        R = Ring([(0, -1, 1)], [(0,)], m, "parity")
        X = (st,)
        c = rotor_certificate(X, R)
        Y, seen = X, set()
        while Y not in seen:
            seen.add(Y)
            Y = R.step(Y)
        L = len(seen)
        print("  m=%-3d p=%-3d d=%+d  orbit length %-4d = p * m/|d| = %d  "
              "(Sunset Parliament maximum at this m)"
              % (m, c["p"], c["d"], L, c["p"] * m // abs(c["d"])))
