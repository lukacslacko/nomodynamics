#!/usr/bin/env python3
"""
width.py — the width scan.

X-A's frontier (and X-E's first map) fixed the box and varied (p,d).  The
n=2/W=1/p=5/d=2 glider — SAT at interior 26, UNSAT at interior 20 — showed the
box was the binding constraint, not the number of kinds.  So the right question
is the *minimum interior width* at which a given (n, W, p, d) becomes
realisable:

    Wmin(n, W, p, d) = least  N - 2W  for which the bounded question is SAT
                       (= +inf if no glider of that (p,d) exists at all)

Each job scans interiors upward and stops at the first SAT.  Every UNSAT along
the way is a complete decision for its own box; the first SAT is a certified
specimen.

    python3 width.py <jobfile.json> <out.jsonl> [workers]

Job dict: n, W, p, d, mode, interiors (list), plus _label.
"""
from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "xamend1d"))
sys.path.insert(0, os.path.dirname(HERE))

import xsat            # noqa: E402
from xsat import Spec  # noqa: E402


def scan(kw):
    lab = kw["_label"]
    n, W, p, d = kw["n"], kw["W"], kw["p"], kw["d"]
    mode = kw.get("mode", "parity")
    steps = []
    t0 = time.time()
    for interior in kw["interiors"]:
        N = interior + 2 * W
        t1 = time.time()
        try:
            st, info = xsat.solve(Spec(n=n, W=W, N=N, p=p, d=d, mode=mode))
        except AssertionError as e:
            return dict(label=lab, status="BUG", note=str(e)[:400])
        except Exception as e:                               # pragma: no cover
            return dict(label=lab, status="ERR", note=repr(e)[:300])
        steps.append([interior, st, round(time.time() - t1, 1)])
        if st == "SAT":
            return dict(label=lab, n=n, W=W, p=p, d=d, mode=mode,
                        status="SAT", wmin=interior, steps=steps,
                        secs=round(time.time() - t0, 1),
                        rules=info["rules"],
                        tgt=[list(x) for x in info["targets"]],
                        seed={str(k): v for k, v in info["frames"][0].items() if v},
                        certified=info["certified"])
    return dict(label=lab, n=n, W=W, p=p, d=d, mode=mode, status="UNSAT",
                wmin=None, steps=steps, secs=round(time.time() - t0, 1))


def main():
    jobfile, outfile = sys.argv[1], sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    jobs = json.load(open(jobfile))
    done = set()
    if os.path.exists(outfile):
        for line in open(outfile):
            if line.strip():
                done.add(json.loads(line)["label"])
    jobs = [j for j in jobs if j["_label"] not in done]
    print("%d scans, %d workers" % (len(jobs), workers), flush=True)
    t0 = time.time()
    with open(outfile, "a") as fh, Pool(workers) as pool:
        for i, r in enumerate(pool.imap_unordered(scan, jobs, chunksize=1)):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print("[%3d/%3d %6.0fs] %-26s %-5s wmin=%-5s %s"
                  % (i + 1, len(jobs), time.time() - t0, r["label"],
                     r["status"], r.get("wmin"),
                     r.get("steps")), flush=True)


if __name__ == "__main__":
    main()
