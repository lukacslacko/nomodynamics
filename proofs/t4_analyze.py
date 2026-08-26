#!/usr/bin/env python3
"""
t4_analyze.py -- TARGET 4: post-processing of the censuses.

Adds to every rotor row the TROPICAL (directed light-cone) test, which is
strictly sharper than the symmetric light cone:

  X-E's Tropical Speed Law.  A finite Z glider of period p and displacement d
  obeys   p*min(lam_min,0) <= d <= p*max(lam_max,0),
  lam the extreme cycle means of the amendment digraph (edge k -> t for every
  t in T_k, weight c_k).  Since |c_k| <= W this implies |d| <= pW.

  A ring rotor (S,p,d) is TRANSPORT-ADMISSIBLE if SOME representative
  e = d (mod m) lies in that interval.  Necessary for S to be the wrapping of
  a finite Z glider of period p; strictly stronger than |d| <= pW.

Usage: python3 t4_analyze.py t4_data/t4_n1.jsonl [...]
"""

from __future__ import annotations

import gzip
import itertools
import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

W = 1


def cycle_means(rules, targets, used=None):
    """(lam_min, lam_max) over the simple cycles of the amendment digraph,
    restricted to the kinds actually used.  None if the digraph is acyclic."""
    n = len(rules)
    ks = list(range(n)) if used is None else sorted(used)
    edges = {k: [t for t in targets[k] if t in ks] for k in ks}
    best_lo = best_hi = None
    for start in ks:
        stack = [(start, [start], 0)]
        while stack:
            v, path, wsum = stack.pop()
            for u in edges[v]:
                w2 = wsum + rules[v][2]
                if u == start:
                    mean = Fraction(w2, len(path))
                    best_lo = mean if best_lo is None else min(best_lo, mean)
                    best_hi = mean if best_hi is None else max(best_hi, mean)
                elif u not in path and u > start:
                    stack.append((u, path + [u], w2))
    return best_lo, best_hi


def tropical_ok(rules, targets, used, m, p, d):
    """(admissible?, interval, unique?).  `unique` is False when the tropical
    interval is at least as long as the ring, in which case EVERY rotation is
    admissible and the test says nothing (the aliasing regime)."""
    lo, hi = cycle_means(rules, targets, used)
    if lo is None:                      # acyclic digraph: nothing can move
        return False, None, None, True
    a = p * min(lo, 0)
    b = p * max(hi, 0)
    uniq = (b - a) < m
    for e in (d, d - m, d + m):
        if a <= e <= b:
            return True, a, b, uniq
    return False, a, b, uniq


def opener(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def load(paths):
    rows = []
    for path in paths:
        with opener(path) as fh:
            for line in fh:
                rows.append(json.loads(line))
    return rows


def enrich(rows):
    for r in rows:
        rules = [tuple(x) for x in r["rules"]]
        targets = [tuple(x) for x in r["targets"]]
        ok, a, b, uniq = tropical_ok(rules, targets, set(r["used"]), r["m"],
                                     r["p"], r["d"])
        r["trop"] = ok
        r["trop_uniq"] = uniq
        r["trop_iv"] = [str(a), str(b)]
        # a light cone narrower than the ring: the representative is unique,
        # so the test is not vacuous (2pW >= m makes every rotor "admissible")
        r["lcs"] = r["lc"] and 2 * r["p"] * W < r["m"]
        r["trops"] = ok and uniq
    return rows


def table(rows, title):
    print("\n### %s" % title)
    hdr = ("m", "rotors", "LC", "LCstrict", "LCs&od1", "LCs&od2+", "LCs&gap",
           "TROPs", "TROPs&od1")
    print("  " + " ".join("%9s" % h for h in hdr))
    by_m = {}
    for r in rows:
        by_m.setdefault(r["m"], []).append(r)
    tot = [0] * 8
    for m in sorted(by_m):
        rs = by_m[m]
        lc = [r for r in rs if r["lcs"]]
        vals = [len(rs), len([r for r in rs if r["lc"]]), len(lc),
                len([r for r in lc if r["od"] <= 1]),
                len([r for r in lc if r["od"] >= 2]),
                len([r for r in lc if r["lift"]]),
                len([r for r in rs if r["trops"]]),
                len([r for r in rs if r["trops"] and r["od"] <= 1])]
        tot = [a + b for a, b in zip(tot, vals)]
        print("  %9d " % m + " ".join("%9d" % v for v in vals))
    print("  %9s " % "ALL" + " ".join("%9d" % v for v in tot))


def detail(rows, pred, title, limit=25):
    sel = [r for r in rows if pred(r)]
    print("\n  %s : %d" % (title, len(sel)))
    seen = set()
    for r in sel:
        key = (r["m"], tuple(map(tuple, r["rules"])),
               tuple(map(tuple, r["targets"])), r["mode"], r["p"], r["d"],
               r["g"], r["od"])
        if key in seen:
            continue
        seen.add(key)
        if len(seen) > limit:
            print("      ... (%d distinct signatures total)" % len(
                {(x["m"], tuple(map(tuple, x["rules"])),
                  tuple(map(tuple, x["targets"])), x["mode"], x["p"], x["d"])
                 for x in sel}))
            break
        print("      m=%-3d %s -> %s [%s] p=%d d=%+d g=%d od=%d card=%d L=%d"
              % (r["m"], r["rules"], r["targets"], r["mode"], r["p"], r["d"],
                 r["g"], r["od"], r["card"], r["L"]))
    return sel


if __name__ == "__main__":
    paths = sys.argv[1:]
    rows = enrich(load(paths))
    table(rows, "rotor census: " + ", ".join(os.path.basename(p)
                                             for p in paths))
    detail(rows, lambda r: r["lcs"] and r["od"] <= 1,
           "STRICTLY LIGHT-CONE-ADMISSIBLE (2pW < m) with OUT-DEGREE <= 1  "
           "(counterexamples to the naive converse)")
    detail(rows, lambda r: r["trops"],
           "TRANSPORT-ADMISSIBLE (tropical, non-vacuous) rotors")
    detail(rows, lambda r: r["trops"] and r["od"] <= 1,
           "TRANSPORT-ADMISSIBLE (non-vacuous) with OUT-DEGREE <= 1")
    detail(rows, lambda r: r["lcs"] and r["lift"],
           "STRICTLY LIGHT-CONE-ADMISSIBLE and g >= 2pW "
           "(Theorem B applies: these MUST lift to Z gliders)")
    detail(rows, lambda r: r["trops"] and r["od"] >= 2,
           "TRANSPORT-ADMISSIBLE (non-vacuous) with OUT-DEGREE >= 2")
    gs = sorted({(r["g"], 2 * r["p"] * W) for r in rows if r["lcs"]})
    print("\n  (g, 2pW) pairs seen among strictly light-cone-admissible "
          "rotors: %s" % gs[:40])
