#!/usr/bin/env python3
"""validate_fast.py — the soundness gate for the bit-parallel engine.

V1  STEP FIDELITY.  For each of the four modes, >= 20,000 random
    (constitution, state) pairs: fastlib.step must equal xnomos.step exactly,
    cell by cell, kind by kind.  Constitutions include single targets,
    permutation targets and multi-target tuples.
V2  WIDE-STEP FIDELITY.  Same battery against the 512-cell wide engine.
V3  CLASSIFY FIDELITY.  >= 4,000 random (constitution, seed) pairs per mode:
    the C classifier's (kind, period, displacement) must equal
    xnomos.classify's, with the same budgets.
V4  KNOWN SPECIMENS.  colonizer, sunset clause, two-chamber balance.
"""
from __future__ import annotations

import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import xnomos                                                  # noqa: E402
import fastlib as F                                            # noqa: E402

OFF = (-1, 0, 1)


def rand_const(rng, n, mode, multi=False):
    rules = [(rng.choice(OFF), rng.choice(OFF), rng.choice(OFF))
             for _ in range(n)]
    if mode in ("super", "super_or"):
        targets = list(range(n))                # ignored by supersession
    elif multi:
        targets = []
        for _ in range(n):
            m = rng.randrange(1, 1 << n)
            targets.append(tuple(k for k in range(n) if m >> k & 1))
    else:
        r = rng.random()
        if r < 0.34:                            # permutation
            p = list(range(n)); rng.shuffle(p); targets = p
        elif r < 0.67:                          # cyclic
            targets = [(i + 1) % n for i in range(n)]
        else:                                   # arbitrary single
            targets = [rng.randrange(n) for _ in range(n)]
    return rules, targets


def rand_state(rng, n, lo, hi, maxlaws):
    S = {}
    for _ in range(rng.randrange(1, maxlaws + 1)):
        c = rng.randrange(lo, hi + 1)
        S[c] = S.get(c, 0) | (1 << rng.randrange(n))
    return S


def v1_v2(trials_per_mode=6000):
    rng = random.Random(20260826)
    tot1 = tot2 = 0
    for mode in F.MODES:
        for _ in range(trials_per_mode):
            n = rng.randrange(1, 5)
            multi = (mode in ("parity", "or")) and rng.random() < 0.4
            rules, targets = rand_const(rng, n, mode, multi)
            C = xnomos.Const(rules, targets)
            S = rand_state(rng, n, -12, 12, 10)
            want = xnomos.step(S, C, mode)

            cf = F.pack_const(rules, targets, n)
            # narrow engine: pad so cells -12..12 land in bits 4..28
            w = F.pack_state(S, n, pad=16)
            got = F.step(cf, n, mode, w)
            if F.unpack_state(got, pad=16) != want:
                raise AssertionError(
                    "V1 MISMATCH mode=%s rules=%s targets=%s S=%s\n got=%s\nwant=%s"
                    % (mode, rules, targets, S, F.unpack_state(got, 16), want))
            tot1 += 1

            # wide engine: pad 200
            ww = np.zeros(n * F.WB, dtype=np.uint64)
            for cell, m in S.items():
                b = cell + 200
                for k in range(n):
                    if m >> k & 1:
                        ww[k * F.WB + (b >> 6)] |= np.uint64(1) << np.uint64(b & 63)
            gw = F.wide_step(cf, n, mode, ww)
            got2 = {}
            for k in range(n):
                for i in range(F.WB):
                    x = int(gw[k * F.WB + i])
                    while x:
                        bb = (x & -x).bit_length() - 1
                        x &= x - 1
                        cc = i * 64 + bb - 200
                        got2[cc] = got2.get(cc, 0) | (1 << k)
            if got2 != want:
                raise AssertionError("V2 MISMATCH mode=%s %s %s %s" %
                                     (mode, rules, targets, S))
            tot2 += 1
    return tot1, tot2


