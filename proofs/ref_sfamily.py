#!/usr/bin/env python3
"""ref_sfamily.py -- REFEREE: the s-family ('A prediction, then the engine').

Claim: kind 2 = ((-s,0), N, E), seeded with kind 2 at c = 0..max(s,1)-1,
realises the lazy counter of profile I = {1,s+1} with a frame of
2 + max(s,1) PERMANENTLY BLOCKED laws, hence |S_{2^k}| = max(s,1)+3.

Independent checks: (i) the reset value on the ENGINE for s=0..5, k=1..12;
(ii) which laws are permanent, and whether each is blocked or active;
(iii) lockstep against my own bit-parallel lazy counter of profile {1,s+1};
(iv) |S_t| = 2 + max(s,1) + wt(y_t).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, card, active_laws, laws

E, W, N, S = (1, 0), (-1, 0), (0, -1), (0, 1)
T = 1 << 13


def counter_step(Y, I):
    """y_n <- y_n xor prod_{i in I} y_{n-i},  y_{<0} = 1."""
    P = None
    for i in I:
        sh = (Y << i) | ((1 << i) - 1)
        P = sh if P is None else (P & sh)
    return Y ^ P


def run(s):
    C = Const([(E, S, N), (S, N, S), ((-s, 0), N, E)], dim=2)
    m = max(s, 1)
    X = state_of([((-1, 0), 0), ((-1, 1), 1)] + [((c, 1), 2) for c in range(m)])
    I = (1, s + 1)
    Y = 0
    resets, perm, aa, ab = set(), None, set(), set()
    err = None
    for t in range(T):
        cur, act = set(), set(active_laws(X, C))
        for cell, k in laws(X):
            cur.add((cell, k))
        if perm is None:
            perm, aa, ab = set(cur), {x for x in cur if x in act}, \
                           {x for x in cur if x not in act}
        else:
            perm &= cur
            aa &= {x for x in cur if x in act}
            ab &= {x for x in cur if x not in act}
        if any(c[1] != 1 for c, kk in laws(X) if kk == 2):
            err = "kind 2 off the ray y=1 at t=%d" % t
            break
        k2 = sorted(c[0] for c, kk in laws(X) if kk == 2)
        if k2[:m] != list(range(m)):
            err = "seeded block 0..%d not intact at t=%d (k2=%s)" % (m - 1, t, k2[:6])
            break
        YY = 0
        for c in k2[m:]:
            YY |= 1 << (c - m)
        if YY != Y:
            err = "counter I={1,%d} diverges at t=%d" % (s + 1, t)
            break
        if card(X) != 2 + m + bin(Y).count("1"):
            err = "|S_t| != 2+max(s,1)+wt(y) at t=%d" % t
            break
        if t and (t & (t - 1)) == 0:
            resets.add(card(X))
        Y = counter_step(Y, I)
        X = step(X, C)
    return resets, perm, aa, ab, err


for s in range(0, 6):
    r, perm, aa, ab, err = run(s)
    m = max(s, 1)
    print("\n--- s = %d  (profile I = {1,%d}) ---" % (s, s + 1))
    print("  |S_{2^k}| over k=1..12 : %s    predicted %d  -> %s"
          % (sorted(r), m + 3, "OK" if r == {m + 3} else "MISMATCH"))
    print("  lockstep vs my lazy counter, t < 2^%d : %s"
          % (T.bit_length() - 1, "OK" if err is None else "FAIL: " + err))
    print("  permanent laws: %d  (claim 2+max(s,1) = %d) -> %s"
          % (len(perm), 2 + m, "OK" if len(perm) == 2 + m else "WRONG"))
    print("    permanently BLOCKED: %s" % sorted(ab))
    print("    permanently ACTIVE : %s" % sorted(aa))
