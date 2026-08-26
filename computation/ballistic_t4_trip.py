"""T4 (TRIPTYCH): glider-vs-wall.  TRIPTYCH collisions mostly EXPLODE, so the
box is smaller and the explosion budget tighter -- stated exactly below.

BOX:  walls = ALL stationary codes with support in cells 0..2, cell 0 occupied
      (448 anchored seeds enumerated completely -> 208 stationary codes:
       24 DEAD, 65 BAL, 119 OSC).
      wall phase 0..min(q,2)-1;  glider phase 0 (p=1);  gap 0..8.
      resolve(T_max=200, N_sep=90, max_card=120, max_span=200).
"""
import sys, json, time
from collections import Counter
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/computation')
from ballistic_lib import *
from ballistic_collide import resolve, fmt_parts
from ballistic_t4_walls import UNIS, enumerate_walls, wall_bucket

C, G, p, d = UNIS["TRIPTYCH"]
print("TRIPTYCH", C.label(), " glider p=%d d=+%d card=%d span=%d"%(p,d,card(G),span(G)))
for mode in ("parity","or"):
    walls = enumerate_walls(C, mode, 3)
    print("mode=%s  208-code box -> %d stationary codes %s"
          % (mode, len(walls), dict(Counter(w[0] for w in walls))))
    if not walls: continue
    rows=[]; t0=time.time()
    for wi,(tag,q,act,WS) in enumerate(walls):
        for wj,W in enumerate(orbit(WS,C,mode,min(q,2))):
            for gap in range(9):
                A=shift(G, min(W)-1-gap-max(G))
                S=union(A,W)
                if card(S)!=card(A)+card(W): continue
                r=resolve(S,C,mode,T_max=200,N_sep=90,max_card=120,max_span=200)
                rows.append({"tag":tag,"wcells":sorted(WS.items()),"wj":wj,
                             "gap":gap,"bucket":wall_bucket(r,W,C,mode),
                             "parts":fmt_parts(r)})
        if wi%50==0: print("   ...wall %d/%d  %.0fs"%(wi,len(walls),time.time()-t0), flush=True)
    c=Counter(r["bucket"] for r in rows)
    print("  N=%d  [%.0fs]"%(len(rows),time.time()-t0))
    for k,v in c.most_common(): print("    %-22s %5d"%(k,v))
    for tg in ("DEAD","BAL","OSC"):
        cc=Counter(r["bucket"] for r in rows if r["tag"]==tg)
        if cc: print("    by wall type %-4s: %s"%(tg,dict(cc)))
    for sp in ("FAN-OUT","REFLECT","TRANSPARENT","WALL-DESTROYED"):
        ex=[r for r in rows if r["bucket"]==sp]
        for r in ex[:5]: print("    *** %s wall=%s wj=%d gap=%d -> %s"%(sp,r["wcells"],r["wj"],r["gap"],r["parts"]))
    json.dump(rows, open("ballistic_walls_trip_%s.json"%mode,"w"))
