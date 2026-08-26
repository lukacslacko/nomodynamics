#!/usr/bin/env python3
"""Task 3: hunt the longest constitutional cycle on rings m<=8.

Three prongs:
  A. exhaustive small seeds: all 1-law, all 2-law codes; all 3-law codes with
     a law at position 0 (covers every 3-law code up to rotation), m=2..8.
  B. randomized 4..6-law seeds, m=4..8 (kinds biased to the 12 live kinds).
  C. EXACT functional graphs of closed subuniverses: any kind-subset is
     dynamically closed (laws toggle only their own kind), so the full state
     space of a 1- or 2-kind universe (2^m / 4^m states) can be enumerated:
     exact maximum cycle over that entire subuniverse + exact GoE counts.
Champion verified with step_ref and rendered.
"""
import sys, random, time, json
from itertools import combinations
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/rings")
from ring import (TYPES, TIDX, ACT3, step, step_ref, from_laws, state_repr,
                  render, active_count, occ_count)

LIVE = [t for k, t in enumerate(TYPES) if any((ACT3[loc] >> k) & 1 for loc in (2, 3, 6, 7))]

def attractor_period(s, budget=2500):
    seen = {}
    cur = s
    t = 0
    while t <= budget:
        if cur in seen:
            return t - seen[cur], seen[cur]      # (period, transient)
        seen[cur] = t
        cur = step(cur)
        t += 1
    return -1, budget                             # holdout


champions = {}   # m -> (period, seed_laws, transient)
allbig = []      # (period, m, laws)

def record(m, per, laws, trans):
    if per > champions.get(m, (0,))[0]:
        champions[m] = (per, laws, trans)
    if per > 4:
        allbig.append((per, m, laws))

