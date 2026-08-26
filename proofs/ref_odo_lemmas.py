#!/usr/bin/env python3
"""ref_odo_lemmas.py -- REFEREE: Lemmas 2.1, 2.2, Thm 2.3, Cor 2.4, Prop 2.5.

Run on the specimen ACTUALLY used in proofs/t2_odometer.py (V-table with
N=(0,-1)); every clause of the lemmas is checked from the full recorded
support, with no assumption carried over from the author's code.
The SAME battery is then run on the specimen of xamend2d (N=(0,+1)),
which is the published THE ODOMETER, to show which clauses fail there.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, card, active_laws, laws

AU = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
      "P": (1, -1), "Q": (-1, -1), "R": (1, 1), "T": (-1, 1)}
XA = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
      "P": (1, 1), "Q": (-1, 1), "R": (1, -1), "T": (-1, -1)}


def mk(V):
    return Const([tuple(V[c] for c in "OEW"), tuple(V[c] for c in "NQR")],
                 [(1,), (0, 1)], dim=2)


SEED = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])

E, W, N, S = (1, 0), (-1, 0), (0, -1), (0, 1)
JUB = Const([(E, S, N), (S, N, S), (W, N, E)], dim=2)
JSEED = state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)])


def battery(V, name, U):
    C = mk(V)
    X = dict(SEED)
    J = dict(JSEED)
    Cj = frozenset([0])          # my own carry automaton
    bad = {}

    def note(key, u, extra=""):
        bad.setdefault(key, (u, extra))

    for u in range(U):
        # ---- even tick t = 2u ------------------------------------------
        cells = {}
        for cell, k in laws(X):
            cells.setdefault(cell, set()).add(k)
        act = set(active_laws(X, C))
        if any(c[0] not in (0, 1) for c in cells):
            note("some cell with x not in {0,1} occupied (even)", 2 * u,
                 sorted(c for c in cells if c[0] not in (0, 1))[:3])
        if any(c[1] < 0 for c in cells):
            note("some cell with y<0 occupied (even)", 2 * u,
                 sorted(c for c in cells if c[1] < 0)[:3])
        if (1, 1) in cells:
            note("(1,1) occupied (even)", 2 * u)
        if cells.get((0, 0)) != {0}:
            note("A@(0,0) missing / cell impure (even)", 2 * u, cells.get((0, 0)))
        if cells.get((1, 0)) != {0}:
            note("A@(1,0) missing / cell impure (even)", 2 * u, cells.get((1, 0)))
        if ((0, 0), 0) in act:
            note("A@(0,0) ACTIVE (even)", 2 * u)
        if ((1, 0), 0) not in act:
            note("A@(1,0) NOT active (even)", 2 * u)
        col1 = sorted(c[1] for c in cells if c[0] == 1)
        if col1 != [0]:
            note("column 1 not just the frame law at even time", 2 * u, col1)
        D = frozenset(c[1] for c, k in laws(X) if k == 1 and c[0] == 0)
        if 1 not in D:
            note("1 not in D_u", 2 * u)
        if 0 in D:
            note("0 in D_u", 2 * u)
        if D != frozenset(c + 1 for c in Cj):
            note("D_u != C_u + 1", 2 * u, sorted(D)[:4])
        if card(X) != 2 + len(D):
            note("|S_O(2u)| != 2 + |D_u|", 2 * u, card(X))
        if card(X) != card(J):
            note("|S_O(2u)| != |S_J(u)|", 2 * u, (card(X), card(J)))
        Cjub = frozenset(c[0] for c, k in laws(J) if k == 2)
        if Cjub != Cj:
            note("engine Jubilee != my carry automaton", u, sorted(Cjub ^ Cj)[:4])
        alpha = frozenset(y for y in D if y == 1 or (y - 1) in D)

        # ---- odd tick t = 2u+1 -----------------------------------------
        X1 = step(X, C)
        cells1 = {}
        for cell, k in laws(X1):
            cells1.setdefault(cell, set()).add(k)
        want = {(0, 0): {0}, (1, 0): {0}}
        want[(0, 0)] = {0}
        for y in D:
            want[(0, y)] = {1}
        want.setdefault((0, 0), set()).add(1)   # B@(0,0) created at the odd tick
        for y in alpha:
            want[(1, y + 1)] = {0, 1}
        want[(1, 0)] = {0}
        if cells1 != want:
            note("odd-time state != frame + B@(0,0) + D + buffer(alpha+1)",
                 2 * u + 1, (sorted(cells1.items())[:4], sorted(want.items())[:4]))
        if card(X1) != 3 + len(D) + 2 * len(alpha):
            note("odd card != 3 + |C| + 2 act(C)", 2 * u + 1, card(X1))
        act1 = set(active_laws(X1, C))
        if any(k == 1 and cc[0] == 1 for cc, k in act1):
            note("a kind-B law in column 1 is ACTIVE", 2 * u + 1)
        X = step(X1, C)
        Dn = frozenset(c[1] for c, k in laws(X) if k == 1 and c[0] == 0)
        if Dn != D ^ frozenset(y + 1 for y in alpha):
            note("D_{u+1} != D_u xor (alpha_u + 1)", 2 * u + 2, sorted(Dn)[:4])
        J = step(J, JUB)
        Cj = Cj ^ frozenset(c + 1 for c in Cj if c == 0 or (c - 1) in Cj)
    print("\n=== %s : u < %d (t < %d) ===" % (name, U, 2 * U))
    if not bad:
        print("  ALL clauses of Lemma 2.1, Lemma 2.2, Thm 2.3 hold.  COMPLETE BOX.")
    else:
        for k, v in sorted(bad.items(), key=lambda kv: kv[1][0]):
            print("  VIOLATED: %-58s first at t=%d  %s" % (k, v[0], v[1]))
    return bad


if __name__ == "__main__":
    U = int(sys.argv[1]) if len(sys.argv) > 1 else (1 << 15)
    battery(AU, "proofs/t2_odometer.py specimen (N=(0,-1)) -- what Sec.2 proves", U)
    battery(XA, "xamend2d specimen (N=(0,+1)) -- the PUBLISHED THE ODOMETER", 64)
