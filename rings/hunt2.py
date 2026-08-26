#!/usr/bin/env python3
"""Task 3 deep-dive.
1. THE SUNSET PARLIAMENT: exact max period of the single-kind (0,-1,1)
   universe (state = m-bit occupancy; x' = x XOR rl(x & ~rl(x,1),1))
   for every m up to 24, with argmax states and basin sizes.
2. Complete 2-kind functional graphs at m=8 (all 66 live pairs).
3. Certified champion for the task constraint (m<=8, seed <=6 laws):
   for the best cycles found, search their full basin for min-law states.
"""
import sys, time, json
from itertools import combinations
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/rings")
from ring import TYPES, TIDX, ACT3, step, from_laws, state_repr, render

LIVE = [t for k, t in enumerate(TYPES) if any((ACT3[loc] >> k) & 1 for loc in (2, 3, 6, 7))]

def sunset_maxp(m):
    """Exact functional graph of the (0,-1,1) universe on ring m."""
    full = (1 << m) - 1
    def stp(x):
        rl1 = ((x << 1) | (x >> (m - 1))) & full
        act = x & ~rl1 & full
        return x ^ (((act << 1) | (act >> (m - 1))) & full)
    nst = 1 << m
    succ = [stp(x) for x in range(nst)]
    color = bytearray(nst)
    maxp, arg = 0, 0
    cyc_nodes = 0
    from collections import Counter
    pc = Counter()
    for x0 in range(nst):
        if color[x0]:
            continue
        path = []
        x = x0
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = succ[x]
        if color[x] == 1:
            i = path.index(x)
            p = len(path) - i
            pc[p] += 1
            cyc_nodes += p
            if p > maxp:
                maxp, arg = p, x
        for yy in path:
            color[yy] = 2
    return maxp, arg, dict(pc), cyc_nodes

def universe_graph(m, kinds):
    """Generic subuniverse graph; returns succ list + encode/decode."""
    K = len(kinds)
    kidx = [TIDX[t] for t in kinds]
    nst = 1 << (K * m)
    def decode(x):
        cells = []
        for i in range(m):
            bits = (x >> (K * i)) & ((1 << K) - 1)
            v = 0
            for j in range(K):
                if (bits >> j) & 1:
                    v |= 1 << kidx[j]
            cells.append(v)
        return tuple(cells)
    def encode(s):
        x = 0
        for i in range(m):
            bits = 0
            for j in range(K):
                if (s[i] >> kidx[j]) & 1:
                    bits |= 1 << j
            x |= bits << (K * i)
        return x
    succ = [0] * nst
    for x in range(nst):
        succ[x] = encode(step(decode(x)))
    return succ, decode, encode

def graph_cycles(succ):
    nst = len(succ)
    color = bytearray(nst)
    from collections import Counter
    pc = Counter()
    best = (0, 0)
    for x0 in range(nst):
        if color[x0]:
            continue
        path = []
        x = x0
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = succ[x]
        if color[x] == 1:
            i = path.index(x)
            p = len(path) - i
            pc[p] += 1
            if p > best[0]:
                best = (p, x)
        for yy in path:
            color[yy] = 2
    return best, pc

def basin_min_laws(succ, decode, cyc_start, nst):
    """Find min-law state whose forward orbit reaches the cycle through cyc_start."""
    # collect cycle nodes
    cyc = set([cyc_start])
    x = succ[cyc_start]
    while x != cyc_start:
        cyc.add(x)
        x = succ[x]
    # reverse edges
    from collections import defaultdict, deque
    pred = defaultdict(list)
    for u in range(nst):
        pred[succ[u]].append(u)
    seen = set(cyc)
    dq = deque(cyc)
    best = None
    while dq:
        u = dq.popleft()
        s = decode(u)
        nl = sum(bin(v).count("1") for v in s)
        if best is None or nl < best[0]:
            best = (nl, s)
        for w in pred[u]:
            if w not in seen:
                seen.add(w)
                dq.append(w)
    return best, len(seen)

if __name__ == "__main__":
    T0 = time.time()
    print("== THE SUNSET PARLIAMENT: max period of the (0,-1,1) universe vs m ==")
    seq = {}
    for m in range(2, 23):
        t0 = time.time()
        maxp, arg, pc, cn = sunset_maxp(m)
        seq[m] = maxp
        big = sorted(pc.items())[-4:]
        print(f" m={m:2d}: MAXP={maxp:5d}   #states-on-cycles={cn}"
              f"   top periods {big}   argmax occ-pattern {bin(arg)}   ({time.time()-t0:.0f}s)",
              flush=True)
    print(" sequence:", [seq[m] for m in sorted(seq)])
    json.dump(seq, open("/Users/lukacs/claude/math/program/phase6/rings/sunset_maxp.json", "w"))

    print("\n== complete 2-kind universes at m=8 ==", flush=True)
    best_all = (0, None, None)
    for pair in combinations(LIVE, 2):
        succ, decode, encode = universe_graph(8, list(pair))
        (p, x), pc = graph_cycles(succ)
        if p > best_all[0]:
            best_all = (p, pair, x)
            print(f"   new best: p={p} kinds={pair}", flush=True)
    p, pair, x = best_all
    print(f" best 2-kind at m=8: period {p} kinds={pair}")

    print("\n== certified <=6-law seeds for best cycles (basin search) ==")
    # (a) the m=8 best pair universe
    succ, decode, encode = universe_graph(8, list(pair))
    (p8, x8), _ = graph_cycles(succ)
    (nl, s), basin = basin_min_laws(succ, decode, x8, len(succ))
    print(f" m=8 pair {pair}: period {p8}; min-law state in basin: {nl} laws, basin size {basin}")
    print(f"   seed: {state_repr(s)}")
    # (b) the m=6 p=6 cycle in (0,-1,1)+(0,1,-1)
    pair6 = [(0, -1, 1), (0, 1, -1)]
    succ, decode, encode = universe_graph(6, pair6)
    (p6, x6), _ = graph_cycles(succ)
    (nl6, s6), basin6 = basin_min_laws(succ, decode, x6, len(succ))
    print(f" m=6 pair {pair6}: period {p6}; min-law seed {nl6} laws, basin {basin6}")
    print(f"   seed: {state_repr(s6)}")
    # (c) sunset parliament m=10: min-law state reaching the p=15 cycle
    succ, decode, encode = universe_graph(10, [(0, -1, 1)])
    (p10, x10), _ = graph_cycles(succ)
    (nl10, s10), basin10 = basin_min_laws(succ, decode, x10, len(succ))
    print(f" m=10 sunset: period {p10}; min-law seed {nl10} laws, basin {basin10}")
    print(f"   seed: {state_repr(s10)}")
    print(f"\ntotal {time.time()-T0:.0f}s")
