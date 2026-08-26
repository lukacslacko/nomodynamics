#!/usr/bin/env python3
"""
run.py — Expedition X-E's parallel driver over X-A's exact SAT instrument.

Each job is ONE bounded existence question:

    "over ALL constitutions with at most n kinds and window W, is there a free
     glider of period p and displacement d whose t=0..p trajectory fits inside
     N - 2W cells?"

UNSAT = a complete no-go for that whole box (every constitution, every seed).
SAT   = a certified specimen (xsat.solve re-verifies with xnomos.verify_glider
        and raises if the engine disagrees).

Usage:
    python3 run.py <jobfile.json> <out.jsonl> [workers]

A jobfile is a JSON list of dicts; each dict is Spec(**kw) plus "_label".
Results are appended to out.jsonl as they complete, so a killed run keeps
everything already decided.
"""
from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
XA = os.path.join(os.path.dirname(HERE), "xamend1d")
sys.path.insert(0, XA)
sys.path.insert(0, os.path.dirname(HERE))

import xsat  # noqa: E402
from xsat import Spec  # noqa: E402


def job(kw):
    kw = dict(kw)
    lab = kw.pop("_label", "")
    t0 = time.time()
    try:
        sp = Spec(**kw)
        st, info = xsat.solve(sp)
    except AssertionError as e:  # uncertified SAT model = encoder bug
        return dict(label=lab, status="BUG", note=str(e)[:600], **kw)
    except Exception as e:  # pragma: no cover
        return dict(label=lab, status="ERR", note=repr(e)[:400], **kw)
    out = dict(label=lab, status=st, secs=round(time.time() - t0, 2),
               n=sp.n, W=sp.W, N=sp.N, p=sp.p, d=sp.d, mode=sp.mode)
    for extra in ("max_outdeg", "min_outdeg", "targets", "kinds_used",
                  "fixed_rules", "allow_self_target"):
        if kw.get(extra) is not None:
            out["cfg_" + extra] = kw[extra]
    if st == "SAT":
        out["rules"] = info["rules"]
        out["tgt"] = [list(x) for x in info["targets"]]
        out["dfound"] = info["d"]
        out["seed"] = {str(k): v for k, v in info["frames"][0].items() if v}
        out["certified"] = info["certified"]
    elif st == "UNSAT":
        out["nv"] = info["nv"]
        out["nc"] = info["nc"]
    return out


def main():
    jobfile, outfile = sys.argv[1], sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 11
    jobs = json.load(open(jobfile))
    done = set()
    if os.path.exists(outfile):
        for line in open(outfile):
            line = line.strip()
            if line:
                done.add(json.loads(line)["label"])
    jobs = [j for j in jobs if j.get("_label") not in done]
    print("%d jobs (%d already done), %d workers" % (len(jobs), len(done), workers))
    t0 = time.time()
    with open(outfile, "a") as fh, Pool(workers) as pool:
        for i, r in enumerate(pool.imap_unordered(job, jobs, chunksize=1)):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print("[%4d/%4d %6.0fs] %-34s %-6s %6.1fs"
                  % (i + 1, len(jobs), time.time() - t0, r["label"],
                     r["status"], r.get("secs", 0)), flush=True)


if __name__ == "__main__":
    main()
