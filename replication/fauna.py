#!/usr/bin/env python3
"""
fauna.py — run the published nomodynamic fauna through the replication
detector and report, honestly, which rung each specimen reaches.

Rung 1 : card unbounded AND at some t the state contains >= 2 support-disjoint
         translated copies of the seed  (EMBEDDED copies -- no gap required)
Rung 2 : >= 2 CAUSAL COMPONENTS (gap > 2R), each an exact translate of the
         seed, debris empty or itself periodic
Rung 3 : the rung-2 copy count is unbounded in t

Compass for the xamend2d specimens is the xa2d one: N=(0,1), S=(0,-1),
P=NE=(1,1), Q=NW=(-1,1), R=SE=(1,-1), T=SW=(-1,-1).

Run:  python3 fauna.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from xnomos import Const, state_of, step, card                        # noqa
from replib import (radius, copy_offsets, max_disjoint, shift)        # noqa
from analyze import copy_census, linear_map                           # noqa

O = (0, 0); E = (1, 0); W = (-1, 0); N = (0, 1); S_ = (0, -1)
P_ = (1, 1); Q_ = (-1, 1); R_ = (1, -1); T_ = (-1, -1)


def audit(name, C, S0, mode, T=64, cardcap=4000, note=""):
    R = radius(C)
    S = dict(S0)
    L = dict(S0)
    maxemb = 0
    maxfree = 0
    maxfree_exact = 0
    firstfree = None
    cards = [card(S0)]
    phiNEL = 0
    for t in range(1, T + 1):
        S = step(S, C, mode)
        L = linear_map(L, C)
        if not S:
            break
        if S != L:
            phiNEL += 1
        cd = card(S)
        cards.append(cd)
        if cd > cardcap:
            break
        ds = copy_offsets(S, S0, C.dim)
        if len(ds) >= 2:
            fam = max_disjoint(S, S0, ds, C.dim, 0)
            maxemb = max(maxemb, len(fam))
        nc, ng, deb, anch = copy_census(S, S0, C, R)
        if nc >= 2:
            maxfree = max(maxfree, nc)
            if deb == 0:
                maxfree_exact = max(maxfree_exact, nc)
                if firstfree is None:
                    firstfree = (t, nc)
    grow = cards[-1] > 2 * cards[0]
    rung = 0
    if grow and maxemb >= 2:
        rung = 1
    if maxfree_exact >= 2:
        rung = 2
    if maxfree_exact >= 4:
        rung = 3
    print("%-22s R=%d  card %d->%d  embedded=%-3d  freeExact=%-3d  "
          "first=%-9s  Phi!=L %d/%d  -> RUNG %d %s"
          % (name, R, cards[0], cards[-1], maxemb, maxfree_exact,
             str(firstfree), phiNEL, T, rung, note))
    return rung


if __name__ == "__main__":
    print("=== anti-cheat controls ===")
    audit("colonizer block n=4", Const([(0, 1, 1)]),
          state_of([(i, 0) for i in range(4)]), "parity", T=40,
          note="(must NOT reach rung 2: copies are adjacent)")
    audit("colonizer 1 law", Const([(0, 1, 1)]), state_of([(0, 0)]),
          "parity", T=40)

    print("\n=== chapter one: own-kind ===")
    audit("PASCAL COLUMN", Const([(O, E, N)], dim=2),
          state_of([((0, 0), 0)]), "parity", T=70,
          note="(DEGENERATE seed: 1 law, 1 cell)")
    audit("JUBILEE CODE", Const([((1, 0), (0, 1), (0, -1)),
                                 ((0, 1), (0, -1), (0, 1)),
                                 ((-1, 0), (0, -1), (1, 0))], dim=2),
          state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)]), "parity", T=200)
    audit("sunset clause", Const([(0, -1, 1)]), state_of([(0, 0)]),
          "parity", T=40)

    print("\n=== chapter two: cross-amendment ===")
    audit("LAND GRANT", Const([(O, P_, P_), (O, E, E), (O, N, N)],
                              [(0, 1, 2), (1,), (2,)], dim=2),
          state_of([((0, 0), 0)]), "parity", T=40)
    audit("SOWER", Const([(O, E, E), (O, N, N)], [(0, 1), (1,)], dim=2),
          state_of([((0, 0), 0)]), "parity", T=40)
    audit("CIRCUIT COURT", Const([(O, E, O), (O, E, E), (O, N, O), (O, N, N)],
                                 [(0, 1), (0, 1), (0, 1, 2, 3), (2, 3)],
                                 dim=2),
          state_of([((0, 0), 2), ((0, 0), 3)]), "parity", T=48)
    audit("ASSIZE (gun)", Const([(O, E, O), (O, E, E), (O, E, O)],
                                [(0, 1), (0, 1), (0, 1)], dim=2),
          state_of([((0, 0), 2)]), "parity", T=48)
    audit("ITINERANT COURT", Const([(O, E, O), (O, E, E), (O, O, O)],
                                   [(0, 1, 2), (0, 1), (2,)], dim=2),
          state_of([((0, 0), 0), ((0, 0), 1)]), "parity", T=48)
    audit("1-D RAKE", Const([(0, 1, 0), (0, 1, 1), (0, -1, 0), (0, -1, -1)],
                            [(0, 1), (0, 1), (0, 1, 2, 3), (2, 3)]),
          state_of([(0, 2), (0, 3)]), "parity", T=64)
    audit("1-D GUN", Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)],
                           [(0, 1), (0, 1), (0, 1)]),
          state_of([(0, 2)]), "parity", T=64)
    audit("PICKET PUFFER", Const([(0, 1, 1), (0, -1, 1)], [(0, 1), (0, 1)]),
          state_of([(0, 0), (5, 1)]), "or", T=64)
    audit("TANDEM-1 glider", Const([(0, -1, 1), (0, -1, 0)],
                                   [(0, 1), (0, 1)]),
          state_of([(0, 0), (0, 1)]), "parity", T=40)

    print("\n=== this expedition ===")
    audit("THE MOOT (additive)", Const([(O, N, E), (O, N, W)],
                                       [(0, 1), (0, 1)], dim=2),
          state_of([((0, 0), 0), ((0, 0), 1), ((2, 0), 0), ((2, 0), 1)]),
          "parity", T=140)
    audit("THE SPLIT DECISION", Const([((0, 0), (-1, -1), (0, -1)),
                                       ((0, 0), (1, 0), (0, 1))],
                                      [(0, 1), (0, 1)], dim=2,
                                      guards=[(1, 0), (1, None)]),
          state_of([((0, 0), 0), ((0, 0), 1), ((2, 0), 0), ((2, 0), 1)]),
          "or", T=140)
    audit("THE QUORUM", Const([((-1, -1), (0, -1), (1, -1)),
                               ((0, 0), (0, -1), (1, -1))],
                              [(0, 1), (0, 1)], dim=2),
          state_of([((0, 0), 1), ((1, 1), 0)]), "super_or", T=140)
    audit("THE PRECEDENT (1-D)", Const([(-1, -1, 1), (-1, -1, 1)],
                                       [(1,), (0,)], dim=1,
                                       guards=[(None, 1), (0, 1)]),
          state_of([(0, 0), (1, 0), (2, 0), (2, 1)]), "parity", T=140)
    audit("THE ENGROSSMENT", Const([((0, -1), (-1, 1), (1, 1)),
                                    ((0, -1), (0, 1), (1, 0))],
                                   [(0, 1), (0, 1)], dim=2),
          state_of([((0, 0), 0), ((0, 0), 1), ((0, 1), 0), ((0, 1), 1)]),
          "parity", T=140)
