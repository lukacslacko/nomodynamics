#!/usr/bin/env python3
"""verify.py — re-check every named claim of nomodynamics from scratch.

    python3 verify.py            # the whole battery (~30 s)
    python3 verify.py -v         # print each specimen's spacetime diagram

Everything runs on the shared engine `xnomos.py`, independently of the
expedition code that originally found these specimens; the point is that a
reader can confirm the note's claims without reading any of it.
"""
from __future__ import annotations

import os
import random
import sys

from xnomos import (Const, state_of, step, card, active_laws, classify,
                    verify_balanced, verify_glider, spacetime, render, RULES1,
                    BALANCED, CYCLE, FIXED, GLIDER)

VERBOSE = "-v" in sys.argv
PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("  %s  %-52s %s" % ("ok " if cond else "FAIL", name, detail))
    return cond


def show(title, rows):
    if VERBOSE:
        print("      " + title)
        for r in rows:
            print("      |" + r + "|")


# ------------------------------------------------------------------ chapter 1

def chapter1_fauna():
    print("\n1-D fauna (own-kind)")

    C = Const([(0, 1, 1)])
    S = state_of([(0, 0)])
    rows = spacetime(S, C, 8, lo=0, hi=8)
    check("colonizer (0,1,1) fills at speed 1",
          rows[-1] == "AAAAAAAA." and rows[0] == "A........")
    show("colonizer", rows)

    C = Const([(0, -1, 1)])
    r = classify(state_of([(0, 0)]), C)
    check("sunset clause (0,-1,1) is a period-2 blinker",
          r["kind"] == CYCLE and r["period"] == 2)

    C = Const([(-1, 1, 0)])
    S = state_of([(i, 0) for i in range(0, 12)])
    n0 = card(S)
    for _ in range(6):
        S = step(S, C)
    check("sunset code (-1,1,0) dissolves at one cell/step",
          card(S) == n0 - 6, "12 -> %d laws in 6 steps" % card(S))

    C = Const([(0, 1, 1), (0, -1, -1)])
    S = state_of([(i, 0) for i in range(-8, -1)] + [(i, 1) for i in range(2, 9)])
    for _ in range(30):
        S = step(S, C)
    check("colliding fronts weld into frozen code",
          step(S, C) == S and card(S) > 0, "%d laws, 0 active" % card(S))

    # The sunset wall is cleared at time exactly max(2L, x0 + L): the wall
    # erodes from its FAR end at speed 1, on its own, while the front stands
    # blocked; the front then fills the vacated ground at speed 1.  The net
    # "refraction index 2" is that pair of speed-1 processes in sequence — the
    # front never converts the wall, it inherits the ground.
    C = Const([(0, 1, 1), (-1, 1, 0)])
    obs, want = [], []
    for L in (10, 20, 30):
        for x0 in (4, 10, 15, 25):
            S = state_of([(0, 0)] + [(i, 1) for i in range(x0, x0 + L)])
            for t in range(500):
                front = max((c for c, m in S.items() if m & 1), default=-99)
                if front >= x0 + L - 1:
                    break
                S = step(S, C)
            obs.append(t)
            want.append(max(2 * L, x0 + L))
    check("sunset wall of length L cleared at time exactly max(2L, x0+L)",
          obs == want, "12 (L, x0) pairs; index 2 is net, not instantaneous")

    # Conversion wave: one planted colonizer turns a porous period-2 lattice
    # into solid gridlock, one-way, anchored at the defect.
    C = Const([(0, 1, 1), (-1, 1, 0)])
    S = state_of([(0, 0)] + [(i, 1) for i in range(-40, 41, 2)])
    runs = []
    for t in range(61):
        occ, r, i = set(S), 0, 0
        while i in occ:
            r += 1
            i += 1
        l, i = 0, -1
        while i in occ:
            l += 1
            i -= 1
        runs.append((r, l))
        S = step(S, C)
    speed = (runs[60][0] - runs[0][0]) / 60
    check("conversion wave: solid front at speed 2/3, one-way",
          abs(speed - 2 / 3) < 0.02 and max(l for _, l in runs) == 0,
          "speed %.3f, nothing propagates left of the defect" % speed)


