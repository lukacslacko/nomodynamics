#!/usr/bin/env python3
"""finalstats.py — the definitive gallery-wide numbers quoted in RESULTS.md."""
import os, sys
from collections import Counter
sys.path.insert(0, '.'); sys.path.insert(0, '..')
import xnomos
from xring import Ring, decode
from certify import to_dict, MODENAME
from unroll import gallery, tile

TAGS = ["own","own2","own3","recip","noninj","cyc3","cyc3all",
        "super1","super2","super3","goe","big2"]
G = gallery(TAGS)
print("rotor classes over ALL censuses: %d" % len(G))
spatial = [(k,v) for k,v in G if k[2] != 0]
screw0  = [(k,v) for k,v in G if k[2] == 0]
print("  spatial (r != 0): %d   pure-screw (r = 0, j != 0): %d"
      % (len(spatial), len(screw0)))
lc = Counter()
for (m,p,r,j,rules,tg,mode),(card,rep) in spatial:
    d = min(r % m, (-r) % m)
    lc["transporting" if d <= 2*p else "barber-pole"] += 1
print("  light cone among SPATIAL rotors: %s" % dict(lc))

ok=bad=0
for (m,p,r,j,rules,tg,mode),(card,rep) in G:
    n=len(rules); X=decode(rep,n,m)
    for q in (2,3):
        R2=Ring(list(rules),list(tg),q*m,MODENAME[mode]); Y=tile(X,m,q); Z=Y
        for _ in range(p): Z=R2.step(Z)
        if Z==R2.rot_state(tuple(Y[(k-j)%n] for k in range(n)), r): ok+=1
        else: bad+=1
print("tiling lift to Z/2m and Z/3m: %d confirmed, %d failed" % (ok,bad))

tally=Counter(); hold=[]
for (m,p,r,j,rules,tg,mode),(card,rep) in G:
    n=len(rules); X=decode(rep,n,m); S=to_dict(X,m)
    C=xnomos.Const(list(rules),list(tg),dim=1,modulus=None)
    res=xnomos.classify(S,C,MODENAME[mode],max_steps=600,max_card=300,max_span=300)
    tally[res["kind"]]+=1
    if res["kind"]==xnomos.UNRESOLVED: hold.append((rules,tg,mode,S))
    if res["kind"]==xnomos.GLIDER: print("*** GLIDER ON Z ***", m, rules, tg, mode, sorted(S.items()))
print("finite chunk released on Z: %s" % dict(tally))
t2=Counter()
for rules,tg,mode,S in hold:
    C=xnomos.Const(list(rules),list(tg),dim=1,modulus=None)
    r2=xnomos.classify(S,C,mode,max_steps=6000,max_card=3000,max_span=3000)
    t2[r2["kind"]]+=1
    if r2["kind"]==xnomos.GLIDER: print("*** GLIDER ON Z (10x) ***", rules, tg, mode, sorted(S.items()))
print("  holdouts at 10x budget: %s" % dict(t2))
