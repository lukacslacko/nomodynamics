"""T1: left-movers.  Mirror constitutions, and single universes carrying both
directions."""
import sys, itertools
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *

def kindswap(S, perm):
    """Apply a permutation of kinds to a state."""
    out = {}
    for c, m in S.items():
        x = 0
        for k in range(16):
            if (m >> k) & 1:
                x |= 1 << perm[k]
        out[c] = x
    return out

SPECS = {}

SPECS["TANDEM-1"] = (Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)]),
                     state_of([(1, 0), (1, 1)]), 1, 1, "parity")
SPECS["SOLO"] = (Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(1, 2), (0,), (0,)]),
                 state_of([(1, 0)]), 2, 1, "parity")
SPECS["TRIPTYCH"] = (Const([(0, 1, 0), (0, -1, 1), (0, 1, -1)], [(0, 1, 2)] * 3),
                     state_of([(c, k) for c in (1, 2, 4) for k in range(3)]),
                     1, 1, "parity")
_mcells = [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21]
SPECS["MIRROR-2/5"] = (Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)]),
                       state_of([(c, k) for c in _mcells for k in (0, 1)]),
                       5, 2, "parity")

print("=" * 78)
print("T0b  CORRECTED SPECIMENS  (verify_glider certificates)")
print("=" * 78)
for nm, (C, S, p, d, mode) in SPECS.items():
    print("%-12s %s" % (nm, C.label()))
    print("   seed card=%d span=%d  verify_glider(p=%d,d=%+d,%s) = %s"
          % (card(S), span(S), p, d, mode, verify_glider(S, C, p, d, mode)))
    print("   OR-mode same (p,d): %s   classify(OR)=%s"
          % (verify_glider(S, C, p, d, "or"),
             classify(S, C, "or", max_steps=120, max_card=300,
                      max_span=300)["kind"]))

print()
print("=" * 78)
print("T1a  MIRROR-IMAGE CONSTITUTIONS  (negate a,b,c; reflect the seed)")
print("=" * 78)
MSPECS = {}
for nm, (C, S, p, d, mode) in SPECS.items():
    Cm = mirror_const(C)
    Sm = mirror_state(S)
    ok = verify_glider(Sm, Cm, p, -d, mode)
    res = classify(Sm, Cm, mode, max_steps=400, max_card=400, max_span=900)
    print("%-12s -> %s" % (nm + "-L", Cm.label()))
    print("   seed cells %s  verify_glider(p=%d,d=%+d) = %s   classify=%s p=%s d=%s"
          % (sorted(Sm), p, -d, ok, res["kind"], res.get("period"),
             res.get("displacement")))
    MSPECS[nm + "-L"] = (Cm, Sm, p, -d, mode)

print()
print("=" * 78)
print("T1b  BOTH DIRECTIONS IN ONE UNIVERSE")
print("=" * 78)
print("MIRROR is PALINDROMIC: rules r0=(0,1,-1), r1=(0,-1,1)=-r0, targets both")
print("{0,1}.  So x->-x composed with the kind-swap 0<->1 is an automorphism of")
print("the universe.  Applying it to the right-moving MIRROR-2/5 glider must")
print("give a LEFT-moving glider IN THE SAME CONSTITUTION.")
C, S, p, d, mode = SPECS["MIRROR-2/5"]
SL = kindswap(mirror_state(S), {0: 1, 1: 0})
SL = shift(SL, -min(SL))
print("  MIRROR-2/5-L seed cells:", sorted(SL))
print("  card=%d span=%d" % (card(SL), span(SL)))
print("  verify_glider(SL, MIRROR, p=5, d=-2, parity) =",
      verify_glider(SL, C, 5, -2, "parity"))
r = classify(SL, C, "parity", max_steps=200, max_card=200, max_span=400)
print("  classify:", r["kind"], "p=", r.get("period"), "d=", r.get("displacement"))
print("  (the kind-swap is *needed*: plain reflection without it gives",
      verify_glider(shift(mirror_state(S), 22), C, 5, -2, "parity"), ")")

print()
print("-" * 78)
print("T1c  SEARCH: palindromic n=2, W=1 universes with SMALL bidirectional")
print("     gliders.  Box: rules {(a,b,c) in {-1,0,1}^3} paired as (r,-r), all")
print("     13 non-zero pairs x 2 target patterns x 2 modes; seeds = all")
print("     non-empty subsets of {0..W-1}x{0,1} anchored at cell 0, W<=6")
print("     (complete enumeration).")
print("-" * 78)
OFF = (-1, 0, 1)
pairs = []
seen = set()
for a in OFF:
    for b in OFF:
        for c in OFF:
            r = (a, b, c)
            nr = (-a, -b, -c)
            if r == nr or r in seen or nr in seen:
                continue
            seen.add(r); seen.add(nr)
            pairs.append((r, nr))
print("palindromic rule pairs:", len(pairs))

TARGS = {"full": [(0, 1), (0, 1)], "recip": [(1,), (0,)]}
hits = []
W = 6
slots = [(c, k) for c in range(W) for k in range(2)]
for (r0, r1) in pairs:
    for tn, tg in TARGS.items():
        Cx = Const([r0, r1], tg)
        for mode in ("parity", "or"):
            got = {}
            for rr in range(1, 2 * W + 1):
                for combo in itertools.combinations(slots, rr):
                    if min(c for c, _ in combo) != 0:
                        continue
                    S0 = state_of(combo)
                    res = classify(S0, Cx, mode, max_steps=120,
                                   max_card=80, max_span=150)
                    if res["kind"] == GLIDER:
                        key = (res["period"], res["displacement"])
                        if key not in got:
                            got[key] = (combo, res)
            ds = {k[1] for k in got}
            if any(x > 0 for x in ds) and any(x < 0 for x in ds):
                hits.append((r0, r1, tn, mode, got))
                print("  BIDIRECTIONAL: rules %s/%s targets=%s mode=%s" %
                      (r0, r1, tn, mode))
                for k in sorted(got):
                    cb, rs = got[k]
                    print("      p=%d d=%+d card=%d seed=%s" %
                          (k[0], k[1], rs["card"], cb))
            elif got:
                pass
print("\nbidirectional palindromic universes found in the box:", len(hits))
