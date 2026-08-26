#!/usr/bin/env python3
"""
sweep2d.py — replicator sweep of 2-D cross-amendment / citation universes.

A hit is a time p at which Phi^p(S0) splits into >= 2 causal components
(sup-distance > 2R apart, Lemma S) each an EXACT translate of the seed.
Debris = the laws in the remaining components.

Each hit also carries two nonlinearity flags:
  bite   : some placed law was INACTIVE (guard blocked) at some step <= p
  nonlin : Phi^t(S0) != L^t(S0) for some t <= p, where L is the unconditional
           linear map (every law fires, guards ignored, parity resolution).
           nonlin = False  <=>  the whole replication is the Fredkin/additive
           phenomenon on that orbit.

Usage: python3 sweep2d.py --trials 200000 --kinds 2 --modes parity,or
                          [--cite] [--seed 0] [--jobs 12] [--out data/x.txt]
"""

from __future__ import annotations

import argparse
import itertools
import os
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

MOORE = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]
K = 1 << 12                    # cell code = x + K*y, K larger than any span


def code(x, y):
    return x + K * y


def decode(c):
    y = (c + K // 2) // K
    return (c - K * y, y)


# ------------------------------------------------------------------ stepping

def run(rules, tmask, guards, mode, S0, steps, cardcap, rel, R, want_lin=True):
    """Return (p, anchors, ncomp, debris, bite, nonlin) of the first
    component-exact replication event, or None."""
    n = len(rules)
    off = [(code(*a), code(*b), code(*c)) for a, b, c in rules]
    S = dict(S0)
    L = dict(S0) if want_lin else None
    bite = False
    nonlin = False
    seen = set()
    span = 2 * R
    seedmap = dict(rel)
    nrel = len(rel)
    for t in range(1, steps + 1):
        # ---- one guarded step, counting blocked laws
        tog = {}
        clear = {}
        enact = {}
        nact = 0
        nlaw = 0
        sup = mode in ("super", "super_or")
        for cell, mask in S.items():
            m = mask
            while m:
                k = (m & -m).bit_length() - 1
                m &= m - 1
                nlaw += 1
                a, b, c = off[k]
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
                nact += 1
                j = cell + c
                if sup:
                    if j in S:
                        clear[j] = clear.get(j, 0) ^ 1
                    else:
                        enact[j] = enact.get(j, 0) | (1 << k)
                elif mode == "parity":
                    tog[j] = tog.get(j, 0) ^ tmask[k]
                else:
                    tog[j] = tog.get(j, 0) | tmask[k]
        if nact < nlaw:
            bite = True
        if sup:
            out = dict(S)
            gone = clear.keys() if mode == "super_or" else \
                [j for j, p in clear.items() if p]
            for j in gone:
                out.pop(j, None)
            for j, mm in enact.items():
                out[j] = out.get(j, 0) | mm
            S = {j: mm for j, mm in out.items() if mm}
        else:
            out = dict(S)
            for j, x in tog.items():
                if not x:
                    continue
                y = out.get(j, 0) ^ x
                if y:
                    out[j] = y
                elif j in out:
                    del out[j]
            S = out
        # ---- the unconditional linear map, in lockstep
        if want_lin and not nonlin:
            tg = {}
            for cell, mask in L.items():
                m = mask
                while m:
                    k = (m & -m).bit_length() - 1
                    m &= m - 1
                    j = cell + off[k][2]
                    tg[j] = tg.get(j, 0) ^ tmask[k]
            o = dict(L)
            for j, x in tg.items():
                y = o.get(j, 0) ^ x
                if y:
                    o[j] = y
                elif j in o:
                    del o[j]
            L = o
            if L != S:
                nonlin = True
        if not S:
            return None
        cd = sum(bin(m).count("1") for m in S.values())
        if cd > cardcap:
            return None
        key = tuple(sorted(S.items()))
        if key in seen:
            return None
        seen.add(key)
        if len(S) < 2 * nrel:
            continue
        # ---- causal components (union-find on the sup-distance-<=2R graph)
        cells = list(S)
        pts = [decode(c) for c in cells]
        par = list(range(len(cells)))

        def find(i):
            while par[i] != i:
                par[i] = par[par[i]]
                i = par[i]
            return i
        for i in range(len(cells)):
            xi, yi = pts[i]
            for j in range(i + 1, len(cells)):
                xj, yj = pts[j]
                if abs(xi - xj) <= span and abs(yi - yj) <= span:
                    ri, rj = find(i), find(j)
                    if ri != rj:
                        par[ri] = rj
        groups = {}
        for i in range(len(cells)):
            groups.setdefault(find(i), []).append(i)
        if len(groups) < 2:
            continue
        anchors, deb = [], 0
        for gp in groups.values():
            if len(gp) == nrel:
                lo = min((pts[i][1], pts[i][0]) for i in gp)
                base = code(lo[1], lo[0])
                if all(S[cells[i]] == seedmap.get(cells[i] - base, -1)
                       for i in gp):
                    anchors.append(decode(base))
                    continue
            deb += sum(bin(S[cells[i]]).count("1") for i in gp)
        if len(anchors) >= 2:
            return (t, sorted(anchors), len(groups), deb, bite, nonlin)
    return None


# -------------------------------------------------------------------- seeds

def gen_seeds(n, boxes):
    full = (1 << n) - 1
    out = []
    for cells in boxes:
        for masks in itertools.product(range(1, full + 1), repeat=len(cells)):
            S = {code(*c): m for c, m in zip(cells, masks)}
            out.append(S)
    return out


BOXES = [
    [(0, 0)],
    [(0, 0), (1, 0)], [(0, 0), (0, 1)], [(0, 0), (1, 1)],
    [(0, 0), (2, 0)], [(0, 0), (0, 2)],
    [(0, 0), (1, 0), (0, 1)], [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]


def task(args):
    (tid, ntrials, nk, modes, cite, steps, cardcap, mincells, sd) = args
    rng = random.Random(sd)
    seeds = gen_seeds(nk, BOXES)
    seeds = [s for s in seeds if len(s) >= mincells]
    tsets = [t for r in range(1, nk + 1)
             for t in itertools.combinations(range(nk), r)]
    gopts = [(None, None)]
    if cite:
        gopts = [(g, h) for g in [None] + list(range(nk))
                 for h in [None] + list(range(nk))]
    hits = []
    for _ in range(ntrials):
        rules = [(rng.choice(MOORE), rng.choice(MOORE), rng.choice(MOORE))
                 for _ in range(nk)]
        ts = [rng.choice(tsets) for _ in range(nk)]
        tmask = [sum(1 << x for x in t) for t in ts]
        guards = [rng.choice(gopts) for _ in range(nk)]
        R = max(max(abs(v) for o in r for v in o) for r in rules)
        mode = rng.choice(modes)
        for S0 in seeds:
            rel = sorted((c - min(S0), m) for c, m in S0.items())
            r = run(rules, tmask, guards, mode, S0, steps, cardcap, rel, R)
            if r:
                hits.append((rules, ts, guards, mode,
                             sorted((decode(c), m) for c, m in S0.items()), r))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=100000)
    ap.add_argument("--kinds", type=int, default=2)
    ap.add_argument("--modes", default="parity,or")
    ap.add_argument("--steps", type=int, default=48)
    ap.add_argument("--cardcap", type=int, default=400)
    ap.add_argument("--mincells", type=int, default=1)
    ap.add_argument("--cite", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--out", default=os.path.join(HERE, "data", "sweep2d.txt"))
    a = ap.parse_args()
    modes = a.modes.split(",")
    per = max(1, a.trials // (a.jobs * 8))
    tasks = [(i, per, a.kinds, modes, a.cite, a.steps, a.cardcap, a.mincells,
              a.seed * 1000003 + i) for i in range((a.trials + per - 1) // per)]
    print("tasks=%d  trials/task=%d  kinds=%d  cite=%s  modes=%s"
          % (len(tasks), per, a.kinds, a.cite, modes), flush=True)
    n = nl = 0
    with open(a.out, "w") as fh:
        fh.write("# sweep2d kinds=%d trials=%d steps=%d cardcap=%d modes=%s "
                 "cite=%s mincells=%d rngseed=%d\n"
                 % (a.kinds, a.trials, a.steps, a.cardcap, a.modes, a.cite,
                    a.mincells, a.seed))
        with Pool(a.jobs) as pool:
            for i, hs in enumerate(pool.imap_unordered(task, tasks)):
                for rules, ts, guards, mode, S0, r in hs:
                    p, anch, ncomp, deb, bite, nonlin = r
                    n += 1
                    nl += bool(nonlin)
                    fh.write("rules=%s|targets=%s|guards=%s|mode=%s|seed=%s|"
                             "p=%d|anchors=%s|ncomp=%d|deb=%d|bite=%d|"
                             "nonlin=%d\n" % (rules, ts, guards, mode, S0, p,
                                              anch, ncomp, deb, int(bite),
                                              int(nonlin)))
                fh.flush()
                if i % 10 == 0:
                    print("  %d/%d hits=%d nonlin=%d" % (i, len(tasks), n, nl),
                          flush=True)
    print("done: %d hits (%d nonlinear) -> %s" % (n, nl, a.out))


if __name__ == "__main__":
    main()
