#!/usr/bin/env python3
"""
t3_fast.py -- bit-parallel engine + glider hunt for the single-field W=1 CA.

Configurations are (bits, lo) with bit i of `bits` = occ(lo + i).  One CA step
is computed with 32 minterms of bitwise operations, so it costs O(1) machine
words per step instead of O(span) Python-set operations.

`glider(S)` returns the generator (p0, d0) of  G(S) = {(t,x) : Phi^t S = s^x S}
-- the minimal period and the displacement per minimal period.
"""
from __future__ import annotations

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from t3_core import rule_table, step_set            # noqa: E402


def compile_rule(cls, mode="parity"):
    tab = rule_table(cls, mode)
    minterms = [m for m in range(32) if tab[m]]
    return tuple(minterms)


def fstep(bits, lo, minterms):
    """One step.  Returns (bits, lo) normalised (bit 0 set) or (0, 0)."""
    if not bits:
        return 0, 0
    L = bits.bit_length()
    ext = bits << 2                 # origin o = lo - 2
    width = L + 4                   # output cells o+0 .. o+L+3
    mask = (1 << width) - 1
    xs = []
    for k in range(5):
        xs.append((ext >> (k - 2)) if k >= 2 else (ext << (2 - k)))
    res = 0
    for m in minterms:
        acc = mask
        for k in range(5):
            acc &= xs[k] if (m >> k) & 1 else ~xs[k]
            if not acc:
                break
        res |= acc
    res &= mask
    if not res:
        return 0, 0
    o = lo - 2
    shift = (res & -res).bit_length() - 1
    return res >> shift, o + shift


def to_set(bits, lo):
    return {lo + i for i in range(bits.bit_length()) if (bits >> i) & 1}


def from_set(S):
    lo = min(S)
    b = 0
    for x in S:
        b |= 1 << (x - lo)
    return b, lo


def glider(S, minterms, max_steps=3000, max_card=1200, max_span=4000):
    """(kind, p0, d0, span).  kind: EXTINCT/FIXED/CYCLE/GLIDER/GROW/OPEN."""
    bits, lo = from_set(S)
    seen = {}
    for t in range(max_steps):
        if not bits:
            return ("EXTINCT", None, None, None)
        L = bits.bit_length()
        if L > max_span or bin(bits).count("1") > max_card:
            return ("GROW", None, None, None)
        prev = seen.get(bits)
        if prev is not None:
            t0, lo0 = prev
            p, d = t - t0, lo - lo0
            if d == 0:
                return ("FIXED" if p == 1 else "CYCLE", p, 0, L)
            return ("GLIDER", p, d, L)
        seen[bits] = (t, lo)
        bits, lo = fstep(bits, lo, minterms)
    return ("OPEN", None, None, None)


def _check_fast_matches_slow(trials=300, seed=3):
    from t3_core import all_parity_classes, all_or_classes
    rng = random.Random(seed)
    par = all_parity_classes()
    orc = all_or_classes()
    n = 0
    for _ in range(trials):
        for mode, pool in (("parity", par), ("or", orc)):
            cls = rng.choice(pool)
            mt = compile_rule(cls, mode)
            tab = rule_table(cls, mode)
            S = {rng.randrange(-8, 9) for _ in range(rng.randrange(1, 10))}
            bits, lo = from_set(S)
            for _t in range(8):
                S = step_set(S, tab)
                bits, lo = fstep(bits, lo, mt)
                n += 1
                assert to_set(bits, lo) == S, (cls, mode, sorted(S),
                                               sorted(to_set(bits, lo)))
                if not S:
                    break
    return n


def hunt(cls, mode="parity", rng=None, nseed=3000, max_seed_span=22,
         max_steps=3000):
    """All minimal (p0,d0) found from a seed sample; value = (seed, span)."""
    mt = compile_rule(cls, mode)
    rng = rng or random.Random(1)
    out = {}
    seeds = [{i for i in range(10) if (m >> i) & 1} for m in range(1, 1 << 10)]
    for _ in range(nseed):
        sp = rng.randrange(2, max_seed_span + 1)
        m = rng.getrandbits(sp) | 1
        seeds.append({i for i in range(sp) if (m >> i) & 1})
    for S in seeds:
        if not S:
            continue
        kind, p, d, span = glider(S, mt, max_steps=max_steps)
        if kind == "GLIDER":
            key = (p, d)
            if key not in out or span < out[key][1]:
                out[key] = (sorted(S), span)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "parity"
    nseed = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    from t3_core import all_parity_classes, all_or_classes
    classes = all_parity_classes() if mode == "parity" else all_or_classes()
    rng = random.Random(20260826)
    best = {}
    per_class = {}
    for i, cls in enumerate(classes):
        f = hunt(cls, mode, rng=rng, nseed=nseed)
        if f:
            per_class[cls] = max(abs(d) for (p, d) in f)
            for (p, d), (S, span) in f.items():
                if (p, d) not in best or span < best[(p, d)][2]:
                    best[(p, d)] = (cls, S, span)
        if (i + 1) % 64 == 0:
            mx = max(per_class.values()) if per_class else 0
            print("  %d/%d classes, max |d0| so far = %d"
                  % (i + 1, len(classes), mx), flush=True)
    print("\nmode=%s   classes with a glider: %d/%d"
          % (mode, len(per_class), len(classes)))
    mx = max(abs(d) for (p, d) in best) if best else 0
    print("MAX |d0| found: %d" % mx)
    print("distinct minimal (p0,d0): %d" % len(best))
    for (p, d) in sorted(best, key=lambda k: (-abs(k[1]), k[0]))[:40]:
        cls, S, span = best[(p, d)]
        print("   p0=%3d d0=%+4d  class=%s seed=%s span=%d"
              % (p, d, cls, S, span))
    import json
    out = os.path.join(HERE, "t3_hunt_%s.json" % mode)
    with open(out, "w") as fh:
        json.dump({"per_class": {str(k): v for k, v in per_class.items()},
                   "best": {str(k): [list(v[0]), v[1], v[2]]
                            for k, v in best.items()}}, fh)
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        n = _check_fast_matches_slow()
        print("fast engine == reference engine on %d steps" % n)
    else:
        main()
