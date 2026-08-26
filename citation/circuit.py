#!/usr/bin/env python3
"""
circuit.py — chapter three's computational substrate (prediction Y3).

THE MECHANISM.  A citation guard is literally

        (a law of kind g stands at i+a)  AND NOT  (a law of kind h stands at i+b)

— an AND-NOT of two kind-fields at fixed offsets — and parity resolution adds
the toggles of all authors of a slot, i.e. XORs them.  So one nomodynamics step
applies, to every target field, an arbitrary XOR of AND-NOT terms over the
neighbourhood.  {AND-NOT, XOR, 1} is functionally complete, so with one scratch
field and two steps every Boolean local rule is realisable.

Two devices make it work, and neither exists under occupancy guards:

  * THE PHANTOM.  Let phi be a kind that is never enacted.  Then "no law of kind
    phi stands at i+b" is vacuously true, so the vacancy clause is free.  Under
    occupancy guards a law standing in a solid region is ALWAYS blocked, which
    is exactly chapter one's Gridlock.
  * THE SELF-CITING CLOCK.  g_k = k with a_k = 0 is a tautology (the law stands
    at its own cell), so a law can be unconditionally active.  One such law per
    cell, targeting the whole gate alphabet, gives a two-phase clock at every
    cell for the price of a single kind.

ARCHITECTURE (compile_eca).  Kinds split into
    DATA    S (state), U (scratch)            — guard (phi, phi): never active
    CLOCK   CK                                — unconditionally active
    GATES   one kind per distinct (a,b,c,g,h) — toggled on and off by CK, so a
                                                gate kind is PLACED only in its
                                                own phase, which frees both
                                                guard clauses for data literals
    PHANTOM phi                               — never placed

Phase 1: U(i) ^= S(i-1)S(i).      Phase 2: S(i) ^= f(S(i-1),S(i),S(i+1)) ^ S(i)
                                             and U(i) ^= S(i-1)S(i)  (clears U).
Two nomodynamics steps = one CA step.

    python3 circuit.py        # gate inventory + all 256 elementary rules
"""

from __future__ import annotations

import itertools
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cite as ct                                              # noqa: E402


# --------------------------------------------------------------- ANF of a rule

def anf(rule):
    """Algebraic normal form of an elementary CA rule, over (x,y,z)=(l,c,r).

    Returns a dict monomial(frozenset of 'x','y','z') -> coefficient in F2.
    rule bit for (x,y,z) is (rule >> (4x+2y+z)) & 1.
    """
    f = {}
    for x, y, z in itertools.product((0, 1), repeat=3):
        f[(x, y, z)] = (rule >> (4 * x + 2 * y + z)) & 1
    coef = {}
    for mx, my, mz in itertools.product((0, 1), repeat=3):
        # Moebius transform: coefficient of monomial m is XOR of f over
        # all points below m.
        s = 0
        for x, y, z in itertools.product((0, 1), repeat=3):
            if x <= mx and y <= my and z <= mz:
                s ^= f[(x, y, z)]
        if s:
            coef[(mx, my, mz)] = 1
    return coef


# ---------------------------------------------------------------- the compiler

