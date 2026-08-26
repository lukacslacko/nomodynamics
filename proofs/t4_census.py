#!/usr/bin/env python3
"""
t4_census.py -- TARGET 4 (c): complete ring-rotor censuses, with the
light-cone / out-degree / vacant-arc classification of every rotor found.

For a given (n kinds, ring size m, mode) the WHOLE state space 2^(n*m) is
enumerated -- so each census is complete over all codes of all law counts and
over all periods (no period bound; the cycle decomposition is exact).  The only
bounds are m, n, and which constitutions the class contains; those are printed
with every table.

Each rotor cycle is reported with
    p    minimal period with Phi^p(S) = rot_d(S)
    d    the representative of the rotation in (-m/2, m/2]
    LC   light-cone-admissible in the STRICT (glider-speed) sense |d| <= p*W
    LC2  admissible in the X-C information sense |d| <= 2*p*W
    od   max out-degree |targets[k]| over the kinds USED on the cycle
    g    the largest vacant arc over the states of the cycle
    lift g >= 2*p*W, the hypothesis of the Lift Theorem

Usage:  python3 t4_census.py n1            # 1 kind, m = 3..22, all 27 rules
        python3 t4_census.py n2 M0 M1      # 2 kinds, m in [M0,M1], all 16 maps
        python3 t4_census.py od1 M0 M1     # 2 kinds, out-degree<=1 maps only
"""

from __future__ import annotations

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from t4_ring import Ring, vacant_arc, rep, verify_rotation_recurrence, \
    verify_via_xnomos

OFFS = (-1, 0, 1)
RULES1 = [(a, b, c) for a in OFFS for b in OFFS for c in OFFS]
W = 1

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "t4_data")


# ------------------------------------------------------- vectorised transition

def _rot(x, r, m, mask):
    r %= m
    if r == 0:
        return x
    return ((x << r) | (x >> (m - r))) & mask


def transition(rules, targets, m, n, mode):
    """f[s] = the packed successor of packed state s, for every state."""
    N = 1 << (n * m)
    dt = np.uint32 if n * m <= 31 else np.uint64
    s = np.arange(N, dtype=dt)
    mask = (1 << m) - 1
    X = [(s >> np.array(k * m, dtype=dt)) & dt(mask) for k in range(n)]
    occ = X[0].copy()
    for k in range(1, n):
        occ |= X[k]
    notocc = (~occ) & dt(mask)
    emit = []
    for k in range(n):
        a, b, c = rules[k]
        act = X[k] & _rot(occ, -a, m, mask) & _rot(notocc, -b, m, mask)
        emit.append(_rot(act, c, m, mask))
    out = np.zeros(N, dtype=dt)
    for t in range(n):
        f = np.zeros(N, dtype=dt)
        for k in range(n):
            if t in targets[k]:
                if mode == "parity":
                    f ^= emit[k]
                else:
                    f |= emit[k]
        out |= ((X[t] ^ f) << dt(t * m))
    return out


def cyclic_states(f, N):
    """The set of states lying on a cycle of the functional graph f."""
    img = np.zeros(N, dtype=bool)
    img[f] = True
    A = np.flatnonzero(img)
    for _ in range(4096):
        img2 = np.zeros(N, dtype=bool)
        img2[f[A]] = True
        B = np.flatnonzero(img2)
        if B.size == A.size:
            return B
        A = B
    raise RuntimeError("image did not stabilise")


def cycles_of(f, cyc):
    """Decompose the cyclic states into cycles (lists of packed states)."""
    seen = set()
    out = []
    fl = f.tolist()
    for s0 in cyc.tolist():
        if s0 in seen:
            continue
        cycle, s = [], s0
        while s not in seen:
            seen.add(s)
            cycle.append(s)
            s = fl[s]
        out.append(cycle)
    return out


# ---------------------------------------------------------------- rotor tests

def unpack(s, m, n):
    mask = (1 << m) - 1
    return tuple((s >> (k * m)) & mask for k in range(n))


def pack(X, m):
    s = 0
    for k, x in enumerate(X):
        s |= x << (k * m)
    return s


def rot_packed(s, r, m, n):
    return pack(tuple(_rotpy(x, r, m) for x in unpack(s, m, n)), m)


def _rotpy(x, r, m):
    r %= m
    if r == 0:
        return x
    mask = (1 << m) - 1
    return ((x << r) | (x >> (m - r))) & mask


def rotor_of_cycle(cycle, f, m, n):
    """Minimal (p, d) with Phi^p(S) = rot_d(S) for S = cycle[0]; None if the
    cycle carries no rotation symmetry other than d = 0 at p = len(cycle)."""
    s0 = cycle[0]
    rots = {}
    for d in range(m):
        rots.setdefault(rot_packed(s0, d, m, n), d)
    L = len(cycle)
    for p in range(1, L + 1):
        s = cycle[p % L]
        if s in rots:
            d = rep(rots[s], m)
            return p, d, (rot_packed(s0, d, m, n) == s0)
    return None


# ---------------------------------------------------------------- the campaign

def used_kinds(cycle, m, n):
    u = set()
    for s in cycle:
        X = unpack(s, m, n)
        for k in range(n):
            if X[k]:
                u.add(k)
    return u


