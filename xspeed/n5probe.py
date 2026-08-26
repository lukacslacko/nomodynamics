#!/usr/bin/env python3
"""n5probe.py — is the single-field cap |d|<=2 broken by a FIFTH channel?
Decides (p,d)=(4,3) and (5,3) at W=1, width-unbounded, over every 5-channel
full-target constitution."""
import itertools, sys, os, time
from multiprocessing import Pool
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
sys.path.insert(0,os.path.join(os.path.dirname(HERE),'xamend1d')); sys.path.insert(0,os.path.dirname(HERE))
import sft
LIVE=[(a,b,c) for a in(-1,0,1) for b in(-1,0,1) for c in(-1,0,1) if a!=b]
def one(arg):
    ch,p,d,mode=arg
    cm=max(c for _,_,c in ch); cn=min(c for _,_,c in ch)
    if cm<1 or cn>0 or d>p*cm: return ('PRUNED',None,ch)
    v,w=sft._search_cycle(sft.step_table(list(ch),1,mode),1,p,d,1200000)
    return (v,w,ch)
if __name__=='__main__':
    n=int(sys.argv[1]); pd=[(int(sys.argv[2]),int(sys.argv[3]))]
    cons=list(itertools.combinations_with_replacement(LIVE,n))
    print('n=%d channels, %d constitutions'%(n,len(cons)),flush=True)
    for (p,d) in pd:
        for mode in ('parity','or'):
            t0=time.time(); hit=None; caps=0
            with Pool(3) as pool:
                for v,w,ch in pool.imap_unordered(one,[(c,p,d,mode) for c in cons],chunksize=16):
                    if v=='CAP': caps+=1
                    elif v=='GLIDER' and hit is None: hit=(ch,sft.witness_state(w,p),sft.verify(list(ch),w,p,d,mode,n))
            print('n=%d p=%d d=%d %-6s -> %s caps=%d %.0fs %s'%(n,p,d,mode,'GLIDER' if hit else ('CAP' if caps else 'NONE'),caps,time.time()-t0,hit or ''),flush=True)
