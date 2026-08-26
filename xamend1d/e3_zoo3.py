"""Full seed census of the n=3 universes SAT found productive: the glider zoo."""
import sys,json,time
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/xamend1d')
import xnomos
from e3_zoo import census, seeds_window, key_to_state
UNIS=[  # (rules, targets, mode) from certified SAT hits
 ([(0,1,0),(0,1,1),(0,1,0)],[(1,2),(0,),(0,)],'parity'),
 ([(0,1,1),(-1,1,0),(0,1,-1)],[(1,2),(0,2),(0,1)],'parity'),
 ([(0,-1,1),(0,-1,0),(-1,1,-1)],[(1,2),(0,2),(0,1)],'parity'),
 ([(0,-1,1),(0,1,1),(0,1,0)],[(0,1),(2,),(0,1,2)],'parity'),
 ([(0,1,1),(0,-1,1),(0,1,0)],[(2,),(0,1),(0,1,2)],'or'),
 ([(0,-1,1),(0,1,1),(0,1,-1)],[(0,1,2),(0,),(0,)],'parity'),
 ([(0,1,-1),(0,1,1),(1,-1,1)],[(0,1,2),(0,1,2),(0,2)],'parity'),
 ([(0,1,0),(0,-1,0),(0,-1,1)],[(1,2),(0,1),(0,2)],'parity'),
 ([(0,-1,1),(1,-1,0),(0,1,0)],[(0,2),(0,2),(0,1,2)],'parity'),
 ([(0,-1,1),(-1,1,1),(-1,1,-1)],[(1,2),(0,),(0,)],'parity'),
 ([(-1,1,1),(0,1,-1),(0,1,0)],[(0,1,2),(0,1),(0,1,2)],'parity'),
 ([(0,-1,1),(-1,1,-1),(0,1,0)],[(0,2),(0,2),(0,1,2)],'parity'),
]
W=int(sys.argv[1]) if len(sys.argv)>1 else 5
sds=seeds_window(3,W)
print('seeds per universe: %d (window %d cells)'%(len(sds),W),flush=True)
allrec=[]
for rules,tg,mode in UNIS:
    t=time.time()
    cyc=census(rules,tg,mode,sds,3)
    best=sorted(((p,abs(d),mc,d,w) for (p,d,mc,w) in cyc.values()),key=lambda x:(-x[0],x[2]))
    print('%s T=%s %-6s : %d glider cycles, %.0fs'%(rules,tg,mode,len(cyc),time.time()-t),flush=True)
    for (p,ad,mc,d,w) in best[:4]:
        S=key_to_state(w); C=xnomos.Const([tuple(r) for r in rules],[tuple(x) for x in tg])
        cl=xnomos.classify(S,C,mode)
        ok=(cl['kind']=='GLIDER' and cl['period']==p and cl['displacement']==d and cl['t']==0
            and xnomos.verify_glider(S,C,p,d,mode))
        print('    p=%2d d=%+d laws=%2d verified=%s seed=%s'%(p,d,mc,ok,sorted(xnomos.laws(S))),flush=True)
        allrec.append(dict(rules=rules,targets=[list(x) for x in tg],mode=mode,p=p,d=d,laws=mc,
                           seed=sorted(xnomos.laws(S)),verified=bool(ok)))
json.dump(allrec,open('/Users/lukacs/claude/math/program/phase6/xamend1d/data/e3_zoo3.json','w'),indent=1)
print('DONE  max minimal period found: %d'%max(r['p'] for r in allrec))
