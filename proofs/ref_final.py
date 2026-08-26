#!/usr/bin/env python3
"""ref_final.py -- REFEREE: (i) identify the author's Sec.2 specimen inside the
xamend2d census notation; (ii) settle min{|S_t| : w(t)=w} = w+3 for every w
with a window that is actually big enough (2w bits)."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, card

XA = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
      "P": (1, 1), "Q": (-1, 1), "R": (1, -1), "T": (-1, -1)}


def mk(lbl):
    rules, tg = [], []
    for tok in lbl.split():
        abc, t = tok.split(">")
        rules.append(tuple(XA[c] for c in abc))
        tg.append(tuple(sorted(ord(c) - ord("A") for c in t)))
    return Const(rules, [t if len(t) > 1 else t[0] for t in tg], dim=2)


SEED5 = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])
print("== which census code is proofs/RESULTS.md Sec.2 really about? ==")
for lbl in ("OEW>B NQR>AB", "OEW>B STP>AB"):
    S = dict(SEED5)
    fl, pk, ht = {}, {}, {}
    for t in range((1 << 14) + 1):
        if t and (t & (t - 1)) == 0:
            fl[t.bit_length() - 1] = card(S)
            ys = [c[1] for c in S]
            ht[t.bit_length() - 1] = max(ys) - min(ys) + 1
        if t and ((t + 1) & t) == 0:
            pk[(t + 1).bit_length() - 1] = card(S)
        S = step(S, mk(lbl))
    ks = sorted(fl)
    print("\n  %s  (xa2d frame, census seed 5)" % lbl)
    print("    card(2^k)     k=1..14:", [fl[k] for k in ks if k >= 1])
    print("    card(2^k - 1) k=1..14:", [pk[k] for k in ks if k >= 1])
    print("    height(2^k)   k=1..14:", [ht[k] for k in ks if k >= 1])
print("\n  Sec.2 of proofs/RESULTS.md predicts card(2^k)=4 for all k>=1 and "
      "crest 6,9,12,18,21,36,39,72,75,144,147,288,291,576")

print("\n== min{|S_t| : w(t)=w} = w+3 : DP with a 2w-bit window ==")


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


rows = []
for w in range(1, 31):
    st = extremes(2 * w)          # bit positions 0..2w-1: {0} u P_0..P_{w-1}
    rows.append((w, st[w][0] + 3, w + 3))
print("  w, min|S| in a 2w-bit window, w+3:", rows[:12], "...")
print("  min == w+3 for every w = 1..30 (window 2w bits):",
      all(a == b for _, a, b in rows))
print("  and in a (2w-1)-bit window the min is strictly larger for w>=10:",
      [(w, extremes(2 * w - 1)[w][0] + 3) for w in range(9, 14)])
print("  17-bit window: the first w whose min exceeds w+3 is",
      min(w for w in range(1, 18) if extremes(17)[w][0] + 3 > w + 3))
