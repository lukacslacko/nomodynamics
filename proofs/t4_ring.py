#!/usr/bin/env python3
"""
t4_ring.py -- TARGET 4 (Expedition Y-D): an INDEPENDENT bitmask ring engine
plus a rotation-recurrence checker that never calls xnomos.classify().

The engine here stores a ring code on Z/m as a tuple of n m-bit words, one per
kind (bit i of word k = "a law of kind k stands at cell i").  It shares no code
with xnomos.py; `crosscheck()` verifies the two agree step-for-step on random
inputs, which is what licenses every certificate produced by this file.

Conventions (identical to xnomos / xrings):
  rule[k] = (a,b,c);  law (i,k) is ACTIVE iff occ(i+a) and not occ(i+b);
  an active law emits one toggle of every kind in targets[k] at cell i+c;
  resolution 'parity' (flip on odd count) or 'or' (flip on >=1).
  rot_r(S) = every law moved r cells forward:  bit i -> bit i+r.
"""

from __future__ import annotations

import itertools
import random

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xnomos


# ------------------------------------------------------------------ the engine

class Ring:
    """A window-1 ring constitution, bitmask semantics.  Independent of xnomos."""

    __slots__ = ("rules", "targets", "m", "n", "mode", "mask", "srcs")

    def __init__(self, rules, targets, m, mode="parity"):
        self.rules = [tuple(r) for r in rules]
        self.n = len(rules)
        self.targets = [tuple(sorted(set(t))) for t in targets]
        self.m = m
        self.mode = mode
        self.mask = (1 << m) - 1
        # srcs[t] = kinds whose laws emit a toggle of kind t
        self.srcs = [[k for k in range(self.n) if t in self.targets[k]]
                     for t in range(self.n)]

    # rot_r: bit i -> bit i+r
    def rot(self, x, r):
        r %= self.m
        return ((x << r) | (x >> (self.m - r))) & self.mask if r else x

    def step(self, X):
        m, mask = self.m, self.mask
        occ = 0
        for x in X:
            occ |= x
        emit = []
        for k in range(self.n):
            a, b, c = self.rules[k]
            act = X[k] & self.rot(occ, -a) & (~self.rot(occ, -b)) & mask
            emit.append(self.rot(act, c))
        out = []
        for t in range(self.n):
            f = 0
            if self.mode == "parity":
                for k in self.srcs[t]:
                    f ^= emit[k]
            else:                                   # 'or'
                for k in self.srcs[t]:
                    f |= emit[k]
            out.append(X[t] ^ f)
        return tuple(out)

    def active_count(self, X):
        occ = 0
        for x in X:
            occ |= x
        tot = 0
        for k in range(self.n):
            a, b, c = self.rules[k]
            act = X[k] & self.rot(occ, -a) & (~self.rot(occ, -b)) & self.mask
            tot += bin(act).count("1")
        return tot

    def rot_state(self, X, r):
        return tuple(self.rot(x, r) for x in X)

    def occ(self, X):
        o = 0
        for x in X:
            o |= x
        return o

    def card(self, X):
        return sum(bin(x).count("1") for x in X)

    # ---- interop (only used to cross-check, never inside a certificate) ----
    def to_xnomos(self, X):
        pairs = []
        for k in range(self.n):
            for i in range(self.m):
                if (X[k] >> i) & 1:
                    pairs.append((i, k))
        return xnomos.state_of(pairs, self.n)

    def from_xnomos(self, S):
        X = [0] * self.n
        for cell, mask in S.items():
            for k in range(self.n):
                if (mask >> k) & 1:
                    X[k] |= 1 << (cell % self.m)
        return tuple(X)

    def xconst(self):
        return xnomos.Const(self.rules, [tuple(t) for t in self.targets],
                            dim=1, modulus=self.m)

    def render(self, X, sym="XYZWVUT"):
        out = []
        for i in range(self.m):
            s = "".join(sym[k] for k in range(self.n) if (X[k] >> i) & 1)
            out.append(s if s else ".")
        w = max(len(s) for s in out)
        return "|" + " ".join(s.ljust(w) for s in out) + "|"


# ------------------------------------------- vacancy / arc geometry on the ring

