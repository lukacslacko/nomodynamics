#!/usr/bin/env python3
"""
bulk.py — the complete census of the BULK MAP, chapter three's new habitat.

In a region every cell of which carries the same kind-set U, offsets are
invisible: every cell sees the same neighbourhood.  So the interior of solid
code evolves by a map

    beta : 2^K -> 2^K ,   beta(U) = U  xor  (xor_{k in A(U)} 1_{T_k})   [parity]
                          beta(U) = U  xor  (union_{k in A(U)} T_k)     [OR]
    A(U) = { k in U : g_k in U^  and  h_k not in U^ },  U^ = U u {ANY}.

`cite.bulk_map` is proved exact on homogeneous ring codes for every modulus by
`cite.py` self-test 3.  Because beta depends ONLY on the guards and target sets
(never on the offsets, never on the modulus), the census below is COMPLETE for
n = 2 and n = 3 with no box caveat whatsoever: there are exactly
((n+1)^2 * 2^n)^n constitutions-up-to-bulk-equivalence, and all are enumerated.

    python3 bulk.py            # the census + the best specimens
"""

from __future__ import annotations

import itertools
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cite as ct                                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)


def bulk_kinds(n):
    """(target set, (g,h)) — everything beta can see about one kind."""
    gs = [None] + list(range(n))
    ts = [t for r in range(n + 1) for t in itertools.combinations(range(n), r)]
    return [(T, (g, h)) for T in ts for g in gs for h in gs]


def make(n, combo):
    return ct.Cit([(0, 0, 0)] * n, [c[0] for c in combo], [c[1] for c in combo])


def census(n, mode="parity"):
    BK = bulk_kinds(n)
    tot = len(BK) ** n
    stats = Counter()
    periods = Counter()
    best = []                      # (period, preperiod, label, orbit)
    gridlock = 0
    for combo in itertools.product(BK, repeat=n):
        C = make(n, combo)
        gl = ct.gridlocked(C)
        gridlock += gl
        maxp = 1
        orb = None
        nfix = 0
        for r in range(n + 1):
            for U in itertools.combinations(range(n), r):
                t0, p, seq = ct.bulk_orbit(C, frozenset(U), mode)
                if p == 1 and t0 == 0:
                    nfix += 1
                if p > maxp:
                    maxp, orb = p, (t0, p, seq, frozenset(U))
        periods[maxp] += 1
        stats[("fixed_plena", nfix)] += 1
        if maxp >= 3:
            best.append((maxp, C.label(), orb))
    return dict(tot=tot, gridlock=gridlock, periods=dict(periods),
                stats={repr(k): v for k, v in stats.items()}, best=best)


def show(n, mode="parity"):
    r = census(n, mode)
    print("\n=== BULK CENSUS n=%d  mode=%s  (COMPLETE: %d constitutions) ==="
          % (n, mode, r["tot"]))
    print("Gridlock survives (h_k in {ANY,k,g_k} for all k): %d  (%.4f%%)"
          % (r["gridlock"], 100.0 * r["gridlock"] / r["tot"]))
    print("living bulk (some solid region acts):             %d  (%.4f%%)"
          % (r["tot"] - r["gridlock"],
             100.0 * (r["tot"] - r["gridlock"]) / r["tot"]))
    print("maximal bulk period, distribution:")
    for p in sorted(r["periods"]):
        print("   period %-3d : %10d  (%.4f%%)"
              % (p, r["periods"][p], 100.0 * r["periods"][p] / r["tot"]))
    if r["best"]:
        r["best"].sort(key=lambda x: -x[0])
        print("longest bulk orbits:")
        for p, lab, orb in r["best"][:4]:
            t0, per, seq, U0 = orb
            cyc = seq[t0:]
            print("   p=%d  %s" % (p, lab))
            print("        orbit: " + " -> ".join(
                "{" + ",".join(map(str, sorted(u))) + "}" for u in cyc)
                + " -> ...")
    return r


def certify_ring(C, U, m, mode="parity"):
    """Realise a bulk orbit as an exact ring code; re-check on xnomos."""
    import xnomos as X
    full = (1 << m) - 1
    mask = tuple(full if k in U else 0 for k in range(C.n))
    t0, p, seq = ct.ring_orbit(mask, C, m, mode)
    XC = C.to_xnomos(modulus=m)
    S = X.state_of([(i, k) for i in range(m) for k in U])
    res = X.classify(S, XC, mode, max_steps=200)
    return t0, p, res


if __name__ == "__main__":
    out = {}
    for n in (2, 3):
        for mode in ("parity", "or"):
            out["n%d_%s" % (n, mode)] = {
                k: v for k, v in show(n, mode).items() if k != "best"}
    with open(os.path.join(DATA, "bulk_census.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote data/bulk_census.json")
