"""T3: the gate table, ballistic sector.  Every gate is stated as a TRUTH
TABLE and machine-checked by running all 2^k input combinations through the
SAME gadget geometry and reading the output at a FIXED (time, window)."""
import sys, json, itertools
from collections import Counter
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *
from ballistic_collide import resolve, bucket, fmt_parts, clusters, sep_forever

MIR = Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)])
CELLS = [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21]
R0 = shift(state_of([(c, k) for c in CELLS for k in (0, 1)]), 0)
R0 = shift(R0, -min(R0))                       # cells 0..19, p=5, d=+2
L0 = mirror_state(R0); L0 = shift(L0, -min(L0))  # cells 0..19, p=5, d=-2
assert verify_glider(R0, MIR, 5, 2) and verify_glider(L0, MIR, 5, -2)

TANDEM = Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)])
TG = state_of([(0, 0), (0, 1)])
assert verify_glider(TG, TANDEM, 1, 1)


def window(S, lo, hi):
    return {c: m for c, m in S.items() if lo <= c <= hi}


def run_to(S, C, mode, T):
    S = dict(S)
    for _ in range(T):
        S = step(S, C, mode)
    return S


def is_glider(W, C, p, d, mode="parity"):
    return bool(W) and verify_glider(W, C, p, d, mode)


print("=" * 78)
print("GATE 1  MIRROR AND-NOT  (DELETE / INHIBIT) -- two travelling signals")
print("=" * 78)
print("""  universe MIRROR = Const([(0,1,-1),(0,-1,1)], targets=[(0,1),(0,1)]),
  mode 'parity'.
  A = the (p=5,d=+2) right-mover on cells 0..19,  phase 0
  B = the (p=5,d=-2) left-mover  on cells 40..59, phase 0   (gap 20)
  seeds:  A = state_of([(c,k) for c in [0,1,2,4,5,6,7,8,10,11,12,14,16,17,18,19]
                              for k in (0,1)])
          B = state_of([(c,k) for c in [40,41,42,43,45,47,48,49,51,52,53,54,55,
                              57,58,59] for k in (0,1)])
  OBSERVE at T=200.  A alone -> cells 80..99;  B alone -> cells -40..-21;
  A+B -> frozen BALANCED debris on cells 16..43 (card 24).
  RIGHT PORT = cells [60,400]   (bit 1 iff a certified (5,+2) glider sits there)
  LEFT  PORT = cells [-400,-5]  (bit 1 iff a certified (5,-2) glider sits there)
""")
A0 = dict(R0)
B0 = shift(L0, max(A0) + 1 + 20 - min(L0))
print("  A cells:", sorted(A0), "\n  B cells:", sorted(B0))
T_OBS = 200
rowsR, rowsL = [], []
for a in (0, 1):
    for b in (0, 1):
        S = union(*( [A0] if a else [] ) + ( [B0] if b else [] )) if (a or b) else {}
        ST = run_to(S, MIR, "parity", T_OBS) if S else {}
        wr = window(ST, 60, 400)
        wl = window(ST, -400, -5)
        orr = int(is_glider(wr, MIR, 5, 2))
        orl = int(is_glider(wl, MIR, 5, -2))
        rowsR.append((a, b, orr)); rowsL.append((a, b, orl))
        print("  A=%d B=%d  T=%d  state=%s  RIGHT=%d LEFT=%d"
              % (a, b, T_OBS,
                 ("cells %d..%d card %d" % (min(ST), max(ST), card(ST)))
                 if ST else "empty", orr, orl))
okR = all(o == (a and not b) for a, b, o in rowsR)
okL = all(o == (b and not a) for a, b, o in rowsL)
print("\n  TRUTH TABLE  RIGHT PORT = A AND NOT B :", okR, rowsR)
print("  TRUTH TABLE  LEFT  PORT = B AND NOT A :", okL, rowsL)
print("  ==> one gadget, two ports, both AND-NOTs.  CERTIFIED." if okR and okL
      else "  ==> FAILED")

print()
print("=" * 78)
print("GATE 1b  CASCADE: (A AND NOT B) AND NOT C   -- 3 inputs, 8 cases")
print("=" * 78)
print("""  Same universe.  A on 0..19 (right-mover), B on 40..59 (left-mover),
  C on 300..319 (left-mover).  Read the RIGHT PORT at T=800, cells [200,4000].
  A alone at T=800 sits on cells 320..339 (2 cells per 5 steps); the A&C
  debris stops at 146..173 and the A&B debris at 16..43, both left of 200.""")
C0 = shift(L0, 300 - min(L0))
rows3 = []
for a in (0, 1):
    for b in (0, 1):
        for c in (0, 1):
            parts = ([A0] if a else []) + ([B0] if b else []) + ([C0] if c else [])
            S = union(*parts) if parts else {}
            ST = run_to(S, MIR, "parity", 800) if S else {}
            wr = window(ST, 200, 4000)
            o = int(is_glider(wr, MIR, 5, 2))
            rows3.append((a, b, c, o))
            print("  A=%d B=%d C=%d -> %d   %s" % (a, b, c, o,
                  ("cells %d..%d card %d" % (min(ST), max(ST), card(ST)))
                  if ST else "empty"))
