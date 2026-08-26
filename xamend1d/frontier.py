#!/usr/bin/env python3
"""
frontier.py — push the exact SAT frontier for each cross-amendment sector.

Each job is one bounded existence question:
    "over ALL constitutions of this class, is there a glider of period p and
     ANY displacement d in 1..pW, whose t=0..p trajectory fits in N-2W cells?"
UNSAT = a complete no-go for that whole box (not a sample).
"""
from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import xsat
from xsat import Spec


def perm_targets(cycles):
    """cycles = list of cycle lengths -> a permutation target list."""
    t, base = [], 0
    for L in cycles:
        for i in range(L):
            t.append((base + (i + 1) % L,))
        base += L
    return t


def job(spec_kw):
    spec_kw = dict(spec_kw)
    lab = spec_kw.pop("_label")
    to = spec_kw.pop("_to", 1800)
    t0 = time.time()
    sp = Spec(**spec_kw)
    try:
        st, info = xsat.solve(sp, timeout=to)
    except AssertionError as e:
        return dict(label=lab, status="BUG", note=str(e)[:400])
    out = dict(label=lab, status=st, secs=round(time.time() - t0, 1),
               n=sp.n, W=sp.W, N=sp.N, p=sp.p, mode=sp.mode)
    if st == "SAT":
        out["rules"] = info["rules"]
        out["targets"] = [list(x) for x in info["targets"]]
        out["d"] = info["d"]
        out["seed"] = {str(k): v for k, v in info["frames"][0].items() if v}
        out["certified"] = info["certified"]
    return out


def build_jobs():
    jobs = []

    def add(label, **kw):
        kw["_label"] = label
        jobs.append(kw)

    # ---------- E2: fixed single targeting by a permutation ----------------
    for mode in ("parity", "or"):
        for cyc, name in ((( 2,), "L2"), ((3,), "L3"), ((4,), "L4"),
                          ((5,), "L5"), ((2, 2), "L2+L2"), ((3, 2), "L3+L2")):
            n = sum(cyc)
            for W in (1, 2):
                for N in ((18, 22) if W == 1 else (16,)):
                    for p in range(1, 13 if W == 1 else 9):
                        add("E2-%s-%s-W%d-N%d-p%d" % (name, mode, W, N, p),
                            n=n, W=W, N=N, p=p,
                            d=list(range(1, p * W + 1)), mode=mode,
                            targets=perm_targets(cyc))

    # ---------- E1: supersession ------------------------------------------
    for mode in ("super", "super_or"):
        for n in (1, 2, 3, 4, 5):
            for W in (1, 2):
                for N in ((18,) if W == 1 else (16,)):
                    for p in range(1, 11 if W == 1 else 8):
                        add("E1-n%d-%s-W%d-N%d-p%d" % (n, mode, W, N, p),
                            n=n, W=W, N=N, p=p,
                            d=list(range(1, p * W + 1)), mode=mode)

    # ---------- own-kind control (must be UNSAT: Anchor Theorem) ----------
    for n in (1, 2, 3):
        for p in range(1, 9):
            add("OWN-n%d-p%d" % (n, p), n=n, W=1, N=16, p=p,
                d=list(range(1, p + 1)), mode="parity",
                targets=[(k,) for k in range(n)])

    return jobs


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    jobs = [j for j in build_jobs() if only in j["_label"]]
    print("%d jobs" % len(jobs))
    res = []
    with Pool(10) as pool:
        for r in pool.imap_unordered(job, jobs):
            res.append(r)
            if r["status"] != "UNSAT":
                print("  *** %-34s %s" % (r["label"], r["status"]))
            if len(res) % 25 == 0:
                print("  ... %d/%d" % (len(res), len(jobs)))
                sys.stdout.flush()
    out = os.path.join(HERE, "data", "frontier%s.json" % (("_" + only) if only else ""))
    with open(out, "w") as f:
        json.dump(res, f, indent=1)
    from collections import Counter
    print(Counter(r["status"] for r in res))
    print("written", out)


if __name__ == "__main__":
    main()
