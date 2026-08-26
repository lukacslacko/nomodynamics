#!/usr/bin/env python3
"""Task 1: fixed-point algebra on nomic rings.

THEORY (proved in RESULTS.md):
  Single-Author Lemma: slot (j,k) can only ever be toggled by the kind-k law
  at j-c(k).  Hence toggle multiplicity <= 1, parity == OR, and
  Dead Letter Theorem: S fixed  <=>  every law in S is blocked.
  Balanced constitutions (active-but-cancelling) DO NOT EXIST.

COUNTING: blockedness of law (i,(a,b,c)) depends only on (a,b) and the
occupancy of i-1,i,i+1.  For occupied i with (L,R) = occupancy of neighbors:
  active guard-pairs = n1*n0, n1 = 1+L+R, n0 = 2-L-R
  -> 0 pairs if L=R=1 (flanked), else 2 pairs -> 6 active kinds.
Allowed masks per occupied cell: any nonempty subset of blocked kinds:
  beta = 2^27-1 if flanked, alpha = 2^21-1 otherwise.
F(m) = sum over occupancy patterns O of prod_{i in O} (alpha or beta)
     = trace(T^m) for m>=3 with 4x4 transfer matrix on neighbor pairs;
m=1,2 handled directly (wrapped neighbors coincide).
Generating function by law count: alpha -> (1+x)^21-1, beta -> (1+x)^27-1.
"""
import sys, time
from itertools import combinations
from math import comb, log2
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/rings")
from ring import TYPES, TIDX, ACT3, step, from_laws, state_repr, active_count

ALPHA = (1 << 21) - 1
BETA = (1 << 27) - 1

# ---------------------------------------------------------------- exact counts
def weight(x, y, z, alpha=ALPHA, beta=BETA):
    if y == 0:
        return 1
    return beta if (x == 1 and z == 1) else alpha

def F_exact(m, alpha=ALPHA, beta=BETA):
    """Exact number of fixed points on ring of size m (integer)."""
    if m == 1:
        return 1 + beta                    # empty, or any nonempty mask (flanked by itself)
    if m == 2:
        return 1 + 2 * alpha + beta * beta # empty; one occupied (isolated); both (flanked)
    # transfer matrix on pairs (x_i, x_{i+1})
    idx = [(0, 0), (0, 1), (1, 0), (1, 1)]
    T = [[0] * 4 for _ in range(4)]
    for r, (x, y) in enumerate(idx):
        for s_, (y2, z) in enumerate(idx):
            if y2 == y:
                T[r][s_] = weight(x, y, z, alpha, beta)
    # F = tr(T^m)
    M = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    P = T
    e = m
    while e:
        if e & 1:
            M = matmul(M, P)
        P = matmul(P, P)
        e >>= 1
    return sum(M[i][i] for i in range(4))

def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

# ------------------------------------------------- generating function version
def ptrunc(p, N):
    return p[: N + 1]

def pmul(p, q, N):
    r = [0] * (min(len(p) + len(q) - 1, N + 1))
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                if b and i + j <= N:
                    r[i + j] += a * b
    return r

def padd(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]

def onepx_pow(e, N):
    """(1+x)^e truncated."""
    return [comb(e, i) for i in range(min(e, N) + 1)]

def F_poly(m, N):
    """Law-count generating function of fixed points on ring m, truncated deg N."""
    a = onepx_pow(21, N); a[0] -= 1        # (1+x)^21 - 1
    b = onepx_pow(27, N); b[0] -= 1
    one = [1]
    if m == 1:
        return padd(one, b)
    if m == 2:
        return padd(padd(one, [2 * c for c in a]), pmul(b, b, N))
    idx = [(0, 0), (0, 1), (1, 0), (1, 1)]
    def w(x, y, z):
        if y == 0:
            return one
        return b if (x == 1 and z == 1) else a
    T = [[[0] for _ in range(4)] for _ in range(4)]
    for r, (x, y) in enumerate(idx):
        for s_, (y2, z) in enumerate(idx):
            if y2 == y:
                T[r][s_] = w(x, y, z)
    M = [[([1] if i == j else [0]) for j in range(4)] for i in range(4)]
    P = T
    e = m
    def pmatmul(A, B):
        return [[ptrunc(padd(padd(padd(pmul(A[i][0], B[0][j], N), pmul(A[i][1], B[1][j], N)),
                                  pmul(A[i][2], B[2][j], N)), pmul(A[i][3], B[3][j], N)), N)
                 for j in range(4)] for i in range(4)]
    while e:
        if e & 1:
            M = pmatmul(M, P)
        P = pmatmul(P, P)
        e >>= 1
    tot = [0]
    for i in range(4):
        tot = padd(tot, M[i][i])
    return ptrunc(tot, N)

