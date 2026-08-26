#!/usr/bin/env python3
"""
t3_theory.py -- machine certificates for the TARGET-3 theorems.

  Lemma 1  (field coincidence)   supp_m Delta supp_m' is a constant of the
                                 motion in any single-field constitution,
                                 either resolution, any window, any dimension.
  Lemma 2  (glider => one field) a glider is aligned: every occupied cell
                                 carries every kind.
  Theorem B (front speed)        beta(t+1) <= beta(t) + W,  alpha(t+1) >=
                                 alpha(t) - W;  hence |d| <= pW.
  Theorem C (front trichotomy)   at W=1 single field the front advances iff
                                 (isolated and u_{+1}) or (right-end and w_{+1}).
  Theorem D (advance spacing)    case IIIa: u_0 = 0 forbids two advances in a
                                 row (so d <= floor(p/2)); u_0 = 1 forces every
                                 later step to advance (so d <= 0 or d = p).
                                 case IIIb: same with (w_0, v_{+1}).
"""
from __future__ import annotations

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import xnomos                                                    # noqa: E402
from t3_core import (all_parity_classes, all_or_classes, rule_table,  # noqa
                     step_set, uvw_to_channels, UVW_to_channels, to_xnomos)
from t3_fast import compile_rule, fstep, from_set, to_set        # noqa: E402


def bitc(x, c):
    """component c in {-1,0,1} of a 3-bit vector/mask."""
    return (x >> (c + 1)) & 1


# ------------------------------------------------------------------ Lemma 1
def check_lemma1(trials=1500, seed=31):
    """supp_m Delta supp_m' constant along the orbit, single field, both modes,
    W in 1..2, dimension 1 and 2."""
    rng = random.Random(seed)
    checks = bad = 0
    for _ in range(trials):
        dim = rng.choice([1, 1, 2])
        W = rng.choice([1, 1, 2])
        n = rng.randrange(2, 5)
        if dim == 1:
            rules = [tuple(rng.randrange(-W, W + 1) for _ in range(3))
                     for _ in range(n)]
        else:
            rules = [tuple(tuple(rng.randrange(-W, W + 1) for _ in range(2))
                           for _ in range(3)) for _ in range(n)]
        C = xnomos.Const(rules, [tuple(range(n))] * n, dim=dim)
        S = {}
        for _ in range(rng.randrange(1, 8)):
            cell = (rng.randrange(-4, 5) if dim == 1
                    else (rng.randrange(-3, 4), rng.randrange(-3, 4)))
            S[cell] = S.get(cell, 0) | (1 << rng.randrange(n))
        for mode in ("parity", "or"):
            X = dict(S)
            base = None
            for _t in range(6):
                deltas = []
                for m in range(n):
                    for m2 in range(m + 1, n):
                        dd = frozenset(
                            c for c, msk in X.items()
                            if ((msk >> m) & 1) != ((msk >> m2) & 1))
                        deltas.append(dd)
                deltas = tuple(deltas)
                if base is None:
                    base = deltas
                else:
                    checks += 1
                    if deltas != base:
                        bad += 1
                X = xnomos.step(X, C, mode)
    return checks, bad


# ------------------------------------------------------------------ Theorem B
def check_theoremB(trials=3000, seed=32):
    rng = random.Random(seed)
    checks = bad = 0
    for _ in range(trials):
        W = rng.choice([1, 1, 2, 3])
        n = rng.randrange(1, 6)
        rules = [tuple(rng.randrange(-W, W + 1) for _ in range(3))
                 for _ in range(n)]
        C = xnomos.Const(rules, [tuple(range(n))] * n)
        cells = {rng.randrange(-6, 7) for _ in range(rng.randrange(1, 8))}
        S = {c: (1 << n) - 1 for c in cells}
        for mode in ("parity", "or"):
            X = dict(S)
            for _t in range(6):
                if not X:
                    break
                b, a = max(X), min(X)
                Y = xnomos.step(X, C, mode)
                if Y:
                    checks += 1
                    if max(Y) > b + W or min(Y) < a - W:
                        bad += 1
                X = Y
    return checks, bad


