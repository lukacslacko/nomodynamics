#!/usr/bin/env python3
"""
xring.py — fast bitmask engine for CROSS-AMENDMENT nomodynamics on the ring Z/m.

Conventions (identical to xnomos.py; validated against it in `test_engine`):

  * kinds K = {0..n-1}; kind k carries rule (a_k, b_k, c_k) and target t(k)
  * a state is a tuple X = (x_0, ..., x_{n-1}) of m-bit ints; bit i of x_k is 1
    iff a law of kind k stands at cell i of Z/m
  * occupancy O = x_0 | ... | x_{n-1}     (OR, not XOR)
  * law (i,k) is ACTIVE iff O[i+a_k] = 1 and O[i+b_k] = 0
  * an active law of kind k at i emits one toggle of kind t(k) at cell i+c_k
  * resolution: 'parity' (XOR the emissions), 'or' (OR them),
    'super'/'super_or' = supersession (target ignored; enact own kind on empty
    ground, else clear the whole target cell; clear votes by parity / by OR)

Rotation:  rot_r(x)[i] = x[i-r], i.e. every law moves r cells forward.
A ROTOR is a state with Phi^p(X) = rot_r(X), r != 0 mod m.
A SCREW ROTOR (only meaningful for homogeneous cyclic constitutions, where the
cyclic relabelling of kinds is an automorphism) is Phi^p(X) = rot_r(tau^j(X)).

Run `python3 xring.py` for the self-test battery.
"""
from __future__ import annotations

import itertools
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OFF = (-1, 0, 1)
RULES27 = [(a, b, c) for a in OFF for b in OFF for c in OFF]
# Lemma 0' of rings/RESULTS.md: 15 of the 27 kinds are unconditional dead
# letters (b == 0 -> vacancy guard reads its own occupied cell; a == b ->
# "occupied and empty").  The 12 live kinds:
RULES12 = [r for r in RULES27 if r[1] != 0 and r[0] != r[1]]
assert len(RULES12) == 12


def is_dead_letter(r):
    return r[1] == 0 or r[0] == r[1]


# --------------------------------------------------------------------- engine

class Ring:
    """A cross-amendment constitution on Z/m, compiled for bitmask stepping."""

    __slots__ = ("rules", "targets", "m", "mask", "n", "mode", "_src")

    def __init__(self, rules, targets=None, m=6, mode="parity"):
        self.rules = [tuple(r) for r in rules]
        self.n = len(self.rules)
        self.targets = list(range(self.n)) if targets is None else list(targets)
        self.m = m
        self.mask = (1 << m) - 1
        self.mode = mode
        # sources[t] = kinds amending t
        self._src = [[k for k in range(self.n) if self.targets[k] == t]
                     for t in range(self.n)]

    # rot_r(x)[i] = x[i-r]
    def rot(self, x, r):
        m = self.m
        r %= m
        return ((x << r) | (x >> (m - r))) & self.mask if r else x

    def occ(self, X):
        o = 0
        for x in X:
            o |= x
        return o

    def active(self, X):
        """Bitmask of active laws, per kind."""
        O = self.occ(X)
        out = []
        for k in range(self.n):
            a, b, _ = self.rules[k]
            out.append(X[k] & self.rot(O, -a) & ~self.rot(O, -b) & self.mask)
        return out

    def step(self, X):
        mode = self.mode
        act = self.active(X)
        emit = [self.rot(act[k], self.rules[k][2]) for k in range(self.n)]
        if mode in ("super", "super_or"):
            O = self.occ(X)
            if mode == "super":
                cleared = 0
                for e in emit:
                    cleared ^= e
                cleared &= O
            else:
                cleared = 0
                for e in emit:
                    cleared |= e
                cleared &= O
            out = []
            for k in range(self.n):
                out.append((X[k] & ~cleared & self.mask) | (emit[k] & ~O
                                                            & self.mask))
            return tuple(out)
        out = list(X)
        for t in range(self.n):
            acc = 0
            if mode == "parity":
                for k in self._src[t]:
                    acc ^= emit[k]
            else:                                   # 'or'
                for k in self._src[t]:
                    acc |= emit[k]
            out[t] ^= acc
        return tuple(out)

    # ---------------------------------------------------------- presentation
    def rot_state(self, X, r):
        return tuple(self.rot(x, r) for x in X)

    def card(self, X):
        return sum(bin(x).count("1") for x in X)

    def render(self, X, sym="XYZWVU"):
        cells = []
        for i in range(self.m):
            ks = [k for k in range(self.n) if (X[k] >> i) & 1]
            if not ks:
                cells.append(".")
            elif len(ks) > 1:
                cells.append("#")
            else:
                cells.append(sym[ks[0]])
        return "|" + "".join(cells) + "|"

    def label(self):
        return " ".join("%d:(%d,%d,%d)->%d" % (k, *self.rules[k],
                                               self.targets[k])
                        for k in range(self.n))


# ------------------------------------------------------- orbit classification

def orbit(R, X0, max_steps=100000):
    """Return (transient t0, period p, states-on-cycle list)."""
    seen = {}
    X = X0
    for t in range(max_steps):
        if X in seen:
            t0 = seen[X]
            p = t - t0
            cyc = []
            Y = X
            for _ in range(p):
                cyc.append(Y)
                Y = R.step(Y)
            return t0, p, cyc
        seen[X] = t
        X = R.step(X)
    raise RuntimeError("no recurrence in %d steps" % max_steps)


