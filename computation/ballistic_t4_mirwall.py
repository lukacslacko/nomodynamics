"""T4 (MIRROR): glider-vs-wall.
BOX: walls = ALL stationary codes with support in cells 0..4, cell 0 occupied
     (768 anchored seeds enumerated completely -> 352 codes: 41 DEAD, 14 BAL,
      297 OSC).  wall phase 0..min(q,2)-1; glider phase 0..4; gap 0..8.
     resolve(T_max=240, N_sep=100, max_card=250, max_span=500).
"""
import sys, json, time
from collections import Counter
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/computation')
from ballistic_lib import *
from ballistic_collide import resolve, fmt_parts
from ballistic_t4_walls import UNIS, enumerate_walls, wall_bucket
C,G,p,d = UNIS["MIRROR"]
print("MIRROR",C.label()," glider p=%d d=+%d card=%d span=%d"%(p,d,card(G),span(G)),flush=True)
for mode in ("parity",):
    walls=enumerate_walls(C,mode,5)
    print("mode=%s -> %d stationary codes %s"%(mode,len(walls),dict(Counter(w[0] for w in walls))),flush=True)
    rows=[];t0=time.time()
    gph=orbit(G,C,mode,p)
    for wi,(tag,q,act,WS) in enumerate(walls):
        for wj,W in enumerate(orbit(WS,C,mode,min(q,2))):
            for gi,A0 in enumerate(gph):
                for gap in range(9):
                    A=shift(A0,min(W)-1-gap-max(A0)); S=union(A,W)
                    if card(S)!=card(A)+card(W): continue
                    r=resolve(S,C,mode,T_max=240,N_sep=100,max_card=250,max_span=500)
                    rows.append({"tag":tag,"q":q,"wcells":sorted(WS.items()),
                                 "wj":wj,"gi":gi,"gap":gap,
                                 "bucket":wall_bucket(r,W,C,mode),"parts":fmt_parts(r)})
        if wi%40==0: print("   wall %d/%d N=%d %.0fs"%(wi,len(walls),len(rows),time.time()-t0),flush=True)
    c=Counter(r["bucket"] for r in rows)
    print("  N=%d  [%.0fs]"%(len(rows),time.time()-t0))
    for k,v in c.most_common(): print("    %-22s %5d"%(k,v))
    for tg in ("DEAD","BAL","OSC"):
        cc=Counter(r["bucket"] for r in rows if r["tag"]==tg)
        if cc: print("    by wall type %-4s (n_walls=%d): %s"%(tg,sum(1 for w in walls if w[0]==tg),dict(cc)))
    for sp in ("FAN-OUT","REFLECT","TRANSPARENT","WALL-DESTROYED","MUTUAL-ANNIHILATION"):
        ex=[r for r in rows if r["bucket"]==sp]
        for r in ex[:5]: print("    *** %s wall=%s tag=%s wj=%d gi=%d gap=%d -> %s"%(sp,r["wcells"],r["tag"],r["wj"],r["gi"],r["gap"],r["parts"]))
    json.dump(rows,open("ballistic_walls_mirror_%s.json"%mode,"w"))
