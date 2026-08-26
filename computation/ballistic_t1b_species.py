"""T1b: what glider species does each specimen universe carry?
Complete small-seed enumeration per universe.  Two species that can MEET =
(a) opposite signs of d (head-on), or (b) same sign, different d/p (rear-end).
"""
import sys, itertools, json
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *
from fractions import Fraction

def sweep(C, mode, W, maxlaws=None, max_steps=150, max_card=80, max_span=160):
    """Complete enumeration of seeds supported in cells 0..W-1, anchored so
    that cell 0 is occupied.  Returns dict (p,d) -> (minimal-card seed, res)."""
    slots = [(c, k) for c in range(W) for k in range(C.n)]
    got, nseed = {}, 0
    ml = maxlaws or len(slots)
    for r in range(1, ml + 1):
        for combo in itertools.combinations(slots, r):
            if min(c for c, _ in combo) != 0:
                continue
            nseed += 1
            S0 = state_of(combo)
            res = classify(S0, C, mode, max_steps=max_steps,
                           max_card=max_card, max_span=max_span)
            if res["kind"] == GLIDER:
                key = (res["period"], res["displacement"])
                if key not in got or res["card"] < got[key][1]["card"]:
                    got[key] = (combo, res)
    return got, nseed

UNIS = [
    ("TANDEM-1", Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)]), 6, None),
    ("SOLO", Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(1, 2), (0,), (0,)]), 4, 4),
    ("TRIPTYCH", Const([(0, 1, 0), (0, -1, 1), (0, 1, -1)], [(0, 1, 2)] * 3), 4, 5),
    ("GUN", Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(0, 1)] * 3), 4, 4),
    ("MIRROR", Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)]), 7, None),
]

print("=" * 78)
print("T1b  GLIDER SPECIES PER UNIVERSE  (complete seed enumeration)")
print("=" * 78)
for nm, C, W, ml in UNIS:
    for mode in ("parity", "or"):
        got, nseed = sweep(C, mode, W, ml)
        sp = sorted({(k[0], k[1]) for k in got})
        speeds = sorted({Fraction(d, p) for p, d in sp})
        print("%-10s %-7s W=%d maxlaws=%s seeds=%d  species=%d  speeds=%s"
              % (nm, mode, W, ml, nseed, len(sp),
                 [str(x) for x in speeds]))
        for k in sorted(got):
            cb, rs = got[k]
            print("        p=%-3d d=%+d card=%-3d t0=%-3d seed=%s"
                  % (k[0], k[1], rs["card"], rs["t"], list(cb)))
    print()
