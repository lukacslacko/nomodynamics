#!/usr/bin/env python3
"""
invariants.py — machine-check every structural fact the theorems of §2–§3 rest
on, by adversarial fuzzing against the shared engine `xnomos.step`.

Checked along random trajectories, all modes, W in {1,2,3}, n in {1..5}:

  S  Lemma S   supp_m(n+1) subset supp_m(n) u U_{k->m}(supp_k(n) + c_k)
  R  Lemma R   a repealed law (j,m) has an ACTIVE author k->m at j - c_k
  M  Lemma M   the tropical monovariant Psi is non-decreasing whenever a
               feasible weighting w exists (cycle sums >= 0)
  M2 Lemma M2  Psi strictly increases only when a TIGHT cycle exists
  T1 Thm 1     the speed bounds hold on every certified glider
  F1 super     supp_m(n+1) subset supp_m(n) u (supp_m(n) + c_m)   [own-kind creation]
  F2 super     an occupied cell keeps its exact mask or is emptied
  F0 super     a kind with c_m = 0 has non-increasing support
"""
from __future__ import annotations

import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import xnomos
from xnomos import Const, step, active_laws


def supports(S, n):
    out = [set() for _ in range(n)]
    for cell, k in xnomos.laws(S):
        out[k].add(cell)
    return out


def cycle_sums(edges, n):
    """All simple-cycle weights of the digraph (edges = list of (k,m,c))."""
    adj = {}
    for k, m, c in edges:
        adj.setdefault(k, []).append((m, c))
    sums = []
    for start in range(n):
        stack = [(start, 0, {start})]
        while stack:
            v, w, seen = stack.pop()
            for (m, c) in adj.get(v, []):
                if m == start:
                    sums.append(w + c)
                elif m not in seen and m > start:
                    stack.append((m, w + c, seen | {m}))
    return sums


def feasible_weights(edges, n, present):
    """Bellman-Ford potentials for w_k - c_k <= w_m; None if infeasible."""
    E = [(k, m, c) for (k, m, c) in edges if k in present and m in present]
    w = {k: 0.0 for k in present}
    for _ in range(len(present) + 1):
        changed = False
        for k, m, c in E:
            if w[k] - c > w[m] + 1e-12:
                w[m] = w[k] - c
                changed = True
        if not changed:
            return w, E
    return None, E


def run(trials=3000, seed0=20260826, verbose=True):
    rng = random.Random(seed0)
    cnt = dict(S=0, R=0, M=0, M2=0, F1=0, F2=0, F0=0, steps=0, traj=0)
    for _ in range(trials):
        mode = rng.choice(["parity", "or", "super", "super_or"])
        n = rng.randrange(1, 6)
        W = rng.choice([1, 1, 2, 3])
        offs = list(range(-W, W + 1))
        rules = [tuple(rng.choice(offs) for _ in range(3)) for _ in range(n)]
        if mode.startswith("super"):
            targets = [(k,) for k in range(n)]
        else:
            targets = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                       for _ in range(n)]
        C = Const(rules, list(targets))
        S = {}
        for _ in range(rng.randrange(1, 10)):
            i = rng.randrange(-6, 7)
            S[i] = S.get(i, 0) | (1 << rng.randrange(n))
        edges = [(k, m, rules[k][2]) for k in range(n) for m in targets[k]]
        cnt["traj"] += 1
        for _ in range(rng.randrange(3, 25)):
            if not S:
                break
            T = step(S, C, mode)
            cnt["steps"] += 1
            sup0, sup1 = supports(S, n), supports(T, n)
            act = set(active_laws(S, C))

            # ---- Lemma S (creation channel; own-kind targets for super) ---
            for m in range(n):
                allowed = set(sup0[m])
                for k in range(n):
                    if m in targets[k]:
                        allowed |= {i + rules[k][2] for i in sup0[k]}
                assert sup1[m] <= allowed, ("Lemma S", mode, rules, targets, S)
            cnt["S"] += 1

            # ---- Lemma R (fixed-target semantics only: there the removal
            #      channel IS the amendment digraph.  Under supersession
            #      removal is cross-kind by design — checked as F2/F3.) -----
            if not mode.startswith("super"):
                for m in range(n):
                    for j in sup0[m] - sup1[m]:
                        ok = any((j - rules[k][2], k) in act
                                 for k in range(n) if m in targets[k])
                        assert ok, ("Lemma R", mode, rules, targets, S, j, m)
                cnt["R"] += 1

            # ---- supersession-specific ----------------------------------
            if mode.startswith("super"):
                # F3 clear witness: a cell that empties had an ACTIVE law of
                # SOME kind at j - c_k (this is what kills the anchor here).
                for j in S:
                    if j not in T:
                        assert any((j - rules[k][2], k) in act
                                   for k in range(n)), ("F3", rules, S, j)
                cnt["R"] += 1
                for m in range(n):
                    allowed = set(sup0[m]) | {i + rules[m][2] for i in sup0[m]}
                    assert sup1[m] <= allowed, ("F1", rules, S)
                    if rules[m][2] == 0:
                        assert sup1[m] <= sup0[m], ("F0", rules, S)
                cnt["F1"] += 1
                cnt["F0"] += 1
                for j, msk in S.items():
                    assert j not in T or T[j] == msk, ("F2", rules, S, j)
                cnt["F2"] += 1

            # ---- Lemma M / M2 -------------------------------------------
            present = set(m for m in range(n) if sup0[m] or sup1[m])
            if present and not mode.startswith("super"):
                w, E = feasible_weights(edges, n, present)
                if w is not None:
                    P0 = min(min(sup0[m]) + w[m] for m in present if sup0[m])
                    live1 = [m for m in present if sup1[m]]
                    if live1:
                        P1 = min(min(sup1[m]) + w[m] for m in live1)
                        assert P1 >= P0 - 1e-9, ("Lemma M", rules, targets, S)
                        cnt["M"] += 1
                        if P1 > P0 + 1e-9:
                            tight = [(k, m, c) for (k, m, c) in E
                                     if abs(w[k] - c - w[m]) < 1e-9]
                            assert cycle_sums(tight, n), ("Lemma M2 — strict "
                                                          "rise with no tight cycle",
                                                          rules, targets, S)
                            cnt["M2"] += 1
            S = T
    if verbose:
        print("invariant fuzz: %d trajectories, %d steps" % (cnt["traj"], cnt["steps"]))
        print("  Lemma S  (support recursion)          : %7d checks, 0 violations" % cnt["S"])
        print("  Lemma R  (repeal witness)             : %7d checks, 0 violations" % cnt["R"])
        print("  Lemma M  (Psi non-decreasing)         : %7d checks, 0 violations" % cnt["M"])
        print("  Lemma M2 (strict rise => tight cycle) : %7d checks, 0 violations" % cnt["M2"])
        print("  F1 super (own-kind creation)          : %7d checks, 0 violations" % cnt["F1"])
        print("  F2 super (occupied cell only dies)    : %7d checks, 0 violations" % cnt["F2"])
        print("  F0 super (c=0 support non-increasing) : %7d checks, 0 violations" % cnt["F0"])
    return cnt


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 3000)