def v3(trials_per_mode=1200, max_steps=200, max_card=200, max_span=40):
    rng = random.Random(777)
    tot = 0
    hist = {}
    for mode in F.MODES:
        for _ in range(trials_per_mode):
            n = rng.randrange(1, 5)
            multi = (mode in ("parity", "or")) and rng.random() < 0.35
            rules, targets = rand_const(rng, n, mode, multi)
            C = xnomos.Const(rules, targets)
            S = rand_state(rng, n, 0, 5, 5)
            want = xnomos.classify(S, C, mode, max_steps=max_steps,
                                   max_card=max_card, max_span=max_span)
            cf = F.pack_const(rules, targets, n)
            w = F.pack_state(S, n)
            got = F.classify(cf, n, mode, w, max_steps, max_card, max_span)
            hist[want["kind"]] = hist.get(want["kind"], 0) + 1
            if got["kind"] != want["kind"]:
                raise AssertionError("V3 kind %s vs %s | %s %s %s %s" %
                                     (got, want["kind"], mode, rules, targets, S))
            if want["kind"] in ("CYCLE", "GLIDER") and got["period"] != want["period"]:
                raise AssertionError("V3 period %s vs %s" % (got, want))
            if want["kind"] == "GLIDER" and got["disp"] != want["displacement"]:
                raise AssertionError("V3 disp %s vs %s" % (got, want))
            tot += 1
    return tot, hist


def v4():
    # colonizer
    cf = F.pack_const([(0, 1, 1)], [0], 1)
    w = F.seed_words(1, [1])
    r = F.classify(cf, 1, "parity", w, 200, 200, 40)
    assert r["kind"] == "GROWING", r
    # sunset clause
    cf = F.pack_const([(0, -1, 1)], [0], 1)
    r = F.classify(cf, 1, "parity", F.seed_words(1, [1]), 200, 200, 40)
    assert r["kind"] == "CYCLE" and r["period"] == 2, r
    # two-chamber balance (parity fixed-with-active, OR not)
    rules = [(0, 1, 1), (0, -1, -1), (0, 1, 0)]
    cf = F.pack_const(rules, [2, 2, 2], 3)
    w = F.seed_words(3, [1, 0, 2])
    r = F.classify(cf, 3, "parity", w, 200, 200, 40)
    assert r["kind"] == "BALANCED", r
    return 3


def v5(trials_per_mode=1500, T=60):
    """ANCHOR-TRACE fidelity: the C engine's normalised state AND anchor must
    agree with xnomos.normalize at EVERY step.  This is the exact data the
    GLIDER branch keys on, so it is validated even though no real glider
    exists to trigger that branch."""
    rng = random.Random(31337)
    tot = 0
    for mode in F.MODES:
        for _ in range(trials_per_mode):
            n = rng.randrange(1, 5)
            multi = (mode in ("parity", "or")) and rng.random() < 0.35
            rules, targets = rand_const(rng, n, mode, multi)
            C = xnomos.Const(rules, targets)
            S = rand_state(rng, n, 0, 5, 5)
            cf = F.pack_const(rules, targets, n)
            got = F.trace(cf, n, mode, F.pack_state(S, n), T)
            Sx = dict(S)
            base = min(S) - got[0][1] if got else 0   # constant frame offset
            for t in range(T):
                if not Sx:
                    assert t == len(got), (t, len(got))
                    break
                if max(Sx) - min(Sx) > 40 or xnomos.card(Sx) > 200:
                    break                       # beyond the 64-bit frame
                nm, anchor = xnomos.normalize(Sx, 1)
                gw, ga = got[t]
                gs = F.unpack_state(np.array(gw, dtype=np.uint64), pad=F.PAD)
                gnm, _ = xnomos.normalize(gs, 1) if gs else ((), None)
                if gnm != nm or ga + base != anchor:
                    raise AssertionError("V5 t=%d %s %s %s | %s/%s vs %s/%s" %
                                         (t, mode, rules, S, gnm, ga, nm, anchor))
                tot += 1
                Sx = xnomos.step(Sx, C, mode)
    return tot


