#!/usr/bin/env python3
"""
t3_sweep.py -- complete width-unbounded sweeps of the single-field W=1 sector.

Because the parity dynamics depends only on (u,v,w) in F_2^9 and the OR
dynamics only on (U,V,W) with U subset V|W, sweeping 512 / 343 classes settles
the sector for EVERY number of kinds, not just n <= 5.

usage:
    python3 t3_sweep.py cap  PMAX [mode]   # d >= 3 for every class, p <= PMAX
    python3 t3_sweep.py full PMAX [mode]   # every (p,d), p <= PMAX
"""
from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from t3_core import all_parity_classes, all_or_classes            # noqa: E402
from t3_decide import decide, check_witness, minimal_pd           # noqa: E402


def reflect(cls):
    """x -> -x on Z:  (u,v,w) -> (rev u, rev w, rev v)."""
    def rev(x):
        return ((x & 1) << 2) | (x & 2) | ((x >> 2) & 1)
    u, v, w = cls
    return (rev(u), rev(w), rev(v))


def sweep(mode, pmax, dmin, out_path, cap=3_000_000):
    classes = all_parity_classes() if mode == "parity" else all_or_classes()
    t0 = time.time()
    recs = []
    n_cap = 0
    worst = 0
    with open(out_path, "w") as fh:
        for idx, cls in enumerate(classes):
            for p in range(1, pmax + 1):
                for d in range(dmin, p + 1):
                    v, cols = decide(cls, p, d, mode, cap=cap)
                    rec = {"cls": list(cls), "mode": mode, "p": p, "d": d,
                           "verdict": v}
                    if v == "GLIDER":
                        assert check_witness(cls, cols, p, d, mode), (cls, p, d)
                        rec["seed"] = [x for x, c in enumerate(cols) if c & 1]
                        rec["span"] = (max(rec["seed"]) - min(rec["seed"]) + 1
                                       if rec["seed"] else 0)
                        rec["min_pd"] = minimal_pd(cls, cols, p, d, mode)
                        worst = max(worst, rec["min_pd"][1] if rec["min_pd"]
                                    else 0)
                    if v == "CAP":
                        n_cap += 1
                    recs.append(rec)
                    fh.write(json.dumps(rec) + "\n")
            if (idx + 1) % 32 == 0:
                print("  %4d/%d classes  %.1fs  CAP=%d  max min-d=%d"
                      % (idx + 1, len(classes), time.time() - t0, n_cap, worst),
                      flush=True)
    return recs, n_cap


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "cap"
    pmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    mode = sys.argv[3] if len(sys.argv) > 3 else "parity"
    dmin = 3 if what == "cap" else 1
    out = os.path.join(HERE, "t3_%s_%s_p%d.jsonl" % (what, mode, pmax))
    recs, n_cap = sweep(mode, pmax, dmin, out)
    g = [r for r in recs if r["verdict"] == "GLIDER"]
    print("\n%s sweep, mode=%s, p<=%d, d>=%d" % (what, mode, pmax, dmin))
    print("  decisions      : %d" % len(recs))
    print("  GLIDER         : %d" % len(g))
    print("  CAP (undecided): %d" % n_cap)
    if g:
        print("  max d realised : %d" % max(r["d"] for r in g))
        md = [r["min_pd"][1] for r in g if r["min_pd"]]
        print("  max MINIMAL d  : %d" % (max(md) if md else 0))
        pds = sorted({(r["min_pd"][0], r["min_pd"][1]) for r in g if r["min_pd"]})
        print("  minimal (p,d)  : %s" % (pds,))
    print("  wrote %s" % out)


if __name__ == "__main__":
    main()
