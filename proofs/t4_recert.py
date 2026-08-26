#!/usr/bin/env python3
"""t4_recert.py -- TARGET 4: full re-certification of the 2-kind census.

All light-cone-admissible rows are re-certified in full (independent ring
engine, three periods, plus xnomos); the remaining rows are re-certified on a
random sample of the stated size.  Lift/no-lift claims are re-checked on every
light-cone-admissible row.
"""
import json, random, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from t4_verify import row_ring, row_state
from t4_ring import rotor_certificate, verify_rotation_recurrence, verify_via_xnomos
from t4_lift import lift_report

paths = sys.argv[1:]
rows = []
for p in paths:
    rows += [json.loads(l) for l in open(p)]
rng = random.Random(11)
lc = [r for r in rows if r["lc"]]
rest = [r for r in rows if not r["lc"]]
sample = rng.sample(rest, min(20000, len(rest)))
print("rows: %d  (light-cone-admissible %d, sampled from the rest %d)"
      % (len(rows), len(lc), len(sample)))
bad = collections.Counter()
for tag, group, xn in (("LC", lc, True), ("sample", sample, False)):
    for r in group:
        R, X = row_ring(r), row_state(r)
        if not (verify_rotation_recurrence(X, R, r["p"], r["d"])
                and R.rot_state(X, r["d"]) != X):
            bad[tag + ":ring"] += 1
        c = rotor_certificate(X, R)
        if c is None or (c["p"], c["d"]) != (r["p"], r["d"]):
            bad[tag + ":minimal"] += 1
        if xn and not verify_via_xnomos(X, R, r["p"], r["d"]):
            bad[tag + ":xnomos"] += 1
print("failures:", dict(bad) or "NONE")
liftable = [r for r in lc if r["g"] >= 2 * r["p"]]
f = 0
for r in liftable:
    rep = lift_report(row_ring(r), row_state(r), r["p"], r["d"])
    if not (rep.get("correspondence") and rep.get("glides") and rep.get("verify_glider")):
        f += 1
print("Theorem B: %d rows with g >= 2pW, %d fail to lift" % (len(liftable), f))
od1 = [r for r in lc if r["od"] <= 1]
g = sum(1 for r in od1 if lift_report(row_ring(r), row_state(r), r["p"], r["d"]).get("glides"))
print("out-degree<=1 LC rotors: %d, of which the cut-lift glides: %d" % (len(od1), g))