class ECA:
    """A compiled elementary-CA simulator as a citation constitution."""

    def __init__(self, rule):
        self.rule = rule
        self.coef = anf(rule)
        # kind indices
        self.PHI, self.S, self.U, self.CK = 0, 1, 2, 3
        self.rules = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.targets = [(), (), (), ()]
        self.guards = [(0, 0), (0, 0), (0, 0), (3, 0)]
        # data kinds cite the phantom as PRECEDENT: never active.
        # CK cites itself at offset 0 (tautology) and the phantom (tautology).
        self.gate = {}            # (phase, a, b, c, g, h) -> kind index
        self.phase_kinds = {1: [], 2: []}
        self._build()
        self.C = ct.Cit(self.rules, self.targets, self.guards)
        # CK targets every gate kind at its own cell
        self.targets[self.CK] = tuple(sorted(self.phase_kinds[1]
                                             + self.phase_kinds[2]))
        self.C = ct.Cit(self.rules, self.targets, self.guards)

    # -- gate allocation ---------------------------------------------------
    def _emit(self, phase, a, b, g, h, target):
        """XOR `target` into the gate (phase; reads g at +a, not h at +b; c=0).

        XOR, not union: a monomial requested twice must CANCEL, because one
        kind can stand at a cell at most once and therefore contributes at
        most one toggle.
        """
        key = (phase, a, b, 0, g, h)
        if key not in self.gate:
            k = len(self.rules)
            self.gate[key] = k
            self.rules.append((a, b, 0))
            self.guards.append((g, h))
            self.targets.append(())
            self.phase_kinds[phase].append(k)
        k = self.gate[key]
        T = set(self.targets[k]) ^ {target}
        self.targets[k] = tuple(sorted(T))

    # -- the two phases ----------------------------------------------------
    def _prod_xy(self, phase, target):
        """target ^= S(i-1)*S(i)   as  x  XOR  (x AND NOT y)."""
        self._emit(phase, -1, 0, self.S, self.PHI, target)     # x
        self._emit(phase, -1, 0, self.S, self.S, target)       # x and not y

    def _build(self):
        S, U, PHI, CK = self.S, self.U, self.PHI, self.CK
        # phase 1: U ^= x*y
        self._prod_xy(1, U)
        # phase 2: U ^= x*y  (clears it), and S ^= Delta
        self._prod_xy(2, U)
        c = self.coef
        # Delta = f XOR y  -> flip the coefficient of the y monomial
        d = dict(c)
        d[(0, 1, 0)] = d.get((0, 1, 0), 0) ^ 1
        for m, v in list(d.items()):
            if not v:
                continue
            if m == (0, 0, 0):                      # constant 1
                self._emit(2, 0, 0, CK, PHI, S)
            elif m == (1, 0, 0):                    # x
                self._emit(2, -1, 0, S, PHI, S)
            elif m == (0, 1, 0):                    # y
                self._emit(2, 0, 0, S, PHI, S)
            elif m == (0, 0, 1):                    # z
                self._emit(2, 1, 0, S, PHI, S)
            elif m == (1, 1, 0):                    # x*y  = U
                self._emit(2, 0, 0, U, PHI, S)
            elif m == (1, 0, 1):                    # x*z  = x XOR (x & ~z)
                self._emit(2, -1, 0, S, PHI, S)
                self._emit(2, -1, 1, S, S, S)
            elif m == (0, 1, 1):                    # y*z  = y XOR (y & ~z)
                self._emit(2, 0, 0, S, PHI, S)
                self._emit(2, 0, 1, S, S, S)
            elif m == (1, 1, 1):                    # x*y*z = U XOR (U & ~z)
                self._emit(2, 0, 0, U, PHI, S)
                self._emit(2, 0, 1, U, S, S)

    # -- seeding and reading ----------------------------------------------
    def seed_ring(self, bits):
        """bits = list of 0/1 of length m.  Returns the ring state tuple."""
        m = len(bits)
        full = (1 << m) - 1
        mask = [0] * self.C.n
        mask[self.CK] = full
        for k in self.phase_kinds[1]:
            mask[k] = full
        for i, b in enumerate(bits):
            if b:
                mask[self.S] |= 1 << i
        return tuple(mask)

    def read_ring(self, mask, m):
        return [(mask[self.S] >> i) & 1 for i in range(m)]

    def seed_line(self, bits, lo=0):
        """Place the machine on a segment of Z.  Edge cells leak; the interior
        is exact while the boundary stays outside the light cone."""
        pairs = []
        for i in range(lo, lo + len(bits)):
            pairs.append((i, self.CK))
            for k in self.phase_kinds[1]:
                pairs.append((i, k))
        for j, b in enumerate(bits):
            if b:
                pairs.append((lo + j, self.S))
        return ct.state_fields(pairs, self.C.n)


def eca_step(bits, rule):
    m = len(bits)
    return [(rule >> (4 * bits[(i - 1) % m] + 2 * bits[i]
                      + bits[(i + 1) % m])) & 1 for i in range(m)]


# ------------------------------------------------------------ gate inventory

