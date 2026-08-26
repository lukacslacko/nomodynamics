"""T3 GATE 1b: the AND-NOT cascade (A AND NOT B) AND NOT C, 3 inputs, 8 cases."""
import sys
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/computation')
from ballistic_lib import *
MIR = Const([(0,1,-1),(0,-1,1)], [(0,1),(0,1)])
CELLS=[2,3,4,6,7,8,9,10,12,13,14,16,18,19,20,21]
R0=state_of([(c,k) for c in CELLS for k in (0,1)]); R0=shift(R0,-min(R0))
L0=mirror_state(R0); L0=shift(L0,-min(L0))
A0=dict(R0); B0=shift(L0,40-min(L0)); C0=shift(L0,300-min(L0))
def run_to(S,T):
    for _ in range(T): S=step(S,MIR,'parity')
    return S
def win(S,lo,hi): return {c:m for c,m in S.items() if lo<=c<=hi}
print("GATE 1b  CASCADE  (A AND NOT B) AND NOT C")
print("  MIRROR/parity.  A=(5,+2) on 0..19;  B=(5,-2) on 40..59;")
print("  C=(5,-2) on 300..319.   OBSERVE T=800, RIGHT PORT = cells [200,4000].")
print("  A alone at T=800 is on cells 320..339 (2 cells per 5 steps).")
rows=[]
for a in (0,1):
  for b in (0,1):
    for c in (0,1):
      P=([A0] if a else [])+([B0] if b else [])+([C0] if c else [])
      S=union(*P) if P else {}
      ST=run_to(dict(S),800) if S else {}
      w=win(ST,200,4000)
      o=int(bool(w) and verify_glider(w,MIR,5,2))
      rows.append((a,b,c,o))
      print("  A=%d B=%d C=%d -> %d   %s"%(a,b,c,o,
        ("cells %d..%d card %d"%(min(ST),max(ST),card(ST))) if ST else "empty"))
ok=all(o==(a and not b and not c) for a,b,c,o in rows)
print("\n  TRUTH TABLE  out = A AND NOT B AND NOT C :",ok)
print("  rows:",rows)
