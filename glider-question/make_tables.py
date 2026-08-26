#!/usr/bin/env python3
"""Emit the empirical-results markdown block from data/*.json."""
import json, os
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

ROWS = [
    ("w1_le3_duel",         "W=1, <=3 laws / 5 cells, COMPLETE, parity+OR duel"),
    ("w2_le2_duel",         "W=2, <=2 laws / 5 cells, COMPLETE, parity+OR duel"),
    ("w2_3law_duel_sample", "W=2, 3 laws / 5 cells, SAMPLED 10^6, parity+OR duel"),
    ("w1_4law_parity",      "W=1, 4 laws / 5 cells, COMPLETE, parity (=OR, Lemma 1)"),
    ("hunt_5law_6cells_or", "W=1, 5 laws / 6 cells, <=4 kinds, SAMPLED 5x10^5, OR"),
    ("hunt_6law_6cells_or", "W=1, 6 laws / 6 cells, <=4 kinds, SAMPLED 5x10^5, OR"),
    ("super_le3",           "W=1 SUPERSESSION, <=3 laws / 5 cells, COMPLETE"),
    ("super_4law_sample",   "W=1 SUPERSESSION, 4 laws / 5 cells, SAMPLED 5x10^5"),
    ("super_5law_sample",   "W=1 SUPERSESSION, 5 laws / 6 cells, SAMPLED 5x10^5"),
]
VERDICTS = ["extinct", "fixed", "cycle", "glider", "big-growth",
            "slow-holdout", "divergence", "anomaly"]

def main():
    print("| sweep | seeds | extinct | fixed | cycle | glider | big-growth | holdout | diverg. | anomaly |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    total = 0
    for name, desc in ROWS:
        p = os.path.join(DATA, name + ".json")
        if not os.path.exists(p):
            print(f"| {desc} | MISSING |")
            continue
        d = json.load(open(p))
        t = d["tally"]; total += d["n"]
        cells = " | ".join(str(t.get(v, 0)) for v in VERDICTS)
        print(f"| {desc} | {d['n']} | {cells} |")
    print(f"\nTotal certified classifications: {total}")
    print("\nCycle-period histograms:")
    for name, desc in ROWS:
        p = os.path.join(DATA, name + ".json")
        if os.path.exists(p):
            d = json.load(open(p))
            if d["cycle_period_histogram"]:
                print(f"- {name}: {d['cycle_period_histogram']}  max transient {d['max_transient'][0]}")
    hp = os.path.join(DATA, "holdouts_resolved.json")
    if os.path.exists(hp):
        h = json.load(open(hp))
        print("\nSlow-holdout deep re-runs (20000 steps, hash cap 400, growth cap 20000):")
        for name, r in h.items():
            if r["n_holdouts"]:
                pinned = sum(1 for x in r["resolved"]
                             if not (x["left_edge_moved"] and x["right_edge_moved"]))
                print(f"- {name}: {r['n_holdouts']} holdouts -> {r.get('deep_tally')}; "
                      f"{pinned}/{r['n_holdouts']} have a pinned edge over 3000 steps")
    vp = os.path.join(DATA, "verify_anchors.json")
    if os.path.exists(vp):
        v = json.load(open(vp))
        print("\nAnchor-invariant machine checks (300-step random trajectories):")
        for k, r in v.items():
            print(f"- {k}: {r['trajectories']} trajectories, {len(r['violations'])} violations")

if __name__ == "__main__":
    main()