def gate_inventory():
    """One-step truth tables for NOT, AND, OR, XOR, AND-NOT and FAN-OUT.

    Inputs are kinds P and Q placed at cell 0; the gate law of kind G sits at
    cell 0 and writes the answer into an output kind at cell 0 (or into two
    kinds, for fan-out).  All eight/four input combinations are checked.
    """
    PHI, P, Q, R1, R2 = 0, 1, 2, 3, 4
    SELF = "SELF"                 # cite my own kind at offset 0: a tautology
    out = []

    def universe(gates):
        rules = [(0, 0, 0)] * 5
        guards = [(PHI, PHI)] * 5          # PHI precedent => data kinds inert
        targets = [()] * 5
        for (a, b, g, h, T) in gates:
            k = len(rules)
            rules.append((a, b, 0))
            guards.append((k if g is SELF else g, h))
            targets.append(tuple(sorted(T)))
        return ct.Cit(rules, targets, guards)

    def run(C, p, q):
        pairs = [(0, k) for k in range(5, C.n)]
        if p:
            pairs.append((0, P))
        if q:
            pairs.append((0, Q))
        F = ct.state_fields(pairs, C.n)
        G = ct.step_fields(F, C)
        bit = 1 << ct.BIAS
        return (1 if G[R1] & bit else 0, 1 if G[R2] & bit else 0)

    tests = [
        ("BUFFER  R1 = P", [(0, 0, P, PHI, {R1})], lambda p, q: p),
        ("NOT     R1 = ~P", [(0, 0, SELF, PHI, {R1}),         # constant 1
                             (0, 0, P, PHI, {R1})], lambda p, q: 1 ^ p),
        ("ANDNOT  R1 = P & ~Q", [(0, 0, P, Q, {R1})], lambda p, q: p & (1 ^ q)),
        ("AND     R1 = P & Q", [(0, 0, P, PHI, {R1}),
                                (0, 0, P, Q, {R1})], lambda p, q: p & q),
        ("XOR     R1 = P ^ Q", [(0, 0, P, PHI, {R1}),
                                (0, 0, Q, PHI, {R1})], lambda p, q: p ^ q),
        # P|Q = Q XOR (P AND NOT Q)
        ("OR      R1 = P | Q", [(0, 0, Q, PHI, {R1}),
                                (0, 0, P, Q, {R1})], lambda p, q: p | q),
        ("FANOUT  R1 = R2 = P", [(0, 0, P, PHI, {R1, R2})],
         lambda p, q: p),
    ]
    ok = 0
    for name, gates, want in tests:
        C = universe(gates)
        good = True
        rows = []
        for p, q in itertools.product((0, 1), repeat=2):
            r1, r2 = run(C, p, q)
            w = want(p, q)
            exp2 = w if name.startswith("FANOUT") else 0
            good &= (r1 == w and r2 == exp2)
            rows.append("%d%d->%d" % (p, q, r1))
        out.append((name, good, " ".join(rows)))
        ok += good
    return out, ok, len(tests)


# ---------------------------------------------------------------- verification

def verify_all_eca(m=13, steps=24, trials=4, seed=1, verbose=False):
    rng = random.Random(seed)
    bad = []
    for rule in range(256):
        M = ECA(rule)
        for _ in range(trials):
            bits = [rng.randrange(2) for _ in range(m)]
            ref = list(bits)
            st = M.seed_ring(bits)
            for t in range(steps):
                st = ct.step_ring(st, M.C, m)
                st = ct.step_ring(st, M.C, m)
                ref = eca_step(ref, rule)
                if M.read_ring(st, m) != ref:
                    bad.append((rule, t))
                    break
            else:
                continue
            break
    return bad


def kind_counts():
    return {r: ECA(r).C.n for r in range(256)}


if __name__ == "__main__":
    print("=== GATE INVENTORY (one nomodynamics step, parity resolution) ===")
    rows, ok, tot = gate_inventory()
    for name, good, tt in rows:
        print("  %-22s %s   %s" % (name, "OK " if good else "FAIL", tt))
    print("  %d/%d gates verified" % (ok, tot))

    print("\n=== ELEMENTARY CA SIMULATION ===")
    kc = kind_counts()
    print("  kinds needed: min %d, max %d, mean %.1f"
          % (min(kc.values()), max(kc.values()),
             sum(kc.values()) / 256.0))
    bad = verify_all_eca()
    print("  all 256 elementary rules, ring m=13, 24 CA steps, 4 random "
          "seeds each: %s" % ("ALL EXACT" if not bad else "MISMATCH %s" % bad))
    M = ECA(110)
    print("\n  Rule 110 constitution: %d kinds" % M.C.n)
    print("  " + M.C.label().replace(" | ", "\n  "))
