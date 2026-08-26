"""T2: the MIRROR head-on collision table.

MIRROR  = Const([(0,1,-1),(0,-1,1)], targets=[(0,1),(0,1)]).
It is PALINDROMIC (r1 = -r0, targets symmetric), so x -> -x is an automorphism
and the d=+2 glider has an exact d=-2 partner in the SAME universe.

R = MIRROR-2/5 right-mover : p=5, d=+2, 32 laws, cells
    {2,3,4,6,7,8,9,10,12,13,14,16,18,19,20,21} x both kinds, normalised to 0..19
L = its reflection            : p=5, d=-2, 32 laws

BOX: phase(R) in 0..4  x  phase(L) in 0..4  x  gap in 0..GAPMAX
     x mode in {parity, or}.  Complete enumeration.
gap = min(supp L) - max(supp R) - 1 at t = 0.
"""
import sys, json, time, itertools
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *
from ballistic_collide import resolve, bucket, fmt_parts, clusters

MIR = Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)])
CELLS = [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21]
R0 = state_of([(c, k) for c in CELLS for k in (0, 1)])
R0 = shift(R0, -min(R0))
L0 = mirror_state(R0)
L0 = shift(L0, -min(L0))
assert verify_glider(R0, MIR, 5, 2, "parity")
assert verify_glider(L0, MIR, 5, -2, "parity")

RPH = orbit(R0, MIR, "parity", 5)
LPH = orbit(L0, MIR, "parity", 5)
print("R phases spans:", [span(x) for x in RPH], "cards:", [card(x) for x in RPH])
print("L phases spans:", [span(x) for x in LPH], "cards:", [card(x) for x in LPH])

GAPMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
MODES = sys.argv[2].split(",") if len(sys.argv) > 2 else ["parity", "or"]

rows = []
t0 = time.time()
for mode in MODES:
    # OR-mode phases are different objects; recompute
    if mode == "or":
        rp = orbit(R0, MIR, "or", 5)
        lp = orbit(L0, MIR, "or", 5)
    else:
        rp, lp = RPH, LPH
    for i in range(5):
        A = rp[i]
        for j in range(5):
            B = lp[j]
            for gap in range(0, GAPMAX + 1):
                Bs = shift(B, max(A) + 1 + gap - min(B))
                S = union(A, Bs)
                assert card(S) == card(A) + card(B)
                res = resolve(S, MIR, mode, T_max=300, N_sep=120,
                              max_card=400, max_span=900)
                b = bucket(res, 1, 1)
                rows.append({"mode": mode, "i": i, "j": j, "gap": gap,
                             "bucket": b, "parts": fmt_parts(res),
                             "t_res": res["t_res"], "forever": res["forever"],
                             "global": res.get("global")})
    print("%s done  %.0fs  n=%d" % (mode, time.time() - t0, len(rows)))

from collections import Counter
out = {}
for mode in MODES:
    sub = [r for r in rows if r["mode"] == mode]
    c = Counter(r["bucket"] for r in sub)
    print("\nMIRROR head-on, mode=%s   box: i,j in 0..4, gap 0..%d  N=%d"
          % (mode, GAPMAX, len(sub)))
    for k, v in c.most_common():
        print("   %-22s %5d" % (k, v))
    c2 = Counter(r["parts"] for r in sub)
    print("  distinct outcome signatures:", len(c2))
    for k, v in c2.most_common(14):
        print("     %-46s %5d" % (k, v))
    out[mode] = {"counts": dict(c), "sigs": dict(c2)}

with open("/Users/lukacs/claude/math/program/phase6/computation/"
          "ballistic_mirror_headon.json", "w") as f:
    json.dump({"box": {"i": [0, 4], "j": [0, 4], "gap": [0, GAPMAX],
                       "modes": MODES}, "rows": rows, "summary": out}, f)
print("\nwrote ballistic_mirror_headon.json")
