#!/usr/bin/env python3
"""oddscan.py — how far does the m=15 odd-ring rotor family reach?
The four rule pairs that carry it at m=15, scanned over larger odd rings."""
import sys, time
from oddrotor import find, report
PAIRS = [((1,-1,0),(0,1,-1)), ((1,-1,-1),(0,-1,1)),
         ((0,1,-1),(-1,1,1)), ((0,-1,1),(-1,1,0))]
MS = [9, 15, 21, 25, 27, 33, 35, 39, 45]
hits = {}
t0=time.time(); calls=0
for m in MS:
    got = []
    for (r1,r2) in PAIRS:
        for rules in ((r1,r2),(r2,r1)):
            for tg in ([1,0],[0,0]):
                for mode in ("parity","or"):
                    for p in (1,2):
                        calls += 1
                        w = find(list(rules), tg, mode, m, p, list(range(1,m)))
                        if w: got.append((p, w[0], rules, tuple(tg), mode, w[1]))
    hits[m] = got
    rs = sorted({(g[0],g[1]) for g in got})
    print("m=%-3d hits=%-4d (p,rot) seen: %s   [%d calls, %.0fs]"
          % (m, len(got), rs, calls, time.time()-t0), flush=True)
print()
for m in MS:
    if hits[m]:
        p, r, rules, tg, mode, W = min(hits[m], key=lambda g:(g[0],g[1]))
        print("m=%d minimal-p witness:" % m)
        report(list(rules), list(tg), mode, m, p, r, W)
        break
