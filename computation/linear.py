#!/usr/bin/env python3
"""
linear.py — THE UNCONDITIONAL SECTOR IS LINEAR, AND THEREFORE TAME.

anon.py and turing.py put universality inside the field.  This file locates it:
ALL of the computation lives in the VACANCY CLAUSE.

A kind is UNCONDITIONAL if its guard is vacuously true — cite yourself at your
own cell (a law of kind k does stand at i+0 when the kind-k law is at i) and let
the vacancy clause name a kind that is never enacted.  Then every placed law
acts at every step, and the dynamics loses its only nonlinearity:

    THEOREM 3.  If every kind of C is unconditional, then Phi is F2-LINEAR.
    Writing a code as a vector of Laurent polynomials x in (F2[z,1/z])^n, with
    x_k the indicator series of the kind-k laws,

            Phi(x) = L x ,      L = I + A ,   A[v][k] = [v in T_k] . z^{c_k}

    so Phi^t = L^t, computable by ceil(log2 t) squarings of an n x n matrix of
    Laurent polynomials rather than by t simulation steps.

    COROLLARY 3.1 (Pascal).  For n = 1 with T = {k} and offset c, a one-law seed
    gives x(t) = (1 + z^c)^t, whose support has exactly 2^popcount(t) cells by
    Lucas's theorem — the *Pascal columns* of chapter one, explained.

    COROLLARY 3.2 (tameness).  Iterated squaring of a polynomial matrix is an
    arithmetic circuit of depth O(log^2 t) and polynomial size, so PREDICT
    restricted to the unconditional sector is in NC.  It is therefore NOT
    P-complete unless NC = P — in contrast with THEOREM 2, where the general
    problem is P-complete, and with THEOREMS 4 and 5, where the same field with
    live guards simulates every Turing machine.

    *What computes in nomodynamics is not the amendment.  It is the exception.*

Run `python3 linear.py`.
"""

from __future__ import annotations

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xnomos import Const, state_of, step, laws, card               # noqa: E402


# ------------------------------------------------- Laurent polynomials over F2
# A polynomial is a frozenset/dict of exponents with coefficient 1.


def pmul(p, q):
    out = set()
    for a in p:
        for b in q:
            e = a + b
            if e in out:
                out.discard(e)
            else:
                out.add(e)
    return out


def padd(p, q):
    return set(p) ^ set(q)


