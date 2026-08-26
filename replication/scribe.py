#!/usr/bin/env python3
"""
scribe.py — THE SCRIBE: unbounded heritable copying in the citation sector.

Eighteen kinds, 2-D, parity, occupancy + citation guards.  A clerk walks along
a blueprint row, copies every symbol one row up BY NAME (a citation guard per
symbol), and on reaching the end marker enacts a clerk of the OPPOSITE
handedness on the fresh row.  The new clerk walks back the other way and does
the same.  Generation k occupies row k and carries an exact copy of the
original blueprint, for every k.

    0 X   blueprint symbol '0'          inert
    1 Y   blueprint symbol '1'          inert
    2 L   left end marker               inert
    3 Z   right end marker              inert
    4-10  the RIGHT-handed clerk: A1 B1 T1X T1Y T1L T1Z S1
    11-17 the LEFT-handed clerk:  A2 B2 T2X T2Y T2L T2Z S2

    A_i  [self | north vacant]                 -> clear own clerk here
    B_i  [self | NO Z (resp. NO L) here]       -> enact own clerk east (west)
    T_is [KIND s HERE | north vacant]          -> enact kind s north
    S_1  [KIND Z HERE | north vacant]          -> enact the LEFT clerk north
    S_2  [KIND L HERE | north vacant]          -> enact the RIGHT clerk north

The B clause is the only place a citation appears in a VACANCY position: the
clerk halts because a named provision stands in its own cell.

Run:  python3 scribe.py
"""

from __future__ import annotations

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from xnomos import Const, state_of, step, card                       # noqa
from replib import to_p, pstep, from_p, frame2d, radius, contains, shift  # noqa

X, Y, L, Z = 0, 1, 2, 3
A1, B1, T1X, T1Y, T1L, T1Z, S1 = range(4, 11)
A2, B2, T2X, T2Y, T2L, T2Z, S2 = range(11, 18)
R1 = (A1, B1, T1X, T1Y, T1L, T1Z, S1)
L2 = (A2, B2, T2X, T2Y, T2L, T2Z, S2)

O, N, E, W = (0, 0), (0, 1), (1, 0), (-1, 0)
INERT = (O, O, O)

RULES = [INERT, INERT, INERT, INERT,
         (O, N, O), (O, O, E), (O, N, N), (O, N, N), (O, N, N), (O, N, N),
         (O, N, N),
         (O, N, O), (O, O, W), (O, N, N), (O, N, N), (O, N, N), (O, N, N),
         (O, N, N)]

TARGETS = [(X,), (Y,), (L,), (Z,),
           R1, R1, (X,), (Y,), (L,), (Z,), L2,
           L2, L2, (X,), (Y,), (L,), (Z,), R1]

GUARDS = [(None, None)] * 4 + [
    (None, None),      # A1 occupancy
    (None, Z),         # B1 halts on the right marker  (CITATION in vacancy)
    (X, None), (Y, None), (L, None), (Z, None),
    (Z, None),         # S1 cites Z -> births the left clerk
    (None, None),      # A2
    (None, L),         # B2 halts on the left marker
    (X, None), (Y, None), (L, None), (Z, None),
    (L, None)]         # S2 cites L -> births the right clerk

SCRIBE = Const(RULES, TARGETS, dim=2, guards=GUARDS)
SYM = "XYLZabcdefgABCDEFG"


def seed(tape, y0=0):
    """row y0 = L s1..sn Z, right-handed clerk on the L cell."""
    pairs = [((0, y0), L)]
    for i, ch in enumerate(tape):
        pairs.append(((i + 1, y0), X if ch == '0' else Y))
    pairs.append(((len(tape) + 1, y0), Z))
    for k in R1:
        pairs.append(((0, y0), k))
    return state_of(pairs)


def read_row(S, y, n):
    """Read row y back as 'L....Z' (blank where a symbol is missing)."""
    out = []
    for x in range(0, n + 2):
        m = S.get((x, y), 0)
        if (m >> L) & 1:
            out.append('L')
        elif (m >> Z) & 1:
            out.append('Z')
        elif (m >> X) & 1:
            out.append('0')
        elif (m >> Y) & 1:
            out.append('1')
        else:
            out.append('.')
    return "".join(out)


def generations(tape, gens, engine="xnomos"):
    """Run long enough for `gens` generations; return the rows read back."""
    n = len(tape)
    S0 = seed(tape)
    steps = (n + 3) * gens + 4
    if engine == "xnomos":
        S = dict(S0)
        for _ in range(steps):
            S = step(S, SCRIBE, "parity")
    else:
        P = to_p(S0)
        for _ in range(steps):
            P = pstep(P, SCRIBE, "parity")
        S = from_p(P)
    return [read_row(S, y, n) for y in range(gens + 1)], S, S0, steps


if __name__ == "__main__":
    print("THE SCRIBE — heritable copying in the citation sector")
    print("kinds = %d   R = %d   mode = parity" % (SCRIBE.n, radius(SCRIBE)))
    print()
    S = seed("011")
    print("  frames, blueprint 011 (L,Z markers; a..g = right clerk, "
          "A..G = left clerk):")
    for t in range(12):
        print("   t=%2d card=%2d" % (t, card(S)))
        for r in frame2d(S, (-1, 6, -1, 3), sym=SYM):
            print("        " + r)
        S = step(S, SCRIBE, "parity")
    print()
    ok = True
    for tape in ["0", "1", "01", "011", "1001", "110100", "0101101",
                 "".join(random.Random(4).choice("01") for _ in range(9))]:
        want = "L" + tape + "Z"
        rows, Sfin, S0, steps = generations(tape, 6)
        rows2, _, _, _ = generations(tape, 6, engine="pstep")
        good = all(r == want for r in rows) and rows == rows2
        ok &= good
        print("  blueprint %-11s  6 generations: %s   %s"
              % (tape, " ".join(rows), "OK" if good else "MISMATCH " + str(rows)))
    print()
    # exact embedded translated copies of the WHOLE seed?
    tape = "1001"
    rows, Sfin, S0, steps = generations(tape, 6)
    hits = [d for d in range(1, 7)
            if contains(Sfin, {c: m & 0xF for c, m in
                               shift({k: v for k, v in S0.items()},
                                     (0, d), 2).items() if m & 0xF})]
    print("  rows carrying an exact translate of the seed's BLUEPRINT: %s"
          % hits)
    print("  clerk laws present at the end:",
          sorted((c, m >> 4) for c, m in Sfin.items() if m >> 4))
    print()
    print("heritable-copying property:", "HOLDS" if ok else "FAILS")