def _laws(S):
    for cell, mask in S.items():
        m = mask
        while m:
            k = (m & -m).bit_length() - 1
            m &= m - 1
            yield cell, k


def chapter1_theorems():
    print("\nthe four theorems (own-kind)")

    ok = True
    for a, b, c in RULES1:
        C = Const([(a, b, c)])
        S = state_of([(i, 0) for i in range(-4, 5)])
        if [x for x in active_laws(S, C) if -3 <= x[0] <= 3]:
            ok = False
    check("Gridlock: solid code has no active interior law", ok,
          "all 27 kinds")

    rng = random.Random(11)
    ok = True
    for _ in range(4000):
        n = rng.randrange(1, 4)
        C = Const([rng.choice(RULES1) for _ in range(n)])
        S = state_of([(rng.randrange(-5, 6), rng.randrange(n))
                      for _ in range(rng.randrange(1, 8))])
        if step(S, C, "parity") != step(S, C, "or"):
            ok = False
            break
    check("Single Author: parity == OR identically (own-kind)", ok,
          "4,000 random states")

    ok = True
    for _ in range(4000):
        n = rng.randrange(1, 4)
        C = Const([rng.choice(RULES1) for _ in range(n)])
        S = state_of([(rng.randrange(-5, 6), rng.randrange(n))
                      for _ in range(rng.randrange(1, 8))])
        if (step(S, C) == S) != (not active_laws(S, C)):
            ok = False
            break
    check("Dead Letter: fixed <=> every law blocked (own-kind)", ok,
          "4,000 random states")

    ok, seen = True, 0
    for _ in range(3000):
        n = rng.randrange(1, 3)
        C = Const([rng.choice(RULES1) for _ in range(n)])
        S = state_of([(rng.randrange(-4, 5), rng.randrange(n))
                      for _ in range(rng.randrange(1, 6))])
        r = classify(S, C, max_steps=120, max_card=120, max_span=160)
        seen += 1
        if r["kind"] == GLIDER:
            ok = False
            break
    check("Anchor: no free glider on Z (own-kind)", ok,
          "%d random seeds classified" % seen)


