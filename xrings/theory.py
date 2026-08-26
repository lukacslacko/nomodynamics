#!/usr/bin/env python3
"""
theory.py — machine checks of the structural theorems of RESULTS.md.

T2  Own-kind unipotency (window 1).  On ANY frozen occupancy O of Z/m the
    own-kind per-kind operator D = sigma^c . diag(g) satisfies
      c = +-1 : D^m = 0            (nilpotent: gcd(c,m)=1 and A != Z/m)
      c = 0   : D^2 = D            (idempotent)
    hence I+D is unipotent / idempotent and every CONSTANT-OCCUPANCY own-kind
    cycle has period a power of two.  Checked over every (kind, m, O).

T3  Cross-amendment breaks it.  For an L-cycle constitution the one-step
    operator is I+N with N block-cyclic; N^L is block-diagonal with k-th block
    sigma^s . (mask), s = sum of the c's round the cycle.  N need NOT be
    nilpotent, and constant-occupancy cycles of non-power-of-2 period exist.
    Exhibited by exhaustive search.

T6  Light cone.  S_{t+1}(j) depends only on S_t(j-2..j+2).  Checked by
    perturbation on random states.
"""
import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from xring import Ring, RULES27, RULES12, decode     # noqa: E402


def mat_of_D(m, c, gmask):
    """D = sigma^c . diag(g) as a list of column bitmasks over m bits."""
    cols = []
    for i in range(m):
        v = 0
        if (gmask >> i) & 1:
            v = 1 << ((i + c) % m)
        cols.append(v)
    return cols


def compose(A, B, m):
    out = []
    for col in B:
        v = 0
        c = col
        while c:
            b = (c & -c).bit_length() - 1
            c &= c - 1
            v ^= A[b]
        out.append(v)
    return out


def t2():
    print("T2: own-kind window-1 nilpotency on every frozen occupancy")
    bad = 0
    tested = 0
    for m in range(3, 13):
        mask = (1 << m) - 1
        for (a, b, c) in RULES27:
            for O in range(1 << m):
                R = Ring([(a, b, c)], [0], m)
                g = R.rot(O, -a) & ~R.rot(O, -b) & mask
                D = mat_of_D(m, c, g)
                tested += 1
                if c == 0:
                    if compose(D, D, m) != D:
                        bad += 1
                else:
                    P = D
                    for _ in range(m - 1):
                        P = compose(D, P, m)
                    if any(P):
                        bad += 1
                        print("   NOT NILPOTENT", m, (a, b, c), bin(O))
    print("   (kind, m, occupancy) triples tested: %d   violations: %d"
          % (tested, bad))
    return bad


def const_occ_cycles(rules, targets, m, mode="parity"):
    """All cycles on which the occupancy never changes; return their periods."""
    R = Ring(rules, targets, m, mode)
    n = len(rules)
    seen = set()
    out = set()
    for v in range(1 << (n * m)):
        if v in seen:
            continue
        path = []
        X = decode(v, n, m)
        idx = {}
        while True:
            key = X
            if key in idx:
                p = len(path) - idx[key]
                cyc = path[idx[key]:]
                if len({R.occ(Z) for Z in cyc}) == 1:
                    out.add(p)
                break
            if key in seen:
                break
            idx[key] = len(path)
            path.append(X)
            X = R.step(X)
        for Z in path:
            seen.add(Z)
    return out


def n_matrix(R, O):
    """The nilpotent-candidate part N of the one-step operator I+N at frozen
    occupancy O, as columns over n*m bits."""
    n, m = R.n, R.m
    cols = []
    for k in range(n):
        for i in range(m):
            X = [0] * n
            X[k] = 1 << i
            act = []
            for kk in range(n):
                a, b, _ = R.rules[kk]
                act.append(X[kk] & R.rot(O, -a) & ~R.rot(O, -b) & R.mask)
            out = [0] * n
            for kk in range(n):
                out[R.targets[kk]] ^= R.rot(act[kk], R.rules[kk][2])
            v = 0
            for kk in range(n):
                v |= out[kk] << (kk * m)
            cols.append(v)
    return cols


