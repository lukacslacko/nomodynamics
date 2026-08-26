#!/usr/bin/env python3
"""3-law ring rotor search, m=3..7, W=1 parity; canonical: first law at cell 0."""
import sys, os, itertools
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nomos_lib import build_tables
from ring_rotor import make_ring_step, classify_ring, verify_rotor
from multiprocessing import Pool

def jobs(m, NT):
    nslots = m * NT
    for first in range(NT):
        yield (m, first)

_G = {}
def _init():
    for m in range(3, 8):
        _G[m] = make_ring_step(1, m)

def run(job):
    m, first = job
    NT = 27
    nslots = m * NT
    step = _G[m]
    tally = Counter(); rot = []
    for rest in itertools.combinations(range(first + 1, nslots), 2):
        slots = (first,) + rest
        S = {}
        for s in slots:
            p, k = divmod(s, NT)
            S[p] = S.get(p, 0) | (1 << k)
        v, t, info = classify_ring(S, step, m, max_steps=3000)
        tally[v] += 1
        if v == "ROTOR":
            T = dict(S)
            for _ in range(t):
                T = step(T)
            ok = verify_rotor(T, step, m, info["period"], info["rot"])
            rot.append((slots, info, ok))
    return m, tally, rot

if __name__ == "__main__":
    agg = {m: Counter() for m in range(3, 8)}
    rotors = []
    alljobs = [j for m in range(3, 8) for j in jobs(m, 27)]
    with Pool(6, initializer=_init) as pool:
        for m, tally, rot in pool.imap_unordered(run, alljobs):
            agg[m].update(tally)
            rotors.extend((m, r) for r in rot)
    for m in range(3, 8):
        print(f"ring m={m} 3-law: {sum(agg[m].values())} seeds -> {dict(agg[m])}", flush=True)
    print("ROTORS:", len(rotors))
    for m, (slots, info, ok) in rotors[:40]:
        print(f"  m={m} slots={slots} {info} verified={ok}")
