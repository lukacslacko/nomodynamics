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


def cycle_ids(f, N):
    """Vectorised functional-graph analysis by pointer doubling.

    Returns (g, cid) where g = f^(2^K) with 2^K >= N (so g maps every state
    onto its cycle, and image(g) = exactly the cyclic states) and
    cid[s] = min{ f^j(s) : 0 <= j < 2^K }, which on a cyclic state is the
    smallest state of its cycle -- a canonical cycle identifier.
    """
    K = max(1, int(N - 1).bit_length())
    h = f
    cid = np.arange(N, dtype=f.dtype)
    for _ in range(K):
        cid = np.minimum(cid, cid[h])
        h = h[h]
    return h, cid


def cyclic_states(f, N):
    """The set of states lying on a cycle of the functional graph f."""
    g, _ = cycle_ids(f, N)
    seen = np.zeros(N, dtype=bool)
    seen[g] = True
    return np.flatnonzero(seen)


def rotor_cycles(f, N, m, n, rots):
    """All rotor cycles of the functional graph f, found VECTORISED.

    A state s lies on a rotor cycle iff rot_d(s) lies on the SAME cycle for
    some d != 0 (rot commutes with Phi, so rot_d maps cycles to cycles; and
    Phi^p(s) = rot_d(s) for some p iff rot_d(s) is in the forward orbit of s
    iff it is on the same cycle).  Cycle membership is read off the canonical
    cycle identifier cid.  Only the -- few -- cycles that pass are then walked
    in Python to extract the minimal (p, d).

    rots[d] is the precomputed permutation s -> rot_d(s) of the state space.
    """
    g, cid = cycle_ids(f, N)
    oncyc = np.zeros(N, dtype=bool)
    oncyc[g] = True
    hit = np.zeros(N, dtype=bool)
    idx = np.arange(N, dtype=f.dtype)
    for d in range(1, m):
        rd = rots[d]
        hit |= oncyc & (rd != idx) & (cid[rd] == cid)
    if not hit.any():
        return []
    reps = np.unique(cid[hit])
    out = []
    for s0 in reps.tolist():
        cycle, s = [], s0
        while True:
            cycle.append(s)
            s = int(f[s])
            if s == s0:
                break
        out.append(cycle)
    return out


# ---------------------------------------------------------------- rotor tests

def rot_perm_array(m, n, d, dt):
    """The permutation of the packed state space induced by rot_d."""
    N = 1 << (n * m)
    s = np.arange(N, dtype=dt)
    if d % m == 0:
        return s
    mask = (1 << m) - 1
    r = d % m
    out = np.zeros(N, dtype=dt)
    for k in range(n):
        x = (s >> dt(k * m)) & dt(mask)
        x = ((x << dt(r)) | (x >> dt(m - r))) & dt(mask)
        out |= x << dt(k * m)
    return out


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


def single_author(targets, n):
    """True when every kind has at most one source: then parity == or."""
    return all(sum(1 for k in range(n) if t in targets[k]) <= 1
               for t in range(n))


def census(rules_list, target_maps, ms, n, modes=("parity", "or"),
           tag="census", verbose=True, dump=True):
    rows = []
    t0 = time.time()
    ncon = 0
    for m in ms:
        N = 1 << (n * m)
        dt = np.uint32 if n * m <= 31 else np.uint64
        rots = [rot_perm_array(m, n, d, dt) for d in range(m)]
        for rules in rules_list:
            for targets in target_maps:
                for mode in modes:
                    if mode == "or" and single_author(targets, n):
                        continue          # Single-Author: parity == or
                    ncon += 1
                    f = transition(rules, targets, m, n, mode)
                    for cycle in rotor_cycles(f, N, m, n, rots):
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
