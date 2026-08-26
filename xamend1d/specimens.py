#!/usr/bin/env python3
"""specimens.py — pull the MINIMAL near-miss specimens out of the smallest
complete worlds and certify each one by independent re-simulation."""
from __future__ import annotations

import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import xnomos                                             # noqa: E402
import fastlib as F                                       # noqa: E402
from nearmiss import scan, certify, show, RULES1          # noqa: E402


def best(consts, seeds, mode, key, worlds_name, topk=2, steps=24, width=52):
    tally, cand = scan(worlds_name, consts, seeds, mode)
    rows = cand[key]
    if not rows:
        print("   (no %s in %s/%s)" % (key, worlds_name, mode))
        return []
    # minimality: fewest placed laws, then smallest period, then smallest |d|
    def w(r):
        S = F.unpack_state(seeds[r[1]])
        return (xnomos.card(S), abs(r[2]), abs(r[3]), r[0])
    rows = sorted(rows, key=w)[:topk]
    out = []
    for ci, si, p, d, nblk in rows:
        rules, targets = consts[ci]
        S0 = F.unpack_state(seeds[si])
        show("SPECIMEN [%s / %s / %s]  p=%d  d=%+d  debris-transitions=%d"
             % (worlds_name, mode, key, p, d, nblk),
             rules, targets, mode, S0, steps=steps, width=width)
        cert = certify(rules, targets, mode, S0, p, d)
        out.append((rules, targets, mode, S0, p, d, cert))
    return out


if __name__ == "__main__":
    print("=" * 78)
    print("E2, L=2 permutation targeting [1,0] — COMPLETE world "
          "(729 consts x 408 canonical seeds <=4 laws/6 cells)")
    print("=" * 78)
    c2 = [(list(r), [1, 0]) for r in itertools.product(RULES1, repeat=2)]
    s2 = F.all_seeds(2, 6, 4)
    for key in ("puffer", "osc_puffer", "gun", "bounded_packet"):
        best(c2, s2, "parity", key, "E2 L=2 [1,0]", topk=1)

    print("\n" + "=" * 78)
    print("E1 supersession, n=2 — COMPLETE world "
          "(729 consts x 1887 canonical seeds <=5 laws/7 cells)")
    print("=" * 78)
    cs = [(list(r), [0, 1]) for r in itertools.product(RULES1, repeat=2)]
    ss = F.all_seeds(2, 7, 5)
    for mode in ("super", "super_or"):
        for key in ("puffer", "osc_puffer", "gun", "bounded_packet"):
            best(cs, ss, mode, key, "SUP n=2", topk=1)
