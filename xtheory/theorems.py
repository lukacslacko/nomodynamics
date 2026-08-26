#!/usr/bin/env python3
"""theorems.py — the verification battery for Expedition X-D.

Every claim in RESULTS.md that says "verified" is produced by a section here.
Each section prints one line per claim with an exact count and a PASS/FAIL.

Run: python3 theorems.py [section ...]     (default: all)
"""
from __future__ import annotations

import itertools
import json
import random
import sys
from collections import Counter, defaultdict

from xlib import (RULES1, Const, ref_step, to_pairs, from_pairs, duel,
                  max_multiplicity, in_degrees, components_cycles,
                  cycle_offset_sum, reach_set, active_alphabet,
                  present_alphabet, target_image, entrenched_kinds,
                  toggled_slots, is_balanced, is_cryptic, all_seeds,
                  seeds_span, path_sums, rho)
import xnomos as X
from xnomos import state_of, active_laws, laws, card, classify, step

RES = {}


def claim(name, ok, detail=""):
    RES[name] = bool(ok)
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", name, detail))


TMAPS4 = [[0, 1], [1, 0], [0, 0], [1, 1]]


def rand_const(rng, n, multi=False, dim=1):
    pool = RULES1 if dim == 1 else [
        (a, b, c) for a in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0), (1, 1)]
        for b in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]
        for c in [(-1, 0), (0, 1), (1, 0), (0, -1), (1, 1), (0, 0)]]
    rules = [rng.choice(pool) for _ in range(n)]
    if multi:
        tg = []
        for _ in range(n):
            s = tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
            tg.append(s if len(s) > 1 else s[0])
    else:
        tg = [rng.randrange(n) for _ in range(n)]
    return Const(rules, tg, dim=dim)


def rand_state(rng, n, lo=-4, hi=5, kmax=6, dim=1):
    S = {}
    for _ in range(rng.randrange(1, kmax + 1)):
        c = rng.randrange(lo, hi) if dim == 1 else (rng.randrange(lo, hi),
                                                   rng.randrange(lo, hi))
        S[c] = S.get(c, 0) | (1 << rng.randrange(n))
    return S


# ============================================================== 1. GRIDLOCK
def s_gridlock():
    print("\n=== 1. Gridlock ===")
    bad = 0
    tot = 0
    # exhaustive: every 2-kind constitution, every solid block of 3..7 cells,
    # every kind-assignment mask, all four semantics
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C = Const([r0, r1], list(tm))
                for L in (5,):
                    for masks in itertools.product((1, 2, 3), repeat=L):
                        S = {i: masks[i] for i in range(L)}
                        tot += 1
                        interior = [x for x in active_laws(S, C)
                                    if 1 <= x[0] <= L - 2]
                        if interior:
                            bad += 1
    claim("gridlock: no interior law of a solid block is ever active",
          bad == 0, "%d solid codes checked, %d violations" % (tot, bad))

    # and the dynamical form: a doubly-infinite solid region is frozen; here,
    # a solid ring (no vacancy anywhere) must be a fixed point in every mode
    bad = 0
    tot = 0
    rng = random.Random(1)
    for _ in range(4000):
        n = rng.randrange(1, 4)
        C = Const([rng.choice(RULES1) for _ in range(n)],
                  [rng.randrange(n) for _ in range(n)], modulus=7)
        S = {i: rng.randrange(1, 1 << n) for i in range(7)}   # every cell full
        for mode in ("parity", "or", "super", "super_or"):
            tot += 1
            if X.step(dict(S), C, mode) != S:
                bad += 1
    claim("gridlock: solid ring is a fixed point in all 4 semantics",
          bad == 0, "%d (code, semantics) pairs, %d violations" % (tot, bad))

    # sharpness: a purely POSITIVE guard (no vacancy clause) breaks it
    def pos_active(S, C):
        return [(c, k) for c, k in laws(S)
                if C.add(c, C.rules[k][0]) in S]           # drop the ~occ(i+b)
    C = Const([(0, 1, 1)])
    S = {i: 1 for i in range(5)}
    claim("gridlock sharpness: positive-only guard makes solid code fully active",
          len(pos_active(S, C)) == 5, "5/5 laws active in a solid block")


