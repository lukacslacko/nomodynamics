#!/usr/bin/env python3
"""balance.py — 2-D balanced constitutions (Expedition X-B, mission 4).

A *balanced constitution* is a code S with Phi(S) = S although some law of S is
still active: the amendments enacted by the active laws cancel exactly, by
parity.  The Dead Letter Theorem of own-kind nomodynamics ("fixed <=> gridlock")
fails here.  Theorem 2 of RESULTS.md says balance needs (a) parity resolution
and (b) a kind with in-degree >= 2 in the amendment digraph.

This module finds MAXIMAL balanced codes inside an n x n box with z3: variables
x[cell][kind], constraint "every slot receives an even number of toggles",
objective "as many active laws as possible".
"""
import sys
import itertools

import z3

from xa2d import Const, state, active, step, verify_balanced, render, card


def solve(C, n=8, want_active=None, maximize=True, timeout=120000):
    """Find a code in [0,n)^2 that is fixed under parity with many active laws."""
    cells = [(x, y) for x in range(n) for y in range(n)]
    halo = [(x, y) for x in range(-1, n + 1) for y in range(-1, n + 1)]
    X = {(c, k): z3.Bool("x_%d_%d_%d" % (c[0], c[1], k))
         for c in cells for k in range(C.n)}

    def occ(j):
        if not (0 <= j[0] < n and 0 <= j[1] < n):
            return z3.BoolVal(False)
        return z3.Or([X[(j, k)] for k in range(C.n)])

    def act(i, k):
        if not (0 <= i[0] < n and 0 <= i[1] < n):
            return z3.BoolVal(False)
        a, b, _ = C.rules[k]
        ja = (i[0] + a[0], i[1] + a[1])
        jb = (i[0] + b[0], i[1] + b[1])
        return z3.And(X[(i, k)], occ(ja), z3.Not(occ(jb)))

    A = {(i, k): act(i, k) for i in cells for k in range(C.n)}
    s = z3.Optimize() if maximize else z3.Solver()
    s.set("timeout", timeout)
    # every slot receives an even number of toggles
    for j in halo:
        for m in range(C.n):
            terms = []
            for k in range(C.n):
                if m not in C.targets[k]:
                    continue
                c = C.rules[k][2]
                i = (j[0] - c[0], j[1] - c[1])
                if 0 <= i[0] < n and 0 <= i[1] < n:
                    terms.append(A[(i, k)])
            if not terms:
                continue
            if len(terms) == 1:
                s.add(z3.Not(terms[0]))
            else:
                s.add(z3.Not(z3.Xor(*terms) if len(terms) == 2
                             else _xor(terms)))
    nact = z3.Sum([z3.If(A[(i, k)], 1, 0)
                   for i in cells for k in range(C.n)])
    if want_active is not None:
        s.add(nact >= want_active)
    if maximize:
        s.maximize(nact)
    if s.check() != z3.sat:
        return None
    M = s.model()
    S = state([(c, k) for c in cells for k in range(C.n)
               if z3.is_true(M.eval(X[(c, k)], model_completion=True))])
    return S


def _xor(terms):
    r = terms[0]
    for t in terms[1:]:
        r = z3.Xor(r, t)
    return r


def report(label, n=8, timeout=120000):
    C = Const.parse(label)
    S = solve(C, n=n, timeout=timeout)
    if S is None:
        return None
    ok = verify_balanced(S, C, "parity")
    na = len(active(S, C))
    return dict(label=label, card=card(S), nactive=na, verified=ok, S=S,
                art=render(S))


CANDIDATES = [
    "OEO>A OEO>A",          # the minimal witness family
    "OSS>A OES>A",          # the two-chamber amendment (nomos2d 5.5)
    "OPP>AB OEP>AB",        # richest found in the census
    "QSS>AB NPP>AB",        # largest card found in the census
    "OPP>AB OPP>AB",
    "OEE>AB OWW>AB",
    "OEW>AB OWE>AB",
    "ONS>AB OSN>AB",
    "OEO>AB OWO>AB",
    "OEN>AB OWS>AB",
]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print("== maximal balanced codes in a %dx%d box (z3, parity) ==\n" % (n, n))
    best = []
    for lab in CANDIDATES:
        r = report(lab, n=n)
        if r is None:
            print("%-16s  UNSAT / timeout" % lab)
            continue
        print("%-16s  card=%-3d active=%-3d verified=%s"
              % (lab, r["card"], r["nactive"], r["verified"]))
        best.append(r)
    best.sort(key=lambda r: (-r["nactive"], -r["card"]))
    print("\n== the richest balanced constitution found ==")
    r = best[0]
    print("constitution: %s   card=%d   active laws=%d   Phi(S)=S: %s"
          % (r["label"], r["card"], r["nactive"], r["verified"]))
    print(r["art"])
    return best


if __name__ == "__main__":
    main()
