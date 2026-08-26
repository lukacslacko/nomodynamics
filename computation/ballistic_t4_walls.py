"""T4: walls, and glider-vs-wall collisions (also the DUPLICATE / REFLECT hunt).

A WALL is a STATIONARY code:
  DEAD    - FIXED with 0 active laws (a dead letter)
  BAL     - FIXED with >=1 active law (a balanced constitution: the enactments
            cancel under parity)
  OSC     - CYCLE of period q >= 2 that does not translate
Enumerated COMPLETELY over supports inside cells 0..WW-1 (every non-empty
subset of {0..WW-1} x kinds whose cell 0 is occupied).

Then every (wall, wall-phase, glider-phase, gap) in the stated box is run and
the outcome certified with ballistic_collide.resolve().
"""
import sys, json, time, itertools
from collections import Counter
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *
from ballistic_collide import resolve, bucket, fmt_parts, clusters

UNIS = {
    "TANDEM-1": (Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)]),
                 state_of([(0, 0), (0, 1)]), 1, 1),
    "SOLO": (Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(1, 2), (0,), (0,)]),
             state_of([(0, 0)]), 2, 1),
    "GUN": (Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(0, 1)] * 3),
            state_of([(0, 0), (0, 1)]), 1, 1),
    "TRIPTYCH": (Const([(0, 1, 0), (0, -1, 1), (0, 1, -1)], [(0, 1, 2)] * 3),
                 state_of([(c, k) for c in (0, 1, 3) for k in range(3)]), 1, 1),
}
_MC = [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19, 20, 21]
_MR = state_of([(c, k) for c in _MC for k in (0, 1)])
UNIS["MIRROR"] = (Const([(0, 1, -1), (0, -1, 1)], [(0, 1), (0, 1)]),
                  shift(_MR, -min(_MR)), 5, 2)


def enumerate_walls(C, mode, WW, max_steps=60):
    """All stationary codes with support in 0..WW-1, cell 0 occupied.
    Returns list of (kindtag, period, active, state)."""
    slots = [(c, k) for c in range(WW) for k in range(C.n)]
    out = []
    for r in range(1, len(slots) + 1):
        for combo in itertools.combinations(slots, r):
            if min(c for c, _ in combo) != 0:
                continue
            S = state_of(combo)
            T = step(S, C, mode)
            if T == S:
                act = len(active_laws(S, C))
                out.append(("DEAD" if act == 0 else "BAL", 1, act, S))
                continue
            res = classify(S, C, mode, max_steps=max_steps, max_card=60,
                           max_span=WW + 30)
            if res["kind"] == CYCLE and res["t"] == 0:
                out.append(("OSC", res["period"], 0, S))
    return out


def wall_bucket(res, wall_state, C, mode):
    parts = res["parts"]
    if res["out"] in ("GROWING", "UNRESOLVED"):
        return "EXPLOSION" if res["out"] == "GROWING" else "UNRESOLVED"
    if not parts or all(p[0] == EXTINCT for p in parts):
        return "MUTUAL-ANNIHILATION"
    movers = [p for p in parts if p[0] == GLIDER]
    right = [p for p in movers if p[2] > 0]
    left = [p for p in movers if p[2] < 0]
    stat = [p for p in parts if p[0] in (FIXED, BALANCED, CYCLE)]
    if len(movers) >= 2:
        return "FAN-OUT"
    if left and not right:
        return "REFLECT"
    if right and stat:
        return "TRANSPARENT"       # glider out the far side, wall still there
    if right and not stat:
        return "WALL-DESTROYED"
    if not movers and stat:
        return "ABSORBED"          # glider eaten, obstacle remains -> DELETE
    return "OTHER"


def run(name, WW, GAPMAX, modes=("parity", "or"), TMAX=220, limit_walls=None):
    C, G, p, d = UNIS[name]
    print("=" * 78)
    print("%s   %s" % (name, C.label()))
    print("  glider p=%d d=%+d card=%d span=%d" % (p, d, card(G), span(G)))
    allrows = []
    for mode in modes:
        walls = enumerate_walls(C, mode, WW)
        nslots = WW * C.n
        nseed = sum(1 for r in range(1, nslots + 1)
                    for cb in itertools.combinations(
                        [(c, k) for c in range(WW) for k in range(C.n)], r)
                    if min(c for c, _ in cb) == 0)
        cnt = Counter(w[0] for w in walls)
        print("  mode=%s  wall box: support in cells 0..%d, all %d anchored "
              "seeds  ->  %d stationary codes  %s"
              % (mode, WW - 1, nseed, len(walls), dict(cnt)))
        if not walls:
            continue
        if limit_walls:
            walls = walls[:limit_walls]
        gph = orbit(G, C, mode, p)
        rows = []
        for wi, (tag, q, act, WS) in enumerate(walls):
            wph = orbit(WS, C, mode, q)
            for wj, W in enumerate(wph):
                for gi, A in enumerate(gph):
                    for gap in range(0, GAPMAX + 1):
                        Ash = shift(A, min(W) - 1 - gap - max(A))
                        S = union(Ash, W)
                        if card(S) != card(Ash) + card(W):
                            continue
                        res = resolve(S, C, mode, T_max=TMAX, N_sep=110,
                                      max_card=300, max_span=600)
                        b = wall_bucket(res, W, C, mode)
                        rows.append({"wall": wi, "tag": tag, "q": q,
                                     "act": act,
                                     "wcells": sorted(WS.items()),
                                     "wj": wj, "gi": gi, "gap": gap,
                                     "bucket": b, "parts": fmt_parts(res),
                                     "t_res": res["t_res"],
                                     "forever": res["forever"]})
        c = Counter(r["bucket"] for r in rows)
        print("    collisions: N=%d   box: %d walls x phases x glider phase "
              "0..%d x gap 0..%d" % (len(rows), len(walls), p - 1, GAPMAX))
        for k, v in c.most_common():
            print("      %-22s %5d" % (k, v))
        for special in ("FAN-OUT", "REFLECT", "ABSORBED", "TRANSPARENT",
                        "WALL-DESTROYED", "MUTUAL-ANNIHILATION"):
            ex = [r for r in rows if r["bucket"] == special]
            if ex and special in ("FAN-OUT", "REFLECT"):
                print("      *** %s examples:" % special)
                for r in ex[:6]:
                    print("        wall=%s tag=%s wj=%d gi=%d gap=%d -> %s"
                          % (r["wcells"], r["tag"], r["wj"], r["gi"],
                             r["gap"], r["parts"]))
        allrows += [dict(r, mode=mode, uni=name) for r in rows]
    return allrows


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = []
    if which in ("all", "small"):
        out += run("TANDEM-1", 5, 12)
        out += run("GUN", 4, 12)
        out += run("SOLO", 4, 12)
        out += run("TRIPTYCH", 3, 12)
    if which in ("all", "mirror"):
        out += run("MIRROR", 5, 12, TMAX=260)
    with open("/Users/lukacs/claude/math/program/phase6/computation/"
              "ballistic_walls_%s.json" % which, "w") as f:
        json.dump(out, f)
    print("\nwrote ballistic_walls_%s.json  rows=%d" % (which, len(out)))
