#!/usr/bin/env python3
"""Task 4: reversibility and Gardens of Eden — EXACT predecessor algebra.

Fix the predecessor's occupancy pattern O (2^m guesses).  Then the step map is
linear per kind over F2:  Phi_O(x) = x XOR D x,  where for kind k=(a,b,c),
(D x)_{i+c} = x_i [i in A_k(O)],  A_k(O) = {i : i+a in O, i+b not in O}.
  * c=+-1 kinds: A_k is never the full ring => D nilpotent => I+D unipotent
    => UNIQUE candidate x_k = sum_j D^j y_k.
  * c=0 kinds: (I+D)x = x off A, 0 on A => solvable iff y_k|A = 0, and then
    x_k is free on A (self-repealing 'ghost' laws).
Candidate must then satisfy occ(x) = O exactly:
  #pred(y) = sum_O  prod_{i in O}(2^{f_i} - [v_i=0]) * prod_{i not in O}[v_i=0],
  (free bits at i not in O are forced 0), v_i = determined 27-bit part at i,
  f_i = number of c=0 kinds with i in A_k.
So: in-degree <= sum_O 2^{#free}; all irreversibility comes from c=0
self-toggles and occupancy collisions.  The map is INJECTIVE modulo ghosts
within each occupancy class.
"""
import sys, random, time, json
from itertools import combinations
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/rings")
from ring import TYPES, TIDX, step, from_laws, state_repr, random_state, ACT3

ALLK = list(range(27))

def indeg_exact(y, m, kinds=None, want_example=False):
    """Exact number of predecessors of state y (tuple of m masks) within the
    universe restricted to kind-index list `kinds` (default: all 27).
    Returns (count, example_predecessor_or_None)."""
    if kinds is None:
        kinds = ALLK
    full = (1 << m) - 1
    def rr(v, s):
        s %= m
        return ((v >> s) | (v << (m - s))) & full if s else v
    def rl(v, s):
        s %= m
        return ((v << s) | (v >> (m - s))) & full if s else v
    # per-kind y as m-bit ints
    yk = {}
    for k in kinds:
        v = 0
        for i in range(m):
            if (y[i] >> k) & 1:
                v |= 1 << i
        yk[k] = v
    total = 0
    example = None
    for O in range(1 << m):
        v = [0] * m            # determined 27-bit part per position
        fbits = []             # (kind, m-bit free mask) for c=0 kinds
        ok = True
        for k in kinds:
            a, b, c = TYPES[k]
            A = rr(O, a) & (~rr(O, b)) & full
            if c == 0:
                if yk[k] & A:
                    ok = False
                    break
                if A:
                    fbits.append((k, A))
                x = yk[k] & ~A
            else:
                x = yk[k]
                for _ in range(m + 1):
                    x = yk[k] ^ rl(x & A, c)
                # verify (I+D)x = y
                assert (x ^ rl(x & A, c)) == yk[k]
            for i in range(m):
                if (x >> i) & 1:
                    v[i] |= 1 << k
        if not ok:
            continue
        cnt = 1
        f = [0] * m
        for k, A in fbits:
            for i in range(m):
                if (A >> i) & 1:
                    f[i] += 1
        for i in range(m):
            if (O >> i) & 1:
                cnt *= (1 << f[i]) - (1 if v[i] == 0 else 0)
                if cnt == 0:
                    break
            else:
                if v[i] != 0:
                    cnt = 0
                    break
        total += cnt
        if cnt and example is None and want_example:
            ex = list(v)
            for i in range(m):
                if (O >> i) & 1 and v[i] == 0:
                    # need at least one free bit set at i
                    for k, A in fbits:
                        if (A >> i) & 1:
                            ex[i] |= 1 << k
                            break
            example = tuple(ex)
    return total, example

# ------------------------------------------------------------------ validation
def validate(seedv=11):
    rng = random.Random(seedv)
    print("validation 1: forward consistency (full universe)")
    for m in (2, 3, 4, 6):
        for _ in range(200):
            x = random_state(m, rng.choice([0.2, 0.7, 2, 8]), rng)
            y = step(x)
            n, ex = indeg_exact(y, m, want_example=True)
            assert n >= 1, (m, x, y)
            if ex is not None:
                assert step(ex) == y
    print("  OK: every step(x) has >=1 predecessor; examples verified by step()")
    print("validation 2: EXACT cross-check vs brute-forced closed subuniverse")
    for m in (3, 4):
        for kinds in ([TIDX[(0, 1, 1)], TIDX[(0, -1, 0)]],
                      [TIDX[(0, -1, 1)], TIDX[(1, -1, 0)]],
                      [TIDX[(0, 1, 0)], TIDX[(-1, 1, 1)], TIDX[(0, -1, -1)]]):
            K = len(kinds)
            nst = 1 << (K * m)
            from collections import Counter
            indeg = Counter()
            enc = {}
            for xi in range(nst):
                s = []
                for i in range(m):
                    bits = (xi >> (K * i)) & ((1 << K) - 1)
                    vv = 0
                    for j in range(K):
                        if (bits >> j) & 1:
                            vv |= 1 << kinds[j]
                    s.append(vv)
                s = tuple(s)
                indeg[step(s)] += 1
                enc[xi] = s
            mism = 0
            for xi in range(nst):
                y = enc[xi]
                n, _ = indeg_exact(y, m, kinds=kinds)
                if n != indeg.get(y, 0):
                    mism += 1
            assert mism == 0, (m, kinds)
        print(f"  OK m={m}: solver == full functional-graph in-degree for every state")