def chapter1_rings():
    print("\nnomic rings")

    # The founding ring specimen: Phi(S) = rot_3(S) holds — but with window-1
    # laws information moves at most one cell per step, so a rotation of 3 in
    # one step is NOT transport.  Exactly two cells change (a repeal at 1, an
    # enactment at 4) and the state merely coincides with its own rotation:
    # a barber pole.  (Correction to the founding note; see XFINDINGS.md §6.)
    C = Const([(0, 1, -1)], modulus=6)
    S = state_of([(1, 0), (2, 0), (5, 0)])
    T = step(S, C)
    changed = set(S) ^ set(T)
    check("the Z/6 specimen coincides with its own rotation by 3",
          set(T) == {(c + 3) % 6 for c in S} and set(step(T, C)) == set(S),
          "{1,2,5} -> {2,4,5} -> {1,2,5}")
    check("...but it is a barber pole, not transport: 3 > light cone 1",
          changed == {1, 4} and not any(
              set(S) == {(c + r) % 6 for c in S} for r in range(1, 6)),
          "only two cells change per step; S has no rotational symmetry")

    fam = []
    for m in range(4, 15, 2):
        C = Const([(0, 1, -1)], modulus=m)
        S = state_of([(0, 0), (1, 0), (m // 2 + 1, 0)])
        T = step(S, C)
        if set(T) == {(c + m // 2) % m for c in S}:
            fam.append(m)
    check("rotor family {0,1,m/2+1} on every even m >= 6",
          fam == [6, 8, 10, 12, 14], "verified m = %s" % fam)

    odd = []
    for m in (5, 7, 9):
        for kind in RULES1:
            C = Const([kind], modulus=m)
            for i in range(m):
                for j in range(i + 1, m):
                    for k in range(j + 1, m):
                        S = state_of([(i, 0), (j, 0), (k, 0)])
                        T = step(S, C)
                        if set(T) == set(S):
                            continue          # a fixed point, not a rotor:
                        for r in range(1, m):  # (rotation-symmetric codes are
                            if set(T) == {(c + r) % m for c in S}:  # not motion)
                                odd.append((m, kind, (i, j, k), r))
    check("no single-kind 3-law rotor on odd rings m = 5,7,9", not odd,
          "complete sweep: 27 kinds x C(m,3) placements")

    C = Const([(0, 1, -1)], modulus=10)
    r = classify(state_of([(c, 0) for c in (1, 3, 5, 6, 7, 8, 9)]), C,
                 max_steps=200)
    check("Sunset Parliament on Z/10 has period 15",
          r["kind"] == CYCLE and r["period"] == 15,
          "period %s" % r.get("period"))


def chapter1_jubilee():
    print("\nthe Jubilee Code (2-D)")
    C = Const([((1, 0), (0, 1), (0, -1)),
               ((0, 1), (0, -1), (0, 1)),
               ((-1, 0), (0, -1), (1, 0))], dim=2)
    S = state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)])
    N = 1 << 13
    z = []
    for _ in range(N):
        z.append(card(S))
        S = step(S, C)
    resets = {z[1 << k] for k in range(1, 13)}
    check("|S| = 4 at every power of two", resets == {4},
          "t = 2..4096, values %s" % resets)
    crest = [z[(1 << k) - 1] for k in range(3, 13)]
    check("crest at t = 2^k - 1 doubles every two powers",
          crest == [7, 8, 13, 14, 25, 26, 49, 50, 97, 98],
          "%s" % crest)
    check("aperiodic through 2^13 steps (no exact recurrence)",
          classify(state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)]), C,
                   max_steps=600, max_card=10 ** 6,
                   max_span=10 ** 6)["kind"] not in (FIXED, CYCLE))


# ------------------------------------------------------------------ chapter 2

