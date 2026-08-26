#!/usr/bin/env python3
"""jobs.py — build the X-E job files.

  python3 jobs.py map      > data/map.json      # the (n,W,p,d) frontier map
  python3 jobs.py deep     > data/deep.json     # push p at the n=3,W=1 cap
  python3 jobs.py wide     > data/wide.json     # box-width robustness
"""
from __future__ import annotations

import json
import sys
from math import gcd


def coprime_pairs(P, W):
    for p in range(1, P + 1):
        for d in range(1, p * W + 1):
            if gcd(p, d) == 1:
                yield p, d


def spec(n, W, N, p, d, mode="parity", tag=""):
    return dict(_label="n%d W%d N%d p%d d%d %s%s" % (n, W, N, p, d, mode, tag),
                n=n, W=W, N=N, p=p, d=d, mode=mode)


def map_jobs():
    out = []
    # interior = N - 2W ; keep interior fixed at 14 across windows
    for W in (1, 2, 3):
        N = 14 + 2 * W
        for n in (2, 3, 4):
            P = {1: 8, 2: 6, 3: 5}[W]
            if n == 4:
                P = {1: 7, 2: 5, 3: 4}[W]
            for p, d in coprime_pairs(P, W):
                out.append(spec(n, W, N, p, d))
    return out


def deep_jobs():
    """n=3, W=1: is |d|>=3 really impossible, or just beyond p<=8?"""
    out = []
    for p in range(4, 19):
        for d in (3, 4, 5):
            if gcd(p, d) == 1 and d <= p:
                out.append(spec(3, 1, 16, p, d))
    # n=2, W=1: every coprime (p,d) up to p<=14 (cheap)
    for p in range(1, 15):
        for d in range(1, p + 1):
            if gcd(p, d) == 1:
                out.append(spec(2, 1, 16, p, d))
    return out


def wide_jobs():
    """Box-width robustness for the load-bearing UNSATs."""
    out = []
    for N in (18, 20, 22, 24):
        for p, d in [(4, 3), (5, 3), (5, 4), (7, 3)]:
            out.append(spec(3, 1, N, p, d))
        for p, d in [(2, 1), (3, 1), (3, 2), (5, 3)]:
            out.append(spec(2, 1, N, p, d))
    return out




def box_jobs():
    """Box-width audit: is each UNSAT a real no-go or a width artefact?

    interior = N - 2W.  X-A and the X-E map used interior 14.
    """
    out = []
    cases = {
        (2, 1): [(2, 1), (3, 1), (3, 2), (4, 1), (4, 3), (5, 2)],
        (2, 2): [(5, 1), (2, 3), (4, 3), (3, 4), (5, 3), (6, 5)],
        (2, 3): [(3, 5), (5, 4), (2, 5), (4, 5), (5, 6)],
        (3, 1): [(4, 3), (5, 3), (5, 4), (6, 5), (7, 4)],
        (3, 2): [(4, 7), (5, 9), (6, 11)],
        (3, 3): [(4, 11), (5, 13), (5, 14)],
    }
    for (n, W), pds in cases.items():
        for interior in (20, 26):
            N = interior + 2 * W
            for p, d in pds:
                out.append(spec(n, W, N, p, d, tag=" box%d" % interior))
    return out


def pmap_jobs():
    """n=2: which PERIODS are alive?  d=1 and d=2 only, p up to 12."""
    out = []
    for W in (1, 2, 3):
        N = 20 + 2 * W
        for p in range(1, 13):
            for d in (1, 2, 3):
                if gcd(p, d) == 1 and d <= p * W:
                    out.append(spec(2, W, N, p, d, tag=" pmap"))
    return out


if __name__ == "__main__":
    print(json.dumps({"map": map_jobs, "deep": deep_jobs, "wide": wide_jobs,
                      "box": box_jobs, "pmap": pmap_jobs}[sys.argv[1]]()))
