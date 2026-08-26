#!/usr/bin/env python3
"""Task 5: gallery of the five most charismatic specimens, with seeds,
certificates, and ASCII spacetime evidence.  Writes gallery.txt."""
from engine2d import (to_state, step_p, render, tparse, tname, sizeof,
                      decode_state, verify_recurrence, GID, state_hw, bits, enc)

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)

def run(S, T):
    for _ in range(T):
        S = step_p(S)
    return S

def hdr(n, name, seed, cert):
    log("=" * 74)
    log(f"SPECIMEN {n}: {name}")
    log(f"  seed: {seed}")
    log(f"  certificate: {cert}")
    log("-" * 74)

# ---- 1. THE JUBILEE CODE ---------------------------------------------------
spec = [((-1, 0), tparse("ESN")), ((-1, 1), tparse("SNS")), ((0, 1), tparse("WNE"))]
hdr(1, "THE JUBILEE CODE (bounded-size aperiodic creeper; universal holdout attractor)",
    "(-1,0)ESN  (-1,1)SNS  (0,1)WNE   [3 laws; equivalent machines arise from "
    "hundreds of 2-4 law seeds]",
    "no recurrence in 300,000 fully-hashed steps; quiescent size ~26, max 771; "
    "frontier = 3*2^m after avalanche epochs t = 2^k  (hw ~ 1.5*sqrt(t))")
S = to_state(spec)
log("anatomy (A=ESN anchor, B=WNE chain, C=SNS pump), t=48:")
log(render(run(to_state(spec), 48), maxw=76))
log("")
log("the avalanche clock: last frontier advances in a 300k-step run:")
log("  ... 130961..131072 (dense burst to hw=767), then silence, then a single")
log("  advance at t = 262144 = 2^18 exactly (hw -> 768).  Size during t=131020..131080:")
S = to_state(spec)
szs = []
for t in range(131100):
    if t >= 131020:
        szs.append(sizeof(S))
    S = step_p(S)
log("  " + " ".join(map(str, szs[:60])))
log("  (a carry avalanche sweeps the whole 767-cell extent and collapses)")

# ---- 2. THE APPELLATE COLUMN ----------------------------------------------
spec2 = [((0, 0), tparse("OEN"))]
hdr(2, "THE APPELLATE COLUMN (perpendicular colonizer, single law OEN)",
    "(0,0)OEN  -- a=self, b=East, c=North: growth direction ORTHOGONAL to guard;"
    " impossible in 1D",
    "exact law size(t) = 2^popcount(t); support = Pascal-mod-2 column, height t;"
    " unbounded, never extinct (origin persists), size dips to 2 at t = 2^k")
log("spacetime of the column (x=0 line shown horizontally, t downward 0..31):")
S = to_state(spec2)
for t in range(32):
    cells = {y for x, y, m in decode_state(S)}
    log("  t=%2d |%s| size %d" % (t, "".join("#" if y in cells else "." for y in range(32)), len(cells)))
    S = step_p(S)
log("  (Sierpinski triangle: the column IS Pascal's triangle mod 2)")

# ---- 3. THE PINWHEEL ORDINANCE (half-turn) --------------------------------
spec3 = [((0, -1), 82), ((1, -1), 82), ((1, 0), 111)]
hdr(3, "THE PINWHEEL ORDINANCE (half-turn rotor: state maps to its own 180-deg "
       "rotation each step)",
    f"(0,-1){tname(82)}  (1,-1){tname(82)}  (1,0){tname(111)}   "
    "[NEW and SWE are a 180-degree type pair]",
    "VERIFIED: S_1 == rot180(S_0) + (2,-1); hence period 2 overall.  "
    f"engine check: {verify_recurrence(spec3, 'p', 0, 1, GID[(2,0)], (2,-1))}")