def t3():
    print("\nT3: is the ONE-STEP operator unipotent under cross-amendment?")
    bad = tested = 0
    worst = {}
    for m in range(3, 9):
        for tg, name in (([0, 1], "own-kind"), ([1, 0], "2-cycle"),
                         ([0, 0], "non-injective")):
            for r1, r2 in itertools.product(RULES12, repeat=2):
                R = Ring([r1, r2], tg, m)
                for O in range(1 << m):
                    N = n_matrix(R, O)
                    P = N                     # square until exponent >= dim
                    e = 1
                    while e < 2 * m:
                        P = compose(P, P, 2 * m)
                        e *= 2
                    tested += 1
                    if any(P):
                        bad += 1
                        worst.setdefault(name, (m, r1, r2, O))
    print("   (constitution, m, occupancy) triples tested: %d" % tested)
    print("   N^(n*m) != 0 (i.e. NOT nilpotent, one step NOT unipotent): %d"
          % bad)
    for k, v in worst.items():
        print("     first non-nilpotent %s: m=%d %s %s O=%s"
              % (k, v[0], v[1], v[2], bin(v[3])))

    print("\nT3b: periods of CONSTANT-OCCUPANCY cycles (complete)")
    for tg, name in (([0], "own-kind 1 kind, all 27, m=3..9"),):
        s = set()
        for m in range(3, 10):
            for r in RULES27:
                s |= const_occ_cycles([r], tg, m)
        print("   %-42s : %s" % (name, sorted(s)))
    for tg, name in (([0, 1], "own-kind 2 live kinds, m=3..7"),
                     ([1, 0], "2-cycle permutation, 2 live kinds, m=3..7"),
                     ([0, 0], "non-injective, 2 live kinds, m=3..7")):
        s = set()
        for m in range(3, 8):
            for r1, r2 in itertools.product(RULES12, repeat=2):
                s |= const_occ_cycles([r1, r2], tg, m)
        print("   %-42s : %s" % (name, sorted(s)))
    s = set()
    for m in range(3, 6):
        for c in itertools.product(RULES12, repeat=3):
            s |= const_occ_cycles(list(c), [1, 2, 0], m)
    print("   %-42s : %s" % ("3-cycle permutation, live, m=3..5", sorted(s)))
    return bad


def t6(trials=4000, seed=99):
    print("\nT6: light cone — S_{t+1}(j) depends only on S_t(j-2..j+2)")
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        n = rng.randrange(1, 4)
        m = rng.randrange(7, 15)
        rules = [rng.choice(RULES27) for _ in range(n)]
        tg = [rng.randrange(n) for _ in range(n)]
        mode = rng.choice(["parity", "or", "super", "super_or"])
        R = Ring(rules, tg, m, mode)
        X = tuple(rng.getrandbits(m) for _ in range(n))
        j = rng.randrange(m)
        far = [i for i in range(m) if min((i - j) % m, (j - i) % m) > 2]
        if not far:
            continue
        i = rng.choice(far)
        k = rng.randrange(n)
        Y = list(X)
        Y[k] ^= 1 << i
        Y = tuple(Y)
        A = R.step(X)
        B = R.step(Y)
        for kk in range(n):
            if ((A[kk] >> j) & 1) != ((B[kk] >> j) & 1):
                bad += 1
                break
    print("   %d random single-cell perturbations at distance > 2: %d "
          "influenced the centre cell" % (trials, bad))
    return bad


if __name__ == "__main__":
    b2 = t2()
    t3()
    b34 = t34()
    b6 = t6()
    print("\nsummary: T2 violations=%d  T3.4 violations=%d  T6 violations=%d"
          % (b2, b34, b6))


def t34(hi=40):
    """The base own-kind rotor family, derived in RESULTS.md S3.4:
    X = {0, 1, g+2} on Z/(2g+4) satisfies Phi(X) = rot_{m/2}(X) for every
    g >= 1, and these are exactly the block words (2,g),(1,g+1)."""
    print("\nT3.4: the derived base family X = {0,1,g+2} on Z/(2g+4)")
    bad = 0
    for g in range(1, hi):
        m = 2 * g + 4
        X = (1 | 2 | (1 << (2 + g)),)
        R = Ring([(0, -1, 1)], [0], m)
        if R.step(X) != R.rot_state(X, m // 2):
            bad += 1
            print("   FAILS at g=%d (m=%d)" % (g, m))
    print("   g = 1..%d  (m = 6, 8, ..., %d): %d failures"
          % (hi - 1, 2 * (hi - 1) + 4, bad))
    return bad