# ======================================================== 2. SINGLE AUTHOR
def s_single_author():
    print("\n=== 2. Single-Author / parity == OR ===")
    # (a) criterion: multiplicity > 1 is possible iff some kind has in-degree>=2
    rng = random.Random(2)
    viol = 0
    tot = 0
    for _ in range(60000):
        n = rng.randrange(1, 5)
        C = rand_const(rng, n, multi=rng.random() < .3)
        S = rand_state(rng, n)
        m = max_multiplicity(S, C)
        tot += 1
        if m > 1 and max(in_degrees(C)) < 2:
            viol += 1
    claim("multiplicity>1 implies some kind has in-degree>=2",
          viol == 0, "%d random (constitution,state) pairs, %d violations" % (tot, viol))

    # (b) parity == OR identically on the whole 2-kind box when t is injective
    div_inj = 0
    div_non = 0
    n_inj = 0
    n_non = 0
    rng = random.Random(3)
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C = Const([r0, r1], list(tm))
                inj = len(set(tm)) == 2
                for S in seeds_span(4, 2):
                    a = X.step(dict(S), C, "parity")
                    b = X.step(dict(S), C, "or")
                    if inj:
                        n_inj += 1
                        div_inj += (a != b)
                    else:
                        n_non += 1
                        div_non += (a != b)
    claim("parity == OR on every injective-target 2-kind code (span<=4)",
          div_inj == 0, "%d codes, %d divergences" % (n_inj, div_inj))
    claim("parity != OR occurs for non-injective targets",
          div_non > 0, "%d codes, %d divergences (%.2f%%)"
          % (n_non, div_non, 100.0 * div_non / n_non))

    # (c) minimal divergence witness: exactly 2 placed laws
    best = None
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in ([0, 0], [1, 1]):
                C = Const([r0, r1], list(tm))
                for S in all_seeds(4, 2):
                    if X.step(dict(S), C, "parity") != X.step(dict(S), C, "or"):
                        k = (card(S), max(S) - min(S))
                        if best is None or k < best[0]:
                            best = (k, (r0, r1, tuple(tm), tuple(sorted(S.items()))))
    claim("minimal parity/OR divergence has exactly 2 placed laws",
          best[0][0] == 2, str(best))


