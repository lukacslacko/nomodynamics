#!/usr/bin/env python3
"""
rank.py — score the hits of sweep2d.py / sweep1d.py against the strict
rung-2 / rung-3 definition and the two additivity tests.

For each unique (constitution, mode, seed):
  p1          first time with >= 2 causal components, each an exact translate
              of the seed, and ZERO debris                      (rung 2-exact)
  nev, maxc   how many such times up to T, and the largest copy count (rung 3)
  phiNEL      # of steps t <= T with Phi^t(S0) != L^t(S0), L = the
              unconditional linear map                    (does the guard bite)
  splitfail   # of splittings S0 = A u B with
              Phi^{p1}(S0) != Phi^{p1}(A) xor Phi^{p1}(B)   (NON-ADDITIVITY)
  atp         Phi^{p1}(S0) != L^{p1}(S0)

GOLD = exact, |supp(seed)| >= 2, splitfail > 0 and atp — a replicator whose
doubling is neither the unconditional linear map nor a superposition of its
own parts.

Usage: python3 rank.py data/s2d_occ.txt [--top 20] [--T 130]
"""

from __future__ import annotations

import argparse
import ast
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from xnomos import Const, step, card, laws                         # noqa
from replib import radius, to_p, pstep                             # noqa
from analyze import linear_map, copy_census                        # noqa


def score(C, S0, mode, T=130, cardcap=3000):
    R = radius(C)
    S = dict(S0)
    L = dict(S0)
    ev = []
    phiNEL = 0
    for t in range(1, T + 1):
        S = step(S, C, mode)
        L = linear_map(L, C)
        if not S or card(S) > cardcap:
            break
        if S != L:
            phiNEL += 1
        nc, ng, deb, anch = copy_census(S, S0, C, R)
        if nc >= 2 and deb == 0:
            ev.append((t, nc, card(S), S != L, tuple(anch)))
    if not ev:
        return None
    p1, nc1, cd1, atp, anch1 = ev[0]
    pl = list(laws(S0))
    fails = tot = 0
    Q = to_p(S0)
    for _ in range(p1):
        Q = pstep(Q, C, mode)
    for r in range(1, len(pl) // 2 + 1):
        for A in itertools.combinations(pl, r):
            Ad, Bd = {}, {}
            for c, k in A:
                Ad[c] = Ad.get(c, 0) | (1 << k)
            for c, k in pl:
                if (c, k) not in A:
                    Bd[c] = Bd.get(c, 0) | (1 << k)
            if not Bd:
                continue
            PA, PB = to_p(Ad), to_p(Bd)
            for _ in range(p1):
                PA = pstep(PA, C, mode)
                PB = pstep(PB, C, mode)
            tot += 1
            if Q != (PA ^ PB):
                fails += 1
    return {"p1": p1, "nev": len(ev), "maxc": max(e[1] for e in ev),
            "phiNEL": phiNEL, "atp": atp, "splitfail": (fails, tot),
            "anchors": anch1, "events": ev[:8], "R": R}


def parse(path):
    out = []
    for line in open(path):
        if line.startswith("#"):
            continue
        d = dict(kv.split("=", 1) for kv in line.strip().split("|"))
        if int(d.get("deb", "1")) != 0:
            continue
        seed = ast.literal_eval(d["seed"])
        if isinstance(seed, tuple):                     # 1-D file format
            seed = list(seed)
        if len(seed) < 2:
            continue
        out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--T", type=int, default=130)
    a = ap.parse_args()
    seen, rows = set(), []
    nfile = 0
    for f in a.files:
        for d in parse(f):
            nfile += 1
            k = (d["rules"], d["targets"], d.get("guards"), d["mode"],
                 d["seed"])
            if k in seen:
                continue
            seen.add(k)
            C = Const(ast.literal_eval(d["rules"]),
                      ast.literal_eval(d["targets"]), dim=2,
                      guards=ast.literal_eval(d["guards"]))
            S0 = {c: m for c, m in ast.literal_eval(d["seed"])}
            try:
                s = score(C, S0, d["mode"], a.T)
            except Exception:
                continue
            if s:
                s["d"] = d
                rows.append(s)
    gold = [r for r in rows if r["splitfail"][0] > 0 and r["atp"]]
    print("exact multi-cell hits read: %d ; unique: %d ; scored: %d"
          % (nfile, len(seen), len(rows)))
    print("GOLD (non-additive AND off the linear map at the event): %d"
          % len(gold))
    gold.sort(key=lambda r: (r["p1"], -r["splitfail"][0] / max(1, r["splitfail"][1]),
                             -r["maxc"]))
    for r in gold[:a.top]:
        d = r["d"]
        print("  p=%-3d nev=%-3d maxcopies=%-3d PhiNEL=%-3d splitfail=%d/%d | "
              "%s %s %s mode=%s seed=%s"
              % (r["p1"], r["nev"], r["maxc"], r["phiNEL"], r["splitfail"][0],
                 r["splitfail"][1], d["rules"], d["targets"], d["guards"],
                 d["mode"], d["seed"]))
    return gold


if __name__ == "__main__":
    main()