def vacant_arc(occ, m):
    """Length of the longest run of vacant cells of the occupancy word `occ`."""
    if occ == 0:
        return m
    if occ == (1 << m) - 1:
        return 0
    best = cur = 0
    # go round twice to catch the wrap-around run
    for i in range(2 * m):
        if not (occ >> (i % m)) & 1:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return min(best, m)


def support_arc_start(occ, m):
    """Start cell of the (unique maximal) support arc: the cell just after the
    longest vacant run.  Returns None if the ring is full or empty."""
    if occ == 0 or occ == (1 << m) - 1:
        return None
    best, bstart, cur, cstart = 0, None, 0, None
    for i in range(2 * m):
        j = i % m
        if not (occ >> j) & 1:
            if cur == 0:
                cstart = j
            cur += 1
            if cur > best:
                best, bstart = cur, cstart
        else:
            cur = 0
    return (bstart + best) % m


# ------------------------------------------------ the rotation-recurrence check

def rep(d, m):
    """Representative of d mod m in (-m/2, m/2]."""
    d %= m
    return d - m if 2 * d > m else d


def rotor_certificate(X0, R, pmax=None):
    """INDEPENDENT rotation-recurrence checker.

    Runs Phi from X0 and returns the minimal (p, d) with Phi^p(X0) = rot_d(X0),
    d given as the representative in (-m/2, m/2].  Returns None if the orbit is
    not purely periodic-up-to-rotation from X0 within the budget.

    Certificate hygiene: `sym` records whether rot_d(X0) == X0 (a rotationally
    symmetric code satisfies the identity for free -- such a hit is NOT a rotor).
    """
    m = R.m
    if pmax is None:
        pmax = 4 << m if m <= 14 else 100000
    rots = {}
    for d in range(m):
        rots.setdefault(R.rot_state(X0, d), d)
    X = X0
    for p in range(1, pmax + 1):
        X = R.step(X)
        if X in rots:
            d = rep(rots[X], m)
            return {"p": p, "d": d, "sym": R.rot_state(X0, d) == X0}
    return None


def verify_rotation_recurrence(X0, R, p, d, laps=3):
    """Re-check Phi^{p*j}(X0) = rot_{d*j}(X0) for j = 1..laps, from scratch."""
    X = X0
    for j in range(1, laps + 1):
        for _ in range(p):
            X = R.step(X)
        if X != R.rot_state(X0, d * j):
            return False
    return True


def verify_via_xnomos(X0, R, p, d, laps=3):
    """The same identity, recomputed entirely inside xnomos (Const/step)."""
    C = R.xconst()
    S = R.to_xnomos(X0)
    S0 = dict(S)
    for j in range(1, laps + 1):
        for _ in range(p):
            S = xnomos.step(S, C, R.mode)
        want = {}
        for cell, mm in S0.items():
            want[(cell + d * j) % R.m] = mm
        if S != want:
            return False
    return True


# ---------------------------------------------------------------- cross-check

def crosscheck(trials=4000, seed=20260826, verbose=True):
    """Ring engine == xnomos reference engine, on random constitutions/codes."""
    rng = random.Random(seed)
    offs = (-1, 0, 1)
    bad = 0
    for _ in range(trials):
        n = rng.randrange(1, 4)
        m = rng.randrange(3, 13)
        mode = rng.choice(["parity", "or"])
        rules = [(rng.choice(offs), rng.choice(offs), rng.choice(offs))
                 for _ in range(n)]
        targets = []
        for _ in range(n):
            sub = [k for k in range(n) if rng.random() < 0.5]
            targets.append(tuple(sub))
        R = Ring(rules, targets, m, mode)
        C = R.xconst()
        X = tuple(rng.randrange(1 << m) for _ in range(n))
        S = R.to_xnomos(X)
        for _ in range(6):
            X = R.step(X)
            S = xnomos.step(S, C, mode)
            if R.from_xnomos(S) != X:
                bad += 1
                break
    if verbose:
        print("crosscheck t4_ring vs xnomos: %d trials x 6 steps, %d mismatches"
              % (trials, bad))
    return bad


if __name__ == "__main__":
    assert crosscheck() == 0
    # arc helpers
    assert vacant_arc(0b0110110, 7) == 2
    assert vacant_arc(0b1111111, 7) == 0
    assert vacant_arc(0b0000001, 7) == 6
    assert support_arc_start(0b0000001, 7) == 0
    print("t4_ring self-tests passed")
