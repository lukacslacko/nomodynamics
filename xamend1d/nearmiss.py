#!/usr/bin/env python3
"""nearmiss.py — Task 4: hunt for motion the strict Phi^p = sigma^d definition
misses, in the E2 (permutation), E1 (supersession) and E3 (multi-target)
universes.

Instrument: the WIDE engine (512 cells, no renormalisation), T steps, then a
search for p <= Pmax and d != 0 such that the FRONT WINDOW — the FW cells
ending at the rightmost occupied cell hi(t) — satisfies

        window(t + p) = window(t)     and     hi(t + p) = hi(t) + d

for every t in the second half of the run.  That is exactly "a bounded packet
travelling at the front speed IS periodic".  Alongside it we test whether the
debris behind the front is p-periodic IN PLACE, whether it oscillates, and
how structured it is (occupied/empty transitions).

Categories:
  MOVING BOUNDED PACKET  front and back edge both advance, population constant
                         -> a genuine glider; verified with xnomos.verify_glider
  PUFFER                 front translates, population grows, debris p-periodic
                         in place AND structured (>= 4 transitions)
  OSCILLATING PUFFER     as above, and the debris genuinely oscillates
  GUN                    front translates, back edge FIXED, debris structured
  BARE FRONT             front translates but the debris is a solid block
                         (the colonizer family) — the uninteresting control
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import xnomos                                                  # noqa: E402
import fastlib as F                                            # noqa: E402

OFF = (-1, 0, 1)
RULES1 = [(a, b, c) for a in OFF for b in OFF for c in OFF]
T_SCAN, PMAX, FW = 140, 16, 28
FR, FL, DP, GR, OS, GP = (F.FLAG_FRONT_R, F.FLAG_FRONT_L, F.FLAG_DEBRIS_P,
                          F.FLAG_GROWS, F.FLAG_OSC, F.FLAG_GAPPY)


# ----------------------------------------------------------------- certifier

def certify(rules, targets, mode, S0, p, d, reps=3, T=None, verbose=True):
    """Independent re-simulation with xnomos.step.  Prints an explicit check of
    exactly which recurrences hold and which fail."""
    T = T or T_SCAN
    C = xnomos.Const(rules, targets)
    S = dict(S0)
    fr = []
    for _ in range(T):
        fr.append(dict(S))
        S = xnomos.step(S, C, mode)
    hi = [max(s) if s else None for s in fr]
    lo = [min(s) if s else None for s in fr]
    cd = [xnomos.card(s) for s in fr]
    t0 = T // 2
    ok_front = ok_debris = True
    checked = 0
    for t in range(t0, T - p):
        if hi[t] is None or hi[t + p] is None:
            ok_front = False
            break
        if hi[t + p] - hi[t] != d:
            ok_front = False
        w1 = {(c - hi[t], m) for c, m in fr[t].items() if c > hi[t] - FW}
        w2 = {(c - hi[t + p], m) for c, m in fr[t + p].items()
              if c > hi[t + p] - FW}
        if w1 != w2:
            ok_front = False
        e = hi[t] - FW
        b1 = {(c, m) for c, m in fr[t].items() if c <= e}
        b2 = {(c, m) for c, m in fr[t + p].items() if c <= e}
        if b1 != b2:
            ok_debris = False
        checked += 1
        if checked >= reps * p + p:
            break
    exact = xnomos.verify_glider(fr[t0], C, p, d, mode)
    if verbose:
        print("   CERTIFICATE (independent re-simulation with xnomos.step, "
              "%d frames, %d lag-checks >= %d periods):" % (T, checked, reps))
        print("     front window (%d cells at hi(t)) is p=%d periodic with "
              "hi(t+p)-hi(t)=%+d : %s" % (FW, p, d, "PASS" if ok_front else "FAIL"))
        print("     debris (cells <= hi(t)-%d) is p-periodic in place        "
              "        : %s" % (FW, "PASS" if ok_debris else "FAIL"))
        print("     STRICT glider Phi^p(S_t0) = sigma^%+d(S_t0) "
              "(xnomos.verify_glider)   : %s" % (d, "PASS" if exact else "FAIL"))
        print("     population card(S_t): %d at t=%d -> %d at t=%d  (growth "
              "%+.3f laws/step)" % (cd[t0], t0, cd[T - 1], T - 1,
                                    (cd[T - 1] - cd[t0]) / (T - 1 - t0)))
        print("     back edge lo(t): %d at t=%d -> %d at t=%d" %
              (lo[t0], t0, lo[T - 1], T - 1))
    return dict(front=ok_front, debris=ok_debris, strict_glider=exact,
                checked=checked, card0=cd[t0], card1=cd[T - 1],
                lo0=lo[t0], lo1=lo[T - 1], hi0=hi[t0], hi1=hi[T - 1])


def show(name, rules, targets, mode, S0, steps=26, width=None):
    C = xnomos.Const(rules, targets)
    S = dict(S0)
    lo = min(S0)
    hi = lo + (width or 46)
    rows = xnomos.spacetime(S0, C, steps, mode, lo=lo - 1, hi=hi)
    print("\n  %s" % name)
    print("  constitution: %s   mode=%s" % (C.label(), mode))
    print("  seed: %s" % sorted(S0.items()))
    for t, r in enumerate(rows):
        print("  t=%-3d |%s|" % (t, r))


# ------------------------------------------------------------------ the scan

def scan(name, consts, seeds, mode, chunk=None, note=""):
    """Wide-frame front scan over consts x seeds; returns bucketed candidates."""
    n = len(consts[0][0])
    chunk = chunk or max(1, 8_000_000 // (len(seeds) * 11))
    tally = dict(runs=0, front_r=0, front_l=0, bounded_packet=0, puffer=0,
                 osc_puffer=0, gun=0, bare_front=0)
    cand = {"bounded_packet": [], "puffer": [], "osc_puffer": [], "gun": []}
    t0 = time.time()
    for c0 in range(0, len(consts), chunk):
        blk = consts[c0:c0 + chunk]
        nc, _, cf = F.pack_consts(blk)
        out = F.frontscan(cf, nc, n, mode, seeds, T_SCAN, PMAX)
        fl = out[:, :, 0]
        tally["runs"] += out.shape[0] * out.shape[1]
        tally["front_r"] += int((fl & FR).astype(bool).sum())
        tally["front_l"] += int((fl & FL).astype(bool).sum())
        has_r = (fl & FR) != 0
        if not has_r.any():
            continue
        cardlo, cardhi = out[:, :, 4], out[:, :, 5]
        lolo, lohi = out[:, :, 6], out[:, :, 7]
        grows = (fl & GR) != 0
        gappy = (fl & GP) != 0
        dperi = (fl & DP) != 0
        osc = (fl & OS) != 0
        pack = has_r & ((fl & FL) != 0) & (cardlo == cardhi) & \
            ((lohi - lolo) == (out[:, :, 9] - out[:, :, 8]))
        puff = has_r & grows & dperi & gappy
        gun = has_r & grows & gappy & (lohi == lolo)
        bare = has_r & grows & ~gappy
        for key, mask in (("bounded_packet", pack), ("puffer", puff),
                          ("osc_puffer", puff & osc), ("gun", gun)):
            idx = np.argwhere(mask)
            tally[key] += len(idx)
            for ci, si in idx[:40]:
                if len(cand[key]) < 400:
                    cand[key].append((c0 + int(ci), int(si),
                                      int(out[ci, si, 1]), int(out[ci, si, 2]),
                                      int(out[ci, si, 10])))
        tally["bare_front"] += int(bare.sum())
    dt = time.time() - t0
    print("%-38s %-9s runs=%-11d %6.1fs | frontR=%-9d frontL=%-9d "
          "bounded_packet=%-5d PUFFER=%-6d osc=%-5d GUN=%-6d bare=%d"
          % (name, mode, tally["runs"], dt, tally["front_r"], tally["front_l"],
             tally["bounded_packet"], tally["puffer"], tally["osc_puffer"],
             tally["gun"], tally["bare_front"]))
    if note:
        print("    scope: %s" % note)
    return tally, cand


# -------------------------------------------------------------------- worlds

def e2_worlds():
    out = []
    cs = [(list(r), [1, 0]) for r in itertools.product(RULES1, repeat=2)]
    out.append(("E2 L=2 [1,0]", cs, F.all_seeds(2, 6, 4),
                "COMPLETE: all 27^2=729 consts x all canonical seeds <=4 laws/6 cells"))
    cs = [(list(r), [1, 2, 0]) for r in itertools.product(RULES1, repeat=3)]
    out.append(("E2 L=3 [1,2,0]", cs, F.all_seeds(3, 5, 3),
                "COMPLETE: all 27^3=19,683 consts x all canonical seeds <=3 laws/5 cells"))
    rng = np.random.default_rng(4242)
    for tg, lbl in (([1, 2, 3, 0], "L=4 [1,2,3,0]"), ([1, 0, 3, 2], "2+2 [1,0,3,2]")):
        idx = rng.integers(0, 27, size=(20000, 4))
        cs = [([RULES1[i] for i in row], tg) for row in idx]
        out.append(("E2 %s" % lbl, cs, F.all_seeds(4, 5, 3),
                    "SAMPLE: 20,000 consts of 27^4 (PCG64 seed 4242) x all "
                    "canonical seeds <=3 laws/5 cells"))
    return out


def sup_worlds():
    out = []
    for n, cells, laws in ((1, 9, 7), (2, 7, 5), (3, 5, 3)):
        cs = [(list(r), list(range(n))) for r in itertools.product(RULES1, repeat=n)]
        out.append(("SUP n=%d" % n, cs, F.all_seeds(n, cells, laws),
                    "COMPLETE: all 27^%d consts x all canonical seeds <=%d laws/%d cells"
                    % (n, laws, cells)))
    rng = np.random.default_rng(909)
    idx = rng.integers(0, 27, size=(20000, 4))
    cs = [([RULES1[i] for i in row], list(range(4))) for row in idx]
    out.append(("SUP n=4", cs, F.all_seeds(4, 5, 3),
                "SAMPLE: 20,000 consts of 27^4 (PCG64 seed 909) x all canonical "
                "seeds <=3 laws/5 cells"))
    return out


def e3_worlds():
    """Multi-target: targets[k] any nonempty subset of the kinds."""
    out = []
    subs2 = [(0,), (1,), (0, 1)]
    cs = [(list(r), list(t))
          for r in itertools.product(RULES1, repeat=2)
          for t in itertools.product(subs2, repeat=2)]
    out.append(("E3 n=2 all-targets", cs, F.all_seeds(2, 6, 4),
                "COMPLETE: all 27^2 x 3^2 = 6,561 consts x all canonical seeds "
                "<=4 laws/6 cells"))
    rng = np.random.default_rng(1717)
    subs3 = [tuple(k for k in range(3) if m >> k & 1) for m in range(1, 8)]
    ri = rng.integers(0, 27, size=(20000, 3))
    ti = rng.integers(0, 7, size=(20000, 3))
    cs3 = [([RULES1[i] for i in ri[j]], [subs3[i] for i in ti[j]])
           for j in range(20000)]
    out.append(("E3 n=3 all-targets", cs3, F.all_seeds(3, 5, 3),
                "SAMPLE: 20,000 (rules,targets) of 27^3 x 7^3 (PCG64 seed 1717)"
                " x all canonical seeds <=3 laws/5 cells"))
    return out


ALL = {"e2": (e2_worlds, ["parity", "or"]),
       "sup": (sup_worlds, ["super", "super_or"]),
       "e3": (e3_worlds, ["parity", "or"])}

if __name__ == "__main__":
    keys = sys.argv[1:] or list(ALL)
    report = []
    stash = {}
    for key in keys:
        wf, modes = ALL[key]
        print("\n=== near-miss scan: %s (T=%d, Pmax=%d, front window FW=%d) ==="
              % (key.upper(), T_SCAN, PMAX, FW))
        for name, cs, sd, note in wf():
            for mode in modes:
                tally, cand = scan(name, cs, sd, mode, note=note)
                report.append(dict(world=key, name=name, mode=mode, note=note,
                                   **tally))
                stash[(key, name, mode)] = (cs, sd, cand)
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    with open(os.path.join(HERE, "data", "nearmiss_%s.json" % "_".join(keys)),
              "w") as f:
        json.dump(report, f, indent=1)
    import pickle
    with open(os.path.join(HERE, "data", "nearmiss_%s.pkl" % "_".join(keys)),
              "wb") as f:
        pickle.dump({k: (v[2],) for k, v in stash.items()}, f)
    print("\nwrote data/nearmiss_%s.json" % "_".join(keys))