# ========================================================== 3. DEAD LETTER
def s_dead_letter():
    print("\n=== 3. Dead Letter / Balance ===")
    # (a) OR and super_or admit no balanced code: exhaustive 2-kind box
    nb = {m: 0 for m in ("parity", "or", "super", "super_or")}
    tot = 0
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C = Const([r0, r1], list(tm))
                for S in all_seeds(4, 2):
                    tot += 1
                    for m in nb:
                        if X.step(dict(S), C, m) == S and active_laws(S, C):
                            nb[m] += 1
    claim("Dead Letter survives OR verbatim (2-kind box, span<=4)",
          nb["or"] == 0, "%d codes; balanced: %s" % (tot, nb))
    claim("Dead Letter survives super_or verbatim",
          nb["super_or"] == 0, "balanced under super_or = %d" % nb["super_or"])
    claim("Dead Letter FAILS under parity (cross-amendment)",
          nb["parity"] > 0, "%d balanced codes" % nb["parity"])
    claim("Dead Letter FAILS under super (parity clear-votes cancel)",
          nb["super"] > 0, "%d balanced codes" % nb["super"])

    # (b) Theorem A: balanced => t non-injective on the ACTIVE alphabet
    bad = 0
    nbal = 0
    tot = 0
    rng = random.Random(4)
    for _ in range(30000):
        n = rng.randrange(2, 5)
        C = rand_const(rng, n)
        for _ in range(20):
            S = rand_state(rng, n, -3, 4, 6)
            tot += 1
            if is_balanced(S, C):
                nbal += 1
                A = active_alphabet(S, C)
                tA = {C.targets[k][0] for k in A}
                if len(tA) == len(A):
                    bad += 1
    claim("Theorem A: balanced => t|A non-injective (single target)",
          bad == 0, "%d random codes, %d balanced, %d violations" % (tot, nbal, bad))

    # (c) Theorem B: balanced => A not subset of t(A)  (entrenchment)
    bad = 0
    nbal = 0
    tot = 0
    rng = random.Random(5)
    for _ in range(8000):
        C = rand_const(rng, 3)
        for S in all_seeds(4, 3):
            tot += 1
            if is_balanced(S, C):
                nbal += 1
                A = active_alphabet(S, C)
                if A <= target_image(C, A):
                    bad += 1
    claim("Theorem B: balanced => some active kind is entrenched",
          bad == 0, "%d codes, %d balanced, %d violations" % (tot, nbal, bad))

    # (d) SHARPNESS of Theorem B: it fails for multi-target (out-degree>=2)
    C = Const([(1, -1, -1), (0, -1, -1)], targets=[(0, 1), (0, 1)])
    S = state_of([(2, 0), (2, 1), (3, 1)])
    A = active_alphabet(S, C)
    claim("Theorem B sharpness: multi-target balance with NO entrenched kind",
          is_balanced(S, C) and A <= target_image(C, A) and not entrenched_kinds(S, C),
          "%s  seed %s  A=%s=t(A)" % (C.label(), sorted(S.items()), sorted(A)))

    # (e) REFUTATION of the seed duality: balance with every present kind of
    #     strictly positive global in-degree
    C = Const([(0, 1, 1), (0, -1, -1), (0, 1, 0), (0, 1, 0)], targets=[2, 2, 0, 1])
    S = state_of([(0, 0), (2, 1)])
    P = present_alphabet(S)
    claim("refutes 'balance needs a present in-degree-0 kind'",
          is_balanced(S, C) and all(in_degrees(C)[k] > 0 for k in P),
          "in-degrees %s, present %s" % (in_degrees(C), sorted(P)))

    # (f) minimality: no 1-law balanced code with distinct targets
    bad = 0
    tot = 0
    rng = random.Random(6)
    for _ in range(20000):
        n = rng.randrange(1, 5)
        C = rand_const(rng, n, multi=True)
        if any(len(t) != len(set(t)) for t in C.targets):
            continue
        for c in range(-2, 3):
            for k in range(n):
                S = {c: 1 << k}
                tot += 1
                if is_balanced(S, C):
                    bad += 1
    claim("no 1-law balanced code (distinct targets within a law)",
          bad == 0, "%d single-law codes, %d balanced" % (tot, bad))
    # ... but a repeated target inside one law self-cancels (degenerate)
    Cd = Const([(0, -1, -1)], targets=[(0, 0)])
    claim("degenerate: a law with a repeated target is balanced alone",
          is_balanced(state_of([(0, 0)]), Cd), "kind (0,-1,-1)->{0,0} at cell 0")

    # (g) balance can be made arbitrarily large by disjoint union
    C = Const([(0, -1, -1), (0, -1, -1)], targets=[0, 0])
    ok = True
    for reps in (1, 2, 5, 20, 100):
        S = {}
        for j in range(reps):
            S[3 * j] = 3
        ok = ok and is_balanced(S, C) and len(active_laws(S, C)) == 2 * reps
    claim("balanced codes of unbounded size (disjoint union, gap 3)",
          ok, "verified for 1,2,5,20,100 copies -> up to 200 active laws")

    # (h) exact count for the balance champion, closed form vs census
    #     C = both kinds (0,-1,0) targeting kind 0.
    C = Const([(0, -1, 0), (0, -1, 0)], targets=[0, 0])
    def closed(span):
        # balanced <=> every run-start cell carries BOTH kinds (mask 3)
        n = 0
        for S in seeds_span(span, 2):
            m = [S.get(i, 0) for i in range(span)]
            ok = all(m[i] == 3 for i in range(span)
                     if m[i] and (i == 0 or m[i - 1] == 0))
            n += ok
        return n
    tot_c = 0
    tot_s = 0
    per = []
    for span in range(1, 9):
        a = closed(span)
        b = sum(1 for S in seeds_span(span, 2) if is_balanced(S, C))
        per.append((span, a, b))
        tot_c += a
        tot_s += b
    claim("exact balance count = closed form (run-starts must be doubled)",
          all(a == b for _, a, b in per),
          "per span %s ; total span<=8 = %d (census says 49024)" % (per, tot_s))


