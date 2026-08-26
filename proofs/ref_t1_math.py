#!/usr/bin/env python3
"""ref_t1_math.py -- REFEREE: Thm 1.7, Cor 1.8, Cor 1.9, Thm 1.10-1.12, 1.14.

Independent code path: my own sigma recursion (sets) AND my own integer
OR-Fibonacci, cross-checked against each other; my own DP for the extremal
statistics; my own brute force over orderings for the max/min optimisation.
"""
import itertools
from collections import defaultdict

NM = 60000


def mex(M):
    q = 0
    while q in M:
        q += 1
    return q


def sigma(M):
    q = mex(M)
    return frozenset([q]) | frozenset(i for i in M if i > q)


def build_sets(n):
    out, p2, p1 = [], frozenset(), frozenset()
    for _ in range(n):
        M = sigma(p1 | p2)
        out.append(M)
        p2, p1 = p1, M
    return out


def build_ints(n):
    out, p2, p1 = [], 0, 0
    for _ in range(n):
        m = (p1 | p2) + 1
        out.append(m)
        p2, p1 = p1, m
    return out


MU = build_ints(NM)
print("== monomials ==")
SETS = build_sets(20000)
agree = all(sum(1 << i for i in SETS[n]) == MU[n] for n in range(20000))
print("  sigma-recursion (sets) == OR-Fibonacci (ints) for n < 20000:", agree)
print("  mu_0..15 =", MU[:16])
print("  strictly increasing for n < %d: %s"
      % (NM, all(MU[i] < MU[i + 1] for i in range(NM - 1))))
print("  every M_n non-empty (mu_n > 0):", all(m > 0 for m in MU))

# ---------------------------------------------------------------- Theorem 1.7
print("\n== Theorem 1.7 (blocks) ==")
bad = []
jmax = 0
for j in range(0, 20):
    Nj = 3 * (1 << j) - 2
    if 2 * Nj + 2 > NM:
        break
    jmax = j
    if MU[Nj] != 1 << (2 * j + 1):
        bad.append(("(2) M_{N_j} != {2j+1}", j))
    if MU[Nj + 1] != 1 << (2 * j + 2):
        bad.append(("(2) M_{N_j+1} != {2j+2}", j))
    if MU[Nj - 1] != (1 << (2 * j + 1)) - 1:
        bad.append(("(1) M_{N_j-1} != [0,2j]", j))
    for i in range(Nj - 1):
        if MU[i] == (1 << (2 * j + 1)) - 1:
            bad.append(("(1) [0,2j] occurs early", j, i))
    for i in range(Nj):
        if MU[i] >= (1 << (2 * j + 1)):
            bad.append(("(1) M_i not subset [0,2j]", j, i))
        if MU[Nj + 2 + i] != MU[i] | (3 << (2 * j + 1)):
            bad.append(("(3) block copy", j, i))
print("  j = 0..%d  (N_j up to %d, indices to %d):"
      % (jmax, 3 * (1 << jmax) - 2, 2 * (3 * (1 << jmax) - 2) + 1),
      "ALL PASS" if not bad else "FAIL %s" % bad[:5])

# the shift rule and its edge case M = [0,2j]
print("\n== the shift-rule edge case  M = [0,2j] exactly ==")
for j in range(0, 4):
    full = frozenset(range(2 * j + 1))
    Q = frozenset([2 * j + 1, 2 * j + 2])
    lhs, rhs = sigma(full | Q), sigma(full) | Q
    print("  j=%d  M=[0,%d]:  sigma(M u Q_j)=%-14s  sigma(M) u Q_j=%-16s %s"
          % (j, 2 * j, sorted(lhs), sorted(rhs),
             "EQUAL" if lhs == rhs else "DIFFER  <- hypothesis M != [0,2j] is essential"))
# exhaustive: does the shift rule hold for every proper subset?
badshift = []
for j in range(0, 4):
    Q = frozenset([2 * j + 1, 2 * j + 2])
    for r in range(0, 2 * j + 2):
        for Mt in itertools.combinations(range(2 * j + 1), r):
            M = frozenset(Mt)
            if M == frozenset(range(2 * j + 1)):
                continue
            if sigma(M | Q) != sigma(M) | Q:
                badshift.append((j, sorted(M)))
print("  shift rule on EVERY proper subset M of [0,2j], j=0..3:",
      "ALL PASS" if not badshift else "FAIL %s" % badshift[:5])
# the j=0, i=1 line of the written proof:  M_{N_j+3} = M_1 u Q_j
print("  the written line  M_{N_j+3} = M_1 u Q_j  at j=0:  M_4 = %s, "
      "M_1 u Q_0 = %s  -> %s"
      % (sorted(SETS[4]), sorted(SETS[1] | frozenset([1, 2])),
         "OK" if SETS[4] == SETS[1] | frozenset([1, 2])
         else "FALSE (vacuous: (3) has range i < N_0 = 1, so i=1 is out of range)"))

