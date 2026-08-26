#!/usr/bin/env python3
"""
t4_odlaw.py -- TARGET 4 (c): the RUN-BUDGET argument and the one-step
out-degree theorem, with its machine checks.

  Exposure Bound.   For every kind k, |E_k| <= beta(X_k), where E_k is the set
     of active kind-k laws and beta(X) the number of maximal runs of X on the
     ring.   (b_k = 0 or a_k = b_k: E_k empty.  b_k = -1: an active law sits at
     a cell of X_k whose left neighbour is UNOCCUPIED, hence at the start of a
     run of X_k -- one per run.  b_k = +1: symmetric.)

  Change Budget.    sum_t |Phi(S)_t  xor  S_t|  <=  sum_k |T_k| * beta(X_k).

  Rotation Cost.    sum_t |rot_{+-1}(S)_t xor S_t| = 2 * sum_t beta(X_t).

  THEOREM D.  If every used kind has |T_k| <= 1 then no ring code satisfies
     Phi(S) = rot_{+-1}(S) != S, on any Z/m, in any number of kinds, under
     parity or or.  (2*sum beta <= sum beta forces sum beta = 0.)
     Out-degree 2 makes the two sides equal -- the threshold is exact, and
     TANDEM-1 and the HOLE ROTOR both sit on the equality.

Checks:
  * randomised: the Exposure Bound and the Change Budget on random
    (constitution, code) pairs of 1..4 kinds;
  * COMPLETE: over all 2^(n*m) codes of every 2-kind constitution with
    out-degree <= 1, m = 3..MAX, parity and or -- zero d = +-1 rotors;
    and the same sweep over the out-degree-2 maps, which finds them.
"""

from __future__ import annotations

import itertools
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from t4_ring import Ring
from t4_census import transition, RULES1

OFFS = (-1, 0, 1)


def beta(x, m):
    """Number of maximal runs of the m-bit cyclic word x."""
    if x == 0:
        return 0
    if x == (1 << m) - 1:
        return 0                       # the full ring has no boundary
    return bin(x ^ (((x << 1) | (x >> (m - 1))) & ((1 << m) - 1))).count("1") // 2


def popcount(x):
    return bin(x).count("1")


def randomised(trials=8000, seed=4242):
    rng = random.Random(seed)
    bad_exp = bad_bud = 0
    for _ in range(trials):
        n = rng.randrange(1, 5)
        m = rng.randrange(3, 14)
        mode = rng.choice(["parity", "or"])
        rules = [(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                 for _ in range(n)]
        targets = [tuple(k for k in range(n) if rng.random() < 0.5)
                   for _ in range(n)]
        R = Ring(rules, targets, m, mode)
        X = tuple(rng.randrange(1 << m) for _ in range(n))
        occ = R.occ(X)
        # exposure bound, per kind
        for k in range(n):
            a, b, c = rules[k]
            act = X[k] & R.rot(occ, -a) & (~R.rot(occ, -b)) & R.mask
            if popcount(act) > beta(X[k], m):
                bad_exp += 1
        # change budget
        Y = R.step(X)
        change = sum(popcount(Y[t] ^ X[t]) for t in range(n))
        budget = 0
        for k in range(n):
            a, b, c = rules[k]
            budget += len(targets[k]) * beta(X[k], m)
        if change > budget:
            bad_bud += 1
    print("randomised: %d (constitution, code) pairs; exposure-bound "
          "violations %d ; change-budget violations %d"
          % (trials, bad_exp, bad_bud))
    return bad_exp, bad_bud


def rot_perm(m, n, dt):
    """R1[s] = the packed state rot_1(s)."""
    N = 1 << (n * m)
    s = np.arange(N, dtype=dt)
    mask = (1 << m) - 1
    out = np.zeros(N, dtype=dt)
    for k in range(n):
        x = (s >> dt(k * m)) & dt(mask)
        x = ((x << dt(1)) | (x >> dt(m - 1))) & dt(mask)
        out |= x << dt(k * m)
    return out


TARGETS2_ALL = list(itertools.product([(), (0,), (1,), (0, 1)], repeat=2))
TARGETS2_OD1 = [t for t in TARGETS2_ALL if all(len(x) <= 1 for x in t)]
TARGETS2_OD2 = [t for t in TARGETS2_ALL if max(len(x) for x in t) == 2]


def complete_d1(maps, ms, label, dump=None):
    """Complete sweep: how many codes satisfy Phi(S) = rot_1(S) != S?"""
    rules2 = list(itertools.product(RULES1, repeat=2))
    print("\n%s -- COMPLETE over all 2^(2m) codes, %d rule pairs x %d target "
          "maps, parity+or" % (label, len(rules2), len(maps)))
    found = []
    for m in ms:
        N = 1 << (2 * m)
        dt = np.uint32
        R1 = rot_perm(m, 2, dt)
        idx = np.arange(N, dtype=dt)
        movable = R1 != idx                    # rot_1(S) != S  (hygiene)
        tot = 0
        t0 = time.time()
        for rules in rules2:
            for targets in maps:
                for mode in ("parity", "or"):
                    if mode == "or" and all(
                            sum(1 for k in (0, 1) if u in targets[k]) <= 1
                            for u in (0, 1)):
                        continue
                    f = transition(rules, targets, m, 2, mode)
                    hit = (f == R1) & movable
                    c = int(hit.sum())
                    if c:
                        tot += c
                        w = int(np.flatnonzero(hit)[0])
                        found.append((m, rules, targets, mode, c, w))
        print("   m=%-3d  codes with Phi(S) = rot_1(S) != S : %-8d  (%.0f s)"
              % (m, tot, time.time() - t0), flush=True)
    return found


if __name__ == "__main__":
    randomised()
    MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    f1 = complete_d1(TARGETS2_OD1, range(3, MAX + 1),
                     "OUT-DEGREE <= 1 (the 9 maps with |T_k| <= 1)")
    print("   >>> out-degree<=1 witnesses found: %d  <<<" % len(f1))
    for r in f1[:10]:
        print("      ", r)
    f2 = complete_d1(TARGETS2_OD2, range(3, min(MAX, 9) + 1),
                     "OUT-DEGREE 2 (the 7 maps with some |T_k| = 2)")
    print("   >>> out-degree-2 constitutions carrying a d=+1 rotor: %d "
          "(m, rules, targets, mode, #codes, one witness) <<<" % len(f2))
    seen = set()
    for r in f2:
        key = (r[1], r[2], r[3])
        if key not in seen:
            seen.add(key)
    print("   distinct out-degree-2 constitutions with a d=+1 rotor: %d"
          % len(seen))
    for r in f2[:12]:
        m, rules, targets, mode, c, w = r
        R = Ring(list(rules), list(targets), m, mode)
        X = tuple((w >> (k * m)) & ((1 << m) - 1) for k in range(2))
        print("      m=%d %s -> %s [%s] %d codes; e.g. %s"
              % (m, rules, targets, mode, c, R.render(X)))
