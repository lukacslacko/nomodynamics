#!/usr/bin/env python3
"""truepuffer.py — does any travelling front lay down NON-SOLID periodic debris?
The GAPPY flag counts transitions over the whole interior, so the frozen SEED
FOSSIL at the far left can fake it.  Here we measure structure ONLY in the band
[lo+FOSSIL, hi-FW] that the front itself wrote, using xnomos.step directly."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath('.'))); sys.path.insert(0,'.')
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6')
import xnomos, fastlib as F
from nearmiss import scan, certify, show, RULES1, FW
FOSSIL = 24
def band_transitions(rules, targets, mode, S0, T=140):
    C = xnomos.Const(rules, targets); S = dict(S0)
    for _ in range(T-1): S = xnomos.step(S, C, mode)
    if not S: return -1, 0
    lo, hi = min(S), max(S)
    a, b = lo+FOSSIL, hi-FW
    if b - a < 12: return -1, 0
    occ = [1 if c in S else 0 for c in range(a, b+1)]
    tr = sum(1 for i in range(1, len(occ)) if occ[i] != occ[i-1])
    return tr, sum(occ)/len(occ)
def hunt(label, consts, seeds, mode):
    tally, cand = scan(label, consts, seeds, mode)
    pool = {tuple(r) for k in ("puffer","osc_puffer","gun") for r in cand[k]}
    best = []
    for ci, si, p, d, nblk in pool:
        rules, targets = consts[ci]; S0 = F.unpack_state(seeds[si])
        tr, dens = band_transitions(rules, targets, mode, S0)
        if tr >= 2: best.append((tr, dens, xnomos.card(S0), ci, si, p, d))
    best.sort(key=lambda x: (-x[0], x[2]))
    print("   candidates with STRUCTURED front-written debris (>=2 transitions "
          "in the band the front wrote): %d of %d front-periodic candidates"
          % (len(best), len(pool)))
    return best, cand
tot = 0
for label, consts, seeds, modes in [
    ("E2 L=2 [1,0]", [(list(r),[1,0]) for r in itertools.product(RULES1,repeat=2)],
     F.all_seeds(2,6,4), ["parity"]),
    ("SUP n=2", [(list(r),[0,1]) for r in itertools.product(RULES1,repeat=2)],
     F.all_seeds(2,7,5), ["super","super_or"]),
    ("E3 n=2 all-targets",
     [(list(r),list(t)) for r in itertools.product(RULES1,repeat=2)
      for t in itertools.product([(0,),(1,),(0,1)],repeat=2)],
     F.all_seeds(2,6,4), ["parity","or"]),
]:
    for mode in modes:
        best, cand = hunt(label, consts, seeds, mode)
        tot += len(best)
        for tr, dens, cd, ci, si, p, d in best[:1]:
            rules, targets = consts[ci]; S0 = F.unpack_state(seeds[si])
            show("TRUE-PUFFER CANDIDATE [%s/%s] p=%d d=%+d band-transitions=%d "
                 "band-density=%.2f" % (label, mode, p, d, tr, dens),
                 rules, targets, mode, S0, steps=22, width=44)
            certify(rules, targets, mode, S0, p, d)
print("\nTOTAL structured-debris (true puffer) candidates:", tot)