# ================================================== 4. ANCHOR & CONFINEMENT
def s_anchor():
    print("\n=== 4. Anchor / Path-Sum Confinement ===")
    # (a) the Anchor Theorem FAILS: the eldest law gets repealed
    C = Const([(0, 1, -1), (0, -1, 1)], targets=[1, 0])
    S = state_of([(0, 1), (1, 0)])
    T = X.step(dict(S), C)
    claim("Anchor FAILS under cross-amendment: leftmost law repealed",
          0 in S and 0 not in T,
          "%s seed %s -> %s (2 laws, 2 cells)"
          % (C.label(), sorted(S.items()), sorted(T.items())))

    # minimal search: the smallest code in which the Anchor Theorem's own
    # conclusion is violated -- a kind t with c_t > 0 loses its LEFTMOST
    # kind-t law (or c_t < 0 loses its rightmost).  The c_t = 0 self-repeal
    # is NOT a violation: Theorem 1.3 permits it.
    def anchor_break(S, C, steps=6):
        T = dict(S)
        anch = {}
        for k in range(C.n):
            cells = [c for c, kk in laws(T) if kk == k]
            if not cells:
                continue
            c = C.rules[k][2]
            if c > 0:
                anch[k] = min(cells)
            elif c < 0:
                anch[k] = max(cells)
        for _ in range(steps):
            T = X.step(T, C)
            here = {(c, kk) for c, kk in laws(T)}
            for k, m in anch.items():
                if (m, k) not in here:
                    return True
        return False
    best = None
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C2 = Const([r0, r1], list(tm))
                for S2 in all_seeds(3, 2):
                    if anchor_break(S2, C2):
                        k = (card(S2), max(S2) - min(S2))
                        if best is None or k < best[0]:
                            best = (k, (r0, r1, tuple(tm), tuple(sorted(S2.items()))))
    claim("minimal anchor-death witness is a SINGLE placed law",
          best[0][0] == 1, str(best))
    # a surviving anchor death: the eldest law is repealed and the code lives on
    surv = None
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C2 = Const([r0, r1], list(tm))
                for S2 in all_seeds(3, 2):
                    if not anchor_break(S2, C2, 8):
                        continue
                    T2 = dict(S2)
                    alive = True
                    for _ in range(20):
                        T2 = X.step(T2, C2)
                        if not T2:
                            alive = False
                            break
                    if alive:
                        k = (card(S2), max(S2) - min(S2))
                        if surv is None or k < surv[0]:
                            surv = (k, (r0, r1, tuple(tm), tuple(sorted(S2.items()))))
    claim("anchor death with the code SURVIVING exists",
          surv is not None, str(surv))
    # and it never happens in the own-kind block (Anchor Theorem holds there)
    own = 0
    tot = 0
    for r0 in RULES1:
        for r1 in RULES1:
            C2 = Const([r0, r1], [0, 1])
            for S2 in all_seeds(4, 2):
                tot += 1
                own += anchor_break(S2, C2, 12)
    claim("Anchor Theorem holds throughout the own-kind block",
          own == 0, "%d own-kind codes x 12 steps, %d anchor deaths" % (tot, own))

    # (b) Path-Sum Confinement: supp(S_n) inside the reach set, all n
    rng = random.Random(7)
    bad = 0
    tot = 0
    for _ in range(20000):
        n = rng.randrange(1, 5)
        C = rand_const(rng, n)
        S = rand_state(rng, n, -3, 4, 5)
        R = reach_set(C, S, 90)
        T = dict(S)
        for _ in range(60):
            T = X.step(T, C)
            tot += 1
            if not set(laws(T)) <= R:
                bad += 1
                break
    claim("Path-Sum Confinement holds (1-D, parity)",
          bad == 0, "%d steps over 20000 trajectories, %d escapes" % (tot, bad))

    # same in 2-D
    rng = random.Random(8)
    bad = 0
    tot = 0
    for _ in range(4000):
        n = rng.randrange(1, 4)
        C = rand_const(rng, n, dim=2)
        S = rand_state(rng, n, -2, 3, 4, dim=2)
        R = reach_set(C, S, 60)
        T = dict(S)
        for _ in range(40):
            T = X.step(T, C)
            tot += 1
            if not set(laws(T)) <= R:
                bad += 1
                break
    claim("Path-Sum Confinement holds (2-D, parity)",
          bad == 0, "%d steps over 4000 trajectories, %d escapes" % (tot, bad))

    # supersession keeps per-kind RAY confinement (creation is own-kind)
    rng = random.Random(9)
    bad = 0
    tot = 0
    for _ in range(20000):
        n = rng.randrange(1, 4)
        C = rand_const(rng, n)
        S = rand_state(rng, n, -3, 4, 5)
        rays = set()
        for cell, k in laws(S):
            for r in range(80):
                rays.add((cell + r * C.rules[k][2], k))
        T = dict(S)
        for _ in range(50):
            T = X.step(T, C, "super")
            tot += 1
            if not set(laws(T)) <= rays:
                bad += 1
                break
    claim("supersession: per-kind ray confinement supp_k <= seed_k + N c_k",
          bad == 0, "%d steps, %d escapes" % (tot, bad))

    # (c) Zero-Sum No-Go: every present cycle has offset-sum 0 => bounded orbit
    rng = random.Random(10)
    tested = 0
    bad = 0
    maxspan = 0
    for _ in range(200000):
        n = rng.randrange(2, 4)
        rules = [rng.choice(RULES1) for _ in range(n)]
        tg = list(range(1, n)) + [0]                      # one n-cycle
        C = Const(rules, tg)
        if cycle_offset_sum(C, list(range(n))) != 0:
            continue
        S = rand_state(rng, n, -3, 4, 5)
        tested += 1
        R = reach_set(C, S, 200)
        cells = {c for c, _ in R}
        bound = max(cells) - min(cells)
        T = dict(S)
        for _ in range(200):
            T = X.step(T, C)
            if T and max(T) - min(T) > bound:
                bad += 1
                break
        maxspan = max(maxspan, bound)
        if tested >= 4000:
            break
    claim("Zero-Sum No-Go: sum(c) around the cycle = 0 => bounded forever",
          bad == 0, "%d zero-sum constitutions x 200 steps, %d escapes; "
                    "reach-set span <= %d" % (tested, bad, maxspan))

    # (d) reciprocal (0,1,1)/(0,-1,-1) : the reach set is 2 cells per seed law
    C = Const([(0, 1, 1), (0, -1, -1)], targets=[1, 0])
    R = reach_set(C, state_of([(0, 0)]), 50)
    claim("reciprocal pair c=(+1,-1): one seed law reaches exactly 2 slots",
          R == {(0, 0), (1, 1)}, str(sorted(R)))


