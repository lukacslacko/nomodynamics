"""T4 core: glider vs DEAD-LETTER walls (FIXED codes with 0 active laws).
BOX (complete in the walls):
  MIRROR   : all 41 DEAD codes with support in cells 0..4 (768 anchored seeds
             enumerated completely); glider phase 0..4; gap 0..8   -> 1845 runs
  TRIPTYCH : all 24 DEAD codes with support in cells 0..2 (448 anchored seeds);
             glider phase 0 (p=1); gap 0..8                        ->  216 runs
  TANDEM-1 / SOLO / GUN : 0 DEAD codes exist in their boxes (see BALLISTIC.md).
resolve(T_max=200, N_sep=70, max_card=200, max_span=400).
"""
import sys, json, time
from collections import Counter
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/computation')
from ballistic_lib import *
from ballistic_collide import resolve, fmt_parts
from ballistic_t4_walls import UNIS, enumerate_walls, wall_bucket
for nm, WW, GAPS in (("MIRROR",5,9), ("TRIPTYCH",3,9)):
    C,G,p,d = UNIS[nm]
    walls=[w for w in enumerate_walls(C,'parity',WW) if w[0]=="DEAD"]
    print("%s: %d DEAD-LETTER walls in cells 0..%d"%(nm,len(walls),WW-1),flush=True)
    gph=orbit(G,C,'parity',p); rows=[]; t0=time.time()
    for wi,(tag,q,act,WS) in enumerate(walls):
        assert step(WS,C,'parity')==WS and not active_laws(WS,C)
        for gi,A0 in enumerate(gph):
            for gap in range(GAPS):
                A=shift(A0,min(WS)-1-gap-max(A0)); S=union(A,WS)
                r=resolve(S,C,'parity',T_max=200,N_sep=70,max_card=200,max_span=400)
                rows.append({"wcells":sorted(WS.items()),"gi":gi,"gap":gap,
                             "bucket":wall_bucket(r,WS,C,'parity'),"parts":fmt_parts(r)})
    c=Counter(r["bucket"] for r in rows)
    print("   N=%d  [%.0fs]"%(len(rows),time.time()-t0))
    for k,v in c.most_common(): print("     %-22s %5d"%(k,v))
    # is the wall RESTORED after absorbing?
    keep=sum(1 for r in rows if r["bucket"]=="ABSORBED")
    print("     walls that survive as SOME stationary code: %d/%d"%(keep,len(rows)))
    for sp in ("FAN-OUT","REFLECT","TRANSPARENT","WALL-DESTROYED","MUTUAL-ANNIHILATION","EXPLOSION"):
        ex=[r for r in rows if r["bucket"]==sp]
        if ex: print("     *** %s x%d e.g. wall=%s gi=%d gap=%d -> %s"%(sp,len(ex),ex[0]["wcells"],ex[0]["gi"],ex[0]["gap"],ex[0]["parts"]))
    json.dump(rows,open("ballistic_walls_dead_%s.json"%nm.replace('/','_'),"w"))
