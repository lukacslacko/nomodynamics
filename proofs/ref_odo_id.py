#!/usr/bin/env python3
"""ref_odo_id.py -- REFEREE: which machine is 'THE ODOMETER'?

xamend2d/xa2d.py uses  N=(0,1), S=(0,-1), P=NE=(1,1), Q=NW=(-1,1),
                       R=SE=(1,-1), T=SW=(-1,-1).
proofs/t2_odometer.py uses N=(0,-1), S=(0,1), P=(1,-1), Q=(-1,-1),
                       R=(1,1),  T=(-1,1).      <-- y-flipped table

Both use the seed literally as A@(0,0), A@(1,0), B@(0,1).  A y-flip of the
RULES without a y-flip of the SEED is NOT a conjugacy.  So compare.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, laws, card, active_laws

# ---- xa2d.py / xamend2d/verify.py convention (the PUBLISHED specimen) ----
XA = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
      "P": (1, 1), "Q": (-1, 1), "R": (1, -1), "T": (-1, -1)}
# ---- proofs/t2_odometer.py convention ----
AU = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
      "P": (1, -1), "Q": (-1, -1), "R": (1, 1), "T": (-1, 1)}


def mk(V):
    return Const([tuple(V[c] for c in "OEW"), tuple(V[c] for c in "NQR")],
                 [(1,), (0, 1)], dim=2)


SEED = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])

TMAX = 1 << 17


def run(C, seed, tmax, label):
    S = dict(seed)
    floors, peaks, heights, widths = {}, {}, {}, {}
    for t in range(tmax + 1):
        if t and (t & (t - 1)) == 0:
            ys = [c[1] for c in S]
            xs = [c[0] for c in S]
            floors[t.bit_length() - 1] = card(S)
            heights[t.bit_length() - 1] = max(ys) - min(ys) + 1
            widths[t.bit_length() - 1] = max(xs) - min(xs) + 1
        if t and ((t + 1) & t) == 0:
            peaks[(t + 1).bit_length() - 1] = card(S)
        S = step(S, C)
    print("\n== %s ==" % label)
    ks = sorted(heights)
    print("  k              :", [k for k in ks])
    print("  card(2^k)      :", [floors[k] for k in ks])
    print("  card(2^k - 1)  :", [peaks.get(k) for k in ks])
    print("  height(2^k)    :", [heights[k] for k in ks])
    print("  width(2^k)     :", [widths[k] for k in ks])
    return floors, peaks, heights, widths


PUB = {10: (4, 57, 20, 2), 12: (6, 75, 26, 3), 14: (4, 111, 38, 2),
       16: (4, 138, 47, 2)}

if __name__ == "__main__":
    for name, V in (("PUBLISHED convention (xa2d OFF table)", XA),
                    ("AUTHOR t2_odometer.py convention", AU)):
        f, p, h, w = run(mk(V), SEED, TMAX, name)
        print("  vs published table (k: card2^k, card2^k-1, height, width):")
        for k, (c, pk, ht, wd) in PUB.items():
            got = (f.get(k), p.get(k), h.get(k), w.get(k))
            print("    k=%2d  published %s   measured %s   %s"
                  % (k, (c, pk, ht, wd), got,
                     "MATCH" if got == (c, pk, ht, wd) else "differ"))
    # also: the y-flipped seed under the published convention
    f, p, h, w = run(mk(XA), state_of([((0, 0), 0), ((1, 0), 0), ((0, -1), 1)]),
                     TMAX, "PUBLISHED convention, seed B@(0,-1) (=author's, reflected)")