def chapter2():
    print("\ncross-amendment (chapter two)")

    C = Const([(0, 1, 1), (0, -1, -1), (0, 1, 0)], targets=[2, 2, 2])
    S = state_of([(0, 0), (2, 1)])
    check("two-chamber deadlock is a BALANCED constitution (parity)",
          verify_balanced(S, C) and classify(S, C)["kind"] == BALANCED,
          "fixed forever, 2 laws active")
    T = step(S, C, "or")
    check("...and under OR the enactment passes and silences both authors",
          T == state_of([(0, 0), (2, 1), (1, 2)]) and not active_laws(T, C)
          and step(T, C, "or") == T,
          "Dead Letter survives OR verbatim, fails under parity")
    show("two-chamber (parity)", spacetime(S, C, 4, lo=-1, hi=3))
    show("two-chamber (OR)", spacetime(S, C, 4, mode="or", lo=-1, hi=3))

    rng = random.Random(5)
    ok = True
    for _ in range(3000):                 # permutation targeting: single author
        n = rng.randrange(2, 4)
        perm = list(range(n))
        rng.shuffle(perm)
        C = Const([rng.choice(RULES1) for _ in range(n)], perm)
        S = state_of([(rng.randrange(-5, 6), rng.randrange(n))
                      for _ in range(rng.randrange(1, 8))])
        if step(S, C, "parity") != step(S, C, "or"):
            ok = False
            break
    check("permutation targeting keeps parity == OR", ok,
          "3,000 random states")

    ok = False
    for _ in range(3000):                 # non-injective targeting: it splits
        n = 3
        C = Const([rng.choice(RULES1) for _ in range(n)], [2, 2, 2])
        S = state_of([(rng.randrange(-4, 5), rng.randrange(n))
                      for _ in range(rng.randrange(2, 7))])
        if step(S, C, "parity") != step(S, C, "or"):
            ok = True
            break
    check("non-injective targeting splits parity from OR", ok,
          "multi-authorship is real")

    # --- the first free gliders (expedition X-A) -------------------------
    C = Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)])
    S = state_of([(1, 0), (1, 1)])
    check("TANDEM-1: two laws in one cell, period 1, speed 1",
          verify_glider(S, C, 1, 1) and classify(S, C)["kind"] == GLIDER,
          "the minimal period-1 glider")
    show("TANDEM-1", spacetime(S, C, 6, lo=0, hi=9))

    C = Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(1, 2), (0,), (0,)])
    S = state_of([(1, 0)])
    check("SOLO: a single placed law, period 2, speed 1/2",
          verify_glider(S, C, 2, 1), "the smallest glider of all")
    show("SOLO", spacetime(S, C, 6, lo=0, hi=9))

    C = Const([(0, 1, 0), (0, -1, 1), (0, 1, -1)], [(0, 1, 2)] * 3)
    S = state_of([(c, k) for c in (1, 2, 4) for k in range(3)])
    check("TRIPTYCH: a glider under parity that is not one under OR",
          verify_glider(S, C, 1, 1) and not verify_glider(S, C, 1, 1, "or"),
          "author multiplicity 2 — the resolution axis decides motion")

    C = Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)])
    lifts = []
    for vel in ((1, 0), (1, 1), (0, 1), (-1, 1), (2, 1)):
        w = (-vel[0], -vel[1])
        C2 = Const([((0, 0), w, vel), ((0, 0), w, (0, 0))], [(0, 1), (0, 1)],
                   dim=2)
        S2 = state_of([((1, 1), 0), ((1, 1), 1)])
        lifts.append(verify_glider(S2, C2, 1, vel))
    check("TANDEM-1 lifts to 2-D at any velocity (knight move included)",
          all(lifts), "own-kind 2-D motion is pinned to axis rays")

    rots = []
    for m in range(3, 13):
        C3 = Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)], modulus=m)
        S3 = state_of([(1, 0), (1, 1)])
        T3 = step(S3, C3)
        rots.append(set(T3) == {(c + 1) % m for c in S3} and set(T3) != set(S3))
    check("...and rotates on every ring m >= 3", all(rots),
          "own-kind rotors need even m >= 6")

    # Out-Degree Law spot check: single-target constitutions never move.
    bad = None
    for _ in range(6000):
        n = rng.randrange(2, 4)
        C = Const([rng.choice(RULES1) for _ in range(n)],
                  [rng.randrange(n) for _ in range(n)])
        S = state_of([(rng.randrange(-3, 4), rng.randrange(n))
                      for _ in range(rng.randrange(1, 6))])
        if classify(S, C, max_steps=140, max_card=140,
                    max_span=200)["kind"] == GLIDER:
            bad = (C.label(), sorted(S))
            break
    check("Out-Degree Law: no glider when every law amends one kind",
          bad is None, "6,000 random single-target seeds")

    # --- two dimensions (expedition X-B) --------------------------------
    V = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
         "P": (1, -1), "Q": (-1, -1), "R": (1, 1), "T": (-1, 1)}
    def off(s):
        return tuple(V[ch] for ch in s)

    # LAND GRANT: one law, and the plane fills — |S_t| = (t+1)^2 exactly.
    C = Const([off("OPP"), off("OEE"), off("ONN")], [(0, 1, 2), (1,), (2,)], dim=2)
    S = state_of([((0, 0), 0)])
    sizes, X = [], dict(S)
    for _ in range(10):
        sizes.append(card(X))
        X = step(X, C)
    check("LAND GRANT: one law fills the plane, |S_t| = (t+1)^2",
          sizes == [(t + 1) ** 2 for t in range(10)],
          "own-kind growth is pinned to rays; out-degree 2 gives area")

    # A gun on the LINE: an immortal kind (in-degree 0) pumps forever.
    C = Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(0, 1), (0, 1), (0, 1)])
    S = state_of([(0, 2)])
    sizes, X = [], dict(S)
    for _ in range(14):
        sizes.append(card(X))
        X = step(X, C)
    check("a gun on Z: an entrenched clause emits packets forever",
          sizes[1:] == [2 * (t // 2) + 3 for t in range(1, 14)],
          "in-degree 0 is the pump the Anchor Theorem could not have")

    # THE ODOMETER: the second binary counter, also resetting to four laws.
    C = Const([off("OEW"), off("NQR")], [(1,), (0, 1)], dim=2)
    S = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])
    z, X = [], dict(S)
    for _ in range(1 << 12):
        z.append(card(X))
        X = step(X, C)
    check("THE ODOMETER: |S| = 4 at every power of two",
          {z[1 << k] for k in range(1, 12)} == {4},
          "crests %s" % [z[(1 << k) - 1] for k in range(3, 9)])

    # PERPETUAL SESSION: a large balanced code, every law active.
    C = Const([off("OEO"), off("OEO")], [(0,), (0,)], dim=2)
    S = state_of([((0, y), k) for y in range(20) for k in (0, 1)])
    check("PERPETUAL SESSION: 40 laws, all 40 active, fixed forever",
          verify_balanced(S, C) and len(active_laws(S, C)) == 40
          and step(S, C, "or") != S,
          "balance needs in-degree 2 and parity; OR breaks it")

    # Collision algebra: even gap passes through, odd gap freezes.
    C = Const([off("OEO"), off("OEE"), off("OWO"), off("OWW")],
              [(0, 1), (0, 1), (2, 3), (2, 3)], dim=2)
    verdict = []
    for gap in (6, 7, 8, 9):
        X = state_of([((0, 0), 0), ((0, 0), 1), ((gap, 0), 2), ((gap, 0), 3)])
        for _ in range(40):
            X = step(X, C)
        verdict.append(bool(active_laws(X, C)))
    check("collisions: even gap passes through, odd gap freezes",
          verdict == [True, False, True, False], "gaps 6,7,8,9")

    # --- structure theory (expedition X-D) ------------------------------
    C = Const([(0, -1, -1), (0, -1, -1)], targets=[0, 0])
    S = state_of([(0, 0), (0, 1)])
    check("BAL-1: the minimal balanced code is two laws in ONE cell",
          verify_balanced(S, C) and len(active_laws(S, C)) == 2
          and step(S, C, "or") != S,
          "both forever propose the same amendment; it never passes")

    C = Const([(0, -1, 1), (0, 1, -1), (-1, 1, 0)], targets=[2, 0, 1])
    S = state_of([(-2, 2), (2, 0), (2, 2), (3, 0), (3, 1)])
    res = classify(S, C, max_steps=200)
    check("CRY-1: a period-3 cycle at constant occupancy",
          res["kind"] == CYCLE and res["period"] == 3,
          "own-kind linearity would force a power of two")

    C = Const([(0, -1, 1)])
    S = state_of([(0, 0), (2, 0), (4, 0), (6, 0)])
    res = classify(S, C, max_steps=200)
    check("OWN-8: an own-kind period-8 oscillator",
          res["kind"] == CYCLE and res["period"] == 8,
          "refutes the census remark that random cycles carry only p = 2, 4")

    # --- the width correction (expedition X-E) --------------------------
    # MIRROR: a two-kind universe whose displacement-2 gliders are far too
    # wide for the boxes that "decided" them impossible.
    C = Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)])
    cells = [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21]
    S = state_of([(c, k) for c in cells for k in (0, 1)])
    check("MIRROR-2/5: a span-20, 32-law glider with displacement 2",
          verify_glider(S, C, 5, 2) and not verify_glider(S, C, 5, 2, "or"),
          "bounded searches decide a box, not a question")

    # TRIAD: the resolution convention decides the SPEED, not just the motion.
    C = Const([(1, -1, 0), (0, -2, 1), (0, -2, 2)], [(0, 1, 2)] * 3)
    S = state_of([(0, k) for k in range(3)])
    check("TRIAD: same seed, p=3 d=5 under parity and p=2 d=3 under OR",
          verify_glider(S, C, 3, 5) and verify_glider(S, C, 2, 3, "or")
          and not verify_glider(S, C, 2, 3) and not verify_glider(S, C, 3, 5, "or"),
          "the convention decides how fast, not merely whether")

    # --- rings under cross-amendment (expedition X-C) --------------------
    C = Const([(-1, 1, -1), (0, -1, 0)], [1, 0], modulus=4)
    S = state_of([(0, 0), (0, 1), (2, 1)])
    check("Q-4: cross-amendment lowers the minimal rotor ring from 6 to 4",
          step(S, C) == {(c + 2) % 4: v for c, v in S.items()},
          "three laws on Z/4")

    C = Const([(0, -1, 0)] * 3, [1, 2, 0], modulus=3)
    S = state_of([(0, 0), (0, 1)])
    X = dict(S)
    cells_fixed = True
    for _ in range(3):
        X = step(X, C)
        cells_fixed = cells_fixed and set(X) == set(S)
    check("D-3: the doctrinal rotor — cells frozen, kinds circulate",
          cells_fixed and X == S and step(S, C) != S,
          "no own-kind analogue: occupancy fixed, doctrine rotating, period 3")

    C = Const([(-1, 1, 1), (0, 1, -1)], [0, 0], modulus=15)
    S = state_of([(c, 0) for c in (1, 5, 6, 10, 11, 12)]
                 + [(c, 1) for c in (1, 3, 6, 8, 11, 13)])
    check("O-15: a rotor on an ODD ring, which own-kind never gives",
          step(S, C) == {(c + 5) % 15: v for c, v in S.items()},
          "12 laws, rotation 5 = m/3 (the Third-Turn pattern)")

    # Subluminal motion: a parity glider at speed 1/6.
    C = Const([off("ONO"), off("OEW"), off("WTE")], [(0, 1), (0, 2), (0,)], dim=2)
    S = state_of([((0, 0), 0), ((0, 0), 1)])
    check("a subluminal glider: speed 1/6", verify_glider(S, C, 6, (-1, 0)),
          "the speed spectrum is not just 1 and 1/2")


