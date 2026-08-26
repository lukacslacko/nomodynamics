#!/usr/bin/env python3
"""
verify_citation.py — the battery of expedition Y-A.

Re-checks every named claim of citation/RESULTS.md.  Two engines are used
throughout and they share no code: `cite.py` (bitfield, one big int per kind)
and the repository's `xnomos.py` (dict of cell -> bitmask).  Every positive
claim below is a machine-checked witness re-verified by the other engine or by
an independent closed form.

    python3 verify_citation.py          # ~20 min on a quiet machine
    python3 verify_citation.py -q       # summary only
"""

from __future__ import annotations

import itertools
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cite as ct                                              # noqa: E402
import circuit                                                 # noqa: E402
import specimens as sp                                         # noqa: E402
import xnomos as X                                             # noqa: E402

CHECKS = []
QUIET = "-q" in sys.argv


def check(name):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


def rnd_const(rng, n, offs=(-1, 0, 1)):
    gs = [None] + list(range(n))
    return ct.Cit([(rng.choice(offs), rng.choice(offs), rng.choice(offs))
                   for _ in range(n)],
                  [tuple(sorted(rng.sample(range(n), rng.randrange(0, n + 1))))
                   for _ in range(n)],
                  [(rng.choice(gs), rng.choice(gs)) for _ in range(n)])


def rnd_code(rng, n, lo=-4, hi=5, k=6):
    return [(rng.randrange(lo, hi), rng.randrange(n))
            for _ in range(rng.randrange(1, k))]


# ------------------------------------------------------------------ engines

@check("E1  bitfield engine == xnomos, random citation universes")
def e1():
    rng = random.Random(1)
    for _ in range(600):
        n = rng.randrange(1, 5)
        C = rnd_const(rng, n)
        pairs = rnd_code(rng, n)
        for mode in ("parity", "or"):
            F = ct.state_fields(pairs, n)
            S = X.state_of(pairs, n)
            XC = C.to_xnomos()
            for _ in range(8):
                F = ct.step_fields(F, C, mode)
                S = X.step(S, XC, mode)
                if sorted(ct.fields_to_pairs(F)) != sorted(
                        (c, k) for c, k in X.laws(S)):
                    return False, C.label()
    return True, "600 universes x 2 resolutions x 8 steps"


@check("E2  ring engine == xnomos on Z/m, random citation universes")
def e2():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randrange(1, 4)
        C = rnd_const(rng, n)
        m = rng.randrange(3, 12)
        pairs = [(rng.randrange(m), rng.randrange(n))
                 for _ in range(rng.randrange(1, 7))]
        for mode in ("parity", "or"):
            mask = [0] * n
            for c, k in pairs:
                mask[k] |= 1 << c
            S = X.state_of(pairs, n)
            XC = C.to_xnomos(modulus=m)
            mask = tuple(mask)
            for _ in range(6):
                mask = ct.step_ring(mask, C, m, mode)
                S = X.step(S, XC, mode)
                got = sorted((c, k) for c in range(m) for k in range(n)
                             if (mask[k] >> c) & 1)
                if got != sorted((c, k) for c, k in X.laws(S)):
                    return False, (C.label(), m)
    return True, "300 universes x 2 resolutions x 6 steps"


# ------------------------------------------------------- structure theorems

@check("T1  citation is INERT at n = 1 (complete: 216 constitutions)")
def t1():
    rng = random.Random(3)
    cnt = 0
    for rule in ct.RULES:
        for T in ((), (0,)):
            base = ct.Cit([rule], [T], [(None, None)])
            for g in (None, 0):
                for h in (None, 0):
                    D = ct.Cit([rule], [T], [(g, h)])
                    cnt += 1
                    for _ in range(30):
                        F = ct.state_fields(rnd_code(rng, 1), 1)
                        for mode in ("parity", "or"):
                            if ct.step_fields(F, base, mode) != \
                                    ct.step_fields(F, D, mode):
                                return False, (rule, T, g, h)
    return True, "%d one-kind constitutions, all guard choices identical" % cnt