# ------------------------------------------------------------------ Theorem C
def check_theoremC(nconf=400, seed=33):
    """Exhaustive over all 512/343 classes x a battery of configurations."""
    rng = random.Random(seed)
    confs = [{i for i in range(10) if (m >> i) & 1} for m in range(1, 1 << 10)]
    for _ in range(nconf):
        sp = rng.randrange(2, 20)
        m = rng.getrandbits(sp) | 1 | (1 << (sp - 1))
        confs.append({i for i in range(sp) if (m >> i) & 1})
    tot = bad = 0
    caseI = caseII = 0
    for mode, classes in (("parity", all_parity_classes()),
                          ("or", all_or_classes())):
        for cls in classes:
            up1 = bitc(cls[0], 1)
            wp1 = bitc(cls[2], 1)
            tab = rule_table(cls, mode)
            if up1 == 0 and wp1 == 0:
                caseI += 1
            if up1 == 1 and wp1 == 1:
                caseII += 1
            for S in confs:
                b = max(S)
                e = 1 if (b - 1) in S else 0
                predicted = up1 if e == 0 else wp1
                T = step_set(S, tab)
                tot += 1
                if ((b + 1) in T) != bool(predicted):
                    bad += 1
                if T and max(T) > b + 1:
                    bad += 1
    return tot, bad, caseI, caseII


# ------------------------------------------------------------------ Theorem D
def check_theoremD(nconf=400, seed=34):
    """The advance-spacing dichotomy, exhaustive over classes."""
    rng = random.Random(seed)
    confs = [{i for i in range(11) if (m >> i) & 1} for m in range(1, 1 << 11)]
    for _ in range(nconf):
        sp = rng.randrange(2, 20)
        m = rng.getrandbits(sp) | 1 | (1 << (sp - 1))
        confs.append({i for i in range(sp) if (m >> i) & 1})
    tot = bad = 0
    tallies = {}
    for mode, classes in (("parity", all_parity_classes()),
                          ("or", all_or_classes())):
        for cls in classes:
            u, v, w = cls
            up1, wp1 = bitc(u, 1), bitc(w, 1)
            tab = rule_table(cls, mode)
            if up1 == 1 and wp1 == 0:
                key = (mode, "IIIa", bitc(u, 0))
                want_again = (bitc(u, 0) == 1)
            elif up1 == 0 and wp1 == 1 and bitc(v, 1) == 0:
                key = (mode, "IIIb", bitc(w, 0))
                want_again = (bitc(w, 0) == 0)
            else:
                continue
            tallies.setdefault(key, 0)
            tallies[key] += 1
            for S in confs:
                b = max(S)
                e = 1 if (b - 1) in S else 0
                adv = (up1 if e == 0 else wp1)
                if not adv:
                    continue
                T = step_set(S, tab)
                assert max(T) == b + 1
                b2 = b + 1
                e2 = 1 if b in T else 0
                adv2 = (up1 if e2 == 0 else wp1)
                tot += 1
                if bool(adv2) != want_again:
                    bad += 1
    return tot, bad, tallies


def main():
    print("Lemma 1  (field coincidence, single field, W<=2, dim 1 and 2)")
    n, b = check_lemma1()
    print("   %d orbit checks, %d violations" % (n, b))
    assert b == 0

    print("\nTheorem B  (front speed |d| <= pW)")
    n, b = check_theoremB()
    print("   %d step checks, %d violations" % (n, b))
    assert b == 0

    print("\nTheorem C  (front trichotomy, W=1 single field)")
    n, b, c1, c2 = check_theoremC()
    print("   %d front checks over ALL 512+343 classes, %d violations"
          % (n, b))
    print("   case I  (u_{+1}=w_{+1}=0, front frozen)      : %d classes" % c1)
    print("   case II (u_{+1}=w_{+1}=1, front advances always): %d classes"
          % c2)
    assert b == 0

    print("\nTheorem D  (advance spacing)")
    n, b, t = check_theoremD()
    print("   %d advance-pair checks, %d violations" % (n, b))
    for k in sorted(t):
        mode, case, bit = k
        print("      %-6s %s with the switching bit = %d : %d classes"
              % (mode, case, bit, t[k]))
    assert b == 0
    print("\nall theorem certificates passed")


if __name__ == "__main__":
    main()
