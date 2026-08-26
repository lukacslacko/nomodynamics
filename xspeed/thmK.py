#!/usr/bin/env python3
"""
thmK.py — test of the Even-Support Law (Theorem K) and of the elementary
front/rear channel dichotomy (Lemma FR), by adversarial fuzzing against the
reference engine `xnomos`.

Theorem K (parity resolution).  Let A in F2^{n x n} be the amendment incidence
matrix, A[m][k] = 1 iff m in T_k.  For every u in F2^n with u^T A = 0 (i.e.
|T_k ∩ U| is even for every kind k, where U = supp u), the set

        Y_U(t) = symmetric difference over m in U of supp_m(t)

is CONSTANT along every orbit; and in a free glider Y_U is empty, i.e. every
cell carries an even number of kinds of U at every time.

  * |U| = 2 with equal author sets is X-A's Twin-Kind Lemma (§8.5).
  * |U| = 3 examples exist with no two kinds twinned, e.g.
    T = [{0,1},{1,2},{0,2}] : |T_k ∩ {0,1,2}| = 2 for every k.
  * det A over F2 is the parity of the number of cycle covers of the
    amendment digraph, and the left kernel is non-trivial exactly when that
    parity is 0.

Lemma FR (any resolution).  For a glider with d > 0: the front satisfies
beta(t+1) <= beta(t) + max_k c_k, and the rearmost occupied cell can only be
repealed by a kind with c_k <= 0.
"""
from __future__ import annotations

import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "xamend1d"))
sys.path.insert(0, os.path.dirname(HERE))

import xnomos  # noqa: E402


def kernel_sets(T, n):
    """All non-empty U ⊆ K with |T_k ∩ U| even for every k."""
    out = []
    for r in range(1, n + 1):
        for U in itertools.combinations(range(n), r):
            s = set(U)
            if all(len(s & set(T[k])) % 2 == 0 for k in range(n)):
                out.append(s)
    return out


def parity_of_cycle_covers(T, n):
    """#{permutations pi with pi(m) -> m for all m} mod 2 = det A over F2."""
    A = [[1 if m in T[k] else 0 for k in range(n)] for m in range(n)]
    cnt = 0
    for pi in itertools.permutations(range(n)):
        if all(A[m][pi[m]] for m in range(n)):
            cnt += 1
    return cnt % 2


def det_f2(T, n):
    A = [[1 if m in T[k] else 0 for k in range(n)] for m in range(n)]
    A = [row[:] for row in A]
    det = 1
    for col in range(n):
        piv = next((r for r in range(col, n) if A[r][col]), None)
        if piv is None:
            return 0
        A[col], A[piv] = A[piv], A[col]
        for r in range(col + 1, n):
            if A[r][col]:
                A[r] = [x ^ y for x, y in zip(A[r], A[col])]
    return det


def fuzz(trials=4000, seed=1):
    rng = random.Random(seed)
    stats = dict(K_checks=0, K_viol=0, K_universes=0,
                 FR_checks=0, FR_viol=0, det_checks=0, det_viol=0,
                 nontwin_K=0)
    for _ in range(trials):
        n = rng.randint(2, 5)
        W = rng.randint(1, 3)
        T = [tuple(sorted(rng.sample(range(n), rng.randint(1, n))))
             for _ in range(n)]
        rules = [(rng.randint(-W, W), rng.randint(-W, W), rng.randint(-W, W))
                 for _ in range(n)]
        C = xnomos.Const(rules, T)
        # -- det A over F2 == parity of cycle covers
        stats["det_checks"] += 1
        if det_f2(T, n) != parity_of_cycle_covers(T, n):
            stats["det_viol"] += 1
        Us = kernel_sets(T, n)
        # a U is "non-twin" if no pair inside it has equal author sets
        def authors(m):
            return frozenset(k for k in range(n) if m in T[k])
        for U in Us:
            if len(U) > 2 and len(set(authors(m) for m in U)) == len(U):
                stats["nontwin_K"] += 1
        if Us:
            stats["K_universes"] += 1
        # random state
        S = {}
        for i in range(rng.randint(1, 10)):
            cell = rng.randint(0, 9)
            S[cell] = S.get(cell, 0) | (1 << rng.randrange(n))
        S = {c: m for c, m in S.items() if m}
        if not S:
            continue
        # Y_U constant along the orbit (parity resolution)
        base = {}
        for U in Us:
            base[tuple(sorted(U))] = frozenset(
                c for c, msk in S.items()
                if bin(msk & sum(1 << m for m in U)).count("1") % 2)
        Tst = dict(S)
        prev = dict(S)
        for _ in range(12):
            Tst = xnomos.step(Tst, C, "parity")
            for U in Us:
                key = tuple(sorted(U))
                cur = frozenset(c for c, msk in Tst.items()
                                if bin(msk & sum(1 << m for m in U)).count("1") % 2)
                stats["K_checks"] += 1
                if cur != base[key]:
                    stats["K_viol"] += 1
            # Lemma FR: rearmost repeal needs c_k <= 0
            if prev and Tst:
                a = min(prev)
                if a not in Tst or (prev[a] & ~Tst.get(a, 0)):
                    # some kind at the rearmost cell was repealed
                    stats["FR_checks"] += 1
                    lost = prev[a] & ~Tst.get(a, 0)
                    ok = True
                    for m in range(n):
                        if not (lost >> m) & 1:
                            continue
                        # an author k with m in T_k, active at a - c_k, must exist
                        acts = xnomos.active_laws(prev, C)
                        good = any(m in T[k] and (a - rules[k][2]) == cell
                                   for (cell, k) in acts)
                        if good:
                            hit = [k for (cell, k) in acts
                                   if m in T[k] and (a - rules[k][2]) == cell]
                            if not any(rules[k][2] <= 0 for k in hit):
                                ok = False
                    if not ok:
                        stats["FR_viol"] += 1
            prev = dict(Tst)
            if not Tst:
                break
    return stats


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    st = fuzz(n)
    for k in sorted(st):
        print("%-14s %d" % (k, st[k]))
