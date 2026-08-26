#!/usr/bin/env python3
"""
sharpness.py — is the theory SHARP?

Theorems 1/2/2' give a NECESSARY condition on the pair (amendment digraph D,
displacement offsets c) for a glider to exist.  Here we test whether it is also
SUFFICIENT, by deciding — exactly, with the SAT instrument — every combination
of (target matrix T, displacement vector c) at n = 2 and n = 3, W = 1, with the
guards (a,b) left free for the solver.

Necessary condition NC(T, c):
  for every nonempty predecessor-closed C' of the digraph, D[C'] contains a
  zero-weight directed cycle, or two cycles of strictly opposite sign.
(Applied with C' ranging over subsets of ALL kinds — a glider may use only some
kinds, so the honest test is: NC holds for SOME nonempty subset C of kinds that
is a candidate support, i.e. NC(T|C, c|C) holds for the induced digraph.)
"""
from __future__ import annotations

import itertools, json, os, sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import xsat
from xsat import Spec


def cycles_of(T, c, C):
    """All simple directed cycle weights of D[C]  (T[k] = tuple of targets)."""
    C = sorted(C)
    out = []
    for start in C:
        stack = [(start, 0, frozenset([start]))]
        while stack:
            v, w, seen = stack.pop()
            for m in T[v]:
                if m not in C:
                    continue
                if m == start:
                    out.append(w + c[v])
                elif m not in seen and m > start:
                    stack.append((m, w + c[v], seen | {m}))
    return out


def pred_closed_subsets(T, C):
    """All nonempty predecessor-closed subsets of C in D[C]."""
    C = set(C)
    res = []
    for r in range(1, len(C) + 1):
        for sub in itertools.combinations(sorted(C), r):
            s = set(sub)
            ok = all((k not in C) or (m not in s) or (k in s)
                     for k in C for m in T[k])
            if ok:
                res.append(s)
    return res


def nc_holds(T, c, C):
    """The necessary condition of Theorems 1/2' for support set C."""
    for Cp in pred_closed_subsets(T, C):
        z = cycles_of(T, c, Cp)
        if not z:
            return False                          # acyclic -> d = 0
        if all(x > 0 for x in z) or all(x < 0 for x in z):
            return False
        if all(x == 0 for x in z):
            return False                          # Theorem 1: d = 0
    return True


def predicted(T, c, n):
    """Theory says a glider is POSSIBLE iff NC holds for some nonempty C."""
    for r in range(1, n + 1):
        for C in itertools.combinations(range(n), r):
            if nc_holds(T, c, set(C)):
                return True
    return False


def decide(args):
    T, c, n, N, P, mode = args
    for p in range(1, P + 1):
        sp = Spec(n=n, W=1, N=N, p=p, d=[x for x in range(-p, p + 1) if x], mode=mode,
                  targets=[tuple(t) for t in T],
                  fixed_rules=[(None, None, c[k]) for k in range(n)])
        st, info = xsat.solve(sp, timeout=900)
        if st == "SAT":
            return (T, c, True, p, info["d"])
        if st == "TIMEOUT":
            return (T, c, None, p, 0)
    return (T, c, False, 0, 0)


def main(n=2, N=14, P=6, mode="parity"):
    tsets = [t for r in range(1, n + 1)
             for t in itertools.combinations(range(n), r)]
    jobs = []
    for T in itertools.product(tsets, repeat=n):
        for c in itertools.product((-1, 0, 1), repeat=n):
            jobs.append((list(T), list(c), n, N, P, mode))
    print("n=%d %s: %d (target-matrix, c-vector) universes, COMPLETE" %
          (n, mode, len(jobs)))
    agree = dis1 = dis2 = 0
    sat = 0
    bad = []
    gliders = []
    with Pool(4) as pool:
        for (T, c, got, p, d) in pool.imap_unordered(decide, jobs, chunksize=8):
            pred = predicted([tuple(t) for t in T], c, n)
            if got is None:
                continue
            sat += bool(got)
            if got:
                gliders.append(dict(T=[list(x) for x in T], c=list(c), p=p, d=d))
            if got == pred:
                agree += 1
            elif got and not pred:
                dis1 += 1
                bad.append(("THEOREM VIOLATED", T, c, p, d))
            else:
                dis2 += 1
                if len(bad) < 12:
                    bad.append(("permitted-but-empty", T, c))
    print("  glider EXISTS in %d universes (decided by SAT, p<=%d, N=%d)" % (sat, P, N))
    print("  theory & machine agree      : %d" % agree)
    print("  glider exists but theory forbids it (WOULD REFUTE THE THEOREMS): %d" % dis1)
    print("  theory permits but no glider found in the box                  : %d" % dis2)
    for b in bad[:12]:
        print("   ", b)
    gliders.sort(key=lambda g: (g["p"], g["c"]))
    print("  gliding universes:")
    for g in gliders[:40]:
        print("    T=%s c=%s  minimal p=%d d=%d" % (g["T"], g["c"], g["p"], g["d"]))
    return dict(n=n, mode=mode, total=len(jobs), sat=sat, agree=agree,
                violated=dis1, permitted_empty=dis2, gliders=gliders)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    P = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    md = sys.argv[4] if len(sys.argv) > 4 else "parity"
    r = main(n, N, P, md)
    f = os.path.join(HERE, "data", "sharpness_n%d_%s.json" % (n, md))
    json.dump(r, open(f, "w"), indent=1)
    print("written", f)
