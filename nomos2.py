#!/usr/bin/env python3
"""Nomodynamics first contact, v2: bitmask engine.
State: dict pos -> 27-bit mask of law types present.
Type index: t = 9*(a+1) + 3*(b+1) + (c+1); offsets a,b,c in {-1,0,1}.
Active law (i,t): occupied(i+a) and not occupied(i+b); toggles bit t at i+c.
"""
import sys
from collections import Counter, defaultdict

TYPES = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]
TIDX = {t: k for k, t in enumerate(TYPES)}

def step(S):
    occ = S.keys()
    tog = defaultdict(int)
    for i, mask in S.items():
        m = mask
        while m:
            k = (m & -m).bit_length() - 1
            m &= m - 1
            a, b, c = TYPES[k]
            if (i + a) in S and (i + b) not in S:
                tog[i + c] ^= (1 << k)
    out = dict(S)
    for i, x in tog.items():
        nm = out.get(i, 0) ^ x
        if nm:
            out[i] = nm
        elif i in out:
            del out[i]
    return out

def norm_key(S):
    if not S:
        return (), 0
    m = min(S)
    return tuple(sorted((i - m, v) for i, v in S.items())), m

def size(S):
    return sum(bin(v).count("1") for v in S.values())

def classify(seed, max_steps=6000, hash_size_cap=400, growth_size=4000):
    S = dict(seed)
    seen = {}
    sizes = []
    for t in range(max_steps):
        if not S:
            return ("extinct", t, None)
        sz = size(S)
        sizes.append(sz)
        if sz > growth_size:
            # growth verdict with crude rate estimate
            half = sizes[len(sizes)//2]
            return ("growth", t, (sz, half))
        if sz <= hash_size_cap:
            key, off = norm_key(S)
            if key in seen:
                t0, off0 = seen[key]
                period, disp = t - t0, off - off0
                if disp == 0:
                    return ("fixed" if period == 1 else "cycle", t0, period)
                return ("glider", t0, (period, disp, sz))
            seen[key] = (t, off)
        S = step(S)
    return ("holdout", max_steps, (size(S), sizes[-1] - sizes[-min(len(sizes),1000)]))

def show(S, lo=-30, hi=30):
    row = ""
    for i in range(lo, hi + 1):
        v = S.get(i, 0)
        n = bin(v).count("1")
        row += "." if n == 0 else (str(n) if n < 10 else "#")
    return row

def seed_single(t):
    return {0: 1 << TIDX[t]}

def seed_pair(t1, t2, d):
    S = {0: 1 << TIDX[t1]}
    S[d] = S.get(d, 0) | (1 << TIDX[t2])
    return S

if __name__ == "__main__":
    print("== SINGLE-LAW SEEDS (27) ==")
    tally = Counter(); rows = []
    for t in TYPES:
        v, tt, data = classify(seed_single(t))
        tally[v] += 1
        rows.append((t, v, tt, data))
    print("tally:", dict(tally))
    for (t, v, tt, data) in rows:
        if v not in ("extinct", "fixed"):
            print(f"  law {t}: {v} @t={tt} {data}")
    sys.stdout.flush()

    print("\n== TWO-LAW SEEDS (second law at offset 0..3) ==")
    tally2 = Counter(); spec = defaultdict(list)
    for t1 in TYPES:
        for t2 in TYPES:
            for d in range(0, 4):
                if d == 0 and TIDX[t2] <= TIDX[t1]:
                    continue
                v, tt, data = classify(seed_pair(t1, t2, d), max_steps=3000)
                tally2[v] += 1
                if len(spec[v]) < 400:
                    spec[v].append((t1, t2, d, tt, data))
    print("tally:", dict(tally2))
    for v in ("glider", "growth", "holdout", "cycle"):
        lst = spec[v]
        print(f"\n  {v}: {len(lst)} recorded; first 10:")
        for (t1, t2, d, tt, data) in lst[:10]:
            print(f"    {t1}@0 + {t2}@{d}: t={tt} {data}")
