#!/usr/bin/env python3
"""
verify_replication.py — re-checks every claim of replication/RESULTS.md.

Everything is re-derived from `xnomos.py` and cross-checked against
`replib.pstep`, an engine written independently on frozensets of placed laws.

Run:  python3 verify_replication.py         (~20 s)
      python3 verify_replication.py -v      (with spacetime frames)
"""

from __future__ import annotations

import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from xnomos import Const, state_of, step, card, active_laws, laws     # noqa
from replib import (radius, to_p, from_p, pstep, certify, shift, supp,  # noqa
                    dist_inf, contains, diff, frame2d, frame1d,
                    superposes, linearity_report, cross_check)
from analyze import copy_census, linear_map                            # noqa
import constructor                                                     # noqa
import scribe                                                          # noqa

VERBOSE = "-v" in sys.argv
OK = [0]
BAD = [0]


def check(label, cond, extra=""):
    (OK if cond else BAD)[0] += 1
    print("  [%s] %s%s" % ("ok " if cond else "FAIL", label,
                           ("   " + extra) if extra else ""))
    return cond


# --------------------------------------------------------------- specimens

O = (0, 0); E = (1, 0); W = (-1, 0); N = (0, 1)

ENGROSSMENT = Const([((0, -1), (-1, 1), (1, 1)),
                     ((0, -1), (0, 1), (1, 0))], [(0, 1), (0, 1)], dim=2)
ENGROSSMENT_SEED = state_of([((0, 0), 0), ((0, 0), 1),
                             ((0, 1), 0), ((0, 1), 1)])

MOOT = Const([(O, N, E), (O, N, W)], [(0, 1), (0, 1)], dim=2)
MOOT_SEED = state_of([((0, 0), 0), ((0, 0), 1), ((2, 0), 0), ((2, 0), 1)])

PASCAL = Const([(O, E, N)], dim=2)
PASCAL_SEED = state_of([((0, 0), 0)])

SPLIT = Const([((0, 0), (-1, -1), (0, -1)), ((0, 0), (1, 0), (0, 1))],
              [(0, 1), (0, 1)], dim=2, guards=[(1, 0), (1, None)])
SPLIT_SEED = state_of([((0, 0), 0), ((0, 0), 1), ((2, 0), 0), ((2, 0), 1)])

QUORUM = Const([((-1, -1), (0, -1), (1, -1)),
                ((0, 0), (0, -1), (1, -1))], [(0, 1), (0, 1)], dim=2)
QUORUM_SEED = state_of([((0, 0), 1), ((1, 1), 0)])

PHANTOM = Const([(0, 0, 1), (0, 0, -1), (0, 0, 0)], [(0, 1), (0, 1), (2,)],
                dim=1, guards=[(None, 2), (None, 2), (None, None)])
PHANTOM_SEED = state_of([(0, 0), (0, 1), (2, 0), (2, 1)])


def exact_events(C, S0, mode, T):
    R = radius(C)
    S = dict(S0)
    ev = []
    for t in range(1, T + 1):
        S = step(S, C, mode)
        if not S or card(S) > 8000:
            break
        nc, ng, deb, anch = copy_census(S, S0, C, R)
        if nc >= 2 and deb == 0:
            ev.append((t, nc, tuple(anch)))
    return ev


def phi_ne_L(C, S0, mode, T):
    S = dict(S0)
    L = dict(S0)
    n = 0
    for _ in range(T):
        S = step(S, C, mode)
        L = linear_map(L, C)
        if S != L:
            n += 1
    return n


