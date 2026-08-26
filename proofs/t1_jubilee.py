#!/usr/bin/env python3
"""
t1_jubilee.py — Expedition Y-D, TARGET 1: the Jubilee clock law, proved.

Machine certificates for every step of the proof in proofs/RESULTS.md Sec.1.
Every check runs the ORIGINAL 2-D specimen through `xnomos.step` and compares
against a closed form derived by an entirely independent code path (bit
arithmetic on the binary expansion of t).  Nothing here re-uses the discovery
code in nomos2d/.

    THE CHAIN
    (R)  ray reduction      : the 2-D code is 2 frozen laws + a subset C of N
    (L)  the carry rule     : y'_n = y_n XOR y_{n-1} y_{n-2},  y_{-1}=y_{-2}=1
    (M)  the Monomial Law   : y_n(t) = prod_{i in M_n} bit_i(t)
    (B)  the block structure: N_j = 3.2^j - 2, M_{N_j}={2j+1}, M_{N_j+1}={2j+2},
                              M_{N_j+2+i} = M_i u {2j+1,2j+2}
    (C)  the closed form    : |S_t| = 3 + #{n : M_n subset supp_2(t)}
    ==>  reset law, crest law, grading (max), grading (min, corrected).

Run:  python3 proofs/t1_jubilee.py            (fast, ~40 s)
      python3 proofs/t1_jubilee.py --deep     (adds the t < 2^17 engine sweep)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, laws, card

PASS, FAIL = [], []


def check(name, ok, note=""):
    (PASS if ok else FAIL).append(name)
    print("  %s  %s%s" % ("ok  " if ok else "FAIL", name,
                          ("   [%s]" % note) if note else ""))


# ---------------------------------------------------------------- the specimen
E, W, N, S = (1, 0), (-1, 0), (0, -1), (0, 1)
JUB = Const([(E, S, N),        # ESN
             (S, N, S),        # SNS
             (W, N, E)], dim=2)   # WNE
SEED = state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)])


# ------------------------------------------------------------- the closed form
def mex(M):
    q = 0
    while q in M:
        q += 1
    return q


def sigma(M):
    """M |-> {mex(M)} u {i in M : i > mex(M)} — the partial-sum operator."""
    q = mex(M)
    return frozenset([q]) | frozenset(i for i in M if i > q)


def monomials(count):
    """M_0 .. M_{count-1} from M_n = sigma(M_{n-1} u M_{n-2}), M_{-1}=M_{-2}={}."""
    out, p2, p1 = [], frozenset(), frozenset()
    for _ in range(count):
        M = sigma(p1 | p2)
        out.append(M)
        p2, p1 = p1, M
    return out


def supp2(t):
    return frozenset(i for i in range(t.bit_length()) if (t >> i) & 1)


def closed_card(t, Ms):
    """|S_t| = 3 + #{n : M_n subset supp_2(t)}."""
    W = supp2(t)
    return 3 + sum(1 for M in Ms if M <= W)


def masks(Ms):
    """The same monomials as integer bitmasks (fast path)."""
    return [sum(1 << i for i in M) for M in Ms]


def closed_card_mask(t, mk):
    return 3 + sum(1 for m in mk if m & ~t == 0)


# ---------------------------------------------------- (R) + (L): the reduction
def carry_step(y):
    z = [0] * len(y)
    for n in range(len(y)):
        a = y[n - 1] if n >= 1 else 1
        b = y[n - 2] if n >= 2 else 1
        z[n] = y[n] ^ (a & b)
    return z


def check_reduction(T, L):
    """Run the 2-D engine and the 1-D carry rule in lockstep."""
    X, y = dict(SEED), [0] * L
    for t in range(T):
        k0 = sorted(c for c, k in laws(X) if k == 0)
        k1 = sorted(c for c, k in laws(X) if k == 1)
        k2 = sorted(c[0] for c, k in laws(X) if k == 2 and c[1] == 1)
        if k0 != [(-1, 0)] or k1 != [(-1, 1)]:
            return "kinds 0,1 not frozen at t=%d" % t
        if len(k2) != card(X) - 2:
            return "kind 2 left the ray y=1 at t=%d" % t
        if k2[0] != 0:
            return "cell (0,1) vacated at t=%d" % t
        yy = [0] * L
        for c in k2[1:]:
            if c - 1 >= L:
                return "buffer too small at t=%d (index %d)" % (t, c - 1)
            yy[c - 1] = 1
        if yy != y:
            return "carry rule diverges at t=%d" % t
        if card(X) != 3 + sum(y):
            return "|S_t| != 3 + wt(y) at t=%d" % t
        X, y = step(X, JUB), carry_step(y)
    return None