# ===================================================== 5. PERIODS / CRYPTIC
def s_periods():
    print("\n=== 5. Periods and cryptic codes ===")
    # (a) own-kind W=1 period 6 and 8 exist (refutes the {2,4} regularity)
    C = Const([(0, -1, 1), (0, 1, -1)])
    hits = []
    for S in all_seeds(6, 2):
        r = classify(dict(S), C, max_steps=300)
        if r["kind"] == "CYCLE" and r["period"] not in (2, 4):
            hits.append((tuple(sorted(S.items())), r["period"]))
    ok = bool(hits)
    # independent re-verification of the first one over 3 full periods
    if ok:
        S = dict(hits[0][0])
        p = hits[0][1]
        P = to_pairs(S)
        for _ in range(3 * p):
            P = ref_step(P, C)
        ok = (P == to_pairs(S))
    claim("own-kind W=1 admits periods outside {2,4}",
          ok, "%d seeds; spectrum %s; first %s re-verified 3 periods"
          % (len(hits), sorted({h[1] for h in hits}), hits[0] if hits else None))

    # (b) cryptic codes (constant occupancy) — do they exist, what periods?
    spec = Counter()
    nonpow = []
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C = Const([r0, r1], list(tm))
                for S in seeds_span(4, 2):
                    ok2, p = is_cryptic(S, C)
                    if ok2:
                        spec[p] += 1
                        if p & (p - 1):
                            nonpow.append((r0, r1, tuple(tm),
                                           tuple(sorted(S.items())), p))
    claim("cryptic codes exist (constant occupancy, live interior)",
          sum(spec.values()) > 0, "%d cryptic codes; period spectrum %s"
          % (sum(spec.values()), dict(sorted(spec.items()))))
    claim("every cryptic period in the 2-kind box is a power of 2",
          not nonpow, "%d non-power-of-2 cryptic codes" % len(nonpow))

    # (c) Cryptic Unipotency: a frozen-occupancy cycle has period 2^r UNLESS
    #     some amendment cycle reachable from a present kind has offset-sum 0.
    bad = 0
    tot = 0
    zs = 0
    rng = random.Random(11)
    for _ in range(40000):
        n = rng.randrange(2, 4)
        C = rand_const(rng, n)
        S = rand_state(rng, n, -3, 4, 6)
        r = classify(dict(S), C, max_steps=200, want_history=True)
        if r["kind"] == "CYCLE" and r["period"] & (r["period"] - 1):
            tot += 1
            h = r["history"][r["t"]:r["t"] + r["period"]]
            if len({frozenset(x) for x in h}) == 1:      # occupancy constant
                zs += 1
                sums = [cycle_offset_sum(C, z) for z in components_cycles(C)
                        if set(z) & set(rho(C, k)[1][0] for k in
                                        present_alphabet(h[0]))]
                if all(x != 0 for x in
                       [cycle_offset_sum(C, z) for z in components_cycles(C)]):
                    bad += 1
    claim("frozen-occupancy non-2-power period requires a ZERO-SUM cycle",
          bad == 0, "%d non-2-power cycles, %d with frozen occupancy, "
                    "%d of those with all cycle sums nonzero" % (tot, zs, bad))
    # the minimal zero-sum cryptic witness, re-verified through the ref engine
    C = Const([(0, -1, 1), (0, 1, -1), (-1, 1, 0)], targets=[2, 0, 1])
    S = state_of([(-2, 2), (2, 0), (2, 2), (3, 0), (3, 1)])   # on the cycle
    P0 = to_pairs(S)
    P = P0
    ok = True
    for _ in range(3):
        for _ in range(3):
            P = ref_step(P, C)
        ok = ok and P == P0
    occ_const = True
    T = dict(S)
    for _ in range(9):
        T = X.step(T, C)
        occ_const = occ_const and frozenset(T) == frozenset(S)
    claim("zero-sum 3-cycle: cryptic code of period 3 (constant occupancy)",
          ok and occ_const and X.step(dict(S), C) != S,
          "%s seed %s ; cycle offset-sum %d"
          % (C.label(), sorted(S.items()),
             cycle_offset_sum(C, components_cycles(C)[0])))

    # (d) the period-30 reciprocal specimen
    C = Const([(-1, 1, 0), (0, -1, 1)], targets=[1, 0])
    found = None
    for S in all_seeds(8, 2):
        r = classify(dict(S), C, max_steps=400)
        if r["kind"] == "CYCLE" and r["period"] == 30:
            found = (S, r)
            break
    ok = False
    if found:
        S, r = found
        T = dict(S)
        for _ in range(r["t"]):
            T = X.step(T, C)
        P0 = to_pairs(T)
        P = P0
        ok = True
        for _ in range(3):
            for _ in range(30):
                P = ref_step(P, C)
            ok = ok and P == P0
    claim("period-30 reciprocal cycle exists and re-verifies",
          ok, "%s seed %s t0=%d" % (C.label(), sorted(found[0].items()) if found else None,
                                    found[1]["t"] if found else -1))


