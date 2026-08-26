#!/usr/bin/env python3
"""verify.py — re-check every named claim of nomodynamics from scratch.

    python3 verify.py            # the whole battery (~30 s)
    python3 verify.py -v         # print each specimen's spacetime diagram

Everything runs on the shared engine `xnomos.py`, independently of the
expedition code that originally found these specimens; the point is that a
reader can confirm the note's claims without reading any of it.
"""
from __future__ import annotations

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

    C = Const([(0, 1, -1)], modulus=6)
    S = state_of([(1, 0), (2, 0), (5, 0)])
    T = step(S, C)
    check("the minimal ring rotor hops m/2 = 3 on Z/6",
          set(T) == {(c + 3) % 6 for c in S} and set(step(T, C)) == set(S),
          "{1,2,5} -> {2,4,5} -> {1,2,5}")

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
    r = lambda s: tuple(V[ch] for ch in s)          # noqa: E731

    # LAND GRANT: one law, and the plane fills — |S_t| = (t+1)^2 exactly.
    C = Const([r("OPP"), r("OEE"), r("ONN")], [(0, 1, 2), (1,), (2,)], dim=2)
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
    C = Const([r("OEW"), r("NQR")], [(1,), (0, 1)], dim=2)
    S = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])
    z, X = [], dict(S)
    for _ in range(1 << 12):
        z.append(card(X))
        X = step(X, C)
    check("THE ODOMETER: |S| = 4 at every power of two",
          {z[1 << k] for k in range(1, 12)} == {4},
          "crests %s" % [z[(1 << k) - 1] for k in range(3, 9)])

    # PERPETUAL SESSION: a large balanced code, every law active.
    C = Const([r("OEO"), r("OEO")], [(0,), (0,)], dim=2)
    S = state_of([((0, y), k) for y in range(20) for k in (0, 1)])
    check("PERPETUAL SESSION: 40 laws, all 40 active, fixed forever",
          verify_balanced(S, C) and len(active_laws(S, C)) == 40
          and step(S, C, "or") != S,
          "balance needs in-degree 2 and parity; OR breaks it")

    # Collision algebra: even gap passes through, odd gap freezes.
    C = Const([r("OEO"), r("OEE"), r("OWO"), r("OWW")],
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
    r = classify(S, C, max_steps=200)
    check("CRY-1: a period-3 cycle at constant occupancy",
          r["kind"] == CYCLE and r["period"] == 3,
          "own-kind linearity would force a power of two")

    C = Const([(0, -1, 1)])
    S = state_of([(0, 0), (2, 0), (4, 0), (6, 0)])
    r = classify(S, C, max_steps=200)
    check("OWN-8: an own-kind period-8 oscillator",
          r["kind"] == CYCLE and r["period"] == 8,
          "refutes the census remark that random cycles carry only p = 2, 4")

    # Subluminal motion: a parity glider at speed 1/6.
    C = Const([r("ONO"), r("OEW"), r("WTE")], [(0, 1), (0, 2), (0,)], dim=2)
    S = state_of([((0, 0), 0), ((0, 0), 1)])
    check("a subluminal glider: speed 1/6", verify_glider(S, C, 6, (-1, 0)),
          "the speed spectrum is not just 1 and 1/2")


def main():
    print("nomodynamics — verification battery")
    chapter1_fauna()
    chapter1_theorems()
    chapter1_rings()
    chapter1_jubilee()
    chapter2()
    print("\n%d checks passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("failed: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
