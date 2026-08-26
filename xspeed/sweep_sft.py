#!/usr/bin/env python3
"""
sweep_sft.py — width-unbounded sweeps over full-target constitutions.

    python3 sweep_sft.py n W pmax dmax out.jsonl [workers] [cap]

For every multiset of `n` live channels (a,b,c) in {-W..W}^3 with a != b (a
channel with a == b is never active and just reduces the kind count), and every
(p,d) with 1 <= p <= pmax, 1 <= d <= min(dmax, p*W), decides EXACTLY — with no
bound on the pattern width — whether a glider with F^p = sigma^d exists, in
both resolutions.  Every GLIDER verdict is re-verified by
`xnomos.verify_glider`.

Pruning that loses nothing (full targets, so D[C] is complete with self-loops):
Theorem 1 needs max_k c_k >= d/p > 0 and Theorem 2 needs a non-positive cycle,
i.e. min_k c_k <= 0.  Constitutions failing either cannot glide with d > 0.
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "xamend1d"))
sys.path.insert(0, os.path.dirname(HERE))

import sft  # noqa: E402


def live_channels(W):
    return [(a, b, c)
            for a in range(-W, W + 1)
            for b in range(-W, W + 1)
            for c in range(-W, W + 1)
            if a != b]


def constitutions(n, W):
    return list(itertools.combinations_with_replacement(live_channels(W), n))


def job(arg):
    chans, W, pd_list, cap = arg
    cmax = max(c for _, _, c in chans)
    cmin = min(c for _, _, c in chans)
    out = []
    if cmax < 1 or cmin > 0:          # Theorem 1 / Theorem 2 prune (d > 0)
        return out
    for (p, d) in pd_list:
        if d > p * cmax:              # Theorem 1
            continue
        for mode in ("parity", "or"):
            t0 = time.time()
            tab = sft.step_table(list(chans), W, mode)
            v, w = sft._search_cycle(tab, W, p, d, cap)
            rec = dict(chans=[list(c) for c in chans], W=W, p=p, d=d,
                       mode=mode, verdict=v, secs=round(time.time() - t0, 2))
            if v == "GLIDER":
                rec["cells"] = sft.witness_state(w, p)
                rec["verified"] = sft.verify(list(chans), w, p, d, mode,
                                             len(chans))
            out.append(rec)
    return out


def main():
    n, W, pmax, dmax = (int(x) for x in sys.argv[1:5])
    outfile = sys.argv[5]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 8
    cap = int(sys.argv[7]) if len(sys.argv) > 7 else 2_000_000
    pd_list = [(p, d) for p in range(1, pmax + 1)
               for d in range(1, min(dmax, p * W) + 1)]
    cons = constitutions(n, W)
    print("n=%d W=%d: %d constitutions x %d (p,d) x 2 modes"
          % (n, W, len(cons), len(pd_list)), flush=True)
    args = [(c, W, pd_list, cap) for c in cons]
    t0 = time.time()
    ngl = 0
    with open(outfile, "a") as fh, Pool(workers) as pool:
        for i, recs in enumerate(pool.imap_unordered(job, args, chunksize=4)):
            for r in recs:
                if r["verdict"] != "NONE":
                    fh.write(json.dumps(r) + "\n")
                    if r["verdict"] == "GLIDER":
                        ngl += 1
            fh.flush()
            if (i + 1) % 50 == 0:
                print("[%5d/%5d %6.0fs] gliders=%d"
                      % (i + 1, len(cons), time.time() - t0, ngl), flush=True)
    print("done: %d glider records, %.0fs" % (ngl, time.time() - t0))


if __name__ == "__main__":
    main()
