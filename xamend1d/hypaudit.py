#!/usr/bin/env python3
"""
hypaudit.py — hypothesis audit for Theorem 3 (supersession no-go).

Theorem 3 rests on exactly one asymmetry: **creation is own-kind (F1) even
though destruction is cross-kind (F2/F3)**.  This script builds the minimal
variant that breaks F1 and nothing else —

   SUPER-CROSS:  an active law of kind k with target cell j = i + c_k
                 * ENACTS kind phi(k) at j if j is empty   (phi a permutation)
                 * CLEARS the whole cell j if j is occupied

— and searches it exhaustively.  If gliders appear here and nowhere in plain
supersession, F1 is proved load-bearing rather than incidental.

The engine is written from scratch (not reusing xnomos.step) and is validated
against xnomos on the phi = identity case, where SUPER-CROSS is by definition
ordinary supersession.
"""
from __future__ import annotations

import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import xnomos


def step_cross(S, rules, phi, or_resolve=True):
    """S: dict cell -> bitmask.  Returns the next state."""
    occ = S
    clear_par, clear_any, enact = {}, set(), {}
    for cell, mask in S.items():
        m = mask
        while m:
            k = (m & -m).bit_length() - 1
            m &= m - 1
            a, b, c = rules[k]
            if (cell + a) in occ and (cell + b) not in occ:
                j = cell + c
                if j in occ:
                    clear_par[j] = clear_par.get(j, 0) ^ 1
                    clear_any.add(j)
                else:
                    tg = phi[k]
                    if isinstance(tg, int):
                        tg = (tg,)
                    for t_ in tg:
                        enact[j] = enact.get(j, 0) | (1 << t_)
    out = dict(S)
    for j in (clear_any if or_resolve else
              {j for j, p in clear_par.items() if p}):
        out.pop(j, None)
    for j, m in enact.items():
        out[j] = out.get(j, 0) | m
    return {j: m for j, m in out.items() if m}


def validate(trials=20000, seed0=4242):
    """phi = identity must reproduce xnomos supersession exactly."""
    rng = random.Random(seed0)
    for mode, orr in (("super_or", True), ("super", False)):
        for _ in range(trials // 2):
            n = rng.randrange(1, 4)
            rules = [tuple(rng.choice((-1, 0, 1)) for _ in range(3))
                     for _ in range(n)]
            S = {}
            for _ in range(rng.randrange(1, 7)):
                S[rng.randrange(-4, 5)] = S.get(rng.randrange(-4, 5), 0) | \
                                          (1 << rng.randrange(n))
            S = {c: m for c, m in S.items() if m}
            C = xnomos.Const(rules, [(k,) for k in range(n)])
            want = xnomos.step(S, C, mode)
            got = step_cross(S, rules, list(range(n)), or_resolve=orr)
            assert want == got, (mode, rules, S, want, got)
    print("hypaudit engine validated against xnomos on %d random states "
          "(phi = id, both clear-resolutions): exact match" % trials)


def normalize(S):
    lo = min(S)
    return tuple(sorted((c - lo, m) for c, m in S.items())), lo


def classify(S0, rules, phi, orr, max_steps=250, max_span=120):
    """Returns (kind, period, displacement, state_at_recurrence_start)."""
    S = dict(S0)
    seen = {}
    for t in range(max_steps):
        if not S:
            return ("EXTINCT", 0, 0, None)
        nm, anchor = normalize(S)
        if nm in seen:
            t0, a0, St0 = seen[nm]
            d = anchor - a0
            if d:
                return ("GLIDER", t - t0, d, St0)
            return ("CYCLE", t - t0, 0, St0)
        seen[nm] = (t, anchor, dict(S))
        if max(S) - min(S) > max_span:
            return ("GROWING", 0, 0, None)
        S = step_cross(S, rules, phi, orr)
    return ("UNRESOLVED", 0, 0, None)


def verify(S0, rules, phi, orr, p, d, reps=3):
    S = dict(S0)
    for r in range(1, reps + 1):
        for _ in range(p):
            S = step_cross(S, rules, phi, orr)
        if S != {c + d * r: m for c, m in S0.items()}:
            return False
    return True


def sweep(n=2, cells=5, orr=True, phi=None, max_steps=250, max_span=120):
    """COMPLETE sweep: all 27^n rule tuples x all seeds in `cells` cells."""
    phi = phi if phi is not None else [(k + 1) % n for k in range(n)]
    offs = (-1, 0, 1)
    R = list(itertools.product(offs, repeat=3))
    hits, total = [], 0
    seeds = []
    for mask in range(1, 1 << (cells * n)):
        S = {}
        for i in range(cells):
            m = (mask >> (i * n)) & ((1 << n) - 1)
            if m:
                S[i] = m
        lo = min(S)
        S = {c - lo: m for c, m in S.items()}
        seeds.append(S)
    uniq = {tuple(sorted(s.items())): s for s in seeds}
    seeds = list(uniq.values())
    for rules in itertools.product(R, repeat=n):
        for S in seeds:
            total += 1
            kind, p, d, St0 = classify(S, list(rules), phi, orr,
                                       max_steps, max_span)
            if kind == "GLIDER":
                # the glider is the state AT the recurrence, not the seed
                assert verify(St0, list(rules), phi, orr, p, d), (rules, S, St0)
                hits.append((list(rules), sorted(St0.items()), p, d))
    return hits, total, len(seeds)


if __name__ == "__main__":
    import time
    validate(4000)

    # (1) SUPER-CROSS: creation channel is a PERMUTATION (out-degree 1).
    for orr in (True, False):
        t0 = time.time()
        hits, total, ns = sweep(n=2, cells=5, orr=orr)
        print("\nSUPER-CROSS n=2, phi = swap, clear-resolution %s"
              % ("OR" if orr else "parity"))
        print("  COMPLETE: 27^2 = 729 constitutions x %d canonical seeds "
              "in 5 cells = %d classifications  (%.0fs)"
              % (ns, total, time.time() - t0))
        print("  GLIDERS (all re-verified over 3 periods): %d" % len(hits))

    # (2) SUPER-MULTI: same guards, same offsets, same clearing -- only the
    #     creation channel gains out-degree 2.  This is the controlled
    #     experiment behind the Out-Degree Law.
    for orr in (True, False):
        hits, total, ns = sweep(n=2, cells=4, orr=orr, phi=[(0, 1), (0, 1)],
                                max_steps=80, max_span=40)
        print("\nSUPER-MULTI n=2, T_0 = T_1 = {0,1}, clear-resolution %s"
              % ("OR" if orr else "parity"))
        print("  COMPLETE: 729 constitutions x %d canonical seeds in 4 cells "
              "= %d classifications" % (ns, total))
        print("  GLIDERS (all re-verified over 3 periods): %d" % len(hits))
        for h in hits[:3]:
            print("    rules=%s seed=%s p=%d d=%+d" % tuple(h))
