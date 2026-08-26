"""T1c: the BOX SWEEP for universes carrying two glider species that can MEET.

BOX (complete enumeration):
  kinds n = 2; rules (a,b,c) in {-1,0,1}^3 -> 27 choices each -> 729 rule pairs
  target patterns: FULL [(0,1),(0,1)], RECIP [(1,),(0,)],
                   MIXA [(0,1),(0,)], MIXB [(1,),(0,1)]
  modes: parity, or
  seeds: every non-empty subset of {0,1,2,3} x {0,1} whose cell 0 is occupied
         (192 seeds), classified with max_steps=90, max_card=40, max_span=90.
Records, per universe, the set of (period, displacement) of every GLIDER found.
Flags universes with two species that can meet: opposite d signs (HEAD-ON) or
same sign, different d/p (REAR-END).
Also flags GUN candidates: a GROWING seed that at t=90 decomposes into >=3
mutually separated clusters.
"""
import sys, itertools, json
from fractions import Fraction
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *
from ballistic_collide import clusters

OFF = (-1, 0, 1)
RULES = [(a, b, c) for a in OFF for b in OFF for c in OFF]
TARGS = {"FULL": [(0, 1), (0, 1)], "RECIP": [(1,), (0,)],
         "MIXA": [(0, 1), (0,)], "MIXB": [(1,), (0, 1)]}
W = 4
SLOTS = [(c, k) for c in range(W) for k in range(2)]
SEEDS = []
for r in range(1, len(SLOTS) + 1):
    for combo in itertools.combinations(SLOTS, r):
        if min(c for c, _ in combo) == 0:
            SEEDS.append(combo)
print("seeds per universe:", len(SEEDS))
print("universes:", len(RULES) ** 2 * len(TARGS) * 2)

meet, guns, allrec = [], [], []
nu = 0
for r0 in RULES:
    for r1 in RULES:
        for tn, tg in TARGS.items():
            C = Const([r0, r1], tg)
            for mode in ("parity", "or"):
                nu += 1
                got = {}
                growers = []
                for combo in SEEDS:
                    S0 = state_of(combo)
                    res = classify(S0, C, mode, max_steps=90, max_card=40,
                                   max_span=90)
                    if res["kind"] == GLIDER:
                        k = (res["period"], res["displacement"])
                        if k not in got or res["card"] < got[k][1]:
                            got[k] = (combo, res["card"])
                    elif res["kind"] == GROWING and len(growers) < 4:
                        growers.append(combo)
                if not got:
                    continue
                sp = sorted(got)
                allrec.append((r0, r1, tn, mode, sp))
                signs = {(1 if d > 0 else -1) for p, d in sp}
                speeds = {Fraction(d, p) for p, d in sp}
                if len(signs) > 1 or len(speeds) > 1:
                    meet.append((r0, r1, tn, mode, sp,
                                 {k: got[k] for k in got}))
                # gun test
                for combo in growers:
                    S = state_of(combo)
                    for _ in range(90):
                        S = step(S, C, mode)
                    cl = clusters(S, 3)
                    if len(cl) >= 3:
                        guns.append((r0, r1, tn, mode, combo, len(cl)))
                        break

print("\nuniverses swept:", nu)
print("universes carrying >=1 glider in the box:", len(allrec))
print("universes with TWO MEETING SPECIES in the box:", len(meet))
for r0, r1, tn, mode, sp, got in meet:
    print("  rules %s %s  targets=%-5s %-6s species:" % (r0, r1, tn, mode))
    for k in sp:
        print("      p=%-2d d=%+d card=%-2d seed=%s" %
              (k[0], k[1], got[k][1], list(got[k][0])))
print("\nGUN candidates (>=3 separated clusters at t=90):", len(guns))
for g in guns[:40]:
    print("  ", g)

with open("/Users/lukacs/claude/math/program/phase6/computation/"
          "ballistic_meeting_universes.json", "w") as f:
    json.dump({"meet": [[list(a), list(b), c, d, [list(x) for x in e],
                         {str(k): [list(map(list, v[0])), v[1]]
                          for k, v in g.items()}]
                        for a, b, c, d, e, g in meet],
               "guns": [[list(a), list(b), c, d, [list(x) for x in e], n]
                        for a, b, c, d, e, n in guns],
               "n_universes": nu, "n_with_glider": len(allrec)}, f, indent=1)
print("\nwrote ballistic_meeting_universes.json")