def census(rules_list, target_maps, ms, n, modes=("parity", "or"),
           tag="census", verbose=True, dump=True):
    rows = []
    t0 = time.time()
    ncon = 0
    for m in ms:
        N = 1 << (n * m)
        for rules in rules_list:
            for targets in target_maps:
                for mode in modes:
                    if n == 1 and mode == "or":
                        continue          # single author: parity == or
                    ncon += 1
                    f = transition(rules, targets, m, n, mode)
                    cyc = cyclic_states(f, N)
                    for cycle in cycles_of(f, cyc):
                        if all(s == 0 for s in cycle):
                            continue
                        r = rotor_of_cycle(cycle, f, m, n)
                        if r is None:
                            continue
                        p, d, sym = r
                        if d == 0 or sym:
                            continue      # a plain cycle, or rotation-symmetric
                        uk = used_kinds(cycle, m, n)
                        od = max(len(targets[k]) for k in uk) if uk else 0
                        gs, best = -1, None
                        for s in cycle:
                            X = unpack(s, m, n)
                            o = 0
                            for x in X:
                                o |= x
                            g = vacant_arc(o, m)
                            if g > gs:
                                gs, best = g, s
                        rows.append({
                            "m": m, "n": n, "mode": mode, "rules": rules,
                            "targets": [list(t) for t in targets],
                            "p": p, "d": d, "L": len(cycle),
                            "card": sum(bin(x).count("1")
                                        for x in unpack(cycle[0], m, n)),
                            "od": od, "used": sorted(uk), "g": gs,
                            "state": best,
                            "lc": abs(d) <= p * W,
                            "lc2": abs(d) <= 2 * p * W,
                            "lift": gs >= 2 * p * W,
                        })
        if verbose:
            print("  m=%-3d done  (%.1f s, %d rotor cycles so far)"
                  % (m, time.time() - t0, len(rows)), flush=True)
    if dump:
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, "t4_%s.jsonl" % tag)
        with open(path, "w") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
        if verbose:
            print("  wrote %s (%d rows, %d constitution-runs)"
                  % (path, len(rows), ncon))
    return rows, ncon


def summarise(rows, ncon, title):
    print("\n### %s" % title)
    print("  constitution-runs (constitution x ring x mode): %d" % ncon)
    print("  rotor cycles found (d != 0, rot_d(S) != S): %d" % len(rows))
    by_m = {}
    for r in rows:
        by_m.setdefault(r["m"], []).append(r)
    print("  %-4s %8s %8s %8s %10s %10s %10s" %
          ("m", "rotors", "LC(<=p)", "LC2(<=2p)", "LC&od=1", "LC&od>=2",
           "LC&lift"))
    for m in sorted(by_m):
        rs = by_m[m]
        lc = [r for r in rs if r["lc"]]
        print("  %-4d %8d %8d %8d %10d %10d %10d"
              % (m, len(rs), len(lc), len([r for r in rs if r["lc2"]]),
                 len([r for r in lc if r["od"] <= 1]),
                 len([r for r in lc if r["od"] >= 2]),
                 len([r for r in lc if r["lift"]])))
    lc1 = [r for r in rows if r["lc"] and r["od"] <= 1]
    print("  *** light-cone-admissible rotors with out-degree <= 1: %d ***"
          % len(lc1))
    for r in lc1[:20]:
        print("      ", r)
    lcnl = [r for r in rows if r["lc"] and not r["lift"]]
    print("  *** light-cone-admissible rotors FAILING the gap hypothesis "
          "(g < 2pW): %d ***" % len(lcnl))
    for r in lcnl[:10]:
        print("      m=%d %s->%s p=%d d=%+d g=%d od=%d card=%d"
              % (r["m"], r["rules"], r["targets"], r["p"], r["d"], r["g"],
                 r["od"], r["card"]))


TARGETS2_ALL = [t for t in itertools.product(
    [(), (0,), (1,), (0, 1)], repeat=2)]
TARGETS2_OD1 = [t for t in TARGETS2_ALL
                if all(len(x) <= 1 for x in t)]


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "n1"
    if what == "n1":
        ms = range(3, 23)
        rows, nc = census([[r] for r in RULES1], [((0,),), ((),)], ms, 1,
                          tag="n1")
        summarise(rows, nc, "1 kind, all 27 rules, both target maps "
                            "({0} and empty), m = 3..22, COMPLETE")
    elif what == "n2":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        rules2 = list(itertools.product(RULES1, repeat=2))
        rows, nc = census(rules2, TARGETS2_ALL, range(a, b + 1), 2,
                          tag="n2_%d_%d" % (a, b))
        summarise(rows, nc, "2 kinds, all 729 rule pairs x all 16 target maps, "
                            "m = %d..%d, parity+or, COMPLETE" % (a, b))
    elif what == "od1":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        rules2 = list(itertools.product(RULES1, repeat=2))
        rows, nc = census(rules2, TARGETS2_OD1, range(a, b + 1), 2,
                          tag="od1_%d_%d" % (a, b))
        summarise(rows, nc, "2 kinds, all 729 rule pairs x the 9 out-degree<=1 "
                            "target maps, m = %d..%d, parity+or, COMPLETE"
                            % (a, b))
    else:
        raise SystemExit(__doc__)