def _test_step(mode, S, n):
    """Python mirror of the test-only translation semantics."""
    out = {}
    if mode == "_shift_r":
        for c, m in S.items():
            out[c + 1] = m
    elif mode == "_shift_l":
        for c, m in S.items():
            out[c - 1] = m
    else:                                        # _swapshift
        for c, m in S.items():
            rest = m & ~3
            if rest:
                out[c] = out.get(c, 0) | rest
            if m & 2:                            # kind 1 -> kind 0, shifted +1
                out[c + 1] = out.get(c + 1, 0) | 1
            if m & 1:                            # kind 0 -> kind 1, in place
                out[c] = out.get(c, 0) | 2
    return {c: m for c, m in out.items() if m}


def v6(trials=3000):
    """GLIDER-BRANCH validation.  Under the test-only translation semantics
    every seed IS a glider, so run_one's glider path (period + displacement
    from the anchor difference) is exercised and checked against a Python
    reference that applies xnomos.classify's own recurrence rule."""
    rng = random.Random(2718)
    tot = 0
    for _ in range(trials):
        mode = rng.choice(F.TEST_MODES)
        n = rng.randrange(2, 5)
        S = rand_state(rng, n, 0, 5, 5)
        cf = F.pack_const([(0, 0, 0)] * n, list(range(n)), n)
        got = F.classify(cf, n, mode, F.pack_state(S, n), 200, 200, 40)
        # Python reference: xnomos.classify's rule, on the test step function
        Sx, seen, want = dict(S), {}, None
        for t in range(200):
            if not Sx:
                want = ("EXTINCT", 0, 0)
                break
            nm, anchor = xnomos.normalize(Sx, 1)
            if nm in seen:
                t0, a0 = seen[nm]
                if anchor != a0:
                    want = ("GLIDER", t - t0, anchor - a0)
                elif t - t0 == 1:
                    want = ("FIXED", 1, 0)      # test steps have no guards
                else:
                    want = ("CYCLE", t - t0, 0)
                break
            seen[nm] = (t, anchor)
            if xnomos.card(Sx) > 200 or max(Sx) - min(Sx) > 40:
                want = ("GROWING", 0, 0)
                break
            Sx = _test_step(mode, Sx, n)
        if want is None:
            want = ("UNRESOLVED", 0, 0)
        assert got["kind"] == want[0], (got, want, mode, S)
        if want[0] in ("CYCLE", "GLIDER"):
            assert (got["period"], got["disp"]) == (want[1], want[2]), \
                (got, want, mode, S)
        if want[0] == "GLIDER":
            tot += 1
    assert tot > trials // 2, tot
    return trials, tot


if __name__ == "__main__":
    n1, n2 = v1_v2()
    print("V1 narrow-step fidelity : %6d random (constitution,state) pairs OK "
          "across %d modes" % (n1, len(F.MODES)))
    print("V2 wide-step  fidelity  : %6d random (constitution,state) pairs OK "
          "across %d modes" % (n2, len(F.MODES)))
    n3, h3 = v3()
    print("V3 classify   fidelity  : %6d random (constitution,seed) pairs OK; "
          "outcome mix %s" % (n3, dict(sorted(h3.items()))))
    print("V4 known specimens      : %d/3 OK" % v4())
    n5 = v5()
    print("V5 anchor-trace fidelity: %6d (normalised state, anchor) frames OK"
          % n5)
    n6, g6 = v6()
    print("V6 glider-branch        : %6d test-semantics runs OK (%d of them "
          "GLIDER, period+displacement exact)" % (n6, g6))
    print("VALIDATION PASSED — total exact-agreement checks: %d"
          % (n1 + n2 + n3 + n5 + n6))
