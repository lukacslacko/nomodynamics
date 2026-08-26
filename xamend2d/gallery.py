#!/usr/bin/env python3
"""gallery.py — the specimen gallery of Expedition X-B, with ASCII frames.

Every specimen here is certified in verify.py by xnomos.py (independent path).
Run:  python3 gallery.py > gallery.txt
"""
import sys

from xa2d import (Const, state, step, card, active, render, classify,
                  verify_glider, verify_balanced, growth_curve, alpha_fit)

SEED = {
    0: [(0, 0, 0)], 1: [(0, 0, 0), (0, 0, 1)], 2: [(0, 0, 0), (1, 0, 1)],
    3: [(0, 0, 0), (0, 1, 1)], 4: [(0, 0, 0), (1, 1, 1)],
    5: [(0, 0, 0), (1, 0, 0), (0, 1, 1)],
}


def frames(label, seed, n, mode="parity", skip=0, w=44, h=22, step_by=1,
           window=None):
    C = Const.parse(label)
    S = state([((x, y), k) for (x, y, k) in seed])
    for _ in range(skip):
        S = step(S, C, mode)
    out = []
    for t in range(n):
        out.append((skip + t * step_by, card(S),
                    render(S, maxw=w, maxh=h, window=window)))
        for _ in range(step_by):
            S = step(S, C, mode)
    return out


def show(title, label, seed, n, mode="parity", skip=0, w=44, h=22, step_by=1,
         note="", window=None):
    print("\n" + "=" * 72)
    print(title)
    print("  constitution : %s      semantics: %s" % (label, mode))
    print("  seed         : %s" % " ".join("%s@(%d,%d)" % (chr(65 + k), x, y)
                                           for (x, y, k) in seed))
    if note:
        for ln in note.strip().split("\n"):
            print("  " + ln)
    print("=" * 72)
    for t, c, art in frames(label, seed, n, mode, skip, w, h, step_by, window):
        print("  t = %-5d |S_t| = %-5d" % (t, c))
        for ln in art.split("\n"):
            print("    " + ln)
        print()