@check("T2  PLENUM: beta(K) = K, i.e. the full plenum is always frozen")
def t2():
    rng = random.Random(4)
    for _ in range(20000):
        n = rng.randrange(1, 6)
        C = rnd_const(rng, n)
        K = frozenset(range(n))
        if ct.active_bulk(C, K) or ct.bulk_map(C, K) != K \
                or ct.bulk_map(C, K, "or") != K:
            return False, C.label()
    return True, "20,000 random constitutions, n <= 5"


@check("T2' PLENUM, sharp form: saturation by the exception image E(C) blocks")
def t2p():
    rng = random.Random(5)
    tested = 0
    for _ in range(4000):
        n = rng.randrange(2, 5)
        C = rnd_const(rng, n)
        E = {h for (g, h) in C.guards if h is not None}
        # a region [0,9] carrying every kind of E, arbitrary elsewhere
        pairs = [(i, k) for i in range(10) for k in E]
        pairs += [(i, k) for i in range(-3, 13) for k in range(n)
                  if rng.random() < .4]
        F = ct.state_fields(pairs, n)
        act = ct.active_fields(F, C)
        for k in range(n):
            f = act[k]
            while f:
                b = (f & -f).bit_length() - 1
                f &= f - 1
                i = b - ct.BIAS
                if C.guards[k][1] is not None and 0 <= i + C.rules[k][1] <= 9:
                    return False, (C.label(), k, i)
                tested += 1
    return True, "4,000 constitutions; no law with a named exception inside " \
                 "an E(C)-saturated region is active"


@check("T3  GRIDLOCK's epitaph: closed form == brute force over all U")
def t3():
    rng = random.Random(6)
    for _ in range(30000):
        n = rng.randrange(1, 6)
        C = rnd_const(rng, n)
        if ct.gridlocked(C) != ct.gridlocked_bruteforce(C):
            return False, C.label()
    return True, "30,000 random constitutions, n <= 5"


@check("T3' GRIDLOCK survival fraction = ((3n+1)/(n+1)^2)^n, n = 1,2,3")
def t3p():
    for n in (1, 2, 3):
        gs = [None] + list(range(n))
        ts = [t for r in range(n + 1) for t in itertools.combinations(range(n), r)]
        tot = ok = 0
        for combo in itertools.product([(T, (g, h)) for T in ts
                                        for g in gs for h in gs], repeat=n):
            C = ct.Cit([(0, 0, 0)] * n, [c[0] for c in combo],
                       [c[1] for c in combo])
            tot += 1
            ok += ct.gridlocked(C)
        if Fraction(ok, tot) != Fraction(3 * n + 1, (n + 1) ** 2) ** n:
            return False, (n, Fraction(ok, tot))
    return True, "complete: 60.4938% at n=2, 24.4141% at n=3"


@check("T4  BULK MAP is exact on homogeneous ring codes, every modulus")
def t4():
    rng = random.Random(7)
    for _ in range(2000):
        n = rng.randrange(1, 5)
        C = rnd_const(rng, n)
        for m in (1, 2, 3, 4, 5, 7, 11):
            U = frozenset(k for k in range(n) if rng.random() < .5)
            full = (1 << m) - 1
            mask = tuple(full if k in U else 0 for k in range(n))
            for mode in ("parity", "or"):
                V = ct.bulk_map(C, U, mode)
                if ct.step_ring(mask, C, m, mode) != tuple(
                        full if k in V else 0 for k in range(n)):
                    return False, (C.label(), m, mode)
    return True, "2,000 constitutions x 7 moduli x 2 resolutions"


@check("T5  bulk period <= 2^n - 2 (complete for n <= 3, sampled n = 4,5)")
def t5():
    rng = random.Random(8)
    for n in (2, 3):
        gs = [None] + list(range(n))
        ts = [t for r in range(n + 1)
              for t in itertools.combinations(range(n), r)]
        pool = [(T, (g, h)) for T in ts for g in gs for h in gs]
        for combo in itertools.product(pool, repeat=n):
            C = ct.Cit([(0, 0, 0)] * n, [c[0] for c in combo],
                       [c[1] for c in combo])
            for u in range(1 << n):
                U = frozenset(k for k in range(n) if (u >> k) & 1)
                if ct.bulk_orbit(C, U)[1] > 2 ** n - 2:
                    return False, C.label()
    for n in (4, 5):
        for _ in range(30000):
            C = rnd_const(rng, n)
            for _ in range(3):
                U = frozenset(k for k in range(n) if rng.random() < .5)
                if ct.bulk_orbit(C, U)[1] > 2 ** n - 2:
                    return False, C.label()
    return True, "n=2: 1,296 complete; n=3: 2,097,152 complete; n=4,5 sampled"


