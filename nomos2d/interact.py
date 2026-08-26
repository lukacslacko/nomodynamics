#!/usr/bin/env python3
"""Task 4: interaction teaser experiments.  Writes interact_report.txt.

I1 head-on collision of two colonizer rays (parity of gap matters?)
I2 crossing rays: does a ray pass through another ray's trail?
I3 ray arriving at a blinking fractal column: gating/refraction
I4 self-eroding block (EWO) + interior point defect ("loophole")
I5 capped-row constitution: inert cap pacifies a live row; remove cap
"""
from engine2d import (to_state, step_p, tname, tparse, render, sizeof,
                      decode_state, enc, bits)

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)

def run(S, T):
    for _ in range(T):
        S = step_p(S)
    return S

def snap(S, title, **kw):
    log(f"-- {title} (size {sizeof(S)})")
    log(render(S, **kw))

def front_x(S):
    return max(x for x, y, m in decode_state(S))

# ---------------- I1: head-on ray collision --------------------------------
log("=" * 72)
log("I1. HEAD-ON RAY COLLISION: OEE ray east from (0,0) vs OWW ray west from (d,0)")
for d in (10, 11):
    spec = [((0, 0), tparse("OEE")), ((d, 0), tparse("OWW"))]
    S = to_state(spec)
    hist = []
    for t in range(40):
        S = step_p(S)
        hist.append(sizeof(S))
    log(f" gap d={d}: sizes t=1..40: {hist[:14]} ... final {hist[-1]}")
    snap(run(to_state(spec), 30), f"d={d} at t=30")

# ---------------- I2: crossing rays ---------------------------------------
log("=" * 72)
log("I2. CROSSING RAYS: OEE east along y=0; ONN north along x=6 from (6,-6)")
spec = [((0, 0), tparse("OEE")), ((6, -6), tparse("ONN"))]
S = to_state(spec)
for t in (4, 6, 8, 12, 20, 30):
    log(f" t={t}: east-front x = {max(x for x,y,m in decode_state(run(to_state(spec), t)) if y == 0)}")
snap(run(to_state(spec), 24), "t=24 (A=OEE, B=ONN)")

log("")
log("I2b. right-of-way: ONN column seeded at (6,-3) occupies (6,0) at t=3,")
log("     BEFORE the ray front arrives (t=5).  Does the ray weld?")
spec = [((0, 0), tparse("OEE")), ((6, -3), tparse("ONN"))]
for t in (4, 5, 6, 8, 16, 30):
    st = run(to_state(spec), t)
    xe = [x for x, y, m in decode_state(st) if y == 0]
    log(f" t={t}: east-front x = {max(xe)}")
snap(run(to_state(spec), 20), "t=20 (A=OEE welds against B=ONN trail)")

log("")
log("I2c. ray vs BLINKING Pascal column: OEN at (6,-6) grows north, its cell")
log("     (6,0) blinks per Pascal parity; the OEE ray must pass the gate.")
spec = [((0, 0), tparse("OEE")), ((6, -6), tparse("OEN"))]
front = []
for t in range(0, 46):
    st = run(to_state(spec), t)
    xe = [x for x, y, m in decode_state(st) if y == 0]
    front.append(max(xe))
log(" east-front x(t), t=0..45:")
log("   " + " ".join(str(v) for v in front))
snap(run(to_state(spec), 40), "t=40 (A=OEE ray, B=OEN blinking column)")

# ---------------- I3: gate timing ------------------------------------------
log("=" * 72)
log("I3. RAY THROUGH A PERIOD-2 GATE: OEW blinker at (8,0) in the path of OEE ray")
spec = [((0, 0), tparse("OEE")), ((8, 0), tparse("OEW"))]
for t in (6, 7, 8, 9, 10, 12, 16, 24):
    st = run(to_state(spec), t)
    xs = sorted((x, tname(k)) for x, y, m in decode_state(st) for k in bits(m))
    log(f" t={t}: cells {xs}")
snap(run(to_state(spec), 24), "t=24")

# ---------------- I4: eroding block + loophole -----------------------------
log("=" * 72)
log("I4. SELF-ERODING BLOCK: 12x7 block of EWO (active iff east occ & west empty; repeals self)")
blk = [((x, y), tparse("EWO")) for x in range(12) for y in range(7)]
S = to_state(blk)
snap(S, "t=0")
snap(run(to_state(blk), 4), "t=4 (west edge erodes)")
snap(run(to_state(blk), 9), "t=9")
log("")
log("I4b. same block with one interior law deleted at (6,3) -- a point defect")
blk2 = [b for b in blk if b[0] != (6, 3)]
S = to_state(blk2)
for t in (2, 4, 6, 8):
    snap(run(to_state(blk2), t), f"defect t={t}")

# ---------------- I5: capped row constitution ------------------------------
log("=" * 72)
log("I5. ENTRENCHMENT: row x=0..9 of OES (active iff east empty; enacts south),")
log("    capped by one INERT law NNO at (10,0).  Stable.  Then repeal the cap.")
row = [((x, 0), tparse("OES")) for x in range(10)]
cap = [((10, 0), tparse("NNO"))]
S = to_state(row + cap)
S1 = step_p(S)
log(f" with cap: step changes state? {S1 is not S}  (size {sizeof(S)} -> {sizeof(S1)})")
S = to_state(row)   # cap repealed
snap(S, "cap removed, t=0")
for t in (1, 2, 3, 5, 8, 12):
    snap(run(to_state(row), t), f"t={t}")

with open("interact_report.txt", "w") as f:
    f.write("\n".join(OUT))
print("\nwrote interact_report.txt")