def main():
    print("XAMEND-2D SPECIMEN GALLERY  ·  Expedition X-B")
    print("Legend: A B C D = a single law of that kind at the cell;")
    print("        #       = two or more laws stacked in one cell;")
    print("        .       = empty ground.  y increases upwards.")

    show("1. THE WRIT OF REMOVAL  —  the first free glider of nomodynamics",
         "OEO>AB OEE>AB", SEED[1], 7, window=(-1, 8, 0, 0),
         note="""A repeals the whole pair where it stands (c = O, targets A and B);
B re-enacts the pair one cell east (c = E, targets A and B).
Phi(S) = sigma^(1,0)(S) exactly: a 2-law packet at the speed of light.
The eldest law CAN be repealed here -- because a different kind repeals it.""")

    show("2. THE DIAGONAL WRIT  —  a direction own-kind 2-D cannot take",
         "OEO>AB OEP>AB", SEED[1], 6, window=(-1, 6, -1, 6),
         note="""Same mechanism with c_B = NE. Phi(S) = sigma^(1,1)(S).
Own-kind 2-D confines every kind to an axis ray (nomos2d Thm 3), so no
own-kind object can move diagonally at all.""")

    show("3. THE ASSIZE  —  a glider gun (period 2, fires forever)",
         "OEO>AB OEE>AB OEO>AB", [(0, 0, 2)], 10, window=(0, 11, 0, 0),
         note="""C is a pump: nobody amends C, so it is immortal; it enacts a fresh
A+B pair on its own cell whenever its east neighbour is clear. The pair
walks away as a Writ, the east clears, and C fires again. One law in,
an infinite periodic stream of free gliders out.  |S_t| = t + 3.""")

    show("4. THE CIRCUIT COURT  —  a rake (a gun that walks)",
         "OEO>AB OEE>AB ONO>ABCD ONN>CD", [(0, 0, 2), (0, 0, 3)], 8,
         window=(0, 9, 0, 8),
         note="""C,D form a north-walking Writ; C's target set also contains A and B,
so the cell the pump vacates is left holding a fresh east-walking Writ.
One glider dropped per step, forever.  |S_t| = 2t + 2.""")

    show("5. THE LAND GRANT  —  alpha = 2 with bounding-box fill -> 1",
         "OPP>ABC OEE>B ONN>C", SEED[0], 7, window=(0, 7, 0, 7),
         note="""A is a diagonal sower: it walks NE and enacts A, B and C on every
diagonal cell it takes. B colonises east along its row, C colonises north
along its column, and the two floods meet exactly on the anti-diagonal.
|S_t| = (t+1)^2 exactly; cells = {(0,0)} u [1,t]^2; fill -> 1.
THE PLANE FILLS.  Impossible for any single-target constitution (Thm 3.1).""")

    show("6. THE SOWER  —  the two-kind minimum for alpha = 2",
         "OEE>AB ONN>B", SEED[0], 7, window=(0, 7, 0, 6),
         note="""A marches east dropping a B on every cell it takes; each B grows a
column north until it is blocked. |S_t| = (t+1)(t+2)/2: a solid triangle,
fill -> 1/2. One law, two kinds, one out-degree-2 clause.""")

    show("7. HEAD-ON WRITS  —  even gap: mutual transparency",
         "OEO>AB OEE>AB OWO>CD OWW>CD",
         [(0, 0, 0), (0, 0, 1), (4, 0, 2), (4, 0, 3)], 8,
         window=(-4, 9, 0, 0),
         note="""An east Writ (A,B) and a west Writ (C,D) in one constitution.
Even gap: both packets occupy the SAME cell for one step and pass through
each other undamaged, then recede forever. (Odd gap instead freezes them
adjacent: a 4-law block with zero active laws -- mutual arrest.)""")

    show("7b. HEAD-ON WRITS  —  odd gap: mutual arrest",
         "OEO>AB OEE>AB OWO>CD OWW>CD",
         [(0, 0, 0), (0, 0, 1), (3, 0, 2), (3, 0, 3)], 5,
         window=(-1, 5, 0, 0))

    show("5b. THE ONE-LAW GLIDER  —  a single statute that relocates itself",
         "OWO>ABC ORQ>A RER>BC", [(0, 0, 0)], 9, window=(-4, 4, -1, 5),
         note="""Phi^4(S) = sigma^(-1,1)(S) with |S| = 1: at every fourth step the
whole code is a SINGLE LAW, one cell up and one cell left of where it was.
Between those instants it swells to three laws and collapses again. Speed
1/4 -- subluminal, which the two-kind sector never produces under parity.""")

    show("5c. THE GRAND ASSIZE  —  a 50-law diagonal spaceship",
         "PQW>B ONE>AC ONP>ABC", [(0, 0, 0), (0, 0, 1), (0, 0, 2)], 3,
         skip=22, w=30, h=24,
         note="""p = 4, d = (4,4): fifty laws moving diagonally at the speed of
light, the largest certified glider in this expedition. Its core is reached
at t = 22 from three stacked laws at the origin.""")

    show("8. THE SESQUICENTENNIAL CLOCK  —  period 192 from three laws",
         "OQP>B RTW>AB", SEED[5], 4, w=30, h=16,
         note="""A 3-law seed whose orbit closes only after 192 steps. Own-kind
nomodynamics never produced a period that was not a power of two; the
cross-amendment sector produces 3, 5, 7, 21, 30, 112, 192, ...""")

    show("9. OWN-KIND PERIOD 3  —  the 2-adic conjecture is false",
         "EQN>A TQS>B", SEED[4], 5, skip=1, window=(-1, 3, -1, 3),
         note="""Both kinds amend ONLY THEMSELVES: this is pure own-kind
nomodynamics, in the sense of nomos2d. Its period is 3. The published
'all periods are powers of 2' regularity holds only for von Neumann
offsets; one diagonal offset breaks it.""")

    show("9b. THE ODOMETER  —  a binary counter with logarithmic reach",
         "OEW>B NQR>AB", [(0, 0, 0), (1, 0, 0), (0, 1, 1)], 9,
         w=8, h=12,
         note="""A column of width 2-3 that counts in binary. At every t = 2^k - 1
the code swells into a carry avalanche spanning its whole extent; at t = 2^k
it collapses to FOUR laws and starts again. Height ~ 0.20 (log2 t)^2:
86 cells at t = 2^20. Bounded card, unbounded reach -- so it can never
recur. The slowest clock in the fauna (the Jubilee code's reach is ~1.5 sqrt t).""")

    show("9c. THE ODOMETER at its jubilees  (t = 2^k - 1 and t = 2^k)",
         "OEW>B NQR>AB", [(0, 0, 0), (1, 0, 0), (0, 1, 1)], 2, skip=255,
         w=8, h=18,
         note="""t = 255 = 2^8 - 1: the avalanche.  t = 256: total collapse.""")

    show("10. THE PERPETUAL SESSION  —  a balanced constitution, 100% active",
         "OEO>A OEO>A",
         [(0, y, k) for y in range(5) for k in (0, 1)], 3, w=8, h=8,
         note="""Both kinds carry the same rule and both amend kind A, so at every
doubly-occupied cell the two authors' toggles cancel by parity. The code
is FIXED FOREVER while every one of its laws is active -- a parliament in
permanent session that never passes anything. Arbitrarily large.
Under OR-toggle this configuration is not fixed at all (Thm 2).""")

    show("11. THE TWO CHAMBERS  —  non-local balance (cancel at distance 2)",
         "ONN>A OSS>A",
         [(x, 0, 0) for x in range(6)] + [(x, 2, 1) for x in range(6)],
         3, w=10, h=6,
         note="""A-laws in the bottom row amend the middle row from below; B-laws in
the top row amend the same cells from above. Every enactment meets its
mirror and dies. The two chambers never see each other -- they only ever
meet in the amendments they cancel.""")

    show("12. THE BREATHING WRIT  —  a SUBLUMINAL glider (OR only)",
         "OEW>AB ONE>A", SEED[1], 7, mode="or", window=(-8, 2, 0, 0),
         note="""p = 2, d = (-1,0): half the speed of light. It inflates to 3 cells
and collapses back. Under parity the same universe has no glider at all:
the extra toggle that OR keeps is exactly what parity cancels.""")


if __name__ == "__main__":
    main()
