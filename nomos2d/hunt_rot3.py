#!/usr/bin/env python3
"""Dedicated hunt: 3-law {k,k,R2k} rotor-family seeds (half-turn pinwheels)."""
import random
from collections import Counter
from engine2d import classify, TPERM, GID, tname
R2 = TPERM[GID[(2, 0)]]
rng = random.Random(99)
seeds = []
for _ in range(30000):
    k = rng.randrange(1, 125)
    spec = set()
    while len(spec) < 3:
        p = (rng.randint(-1, 1), rng.randint(-1, 1))
        kk = k if len(spec) < 2 else R2[k]
        spec.add((p, kk))
    seeds.append(sorted(spec))
tal = Counter()
finds = []
for s in seeds:
    v = classify(s, max_steps=200, growth_cap=900)
    key = v["v"] if v["v"] != "cycle" else f"cycle-{v['p']}"
    tal[key] += 1
    if v["v"] in ("rotor", "glide", "glider"):
        finds.append((s, v))
print("rot3 hunt tally:", dict(sorted(tal.items(), key=lambda x: -x[1])))
print("rotor/glide/glider finds:", len(finds))
for s, v in finds[:12]:
    print("  ", [(p, tname(k)) for p, k in s], {a: b for a, b in v.items() if a != "sizes"})
