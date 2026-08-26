#!/usr/bin/env python3
"""
linorder.py — the multiplicative order of the FROZEN-OCCUPANCY step operator.

Fix an occupancy O.  The step is X -> M X with M = I + N over F2, N block-cyclic
(block-diagonal for own-kind).  The periods of every constant-occupancy cycle
divide the eventual multiplicative period q(M) of M in the matrix monoid
(smallest q with M^{K+q} = M^K for some K).  Own-kind window-1 forces each
block of N to be nilpotent (c = +-1) or idempotent (c = 0), so q(M) is a power
of 2.  For an L-cycle constitution N^L can be sigma^s times a mask, and the
subalgebra F2[N]/(N^L - 1) then contains F_{2^d}: for L = 3 that is F4, where
1 + omega = omega^2 has ORDER 3.  So q(M) = 3 becomes available -- and with it
every non-power-of-2 period.  This script measures q(M) exactly.
"""
import itertools, sys
sys.path.insert(0, '.')
from xring import Ring, RULES12, RULES27

def step_matrix(R, O):
    n, m = R.n, R.m
    cols = []
    for k in range(n):
        for i in range(m):
            X = [0]*n; X[k] = 1 << i
            act = [X[kk] & R.rot(O, -R.rules[kk][0]) &
                   ~R.rot(O, -R.rules[kk][1]) & R.mask for kk in range(n)]
            out = list(X)
            for kk in range(n):
                out[R.targets[kk]] ^= R.rot(act[kk], R.rules[kk][2])
            v = 0
            for kk in range(n):
                v |= out[kk] << (kk*m)
            cols.append(v)
    return tuple(cols)

def compose(A, B):
    out = []
    for col in B:
        v = 0; c = col
        while c:
            b = (c & -c).bit_length() - 1; c &= c - 1; v ^= A[b]
        out.append(v)
    return tuple(out)

def mult_period(M, cap=4096):
    seen = {}; P = M; t = 1
    while t <= cap:
        if P in seen:
            return t - seen[P]
        seen[P] = t
        P = compose(M, P); t += 1
    return None

def survey(tmaps, pool, n, ms, label):
    qs = {}
    for m in ms:
        for rules in itertools.product(pool, repeat=n):
            for tg in tmaps:
                R = Ring(list(rules), list(tg), m)
                for O in range(1 << m):
                    q = mult_period(step_matrix(R, O))
                    if q not in qs:
                        qs[q] = (m, rules, tg, O)
    print("  %-46s q(M) values: %s" % (label, sorted(qs)))
    for q in sorted(qs):
        if q & (q-1):
            m, rules, tg, O = qs[q]
            print("      q=%-3d first at m=%d %s -> %s  O=%s"
                  % (q, m, list(rules), list(tg), format(O, '0%db' % m)))
    return qs

if __name__ == "__main__":
    print("multiplicative period q(M) of the frozen-occupancy step operator")
    survey([[0]], RULES27, 1, range(3, 11), "own-kind, 1 kind, all 27, m=3..10")
    survey([[0,1]], RULES12, 2, range(3, 9), "own-kind, 2 live kinds, m=3..8")
    survey([[1,0]], RULES12, 2, range(3, 9), "2-cycle permutation, m=3..8")
    survey([[0,0]], RULES12, 2, range(3, 9), "non-injective [0,0], m=3..8")
    survey([[0,1,2]], RULES12, 3, range(3, 7), "own-kind, 3 live kinds, m=3..6")
    survey([[1,2,0]], RULES12, 3, range(3, 7), "3-cycle permutation, m=3..6")


def predict(L):
    """Odd part L' of L; F2[y]/(y^L'-1) = prod F_{2^d}, d = ord_{L'/factor}(2).
    Orders of 1+zeta divide 2^d - 1 on each nontrivial factor."""
    Lp = L
    while Lp % 2 == 0:
        Lp //= 2
    return Lp


def survey_L(L, ms, ntrials, seed=7):
    """Random L-cycle constitutions: which q(M) appear?"""
    import random
    rng = random.Random(seed)
    tg = [(k + 1) % L for k in range(L)]
    qs = {}
    for m in ms:
        for _ in range(ntrials):
            rules = [rng.choice(RULES12) for _ in range(L)]
            R = Ring(rules, tg, m)
            for O in range(1 << m):
                q = mult_period(step_matrix(R, O), cap=600)
                if q not in qs:
                    qs[q] = (m, tuple(rules), O)
    odd = sorted(q for q in qs if q and q % 2)
    print("  L=%d (odd part %d)  m in %s, %d random constitutions per m: "
          "q(M) = %s" % (L, predict(L), list(ms), ntrials, sorted(qs)))
    print("        odd q(M) values: %s" % (odd if odd != [1] else "none but 1"))
    for q in sorted(qs):
        if q and q & (q - 1):
            m, rules, O = qs[q]
            print("        q=%-3d first at m=%d %s O=%s"
                  % (q, m, list(rules), format(O, '0%db' % m)))
    return qs
