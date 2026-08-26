#!/usr/bin/env python3
"""
sunset.py — prediction Y8: is the impermanence sector rich, and does citation
make it richer?

SEMANTICS.  Sunset-by-default with lifetime tau = 1: a law lapses unless
re-enacted, so the next state is exactly the set of slots receiving an odd
(parity) / at least one (OR) toggle.  Implemented as `cite.step_sunset`.

THREE SWEEPS, all with seeds of span <= 3 (48 seeds) and both resolutions,
budgets 200 steps / card 200 / span 120, every reported glider re-certified
from its core over three full periods by `cite.verify_glider_sunset`:

  1. a 40,000-constitution random sample of the full n = 2, W = 1 citation box;
  2. the COMPLETE occupancy corner (108^2 = 11,664 constitutions);
  3. a size-matched random sample of CITING constitutions (11,664).

(2) and (3) are the controlled experiment: same rule pool, same targets, same
seeds, same budgets, differing only in whether the guards name kinds.

    python3 sunset.py           # ~10 min; writes data/sunset.json
"""

from __future__ import annotations

import itertools
import json
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cite as ct                                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

SEEDS = ct.seeds_span(3, 2)
KINDS = ct.all_kinds(2)
TSETS = [t for r in range(3) for t in itertools.combinations(range(2), r)]
OCC = [(rule, T, (None, None)) for rule in ct.RULES for T in TSETS]
BUDGET = dict(max_steps=200, max_card=200, max_span=120)


def sweep(pairs, label):
    res = Counter()
    spec = Counter()
    gcon = 0
    ncert = 0
    for (k1, k2) in pairs:
        C = ct.Cit([k1[0], k2[0]], [k1[1], k2[1]], [k1[2], k2[2]])
        hit = False
        for s in SEEDS:
            for mode in ("parity", "or"):
                r = ct.classify_sunset(list(s), C, mode, **BUDGET)
                res[r["kind"]] += 1
                if r["kind"] != ct.GLIDER:
                    continue
                core = list(s)
                for _ in range(r["t"]):
                    core = ct.step_sunset(core, C, mode)
                assert ct.verify_glider_sunset(core, C, r["period"],
                                               r["displacement"], mode), \
                    C.label()
                ncert += 1
                spec[(r["period"], r["displacement"])] += 1
                hit = True
        gcon += hit
    n = sum(res.values())
    out = {"label": label, "constitutions": len(pairs), "runs": n,
           "classes": dict(res), "glider_bearing": gcon,
           "glider_bearing_pct": 100.0 * gcon / len(pairs),
           "certified_gliders": ncert,
           "speeds": sorted({abs(d) / p for (p, d) in spec}),
           "spectrum": {"%d,%d" % k: v for k, v in spec.most_common(12)}}
    print("%s: %d constitutions, %d runs" % (label, len(pairs), n))
    for k, v in res.most_common():
        print("    %-11s %9d  %6.3f%%" % (k, v, 100.0 * v / n))
    print("    glider-bearing constitutions: %d = %.2f%%   (all %d gliders "
          "re-certified)" % (gcon, out["glider_bearing_pct"], ncert))
    print("    speeds: %s" % out["speeds"])
    return out


def main():
    rng = random.Random(31)
    res = {}
    samp = [(KINDS[rng.randrange(len(KINDS))], KINDS[rng.randrange(len(KINDS))])
            for _ in range(40000)]
    res["box_sample"] = sweep(samp, "SUNSET, 40k random sample of the box")
    res["occupancy_corner"] = sweep([(a, b) for a in OCC for b in OCC],
                                    "SUNSET + occupancy guards (COMPLETE)")
    rng2 = random.Random(77)
    cit = []
    while len(cit) < 11664:
        k1 = KINDS[rng2.randrange(len(KINDS))]
        k2 = KINDS[rng2.randrange(len(KINDS))]
        if k1[2] == (None, None) and k2[2] == (None, None):
            continue
        cit.append((k1, k2))
    res["citing_matched"] = sweep(cit, "SUNSET + citation (matched sample)")
    with open(os.path.join(DATA, "sunset.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print("\nwrote data/sunset.json")


if __name__ == "__main__":
    main()