# ---------------------------------------------------------------- Cor 1.8/1.9
print("\n== Corollary 1.8 (singletons) ==")
sing = [n for n in range(NM) if MU[n] & (MU[n] - 1) == 0]
ks = [MU[n].bit_length() - 1 for n in sing]
pred = [0] + [x for j in range(0, 30) for x in (3 * (1 << j) - 2, 3 * (1 << j) - 1)
              if x < NM]
pred = sorted(set(pred))
print("  #singletons among n < %d: %d ; exponents = 0..%d each exactly once: %s"
      % (NM, len(sing), len(ks) - 1, ks == list(range(len(ks)))))
print("  singleton indices == {0} u {N_j, N_j+1}: %s"
      % (sing == [n for n in pred if n < NM][:len(sing)]))
print("  first 12 singleton indices:", sing[:12])

print("\n== Corollary 1.9 (initial segments) ==")


def A(K):
    if K < 0:
        return 0
    lim = 1 << (K + 1)
    return sum(1 for m in MU if m < lim)


okA = True
for K in range(-1, 30):
    if K >= 0:
        idx = [n for n in range(NM) if MU[n] < (1 << (K + 1))]
        if idx != list(range(len(idx))):
            okA = False
    if K < 0:
        want = 0
    elif K % 2 == 0:
        want = 3 * (1 << (K // 2)) - 2
    else:
        want = 3 * (1 << ((K - 1) // 2)) - 1
    if A(K) != want:
        okA = False
        print("  A(%d) = %d, want %d" % (K, A(K), want))
print("  {n : M_n subset [0,K]} is an initial segment and A(K) matches the "
      "formula for K = -1..29:", okA)

# ------------------------------------------------------------ the three laws
print("\n== Theorem 1.10 (reset) / 1.11 (crest), closed form ==")


def cardt(t):
    lim = 1 << (t.bit_length() or 1)
    return 3 + sum(1 for m in MU if m < lim and m & ~t == 0)


resets = [cardt(1 << k) for k in range(0, 30)]
print("  |S_{2^k}| for k = 0..29:", set(resets), "->",
      "4 EVERYWHERE" if set(resets) == {4} else "FAIL")
crest = [cardt((1 << k) - 1) for k in range(1, 27)]
predc = [3 + A(k - 1) for k in range(1, 27)]
formula = [3 * (1 << ((k - 1) // 2)) + (1 if k % 2 else 2) for k in range(1, 27)]
print("  |S_{2^k-1}| k=1..26:", crest[:16], "...")
print("  == 3 + A(k-1):", crest == predc, "  == closed formula:", crest == formula)
print("  JUBILEE-LAW.md table k=3..17:", crest[2:17],
      crest[2:17] == [7, 8, 13, 14, 25, 26, 49, 50, 97, 98, 193, 194, 385, 386, 769])

# ---------------------------------------------------------------- the grading
print("\n== Theorem 1.12 (grading) ==")


def Fpair(t):
    F = t & 1
    j = 0
    while (t >> (2 * j + 1)):
        a = ((t >> (2 * j + 1)) & 1) + ((t >> (2 * j + 2)) & 1)
        F = 2 * F + 2 if a == 2 else F + a
        j += 1
    return F


okF = all(Fpair(t) == cardt(t) - 3 for t in range(1 << 14))
print("  pair recursion == closed form (M_n count) for every t < 2^14:", okF)

# uniqueness of the crest maximiser (via the verified pair recursion)
uniq = True
for k in range(1, 21):
    vals = [Fpair(t) for t in range(1 << k)]
    mx = max(vals)
    if vals.index(mx) != (1 << k) - 1 or vals.count(mx) != 1:
        uniq = False
        print("   k=%d: max at %d, count %d" % (k, vals.index(mx), vals.count(mx)))
print("  t = 2^k-1 the UNIQUE maximiser of |S_t| over t < 2^k, k = 1..20:", uniq)

# exact min/max per weight class inside a B-bit window, by DP over pairs
def extremes(B):
    """bit positions 0..B-1 = {0} u P_0..P_{J-1} truncated at B."""
    # states: dict weight -> (minF, maxF)
    st = {0: (0, 0), 1: (1, 1)} if B >= 1 else {0: (0, 0)}
    j = 0
    while 2 * j + 1 <= B - 1:
        hi = 2 * j + 2 <= B - 1
        new = defaultdict(lambda: (10 ** 18, -1))
        for w, (mn, mx) in st.items():
            opts = [(0, lambda F: F), (1, lambda F: F + 1)]
            if hi:
                opts.append((2, lambda F: 2 * F + 2))
            for dw, g in opts:
                a, b = new[w + dw]
                new[w + dw] = (min(a, g(mn)), max(b, g(mx)))
        st = dict(new)
        j += 1
    return st


for B in (17, 41):
    st = extremes(B)
    mns = [st[w][0] + 3 for w in sorted(st) if w >= 1]
    mxs = [st[w][1] + 3 for w in sorted(st) if w >= 1]
    print("\n  window of %d bits (t < 2^%d):" % (B, B))
    print("    min per weight w=1..%d: %s" % (len(mns), mns[:20]))
    print("    max per weight w=1..%d: %s" % (len(mxs), mxs[:14]))
    if B == 17:
        pubmin = [w + 3 for w in range(1, 10)] + [14, 19, 30, 53, 100, 195, 386, 769]
        print("    == JUBILEE-LAW.md published min row:", mns == pubmin)
    else:
        print("    min == w+3 for every w:",
              mns == [w + 3 for w in range(1, len(mns) + 1)])
        fm = [(1 << (w // 2 + 1)) + 1 if w % 2 == 0 else 3 * (1 << ((w - 1) // 2)) + 1
              for w in range(1, len(mxs) + 1)]
        print("    max == formula:", mxs == fm)

# brute force cross-check of the DP inside t < 2^18
mn, mx = defaultdict(lambda: 10 ** 9), defaultdict(int)
for t in range(1, 1 << 18):
    w = bin(t).count("1")
    c = Fpair(t) + 3
    if c < mn[w]:
        mn[w] = c
    if c > mx[w]:
        mx[w] = c
st17 = extremes(18)
print("\n  brute force t < 2^18 vs DP(18 bits):",
      all(mn[w] == st17[w][0] + 3 and mx[w] == st17[w][1] + 3
          for w in range(1, 19)))
print("    brute min w=1..18:", [mn[w] for w in range(1, 19)])
print("    brute max w=1..18:", [mx[w] for w in range(1, 19)])

# the max exchange argument, brute-forced over ALL orderings
print("\n== the max/min optimisation, brute force over ALL op orderings ==")
bad = []
for w in range(0, 15):
    best, worst = -1, 10 ** 9
    for d in range(w // 2 + 1):
        s = w - 2 * d
        for eps in (0, 1):
            if eps > s:
                continue
            ss = s - eps
            for pos in itertools.combinations(range(ss + d), d):
                F = eps
                dd = set(pos)
                for i in range(ss + d):
                    F = 2 * F + 2 if i in dd else F + 1
                best = max(best, F)
                worst = min(worst, F)
    fm = (1 << (w // 2 + 1)) - 2 if w % 2 == 0 else 3 * (1 << ((w - 1) // 2)) - 2
    if best != fm or worst != w:
        bad.append((w, best, fm, worst))
print("  w=0..14: max over every ordering == closed formula and min == w:",
      "ALL PASS" if not bad else "FAIL %s" % bad)
print("  (order matters: +1 then double gives 2F+4; double then +1 gives 2F+3)")

# smallest maximiser per weight class
bt = {}
bv = defaultdict(lambda: -1)
for t in range(1, 1 << 20):
    w = bin(t).count("1")
    v = Fpair(t) + 3
    if v > bv[w]:
        bv[w], bt[w] = v, t
print("\n  smallest maximiser over t < 2^20, w=1..12:",
      [(w, bt[w], bt[w] == (1 << w) - 1) for w in range(1, 13)])

# ------------------------------------------------------- Theorem 1.14 general
print("\n== Theorem 1.14 (general lazy counter) ==")


def orfib_I(I, n):
    R = max(I)
    hist = [0] * R
    out = []
    for _ in range(n):
        v = 0
        for i in I:
            v |= hist[-i]
        m = v + 1
        out.append(m)
        hist.append(m)
    return out


bad = []
fams = 0
for R in range(1, 7):
    for r in range(1, R + 1):
        for I in itertools.combinations(range(1, R + 1), r):
            if max(I) != R:
                continue
            mu = orfib_I(I, 4000)
            inc = all(mu[i] < mu[i + 1] for i in range(len(mu) - 1))
            hits = defaultdict(int)
            for m in mu:
                if m & (m - 1) == 0:
                    hits[m.bit_length() - 1] += 1
            KM = mu[-1].bit_length() - 1
            allpw = all(hits.get(k, 0) == 1 for k in range(KM))
            if 1 in I:
                fams += 1
                if not (inc and allpw):
                    bad.append((I, inc, allpw))
            else:
                # what happens without 1 in I?  report, do not fail
                pass
print("  every I subset [1,6] with 1 in I (%d profiles), 4000 terms: "
      "strictly increasing AND each 2^k exactly once: %s"
      % (fams, "ALL PASS" if not bad else "FAIL %s" % bad[:4]))
print("  counter-examples WITHOUT 1 in I (the hypothesis is needed):")
for I in [(2,), (3,), (2, 3)]:
    mu = orfib_I(I, 20)
    hits = defaultdict(int)
    for m in mu:
        if m & (m - 1) == 0:
            hits[m.bit_length() - 1] += 1
    print("    I=%-8s mu = %s ... increasing=%s, 2^k multiplicities=%s"
          % (str(I), mu[:10], all(mu[i] < mu[i + 1] for i in range(19)),
             dict(sorted(hits.items())[:6])))
mu1 = orfib_I((1,), 1 << 13)
ok = all(sum(1 for m in mu1 if m & ~t == 0) == (1 << bin(t).count("1")) - 1
         for t in range(1 << 12))
print("  I={1}: wt(y(t)) == 2^popcount(t) - 1 for t < 2^12:", ok)
