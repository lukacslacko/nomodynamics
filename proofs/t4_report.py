#!/usr/bin/env python3
"""
t4_report.py -- TARGET 4: the consolidated tables, printed from the raw data.

Run after the censuses in t4_data/.  Every number quoted in the write-up is
printed here.
"""

from __future__ import annotations

import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from t4_analyze import enrich, load
from t4_verify import row_ring, row_state

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "t4_data")
W = 1


def block(paths, title):
    files = [p for p in paths if os.path.exists(p)]
    if not files:
        print("\n### %s -- NO DATA" % title)
        return []
    rows = enrich(load(files))
    print("\n### %s" % title)
    print("    files: %s" % ", ".join(os.path.basename(f) for f in files))
    hdr = ("m", "rotorcyc", "LC", "LCstrict", "LCs&od<=1", "LCs&od>=2",
           "LCs&gap", "LCs&gap&od<=1")
    print("    " + " ".join("%13s" % h for h in hdr))
    by_m = collections.defaultdict(list)
    for r in rows:
        by_m[r["m"]].append(r)
    tot = [0] * 7
    for m in sorted(by_m):
        rs = by_m[m]
        lcs = [r for r in rs if r["lcs"]]
        v = [len(rs), sum(1 for r in rs if r["lc"]), len(lcs),
             sum(1 for r in lcs if r["od"] <= 1),
             sum(1 for r in lcs if r["od"] >= 2),
             sum(1 for r in lcs if r["lift"]),
             sum(1 for r in lcs if r["lift"] and r["od"] <= 1)]
        tot = [a + b for a, b in zip(tot, v)]
        print("    %13d " % m + " ".join("%13d" % x for x in v))
    print("    %13s " % "TOTAL" + " ".join("%13d" % x for x in tot))
    return rows


def counterexamples(rows):
    sel = [r for r in rows if r["lcs"] and r["od"] <= 1]
    print("\n### THE COUNTEREXAMPLES  (strictly light-cone-admissible, "
          "out-degree <= 1)")
    print("    rotor cycles: %d" % len(sel))
    ap = tr = both = 0
    for r in sel:
        R, X = row_ring(r), row_state(r)
        a = not any(R.rot_state(X, d) == X for d in range(1, r["m"]))
        ap += a
        tr += r["trops"]
        both += a and r["trops"]
    print("    of which rotationally APERIODIC (trivial stabiliser) : %d" % ap)
    print("    of which TRANSPORT-admissible (tropical, non-vacuous): %d" % tr)
    print("    of which BOTH                                        : %d" % both)
    print("    vacant-arc values g occurring                        : %s"
          % sorted({r["g"] for r in sel}))
    sig = collections.OrderedDict()
    for r in sel:
        k = (r["m"], tuple(map(tuple, r["rules"])),
             tuple(map(tuple, r["targets"])), r["mode"], r["p"], r["d"])
        sig[k] = sig.get(k, 0) + 1
    print("    distinct (m, constitution, mode, p, d) signatures     : %d"
          % len(sig))
    for k, v in list(sig.items())[:14]:
        print("      m=%-3d %s -> %s [%s] p=%d d=%+d   x%d"
              % (k[0], list(k[1]), [list(t) for t in k[2]], k[3], k[4], k[5],
                 v))
    if len(sig) > 14:
        print("      ... %d more" % (len(sig) - 14))


if __name__ == "__main__":
    r1 = block([os.path.join(D, "t4_n1.jsonl")],
               "1 KIND -- all 27 rules x 2 target maps, m = 3..22, "
               "COMPLETE over all 2^m codes and all periods")
    r2 = block(sorted(glob.glob(os.path.join(D, "t4_n2_*.jsonl"))),
               "2 KINDS -- all 729 rule pairs x all 16 target maps, "
               "parity+or, COMPLETE over all 2^(2m) codes and all periods")
    r3 = block(sorted(glob.glob(os.path.join(D, "t4_od1_*.jsonl"))),
               "2 KINDS, OUT-DEGREE <= 1 -- all 729 rule pairs x the 9 maps "
               "with |T_k| <= 1, parity+or, COMPLETE")
    counterexamples(r1 + r2 + r3)