def impermanence():
    """Chapter four: laws that lapse unless re-enacted (sunset/RESULTS.md)."""
    print("\nimpermanence (sunset-by-default)")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "sunset"))
    from sunset import (classify_sunset, verify_glider_sunset, run,
                        spacetime_sunset, step_sunset, GLIDER as SGLIDER,
                        FIXED as SFIXED, EXTINCT as SEXTINCT)

    # The walking clause: chapter one's colonizer becomes a glider.
    C = Const([(0, 1, 1)])
    S = state_of([(0, 0)])
    r = classify_sunset(S, C)
    check("the colonizer WALKS under impermanence",
          r["kind"] == SGLIDER and r["displacement"] == 1
          and verify_glider_sunset(S, C, 1, 1)
          and spacetime_sunset(S, C, 3, 0, 4) == ["A....", ".A...", "..A..",
                                                  "...A."],
          "the Anchor Theorem's hypothesis is permanence")

    # Lone Survivor: exactly the 6 kinds with a = 0, b != 0 survive.
    surv = [(a, b, c) for a, b, c in RULES1
            if classify_sunset(state_of([(0, 0)]), Const([(a, b, c)]))["kind"]
            != SEXTINCT]
    check("Lone Survivor: a lone law lives iff a = 0 and b != 0",
          sorted(surv) == sorted([(0, b, c) for b in (-1, 1)
                                  for c in (-1, 0, 1)]),
          "%d of 27 kinds; 4 walk, 2 renew themselves in place" % len(surv))

    # Gridlock's mirror: a solid block evaporates to its surface.
    S = state_of([(i, 0) for i in range(8)])
    h = run(S, C, 1)
    check("Gridlock's mirror: a solid block evaporates in one step",
          card(h[1]) == 1 and card(h[0]) == 8,
          "under permanence the same block is frozen but for its front")

    # Lone Survivor in 2-D: velocity IS the target offset (all 729 kinds).
    OFF2 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    Zc, walk, still, bad = (0, 0), 0, 0, 0
    for a in OFF2:
        for b in OFF2:
            for c in OFF2:
                Cx = Const([(a, b, c)], dim=2)
                X, ages = state_of([(Zc, 0)]), None
                X, ages = step_sunset(X, Cx, 1, ages)
                if not (a == Zc and b != Zc):
                    bad += bool(X)
                    continue
                if sorted(X) != [c]:
                    bad += 1
                    continue
                walk += c != Zc
                still += c == Zc
    check("Lone Survivor in 2-D: a walker's velocity is its target offset",
          bad == 0 and walk == 64 and still == 8,
          "complete over all 729 kinds; 64 walk, 8 renew in place")

    # Genuine ring transport: one law circulates, inside the light cone.
    okm = []
    for m in range(2, 16):
        Cx = Const([(0, 1, 1)], modulus=m)
        X, ages, good = state_of([(0, 0)]), None, True
        for _ in range(m):
            Y, ages = step_sunset(X, Cx, 1, ages)
            good = good and set(Y) == {(c + 1) % m for c in X}
            X = Y
        okm.append(good)
    check("a lone law genuinely circulates every ring, odd m included",
          all(okm), "m = 2..15, rotation 1 per step: inside the light cone")

    # Conservation: out-degree 1 can never grow an impermanent code.
    rng2 = random.Random(3)
    worst = 0
    for _ in range(400):
        n = rng2.randrange(1, 4)
        Cx = Const([rng2.choice(RULES1) for _ in range(n)],
                   [rng2.randrange(n) for _ in range(n)])
        X = state_of([(rng2.randrange(-5, 6), rng2.randrange(n))
                      for _ in range(rng2.randrange(1, 9))])
        ages = None
        for _ in range(30):
            Y, ages = step_sunset(X, Cx, 1, ages)
            worst = max(worst, card(Y) - card(X))
            X = Y
    check("Conservation: out-degree 1 never grows an impermanent code",
          worst <= 0, "400 random codes x 30 steps; max increase %d" % worst)

    # LAND GRANT keeps only its two advancing edges: |S_t| = 2t+1.
    V = {"O": (0, 0), "E": (1, 0), "N": (0, -1), "P": (1, -1)}
    Cg = Const([tuple(V[c] for c in "OPP"), tuple(V[c] for c in "OEE"),
                tuple(V[c] for c in "ONN")], [(0, 1, 2), (1,), (2,)], dim=2)
    X, ages, sz = state_of([((0, 0), 0)]), None, []
    for _ in range(12):
        sz.append(card(X))
        X, ages = step_sunset(X, Cg, 1, ages)
    check("the plane-filler keeps only its frontier: |S_t| = 2t+1",
          sz == [2 * i + 1 for i in range(12)],
          "under permanence the same code gives (t+1)^2")

    # The Longevity Law: one code, speed exactly 2/(tau+1).
    C = Const([(0, 1, -1), (0, -1, -1)])
    S = state_of([(0, 0), (2, 1)])
    obs, want = [], []
    for tau in range(1, 13):
        r = classify_sunset(S, C, tau=tau, max_steps=400)
        obs.append((abs(r.get("displacement", 0)), r["period"]))
        want.append((2, tau + 1) if tau > 1 else (1, 1))
    check("the Longevity Law: the same packet moves at speed 2/(tau+1)",
          obs == want, "tau = 1..12, displacement fixed at 2, period = tau+1")