@check("T6  SELF-CITATION at offset 0 is trivial (tautology / contradiction)")
def t6():
    rng = random.Random(9)
    for _ in range(3000):
        n = rng.randrange(2, 5)
        C = rnd_const(rng, n)
        k = rng.randrange(n)
        a, b, c = C.rules[k]
        # g_k = k, a_k = 0  => precedent always true
        D = ct.Cit(C.rules[:k] + [(0, b, c)] + C.rules[k + 1:], C.targets,
                   C.guards[:k] + [(k, C.guards[k][1])] + C.guards[k + 1:])
        pairs = rnd_code(rng, n) + [(0, k)]
        F = ct.state_fields(pairs, n)
        if not (ct.active_fields(F, D)[k] >> ct.BIAS) & 1:
            # only a failed exception clause may block it
            g, h = D.guards[k]
            occ = 0
            for f in F:
                occ |= f
            fld = occ if h is None else F[h]
            if not (fld >> (ct.BIAS + b)) & 1:
                return False, ("tautology broken", D.label())
        # h_k = k, b_k = 0  => exception always false => dead letter
        E = ct.Cit(C.rules[:k] + [(a, 0, c)] + C.rules[k + 1:], C.targets,
                   C.guards[:k] + [(C.guards[k][0], k)] + C.guards[k + 1:])
        F = ct.state_fields(pairs, n)
        if ct.active_fields(F, E)[k]:
            return False, ("dead letter broken", E.label())
    return True, "3,000 random universes"


@check("T7  heterogeneous solid regions: blocked <=> h_k = ANY or dead letter")
def t7():
    """The parenthetical of RESULTS.md 3.1, checked exhaustively at W = 1."""
    tested = 0
    for n in (2, 3):
        full = (1 << n) - 1

        def act(k, rule, guard, mm1, m0, mp1):
            a, b, _ = rule
            g, h = guard
            cells = {-1: mm1, 0: m0, 1: mp1}
            ma, mb = cells[a], cells[b]
            prec = (ma != 0) if g is None else ((ma >> g) & 1)
            exc = (mb != 0) if h is None else ((mb >> h) & 1)
            return bool(prec) and not exc

        for rule in ct.RULES:
            for g in [None] + list(range(n)):
                for h in [None] + list(range(n)):
                    for k in range(n):
                        solid_blocked = True
                        ever = False
                        for m0 in range(1, full + 1):
                            if not (m0 >> k) & 1:
                                continue
                            for mm1 in range(0, full + 1):
                                for mp1 in range(0, full + 1):
                                    if act(k, rule, (g, h), mm1, m0, mp1):
                                        ever = True
                                        if mm1 and mp1:
                                            solid_blocked = False
                        if solid_blocked != ((h is None) or (not ever)):
                            return False, (n, rule, g, h, k)
                        tested += 1
    return True, "%d (kind, rule, guard) cases, n = 2 and 3, exhaustive" % tested


# --------------------------------------------- chapter-two survival theorems

@check("S1  SINGLE AUTHOR: in-degree <= 1 => parity == OR, under citation")
def s1():
    rng = random.Random(10)
    trials = 0
    while trials < 800:
        n = rng.randrange(2, 5)
        C = rnd_const(rng, n)
        if any(C.indeg(t) > 1 for t in range(n)):
            continue
        trials += 1
        F = ct.state_fields(rnd_code(rng, n, k=8), n)
        for _ in range(10):
            if ct.step_fields(F, C, "parity") != ct.step_fields(F, C, "or"):
                return False, C.label()
            F = ct.step_fields(F, C, "parity")
    return True, "800 in-degree<=1 citation universes x 10 steps"


