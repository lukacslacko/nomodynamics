#!/usr/bin/env python3
"""ref_odo_reach.py -- REFEREE: the PUBLISHED Odometer's reach out to t = 2^20.

Published (xamend2d/RESULTS.md headline 9 + Sec 11.2): heights
20, 26, 38, 44, 47, 50, 74, 86 at k = 10, 12, 14, 15, 16, 17, 19, 20.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, card

XA = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
      "P": (1, 1), "Q": (-1, 1), "R": (1, -1), "T": (-1, -1)}
ODO = Const([tuple(XA[c] for c in "OEW"), tuple(XA[c] for c in "NQR")],
            [(1,), (0, 1)], dim=2)
SEED = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])

T = 1 << 20
S = dict(SEED)
rows = []
for t in range(T + 1):
    if t and (t & (t - 1)) == 0:
        ys = [c[1] for c in S]
        xs = [c[0] for c in S]
        rows.append((t.bit_length() - 1, card(S), max(ys) - min(ys) + 1,
                     max(xs) - min(xs) + 1, min(ys), max(ys)))
    S = step(S, ODO)
print("k  card  height  width  ymin ymax")
for r in rows:
    print("%2d  %4d  %6d  %5d  %4d %4d" % r)
pub = {10: 20, 12: 26, 14: 38, 15: 44, 16: 47, 17: 50, 19: 74, 20: 86}
h = {r[0]: r[2] for r in rows}
print("\npublished vs measured height:")
for k in sorted(pub):
    print("  k=%2d published %3d  measured %3d  %s"
          % (k, pub[k], h.get(k), "MATCH" if h.get(k) == pub[k] else "DIFFER"))