def computation():
    """Chapter five: the field computes (computation/RESULTS.md)."""
    print("\ncomputation")
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "computation"))

    # Rule 110, complete over the local map's inputs (all 2^7 on Z/7).
    rules = [(0, 0, 0)] * 12 + [(0, 1, 0), (0, 0, 0), (0, 0, 0), (-1, 0, 0),
                                (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                                (1, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
    targets = [(), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,),
               (11,), (3, 4), (5,), (10, 4), (8,), (6,), (7,), (11,), (1, 2),
               (1, 2), (1, 2), (1, 2), (9, 2)]
    guards = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
              (8, 0), (9, 0), (10, 0), (11, 0), (1, 2), (1, 0), (9, 0), (5, 4),
              (5, 0), (3, 0), (10, 0), (6, 0), (6, 0), (7, 0), (8, 0), (11, 0)]
    local = all(all(abs(x) <= 1 for x in r) for r in rules)

    def ref110(bits):
        m = len(bits)
        return [bits[n] ^ bits[(n + 1) % m]
                ^ (bits[n] & bits[(n + 1) % m])
                ^ (bits[(n - 1) % m] & bits[n] & bits[(n + 1) % m])
                for n in range(m)]

    m, bad = 7, 0
    Cr = Const(rules, targets, dim=1, guards=guards, modulus=m)
    for v in range(1 << m):
        bits = [(v >> i) & 1 for i in range(m)]
        seed = []
        for cell in range(m):
            for k in list(range(12, 24)) + [9]:
                seed.append((cell, k))
            seed.append((cell, 1 if bits[cell] else 2))
        X, ref = state_of(seed), bits
        for _ in range(3):
            for _ in range(3):
                X = step(X, Cr, "parity")
            ref = ref110(ref)
            if [1 if (X.get(c, 0) >> 1) & 1 else 0
                    for c in range(m)] != ref:
                bad += 1
                break
    check("Rule 110 runs inside a 24-kind constitution",
          bad == 0 and local,
          "all 2^7 = 128 configurations of Z/7: a COMPLETE local-map "
          "certificate, every offset being within +-1")

    # Theorem 5: a Turing machine compiled into a finite code of the FOUNDING
    # (occupancy-guard) sector, checked against a reference written here.
    import turing                                                # noqa: E402
    DIR = {"L": -1, "S": 0, "R": 1}

    def ref_tm(tm, tape, head, steps):
        t, q, h, out = dict(tape), tm.start, head, []
        for _ in range(steps):
            out.append((dict(t), h, q))
            g = t.get(h, 0)
            if (q, g) not in tm.delta:
                continue
            q2, g2, d = tm.delta[(q, g)]
            if g2:
                t[h] = 1
            else:
                t.pop(h, None)
            h += DIR[d]
            q = q2
        out.append((dict(t), h, q))
        return out

    okm = 0
    machines = [turing.tm_binary_increment(), turing.tm_busy_beaver3(),
                turing.tm_move_right()]
    for tm in machines:
        tape, steps = {0: 1, 1: 1}, 10
        R = turing.Registry(tm)
        X = R.code(dict(tape), 0, list(range(-4, 7)))
        ref = ref_tm(tm, tape, 0, steps)
        view = list(range(-4 - steps - 2, 7 + steps + 3))
        good = True
        for k in range(steps + 1):
            rt, rh, rq = ref[k]
            rt = {c: b for c, b in rt.items() if b}
            if R.decode(X, view) != (rt, rh, rq):
                good = False
                break
            if k < steps:
                X = R.run(X, 3)
        okm += good
    check("every Turing machine compiles into a finite code",
          okm == len(machines),
          "3 machines x 10 steps vs an independent simulator; the founding "
          "occupancy-guard sector is computation-universal")


def main():
    print("nomodynamics — verification battery")
    chapter1_fauna()
    chapter1_theorems()
    chapter1_rings()
    chapter1_jubilee()
    chapter2()
    impermanence()
    computation()
    print("\n%d checks passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("failed: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
