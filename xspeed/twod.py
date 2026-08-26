#!/usr/bin/env python3
"""twod.py — does the 1-D quantisation survive in 2 dimensions?

Sample (not a decision): full-target constitutions in dim 2, W=1, n kinds.
By the Twin-Kind Lemma a full-target constitution is again a single-field CA,
now on Z^2 with n channels.  We enumerate/sample constitutions and classify
small seeds with the reference engine, recording every glider's (p, v) and the
reduced velocity v/gcd.
"""
import itertools, random, sys, os, collections, json
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, os.path.join(os.path.dirname(HERE),'xamend1d'))
import xnomos

OFF=[(a,b) for a in(-1,0,1) for b in(-1,0,1)]

def run(n, trials, seedcells, mode, rng):
    found=collections.defaultdict(list)
    chan=[ (a,b,c) for a in OFF for b in OFF for c in OFF if a!=b ]
    for _ in range(trials):
        rules=[rng.choice(chan) for _ in range(n)]
        C=xnomos.Const(rules, [tuple(range(n))]*n, dim=2)
        for _ in range(seedcells):
            k=rng.randint(1,5)
            cells=set()
            while len(cells)<k:
                cells.add((rng.randint(0,2), rng.randint(0,2)))
            S={c:(1<<n)-1 for c in cells}
            r=xnomos.classify(S,C,mode,max_steps=90,max_card=90,max_span=60)
            if r['kind']=='GLIDER' and r.get('displacement') not in (None,(0,0)):
                v=r['displacement']; p=r['period']
                if isinstance(v,tuple) and v!=(0,0):
                    from math import gcd
                    g=gcd(gcd(abs(v[0]),abs(v[1])),p)
                    found[(p,v)].append((rules,sorted(S)))
    return found

if __name__=='__main__':
    rng=random.Random(7)
    for n in (2,3):
        for mode in ('parity','or'):
            f=run(n, int(sys.argv[1]) if len(sys.argv)>1 else 3000, 6, mode, rng)
            keys=sorted(f)
            print('n=%d %s: %d distinct (p,v)'%(n,mode,len(keys)))
            for k in keys[:200]:
                p,v=k
                from math import gcd
                g=gcd(gcd(abs(v[0]),abs(v[1])),p)
                print('   p=%d v=%s  reduced=(%d,(%d,%d))  eg rules=%s seed=%s'%(p,v,p//g,v[0]//g,v[1]//g,f[k][0][0],f[k][0][1]))
