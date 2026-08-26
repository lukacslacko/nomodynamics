import sys, time
from collections import Counter
from xring import *

def full_spectrum(R):
    """Complete state-space cycle census. Returns Counter{period: #cycles},
    plus rotor list [(p,r,period,state)]."""
    n, m = R.n, R.m
    N = 1 << (n*m)
    succ = [0]*N
    for v in range(N):
        X = decode(v, n, m)
        succ[v] = encode(R.step(X), m)
    color = bytearray(N); idx = [0]*N
    periods = Counter(); reps = []
    for s0 in range(N):
        if color[s0]: continue
        path = []
        v = s0
        while color[v] == 0:
            color[v] = 1; idx[v] = len(path); path.append(v); v = succ[v]
        if color[v] == 1:
            p = len(path) - idx[v]
            periods[p] += 1
            reps.append((p, v))
        for u in path: color[u] = 2
    return periods, reps

t0=time.time()
best = {}
for m in (5,6):
    for i1,r1 in enumerate(RULES27):
        for r2 in RULES27:
            R = Ring([r1,r2],[1,0],m,'parity')
            per, reps = full_spectrum(R)
            for p,_ in reps:
                if p not in best or best[p][0] > m:
                    best[p] = (m, r1, r2)
    print("m=%d done %.1fs  periods seen: %s" % (m, time.time()-t0, sorted(best)), flush=True)
print(best)
