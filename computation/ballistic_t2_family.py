"""T2 (cont.): the MIRROR family collision table -- HEAD-ON across species and
REAR-END (a fast glider overtaking a slow one).  MIRROR carries d=+2 gliders at
p = 4, 5, 12 (speeds 1/2, 2/5, 1/6) and, by the palindromic automorphism
x -> -x, the mirrored d=-2 partner of each.
"""
import sys, json, time, itertools
from collections import Counter
from fractions import Fraction
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *
from ballistic_collide import resolve, bucket, fmt_parts

MIR = Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)])
SEEDS = {
    "M2/5": (5, [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21]),
    "M1/2": (4, [1, 2, 3, 4, 5, 7, 9, 10, 11, 13, 15, 17, 19, 21, 23, 26, 28,
                 30, 31, 32, 33, 34, 36, 38, 40, 42, 43, 44, 46, 47, 48, 49,
                 50, 51, 52, 53]),
    "M1/6": (12, [3, 6, 7, 8, 10, 11, 12, 13, 14, 16, 18, 19, 20, 22, 24, 25,
                  26, 28, 29, 30, 32, 33, 34, 36, 37, 38, 39, 40, 41]),
}
RIGHT, LEFT = {}, {}
for nm, (p, cells) in SEEDS.items():
    S = {c: 3 for c in cells}
    S = shift(S, -min(S))
    assert verify_glider(S, MIR, p, 2, "parity"), nm
    RIGHT[nm] = (p, 2, S)
    T = mirror_state(S); T = shift(T, -min(T))
    assert verify_glider(T, MIR, p, -2, "parity"), nm + "-L"
    LEFT[nm] = (p, -2, T)
    print("%-5s p=%2d d=+2 span=%2d card=%3d  speed=%s   mirror partner d=-2 OK"
          % (nm, p, span(S), card(S), Fraction(2, p)))


def sweep(nameA, nameB, kindB, GAPMAX, TMAX, NSEP=140):
    """A is the LEFT object, B the RIGHT object.  kindB = 'L' -> head-on,
    'R' -> rear-end (A must then be the faster)."""
    pA, dA, SA = RIGHT[nameA]
    pB, dB, SB = (LEFT if kindB == "L" else RIGHT)[nameB]
    phA = orbit(SA, MIR, "parity", pA)
    phB = orbit(SB, MIR, "parity", pB)
    rows, t0 = [], time.time()
    for i in range(pA):
        for j in range(pB):
            for gap in range(GAPMAX + 1):
                A = phA[i]
                B = shift(phB[j], max(A) + 1 + gap - min(phB[j]))
                S = union(A, B)
                assert card(S) == card(A) + card(B)
                res = resolve(S, MIR, "parity", T_max=TMAX, N_sep=NSEP,
                              max_card=600, max_span=1600)
                rows.append({"i": i, "j": j, "gap": gap,
                             "bucket": bucket(res, 1 if kindB == "L" else 0,
                                              1 if kindB == "L" else 2),
                             "parts": fmt_parts(res), "t_res": res["t_res"],
                             "forever": res["forever"], "out": res["out"]})
    c = Counter(r["bucket"] for r in rows)
    print("\n%s(right,left-hand) vs %s(%s)   box: phase %d x %d, gap 0..%d "
          "-> N=%d   [%.0fs]"
          % (nameA, nameB, "left-mover, HEAD-ON" if kindB == "L"
             else "right-mover, REAR-END", pA, pB, GAPMAX, len(rows),
             time.time() - t0))
    for k, v in c.most_common():
        print("    %-24s %5d" % (k, v))
    c2 = Counter(r["parts"] for r in rows)
    print("    distinct signatures: %d" % len(c2))
    for k, v in c2.most_common(8):
        print("       %-44s %5d" % (k, v))
    odd = [r for r in rows if r["bucket"] not in
           ("ARREST", "ANNIHILATION", "EXPLOSION")]
    if odd:
        print("    *** NON-ARREST outcomes (%d):" % len(odd))
        for r in odd[:20]:
            print("       i=%d j=%d gap=%d -> %s  %s"
                  % (r["i"], r["j"], r["gap"], r["bucket"], r["parts"]))
    return rows


if __name__ == "__main__":
    out = {}
    job = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("\n" + "=" * 78)
    print("HEAD-ON, ACROSS SPECIES")
    print("=" * 78)
    if job in ("all", "ho"):
        out["M1/2 vs M1/2 L"] = sweep("M1/2", "M1/2", "L", 24, 400)
        out["M1/2 vs M2/5 L"] = sweep("M1/2", "M2/5", "L", 24, 400)
        out["M2/5 vs M1/6 L"] = sweep("M2/5", "M1/6", "L", 24, 400)
        out["M1/6 vs M1/6 L"] = sweep("M1/6", "M1/6", "L", 16, 500)
    print("\n" + "=" * 78)
    print("REAR-END (fast catches slow)")
    print("=" * 78)
    if job in ("all", "re"):
        out["M1/2 catches M2/5"] = sweep("M1/2", "M2/5", "R", 20, 900)
        out["M1/2 catches M1/6"] = sweep("M1/2", "M1/6", "R", 16, 700)
        out["M2/5 catches M1/6"] = sweep("M2/5", "M1/6", "R", 16, 900)
    with open("/Users/lukacs/claude/math/program/phase6/computation/"
              "ballistic_family_%s.json" % job, "w") as f:
        json.dump({k: Counter(r["bucket"] for r in v) for k, v in out.items()},
                  f, indent=1)
    print("\ndone")
