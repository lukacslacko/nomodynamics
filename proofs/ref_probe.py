#!/usr/bin/env python3
"""ref_probe.py -- REFEREE: (a) the real Odometer's column/row structure,
(b) the actual error of the published 0.20(log2 t)^2 fit,
(c) max per weight class inside a 17-bit window for w = 15,16,17."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, card, laws, active_laws

XA = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
      "P": (1, 1), "Q": (-1, 1), "R": (1, -1), "T": (-1, -1)}
ODO = Const([tuple(XA[c] for c in "OEW"), tuple(XA[c] for c in "NQR")],
            [(1,), (0, 1)], dim=2)
SEED = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])

print("== the PUBLISHED Odometer: structure ==")
S = dict(SEED)
cols = set()
perm = None
maxy = -10 ** 9
for t in range(1 << 14):
    cur = {(c, k) for c, k in laws(S)}
    perm = set(cur) if perm is None else (perm & cur)
    for c in S:
        cols.add(c[0])
    maxy = max(maxy, max(c[1] for c in S))
    S = step(S, ODO)
print("  columns ever occupied, t < 2^14:", sorted(cols))
print("  max y ever:", maxy)
print("  laws standing at EVERY t < 2^14:", sorted(perm))
print("  (so 'no cell with x not in {0,1} or y<0 is ever occupied' and")
print("   '(1,1) is never occupied' are both FALSE for this specimen)")

print("\n== the published fit 0.20 (log2 t)^2, error per k ==")
pub = {10: 20, 12: 26, 14: 38, 15: 44, 16: 47, 17: 50, 19: 74, 20: 86}
for k in sorted(pub):
    f = 0.20 * k * k
    print("   k=%2d  measured %3d   0.20k^2 = %6.2f   error %+6.1f%%"
          % (k, pub[k], f, 100 * (f - pub[k]) / pub[k]))

print("\n== Jubilee max per weight class inside a 17-bit window ==")


def extremes(B):
    st = {0: (0, 0), 1: (1, 1)}
    j = 0
    while 2 * j + 1 <= B - 1:
        hi = 2 * j + 2 <= B - 1
        new = defaultdict(lambda: (10 ** 18, -1))
        for w, (mn, mx) in st.items():
            opts = [(0, lambda F: F), (1, lambda F: F + 1)]
            if hi:
                opts.append((2, lambda F: 2 * F + 2))
            for dw, g in opts:
                a, b = new[w + dw]
                new[w + dw] = (min(a, g(mn)), max(b, g(mx)))
        st = dict(new)
        j += 1
    return st


st = extremes(17)
for w in range(1, 18):
    fm = (1 << (w // 2 + 1)) + 1 if w % 2 == 0 else 3 * (1 << ((w - 1) // 2)) + 1
    got = st[w][1] + 3
    print("   w=%2d  17-bit max %6d   formula %6d   %s"
          % (w, got, fm, "ok" if got == fm else "SHORT"))
