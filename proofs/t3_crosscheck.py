#!/usr/bin/env python3
"""
t3_crosscheck.py -- head-to-head between this expedition's decider
(t3_decide, driven by the (u,v,w) type reduction) and X-E's SFT decider
(xspeed/sft.py, driven by the raw channel list), plus a replication of the
published MIRROR table.

Two genuinely independent code paths: sft.py builds its 2r+1 = 5-cell lookup
table by looping over channels; t3_decide builds its 5-cell table from the
four CELL TYPES and the three emission vectors (u,v,w).  They must agree on
every question.
"""
from __future__ import annotations

import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "xspeed"))

import xnomos                                                     # noqa: E402
import sft                                                        # noqa: E402
from t3_core import channels_to_uvw, channels_to_UVW, rule_table  # noqa: E402
from t3_decide import decide, check_witness                       # noqa: E402

LIVE = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1)
        for c in (-1, 0, 1) if a != b]


def table_agreement():
    """The 32-entry local rules must be identical, channel list vs types."""
    rng = random.Random(99)
    bad = n = 0
    for _ in range(4000):
        k = rng.randrange(1, 7)
        ch = [rng.choice(LIVE) for _ in range(k)]
        for mode in ("parity", "or"):
            cls = (channels_to_uvw(ch) if mode == "parity"
                   else channels_to_UVW(ch))
            n += 1
            if rule_table(cls, mode) != sft.step_table(ch, 1, mode):
                bad += 1
    return n, bad


def decider_agreement(samples=260, seed=7):
    rng = random.Random(seed)
    rows = []
    dis = 0
    for _ in range(samples):
        k = rng.randrange(1, 6)
        ch = [rng.choice(LIVE) for _ in range(k)]
        mode = rng.choice(["parity", "or"])
        p = rng.randrange(1, 6)
        d = rng.randrange(1, p + 1)
        cls = (channels_to_uvw(ch) if mode == "parity"
               else channels_to_UVW(ch))
        mine, cols = decide(cls, p, d, mode)
        theirs, tcols = sft._search_cycle(sft.step_table(ch, 1, mode),
                                          1, p, d, 3_000_000)
        agree = (mine == theirs)
        if not agree:
            dis += 1
            rows.append((ch, mode, p, d, mine, theirs))
        if mine == "GLIDER":
            assert check_witness(cls, cols, p, d, mode)
    return samples, dis, rows


def mirror_table():
    """Replicate the published MIRROR family table (xspeed/RESULTS.md 7.1)."""
    mir = [(0, 1, -1), (0, -1, 1)]
    out = []
    for p in range(4, 8):
        row = [p]
        for (d, mode) in [(2, "parity"), (2, "or"), (3, "parity"), (3, "or")]:
            cls = (channels_to_uvw(mir) if mode == "parity"
                   else channels_to_UVW(mir))
            v, cols = decide(cls, p, d, mode)
            if v == "GLIDER":
                seed = [x for x, c in enumerate(cols) if c & 1]
                span = max(seed) - min(seed) + 1
                S = {c: 3 for c in seed}
                C = xnomos.Const(mir, [(0, 1), (0, 1)])
                assert xnomos.verify_glider(S, C, p, d, mode)
                row.append("GLIDER span %d" % span)
            else:
                row.append(v)
        out.append(row)
    return out


def n_le_5_sweep(nmax=5, pmax=4, mode="parity"):
    """Every single-field constitution with <= nmax live channels (multisets),
    every (p,d) with p <= pmax: the maximum MINIMAL displacement.  This is the
    exact analogue of X-E's Table A, with the minimality test added."""
    from t3_decide import minimal_pd
    best = {}
    seen_cls = set()
    for n in range(1, nmax + 1):
        for combo in itertools.combinations_with_replacement(LIVE, n):
            cls = (channels_to_uvw(list(combo)) if mode == "parity"
                   else channels_to_UVW(list(combo)))
            if cls in seen_cls:
                continue
            seen_cls.add(cls)
            for p in range(1, pmax + 1):
                for d in range(1, p + 1):
                    v, cols = decide(cls, p, d, mode)
                    if v == "GLIDER":
                        m = minimal_pd(cls, cols, p, d, mode)
                        if m and (m not in best):
                            best[m] = (combo, [x for x, c in enumerate(cols)
                                               if c & 1])
    return seen_cls, best


def main():
    print("1. local rule tables, channel-list vs (u,v,w) type reduction")
    n, bad = table_agreement()
    print("   %d tables compared, %d disagreements" % (n, bad))
    assert bad == 0

    print("\n2. width-unbounded deciders head to head "
          "(t3_decide vs xspeed/sft.py)")
    n, dis, rows = decider_agreement()
    print("   %d random questions, %d disagreements" % (n, dis))
    for r in rows:
        print("     ", r)
    assert dis == 0

    print("\n3. replication of the published MIRROR table "
          "(xspeed/RESULTS.md 7.1)")
    print("   p | d=2 parity        | d=2 or | d=3 parity | d=3 or")
    for row in mirror_table():
        print("   %d | %-18s | %-6s | %-10s | %s"
              % (row[0], row[1], row[2], row[3], row[4]))
    print("   (published: GLIDER spans 53, 20, 616, 438 for p=4,5,6,7;")
    print("    NONE for d=2 under OR and for d=3 under either)")

    print("\n4. the n<=5 single-field sector, WITH the minimality test")
    for mode in ("parity", "or"):
        cls, best = n_le_5_sweep(5, 4, mode)
        print("   mode=%s: %d distinct classes reachable with n<=5 channels"
              % (mode, len(cls)))
        print("   minimal (p0,d0) realised with p0<=4:")
        for m in sorted(best):
            combo, seed = best[m]
            flag = "   <-- BEATS THE PUBLISHED CAP" if abs(m[1]) > 2 else ""
            print("      (p0,d0)=%-8s n=%d %s seed=%s%s"
                  % (str(m), len(combo), list(combo), seed, flag))


if __name__ == "__main__":
    main()
