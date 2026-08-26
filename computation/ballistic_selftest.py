"""POSITIVE CONTROLS for ballistic_collide: prove the detector can SEE the
buckets that came back empty, so the zeros in BALLISTIC.md are results and not
artefacts of the machinery."""
import sys
sys.path.insert(0,'/Users/lukacs/claude/math/program/phase6/computation')
from ballistic_lib import *
from ballistic_collide import resolve, sep_forever, bucket, fmt_parts, clusters

MIR=Const([(0,1,-1),(0,-1,1)],[(0,1),(0,1)])
CE=[2,3,4,6,7,8,9,10,12,13,14,16,18,19,20,21]
R=state_of([(c,k) for c in CE for k in (0,1)]); R=shift(R,-min(R))
L=mirror_state(R); L=shift(L,-min(L))
ok=[]

# 1. TRANSPARENCY detector: two certified gliders MOVING APART must be
#    certified as a 2-packet SPLIT and bucketed TRANSPARENCY.
comps=[shift(L,0), shift(R,60)]
f,a,certs=sep_forever(comps,MIR,'parity',N=140)
res={"out":"SPLIT","parts":[(c["kind"],c.get("period",0),c.get("displacement",0),
      c.get("card",0)) for c in certs],"t_res":0,"forever":a}
b=bucket(res,1,1)
print("1 TRANSPARENCY control  sep=%s forever=%s parts=%s bucket=%s"
      %(f,a,fmt_parts(res),b)); ok.append(f and a and b=="TRANSPARENCY")

# 2. FAN-OUT detector: three gliders spreading (1 left, 2 right at different
#    speeds) declared with only 1 input must bucket FAN-OUT.
S12={c:3 for c in [1,2,3,4,5,7,9,10,11,13,15,17,19,21,23,26,28,30,31,32,33,34,
                   36,38,40,42,43,44,46,47,48,49,50,51,52,53]}
S12=shift(S12,-min(S12))
comps=[shift(L,0), shift(S12,200), shift(R,400)]
f,a,certs=sep_forever(comps,MIR,'parity',N=160)
res={"out":"SPLIT","parts":[(c["kind"],c.get("period",0),c.get("displacement",0),
      c.get("card",0)) for c in certs],"t_res":0,"forever":a}
print("2 FAN-OUT control       sep=%s forever=%s parts=%s bucket=%s"
      %(f,a,fmt_parts(res),bucket(res,1,0)))
ok.append(f and bucket(res,1,0)=="FAN-OUT")

# 3. ABSORPTION detector: one surviving glider + one stationary wall.
W=state_of([(0,0),(0,1),(1,0)])
T=Const([(0,-1,1),(0,-1,0)],[(0,1),(0,1)])
G=state_of([(0,0),(0,1)])
comps=[shift(W,0), shift(G,40)]
f,a,certs=sep_forever(comps,T,'parity',N=120)
res={"out":"SPLIT","parts":[(c["kind"],c.get("period",0),c.get("displacement",0),
      c.get("card",0)) for c in certs],"t_res":0,"forever":a}
print("3 ABSORPTION control    sep=%s parts=%s bucket=%s"
      %(f,fmt_parts(res),bucket(res,1,1)))
ok.append(f and bucket(res,1,1)=="ABSORPTION")

# 4. REFLECTION detector: input = 1 right-mover, output = 1 left-mover.
res={"out":"SINGLE","parts":[(GLIDER,5,-2,32)],"t_res":0,"forever":True}
print("4 REFLECTION control    bucket=%s"%bucket(res,0,1))
ok.append(bucket(res,0,1)=="REFLECTION")

# 5. ANNIHILATION / ARREST / EXPLOSION labels
print("5 ANNIHILATION control  bucket=%s"%bucket(
    {"out":"SINGLE","parts":[(EXTINCT,0,0,0)],"t_res":0,"forever":True},1,1))
print("  ARREST control        bucket=%s"%bucket(
    {"out":"SINGLE","parts":[(BALANCED,1,0,24)],"t_res":0,"forever":True},1,1))
print("  EXPLOSION control     bucket=%s"%bucket(
    {"out":"GROWING","parts":[],"t_res":9,"forever":False},1,1))
ok.append(bucket({"out":"SINGLE","parts":[(EXTINCT,0,0,0)],"t_res":0,
                  "forever":True},1,1)=="ANNIHILATION")

# 6. the separation lemma itself: on a certified split, the union really does
#    evolve as the union, step by step, for 200 steps.
A,B=shift(L,0), shift(R,60)
U=union(A,B); a1,b1=dict(A),dict(B)
good=True
for t in range(200):
    U=step(U,MIR,'parity'); a1=step(a1,MIR,'parity'); b1=step(b1,MIR,'parity')
    if U!=union(a1,b1): good=False; print("   lemma broke at t=%d"%t); break
print("6 separation lemma holds for 200 steps on the control:",good)
ok.append(good)
print("\nPOSITIVE CONTROLS PASSED: %d/%d"%(sum(ok),len(ok)))
