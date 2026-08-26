"""T0: verify the five specimens reproduce; correct seeds by small search."""
import sys
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *

def report(name, C, seed, mode, want=None):
    S = state_of(seed)
    res = classify(S, C, mode, max_steps=400, max_card=400, max_span=400)
    line = "%-10s %-12s seed=%-26s -> %s" % (name, mode, seed, res["kind"])
    if res["kind"] == GLIDER:
        p, d = res["period"], res["displacement"]
        ok = verify_glider(orbit(S, C, mode, 1)[0] if res["t"] == 0 else
                           _at(S, C, mode, res["t"]), C, p, d, mode)
        line += "  p=%d d=%+d t0=%d card=%d verify=%s" % (p, d, res["t"],
                                                          res["card"], ok)
    elif res["kind"] in (FIXED, BALANCED, CYCLE):
        line += "  period=%s t0=%d card=%s" % (res.get("period"), res["t"],
                                               res.get("card"))
    else:
        line += "  t=%d" % res["t"]
    print(line)
    return res

def _at(S, C, mode, t):
    for _ in range(t):
        S = step(S, C, mode)
    return S

print("=" * 78)
print("T0  SPECIMEN VERIFICATION")
print("=" * 78)

# ---- TANDEM-1
T1 = Const([(0, -1, 1), (0, -1, 0)], targets=[(0, 1), (0, 1)])
print("\nTANDEM-1  rules=[(0,-1,1),(0,-1,0)] targets=[(0,1),(0,1)]")
for seed in [[(1, 0), (1, 1)], [(0, 0), (0, 1)]]:
    report("TANDEM-1", T1, seed, "parity")
    report("TANDEM-1", T1, seed, "or")

# ---- SOLO
SOLO = Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], targets=[(1, 2), (0,), (0,)])
print("\nSOLO  rules=[(0,1,0),(0,1,1),(0,1,0)] targets=[(1,2),(0,),(0,)]")
for seed in [[(1, 0)], [(0, 0)]]:
    report("SOLO", SOLO, seed, "parity")
    report("SOLO", SOLO, seed, "or")

# ---- TRIPTYCH
TRI = Const([(0, 1, 0), (0, -1, 1), (0, 1, -1)], targets=[(0, 1, 2)] * 3)
print("\nTRIPTYCH  rules=[(0,1,0),(0,-1,1),(0,1,-1)] targets=[(0,1,2)]*3")
for seed in [[(1, 0), (2, 1), (4, 2)], [(1, 0), (2, 1), (4, 2)]]:
    report("TRIPTYCH", TRI, seed, "parity")
    break
# small search for a p=1 d=+1 glider
print("  -- search for p=1 d=+1 gliders, support in cells 0..5, <=4 laws:")
g = find_gliders(TRI, "parity", max_cells=4, cell_range=range(0, 6),
                 max_steps=200)
seen = set()
for combo, res in g:
    key = (res["period"], res["displacement"])
    if key in seen and len(seen) > 6:
        continue
    seen.add(key)
    print("     %-30s p=%d d=%+d card=%d t0=%d" %
          (combo, res["period"], res["displacement"], res["card"], res["t"]))

# ---- 1-D GUN
GUN = Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], targets=[(0, 1), (0, 1), (0, 1)])
print("\n1-D GUN  rules=[(0,1,0),(0,1,1),(0,1,0)] targets=[(0,1)]*3  seed [(0,2)]")
S = state_of([(0, 2)])
cards = []
for t in range(20):
    cards.append(card(S))
    S = step(S, GUN, "parity")
print("  |S_t| t=0..19 :", cards)
print("  predicted 2*floor(t/2)+3 :", [2 * (t // 2) + 3 for t in range(20)])
print("  match:", cards == [2 * (t // 2) + 3 for t in range(20)])
S = state_of([(0, 2)])
for r in spacetime(S, GUN, 12, "parity", lo=-8, hi=8):
    print("   ", r)

# ---- MIRROR
MIR = Const([(0, 1, -1), (0, -1, 1)], targets=[(0, 1), (0, 1)])
print("\nMIRROR  rules=[(0,1,-1),(0,-1,1)] targets=[(0,1),(0,1)]")
print("  -- complete sweep, support in cells 0..5, <=4 laws, parity:")
g = find_gliders(MIR, "parity", max_cells=4, cell_range=range(0, 6),
                 max_steps=400, max_card=200, max_span=800)
byd = {}
for combo, res in g:
    byd.setdefault((res["period"], res["displacement"]), []).append((combo, res))
for k in sorted(byd):
    ex = byd[k][0]
    print("     p=%d d=%+d  count=%d  ex=%s card=%d" %
          (k[0], k[1], len(byd[k]), ex[0], ex[1]["card"]))
