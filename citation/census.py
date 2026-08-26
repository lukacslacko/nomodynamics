#!/usr/bin/env python3
"""
census.py — the complete citation census of chapter three.

THE BOX (stated exactly, and it is a box, not a question):

    n = 2 kinds;  dimension 1 on Z;  window W = 1 (all offsets in {-1,0,1});
    every rule (a,b,c) in {-1,0,1}^3                         27 choices
    every target set T subset of {0,1}                        4 choices
    every citation pair (g,h) in ({0,1} u {ANY})^2            9 choices
      => 972 kinds per slot, 972^2 = 944,784 constitutions;
    every seed inside 3 cells with the leftmost cell occupied  48 seeds
      (= every nonempty code of span <= 3, up to translation);
    both resolutions (parity, OR).

    Stage 1 budgets: 200 steps, card <= 200, span <= 120.
    Stage 2 (residue only): 1500 steps, card <= 1200, span <= 1500.

The constitution set is quotiented by the symmetry group
    G = <mirror> x <kind relabelling>  (order 2 * 2! = 4)
and each orbit representative is weighted by its orbit size.  The seed set is
closed under G (see RESULTS.md, Lemma S), so the quotient is exact.

Usage:
    python3 census.py stage1 [--procs 12]
    python3 census.py stage2 [--procs 12]
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cite as ct                                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

N = 2
KINDS = ct.all_kinds(N)
SEEDS = ct.seeds_span(3, N)
MODES = ("parity", "or")

S1 = dict(max_steps=200, max_card=200, max_span=120)
S2 = dict(max_steps=1500, max_card=1200, max_span=1500)


def const_of(i, j):
    k1, k2 = KINDS[i], KINDS[j]
    return ct.Cit([k1[0], k2[0]], [k1[1], k2[1]], [k1[2], k2[2]])


def reps():
    """Orbit representatives of the constitution box, with orbit sizes."""
    out = []
    seen = set()
    for i in range(len(KINDS)):
        for j in range(len(KINDS)):
            C = const_of(i, j)
            k = C.key()
            if k in seen:
                continue
            o = ct.orbit_of(C)
            for kk in o:
                seen.add(kk)
            out.append((i, j, len(o)))
    return out


def _work(chunk):
    """chunk = list of (i, j, orbit_size).  Returns aggregates."""
    counts = Counter()
    gliders = []
    residue = []
    feat = Counter()
    for (i, j, w) in chunk:
        C = const_of(i, j)
        gl = ct.gridlocked(C)
        od = C.outdeg()
        for mode in MODES:
            for si, s in enumerate(SEEDS):
                r = ct.classify(list(s), C, mode, **S1)
                kind = r["kind"]
                counts[(mode, kind)] += w
                counts[(mode, kind, "gl", gl)] += w
                counts[(mode, kind, "od", od)] += w
                if kind == ct.GLIDER:
                    gliders.append((i, j, si, mode, r["period"],
                                    r["displacement"], r["card"], w))
                elif kind in (ct.GROWING, ct.UNRESOLVED):
                    residue.append((i, j, si, mode))
                elif kind == ct.CYCLE:
                    feat[("period", mode, min(r["period"], 64))] += w
        feat[("consts", gl, od)] += w
    return counts, gliders, residue, feat


def chunks(lst, m):
    for a in range(0, len(lst), m):
        yield lst[a:a + m]


def stage1(procs):
    t0 = time.time()
    R = reps()
    print("orbit representatives: %d   (box: %d constitutions)"
          % (len(R), len(KINDS) ** 2))
    print("  weight check: sum of orbit sizes = %d" % sum(w for _, _, w in R))
    counts = Counter()
    feat = Counter()
    gliders, residue = [], []
    with Pool(procs) as p:
        for c, g, rs, f in p.imap_unordered(_work, list(chunks(R, 400))):
            counts.update(c)
            feat.update(f)
            gliders.extend(g)
            residue.extend(rs)
    print("stage1 done in %.1f s" % (time.time() - t0))
    with open(os.path.join(DATA, "census1.json"), "w") as fh:
        json.dump({"counts": {repr(k): v for k, v in counts.items()},
                   "feat": {repr(k): v for k, v in feat.items()},
                   "n_reps": len(R), "n_box": len(KINDS) ** 2,
                   "n_seeds": len(SEEDS), "budgets": S1,
                   "n_gliders": len(gliders), "n_residue": len(residue)},
                  fh, indent=1)
    with open(os.path.join(DATA, "gliders1.txt"), "w") as fh:
        for g in gliders:
            fh.write("%d %d %d %s %d %d %d %d\n" % g)
    with open(os.path.join(DATA, "residue1.txt"), "w") as fh:
        for r in residue:
            fh.write("%d %d %d %s\n" % r)
    for mode in MODES:
        tot = sum(v for k, v in counts.items() if len(k) == 2 and k[0] == mode)
        print("\n-- %s (weighted runs: %d)" % (mode, tot))
        for cl in ct.CLASSES:
            v = counts[(mode, cl)]
            print("   %-11s %12d  %6.3f%%" % (cl, v, 100.0 * v / tot))


def _work2(chunk):
    out = Counter()
    gl, res = [], []
    for (i, j, si, mode) in chunk:
        C = const_of(i, j)
        r = ct.classify(list(SEEDS[si]), C, mode, **S2)
        out[r["kind"]] += 1
        if r["kind"] == ct.GLIDER:
            gl.append((i, j, si, mode, r["period"], r["displacement"],
                       r["card"]))
        elif r["kind"] == ct.UNRESOLVED:
            res.append((i, j, si, mode))
    return out, gl, res


def stage2(procs):
    t0 = time.time()
    rows = []
    with open(os.path.join(DATA, "residue1.txt")) as fh:
        for line in fh:
            a, b, c, m = line.split()
            rows.append((int(a), int(b), int(c), m))
    print("stage-2 residue runs: %d" % len(rows))
    out = Counter()
    gl, res = [], []
    with Pool(procs) as p:
        for o, g, r in p.imap_unordered(_work2, list(chunks(rows, 500))):
            out.update(o)
            gl.extend(g)
            res.extend(r)
    print("stage2 done in %.1f s" % (time.time() - t0))
    print(dict(out))
    print("new gliders found in the residue: %d" % len(gl))
    with open(os.path.join(DATA, "gliders2.txt"), "w") as fh:
        for g in gl:
            fh.write("%d %d %d %s %d %d %d\n" % g)
    with open(os.path.join(DATA, "residue2.txt"), "w") as fh:
        for r in res:
            fh.write("%d %d %d %s\n" % r)
    with open(os.path.join(DATA, "census2.json"), "w") as fh:
        json.dump({"counts": dict(out), "budgets": S2,
                   "n_rows": len(rows), "n_new_gliders": len(gl),
                   "n_unresolved": len(res)}, fh, indent=1)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stage1"
    pr = 12
    if "--procs" in sys.argv:
        pr = int(sys.argv[sys.argv.index("--procs") + 1])
    {"stage1": stage1, "stage2": stage2}[cmd](pr)