# ------------------------------------------------------- sparse brute force
AB = [(a, b) for (a, b, c) in TYPES]   # guard pair per kind index

def count_fixed_sparse(m, nmax):
    """Enumerate ALL codes with 1..nmax laws on ring m; count fixed by n.
    A code is fixed iff no law is active (Dead Letter theorem, engine-verified)."""
    nslots = 27 * m
    pos = [s // 27 for s in range(nslots)]
    ab = [AB[s % 27] for s in range(nslots)]
    counts = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        c = 0
        for combo in combinations(range(nslots), n):
            occ = 0
            for s_ in combo:
                occ |= 1 << pos[s_]
            ok = True
            for s_ in combo:
                i = pos[s_]
                a, b = ab[s_]
                if (occ >> ((i + a) % m)) & 1 and not (occ >> ((i + b) % m)) & 1:
                    ok = False
                    break
            if ok:
                c += 1
        counts[n] = c
    return counts

# ---------------------------------------------------------------- char poly
def charpoly_T():
    """det(lambda I - T) for the numeric transfer matrix, exact integer coeffs.
    Returns list c[0..4], c[4]=1: sum c_i lambda^i."""
    # symbolic in lambda: entries are linear polys [const, lam]
    idx = [(0, 0), (0, 1), (1, 0), (1, 1)]
    M = [[[0, 0] for _ in range(4)] for _ in range(4)]
    for r, (x, y) in enumerate(idx):
        for s_, (y2, z) in enumerate(idx):
            w = weight(x, y, z) if y2 == y else 0
            M[r][s_] = [-w, 1 if r == s_ else 0]
    def pdet(rows, cols):
        if len(rows) == 1:
            return M[rows[0]][cols[0]]
        tot = [0]
        r = rows[0]
        for j, cc in enumerate(cols):
            minor = pdet(rows[1:], cols[:j] + cols[j + 1:])
            term = pmul(M[r][cc], minor, 8)
            if j % 2:
                term = [-t for t in term]
            tot = padd(tot, term)
        return tot
    return pdet([0, 1, 2, 3], [0, 1, 2, 3])

if __name__ == "__main__":
    t0 = time.time()
    print("== EXACT FIXED-POINT COUNTS F(m) (parity == OR semantics) ==")
    print(f"alpha=2^21-1 (cell with an empty neighbor), beta=2^27-1 (flanked cell)")
    for m in list(range(1, 13)) + [16, 24]:
        F = F_exact(m)
        tot = 1 << (27 * m)
        full = BETA ** m           # fully-occupied gridlock states (all fixed)
        porous = F - full
        nonfixed = tot - F
        print(f" m={m:2d}  F={F}")
        print(f"        log2 F = {log2(F):.6f}   (state space 2^{27*m})"
              f"   non-fixed fraction = {nonfixed/tot:.3e}")
        print(f"        full-occupancy fixed = beta^m ({full})   porous fixed = {porous}"
              f"   porous share = {porous/F:.3e}")
    print()
    print("== char poly of transfer matrix ==")
    cp = charpoly_T()
    print(" det(lI-T) coeffs (const..l^4):", cp)
    # growth rate
    F23, F24 = F_exact(23), F_exact(24)
    print(f" dominant eigenvalue ~ F(24)/F(23) = {F24/F23:.6f} = 2^{log2(F24/F23):.9f}")
    print(f" (beta = {BETA} = 2^{log2(BETA):.9f})")
    print()

    N = 6
    print(f"== LAW-COUNT GENERATING FUNCTION [x^n] F(m,x), n<=6 ==")
    print(" (number of stable constitutions with exactly n laws)")
    gf = {}
    for m in range(1, 13):
        gf[m] = F_poly(m, N)
        print(f" m={m:2d}: " + "  ".join(f"n={n}:{gf[m][n] if n < len(gf[m]) else 0}" for n in range(0, N + 1)))
    print()

    print("== SPARSE BRUTE-FORCE CROSS-CHECK (all codes with <=nmax laws) ==")
    plan = [(2, 4), (3, 4), (4, 4), (5, 3), (6, 3)]
    for m, nmax in plan:
        t1 = time.time()
        bc = count_fixed_sparse(m, nmax)
        ok = all(bc[n] == (gf[m][n] if n < len(gf[m]) else 0) for n in range(1, nmax + 1))
        tag = "MATCH" if ok else "MISMATCH!!!"
        print(f" m={m} n<=%d: brute {bc[1:]} vs GF {[gf[m][n] for n in range(1, nmax+1)]}  {tag}"
              % nmax + f"   ({time.time()-t1:.1f}s)")
    print()

    # step-verify every sparse fixed point found for m=3, n<=2 (belt and braces)
    print("== step()-verification of blocked-criterion on m=3, n<=2 ==")
    nslots = 81
    cnt = fx = 0
    for n in (1, 2):
        for combo in combinations(range(nslots), n):
            laws = [(s // 27, TYPES[s % 27]) for s in combo]
            S = from_laws(3, laws)
            isfix = step(S) == S
            occ = sum(1 << i for i, v in enumerate(S) if v)
            blocked = all(not ((occ >> ((i + a) % 3)) & 1 and not (occ >> ((i + b) % 3)) & 1)
                          for i, (a, b, c) in laws)
            assert isfix == blocked
            cnt += 1
            fx += isfix
            if isfix:
                assert active_count(S) == 0   # NO balanced constitutions
    print(f"  {cnt} codes checked, {fx} fixed, all fixed had 0 active laws (no balanced). OK")
    print()

    print("== MINIMAL SPECIMENS ==")
    # dead-letter kinds: never active under any local occupancy WITH the law's
    # own cell occupied (loc has C-bit set -- the only realizable patterns)
    dead = [t for k, t in enumerate(TYPES) if all(not (ACT3[loc] >> k) & 1 for loc in (2, 3, 6, 7))]
    print(f" unconditional dead-letter kinds (never active anywhere): {len(dead)}")
    print("   = kinds with b=0 (self-slot occupied: vacancy-guard always fails)"
          " or a=b (guard self-contradictory):")
    print("   " + " ".join(str(t) for t in dead))
    live = [t for t in TYPES if t not in dead]
    print(f" live kinds: {len(live)}: {live}")
    # single-law fixed points on m>=2
    single_fixed = []
    for t in TYPES:
        S = from_laws(4, [(0, t)])
        if step(S) == S:
            single_fixed.append(t)
    print(f" single isolated law: fixed for {len(single_fixed)}/27 kinds"
          f" (active: {[t for t in TYPES if t not in single_fixed]})")
    # the mutual-veto pair (taut 2-law constitution)
    print("\n THE MUTUAL-VETO CONSTITUTION (smallest taut stable code):")
    S = from_laws(4, [(0, (0, 1, 1)), (1, (0, -1, -1))])
    print(f"   laws: (0,1,1)@0  (0,-1,-1)@1  on m=4;  fixed: {step(S)==S}")
    for dropi in (0, 1):
        laws = state_repr(S)
        S2 = from_laws(4, [laws[1 - dropi]])
        print(f"   drop law @{dropi}: remaining {state_repr(S2)} fixed: {step(S2)==S2}"
              f" (active={active_count(S2)})")
    # census of taut 2-law fixed points on m=4
    taut = 0; tot2 = 0; taut_ex = []
    for combo in combinations(range(27 * 4), 2):
        laws = [(s // 27, TYPES[s % 27]) for s in combo]
        S = from_laws(4, laws)
        if step(S) != S:
            continue
        tot2 += 1
        t_ok = all(step(from_laws(4, [laws[j]])) != from_laws(4, [laws[j]]) for j in (0, 1))
        if t_ok:
            taut += 1
            if len(taut_ex) < 6:
                taut_ex.append(laws)
    print(f"\n 2-law fixed points on m=4: {tot2}; taut (every deletion destabilizes): {taut}")
    for ex in taut_ex:
        print(f"   taut example: {ex}")
    print(f"\ntotal {time.time()-t0:.1f}s")