def split_fail(C, S0, mode, p):
    pl = list(laws(S0))
    Q = to_p(S0)
    for _ in range(p):
        Q = pstep(Q, C, mode)
    f = t = 0
    for r in range(1, len(pl) // 2 + 1):
        for A in itertools.combinations(pl, r):
            Ad, Bd = {}, {}
            for c, k in A:
                Ad[c] = Ad.get(c, 0) | (1 << k)
            for c, k in pl:
                if (c, k) not in A:
                    Bd[c] = Bd.get(c, 0) | (1 << k)
            if not Bd:
                continue
            PA, PB = to_p(Ad), to_p(Bd)
            for _ in range(p):
                PA = pstep(PA, C, mode)
                PB = pstep(PB, C, mode)
            t += 1
            if Q != (PA ^ PB):
                f += 1
    return f, t


# ------------------------------------------------------------------- checks

def sec(t):
    print("\n%s" % t)


def main():
    sec("0. engines")
    rng = random.Random(3)
    OFFS = (-1, 0, 1)
    agree = True
    for _ in range(200):
        n = rng.randrange(1, 4)
        C = Const([(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                   for _ in range(n)],
                  [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                   for _ in range(n)], dim=1,
                  guards=[(rng.choice([None] + list(range(n))),
                           rng.choice([None] + list(range(n))))
                          for _ in range(n)])
        S = {rng.randrange(-4, 5): rng.randrange(1, 1 << n)
             for _ in range(rng.randrange(1, 5))}
        for m in ("parity", "or", "super", "super_or"):
            agree &= cross_check(S, C, m, 10)
    check("xnomos.step and replib.pstep agree, 200 random constitutions "
          "x 4 modes x 10 steps", agree)

    sec("1. Lemma S (separation => independence), measured")
    good = True
    for _ in range(400):
        n = rng.randrange(1, 4)
        C = Const([(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                   for _ in range(n)],
                  [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                   for _ in range(n)], dim=1)
        A = {rng.randrange(-3, 4): rng.randrange(1, 1 << n)
             for _ in range(rng.randrange(1, 4))}
        B = {rng.randrange(-3, 4) + 40: rng.randrange(1, 1 << n)
             for _ in range(rng.randrange(1, 4))}
        for m in ("parity", "or", "super", "super_or"):
            lhs = pstep(to_p(A) | to_p(B), C, m)
            good &= (lhs == (pstep(to_p(A), C, m) | pstep(to_p(B), C, m)))
    check("Phi(A u B) = Phi(A) u Phi(B) at sup-distance > 2R, 400 x 4", good)

    sec("2. Theorem A (light cone / polynomial population bound), measured")
    good = True
    for _ in range(300):
        n = rng.randrange(1, 4)
        C = Const([(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                   for _ in range(n)],
                  [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                   for _ in range(n)], dim=1)
        S = {rng.randrange(-2, 3): rng.randrange(1, 1 << n)
             for _ in range(rng.randrange(1, 4))}
        lo, hi = min(S), max(S)
        R = radius(C)
        for t in range(1, 25):
            S = step(S, C, "parity")
            if not S:
                break
            good &= (min(S) >= lo - R * t and max(S) <= hi + R * t)
            good &= card(S) <= C.n * (hi - lo + 2 * R * t + 1)
    check("supp(S_t) inside the light cone and card <= n*(span+2Rt+1), "
          "300 runs x 25 steps", good)

    sec("3. anti-cheat: a growing solid block is NOT a rung-2 replicator")
    Ccol = Const([(0, 1, 1)])
    blk = state_of([(i, 0) for i in range(4)])
    ev = exact_events(Ccol, blk, "parity", 40)
    check("colonizer block: no causal component is an exact translate of the "
          "seed in 40 steps", ev == [], "events=%s" % ev)
    ok2, info = certify(blk, Ccol, "parity", 4, [0, 4])
    check("colonizer block: certify() rejects the adjacent 'copies'",
          not ok2, info.get("fail", ""))

    sec("4. THE ENGROSSMENT — rung 2 exact, rung 3, non-additive")
    C, S0 = ENGROSSMENT, ENGROSSMENT_SEED
    R = radius(C)
    ok3, info = certify(S0, C, "parity", 4, [(0, 0), (4, 4)])
    check("Phi^4(S) contains S and sigma^(4,4)S, gap %s > 2R=%d, debris %s"
          % (info.get("gaps"), 2 * R, info.get("debris")), ok3 and info["exact"])
    P = to_p(S0)
    for _ in range(4):
        P = pstep(P, C, "parity")
    want = to_p(S0) | to_p(shift(S0, (4, 4), 2))
    check("independent engine: Phi^4(S) EQUALS S u sigma^(4,4)S exactly",
          P == want)
    ev = exact_events(C, S0, "parity", 260)
    counts = [c for _, c, _ in ev]
    check("colony: exact free-copy counts reach %d within t<=260 (rung 3)"
          % max(counts), max(counts) >= 32, "events=%s" % ev[:8])
    check("copy count at t=4m is 2^popcount(m)",
          all(c == 2 ** bin(t // 4).count("1")
              for t, c, _ in ev if t % 4 == 0))
    nd = phi_ne_L(C, S0, "parity", 140)
    check("Phi differs from the unconditional linear map L at every one of "
          "140 steps", nd == 140)
    f, t = split_fail(C, S0, "parity", 4)
    check("superposition FAILS for %d of %d splittings of the seed" % (f, t),
          f > 0)
    nact = len(active_laws(S0, C))
    check("the guard bites at t=0: %d of %d laws active" % (nact, card(S0)),
          nact < card(S0))
    fa = superposes(C, "parity", S0, shift(S0, (60, 60), 2))
    check("far-apart superposition control holds (Lemma S)", fa)
    if VERBOSE:
        S = dict(S0)
        for t in range(6):
            print("      t=%d card=%d" % (t, card(S)))
            for r in frame2d(S, (-1, 7, -1, 6)):
                print("        " + r)
            S = step(S, C, "parity")

    sec("4a. THE SPLIT DECISION — p=2 binary fission, monotone colony")
    ok7, info = certify(SPLIT_SEED, SPLIT, "or", 2, [(0, -2), (0, 2)])
    check("Phi^2(S) = sigma^(0,-2)S u sigma^(0,2)S, gap %s, debris %s -- the "
          "parent does NOT survive" % (info.get("gaps"), info.get("debris")),
          ok7 and info["exact"])
    P = to_p(SPLIT_SEED)
    for _ in range(2):
        P = pstep(P, SPLIT, "or")
    check("independent engine: exact equality",
          P == to_p(shift(SPLIT_SEED, (0, -2), 2)) |
          to_p(shift(SPLIT_SEED, (0, 2), 2)))
    ev = exact_events(SPLIT, SPLIT_SEED, "or", 198)
    check("at EVERY even t the state is exactly t/2+1 free copies "
          "(max %d at t=198)" % max(c for _, c, _ in ev),
          all(c == t // 2 + 1 for t, c, _ in ev) and
          len(ev) == 99 and max(c for _, c, _ in ev) == 100)
    f, t = split_fail(SPLIT, SPLIT_SEED, "or", 2)
    check("superposition fails for %d of %d splittings" % (f, t), f > 0)
    check("the constitution CITES kinds %s" % sorted(SPLIT.cites()),
          SPLIT.cited)

    sec("4b. THE QUORUM — the minimal non-additive replicator, 2 placed laws")
    ok6, info = certify(QUORUM_SEED, QUORUM, "super_or", 4, [(0, 0), (4, -4)])
    check("Phi^4(S) = S u sigma^(4,-4)S, gap %s > 2R=2, debris %s"
          % (info.get("gaps"), info.get("debris")), ok6 and info["exact"])
    check("seed is 2 placed laws in 2 cells (minimal under clause 1.4(b))",
          card(QUORUM_SEED) == 2 and len(QUORUM_SEED) == 2)
    f, t = split_fail(QUORUM, QUORUM_SEED, "super_or", 4)
    check("both splittings of the seed violate superposition (%d/%d)" % (f, t),
          f == t == 2)
    ev = exact_events(QUORUM, QUORUM_SEED, "super_or", 260)
    check("colony reaches %d exact free copies" % max(c for _, c, _ in ev),
          max(c for _, c, _ in ev) >= 32)

    sec("5. THE MOOT — rung 3, additive (the Fredkin phenomenon)")
    ev = exact_events(MOOT, MOOT_SEED, "parity", 520)
    check("exact free copies reach %d (rung 3)"
          % max(c for _, c, _ in ev), max(c for _, c, _ in ev) >= 21)
    check("Phi == L at every one of 200 steps (fully additive)",
          phi_ne_L(MOOT, MOOT_SEED, "parity", 200) == 0)
    ok4, info = certify(MOOT_SEED, MOOT, "parity", 8, [(0, 0), (-8, 0), (8, 0)])
    check("certify 3 free copies at p=8, offsets 0,-8,+8, debris %s"
          % info.get("debris"), ok4 and info["exact"])

    sec("6. PASCAL COLUMN — rung 3 but a DEGENERATE (one-law) seed, additive")
    ev = exact_events(PASCAL, PASCAL_SEED, "parity", 70)
    check("exact free copies reach %d" % max(c for _, c, _ in ev),
          max(c for _, c, _ in ev) >= 16)
    check("Phi == L at every one of 70 steps (fully additive)",
          phi_ne_L(PASCAL, PASCAL_SEED, "parity", 70) == 0)
    check("seed occupies 1 cell -> excluded by pre-registration 1.4(b)",
          len(PASCAL_SEED) == 1)

    sec("7. 1-D citation replicator (phantom kind) — rung 3, additive")
    ev = exact_events(PHANTOM, PHANTOM_SEED, "parity", 300)
    check("exact free copies reach %d on Z" % max(c for _, c, _ in ev),
          max(c for _, c, _ in ev) >= 40)
    check("Phi == L at every one of 200 steps (the citation is vacuous)",
          phi_ne_L(PHANTOM, PHANTOM_SEED, "parity", 200) == 0)
    ok5, info = certify(PHANTOM_SEED, PHANTOM, "parity", 8, [0, 8, -8])
    check("certify 3 free copies at p=8, gaps %s, debris %s"
          % (info.get("gaps"), info.get("debris")), ok5 and info["exact"])

    sec("8. THE ENGROSSING CLERK — a blueprint-driven constructor")
    good = True
    for tape in ["0", "1", "01", "10", "0110", "1001", "111000",
                 "0101010101", "1101001110"]:
        S, _ = constructor.run(tape)
        good &= (constructor.built_row(S, 1) == tape)
        P2 = to_p(constructor.seed(tape))
        for _ in range(len(tape) + 2):
            P2 = pstep(P2, constructor.CLERK, "parity")
        good &= (constructor.built_row(from_p(P2), 1) == tape)
    check("built row = the blueprint, decoded into kinds U,V, for 9 "
          "blueprints, on both engines", good)
    check("the constructor uses CITATION guards (chapter three)",
          constructor.CLERK.cited)

    sec("9. THE SCRIBE — unbounded heritable copying")
    good = True
    for tape in ["0", "1", "01", "011", "1001", "110100", "0101101"]:
        rows, _, _, _ = scribe.generations(tape, 6)
        rows2, _, _, _ = scribe.generations(tape, 6, engine="pstep")
        good &= all(r == "L" + tape + "Z" for r in rows) and rows == rows2
    check("6 generations reproduce the blueprint exactly, 7 blueprints, "
          "both engines", good)

    sec("10. no free colony forever (Corollary A2), measured on THE "
        "ENGROSSMENT")
    ev = exact_events(ENGROSSMENT, ENGROSSMENT_SEED, "parity", 260)
    d = dict((t, c) for t, c, _ in ev)
    check("the naive iterate fails: Phi^8(S) is 2 free copies, not 4 -- the "
          "two children of the first fission collide", d.get(8) == 2)
    peaks = [(t, c) for t, c in sorted(d.items())
             if c == 2 ** bin(t // 4).count("1") and (t // 4 + 1) &
             (t // 4) == 0]
    check("the copy count peaks 2^k occur at t = 4(2^k - 1): %s -- the "
          "doubling period doubles, so copies grow like t and not like "
          "2^(t/4)" % peaks[:7], len(peaks) >= 6)
    check("copies(t) <= card(S_t)/card(S) <= n(span+2Rt+1)^2 / 4 "
          "(Theorem A): max %d copies at t<=260" % max(d.values()),
          max(d.values()) <= 2 * 260)

    print("\n%d checks passed, %d failed" % (OK[0], BAD[0]))
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
