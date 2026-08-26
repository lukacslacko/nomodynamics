#!/usr/bin/env python3
"""Nomodynamics: first contact. Window-1 nomic chain simulator + seed census.

State: set of (pos, (a,b,c)) with a,b,c in {-1,0,1}.
Law (i,(a,b,c)) active iff some law at i+a and no law at i+b.
Active law toggles (i+c, (a,b,c)). Synchronous, parity resolution.
"""
import itertools
from collections import Counter

TYPES = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]

def step(S):
    occ = {i for (i, t) in S}
    toggles = Counter()
    for (i, (a, b, c)) in S:
        if (i + a) in occ and (i + b) not in occ:
            toggles[(i + c, (a, b, c))] += 1
    T = {x for x, k in toggles.items() if k % 2 == 1}
    return S ^ T

def normalize(S):
    """translation-normalized canonical form + offset"""
    if not S:
        return frozenset(), 0
    m = min(i for (i, t) in S)
    return frozenset((i - m, t) for (i, t) in S), m

def classify(seed, max_steps=20000, max_size=30000):
    """returns (verdict, data)"""
    S = set(seed)
    seen = {}
    for t in range(max_steps):
        if not S:
            return ("extinct", t)
        if len(S) > max_size:
            return ("growth", (t, len(S)))
        norm, off = normalize(S)
        key = norm
        if key in seen:
            t0, off0 = seen[key]
            period = t - t0
            disp = off - off0
            if disp == 0:
                if period == 0:  # shouldn't happen
                    return ("fixed?", t)
                # distinguish fixed point (period1, same set) from cycle
                return ("fixed" if period == 1 and step(set(S)) == S else "cycle",
                        (t0, period))
            else:
                return ("glider", (t0, period, disp, len(S)))
        seen[key] = (t, off)
        S = step(S)
    return ("holdout", (max_steps, len(S)))

def show(S, lo=-15, hi=15):
    """one-line occupancy sketch"""
    occ = Counter(i for (i, t) in S)
    return "".join("." if occ[i] == 0 else (str(occ[i]) if occ[i] < 10 else "#")
                   for i in range(lo, hi + 1))

if __name__ == "__main__":
    print("== SINGLE-LAW SEEDS (27) ==")
    tally = Counter()
    interesting = []
    for t in TYPES:
        seed = frozenset({(0, t)})
        verdict, data = classify(seed)
        tally[verdict] += 1
        if verdict in ("glider", "growth", "holdout", "cycle"):
            interesting.append((t, verdict, data))
    print("tally:", dict(tally))
    for (t, verdict, data) in interesting:
        print(f"  law {t}: {verdict} {data}")

    print("\n== TWO-LAW SEEDS: second law at offset d in 0..3 ==")
    tally2 = Counter()
    specimens = {"glider": [], "growth": [], "holdout": [], "cycle": []}
    for t1 in TYPES:
        for t2 in TYPES:
            for d in range(0, 4):
                if d == 0 and t2 <= t1:
                    continue  # same site: unordered pair
                seed = frozenset({(0, t1), (d, t2)})
                verdict, data = classify(seed, max_steps=5000, max_size=20000)
                tally2[verdict] += 1
                if verdict in specimens and len(specimens[verdict]) < 12:
                    specimens[verdict].append((t1, t2, d, data))
    print("tally:", dict(tally2))
    for v, lst in specimens.items():
        if lst:
            print(f"\n  sample {v}:")
            for (t1, t2, d, data) in lst[:8]:
                print(f"    {t1} @0 + {t2} @{d}: {data}")
