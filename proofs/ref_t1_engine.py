#!/usr/bin/env python3
"""ref_t1_engine.py -- REFEREE: independent engine lockstep for Sec 1.1-1.3.

Records the FULL support at every step (no assumption that anything is frozen)
and checks, from scratch:
   (a) supp_0 == {(-1,0)} and supp_1 == {(-1,1)} for every t
   (b) supp_2 subset {(c,1): c>=0}
   (c) NO cell off the three rays is ever occupied
   (d) no cell ever carries two kinds
   (e) 0 in C_t
   (f) C_{t+1} == C_t xor {c+1 : c in C_t, (c=0 or c-1 in C_t)}
   (g) |S_t| == 2 + |C_t|
   (h) |S_t| == 3 + #{n : mu_n & ~t == 0}   (my own OR-Fibonacci, computed here)
   (i) the frame laws are BLOCKED (not active) and WNE@(0,1) is ACTIVE, always
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, card, active_laws

E, W, N, S = (1, 0), (-1, 0), (0, -1), (0, 1)
JUB = Const([(E, S, N), (S, N, S), (W, N, E)], dim=2)
SEED = state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)])

TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else (1 << 17)


def orfib(count):
    out, p2, p1 = [], 0, 0
    for _ in range(count):
        m = (p1 | p2) + 1
        out.append(m)
        p2, p1 = p1, m
    return out


MU = orfib(4000)


def main():
    Sx = dict(SEED)
    C = frozenset([0])
    fails = []
    ray0 = lambda c: c[0] == -1 and c[1] <= 0
    ray1 = lambda c: c[0] == -1 and c[1] >= 1
    ray2 = lambda c: c[1] == 1 and c[0] >= 0
    maxc = 0
    for t in range(TMAX):
        s0, s1, s2, offray, multi = [], [], [], [], []
        for cell, mask in Sx.items():
            if bin(mask).count("1") > 1:
                multi.append((cell, mask))
            for k in range(3):
                if (mask >> k) & 1:
                    if k == 0:
                        s0.append(cell)
                    elif k == 1:
                        s1.append(cell)
                    else:
                        s2.append(cell)
            if not (ray0(cell) or ray1(cell) or ray2(cell)):
                offray.append(cell)
        if sorted(s0) != [(-1, 0)]:
            fails.append(("supp_0", t, sorted(s0)[:5]))
            break
        if sorted(s1) != [(-1, 1)]:
            fails.append(("supp_1", t, sorted(s1)[:5]))
            break
        if any(c[1] != 1 or c[0] < 0 for c in s2):
            fails.append(("supp_2 off ray", t, sorted(s2)[:5]))
            break
        if offray:
            fails.append(("off-ray cell occupied", t, offray[:5]))
            break
        if multi:
            fails.append(("two kinds in one cell", t, multi[:5]))
            break
        Cnow = frozenset(c[0] for c in s2)
        if Cnow != C:
            fails.append(("C_t != automaton", t, sorted(Cnow ^ C)[:5]))
            break
        if 0 not in C:
            fails.append(("0 not in C_t", t, None))
            break
        if card(Sx) != 2 + len(C):
            fails.append(("|S| != 2+|C|", t, (card(Sx), len(C))))
            break
        if card(Sx) != 3 + sum(1 for m in MU if m & ~t == 0):
            fails.append(("|S| != closed form", t, card(Sx)))
            break
        act = set(active_laws(Sx, JUB))
        if ((-1, 0), 0) in act or ((-1, 1), 1) in act:
            fails.append(("a frame law is ACTIVE", t, None))
            break
        if ((0, 1), 2) not in act:
            fails.append(("WNE@(0,1) not active", t, None))
            break
        want_act = {((c, 1), 2) for c in C if c == 0 or (c - 1) in C}
        if act != want_act:
            fails.append(("active set wrong", t, sorted(act ^ want_act)[:5]))
            break
        maxc = max(maxc, max(C))
        Sx = step(Sx, JUB)
        C = C ^ {c + 1 for c in C if c == 0 or (c - 1) in C}
    if fails:
        print("FAIL", fails)
        return 1
    print("ref_t1_engine: COMPLETE BOX t < %d (=2^%d): all of (a)-(i) hold."
          % (TMAX, TMAX.bit_length() - 1))
    print("  max ray coordinate reached: c = %d" % maxc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
