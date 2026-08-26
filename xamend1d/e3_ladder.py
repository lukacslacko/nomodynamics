"""Largest MINIMAL period: climb p with d=1 (slow gliders), n=3 and n=4."""
import sys,time,json
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/xamend1d')
import multiprocessing as mp
def job(a):
    import xsat,xnomos
    from xsat import Spec
    n,N,p,d,mode=a
    sp=Spec(n=n,W=1,N=N,p=p,d=d,mode=mode,prime_period=True)
    t=time.time(); st,info=xsat.solve(sp,timeout=500)
    r=dict(n=n,N=N,p=p,d=d,mode=mode,status=st,secs=round(time.time()-t,1))
    if st=='SAT':
        C=xnomos.Const(info['rules'],list(info['targets']))
        S={c:m for c,m in info['frames'][0].items() if m}
        cl=xnomos.classify(S,C,mode)
        r.update(rules=[list(x) for x in info['rules']],targets=[list(x) for x in info['targets']],
                 seed=sorted(xnomos.laws(S)),recert=bool(xnomos.verify_glider(S,C,p,d,mode)),
                 cls=[cl['kind'],cl.get('period'),cl.get('displacement'),cl.get('t')])
    return r
jobs=[(n,14,p,1,'parity') for n in (3,4) for p in (8,9,10,11,12)]
if __name__=='__main__':
    out=[]
    with mp.Pool(4) as pool:
        for r in pool.imap_unordered(job,jobs):
            out.append(r); print(json.dumps(r),flush=True)
    json.dump(out,open('/Users/lukacs/claude/math/program/phase6/xamend1d/data/e3_ladder.json','w'),indent=1)
    print('DONE')
