#!/usr/bin/env python3
"""Task 2: attractor natural history — density sweep on nomic rings.

For each (m, lambda): random seeds with each of the 27m law-slots filled
independently with prob lambda/27 (expected laws/cell = lambda).
Iterate to attractor (full hashing, budget 50k steps).
Classify: extinct / fixed-porous / fixed-solid (full occupancy gridlock) /
cycle (period distribution) / holdout.  A 'balanced-fixed' class is asserted
impossible (Dead Letter Theorem): every fixed attractor is checked for zero
active laws.
"""
import sys, json, random, time
from collections import Counter
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/rings")
from ring import (step, active_count, nlaws, occ_count, run_to_attractor,
                  cycle_states, random_state)

MS = [4, 6, 8, 12, 16, 24]
LAMS = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 4.0]
NSEEDS = 400
BUDGET = 50000

def sweep(seed0=2026):
    rng = random.Random(seed0)
    results = {}
    for m in MS:
        for lam in LAMS:
            t0 = time.time()
            cls = Counter()
            periods = Counter()
            transients = []
            fin_occ = []
            fin_laws = []
            churns = []          # mean active laws along cycle attractors
            maxtrans = 0
            for _ in range(NSEEDS):
                s = random_state(m, lam, rng)
                kind, trans, per, attr, used = run_to_attractor(s, BUDGET)
                transients.append(trans)
                maxtrans = max(maxtrans, trans)
                if kind == "extinct":
                    cls["extinct"] += 1
                    fin_occ.append(0.0); fin_laws.append(0.0)
                elif kind == "fixed":
                    assert active_count(attr) == 0   # no balanced constitutions
                    if occ_count(attr) == m:
                        cls["fixed-solid"] += 1
                    else:
                        cls["fixed-porous"] += 1
                    fin_occ.append(occ_count(attr) / m)
                    fin_laws.append(nlaws(attr) / m)
                elif kind == "cycle":
                    cls["cycle"] += 1
                    periods[per] += 1
                    st = cycle_states(attr, per)
                    churns.append(sum(active_count(x) for x in st) / per)
                    fin_occ.append(sum(occ_count(x) for x in st) / per / m)
                    fin_laws.append(sum(nlaws(x) for x in st) / per / m)
                else:
                    cls["holdout"] += 1
            n = NSEEDS
            row = dict(
                m=m, lam=lam, n=n,
                frac={k: v / n for k, v in cls.items()},
                periods=dict(periods),
                mean_transient=sum(transients) / n,
                max_transient=maxtrans,
                mean_final_occ=sum(fin_occ) / max(len(fin_occ), 1),
                mean_final_lawspercell=sum(fin_laws) / max(len(fin_laws), 1),
                mean_cycle_churn=(sum(churns) / len(churns)) if churns else 0.0,
                secs=round(time.time() - t0, 1),
            )
            results[f"m{m}_lam{lam}"] = row
            fr = row["frac"]
            print(f"m={m:2d} lam={lam:<4} | ext {fr.get('extinct',0):.3f}"
                  f"  fixP {fr.get('fixed-porous',0):.3f}"
                  f"  fixS {fr.get('fixed-solid',0):.3f}"
                  f"  cyc {fr.get('cycle',0):.3f}"
                  f"  hold {fr.get('holdout',0):.3f}"
                  f" | occ* {row['mean_final_occ']:.3f}"
                  f" laws* {row['mean_final_lawspercell']:.2f}"
                  f" | trans mean {row['mean_transient']:.1f} max {maxtrans}"
                  f" | periods {dict(sorted(periods.items()))}"
                  f" | {row['secs']}s", flush=True)
    return results

if __name__ == "__main__":
    t0 = time.time()
    res = sweep()
    with open("/Users/lukacs/claude/math/program/phase6/rings/attractors.json", "w") as f:
        json.dump(res, f, indent=1)
    print(f"\ntotal {time.time()-t0:.0f}s -> attractors.json")
