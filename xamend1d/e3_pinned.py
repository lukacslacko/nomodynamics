"""Guard-resolved COMPLETE classification of n=2, W=1: every one of the 6561
universes gets its own SAT question with rules AND targets pinned."""
import sys,json,time,itertools
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/xamend1d')
import multiprocessing as mp
OFF=(-1,0,1); RULES=[(a,b,c) for a in OFF for b in OFF for c in OFF]
TS=[(0,),(1,),(0,1)]
def job(a):
    import xsat,xnomos
    from xsat import Spec
    r0,r1,t0,t1,mode,N,pmax=a
    hits=[]
    for p in range(1,pmax+1):
        for d in list(range(1,p+1))+list(range(-1,-p-1,-1)):
            sp=Spec(n=2,W=1,N=N,p=p,d=d,mode=mode,fixed_rules=[r0,r1],targets=[t0,t1],prime_period=True)
            st,info=xsat.solve(sp,timeout=200)
            if st=='SAT':
                C=xnomos.Const([r0,r1],[t0,t1]); S={c:m for c,m in info['frames'][0].items() if m}
                assert xnomos.verify_glider(S,C,p,d,mode)
                hits.append((p,d,xnomos.card(S),sorted(xnomos.laws(S))))
            elif st=='TIMEOUT': hits.append(('TO',p,d))
    return (r0,r1,t0,t1,mode,hits)
if __name__=='__main__':
    mode=sys.argv[1]; N=int(sys.argv[2]); pmax=int(sys.argv[3])
    jobs=[(r0,r1,t0,t1,mode,N,pmax) for r0 in RULES for r1 in RULES for t0 in TS for t1 in TS]
    print('%d universes, mode=%s N=%d pmax=%d'%(len(jobs),mode,N,pmax),flush=True)
    out=[]; t0_=time.time()
    with mp.Pool(6) as pool:
        for i,r in enumerate(pool.imap_unordered(job,jobs,chunksize=8)):
            out.append(r)
            if (i+1)%500==0: print('  %d/%d %.0fs'%(i+1,len(jobs),time.time()-t0_),flush=True)
    ng=[r for r in out if r[5]]
    print('universes with a glider (rules AND targets pinned, seeds free in %d cells): %d'%(N-2,len(ng)))
    json.dump([[list(r[0]),list(r[1]),list(r[2]),list(r[3]),r[4],r[5]] for r in ng],
              open('/Users/lukacs/claude/math/program/phase6/xamend1d/data/e3_pinned_%s.json'%mode,'w'),indent=1)
