#!/usr/bin/env python3
"""ref_lemma14.py -- REFEREE: the partial-sum lemma, exhaustively.

Claim (Lemma 1.4):  sum_{s<t} f_M(s) = f_{sigma(M)}(t)  (mod 2),
where f_M(t) = [M subset supp_2(t)], sigma(M) = {q} u {i in M : i > q},
q = mex(M).

COMPLETE BOX: every M subset [0,8] (all 512 subsets, |M| unrestricted,
including M = empty and every M with mex(M) = 0) and every t < 2^12.
Also: a second, independent formulation via integer masks, and the
"sigma == binary increment" identity.
"""
import itertools


def mex(M):
    q = 0
    while q in M:
        q += 1
    return q


def sigma(M):
    q = mex(M)
    return frozenset([q]) | frozenset(i for i in M if i > q)


def f(M, t):
    return 1 if all((t >> i) & 1 for i in M) else 0


def main():
    TMAX = 1 << 12
    bad = []
    nsets = 0
    empty_ok = None
    mex0 = 0
    for r in range(0, 10):
        for Mt in itertools.combinations(range(9), r):
            M = frozenset(Mt)
            nsets += 1
            if mex(M) == 0:
                mex0 += 1
            sg = sigma(M)
            acc = 0
            for t in range(TMAX):
                if f(sg, t) != acc:
                    bad.append((sorted(M), t, acc, f(sg, t)))
                    break
                acc ^= f(M, t)
            if M == frozenset() and not bad:
                empty_ok = sorted(sg)
    print("Lemma 1.4 exhaustive: %d subsets of [0,8] x %d times = %d identities"
          % (nsets, TMAX, nsets * TMAX))
    print("  subsets with mex(M)=0 (i.e. 0 not in M): %d" % mex0)
    print("  M = {} : sigma = %s   (sum_{s<t} 1 = t = bit_0(t) mod 2)" % empty_ok)
    print("  RESULT:", "ALL PASS" if not bad else ("FAIL %s" % bad[:5]))

    # sigma is binary increment
    bad2 = []
    for r in range(0, 11):
        for Mt in itertools.combinations(range(10), r):
            M = frozenset(Mt)
            m = sum(1 << i for i in M)
            s = sum(1 << i for i in sigma(M))
            if s != m + 1:
                bad2.append((sorted(M), m, s))
    print("  sigma == binary increment on every subset of [0,9] (1024 sets):",
          "PASS" if not bad2 else "FAIL %s" % bad2[:3])

    # the surviving-term identity, checked term by term for a few M
    print("\n  term-by-term check of the counting argument (M, q=mex, "
          "#{i<q not in M}) for a sample:")
    for Mt in [(), (0,), (1,), (0, 1), (0, 2), (2, 3), (0, 1, 3, 5), (3,)]:
        M = frozenset(Mt)
        q = mex(M)
        print("    M=%-14s mex=%d  sigma=%-14s exponent#{i<q,i notin M}=%d"
              % (sorted(M), q, sorted(sigma(M)),
                 len([i for i in range(q) if i not in M])))
    return 0 if not bad and not bad2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