# ------------------------------------------------------------------ surveys
def survey():
    out = {}
    print("\n== in-degree of the EMPTY BOOK (one-step extinctions + itself) ==")
    for m in range(2, 11):
        y = tuple([0] * m)
        n, _ = indeg_exact(y, m)
        # closed form: sum over O with no flanked cell of 3^|O|  (+O=0 term)
        full = (1 << m) - 1
        tot = 0
        for O in range(1 << m):
            okO = True
            pc = 0
            for i in range(m):
                if (O >> i) & 1:
                    pc += 1
                    if (O >> ((i - 1) % m)) & 1 and (O >> ((i + 1) % m)) & 1:
                        okO = False
                        break
            if okO:
                tot += 3 ** pc
        print(f" m={m}: indeg(empty) = {n}  closed-form sum 3^|O| (no flanked cell): {tot}  match={n==tot}")
        out[f"indeg_empty_m{m}"] = n

    print("\n== GoE census among ALL sparse codes (exact, full 27-kind universe) ==")
    for m, nmax in ((3, 2), (4, 2), (5, 2), (6, 2)):
        t0 = time.time()
        res = {}
        for nl in range(1, nmax + 1):
            goe = tot = 0
            mx = 0
            for combo in combinations(range(27 * m), nl):
                y = from_laws(m, [(s // 27, TYPES[s % 27]) for s in combo])
                n, _ = indeg_exact(y, m)
                tot += 1
                mx = max(mx, n)
                if n == 0:
                    goe += 1
            res[nl] = (goe, tot, mx)
            print(f" m={m} n={nl}: GoE {goe}/{tot} = {goe/tot:.4f}   max indeg {mx}"
                  f"   ({time.time()-t0:.0f}s)")
        out[f"sparse_goe_m{m}"] = res

    print("\n== single-law GoE anatomy (m=5): which lone statutes are un-enactable? ==")
    goek, havek = [], []
    for k, t in enumerate(TYPES):
        y = from_laws(5, [(0, t)])
        n, _ = indeg_exact(y, 5)
        (goek if n == 0 else havek).append((t, n))
    print(f"  GoE single laws ({len(goek)}): {[t for t,_ in goek]}")
    print(f"  enactable single laws ({len(havek)}): {[(t,n) for t,n in havek]}")
    out["single_law_goe_m5"] = [t for t, _ in goek]

    print("\n== GoE fraction vs seed density (sampled, exact per state) ==")
    rng = random.Random(5)
    for m in (4, 6, 8):
        row = {}
        for lam in (0.1, 0.3, 0.5, 1.0, 2.0, 4.0):
            NS = 400 if m <= 6 else 250
            goe = 0
            indegs = []
            for _ in range(NS):
                y = random_state(m, lam, rng)
                n, _ = indeg_exact(y, m)
                indegs.append(n)
                if n == 0:
                    goe += 1
            row[lam] = (goe / NS, max(indegs))
            print(f" m={m} lam={lam:<4}: GoE fraction {goe/NS:.3f}   max indeg {max(indegs)}", flush=True)
        out[f"goe_vs_lam_m{m}"] = row

    print("\n== uniform-measure GoE: theory ==")
    print(" GoE states are non-fixed (fixed points are their own predecessor);")
    print(" non-fixed fraction = 1 - F(m)/2^(27m) ~= m * 2^-27  (Task 1, exact).")
    print(" So under the uniform measure the reachable set has full measure:")
    print(" GoE fraction <= m * 7.45e-9.  Irreversibility is a SPARSE-sector affair.")
    with open("/Users/lukacs/claude/math/program/phase6/rings/eden.json", "w") as f:
        json.dump({str(k): str(v) for k, v in out.items()}, f, indent=1)

if __name__ == "__main__":
    T0 = time.time()
    validate()
    survey()
    print(f"\ntotal {time.time()-T0:.0f}s")
