#!/usr/bin/env python3
"""
t4_sat.py -- TARGET 4 (c): a SAT decider for light-cone-admissible ring rotors.

"Is there a code S on Z/m with Phi^p(S) = rot_d(S) and rot_d(S) != S?" is a
propositional formula in (p+1)*n*m variables with only local clauses, so z3
settles it far beyond any enumeration.  (Such an S is automatically recurrent:
Phi^{p*ord(d)}(S) = S.)  This reaches ring sizes the complete censuses cannot,
at the price of a BOUND ON p -- every table below states its p-box.

Validated against the complete enumerations of t4_census.py.
"""

from __future__ import annotations

import itertools
import json
import os
import sys
import time

import z3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from t4_ring import Ring, verify_rotation_recurrence, verify_via_xnomos

OFFS = (-1, 0, 1)
RULES1 = [(a, b, c) for a in OFFS for b in OFFS for c in OFFS]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "t4_data")


def rotor_sat(rules, targets, m, p, d, mode="parity", timeout_ms=20000):
    """Return a witness state (tuple of n bitmasks) or None."""
    n = len(rules)
    s = z3.Solver()
    s.set("timeout", timeout_ms)
    x = [[[z3.Bool("x_%d_%d_%d" % (t, k, i)) for i in range(m)]
          for k in range(n)] for t in range(p + 1)]
    for t in range(p):
        occ = [z3.Or(*[x[t][k][i] for k in range(n)]) for i in range(m)]
        act = []
        for k in range(n):
            a, b, _ = rules[k]
            act.append([z3.And(x[t][k][i], occ[(i + a) % m],
                               z3.Not(occ[(i + b) % m])) for i in range(m)])
        for u in range(n):
            for j in range(m):
                terms = []
                for k in range(n):
                    if u in targets[k]:
                        c = rules[k][2]
                        terms.append(act[k][(j - c) % m])
                if not terms:
                    s.add(x[t + 1][u][j] == x[t][u][j])
                elif mode == "parity":
                    flip = terms[0]
                    for e in terms[1:]:
                        flip = z3.Xor(flip, e)
                    s.add(x[t + 1][u][j] == z3.Xor(x[t][u][j], flip))
                else:
                    flip = z3.Or(*terms)
                    s.add(x[t + 1][u][j] == z3.Xor(x[t][u][j], flip))
    # closure  Phi^p(S) = rot_d(S):  rot_d(S)[j] = S[j-d]
    for k in range(n):
        for j in range(m):
            s.add(x[p][k][j] == x[0][k][(j - d) % m])
    # hygiene: rot_d(S) != S, and S nonempty
    s.add(z3.Or(*[x[0][k][j] != x[0][k][(j - d) % m]
                  for k in range(n) for j in range(m)]))
    s.add(z3.Or(*[x[0][k][j] for k in range(n) for j in range(m)]))
    r = s.check()
    if r != z3.sat:
        return None if r == z3.unsat else "TIMEOUT"
    mod = s.model()
    return tuple(sum(1 << i for i in range(m)
                     if z3.is_true(mod.eval(x[0][k][i], model_completion=True)))
                 for k in range(n))


def recertify(rules, targets, m, p, d, mode, X):
    R = Ring(rules, targets, m, mode)
    return (verify_rotation_recurrence(X, R, p, d)
            and verify_via_xnomos(X, R, p, d)
            and R.rot_state(X, d) != X)


def live(rule):
    a, b, c = rule
    return b != 0 and a != b            # otherwise the law can never fire


def campaign(name, cons, ms, pmax, modes=("parity",), verbose=True,
             positive_d_only=True):
    """cons: list of (rules, targets).  Decide every (m, p, d, mode) with
    1 <= p <= pmax and 1 <= |d| <= p (the strict light cone at W = 1).

    positive_d_only: the rule pool is closed under the mirror
    (a,b,c) -> (-a,-b,-c), which conjugates a d-rotor into a (-d)-rotor, so
    sweeping d > 0 over the whole pool is complete.
    """
    hits, calls, t0 = [], 0, time.time()
    for m in ms:
        found_m = 0
        for rules, targets in cons:
            if not any(live(r) for r in rules):
                continue                # nothing can ever fire: f = identity
            for mode in modes:
                if mode == "or" and all(
                        sum(1 for k in range(len(rules))
                            if u in targets[k]) <= 1
                        for u in range(len(rules))):
                    continue            # Single-Author: parity == or
                for p in range(1, pmax + 1):
                    lo = 1 if positive_d_only else -p
                    for d in range(lo, p + 1):
                        if d == 0 or d % m == 0:
                            continue
                        calls += 1
                        X = rotor_sat(rules, targets, m, p, d, mode)
                        if X is None:
                            continue
                        if X == "TIMEOUT":
                            hits.append({"m": m, "rules": rules,
                                         "targets": [list(t) for t in targets],
                                         "p": p, "d": d, "mode": mode,
                                         "status": "TIMEOUT"})
                            continue
                        ok = recertify(rules, targets, m, p, d, mode, X)
                        hits.append({"m": m, "rules": rules,
                                     "targets": [list(t) for t in targets],
                                     "p": p, "d": d, "mode": mode,
                                     "state": list(X), "recertified": ok})
                        found_m += 1
        if verbose:
            print("  m=%-3d  %d hits  (%d calls, %.0f s)"
                  % (m, found_m, calls, time.time() - t0), flush=True)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "t4_sat_%s.jsonl" % name), "w") as fh:
        for h in hits:
            fh.write(json.dumps(h) + "\n")
    print("%s: %d SAT decisions, %d light-cone-admissible rotors found"
          % (name, calls, len(hits)))
    return hits, calls


OD1_MAPS = [t for t in itertools.product([(0,), (1,)], repeat=2)]
OD2_MAPS = [t for t in itertools.product([(), (0,), (1,), (0, 1)], repeat=2)
            if max(len(x) for x in t) == 2]


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "own"
    if what == "control":
        # validation against the complete census: TANDEM-1 must be found on
        # every ring, and the own-kind class must be empty at p=1,|d|=1.
        print("TANDEM-1 sanity:")
        for m in (3, 5, 7, 9, 15, 21, 31, 45):
            X = rotor_sat([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)], m, 1, 1)
            print("   m=%-3d sat=%s recert=%s" % (
                m, X is not None,
                recertify([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)],
                          m, 1, 1, "parity", X) if X else "-"))
    elif what == "own":
        cons = [([r], [(0,)]) for r in RULES1]
        campaign("own1", cons, list(range(3, 42)), 6)
    elif what == "od1":
        rules2 = list(itertools.product(RULES1, repeat=2))
        cons = [(list(r), list(t)) for r in rules2 for t in OD1_MAPS]
        ms = [int(a) for a in sys.argv[2:]] or [9, 15, 21]
        campaign("od1", cons, ms, 3, modes=("parity", "or"))
    elif what == "od2":
        rules2 = list(itertools.product(RULES1, repeat=2))
        cons = [(list(r), list(t)) for r in rules2 for t in OD2_MAPS]
        ms = [int(a) for a in sys.argv[2:]] or [15]
        campaign("od2", cons, ms, 1, modes=("parity",))
    else:
        raise SystemExit(__doc__)