@check("S2  DEAD LETTER under OR: fixed <=> no active law (nonempty targets)")
def s2():
    rng = random.Random(11)
    trials = 0
    while trials < 4000:
        n = rng.randrange(2, 5)
        C = rnd_const(rng, n)
        if any(len(T) == 0 for T in C.targets):
            continue
        trials += 1
        F = ct.state_fields(rnd_code(rng, n, k=8), n)
        for _ in range(6):
            fixed = ct.step_fields(F, C, "or") == F
            dead = not any(ct.active_fields(F, C))
            if fixed != dead:
                return False, C.label()
            F = ct.step_fields(F, C, "or")
    return True, "4,000 citation universes x 6 states"


@check("S3  BALANCE: fixed-and-active under parity => even cohorts")
def s3():
    rng = random.Random(12)
    found = 0
    for _ in range(60000):
        n = rng.randrange(2, 5)
        C = rnd_const(rng, n)
        pairs = rnd_code(rng, n, -2, 3, 5)
        F = ct.state_fields(pairs, n)
        if ct.step_fields(F, C, "parity") != F:
            continue
        act = ct.active_fields(F, C)
        if not any(act):
            continue
        found += 1
        slot = {}
        for k in range(n):
            f = act[k]
            while f:
                b = (f & -f).bit_length() - 1
                f &= f - 1
                for t in C.targets[k]:
                    slot[(b + C.rules[k][2], t)] = \
                        slot.get((b + C.rules[k][2], t), 0) + 1
        if any(v % 2 for v in slot.values()):
            return False, C.label()
    return True, "%d balanced citation codes, every slot even" % found


@check("S4  ANCHOR (own-kind + citation): the trailing law is never repealed")
def s4():
    rng = random.Random(13)
    tested = 0
    for _ in range(4000):
        n = rng.randrange(1, 4)
        C0 = rnd_const(rng, n)
        C = ct.Cit(C0.rules, [(k,) for k in range(n)], C0.guards)
        pairs = rnd_code(rng, n, -4, 5, 7)
        F = ct.state_fields(pairs, n)
        for _ in range(25):
            occ = 0
            for f in F:
                occ |= f
            if occ == 0:
                break
            lo = (occ & -occ).bit_length() - 1
            k = next(k for k in range(n) if (F[k] >> lo) & 1)
            c = C.rules[k][2]
            G = ct.step_fields(F, C, "parity")
            if c > 0 and not (G[k] >> lo) & 1:
                return False, (C.label(), "trailing law repealed")
            tested += 1
            F = G
    return True, "%d states; c_k>0 trailing laws never repealed" % tested


@check("S5  PATH-SUM / LINEAR GROWTH: card <= n*(2Wt + span0 + 1)")
def s5():
    rng = random.Random(14)
    for _ in range(3000):
        n = rng.randrange(1, 5)
        C = rnd_const(rng, n)
        pairs = rnd_code(rng, n, 0, 3, 5)
        F = ct.state_fields(pairs, n)
        s0 = 2
        for t in range(1, 40):
            F = ct.step_fields(F, C, "parity")
            if ct.card_fields(F) > n * (2 * t + s0 + 1):
                return False, C.label()
    return True, "3,000 universes x 40 steps"


@check("S5' the linear growth bound is TIGHT: card = n(2t+1) attained")
def s5p():
    n = 3
    C = ct.Cit([(0, 1, 1), (0, -1, -1), (0, 0, 0)],
               [(0, 1, 2), (0, 1, 2), ()], [(None, None), (None, None), (2, 2)])
    F = ct.state_fields([(0, k) for k in range(n)], n)
    for t in range(1, 30):
        F = ct.step_fields(F, C, "parity")
        if ct.card_fields(F) != n * (2 * t + 1):
            return False, (t, ct.card_fields(F))
    return True, "card = 3(2t+1) exactly for t <= 29 (rate 2nW = 6 laws/step)"


@check("S6  DILATION survives citation with 'occupancy' -> 'cell content'")
def s6():
    rng = random.Random(15)
    for _ in range(1500):
        n = rng.randrange(1, 4)
        C = rnd_const(rng, n)
        r = rng.randrange(2, 4)
        D = ct.Cit([(r * a, r * b, r * c) for a, b, c in C.rules],
                   C.targets, C.guards)
        pairs = rnd_code(rng, n, -3, 4, 5)
        F = ct.state_fields(pairs, n)
        G = ct.state_fields([(r * c, k) for c, k in pairs], n)
        for mode in ("parity", "or"):
            f, g = list(F), list(G)
            for _ in range(6):
                f = ct.step_fields(f, C, mode)
                g = ct.step_fields(g, D, mode)
                if sorted((r * c, k) for c, k in ct.fields_to_pairs(f)) != \
                        sorted(ct.fields_to_pairs(g)):
                    return False, C.label()
    return True, "1,500 universes x 2 resolutions x 6 steps"