S = to_state(spec3)
for t in range(4):
    log(f" t={t}  (A=NEW, B=SWE)")
    for ln in render(S, maxw=30).splitlines():
        log("   " + ln)
    S = step_p(S)
log(" THEOREM: quarter-turn pinwheels need >= 4 rotation-closed types; none found")
log(" in 48,000 C4-closed seeds.  Half-turn rotors, by contrast, are a family:")
log(" a targeted {k,k,R2k} hunt (hunt_rot3.py) finds 238 / 30,000 (0.8%), all")
log(" 3-law period-1-mod-rot180 flip-flops, across many type pairs")
log(" (OEW/OWE, NSN/SNS, EWE/WEW, ONS/OSN, ESN/WNS, ...).")

# ---- 4. THE RIGHT-OF-WAY DOCTRINE -----------------------------------------
hdr(4, "THE RIGHT-OF-WAY DOCTRINE (crossing rays: priority by arrival time)",
    "OEE ray from (0,0) + ONN column from (6,-6) (tie)  vs  from (6,-3) (column first)",
    "deterministic crossing law: tie -> mutual transparency (both fronts pass "
    "through the shared cell); prior occupancy -> permanent weld; a blinking "
    "Pascal-trail gate delays a crossing ray 0..3 steps depending on phase")
spec4a = [((0, 0), tparse("OEE")), ((6, -6), tparse("ONN"))]
spec4b = [((0, 0), tparse("OEE")), ((6, -3), tparse("ONN"))]
log(" tie (seeded equidistant), t=12 -- the ray sails through the crossing:")
for ln in render(run(to_state(spec4a), 12), maxw=40).splitlines():
    log("   " + ln)
log(" column arrives first, t=12 -- the ray welds at x=5 forever:")
for ln in render(run(to_state(spec4b), 12), maxw=40).splitlines():
    log("   " + ln)

# ---- 5. THE TWO-CHAMBER AMENDMENT (cross-amendment teaser) ----------------
hdr(5, "THE TWO-CHAMBER AMENDMENT (cross-amendment: parity and OR finally split;"
       " the plane opens diagonally)",
    "universe A=OSS->A, B=OES->A, both at (-1,0)  |  and relay A=ONE->B, B=OEN->A"
    " seeded A@(0,0)",
    "with target-kind extension, two authors can hit one (cell,kind): "
    "20/4000 random seeds diverge between parity and OR; relay seeds walk "
    "DIAGONAL staircases -- a direction unreachable by own-kind laws (whose "
    "c-offsets are axis-aligned) -- though support stays 1-dimensional")
log(" divergence witness: A=OSS->A + B=OES->A, laws A,B stacked at (-1,0):")
log("   parity: both authors toggle A at (-1,-1); toggles cancel -> FIXED at t=0")
log("   OR:     the double enactment passes -> sustained colonization, +1 law/step")
log("           (verified 3000 steps: size 2 -> 3001)")
log(" relay staircase (A=ONE->B, B=OEN->A from one A law): EVER-OCCUPIED set")
log(" through t=48 -- own-kind Theorem 3 confines support to AXIS rays; the")
log(" cross-amendment relay escapes into a diagonal (still 1-D):")
from xamend import np_xrun
import numpy as np
ever = None
for tt in range(49):
    A, B, s, R = np_xrun([((0, 0), 0)], (tparse("ONE"), 1, tparse("OEN"), 1), tt,
                         sem="p", R=54)
    occ = A | B
    if ever is None:
        ever = occ
    else:
        ever = ever | occ
Sd = {}
for i, j in np.argwhere(ever):
    Sd[enc(int(i)-R, int(j)-R)] = 1
for ln in render(Sd, legend={0: "#"}, maxw=56, maxh=52).splitlines():
    log("   " + ln)

with open("gallery.txt", "w") as f:
    f.write("\n".join(OUT))
print("\n".join(OUT[:4]))
print(f"... wrote gallery.txt ({len(OUT)} lines)")