def prong_A():
    t0 = time.time()
    holdouts = 0
    for m in range(2, 9):
        nslots = 27 * m
        # 1-law
        for k in range(27):
            laws = [(0, TYPES[k])]
            per, tr = attractor_period(from_laws(m, laws))
            if per < 0: holdouts += 1
            else: record(m, per, laws, tr)
        # 2-law: all combos
        for combo in combinations(range(nslots), 2):
            laws = [(s // 27, TYPES[s % 27]) for s in combo]
            per, tr = attractor_period(from_laws(m, laws))
            if per < 0: holdouts += 1
            else: record(m, per, laws, tr)
        # 3-law up to rotation: smallest slot id s0 at position 0 (ids 0..26),
        # remaining two slots anywhere above s0 (position 0 allowed again)
        for s0 in range(27):
            for combo in combinations(range(s0 + 1, nslots), 2):
                laws = [(s // 27, TYPES[s % 27]) for s in (s0,) + combo]
                per, tr = attractor_period(from_laws(m, laws))
                if per < 0: holdouts += 1
                else: record(m, per, laws, tr)
        print(f"  A: m={m} done ({time.time()-t0:.0f}s)", flush=True)
    print(f"  A holdouts: {holdouts}")

def prong_B(nrand=60000, seed0=7):
    rng = random.Random(seed0)
    holdouts = 0
    for m in (4, 5, 6, 7, 8):
        for _ in range(nrand):
            n = rng.randint(4, 6)
            laws = []
            for _ in range(n):
                t = rng.choice(LIVE) if rng.random() < 0.8 else rng.choice(TYPES)
                laws.append((rng.randrange(m), t))
            per, tr = attractor_period(from_laws(m, laws))
            if per < 0: holdouts += 1
            else: record(m, per, laws, tr)
    print(f"  B holdouts: {holdouts}")

def functional_graph_universe(m, kinds):
    """Exact analysis of the closed subuniverse over `kinds` on ring m.
    Returns (ncells_states, max_period, n_goe, n_states_on_cycles, period_counter)."""
    K = len(kinds)
    kidx = [TIDX[t] for t in kinds]
    nst = 1 << (K * m)
    # decode idx -> state tuple
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
    indeg = [0] * nst
    for x in range(nst):
        y = encode(step(decode(x)))
        succ[x] = y
        indeg[y] += 1
    # cycles via coloring
    color = [0] * nst          # 0 unvisited, 1 in progress, 2 done
    from collections import Counter
    pc = Counter()
    oncyc = 0
    maxp = 0
    best_state = None
    for x0 in range(nst):
        if color[x0]:
            continue
        path = []
        x = x0
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = succ[x]
        if color[x] == 1:      # new cycle
            i = path.index(x)
            p = len(path) - i
            pc[p] += 1
            oncyc += p
            if p > maxp:
                maxp = p
                best_state = decode(x)
        for y in path:
            color[y] = 2
    n_goe = sum(1 for x in range(nst) if indeg[x] == 0)
    return nst, maxp, n_goe, oncyc, dict(pc), best_state

def prong_C():
    print("  C: exact subuniverse functional graphs")
    out = []
    # all 12 single live kinds, m=4..10
    best = (0, None, None)
    for m in (4, 5, 6, 7, 8, 9, 10):
        for t in LIVE:
            nst, maxp, goe, oncyc, pc, bs = functional_graph_universe(m, [t])
            out.append(dict(m=m, kinds=[t], nst=nst, maxp=maxp, goe=goe, oncyc=oncyc))
            if maxp > best[0]:
                best = (maxp, m, [t], bs)
    print(f"    1-kind universes: best max period {best[0]} at m={best[1]} kinds={best[2]}")
    # all 66 live pairs, m=4..7 (4^m states)
    best2 = (0, None, None, None)
    for m in (4, 5, 6, 7):
        t0 = time.time()
        for pair in combinations(LIVE, 2):
            nst, maxp, goe, oncyc, pc, bs = functional_graph_universe(m, list(pair))
            out.append(dict(m=m, kinds=list(pair), nst=nst, maxp=maxp, goe=goe, oncyc=oncyc))
            if maxp > best2[0]:
                best2 = (maxp, m, list(pair), bs)
        print(f"    2-kind universes m={m}: done ({time.time()-t0:.0f}s), running best {best2[:3]}", flush=True)
    print(f"    2-kind universes: best max period {best2[0]} at m={best2[1]} kinds={best2[2]}")
    if best2[3]:
        record(best2[1], best2[0], state_repr(best2[3]), 0)
    if best[3] is not None and best[0] > 0:
        record(best[1], best[0], state_repr(best[3]), 0)
    with open("/Users/lukacs/claude/math/program/phase6/rings/subuniverses.json", "w") as f:
        json.dump(out, f, indent=0, default=str)
    return out

if __name__ == "__main__":
    T0 = time.time()
    print("== PRONG A: exhaustive seeds (1,2-law all; 3-law up to rotation), m=2..8 ==", flush=True)
    prong_A()
    print("champions so far:", {m: (p, l) for m, (p, l, tr) in sorted(champions.items())})
    print("\n== PRONG B: randomized 4-6 law seeds ==", flush=True)
    prong_B()
    print("champions so far:", {m: (p, l) for m, (p, l, tr) in sorted(champions.items())})
    print("\n== PRONG C: exact closed subuniverses ==", flush=True)
    prong_C()
    print("\n== CHAMPIONS by ring size ==")
    for m in sorted(champions):
        p, laws, tr = champions[m]
        print(f" m={m}: period {p} (transient {tr})  seed {laws}")
    print("\n periods>4 found:", sorted(set((p, m) for p, m, _ in allbig)))
    # overall champion: verify and render
    mstar = max(champions, key=lambda m: champions[m][0])
    p, laws, tr = champions[mstar]
    print(f"\n== OVERALL CHAMPION: m={mstar}, period {p} ==")
    print(f" seed: {laws}")
    s = from_laws(mstar, laws)
    for _ in range(tr + 5):
        s = step(s)
    # find the cycle start
    seen = {}
    cur = s
    t = 0
    while cur not in seen:
        seen[cur] = t
        cur = step(cur)
        t += 1
    print(" spacetime of one full period (cells: law count; step_ref-verified):")
    cyc0 = cur
    x = cyc0
    for i in range(min(p + 1, 40)):
        print(f"   t={i:3d}  {render(x)}   occ={occ_count(x)} active={active_count(x)} laws={state_repr(x)}" if i < 3 or p <= 20
              else f"   t={i:3d}  {render(x)}   occ={occ_count(x)} active={active_count(x)}")
        nx = step_ref(x)
        assert nx == step(x)
        x = nx
    occs = set()
    x = cyc0
    for i in range(p):
        occs.add(tuple(1 if v else 0 for v in x))
        x = step(x)
    print(f" occupancy patterns along cycle: {len(occs)} distinct"
          f" ({'CONSTANT occupancy' if len(occs)==1 else 'occupancy oscillates'})")
    print(f"\ntotal {time.time()-T0:.0f}s")
