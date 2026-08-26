#!/usr/bin/env python3
"""
t4_zbox.py -- TARGET 4: a belt-and-braces bounded glider search on Z for the
out-degree-1 counterexample constitutions.

The Out-Degree Law (Expedition X-E) already proves that a constitution whose
used kinds all amend at most one kind carries no free glider on Z.  This is an
independent confirmation inside an explicitly stated BOX: every code whose
support fits in a window of `span` cells, every p <= PMAX, every |d| <= p.

Z is simulated as a ring Z/M with M large enough that the orbit cannot wrap
(Lemma W: correspondence holds while the support stays inside an interval of
m - 2W cells), and the run is aborted the moment the support could reach the
seam -- so a "glider" reported here is a genuine Z glider.
"""

from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from t4_ring import Ring

M = 64
PMAX = 8


def scan(rules, targets, mode="parity", span=9, pmax=PMAX, base=20):
    """All codes with support in [base, base+span-1]; report Z gliders."""
    R = Ring(rules, targets, M, mode)
    n = len(rules)
    hits = []
    tried = 0
    for bits in itertools.product(range(1 << n), repeat=span):
        X = [0] * n
        for j, b in enumerate(bits):
            for k in range(n):
                if (b >> k) & 1:
                    X[k] |= 1 << (base + j)
        X = tuple(X)
        if not any(X):
            continue
        tried += 1
        Y = X
        lo, hi = base, base + span - 1
        for p in range(1, pmax + 1):
            Y = R.step(Y)
            lo -= 1
            hi += 1
            if lo < 2 or hi > M - 3:          # the orbit could reach the seam
                break
            for d in range(-p, p + 1):
                if d == 0:
                    continue
                if Y == R.rot_state(X, d):
                    hits.append((X, p, d))
    return tried, hits


CASES = [
    ("SP  (own-kind (0,-1,1))", [(0, -1, 1)], [(0,)], "parity"),
    ("SP  (own-kind (0,1,-1))", [(0, 1, -1)], [(0,)], "parity"),
    ("DUET-8   X:(-1,1,-1)->X  Y:(0,-1,1)->X", [(-1, 1, -1), (0, -1, 1)],
     [(0,), (0,)], "parity"),
    ("DUET-8b  X:(0,-1,1)->X   Y:(0,-1,0)->X", [(0, -1, 1), (0, -1, 0)],
     [(0,), (0,)], "parity"),
    ("TANDEM-1 X:(0,-1,1)->XY  Y:(0,-1,0)->XY  [out-degree 2, control]",
     [(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)], "parity"),
    ("HOLE     X:(0,-1,0)->XY  Y:(0,-1,-1)->XY [out-degree 2, control]",
     [(0, -1, 0), (0, -1, -1)], [(0, 1), (0, 1)], "parity"),
]


if __name__ == "__main__":
    span = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    print("BOX: every code with support in a window of %d cells, "
          "1 <= p <= %d, 1 <= |d| <= p, on Z (simulated on Z/%d, aborted "
          "before the seam)\n" % (span, PMAX, M))
    for name, rules, targets, mode in CASES:
        n = len(rules)
        tried, hits = scan(rules, targets, mode, span)
        sigs = sorted({(p, d) for _, p, d in hits})
        print("%-58s codes %-9d gliders %-7d (p,d) seen: %s"
              % (name, tried, len(hits), sigs[:8]))