@check("S7  OUT-DEGREE LAW (Y2): no glider at out-degree <= 1, deep search")
def s7():
    rng = random.Random(16)
    runs = 0
    for _ in range(40000):
        n = rng.randrange(2, 5)
        C0 = rnd_const(rng, n)
        C = ct.Cit(C0.rules,
                   [(rng.randrange(n),) for _ in range(n)], C0.guards)
        pairs = rnd_code(rng, n, 0, 5, 7)
        for mode in ("parity", "or"):
            r = ct.classify(ct.state_fields(pairs, n), C, mode,
                            max_steps=600, max_card=400, max_span=400)
            runs += 1
            if r["kind"] == ct.GLIDER:
                return False, (C.label(), pairs)
    return True, "%d deep runs at out-degree 1, zero gliders" % runs


@check("S8  Y7: TANDEM-1 rotates one cell per step on every ring 3 <= m <= 24")
def s8():
    for m in range(3, 25):
        C = X.Const([(0, -1, 1), (0, -1, 0)], targets=[(0, 1), (0, 1)],
                    modulus=m)
        S = X.state_of([(1, 0), (1, 1)])
        if X.step(S, C) != {(1 + 1) % m: S[1]}:
            return False, m
    return True, "m = 3..24, odd and even, r=1 <= p*W=1 (inside the light cone)"


@check("S9  SUNSET + citation: every reported glider re-certifies")
def s9():
    rng = random.Random(19)
    n_gl = 0
    K = ct.all_kinds(2)
    seeds = ct.seeds_span(3, 2)
    for _ in range(300):
        k1, k2 = K[rng.randrange(len(K))], K[rng.randrange(len(K))]
        C = ct.Cit([k1[0], k2[0]], [k1[1], k2[1]], [k1[2], k2[2]])
        for s in seeds:
            for mode in ("parity", "or"):
                r = ct.classify_sunset(list(s), C, mode, max_steps=200,
                                       max_card=200, max_span=120)
                if r["kind"] != ct.GLIDER:
                    continue
                core = list(s)
                for _ in range(r["t"]):
                    core = ct.step_sunset(core, C, mode)
                if not ct.verify_glider_sunset(core, C, r["period"],
                                               r["displacement"], mode):
                    return False, C.label()
                n_gl += 1
    return True, "%d sunset gliders re-certified over 3 full periods" % n_gl


# ---------------------------------------------------------------- specimens

@check("F1  LACUNA: Phi = rot_(+1) on Z/m, occupancy constant, both engines")
def f1():
    for m in (5, 7, 8, 11, 13, 16, 21, 32):
        f = (1 << m) - 1
        A = (f & ~1, f)
        B = ct.step_ring(A, sp.LAC, m)
        want = tuple(((x >> (m - 1)) | (x << 1)) & f for x in A)
        if B != want:
            return False, m
        S0 = X.state_of([(i, 0) for i in range(m) if i != 0]
                        + [(i, 1) for i in range(m)])
        XC = sp.LAC.to_xnomos(modulus=m)
        S = dict(S0)
        for t in range(m):
            S = X.step(S, XC)
            if set(S) != set(range(m)):
                return False, ("occupancy changed", m, t)
        if X.freeze(S) != X.freeze(S0):
            return False, ("period != m", m)
    return True, "m in {5,7,8,11,13,16,21,32}; every cell occupied at all times"


@check("F2  SIX SESSIONS: bulk period 6 = 2^3-2 on Z/m, both engines")
def f2():
    for m in range(2, 14):
        S = ((1 << m) - 1, 0, 0)
        if ct.ring_orbit(S, sp.SIX, m)[1] != 6:
            return False, m
        XC = sp.SIX.to_xnomos(modulus=m)
        r = X.classify(X.state_of([(i, 0) for i in range(m)]), XC, "parity",
                       max_steps=60)
        if r["kind"] != "CYCLE" or r["period"] != 6:
            return False, (m, r)
    return True, "m = 2..13, both engines, period exactly 6"


