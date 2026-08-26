#!/usr/bin/env python3
"""
deep.py — mechanism analysis of the champion long cycles, the Garden-of-Eden
census, and resolution of the Z-holdouts left by unroll.py.

Mechanism model (established for own-kind by Expedition N-C, extended here):
along a cycle the occupancy trajectory O_n is periodic with some period q | p;
given the occupancy, each step is the F2-linear map M_n = I + N(O_n) on
F2^(n*m).  The monodromy T = M_{q-1} ... M_0 is linear, and

        p = q * ord(T on X).

Own-kind forces N nilpotent (window 1) => T unipotent => ord a power of 2.
Cross-amendment makes N block-cyclic and NOT nilpotent, so ord(T) can be the
order of an arbitrary F2 polynomial.  This is the whole story of the period
spectrum, and it is what the numbers below exhibit.
"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("XR_RAW", os.path.join(HERE, "raw"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import xnomos                                        # noqa: E402
from xring import Ring, decode                       # noqa: E402
from certify import to_dict, MODENAME                # noqa: E402


# ---------------------------------------------------------------- mechanism

def linear_step_matrix(R, O):
    """The F2 matrix of X -> X + emissions with the guards frozen at
    occupancy O.  Columns indexed by (kind, cell); returned as a list of
    column bitmasks over n*m bits."""
    n, m = R.n, R.m
    cols = []
    for k in range(n):
        for i in range(m):
            X = [0] * n
            X[k] = 1 << i
            X = tuple(X)
            act = []
            for kk in range(n):
                a, b, _ = R.rules[kk]
                act.append(X[kk] & R.rot(O, -a) & ~R.rot(O, -b) & R.mask)
            out = list(X)
            for kk in range(n):
                out[R.targets[kk]] ^= R.rot(act[kk], R.rules[kk][2])
            v = 0
            for kk in range(n):
                v |= out[kk] << (kk * m)
            cols.append(v)
    return cols


def matmul(A, B, dim):
    """Compose column-list matrices over F2: (A o B) column j = A applied to
    B's column j."""
    out = []
    for col in B:
        v = 0
        c = col
        while c:
            b = (c & -c).bit_length() - 1
            c &= c - 1
            v ^= A[b]
        out.append(v)
    return out


def apply(A, v):
    out = 0
    while v:
        b = (v & -v).bit_length() - 1
        v &= v - 1
        out ^= A[b]
    return out


def mechanism(rules, targets, m, mode, X, p):
    R = Ring(list(rules), list(targets), m, mode)
    orb = [X]
    Y = X
    for _ in range(p - 1):
        Y = R.step(Y)
        orb.append(Y)
    occ = [R.occ(Z) for Z in orb]
    q = next(t for t in range(1, p + 1)
             if p % t == 0 and all(occ[(i + t) % p] == occ[i]
                                   for i in range(p)))
    dim = R.n * m
    T = [1 << i for i in range(dim)]
    for i in range(q):
        T = matmul(linear_step_matrix(R, occ[i]), T, dim)
    v0 = 0
    for k in range(R.n):
        v0 |= X[k] << (k * m)
    v, order = v0, 0
    for t in range(1, 4 * p + 4):
        v = apply(T, v)
        if v == v0:
            order = t
            break
    cards = sorted(set(R.card(Z) for Z in orb))
    return {"p": p, "occ_period": q, "monodromy_order": order,
            "q_times_ord": q * order, "cards": cards,
            "occ_states": len(set(occ))}


def champions():
    print("=== champion long cycles: mechanism decomposition ===")
    print("   p = (occupancy period q) x (order of the F2 monodromy on X)\n")
    picks = []
    for tag in ("own", "own2", "own3", "recip", "noninj", "cyc3", "super2",
                "super3", "big2"):
        path = os.path.join(RAW, tag + ".jsonl")
        if not os.path.exists(path):
            continue
        best = {}
        for line in open(path):
            r = json.loads(line)
            ps = {int(k): v for k, v in r["periods"].items()}
            if not ps:
                continue
            p = max(ps)
            key = (tag, r["m"])
            if key not in best or p > best[key][0]:
                best[key] = (p, ps[p][1], ps[p][2], r)
        for key, (p, card, rep, r) in sorted(best.items()):
            if p >= 14:
                picks.append((tag, r, p, card, rep))
    for tag, r, p, card, rep in picks:
        n, m, mode = r["n"], r["m"], MODENAME[r["mode"]]
        X = decode(rep, n, m)
        d = mechanism([tuple(x) for x in r["rules"]], r["targets"], m, mode,
                      X, p)
        R = Ring([tuple(x) for x in r["rules"]], r["targets"], m, mode)
        ok = (d["q_times_ord"] == p)
        print("  %-8s m=%-3d p=%-4d laws=%-3d  q=%-3d ord=%-5d q*ord=%-5d %s"
              % (tag, m, p, card, d["occ_period"], d["monodromy_order"],
                 d["q_times_ord"], "OK" if ok else "MISMATCH"))
        print("           %s   %s -> %s  occupancies on cycle: %d, cards %s"
              % (R.render(X), r["rules"], r["targets"], d["occ_states"],
                 d["cards"]))
    return picks


# ------------------------------------------------------------------- Eden

def eden():
    print("\n=== Garden of Eden on rings (complete state spaces) ===")
    path = os.path.join(RAW, "goe.jsonl")
    agg = {}
    for line in open(path):
        r = json.loads(line)
        crossed = not all(r["targets"][k] == k for k in range(r["n"]))
        key = (r["m"], MODENAME[r["mode"]],
               "cross" if crossed else "own-kind")
        a = agg.setdefault(key, [0, 0, 0, 0])
        a[0] += r["goe"]
        a[1] += r["N"]
        a[2] += r["nfix"]
        a[3] += 1
    print("   m  semantics   class      GoE fraction   fixed fraction  consts")
    for key in sorted(agg):
        g, N, f, c = agg[key]
        print("  %3d  %-10s %-9s  %12.4f  %14.6f  %5d"
              % (key[0], key[1], key[2], g / N, f / N, c))


# ---------------------------------------------------------------- holdouts

def holdouts():
    print("\n=== resolving the Z-holdouts of unroll.py (10x budget) ===")
    from unroll import gallery
    G = gallery(["own", "own2", "own3", "recip", "noninj", "cyc3", "cyc3all",
                 "super2", "super3", "big2"])
    tally = Counter()
    for (m, p, r, j, rules, tg, mode), (card, rep) in G:
        n = len(rules)
        X = decode(rep, n, m)
        S = to_dict(X, m)
        C = xnomos.Const(list(rules), list(tg), dim=1, modulus=None)
        res = xnomos.classify(S, C, MODENAME[mode], max_steps=600,
                              max_card=300, max_span=300)
        if res["kind"] != xnomos.UNRESOLVED:
            continue
        res2 = xnomos.classify(S, C, MODENAME[mode], max_steps=6000,
                               max_card=3000, max_span=3000)
        tally[res2["kind"]] += 1
        if res2["kind"] == xnomos.GLIDER:
            print("   *** GLIDER ON Z ***", m, rules, tg, MODENAME[mode],
                  sorted(S.items()), res2)
    print("   holdouts re-run at 10x budget:", dict(tally))


if __name__ == "__main__":
    champions()
    eden()
    holdouts()
