#!/usr/bin/env python3
"""mirror.py — the MIRROR family: for which p is (p, 2) a glider?
MIRROR = n=2, W=1, channels (0,-1,1) and (0,1,-1), full targets, parity.
Width-unbounded decisions, one period at a time."""
import sys, os, time
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
sys.path.insert(0,os.path.dirname(HERE)); sys.path.insert(0,os.path.join(os.path.dirname(HERE),'xamend1d'))
import sft
CH=[(0,-1,1),(0,1,-1)]
cap=int(sys.argv[1]) if len(sys.argv)>1 else 12_000_000
for p in range(4, 13):
    for d in (2,3):
        for mode in ('parity','or'):
            t0=time.time()
            v,w=sft._search_cycle(sft.step_table(CH,1,mode),1,p,d,cap)
            extra=''
            if v=='GLIDER':
                cells=sft.witness_state(w,p)
                extra=' span=%d verified=%s'%(max(cells)-min(cells)+1, sft.verify(CH,w,p,d,mode,2))
            print('MIRROR p=%2d d=%d %-6s -> %-7s %6.0fs%s'%(p,d,mode,v,time.time()-t0,extra), flush=True)
