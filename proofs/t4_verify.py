#!/usr/bin/env python3
"""
t4_verify.py -- TARGET 4: re-certification battery.

Every rotor row of every census is re-checked
  (1) through the independent bitmask engine t4_ring, over THREE full periods
      (Phi^{jp}(S) = rot_{jd}(S), j = 1,2,3), with rot_d(S) != S enforced;
  (2) through the xnomos.Const/step reference engine, likewise;
  (3) for the rows where the Lift Theorem applies (light-cone-admissible and
      vacant arc g >= 2pW): the cut-lift is built on Z and must satisfy
      Phi_Z^p(T) = sigma^d(T) -- verified again by xnomos.verify_glider;
  (4) for the light-cone-admissible rows with out-degree <= 1: the cut-lift is
      released on Z and classified; it must NOT be a glider with that (p,d)
      (the Out-Degree Law says it cannot be a glider at all).

Usage: python3 t4_verify.py t4_data/*.jsonl
"""

from __future__ import annotations

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xnomos
from t4_ring import (Ring, rotor_certificate, verify_rotation_recurrence,
                     verify_via_xnomos, vacant_arc)
from t4_lift import lift_report, zconst

W = 1


def row_ring(r):
    return Ring([tuple(x) for x in r["rules"]],
                [tuple(x) for x in r["targets"]], r["m"], r["mode"])


def row_state(r):
    m, n = r["m"], r["n"]
    s = r["state"]
    return tuple((s >> (k * m)) & ((1 << m) - 1) for k in range(n))


def main(paths, xnomos_sample=4000, seed=5):
    rows = []
    for p in paths:
        with open(p) as fh:
            rows += [json.loads(l) for l in fh]
    print("rows to re-certify: %d" % len(rows))
    rng = random.Random(seed)
    bad_ring = bad_xn = bad_min = 0
    n_xn = 0
    for r in rows:
        R, X = row_ring(r), row_state(r)
        # (1) the recorded certificate, three full periods, hygiene enforced
        if not (verify_rotation_recurrence(X, R, r["p"], r["d"])
                and R.rot_state(X, r["d"]) != X):
            bad_ring += 1
        # minimality of p, recomputed from scratch
        c = rotor_certificate(X, R)
        if c is None or c["p"] != r["p"] or c["d"] != r["d"]:
            bad_min += 1
        # (2) the same, inside xnomos
        if rng.random() < xnomos_sample / max(1, len(rows)):
            n_xn += 1
            if not verify_via_xnomos(X, R, r["p"], r["d"]):
                bad_xn += 1
    print("  (1) ring-engine re-checks    : %d rows, %d failures"
          % (len(rows), bad_ring))
    print("  (1b) minimal-(p,d) recomputed: %d rows, %d disagreements"
          % (len(rows), bad_min))
    print("  (2) xnomos re-checks         : %d sampled rows, %d failures"
          % (n_xn, bad_xn))

    # (3) Theorem B: every light-cone-admissible rotor with g >= 2pW lifts
    liftable = [r for r in rows if r["lc"] and r["g"] >= 2 * r["p"] * W]
    bad_lift = []
    for r in liftable:
        R, X = row_ring(r), row_state(r)
        rep = lift_report(R, X, r["p"], r["d"])
        if not (rep.get("correspondence") and rep.get("glides")
                and rep.get("verify_glider")):
            bad_lift.append((r, rep))
    print("  (3) Theorem B (LC and g >= 2pW): %d rows, %d that fail to lift"
          % (len(liftable), len(bad_lift)))
    for r, rep in bad_lift[:5]:
        print("      FAIL", r["m"], r["rules"], r["targets"], r["p"], r["d"],
              rep)

    # (4) light-cone-admissible with out-degree <= 1: cannot be wrapped gliders
    od1 = [r for r in rows if r["lc"] and r["od"] <= 1]
    sig = {}
    for r in od1:
        sig.setdefault((r["m"], tuple(map(tuple, r["rules"])),
                        tuple(map(tuple, r["targets"])), r["mode"],
                        r["p"], r["d"]), r)
    print("  (4) LC rotors with out-degree <= 1: %d rows, %d distinct "
          "(m, constitution, mode, p, d) signatures" % (len(od1), len(sig)))
    glide = 0
    for r in sig.values():
        R, X = row_ring(r), row_state(r)
        rep = lift_report(R, X, r["p"], r["d"])
        if rep.get("glides"):
            glide += 1
            print("      !!! an out-degree-1 rotor DID lift:", r)
    print("      cut-lifts that reproduce the rotor as a Z glider: %d "
          "(the Out-Degree Law predicts 0)" % glide)
    return bad_ring + bad_xn + bad_min + len(bad_lift) + glide


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "t4_data")
        paths = [os.path.join(d, f) for f in sorted(os.listdir(d))
                 if f.endswith(".jsonl") and not f.startswith("t4_sat")]
    sys.exit(0 if main(paths) == 0 else 1)