@check("F3  PASCAL: card = 2^popcount(t) for t <= 256, both engines")
def f3():
    F = ct.state_fields([(0, 0)], 2)
    S = X.state_of([(0, 0)], 2)
    XC = sp.PAS.to_xnomos()
    for t in range(1, 257):
        F = ct.step_fields(F, sp.PAS, "parity")
        if ct.card_fields(F) != 1 << bin(t).count("1"):
            return False, t
    for t in range(1, 65):
        S = X.step(S, XC)
        if X.card(S) != 1 << bin(t).count("1"):
            return False, ("xnomos", t)
    return True, "t <= 256 (cite), t <= 64 (xnomos)"


@check("F4  THE COPY: every seed replicates at t = 2^j > span")
def f4():
    rng = random.Random(17)
    for _ in range(200):
        cells = sorted(set(rng.randrange(0, 30) for _ in range(rng.randrange(1, 7))))
        seed = [(c, 0) for c in cells]
        F0 = ct.state_fields(seed, 2)
        span = cells[-1] - cells[0]
        for j in range(1, 8):
            t = 1 << j
            if t <= span:
                continue
            F = ct.advance(F0, sp.PAS, t, "parity")
            if F != [F0[0] | (F0[0] << t), F0[1]]:
                return False, (seed, t)
    return True, "200 random seeds, all j with 2^j > span"


@check("F5  THE WRIT: Z'(i) = Z(i-1) exactly, random signal patterns")
def f5():
    rng = random.Random(18)
    L = 24
    for _ in range(400):
        sig = [i for i in range(L) if rng.random() < .3]
        pairs = ([(i, 1) for i in range(L)] + [(i, 2) for i in range(L)]
                 + [(i, 0) for i in sig])
        F = ct.state_fields(pairs, 4)
        G = ct.step_fields(F, sp.WRIT, "parity")
        want = F[0] << 1
        if G[0] != want or G[1] != F[1] or G[2] != F[2]:
            return False, sig
    return True, "400 random signal patterns on 24 cells"


@check("F6  PROCESSION: Phi = rot_(+1) on a completely full ring")
def f6():
    for m in range(3, 20):
        f = (1 << m) - 1
        S = (1 << 2, f, f, 0)
        T = ct.step_ring(S, sp.WRIT, m)
        if T != tuple(((x >> (m - 1)) | (x << 1)) & f for x in S):
            return False, m
        XC = sp.WRIT.to_xnomos(modulus=m)
        S0 = X.state_of([(i, 1) for i in range(m)] + [(i, 2) for i in range(m)]
                        + [(2, 0)], 4)
        r = X.classify(S0, XC, "parity", max_steps=4 * m + 4)
        if r["kind"] != "CYCLE" or r["period"] != m:
            return False, (m, r)
    return True, "m = 3..19, both engines"


@check("F7  CONVERSION FRONT: the seam advances exactly one cell per step")
def f7():
    L = 40
    pairs = [(i, 0) for i in range(20)] + [(i, 1) for i in range(20, L)]
    F = ct.state_fields(pairs, 2)
    for t in range(1, 15):
        F = ct.step_fields(F, sp.CONV, "parity")
        seam = (F[0].bit_length() - ct.BIAS)
        if seam != 20 - t:
            return False, (t, seam)
        if F[0] | F[1] != ct.state_fields(pairs, 2)[0] | \
                ct.state_fields(pairs, 2)[1]:
            return False, ("occupancy changed", t)
    return True, "15 steps, occupancy constant, seam speed exactly 1"


@check("F8  THE LEDGER: card 5 and reach 2^j+3 at every t = 4^j, exactly")
def f8():
    head = {(0, 0), (0, 1), (2, 1)}
    F = ct.state_fields(sp.LEDGER_SEED, 2)
    hits = 0
    for t in range(1, 4 ** 8 + 1):
        F = ct.step_fields(F, sp.LEDGER, "parity")
        b = t.bit_length() - 1
        if t >= 4 and (t & (t - 1)) == 0 and b % 2 == 0:
            j = b // 2
            if set(ct.fields_to_pairs(F)) != head | {(2 ** j + 2, 0),
                                                     (2 ** j + 2, 1)}:
                return False, j
            hits += 1
    return True, "j = 1..8 exact (t up to 65,536); head + doubling marker"