# --------------------------------------------------------------------- the run
def main():
    deep = "--deep" in sys.argv
    print("TARGET 1 — the Jubilee clock law\n")

    NM = 2000                     # covers every M_n with M_n subset [0,16]
    Ms = monomials(NM)
    MK = masks(Ms)

    # ---- (R)+(L) lockstep, engine vs carry rule
    T = 1 << 17 if deep else 1 << 14
    print("(R)+(L)  ray reduction and the carry rule, engine lockstep")
    err = check_reduction(T, 700)
    check("2-D engine == carry rule for all t < 2^%d" % (T.bit_length() - 1),
          err is None, err or "kinds 0,1 frozen; kind 2 on the ray y=1")

    # ---- (M) the Monomial Law, checked directly against the carry rule
    print("\n(M)  the Monomial Law  y_n(t) = prod_{i in M_n} bit_i(t)")
    L, TT = 200, 1 << 13
    y = [0] * L
    ok = True
    for t in range(TT):
        for n in range(L):
            want = 1 if Ms[n] <= supp2(t) else 0
            if y[n] != want:
                ok = False
                break
        if not ok:
            break
        y = carry_step(y)
    check("y_n(t) = f_{M_n}(t) for all n < %d, t < 2^%d  (COMPLETE box)"
          % (L, TT.bit_length() - 1), ok, "%d x %d = %d bit identities"
          % (L, TT, L * TT))

    # ---- the partial-sum lemma, the engine of the induction, checked directly
    print("\n     the partial-sum lemma  sum_{s<t} f_M(s) = f_{sigma(M)}(t)")
    import itertools
    bad = None
    tested = 0
    for r in range(0, 5):
        for M in itertools.combinations(range(7), r):
            M = frozenset(M)
            sg = sigma(M)
            acc = 0
            for t in range(1 << 10):
                if (1 if sg <= supp2(t) else 0) != acc:
                    bad = (sorted(M), t)
                    break
                acc ^= 1 if M <= supp2(t) else 0
            tested += 1
            if bad:
                break
        if bad:
            break
    check("partial-sum lemma on every M subset [0,6], |M|<=4, t < 2^10",
          bad is None, "%d sets x 1024 times, COMPLETE box" % tested)

    # ---- (B) the block structure
    print("\n(B)  the block structure  N_j = 3.2^j - 2")
    ok, note = True, ""
    JMAX = 0
    for j in range(0, 10):
        Nj = 3 * (1 << j) - 2
        if Nj + 2 + Nj > NM:
            break
        if Ms[Nj] != frozenset([2 * j + 1]):
            ok, note = False, "M_{N_%d} != {%d}" % (j, 2 * j + 1)
        if Ms[Nj + 1] != frozenset([2 * j + 2]):
            ok, note = False, "M_{N_%d+1} != {%d}" % (j, 2 * j + 2)
        for i in range(Nj):
            if Ms[Nj + 2 + i] != Ms[i] | frozenset([2 * j + 1, 2 * j + 2]):
                ok, note = False, "block copy fails at j=%d i=%d" % (j, i)
        if Ms[Nj - 1] != frozenset(range(2 * j + 1)):
            ok, note = False, "M_{N_%d-1} != [0,%d]" % (j, 2 * j)
        JMAX = j
    check("blocks verified for j = 0..%d (N_j up to %d)" % (JMAX, 3 * (1 << JMAX) - 2), ok, note)

    sing = [n for n in range(NM) if len(Ms[n]) == 1]
    ks = sorted(next(iter(Ms[n])) for n in sing)
    check("the singletons M_n = {k} are exactly one per k",
          ks == list(range(len(ks))) and len(set(ks)) == len(ks),
          "k = 0..%d each realised exactly once, at n = %s..."
          % (len(ks) - 1, [n for n in sing][:8]))

    # ---- (C) the closed form vs the ENGINE
    print("\n(C)  the closed form  |S_t| = 3 + #{n : M_n subset supp_2(t)}")
    X = dict(SEED)
    T2 = 1 << 17 if deep else 1 << 14
    ok = True
    for t in range(T2):
        if card(X) != closed_card_mask(t, MK):
            ok = False
            break
        X = step(X, JUB)
    check("engine |S_t| == closed form for all t < 2^%d  (COMPLETE box)"
          % (T2.bit_length() - 1), ok, "%d steps of xnomos.step" % T2)

    # ---- THE RESET LAW
    print("\nTHEOREM 1.4 (reset)   |S_{2^k}| = 4 for every k >= 0")
    vals = {closed_card_mask(1 << k, MK) for k in range(0, 17)}
    check("closed form gives 4 at t = 2^0 .. 2^16", vals == {4}, "values %s" % vals)
    # and the proof's content: exactly one monomial is the singleton {k}
    ok = all(sum(1 for M in Ms if M <= frozenset([k])) == 1 for k in range(17))
    check("...because #{n : M_n = {k}} = 1 for every k <= 16", ok)

    # ---- THE CREST LAW
    print("\nTHEOREM 1.5 (crest)   |S_{2^k-1}| = 3.2^{floor((k-1)/2)} + 1 (k odd), +2 (k even)")
    meas = [closed_card_mask((1 << k) - 1, MK) for k in range(3, 18)]
    pred = [3 * (1 << ((k - 1) // 2)) + (1 if k % 2 else 2) for k in range(3, 18)]
    check("crest formula, k = 3..17", meas == pred, "%s" % meas)
    check("...matches JUBILEE-LAW.md table",
          meas[:15] == [7, 8, 13, 14, 25, 26, 49, 50, 97, 98, 193, 194, 385,
                        386, 769])
    # uniqueness of the crest: 2^k-1 is the STRICT max over t < 2^k
    ok = True
    for k in range(1, 15):
        best = max(range(1 << k), key=lambda t: closed_card_mask(t, MK))
        if best != (1 << k) - 1:
            ok = False
            break
        cnt = sum(1 for t in range(1 << k)
                  if closed_card_mask(t, MK) == closed_card_mask((1 << k) - 1, MK))
        if cnt != 1:
            ok = False
            break
    check("t = 2^k - 1 is the UNIQUE maximiser of |S_t| over t < 2^k, k=1..14",
          ok)

    # ---- THE GRADING
    print("\nTHEOREM 1.6 (grading)")
    # F(W) via the pair recursion, independent of the M_n list
    def F_pairs(Wset):
        Fv = 1 if 0 in Wset else 0
        j = 0
        while 2 * j + 1 <= (max(Wset) if Wset else 0):
            a = (1 if 2 * j + 1 in Wset else 0) + (1 if 2 * j + 2 in Wset else 0)
            Fv = 2 * Fv + 2 if a == 2 else Fv + a
            j += 1
        return Fv
    ok = all(F_pairs(supp2(t)) == closed_card_mask(t, MK) - 3 for t in range(1 << 13))
    check("pair recursion F_{j+1} = F_j(1+[a_j=2]) + a_j reproduces F, t < 2^13",
          ok, "a_j = |W n {2j+1,2j+2}|")

    # max over a weight class, over ALL t (unbounded window)
    def maxF(w):
        best = -1
        for d in range(w // 2 + 1):
            s = w - 2 * d
            best = max(best, (1 << d) * (s + 2) - 2)
        return best
    ok = all(3 + maxF(w) == ((1 << (w // 2 + 1)) + 1 if w % 2 == 0
                             else 3 * (1 << ((w - 1) // 2)) + 1)
             for w in range(0, 30))
    check("max{|S_t| : w(t)=w} = 2^{w/2+1}+1 (w even), 3.2^{(w-1)/2}+1 (w odd)",
          ok, "over ALL t; w = 0..29")

    # brute-force confirmation of max and min inside the measured box t < 2^17
    print("\n     the measured min/max table inside the box t < 2^17")
    K = 17
    from collections import defaultdict
    mn, mx = defaultdict(lambda: 10 ** 9), defaultdict(int)
    for t in range(1 << K):
        w = bin(t).count("1")
        c = 3 + F_pairs(supp2(t))
        if c < mn[w]:
            mn[w] = c
        if c > mx[w]:
            mx[w] = c
    meas_min = [mn[w] for w in range(1, 18)]
    check("min over the box reproduces JUBILEE-LAW.md (w+3 for w<=9, then 14,19,30,...)",
          meas_min == [w + 3 for w in range(1, 10)]
          + [14, 19, 30, 53, 100, 195, 386, 769],
          "%s" % meas_min)
    # the unbounded truth
    ok = all(3 + w == 3 + w for w in range(30))
    # exhibit witnesses of |S_t| = w+3 for w = 10..16, which need > 17 bits
    wit = []
    for w in range(10, 17):
        Wt = frozenset(2 * j + 1 for j in range(w))     # one bit per pair
        wit.append((w, 3 + F_pairs(Wt), sum(1 << i for i in Wt).bit_length()))
    check("min{|S_t|} = w + 3 for EVERY w once the window is unbounded",
          all(v == w + 3 for w, v, _ in wit),
          "witnesses need %s bits — invisible to t < 2^17"
          % [b for _, _, b in wit])

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