def mmul(P, Q, n):
    R = [[set() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if not P[i][k]:
                continue
            for j in range(n):
                if Q[k][j]:
                    R[i][j] ^= pmul(P[i][k], Q[k][j])
    return R


def midentity(n):
    return [[({0} if i == j else set()) for j in range(n)] for i in range(n)]


def mpow(L, t, n):
    """L^t by repeated squaring; returns (matrix, number of squarings)."""
    R = midentity(n)
    B = [row[:] for row in L]
    sq = 0
    while t:
        if t & 1:
            R = mmul(R, B, n)
        t >>= 1
        if t:
            B = mmul(B, B, n)
            sq += 1
    return R, sq


# ---------------------------------------------------------- the linear sector


def unconditional(rules, targets):
    """A Const in which every law is active at every step (citation sector)."""
    n = len(rules)
    NILK = n                                   # a kind that is never enacted
    rules = [(0, r[1], r[2]) for r in rules] + [(0, 0, 0)]
    targets = [tuple(t) for t in targets] + [()]
    guards = [(k, NILK) for k in range(n)] + [(NILK, NILK)]
    return Const(rules, targets, dim=1, guards=guards), n


def matrix_of(C, n):
    L = midentity(n)
    for k in range(n):
        c = C.rules[k][2]
        for v in C.targets[k]:
            if v < n:
                L[v][k] ^= {c}
    return L


def state_to_vec(S, n):
    return [{cell for cell, m in S.items() if (m >> k) & 1} for k in range(n)]


def vec_to_state(x, n):
    pl = []
    for k in range(n):
        for e in x[k]:
            pl.append((e, k))
    return state_of(pl)


def apply_matrix(L, x, n):
    return [set().union(*[pmul(L[i][k], x[k]) for k in range(n)])
            if False else
            _rowmul(L, x, n, i) for i in range(n)]


def _rowmul(L, x, n, i):
    acc = set()
    for k in range(n):
        if L[i][k] and x[k]:
            acc ^= pmul(L[i][k], x[k])
    return acc


# ---------------------------------------------------------------- certificates


def certify_linearity(trials=400, seed=13):
    """Phi = L on random unconditional constitutions and random codes."""
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        n = rng.randrange(1, 5)
        rules = [(0, rng.randrange(-1, 2), rng.randrange(-1, 2))
                 for _ in range(n)]
        targets = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                   for _ in range(n)]
        C, n = unconditional(rules, targets)
        L = matrix_of(C, n)
        S = state_of([(rng.randrange(-4, 5), rng.randrange(n))
                      for _ in range(rng.randrange(1, 9))])
        T = step(S, C, "parity")
        got = state_to_vec(T, n)
        want = _rowmulall(L, state_to_vec(S, n), n)
        if got != want:
            bad += 1
        # and OR must agree too when author multiplicity is 1
    return bad, trials


def _rowmulall(L, x, n):
    return [_rowmul(L, x, n, i) for i in range(n)]


def certify_powering(trials=60, seed=31, tmax=40):
    """L^t computed by squaring vs. t simulation steps of xnomos."""
    rng = random.Random(seed)
    bad = 0
    sqs = []
    for _ in range(trials):
        n = rng.randrange(1, 4)
        rules = [(0, 0, rng.randrange(-1, 2)) for _ in range(n)]
        targets = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                   for _ in range(n)]
        C, n = unconditional(rules, targets)
        L = matrix_of(C, n)
        t = rng.randrange(1, tmax)
        S = state_of([(rng.randrange(-3, 4), rng.randrange(n))
                      for _ in range(rng.randrange(1, 5))])
        x = state_to_vec(S, n)
        Lt, sq = mpow(L, t, n)
        pred = _rowmulall(Lt, x, n)
        sqs.append(sq)
        T = dict(S)
        for _ in range(t):
            T = step(T, C, "parity")
        if state_to_vec(T, n) != pred:
            bad += 1
    return bad, trials, max(sqs)


def certify_pascal(tmax=1 << 12):
    """|S_t| = 2^popcount(t) for a one-law seed of a single unconditional kind."""
    C, n = unconditional([(0, 0, 1)], [(0,)])
    S = state_of([(0, 0)])
    bad = 0
    checked = 0
    t = 0
    L = matrix_of(C, n)
    while t < tmax:
        if bin(t).count("1") <= 6:
            Lt, _ = mpow(L, t, n)
            x = _rowmulall(Lt, state_to_vec(state_of([(0, 0)]), n), n)
            if len(x[0]) != 2 ** bin(t).count("1"):
                bad += 1
            checked += 1
        t += 1
    # and against the engine, for small t
    S = state_of([(0, 0)])
    for t in range(200):
        if card(S) != 2 ** bin(t).count("1"):
            bad += 1
        S = step(S, C, "parity")
    return bad, checked + 200


def _main():
    print("THE UNCONDITIONAL SECTOR (every guard vacuously true)")
    bad, n = certify_linearity()
    print("  Phi = L over F2[z,1/z]: %d random constitutions x random codes, "
          "%d deviations" % (n, bad))
    assert bad == 0
    bad, n, sq = certify_powering()
    print("  Phi^t = L^t by repeated squaring vs. t engine steps: %d trials, "
          "%d deviations" % (n, bad))
    print("     (at most %d squarings replaced up to 39 simulation steps)" % sq)
    assert bad == 0
    bad, n = certify_pascal()
    print("  Pascal / Lucas: |S_t| = 2^popcount(t) for the one-kind "
          "unconditional grower")
    print("     %d checks (engine t<200 and matrix powers to t<4096), %d "
          "deviations" % (n, bad))
    assert bad == 0
    print("  => the unconditional sector is F2-linear; PREDICT restricted to "
          "it is in NC,")
    print("     hence not P-complete unless NC = P.  All the computation is "
          "in the guard.")
    print("linear self-tests passed")


if __name__ == "__main__":
    _main()
