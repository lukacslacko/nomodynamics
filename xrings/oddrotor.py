#!/usr/bin/env python3
"""
oddrotor.py — the odd-ring rotor question, focused.

Own-kind nomodynamics has NO rotor on any odd ring (complete state spaces
m <= 19; SAT decision m <= 31).  Cross-amendment breaks that.  This script
(1) locates the smallest odd ring carrying a rotor, per constitution class,
(2) minimises the law count of the witness (z3 cardinality constraint),
(3) separates BARBER POLES (apparent rotation faster than the light cone,
    min(r, m-r) > 2p) from TRANSPORTING rotors, and asks the sharper
    question: does an odd ring carry a transporting rotor?
"""
import itertools
import sys
import time

from z3 import Solver, Bool, Or, And, Not, PbLe, sat, unsat

import satrotor as S
from xring import Ring, RULES12, RULES27
from certify import certify_rotor


def find(rules, targets, mode, m, p, rs, maxcard=None, timeout_ms=120000):
    s = Solver()
    s.set("timeout", timeout_ms)
    n = len(rules)
    X = S.build(s, rules, targets, mode, m, p, "a")
    sel = [Bool("sel_%d" % r) for r in rs]
    s.add(Or(sel))
    for si, r in zip(sel, rs):
        cond = [X[p][k][i] == X[0][k][(i - r) % m]
                for k in range(n) for i in range(m)]
        cond.append(Or([X[0][k][i] != X[0][k][(i - r) % m]
                        for k in range(n) for i in range(m)]))
        s.add(Or(Not(si), And(cond)))
    s.add(Or([X[0][k][i] for k in range(n) for i in range(m)]))
    if maxcard is not None:
        s.add(PbLe([(X[0][k][i], 1) for k in range(n) for i in range(m)],
                   maxcard))
    if s.check() != sat:
        return None
    mdl = s.model()
    r = next(rs[i] for i in range(len(rs))
             if mdl.evaluate(sel[i], model_completion=True))
    W = tuple(sum((1 << i) for i in range(m)
                  if mdl.evaluate(X[0][k][i], model_completion=True))
              for k in range(n))
    return r, W


def report(rules, targets, mode, m, p, r, W):
    R = Ring(list(rules), list(targets), m, mode)
    ok = certify_rotor(list(rules), list(targets), m, mode, W, p, r, 0)
    card = R.card(W)
    d = min(r % m, (-r) % m)
    kind = "TRANSPORTING" if d <= 2 * p else "barber-pole"
    print("    m=%-3d p=%d rot=%-3d laws=%-3d %-13s cert=%s  %s"
          % (m, p, r, card, kind, ok, R.render(W)))
    Y = W
    for t in range(min(2 * p + 1, 7)):
        print("      t=%d %s" % (t, R.render(Y)))
        Y = R.step(Y)
    return ok


def scan(pool, tmaps, modes, ms, pmax, n, transporting_only=False,
         limit=None):
    found = []
    t0 = time.time()
    calls = 0
    for m in ms:
        hit_this_m = 0
        for rules in itertools.product(pool, repeat=n):
            for targets in tmaps:
                for mode in modes:
                    if mode in ("super", "super_or") and targets != tmaps[0]:
                        continue
                    for p in range(1, pmax + 1):
                        rs = [r for r in range(1, m)
                              if (not transporting_only)
                              or min(r, m - r) <= 2 * p]
                        if not rs:
                            continue
                        calls += 1
                        w = find(list(rules), list(targets), mode, m, p, rs)
                        if w:
                            found.append((m, p, rules, targets, mode) + w)
                            hit_this_m += 1
                            if limit and hit_this_m >= limit:
                                break
                    if limit and hit_this_m >= limit:
                        break
                if limit and hit_this_m >= limit:
                    break
            if limit and hit_this_m >= limit:
                break
        print("  m=%-3d : %d hits (%d SAT calls, %.0fs)"
              % (m, hit_this_m, calls, time.time() - t0), flush=True)
    return found


def main():
    what = sys.argv[1]
    if what == "own":
        print("own-kind (1 kind), odd rings m=3..41, p<=4, all 27 kinds:")
        f = scan(RULES27, [(0,)], ["parity"], list(range(3, 42, 2)), 4, 1)
        print("  total rotors: %d" % len(f))
    elif what == "cross":
        print("2 live kinds, odd rings, p<=2, all target classes:")
        f = scan(RULES12, [(1, 0), (0, 1), (0, 0)],
                 ["parity", "or", "super", "super_or"],
                 [13, 15, 17, 19, 21], 2, 2, limit=3)
        for (m, p, rules, tg, mode, r, W) in f:
            print("  %s -> %s [%s]" % (list(rules), list(tg), mode))
            report(rules, tg, mode, m, p, r, W)
    elif what == "transport":
        print("TRANSPORTING rotors on ODD rings (light-cone-respecting), "
              "2 live kinds, m=5..21 odd, p<=4:")
        f = scan(RULES12, [(1, 0), (0, 1), (0, 0)],
                 ["parity", "or", "super", "super_or"],
                 list(range(5, 22, 2)), 4, 2, transporting_only=True, limit=2)
        for (m, p, rules, tg, mode, r, W) in f:
            print("  %s -> %s [%s]" % (list(rules), list(tg), mode))
            report(rules, tg, mode, m, p, r, W)
        print("  total: %d" % len(f))
    elif what == "minimal":
        print("minimising the law count of the m=15 odd-ring rotors:")
        for (rules, tg, mode, p) in [
                ([(-1, 1, 1), (0, 1, -1)], [0, 0], "parity", 1),
                ([(-1, 1, 0), (0, -1, 1)], [1, 0], "parity", 2)]:
            best = None
            for c in range(2, 26):
                w = find(rules, tg, mode, 15, p, list(range(1, 15)),
                         maxcard=c)
                if w:
                    best = (c, w)
                    break
            print("  %s -> %s [%s] p=%d : minimum %d laws"
                  % (rules, tg, mode, p, best[0]))
            report(rules, tg, mode, 15, p, best[1][0], best[1][1])


if __name__ == "__main__":
    main()
