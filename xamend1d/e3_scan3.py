"""COMPLETE scan: all 19683 n=3 rule triples x selected target matrices x all
translation-normalised seeds in a 2-cell window (56 seeds).  Records every
glider cycle's MINIMAL period and displacement."""
import sys,json,time,itertools
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/xamend1d')
import multiprocessing as mp
OFF=(-1,0,1); RULES=[(a,b,c) for a in OFF for b in OFF for c in OFF]
TGS=[[(0,1,2),(0,1,2),(0,1,2)],
     [(1,2),(0,2),(0,1)],
     [(1,2),(0,),(0,)],
     [(0,1),(2,),(0,1,2)],
     [(0,1,2),(0,),(0,)],
     [(0,2),(0,2),(0,1,2)],
     [(0,1),(0,1),(0,1,2)],
     [(1,2),(0,1),(0,2)]]
def job(a):
    from e3_zoo import census, seeds_window
    ti,mode=a
    tg=TGS[ti]
    sds=seeds_window(3,2)
    best=None; rows={}
    for r0 in RULES:
        for r1 in RULES:
            for r2 in RULES:
                cyc=census([r0,r1,r2],tg,mode,sds,3)
                for (p,d,mc,w) in cyc.values():
                    key=(p,d)
                    if key not in rows or mc<rows[key][0]:
                        rows[key]=(mc,[list(r0),list(r1),list(r2)],list(w))
    return (ti,mode,{('%d,%d'%k):v for k,v in rows.items()})
if __name__=='__main__':
    jobs=[(i,m) for i in range(len(TGS)) for m in ('parity','or')]
    out=[]
    with mp.Pool(4) as pool:
        for ti,mode,rows in pool.imap_unordered(job,jobs):
            mx=max((int(k.split(',')[0]) for k in rows),default=0)
            print('T=%s %-6s : %d (p,d) classes, max minimal period %d'%(TGS[ti],mode,len(rows),mx),flush=True)
            out.append(dict(targets=[list(t) for t in TGS[ti]],mode=mode,rows=rows))
    json.dump(out,open('/Users/lukacs/claude/math/program/phase6/xamend1d/data/e3_scan3.json','w'),indent=1)
    print('DONE')
