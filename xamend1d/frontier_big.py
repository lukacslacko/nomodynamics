#!/usr/bin/env python3
"""frontier_big.py — the aggressive frontier: how far does UNSAT reach?"""
from __future__ import annotations

import json, os, sys, time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from frontier import job, perm_targets


def build():
    jobs = []

    def add(label, **kw):
        kw["_label"] = label
        kw["_to"] = 3600
        jobs.append(kw)

    CYC = ((( 2,), "L2"), ((3,), "L3"), ((4,), "L4"), ((5,), "L5"),
           ((6,), "L6"), ((2, 2), "L2+L2"), ((3, 3), "L3+L3"),
           ((3, 2), "L3+L2"), ((4, 2), "L4+L2"), ((2, 2, 2), "L2x3"))

    for mode in ("parity", "or"):
        for cyc, name in CYC:
            n = sum(cyc)
            for W, N, P in ((1, 28, 20), (2, 24, 12), (3, 20, 8)):
                for p in range(1, P + 1):
                    add("E2-%s-%s-W%d-N%d-p%d" % (name, mode, W, N, p),
                        n=n, W=W, N=N, p=p, d=list(range(1, p * W + 1)),
                        mode=mode, targets=perm_targets(cyc))

    for mode in ("super", "super_or"):
        for n in (1, 2, 3, 4, 5, 6):
            for W, N, P in ((1, 28, 18), (2, 24, 12), (3, 20, 8)):
                for p in range(1, P + 1):
                    add("E1-n%d-%s-W%d-N%d-p%d" % (n, mode, W, N, p),
                        n=n, W=W, N=N, p=p, d=list(range(1, p * W + 1)),
                        mode=mode)

    for n in (1, 2, 3, 4):
        for W, N, P in ((1, 24, 14), (2, 20, 10)):
            for p in range(1, P + 1):
                add("OWN-n%d-W%d-p%d" % (n, W, p), n=n, W=W, N=N, p=p,
                    d=list(range(1, p * W + 1)), mode="parity",
                    targets=[(k,) for k in range(n)])
    return jobs


if __name__ == "__main__":
    jobs = build()
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    jobs = [j for j in jobs if only in j["_label"]]
    jobs.sort(key=lambda j: (j["p"], j["n"], j["N"]))
    print("%d jobs" % len(jobs)); sys.stdout.flush()
    res = []
    with Pool(11) as pool:
        for r in pool.imap_unordered(job, jobs):
            res.append(r)
            if r["status"] != "UNSAT":
                print("  *** %-36s %s" % (r["label"], r["status"])); sys.stdout.flush()
            if len(res) % 25 == 0:
                print("  ... %d/%d" % (len(res), len(jobs))); sys.stdout.flush()
                json.dump(res, open(os.path.join(HERE, "data", "frontier_big.json"), "w"))
    json.dump(res, open(os.path.join(HERE, "data", "frontier_big.json"), "w"), indent=1)
    from collections import Counter
    print(Counter(r["status"] for r in res))
    r2 = sorted(res, key=lambda x: -x["secs"])
    for x in r2[:10]:
        print("  slowest %-38s %s %.0fs" % (x["label"], x["status"], x["secs"]))
    print("total cpu-secs", round(sum(x["secs"] for x in res)))
