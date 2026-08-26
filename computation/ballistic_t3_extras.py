"""Extras: spacetime of the TANDEM-1 wall DELETE, and glider-vs-GUN."""
import sys
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/computation')
from ballistic_lib import *
from ballistic_collide import resolve, fmt_parts, clusters
from collections import Counter

T=Const([(0,-1,1),(0,-1,0)],[(0,1),(0,1)])
G=state_of([(0,0),(0,1)]); W=state_of([(8,0),(8,1),(9,0)])
print("TANDEM-1 glider (cell 0) vs period-2 wall at cells 8,9  --  parity")
print("  wall alone:", classify(W,T,'parity',max_steps=20)['kind'],
      classify(W,T,'parity',max_steps=20).get('period'))
for i,r in enumerate(spacetime(union(G,W),T,16,'parity',lo=-1,hi=16)):
    print("   t=%2d  %s"%(i,r))
res=resolve(union(G,W),T,'parity')
print("  outcome:",fmt_parts(res),"  <- the wall is CONSUMED down to a card-1")
print("     period-2 oscillator; it is NOT restored, so the gate is one-shot.")

print()
print("GUN universe: does the immortal kind-2 source absorb an incoming glider?")
GU=Const([(0,1,0),(0,1,1),(0,1,0)],[(0,1)]*3)
gun=state_of([(0,2)]); gl=state_of([(0,0),(0,1)])
print("  gun alone |S_t|, t=0..11:", end=' ')
S=dict(gun); out=[]
for _ in range(12): out.append(card(S)); S=step(S,GU,'parity')
print(out, " (= 2*floor(t/2)+3 for t>=1)")
cnt=Counter(); N=0
for gp in range(1):
  for gap in range(0,31):
    S=union(shift(gl,-1-gap-0), gun)
    r=resolve(S,GU,'parity',T_max=200,max_card=300,max_span=500)
    N+=1; cnt[r['out']+':'+fmt_parts(r)]+=1
print("  glider fired into the gun from the left, gap 0..30 (N=%d):"%N)
for k,v in cnt.most_common(6): print("     %-40s %d"%(k,v))
