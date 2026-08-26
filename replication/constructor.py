#!/usr/bin/env python3
"""
constructor.py — the citation-sector constructor (rung 4 attempt).

THE ENGROSSING CLERK.  Eight kinds, 2-D, occupancy AND citation guards,
parity resolution.

    0 X   blueprint symbol "0"      inert dead letter (a = b, guard self-refutes)
    1 Y   blueprint symbol "1"      inert
    2 U   built symbol "0"          inert
    3 V   built symbol "1"          inert
    4 A   clerk, repeal clause      [self | north vacant] -> clear {A,B,P,Q} here
    5 B   clerk, motion clause      [self | north vacant] -> enact {A,B,P,Q} east
    6 P   engrossing clause for X   [X HERE | north vacant] -> enact U north
    7 Q   engrossing clause for Y   [Y HERE | north vacant] -> enact V north

P and Q are the citation clauses: each fires only if a law OF A NAMED KIND
stands in its own cell.  The clerk therefore READS the blueprint under it and
WRITES a different, decoded pattern one row up.  The built row is a function of
the blueprint, not of the constitution: change the tape, change what is built.

Run:  python3 constructor.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from xnomos import Const, state_of, step, card, active_laws          # noqa
from replib import to_p, pstep, from_p, frame2d, radius             # noqa

X, Y, U, V, A, B, P, Q = range(8)
O, N, E = (0, 0), (0, 1), (1, 0)

INERT = (O, O, O)                      # occ(self) AND NOT occ(self) -- never

CLERK = Const(
    rules=[INERT, INERT, INERT, INERT,
           (O, N, O),                  # A : clear the cell it stands in
           (O, N, E),                  # B : re-enact the clerk one cell east
           (O, N, N),                  # P : write north
           (O, N, N)],                 # Q : write north
    targets=[(X,), (Y,), (U,), (V,),
             (A, B, P, Q), (A, B, P, Q), (U,), (V,)],
    dim=2,
    guards=[(None, None)] * 4 +
           [(None, None),              # A : occupancy guard
            (None, None),              # B : occupancy guard
            (X, None),                 # P : CITES kind X in its own cell
            (Y, None)])                # Q : CITES kind Y in its own cell

HEAD = (A, B, P, Q)


def seed(tape, x0=0, y0=0):
    """tape: a string over '01'.  Blueprint on row y0, clerk on its first cell."""
    pairs = []
    for i, ch in enumerate(tape):
        pairs.append(((x0 + i, y0), X if ch == '0' else Y))
    for k in HEAD:
        pairs.append(((x0, y0), k))
    return state_of(pairs)


def built_row(S, y):
    """Read the built row y back out as a string over '01' (None if absent)."""
    xs = [c[0] for c in S if c[1] == y and S[c] & ((1 << U) | (1 << V))]
    if not xs:
        return ""
    out = []
    for x in range(min(xs), max(xs) + 1):
        m = S.get((x, y), 0)
        out.append('0' if (m >> U) & 1 else '1' if (m >> V) & 1 else '?')
    return "".join(out)


def run(tape, steps=None, show=False):
    S = seed(tape)
    steps = steps or len(tape) + 2
    frames = []
    for t in range(steps):
        if show:
            frames.append((t, card(S), frame2d(S, (-1, len(tape) + 1, -1, 2),
                                               sym="XYUVABPQ")))
        S = step(S, CLERK, "parity")
    return S, frames


def decode(tape):
    return tape                      # U/V are the images of X/Y, index-for-index


if __name__ == "__main__":
    print("THE ENGROSSING CLERK — a blueprint-driven constructor")
    print("R =", radius(CLERK))
    print()
    S, frames = run("0110", steps=7, show=True)
    for t, cd, rows in frames:
        print("  t=%d card=%d" % (t, cd))
        for r in rows:
            print("     " + r)
    print()
    ok = True
    for tape in ["0", "1", "01", "10", "0110", "1001", "111000",
                 "0101010101", "1101001110", "00000", "11111"]:
        S, _ = run(tape)
        got = built_row(S, 1)
        want = decode(tape)
        # independent engine
        P2 = to_p(seed(tape))
        for _ in range(len(tape) + 2):
            P2 = pstep(P2, CLERK, "parity")
        got2 = built_row(from_p(P2), 1)
        good = (got == want == got2)
        ok &= good
        print("  blueprint %-12s -> built %-12s  want %-12s  %s%s"
              % (tape, got, want, "OK" if good else "MISMATCH",
                 "" if got == got2 else "  (ENGINES DISAGREE)"))
    print()
    print("constructor property:", "HOLDS" if ok else "FAILS")
