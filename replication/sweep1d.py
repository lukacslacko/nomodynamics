#!/usr/bin/env python3
"""
sweep1d.py — complete replicator sweep of the 2-kind cross-amendment universe
on Z, window 1.

Scope (stated exactly, per the width correction):
  kinds        2
  offsets      a,b,c in {-1,0,1}    -> 27 rules per kind, 729 rule pairs
  targets      T_0, T_1 in {{0},{1},{0,1}}          -> 9 combinations
  guards       occupancy (chapters 1-2) unless --cite
  modes        parity, or, super, super_or (selectable)
  seeds        every code of span <= SPAN with both end cells occupied
  budget       T steps, card cap CARDCAP

Reports every (constitution, mode, seed) for which some Phi^p(S) contains two
or more pairwise FREE translated copies of S (gap > 2R).

Usage:  python3 sweep1d.py [--span 3] [--steps 40] [--modes parity,or]
                           [--jobs 12] [--out data/sweep1d.txt] [--cite]
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys
from collections import defaultdict
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

OFF = (-1, 0, 1)
RULES = [(a, b, c) for a in OFF for b in OFF for c in OFF]
TSETS = [(0,), (1,), (0, 1)]


# ------------------------------------------------------------------ fast step

def make_step(rules, targets, guards, mode):
    """Specialised 1-D stepper: state = dict {cell: mask}."""
    n = len(rules)

    def step(S):
        tog = {}
        for cell, mask in S.items():
            m = mask
            while m:
                k = (m & -m).bit_length() - 1
                m &= m - 1
                a, b, c = rules[k]
                g, h = guards[k]
                v = S.get(cell + a, 0)
                if g is None:
                    if not v:
                        continue
                elif not (v >> g) & 1:
                    continue
                v = S.get(cell + b, 0)
                if h is None:
                    if v:
                        continue
                elif (v >> h) & 1:
                    continue
                j = cell + c
                tog[j] = tog.get(j, 0) ^ targets[k] if mode == "parity" \
                    else tog.get(j, 0) | targets[k]
        out = dict(S)
        for j, x in tog.items():
            if not x:
                continue
            y = out.get(j, 0) ^ x
            if y:
                out[j] = y
            elif j in out:
                del out[j]
        return out

    def step_super(S):
        clear = {}
        enact = {}
        for cell, mask in S.items():
            m = mask
            while m:
                k = (m & -m).bit_length() - 1
                m &= m - 1
                a, b, c = rules[k]
                g, h = guards[k]
                v = S.get(cell + a, 0)
                if g is None:
                    if not v:
                        continue
                elif not (v >> g) & 1:
                    continue
                v = S.get(cell + b, 0)
                if h is None:
                    if v:
                        continue
                elif (v >> h) & 1:
                    continue
                j = cell + c
                if j in S:
                    clear[j] = clear.get(j, 0) ^ 1
                else:
                    enact[j] = enact.get(j, 0) | (1 << k)
        out = dict(S)
        gone = clear.keys() if mode == "super_or" else \
            [j for j, p in clear.items() if p]
        for j in gone:
            out.pop(j, None)
        for j, m in enact.items():
            out[j] = out.get(j, 0) | m
        return {j: m for j, m in out.items() if m}

    return step_super if mode in ("super", "super_or") else step


# --------------------------------------------------------------- copy finding

def free_copies(St, rel, mask0, R):
    """Max family of pairwise free (gap > 2R) copies of the seed in St.

    rel: list of (offset-from-anchor, mask), rel[0] = (0, mask0).
    Returns list of anchor cells, or [] if fewer than two.
    """
    anchors = []
    for cell, m in St.items():
        if (m & mask0) != mask0:
            continue
        ok = True
        for r, mm in rel:
            if (St.get(cell + r, 0) & mm) != mm:
                ok = False
                break
        if ok:
            anchors.append(cell)
    if len(anchors) < 2:
        return []
    lo = rel[0][0]
    hi = max(r for r, _ in rel)
    anchors.sort()
    # copies are intervals [a+lo, a+hi]; free iff next start - prev end > 2R
    chosen = [anchors[0]]
    for a in anchors[1:]:
        if a + lo - (chosen[-1] + hi) > 2 * R:
            chosen.append(a)
    return chosen if len(chosen) >= 2 else []


def seeds_of_span(span, n=2):
    """All codes on cells 0..span-1 with cells 0 and span-1 occupied."""
    full = (1 << n) - 1
    if span == 1:
        for m in range(1, full + 1):
            yield {0: m}
        return
    inner = list(range(0, full + 1))
    for m0 in range(1, full + 1):
        for me in range(1, full + 1):
            for mid in itertools.product(inner, repeat=span - 2):
                S = {0: m0, span - 1: me}
                for i, mm in enumerate(mid):
                    if mm:
                        S[i + 1] = mm
                yield S


def run_one(args):
    (ri, rj, ti, tj, gi, gj, mode, seeds, steps, cardcap, mincells) = args
    rules = [RULES[ri], RULES[rj]]
    tmask = [sum(1 << t for t in TSETS[ti]), sum(1 << t for t in TSETS[tj])]
    guards = [gi, gj]
    R = max(max(abs(x) for x in r) for r in rules)
    stp = make_step(rules, tmask, guards, mode)
    hits = []
    for S0 in seeds:
        if len(S0) < mincells:
            continue
        lo = min(S0)
        mask0 = S0[lo]
        rel = sorted((c - lo, m) for c, m in S0.items())
        card0 = sum(bin(m).count("1") for m in S0.values())
        S = dict(S0)
        seen = set()
        best = None
        for t in range(1, steps + 1):
            S = stp(S)
            if not S:
                break
            cd = sum(bin(m).count("1") for m in S.values())
            if cd > cardcap:
                break
            key = tuple(sorted(S.items()))
            if key in seen:
                break
            seen.add(key)
            if cd < 2 * card0:
                continue
            fam = free_copies(S, rel, mask0, R)
            if len(fam) >= 2:
                cov = {}
                for a in fam:
                    for r, m in rel:
                        cov[a + r] = cov.get(a + r, 0) | m
                deb = 0
                for c, m in S.items():
                    deb += bin(m & ~cov.get(c, 0)).count("1")
                cand = (deb, -len(fam), t, tuple(fam), cd)
                if best is None or cand < best:
                    best = cand
                if deb == 0:
                    break                 # cannot do better
        if best is not None:
            deb, nf, t, fam, cd = best
            hits.append((ri, rj, ti, tj, gi, gj, mode,
                         tuple(sorted(S0.items())), t, fam, deb, cd))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--span", type=int, default=3)
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--cardcap", type=int, default=200)
    ap.add_argument("--modes", default="parity,or")
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--out", default=os.path.join(HERE, "data", "sweep1d.txt"))
    ap.add_argument("--cite", action="store_true",
                    help="also sweep citation guards (g,h in {None,0,1})")
    ap.add_argument("--mincells", type=int, default=2)
    a = ap.parse_args()

    seeds = []
    for sp in range(1, a.span + 1):
        seeds.extend(seeds_of_span(sp))
    modes = a.modes.split(",")
    gopts = [(None, None)]
    if a.cite:
        gopts = [(g, h) for g in (None, 0, 1) for h in (None, 0, 1)]

    tasks = []
    for ri in range(27):
        for rj in range(27):
            for ti in range(3):
                for tj in range(3):
                    for gi in gopts:
                        for gj in gopts:
                            for mode in modes:
                                tasks.append((ri, rj, ti, tj, gi, gj, mode,
                                              seeds, a.steps, a.cardcap,
                                              a.mincells))
    print("tasks: %d   seeds/task: %d   steps: %d" %
          (len(tasks), len(seeds), a.steps), flush=True)

    nhit = 0
    with open(a.out, "w") as fh:
        fh.write("# sweep1d span<=%d steps=%d cardcap=%d modes=%s cite=%s "
                 "mincells=%d\n" % (a.span, a.steps, a.cardcap, a.modes,
                                    a.cite, a.mincells))
        with Pool(a.jobs) as pool:
            for i, hits in enumerate(pool.imap_unordered(run_one, tasks,
                                                         chunksize=64)):
                for h in hits:
                    ri, rj, ti, tj, gi, gj, mode, S0, t, fam, deb, cd = h
                    fh.write("%s|%s|%s|%s|%s|%s|%s|%s|p=%d|copies=%s|deb=%d|"
                             "card=%d\n" % (RULES[ri], RULES[rj], TSETS[ti],
                                            TSETS[tj], gi, gj, mode, S0, t,
                                            fam, deb, cd))
                    nhit += 1
                if i % 20000 == 0:
                    print("  %d/%d  hits=%d" % (i, len(tasks), nhit),
                          flush=True)
    print("done: %d hits -> %s" % (nhit, a.out))


if __name__ == "__main__":
    main()