def rotor_data(R, X):
    """If X is on a cycle, return (p, r) minimal with Phi^p(X) = rot_r(X),
    r != 0; else None.  X must be recurrent."""
    m = R.m
    rots = {}
    for r in range(m):
        rots[R.rot_state(X, r)] = r
    Y = X
    p = 0
    while True:
        Y = R.step(Y)
        p += 1
        if Y in rots:
            r = rots[Y]
            return None if r == 0 else (p, r)
        if p > 4 * m * m + 4096:
            return None


def verify_rotor(R, X, p, r, reps=3):
    """Independent re-verification over `reps` full periods (fresh code path:
    uses the reference dict-based xnomos engine, not the bitmask engine)."""
    import xnomos
    C = xnomos.Const(R.rules, R.targets, dim=1, modulus=R.m)
    S = {}
    for k in range(R.n):
        for i in range(R.m):
            if (X[k] >> i) & 1:
                S[i] = S.get(i, 0) | (1 << k)
    T = dict(S)
    for rep in range(1, reps + 1):
        for _ in range(p):
            T = xnomos.step(T, C, R.mode)
        want = {}
        for cell, msk in S.items():
            want[(cell + r * rep) % R.m] = msk
        if T != want:
            return False
    return True


def verify_balanced(R, X):
    """Fixed point with at least one active law."""
    if R.step(X) != X:
        return False
    return any(R.active(X))


# ------------------------------------------------------------- state encoding

def encode(X, m):
    v = 0
    for k, x in enumerate(X):
        v |= x << (k * m)
    return v


def decode(v, n, m):
    msk = (1 << m) - 1
    return tuple((v >> (k * m)) & msk for k in range(n))


# ------------------------------------------------------------------ self-test

def test_engine(trials=4000, seed=20260826):
    """Lockstep equality with the reference xnomos.py engine, all four modes."""
    import random
    import xnomos
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        n = rng.randrange(1, 4)
        m = rng.randrange(3, 12)
        rules = [rng.choice(RULES27) for _ in range(n)]
        if rng.random() < 0.5:                       # permutation target
            perm = list(range(n))
            rng.shuffle(perm)
            targets = perm
        else:                                        # arbitrary (may be non-inj)
            targets = [rng.randrange(n) for _ in range(n)]
        mode = rng.choice(["parity", "or", "super", "super_or"])
        X = tuple(rng.getrandbits(m) for _ in range(n))
        R = Ring(rules, targets, m, mode)
        C = xnomos.Const(rules, targets, dim=1, modulus=m)
        S = {}
        for k in range(n):
            for i in range(m):
                if (X[k] >> i) & 1:
                    S[i] = S.get(i, 0) | (1 << k)
        for _ in range(6):
            X = R.step(X)
            S = xnomos.step(S, C, mode)
            S2 = {}
            for k in range(n):
                for i in range(m):
                    if (X[k] >> i) & 1:
                        S2[i] = S2.get(i, 0) | (1 << k)
            if S2 != S:
                bad += 1
                print("MISMATCH", rules, targets, m, mode)
                break
    return bad


def _tests():
    ok = 0
    bad = test_engine()
    assert bad == 0, bad
    print("  [1] bitmask engine == xnomos reference: 4000 random configs x 6 "
          "steps, 4 modes, 0 mismatches")
    ok += 1

    # the known own-kind Z/6 rotor: kind (0,1,-1) at {1,2,5}, hop 3
    R = Ring([(0, 1, -1)], [0], 6)
    X = (0b100110,)                                 # cells 1,2,5
    assert R.step(X) == R.rot_state(X, 3), (bin(R.step(X)[0]),)
    assert rotor_data(R, X) == (1, 3)
    assert verify_rotor(R, X, 1, 3)
    print("  [2] Z/6 own-kind rotor reproduced and re-verified by xnomos path")
    ok += 1

    # Single-Author: permutation targets => parity == OR, on rings
    import random
    rng = random.Random(11)
    for _ in range(2000):
        n = rng.randrange(1, 4)
        m = rng.randrange(3, 13)
        rules = [rng.choice(RULES27) for _ in range(n)]
        perm = list(range(n))
        rng.shuffle(perm)
        X = tuple(rng.getrandbits(m) for _ in range(n))
        A = Ring(rules, perm, m, "parity")
        B = Ring(rules, perm, m, "or")
        for _ in range(8):
            assert A.step(X) == B.step(X)
            X = A.step(X)
    print("  [3] permutation targeting: parity == OR on 2000x8 random ring "
          "states (Single-Author survives on Z/m)")
    ok += 1

    # dead-letter classification
    for r in RULES27:
        R = Ring([r], [0], 7)
        dead = all(not R.active((x,))[0] for x in range(128))
        assert dead == is_dead_letter(r), r
    print("  [4] dead-letter classification verified by exhaustion on Z/7 "
          "(all 27 kinds x all 128 states)")
    ok += 1

    print("xring self-tests passed: %d/4" % ok)


if __name__ == "__main__":
    _tests()
