"""T3 (cont.): NOT, the AND attempt, OR, XOR.  All in MIRROR / parity.

CONVENTIONS.
  A RIGHT WIRE carries a bit as the presence/absence of the (5,+2) glider on a
  fixed launch cell-range at t=0.  A LEFT WIRE carries a bit as the (5,-2)
  glider.  A CONSTANT is a glider planted in the initial condition as part of
  the gadget geometry (not an input).
  A gate is CERTIFIED when all 2^k input cases run through the SAME geometry
  and the output port -- a fixed (time, cell-window) -- holds the right bit,
  the bit being read by verify_glider() on the window content.
"""
import sys
from collections import Counter
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *
from ballistic_collide import clusters

MIR = Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)])
CELLS = [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21]
R0 = state_of([(c, k) for c in CELLS for k in (0, 1)]); R0 = shift(R0, -min(R0))
L0 = mirror_state(R0); L0 = shift(L0, -min(L0))


def R(at):  return shift(R0, at - min(R0))
def L(at):  return shift(L0, at - min(L0))
def run_to(S, T):
    S = dict(S)
    for _ in range(T):
        S = step(S, MIR, "parity")
    return S
def win(S, lo, hi): return {c: m for c, m in S.items() if lo <= c <= hi}
def bitR(S, lo, hi):
    w = win(S, lo, hi); return int(bool(w) and verify_glider(w, MIR, 5, 2))
def bitL(S, lo, hi):
    w = win(S, lo, hi); return int(bool(w) and verify_glider(w, MIR, 5, -2))
def free_gliders(S):
    """count the certified free gliders anywhere in S (either polarity)."""
    n = 0
    for cl in clusters(S, 3):
        if verify_glider(cl, MIR, 5, 2) or verify_glider(cl, MIR, 5, -2):
            n += 1
    return n


print("=" * 78)
print("GATE 3  NOT  (cross-polarity; one planted constant)")
print("=" * 78)
print("""  geometry:  input A = (5,+2) right-mover launched on cells 0..19
             CONSTANT K = (5,-2) left-mover planted on cells 40..59
  output port: LEFT, cells [-400,-5] at T=200; bit = a certified (5,-2) glider.
  K alone reaches cells -40..-21;  A+K arrest as BALANCED debris on 16..43.""")
rows = []
for a in (0, 1):
    S = union(*(([R(0)] if a else []) + [L(40)]))
    ST = run_to(S, 200)
    o = bitL(ST, -400, -5)
    rows.append((a, o))
    print("   A=%d -> out=%d    state cells %d..%d card %d"
          % (a, o, min(ST), max(ST), card(ST)))
print("   TRUTH TABLE out = NOT A :", all(o == 1 - a for a, o in rows), rows)
print("   (the output is a LEFT-moving wire; NOT flips polarity.)")

print()
print("=" * 78)
print("GATE 4  XOR  (two travelling signals, GLOBAL free-glider readout)")
print("=" * 78)
print("""  geometry: A = (5,+2) on 0..19  (right wire)
            B = (5,-2) on 40..59 (left  wire)
  output: the NUMBER of certified free gliders anywhere in the universe at
  T=200.  Readout is NON-LOCAL: it is not a single spatial port.  Marked as a
  weaker gate for exactly that reason.""")
rows = []
for a in (0, 1):
    for b in (0, 1):
        P = ([R(0)] if a else []) + ([L(40)] if b else [])
        S = union(*P) if P else {}
        ST = run_to(S, 200) if S else {}
        n = free_gliders(ST) if ST else 0
        rows.append((a, b, n))
        print("   A=%d B=%d -> free gliders = %d" % (a, b, n))
print("   TRUTH TABLE  #free = A XOR B :",
      all(n == (a ^ b) for a, b, n in rows), rows)

print()
print("=" * 78)
print("GATE 5 ATTEMPT  AND(A,B) for two RIGHT wires -- WHY IT FAILS")
print("=" * 78)
print("""  Plan: stage 1 turns A into the left wire NOT-A (gate 3); stage 2 feeds B
  into NOT-A, so the right port of stage 2 should hold B AND NOT(NOT A) = A&B.
  geometry: A on 0..19; CONSTANT K = (5,-2) on 40..59;  B on -200..-181.
  read the RIGHT port at T=900, cells [200,5000].""")
rows = []
for a in (0, 1):
    for b in (0, 1):
        P = ([R(0)] if a else []) + [L(40)] + ([R(-200)] if b else [])
        S = union(*P)
        ST = run_to(S, 900)
        o = bitR(ST, 200, 5000)
        rows.append((a, b, o))
        cl = clusters(ST, 3)
        print("   A=%d B=%d -> out=%d   clusters: %s" % (a, b, o,
              [(min(x), max(x), card(x),
                "G+2" if verify_glider(x, MIR, 5, 2) else
                ("G-2" if verify_glider(x, MIR, 5, -2) else "stat"))
               for x in cl]))
print("   TRUTH TABLE  out = A AND B :", all(o == (a & b) for a, b, o in rows),
      rows)
print("""   FAILURE MODE (machine-visible above): when A=1 the stage-1 collision
   leaves BALANCED DEBRIS standing on B's lane.  Every glider-vs-debris run in
   the T3 debris box (4375 runs) is ABSORBED, so B dies on the debris and
   A=1,B=1 gives 0 instead of 1.  In one spatial dimension there is no second
   lane to route B around the debris, and no certified transparent obstacle.""")

print()
print("=" * 78)
print("GATE 6 ATTEMPT  OR(A,B) -- two wires merging into one")
print("=" * 78)
print("""  OR needs two distinct input carriers to produce one output carrier on a
  single port.  In MIRROR the only two carriers that can meet are the two
  polarities, and the head-on box (1025 runs, T2) is 100%% ARREST -- so the
  single-port output of any head-on gadget is A AND NOT B (right) or
  B AND NOT A (left), never A OR B.  Machine check of the natural attempt
  (read EITHER port and OR the two bits):""")
rows = []
for a in (0, 1):
    for b in (0, 1):
        P = ([R(0)] if a else []) + ([L(40)] if b else [])
        S = union(*P) if P else {}
        ST = run_to(S, 200) if S else {}
        o = (bitR(ST, 60, 4000) | bitL(ST, -4000, -5)) if ST else 0
        rows.append((a, b, o))
        print("   A=%d B=%d -> right|left = %d   (A OR B would be %d)"
              % (a, b, o, a | b))
print("   TRUTH TABLE out = A OR B :", all(o == (a | b) for a, b, o in rows))
print("   out = A XOR B :", all(o == (a ^ b) for a, b, o in rows),
      "  <-- the two-port OR is in fact XOR")
