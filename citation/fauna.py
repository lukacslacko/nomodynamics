#!/usr/bin/env python3
"""
fauna.py — the living bulk: hunts for phenomena with no chapter-one or
chapter-two analogue, i.e. things that happen INSIDE fully occupied code.

Two hunts, both over the COMPLETE n=2, W=1 citation box (237,006 symmetry
representatives of 944,784 constitutions), and a sampled n=3 hunt:

  DEFECT HUNT.  Take a background phase U with beta(U) = U (a solid region that
  is a fixed point of the bulk map), put it on a ring Z/m, spoil ONE cell, and
  ask whether the spoilt cell TRAVELS: Phi^p(S) = rot_r(S) with 0 < |r| <= p
  (inside the light cone, so it is transport and not a barber pole — the test
  X-C's retraction demands).

  BOUNDARY HUNT.  Take two distinct beta-fixed phases U, V, lay half a ring in
  each, and ask what the seam does: frozen / oscillating / a CONVERSION FRONT
  that eats one phase and lays down the other, inside solid code.

    python3 fauna.py defect [--procs 4] [--n 2]
    python3 fauna.py boundary [--procs 4] [--n 2]
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cite as ct                                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

MODULI = (11, 13)            # defect hunt
BOUNDARY_MODULI = (12,)      # boundary hunt
MODES = ("parity", "or")


def rotr(x, s, m):
    s %= m
    return ((x >> s) | (x << (m - s))) & ((1 << m) - 1)


def rot_state(S, s, m):
    return tuple(rotr(x, s, m) for x in S)


def fixed_phases(C, mode):
    """Nonempty U with beta(U) = U — the solid phases that persist."""
    out = []
    for u in range(1, 1 << C.n):
        U = frozenset(k for k in range(C.n) if (u >> k) & 1)
        if ct.bulk_map(C, U, mode) == U:
            out.append(U)
    return out


def plenum(U, C, m):
    full = (1 << m) - 1
    return tuple(full if k in U else 0 for k in range(C.n))


def travelling(seq, m, W=1):
    """Earliest (p, r) with seq[p] = rot_r(seq[0]), r != 0, |r| <= p*W."""
    S0 = seq[0]
    for p in range(1, len(seq)):
        for r in range(-p * W, p * W + 1):
            if r == 0:
                continue
            if rot_state(S0, -r, m) == seq[p]:
                if rot_state(S0, -r, m) != S0:
                    return p, r
    return None


def _defect(chunk):
    hits, stats = [], Counter()
    for (i, j) in chunk:
        C = const_of(i, j)
        for mode in MODES:
            phases = fixed_phases(C, mode)
            if not phases:
                continue
            for U in phases:
                um = sum(1 << k for k in U)
                for vm in range(1 << C.n):
                    if vm == um:
                        continue
                    for m in MODULI:
                        S = list(plenum(U, C, m))
                        for k in range(C.n):
                            bit = 1
                            if (vm >> k) & 1:
                                S[k] |= bit
                            else:
                                S[k] &= ~bit & ((1 << m) - 1)
                        S = tuple(S)
                        t0, p, seq = ct.ring_orbit(S, C, m, mode, max_steps=200)
                        if p is None:
                            stats["nonperiodic"] += 1
                            continue
                        tr = travelling(seq[:min(len(seq), 60)], m)
                        stats["runs"] += 1
                        if tr:
                            stats["travelling"] += 1
                            hits.append((i, j, mode, sorted(U), vm, m,
                                         tr[0], tr[1]))
    return hits, stats


def _boundary(chunk):
    hits, stats = [], Counter()
    for (i, j) in chunk:
        C = const_of(i, j)
        for mode in MODES:
            ph = fixed_phases(C, mode)
            if len(ph) < 2:
                continue
            for a in range(len(ph)):
                for b in range(len(ph)):
                    if a == b:
                        continue
                    for m in BOUNDARY_MODULI:
                        U, V = ph[a], ph[b]
                        half = (1 << (m // 2)) - 1
                        S = tuple(((half if k in U else 0)
                                   | ((((1 << m) - 1) ^ half) if k in V else 0))
                                  for k in range(C.n))
                        t0, p, seq = ct.ring_orbit(S, C, m, mode, max_steps=200)
                        stats["runs"] += 1
                        if p is None:
                            stats["nonperiodic"] += 1
                            continue
                        tr = travelling(seq[:min(len(seq), 60)], m)
                        if tr:
                            stats["travelling_seam"] += 1
                            hits.append((i, j, mode, sorted(U), sorted(V), m,
                                         tr[0], tr[1]))
                        elif p > 1:
                            stats["oscillating_seam"] += 1
    return hits, stats


KINDS = None


def _init(n):
    global KINDS
    KINDS = ct.all_kinds(n)


def const_of(i, j):
    k1, k2 = KINDS[i], KINDS[j]
    return ct.Cit([k1[0], k2[0]], [k1[1], k2[1]], [k1[2], k2[2]])


def reps(n):
    out, seen = [], set()
    for i in range(len(KINDS)):
        for j in range(len(KINDS)):
            C = const_of(i, j)
            if C.key() in seen:
                continue
            for kk in ct.orbit_of(C):
                seen.add(kk)
            out.append((i, j))
    return out


def chunks(lst, m):
    for a in range(0, len(lst), m):
        yield lst[a:a + m]


def run(which, procs, n):
    global KINDS
    KINDS = ct.all_kinds(n)
    R = reps(n)
    print("box: %d constitutions, %d symmetry representatives"
          % (len(KINDS) ** 2, len(R)))
    fn = {"defect": _defect, "boundary": _boundary}[which]
    hits, stats = [], Counter()
    with Pool(procs, initializer=_init, initargs=(n,)) as p:
        for h, s in p.imap_unordered(fn, list(chunks(R, 200))):
            hits.extend(h)
            stats.update(s)
    print(which, dict(stats))
    print("hits:", len(hits))
    with open(os.path.join(DATA, "%s_hits.txt" % which), "w") as fh:
        for h in hits:
            fh.write(repr(h) + "\n")
    with open(os.path.join(DATA, "%s_stats.json" % which), "w") as fh:
        json.dump({"stats": dict(stats), "hits": len(hits),
                   "box": len(KINDS) ** 2, "reps": len(R),
                   "moduli": list(MODULI if which == "defect"
                                  else BOUNDARY_MODULI)}, fh, indent=1)


if __name__ == "__main__":
    which = sys.argv[1]
    pr = 4
    n = 2
    if "--procs" in sys.argv:
        pr = int(sys.argv[sys.argv.index("--procs") + 1])
    if "--n" in sys.argv:
        n = int(sys.argv[sys.argv.index("--n") + 1])
    run(which, pr, n)