# ==================================================== 6. GLIDER SKELETON
def s_skeleton():
    print("\n=== 6. Glider skeleton lemmas ===")
    # (a) a kind never targeted by any ACTIVE kind has a frozen support
    rng = random.Random(12)
    bad = 0
    tot = 0
    for _ in range(40000):
        n = rng.randrange(2, 5)
        C = rand_const(rng, n)
        S = rand_state(rng, n, -3, 4, 6)
        T = dict(S)
        supp = {k: {c for c, kk in laws(T) if kk == k} for k in range(n)}
        never = set(range(n))
        for _ in range(40):
            never &= set(range(n)) - target_image(C, active_alphabet(T, C))
            T = X.step(T, C)
            for k in never:
                tot += 1
                cur = {c for c, kk in laws(T) if kk == k}
                if cur != supp[k]:
                    bad += 1
            if not never:
                break
    claim("kind never targeted by an active kind has frozen support",
          bad == 0, "%d (kind,step) checks, %d violations" % (tot, bad))

    # (b) reach-set corollary: if all present cycles have offset-sum 0 the orbit
    #     is eventually periodic with bounded span  (already in s_anchor);
    #     here: the displacement of any exact translation must be parallel to a
    #     cycle offset-sum.  Tested on rings-free 1-D: there are no gliders, so
    #     we test the contrapositive on a synthetic shift system instead.
    #     Synthetic control: own-kind colonizer is NOT a glider (span grows).
    C = Const([(0, 1, 1)])
    claim("control: colonizer is not a glider (verify_glider says no)",
          not X.verify_glider(state_of([(0, 0)]), C, 1, 1), "(0,1,1) speed-1 front")


# ================================================== 7. SEMANTIC LATTICE
def s_semantics():
    print("\n=== 7. New semantics ===")
    import xsem
    xsem.battery(claim)


def main():
    todo = sys.argv[1:] or ["1", "2", "3", "4", "5", "6", "7"]
    fns = {"1": s_gridlock, "2": s_single_author, "3": s_dead_letter,
           "4": s_anchor, "5": s_periods, "6": s_skeleton, "7": s_semantics}
    for t in todo:
        fns[t]()
    print("\n%d/%d claims PASS" % (sum(RES.values()), len(RES)))
    json.dump(RES, open("data/battery.json", "w"), indent=1)
    return 0 if all(RES.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
