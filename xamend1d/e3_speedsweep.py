import sys,time,json,math
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/xamend1d')
import multiprocessing as mp
DATA='/Users/lukacs/claude/math/program/phase6/xamend1d/data/e3_speed23.json'
def job(a):
    import xsat,xnomos
    from xsat import Spec
    n,N,p,d,mode=a
    sp=Spec(n=n,W=1,N=N,p=p,d=d,mode=mode,prime_period=True)
    t=time.time()
    st,info=xsat.solve(sp,timeout=400)
    r=dict(n=n,N=N,p=p,d=d,mode=mode,status=st,secs=round(time.time()-t,1))
    if st=='SAT':
        C=xnomos.Const(info['rules'],list(info['targets']))
        S={c:m for c,m in info['frames'][0].items() if m}
        r.update(rules=[list(x) for x in info['rules']],targets=[list(x) for x in info['targets']],
                 seed=sorted(xnomos.laws(S)),ncard=xnomos.card(S),
                 recert=bool(xnomos.verify_glider(S,C,p,info['d'],mode)),
                 cls=[xnomos.classify(S,C,mode)[k] for k in ('kind','period','displacement','t')])
    return r
jobs=[]
for mode in ('parity','or'):
  for n in (2,3):
    N = 14
    for p in range(1,9):
      for d in range(1,p+1):
        if math.gcd(p,d)!=1: continue
        jobs.append((n,N,p,d,mode))
if __name__=='__main__':
    out=[]
    with mp.Pool(5) as pool:
        for r in pool.imap_unordered(job,jobs):
            out.append(r); print(json.dumps(r)[:230],flush=True)
    json.dump(out,open(DATA,'w'),indent=1)
    print('done',len(out))
