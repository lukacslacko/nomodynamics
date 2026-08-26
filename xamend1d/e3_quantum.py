"""Is there a DISPLACEMENT QUANTUM?  Test |d| >= 3 at n = 3, 4, 5 (free targets)."""
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
        r.update(rules=[list(x) for x in info['rules']],targets=[list(x) for x in info['targets']],
                 seed=sorted(xnomos.laws(S)),recert=bool(xnomos.verify_glider(S,C,p,d,mode)),
                 outdeg=[len(x) for x in info['targets']])
    return r
jobs=[]
for mode in ('parity','or'):
    for n in (3,4,5):
        for (p,d) in [(2,2),(3,3),(4,4),(4,3),(5,3),(5,4),(6,3),(7,3),(9,2),(8,3)]:
            jobs.append((n,14,p,d,mode))
if __name__=='__main__':
    out=[]
    with mp.Pool(4) as pool:
        for r in pool.imap_unordered(job,jobs):
            out.append(r); print(json.dumps(r),flush=True)
    json.dump(out,open('/Users/lukacs/claude/math/program/phase6/xamend1d/data/e3_quantum.json','w'),indent=1)
    print('DONE')
