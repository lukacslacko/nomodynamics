#!/usr/bin/env python3
"""
rule110.py — THE STATUTE OF ONE HUNDRED AND TEN.

A single citation constitution on Z, window 1, parity resolution, 24 kinds,
that simulates elementary cellular automaton Rule 110 exactly, with time
dilation 3 and space dilation 1 (one Rule-110 cell = one nomodynamics cell).

    Rule 110:   y_n = x_n XOR x_{n+1} XOR x_n x_{n+1} XOR x_{n-1} x_n x_{n+1}

THE CIRCUIT (all wires and all gate laws live at the cell they belong to; the
gate laws are IMMORTAL — no kind's target set contains them — so the hardware
is a permanent statute book and only the data moves).

  wires   X  Xb        the cell's bit and its complement          (phase 0)
          A  Ab        A = x_n & x_{n+1}, and its complement      (phase 1)
          X1           x_n delayed one step                       (phase 1)
          X2  A2  B    x_n, A, and B = x_{n-1} & A                (phase 2)
          K0 K1 K2     the three-phase clock, present at every hardware cell

  phase 0   gA   cite(X @0, not Xb @+1) -> {A, Ab}      A  <- x_n & x_{n+1}
            gX1  cite(X @0, not NIL)    -> {X1}         X1 <- x_n
            kK0  cite(K0@0, not NIL)    -> {K1, Ab}     clock, and the 1 that
                                                        turns A into ~A
  phase 1   gB   cite(X1@-1, not Ab @0) -> {B}          B  <- x_{n-1} & A
            gX2  cite(X1@0, not NIL)    -> {X2}
            gA2  cite(A @0, not NIL)    -> {A2}
            kK1  cite(K1@0, not NIL)    -> {K2}
  phase 2   gY0  cite(X2@0,  not NIL)   -> {X, Xb}      the four terms of the
            gY1  cite(X2@+1, not NIL)   -> {X, Xb}      Rule-110 polynomial,
            gY2  cite(A2@0,  not NIL)   -> {X, Xb}      XOR-merged into X
            gY3  cite(B @0,  not NIL)   -> {X, Xb}
            kK2  cite(K2@0,  not NIL)   -> {K0, Xb}     clock, and the 1 that
                                                        turns X into ~X in Xb

Every gate is self-timed: its input wire is present only in its own phase, so
the three stages fire in sequence with no external clocking beyond K0/K1/K2.

THE CERTIFICATE.  Every offset lies in {-1,0,+1}, so one nomodynamics step
moves information at most one cell and three steps have radius <= 3.  The
3-step map is therefore a local map f : {0,1}^7 -> {0,1}.  Running all 2^7 = 128
configurations of the ring Z/7 evaluates f at every one of its inputs, so
agreement there is agreement on Z for EVERY configuration, finite or not.
That check is `certify_local()` and it is a complete enumeration.

Run `python3 rule110.py`.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from statute import Machine, NIL                                  # noqa: E402


# ------------------------------------------------------------ the constitution


def build(modulus=None):
    M = Machine(dim=1, modulus=modulus)
    for w in ("X", "Xb", "A", "Ab", "X1", "X2", "A2", "B", "K0", "K1", "K2"):
        M.wire(w)
    # phase 0
    M.gate("gA",  "X",  0, "Xb", +1, 0, ["A", "Ab"])
    M.gate("gX1", "X",  0, NIL,   0, 0, ["X1"])
    M.gate("kK0", "K0", 0, NIL,   0, 0, ["K1", "Ab"])
    # phase 1
    M.gate("gB",  "X1", -1, "Ab", 0, 0, ["B"])
    M.gate("gX2", "X1", 0, NIL,   0, 0, ["X2"])
    M.gate("gA2", "A",  0, NIL,   0, 0, ["A2"])
    M.gate("kK1", "K1", 0, NIL,   0, 0, ["K2"])
    # phase 2
    M.gate("gY0", "X2", 0,  NIL, 0, 0, ["X", "Xb"])
    M.gate("gY1", "X2", +1, NIL, 0, 0, ["X", "Xb"])
    M.gate("gY2", "A2", 0,  NIL, 0, 0, ["X", "Xb"])
    M.gate("gY3", "B",  0,  NIL, 0, 0, ["X", "Xb"])
    M.gate("kK2", "K2", 0,  NIL, 0, 0, ["K0", "Xb"])
    return M


GATES = build().gates


def encode(M, bits, cells=None):
    """A phase-0 code for the configuration `bits` on `cells`."""
    if cells is None:
        cells = list(range(len(bits)))
    pl = []
    for c in cells:
        pl += [(c, g) for g in GATES]
        pl.append((c, "K0"))
    for c, b in zip(cells, bits):
        pl.append((c, "X" if b else "Xb"))
    return M.code(pl)


def decode(M, S, cells):
    return [M.read(S, c, "X") for c in cells]


# ------------------------------------------------------- independent reference


def rule110_step(bits, ring=True, left=0, right=0):
    n = len(bits)
    out = []
    for i in range(n):
        p = bits[(i - 1) % n] if ring else (bits[i - 1] if i > 0 else left)
        q = bits[i]
        r = bits[(i + 1) % n] if ring else (bits[i + 1] if i < n - 1 else right)
        # the table, written out — NOT the polynomial the construction uses
        out.append({(1, 1, 1): 0, (1, 1, 0): 1, (1, 0, 1): 1, (1, 0, 0): 0,
                    (0, 1, 1): 1, (0, 1, 0): 1, (0, 0, 1): 1,
                    (0, 0, 0): 0}[(p, q, r)])
    return out


# ------------------------------------------------------------- the certificates


def max_offset(M):
    C = M.const()
    return max(max(abs(x) for x in r) for r in C.rules)


def certify_local(verbose=False):
    """COMPLETE: all 2^7 configurations of Z/7.  Decides Z entirely."""
    M = build(modulus=7)
    assert max_offset(M) == 1, max_offset(M)
    assert not M.check_normal_form(), M.check_normal_form()
    cells = list(range(7))
    bad = []
    for code in range(128):
        bits = [(code >> i) & 1 for i in range(7)]
        S = encode(M, bits, cells)
        T = M.run(S, 3)
        got = decode(M, T, cells)
        want = rule110_step(bits)
        if got != want:
            bad.append((bits, got, want))
        elif verbose:
            print("  ", bits, "->", got)
    return len(bad) == 0, bad, 128


def certify_ring(m, steps=24, exhaustive=True, samples=400, seed=5):
    """All 2^m configurations of Z/m (exhaustive) run for `steps` R110 steps."""
    import random
    rng = random.Random(seed)
    M = build(modulus=m)
    cells = list(range(m))
    src = (range(1 << m) if exhaustive
           else [rng.randrange(1 << m) for _ in range(samples)])
    n = 0
    for code in src:
        bits = [(code >> i) & 1 for i in range(m)]
        S = encode(M, bits, cells)
        ref = list(bits)
        for _ in range(steps):
            S = M.run(S, 3)
            ref = rule110_step(ref)
            if decode(M, S, cells) != ref:
                return False, n, (bits, code)
        n += 1
    return True, n, None


def certify_phase_purity(m=11, steps=30, seed=3):
    """At every t = 3k the code is EXACTLY a phase-0 code: K0 everywhere, one
    of X/Xb per cell, every other wire empty, and the 12 gate laws unmoved."""
    import random
    rng = random.Random(seed)
    M = build(modulus=m)
    cells = list(range(m))
    bits = [rng.randrange(2) for _ in cells]
    S = encode(M, bits, cells)
    G0 = {(c, g) for c in cells for g in GATES}
    for k in range(steps):
        for c in cells:
            assert M.read(S, c, "K0") == 1
            assert M.read(S, c, "X") ^ M.read(S, c, "Xb") == 1
            for w in ("A", "Ab", "X1", "X2", "A2", "B", "K1", "K2"):
                if M.read(S, c, w):
                    return False, "wire %s dirty at t=%d" % (w, 3 * k)
        got = {(c, g) for c in cells for g in GATES if M.read(S, c, g)}
        if got != G0:
            return False, "hardware moved at t=%d" % (3 * k)
        S = M.run(S, 3)
    return True, "%d phase-0 checkpoints clean" % steps


def certify_line(n=40, steps=12, seed=9):
    """On Z with hardware on [0,n-1]: the light cone.  After s Rule-110 steps
    the interior [s, n-1-s] must match Rule 110 with ANY boundary."""
    import random
    rng = random.Random(seed)
    M = build()
    cells = list(range(n))
    bits = [rng.randrange(2) for _ in cells]
    S = encode(M, bits, cells)
    ref = list(bits)
    for s in range(1, steps + 1):
        S = M.run(S, 3)
        ref = rule110_step(ref, ring=False, left=0, right=0)
        lo, hi = s, n - 1 - s
        if decode(M, S, cells)[lo:hi + 1] != ref[lo:hi + 1]:
            return False, s
    return True, steps


def spacetime110(bits, steps, ring=True):
    m = len(bits)
    M = build(modulus=m if ring else None)
    cells = list(range(m))
    S = encode(M, bits, cells)
    rows = []
    for _ in range(steps):
        rows.append("".join("#" if b else "." for b in decode(M, S, cells)))
        S = M.run(S, 3)
    return rows


def _main():
    M = build()
    print("THE STATUTE OF ONE HUNDRED AND TEN")
    print("  kinds: %d (1 NIL + %d wires + %d gate laws)   window: %d   "
          "resolution: parity" % (len(M.names), len(M.wires), len(M.gates),
                                  max_offset(M)))
    print("  normal-form audit:", M.check_normal_form() or "clean")
    print()
    ok, bad, n = certify_local()
    print("  COMPLETE local certificate: all %d configurations of Z/7 "
          "(= all inputs of the radius-3 local map)  -> %s" %
          (n, "EXACT" if ok else "FAIL %r" % (bad[:3],)))
    assert ok
    for m in (8, 9, 10, 11, 12):
        good, cnt, why = certify_ring(m, steps=16)
        print("  ring Z/%-2d : all %6d configurations x 16 Rule-110 steps "
              "-> %s" % (m, cnt, "EXACT" if good else "FAIL %r" % (why,)))
        assert good
    good, cnt, why = certify_ring(17, steps=60, exhaustive=False, samples=200)
    print("  ring Z/17 : %d random configurations x 60 Rule-110 steps -> %s"
          % (cnt, "EXACT" if good else "FAIL"))
    assert good
    good, msg = certify_phase_purity()
    print("  phase purity + hardware immortality:", msg, "->",
          "OK" if good else "FAIL")
    assert good
    good, s = certify_line()
    print("  on Z, hardware [0,39], light-cone interior, %d Rule-110 steps -> %s"
          % (s, "EXACT" if good else "FAIL"))
    assert good
    print()
    print("  a glider of Rule 110 inside the statute book (ring Z/28, ether):")
    ether = [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1] * 2
    for r in spacetime110(ether, 8):
        print("   ", r)


if __name__ == "__main__":
    _main()