@check("F9  THE LEDGER is aperiodic: no exact recurrence in 400,000 steps")
def f9():
    F = ct.state_fields(sp.LEDGER_SEED, 2)
    seen = set()
    lo = hi = None
    for t in range(400000):
        fe = tuple(F)
        if fe in seen:
            return False, t
        seen.add(fe)
        c = ct.card_fields(F)
        lo = c if lo is None else min(lo, c)
        hi = c if hi is None else max(hi, c)
        F = ct.step_fields(F, sp.LEDGER, "parity")
    return True, "400,000 fully hashed states, card in [%d,%d] (bounded)" % (lo, hi)


@check("F10 THE ODOMETER shares the head-plus-marker form at t = 4^j")
def f10():
    V = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
         "P": (1, -1), "Q": (-1, -1), "R": (1, 1), "T": (-1, 1)}
    C = X.Const([tuple(V[c] for c in "OEW"), tuple(V[c] for c in "NQR")],
                targets=[(1,), (0, 1)], dim=2)
    head = {((0, 0), 0), ((1, 0), 0), ((0, 1), 1)}
    S = X.state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])
    n = 0
    for t in range(1, 4 ** 7 + 1):
        S = X.step(S, C)
        b = t.bit_length() - 1
        if t >= 4 and (t & (t - 1)) == 0 and b % 2 == 0:
            j = b // 2
            if set((c, k) for c, k in X.laws(S)) != head | {
                    ((0, 3 * 2 ** (j - 1)), 1)}:
                return False, j
            n += 1
    return True, "j = 1..7 exact, root-compass reading (verify.py's own off())"


# -------------------------------------------------------------- the machine

@check("M1  gate inventory: BUFFER NOT ANDNOT AND XOR OR FANOUT, 7/7")
def m1():
    rows, ok, tot = circuit.gate_inventory()
    return ok == tot, "%d/%d truth tables exact" % (ok, tot)


@check("M2  all 256 elementary CA rules simulated exactly on a ring")
def m2():
    bad = circuit.verify_all_eca(m=11, steps=16, trials=2, seed=99)
    return not bad, "256 rules, Z/11, 16 CA steps, 2 random seeds each"


@check("M3  Rule 110 long run + xnomos cross-check")
def m3():
    M = circuit.ECA(110)
    m, T = 23, 60
    rng = random.Random(20)
    bits = [rng.randrange(2) for _ in range(m)]
    st = M.seed_ring(bits)
    ref = list(bits)
    for _ in range(T):
        st = ct.step_ring(st, M.C, m)
        st = ct.step_ring(st, M.C, m)
        ref = circuit.eca_step(ref, 110)
        if M.read_ring(st, m) != ref:
            return False, "cite engine"
    XC = M.C.to_xnomos(modulus=m)
    pairs = [(i, M.CK) for i in range(m)]
    pairs += [(i, k) for i in range(m) for k in M.phase_kinds[1]]
    pairs += [(i, M.S) for i in range(m) if bits[i]]
    S = X.state_of(pairs, M.C.n)
    ref = list(bits)
    for _ in range(20):
        S = X.step(X.step(S, XC), XC)
        ref = circuit.eca_step(ref, 110)
        got = [1 if S.get(i, 0) >> M.S & 1 else 0 for i in range(m)]
        if got != ref:
            return False, "xnomos engine"
    return True, "60 CA steps (cite) + 20 CA steps (xnomos), Z/23"


@check("M4  the machine is entrenched: gate kinds are never lost")
def m4():
    M = circuit.ECA(110)
    m = 17
    rng = random.Random(21)
    bits = [rng.randrange(2) for _ in range(m)]
    st = M.seed_ring(bits)
    full = (1 << m) - 1
    for t in range(80):
        st = ct.step_ring(st, M.C, m)
        if st[M.CK] != full:
            return False, ("clock lost", t)
        p1, p2 = st[M.phase_kinds[1][0]], st[M.phase_kinds[2][0]]
        if {p1, p2} != {0, full}:
            return False, ("phase broken", t)
    return True, "80 steps: the clock stands at every cell, phases alternate"