ok3 = all(o == (a and not b and not c) for a, b, c, o in rows3)
print("\n  TRUTH TABLE  out = A AND NOT B AND NOT C :", ok3)

print()
print("=" * 78)
print("GATE 2  TANDEM-1 WALL-DELETE  (one travelling signal, STATIC control)")
print("=" * 78)
print("""  universe TANDEM-1 = Const([(0,-1,1),(0,-1,0)], targets=[(0,1),(0,1)]).
  A = the (p=1,d=+1) glider, both kinds in cell 0: state_of([(0,0),(0,1)])
  W = the period-2 wall  state_of([(20,0),(20,1),(21,0)])
  OBSERVE T=40, window cells [30,60].  A alone sits at cell 40.""")
W1 = state_of([(20, 0), (20, 1), (21, 0)])
rw = classify(W1, TANDEM, "parity", max_steps=40)
print("  wall certificate:", rw["kind"], "period", rw.get("period"),
      " (it never translates)")
rows4 = []
for a in (0, 1):
    for w in (0, 1):
        parts = ([TG] if a else []) + ([W1] if w else [])
        S = union(*parts) if parts else {}
        ST = run_to(S, TANDEM, "parity", 40) if S else {}
        win = window(ST, 30, 60)
        o = int(is_glider(win, TANDEM, 1, 1))
        rows4.append((a, w, o))
        print("  A=%d W=%d -> out=%d  port=%s" % (a, w, o, sorted(win.items())))
print("\n  TRUTH TABLE out = A AND NOT W :",
      all(o == (a and not w) for a, w, o in rows4), rows4)
print("  HONEST NOTE: W is a static control, not a travelling signal, so this")
print("  gate cannot be cascaded -- no gate output can drive W.")

print()
print("=" * 78)
print("REUSABILITY / DEBRIS: does the AND-NOT gate survive a second shot?")
print("=" * 78)
print("  Fire A, then a second right-mover A2 far behind it, against one B.")
A2 = shift(R0, -200)                # 200 cells behind A
for b in (0, 1):
    parts = [A0, A2] + ([B0] if b else [])
    S = union(*parts)
    ST = run_to(S, MIR, "parity", 900)
    cl = clusters(ST, 3)
    print("  B=%d -> %d clusters:" % (b, len(cl)),
          [(min(x), max(x), card(x),
            "G+2" if verify_glider(x, MIR, 5, 2) else
            ("G-2" if verify_glider(x, MIR, 5, -2) else "stat"))
           for x in cl])

print()
print("=" * 78)
print("FAN-OUT / DUPLICATE and REFLECT hunt: glider vs the ARREST DEBRIS")
print("=" * 78)
print("""  BOX: the 8 distinct debris signatures produced by the T2 head-on sweep
  are re-used as obstacles; a fresh (5,+2) right-mover is fired into each from
  the left at every phase 0..4 and every gap 0..24  (8 x 5 x 25 = 1000 runs).""")
dbg = []
seen = set()
for i in range(5):
    Ai = orbit(R0, MIR, "parity", 5)[i]
    for j in range(5):
        Bj = orbit(L0, MIR, "parity", 5)[j]
        for gap in (0, 3, 7, 11):
            Bs = shift(Bj, max(Ai) + 1 + gap - min(Bj))
            S = union(Ai, Bs)
            ST = run_to(S, MIR, "parity", 300)
            key = (card(ST), span(ST), tuple(sorted(
                (c - min(ST), m) for c, m in ST.items())))
            if key[2] in seen:
                continue
            seen.add(key[2])
            dbg.append(shift(ST, -min(ST)))
print("  distinct debris states harvested:", len(dbg))
cnt = Counter()
hits = []
NRUN = 0
for wi, D in enumerate(dbg[:40]):
    for gi in range(5):
        A = orbit(R0, MIR, "parity", 5)[gi]
        for gap in range(0, 25):
            Ash = shift(A, min(D) - 1 - gap - max(A))
            S = union(Ash, D)
            if card(S) != card(Ash) + card(D):
                continue
            NRUN += 1
            res = resolve(S, MIR, "parity", T_max=300, N_sep=110,
                          max_card=400, max_span=900)
            parts = res["parts"]
            movers = [p for p in parts if p[0] == GLIDER]
            right = [p for p in movers if p[2] > 0]
            left = [p for p in movers if p[2] < 0]
            if res["out"] in ("GROWING", "UNRESOLVED"):
                b = "EXPLOSION" if res["out"] == "GROWING" else "UNRESOLVED"
            elif len(movers) >= 2:
                b = "FAN-OUT"
            elif left:
                b = "REFLECT"
            elif right:
                b = "TRANSPARENT"
            elif not parts or all(p[0] == EXTINCT for p in parts):
                b = "MUTUAL-ANNIHILATION"
            else:
                b = "ABSORBED"
            cnt[b] += 1
            if b in ("FAN-OUT", "REFLECT", "TRANSPARENT"):
                hits.append((wi, gi, gap, b, fmt_parts(res)))
print("  runs:", NRUN, " debris used:", min(len(dbg), 40))
for k, v in cnt.most_common():
    print("    %-22s %5d" % (k, v))
for h in hits[:20]:
    print("    *** debris=%d phase=%d gap=%d -> %s  %s" % h)