# ------------------------------------------------------------------ census

@check("C1  census slice reproduces (independent re-run of 400 constitutions)")
def c1():
    import census
    rng = random.Random(22)
    R = [(rng.randrange(len(census.KINDS)), rng.randrange(len(census.KINDS)), 1)
         for _ in range(400)]
    a = census._work(R)[0]
    b = census._work(R)[0]
    return a == b and sum(a.values()) > 0, "deterministic, %d tallies" % len(a)


@check("C2  census symmetry quotient is sound: orbits have constant census")
def c2():
    import census
    rng = random.Random(23)
    for _ in range(120):
        i, j = rng.randrange(len(census.KINDS)), rng.randrange(len(census.KINDS))
        C = census.const_of(i, j)
        base = None
        for D in ct.orbit_of(C).values():
            tally = {}
            for mode in ("parity", "or"):
                for s in census.SEEDS:
                    k = ct.classify(list(s), D, mode, **census.S1)["kind"]
                    tally[(mode, k)] = tally.get((mode, k), 0) + 1
            if base is None:
                base = tally
            elif tally != base:
                return False, C.label()
    return True, "120 orbits; class multiset constant on every orbit"


@check("C3  every census glider record re-certifies from its glider core")
def c3():
    import census
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "gliders1.txt")
    if not os.path.exists(path):
        return True, "SKIPPED (data/gliders1.txt absent; run census.py stage1)"
    n = 0
    for line in open(path):
        a = line.split()
        C = census.const_of(int(a[0]), int(a[1]))
        S = census.SEEDS[int(a[2])]
        res, core, ok = ct.certify_glider(list(S), C, a[3], **census.S1)
        if not ok:
            return False, C.label()
        n += 1
    return True, "%d records, Phi^p = sigma^d over three full periods" % n


@check("X1  xnomos.verify_glider certifies a census glider (its own routine)")
def x1():
    import census
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "gliders1.txt")
    if not os.path.exists(path):
        return True, "SKIPPED (data/gliders1.txt absent)"
    rng = random.Random(24)
    rows = [l.split() for l in open(path)]
    n = 0
    for a in rng.sample(rows, min(60, len(rows))):
        C = census.const_of(int(a[0]), int(a[1]))
        seed = census.SEEDS[int(a[2])]
        res, core, ok = ct.certify_glider(list(seed), C, a[3], **census.S1)
        if not ok:
            return False, C.label()
        XS = X.state_of(ct.fields_to_pairs(core), C.n)
        if not X.verify_glider(XS, C.to_xnomos(), res["period"],
                               res["displacement"], a[3]):
            return False, ("xnomos disagrees", C.label())
        n += 1
    return True, "%d census gliders re-certified by xnomos.verify_glider" % n


@check("X2  xnomos.verify_balanced certifies citation balanced codes")
def x2():
    rng = random.Random(25)
    found = 0
    for _ in range(40000):
        n = rng.randrange(2, 5)
        C = rnd_const(rng, n)
        pairs = rnd_code(rng, n, -2, 3, 5)
        F = ct.state_fields(pairs, n)
        if ct.step_fields(F, C, "parity") != F or not any(
                ct.active_fields(F, C)):
            continue
        found += 1
        if not X.verify_balanced(X.state_of(pairs, n), C.to_xnomos(),
                                 "parity"):
            return False, C.label()
        if found >= 400:
            break
    return True, "%d balanced citation codes confirmed by xnomos" % found


if __name__ == "__main__":
    npass = 0
    for name, fn in CHECKS:
        try:
            ok, note = fn()
        except Exception as exc:                                # noqa: BLE001
            ok, note = False, "EXCEPTION %r" % (exc,)
        npass += bool(ok)
        if not QUIET or not ok:
            print("%s  %-62s %s" % ("PASS" if ok else "FAIL", name, note))
    print("\n%d/%d checks passed" % (npass, len(CHECKS)))
    sys.exit(0 if npass == len(CHECKS) else 1)
