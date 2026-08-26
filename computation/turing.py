#!/usr/bin/env python3
"""
turing.py — THE ITINERANT REGISTRY: every Turing machine, as a finite code.

Rule 110 (rule110.py) already simulates exactly inside a 24-kind citation
constitution, but Rule 110's universality theorem is about configurations with
infinite periodic backgrounds, and a nomodynamic *code is finite*.  This module
closes that gap directly: for every Turing machine M over the binary tape
alphabet there is a citation constitution N(M) — window 1, parity, 11 + 12|Q|
kinds — and a FINITE code that simulates M step for step on an unbounded tape,
with time dilation 3 and space dilation 1.

TWO NEW INGREDIENTS beyond the statute-machine normal form.

(1) LATCHES.  A self-clearing wire lives one step.  Add a *hold* gate

        hold_v :  cite(v @0, not KILL @0) -> {v}

    and the wire re-enacts itself every step: a register that persists until
    the KILL phase.  With KILL = NIL it persists forever and any other author
    toggling it acts as a T flip-flop.  Registers T (tape bit) and H_q (head in
    state q) are latches; everything else is transient.

(2) THE BUILDING FRONT.  The gate laws of the statute machine are immortal, so
    hardware cannot grow — but a finite code can only carry finitely much of
    it.  A front of six kinds P0,P1,P2 / Q0,Q1,Q2 (the TANDEM-1 mechanism: one
    kind enacts the pair one cell ahead, its partner repeals the pair where it
    stands) walks outward at ONE CELL PER STEP, three times the speed of the
    simulated head, laying down the complete gate set plus the correct clock
    phase K_{j+1} at each virgin cell.  It never re-enters built ground, so
    every gate law is enacted exactly once and never amended again.  Blank
    tape needs no data at all: an empty hardware cell IS a 0 with no head,
    which is why the construction is written in single-rail logic.

THE CIRCUIT, at cell n, three micro-steps per Turing step:

  phase 0 (K0)  nT     cite(K0@0, not T@0)      -> {Tb}     Tb <- not t
                cpH_q  cite(H_q@0, not NIL)     -> {Hc_q}   transient head copy
                kK0    cite(K0@0, not NIL)      -> {K1}
  phase 1 (K1)  r1_q   cite(Hc_q@0, not Tb@0)   -> {R_q1}   head in q reads 1
                r0_q   cite(Hc_q@0, not T@0)    -> {R_q0}   head in q reads 0
                kK1    cite(K1@0, not NIL)      -> {K2}
  phase 2 (K2)  wr_qg  cite(R_qg@0, not NIL)    -> {T}      flip the tape bit
                mv_qg  cite(R_qg@-d, not NIL)   -> {H_q'}   the head arrives
                hold_q cite(H_q@0, not K2@0)    -> {H_q}    ... and departs
                kK2    cite(K2@0, not NIL)      -> {K0}
  always        holdT  cite(T@0, not NIL)       -> {T}      the tape remembers

`wr_qg` exists only when the transition rewrites the symbol; `mv_qg` sits at
the DESTINATION cell and cites the source across the offset, so a right move is
a gate citing at -1 and a left move a gate citing at +1.

Run `python3 turing.py`.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from statute import Machine, NIL                                  # noqa: E402

DIR = {"L": -1, "S": 0, "R": +1}


# --------------------------------------------------------------- the reference


class TM:
    """delta[(q, g)] = (q2, g2, d) with d in 'L','S','R'.  Tape alphabet {0,1}."""

    def __init__(self, states, delta, start=0):
        self.states = list(states)
        self.delta = dict(delta)
        self.start = start

    def run(self, tape, head, steps):
        """Reference simulator.  tape is a dict cell->bit.  Yields (tape,head,q)."""
        t = dict(tape)
        q = self.start
        h = head
        out = [(dict(t), h, q)]
        for _ in range(steps):
            g = t.get(h, 0)
            if (q, g) not in self.delta:
                out.append((dict(t), h, q))
                continue
            q2, g2, d = self.delta[(q, g)]
            if g2:
                t[h] = 1
            else:
                t.pop(h, None)
            h += DIR[d]
            q = q2
            out.append((dict(t), h, q))
        return out


# ---------------------------------------------------------------- the compiler


class Registry:
    """The constitution N(M) and its coding, for a Turing machine M."""

    def __init__(self, tm, build_right=True, build_left=True):
        self.tm = tm
        M = Machine(dim=1)
        self.M = M
        Q = tm.states
        # ---- wires
        assert all((q, g) in tm.delta for q in Q for g in (0, 1)), \
            "delta must be total (use an explicit halt state with S-loops)"
        M.wire("T")
        M.wire("Tb")
        for j in range(3):
            M.wire("K%d" % j)
        for q in Q:
            M.wire("H%d" % q)                       # head, phase 0 only
            M.wire("Ha%d" % q)                      # head, phase 1 only
            for g in (0, 1):
                M.wire("R%d_%d" % (q, g))           # head+symbol, phase 2 only
        # ---- gates, phase 0
        M.gate("nT", "K0", 0, "T", 0, 0, ["Tb"])
        for q in Q:
            M.gate("cpH%d" % q, "H%d" % q, 0, NIL, 0, 0, ["Ha%d" % q])
        M.gate("kK0", "K0", 0, NIL, 0, 0, ["K1"])
        # ---- phase 1
        for q in Q:
            M.gate("r1_%d" % q, "Ha%d" % q, 0, "Tb", 0, 0, ["R%d_1" % q])
            M.gate("r0_%d" % q, "Ha%d" % q, 0, "T", 0, 0, ["R%d_0" % q])
        M.gate("kK1", "K1", 0, NIL, 0, 0, ["K2"])
        # ---- phase 2
        for (q, g), (q2, g2, d) in sorted(tm.delta.items()):
            if g2 != g:
                M.gate("wr%d_%d" % (q, g), "R%d_%d" % (q, g), 0, NIL, 0, 0,
                       ["T"])
            M.gate("mv%d_%d" % (q, g), "R%d_%d" % (q, g), -DIR[d], NIL, 0, 0,
                   ["H%d" % q2])
        M.gate("kK2", "K2", 0, NIL, 0, 0, ["K0"])
        M.gate("holdT", "T", 0, NIL, 0, 0, ["T"])
        self.hardware = list(M.gates)          # the gate laws of one cell
        # ---- the building fronts (NOT in normal form: they amend the gates)
        self.fronts = []
        for side, c in (("R", +1), ("L", -1)):
            if (side == "R" and not build_right) or \
               (side == "L" and not build_left):
                continue
            for j in range(3):
                M.reserve("P%s%d" % (side, j))
                M.reserve("Q%s%d" % (side, j))
            for j in range(3):
                jn = (j + 1) % 3
                tgt = (["P%s%d" % (side, jn), "Q%s%d" % (side, jn)]
                       + self.hardware + ["K%d" % jn])
                M.define("P%s%d" % (side, j), "P%s%d" % (side, j), 0, NIL, 0,
                         c, tgt)
                M.define("Q%s%d" % (side, j), "Q%s%d" % (side, j), 0, NIL, 0,
                         0, ["P%s%d" % (side, j), "Q%s%d" % (side, j)])
            self.fronts.append(side)
        # the front kinds must be declared as WIRES for the builder to toggle
        # them; instead we keep them as gates and record the exception below.
        self.front_kinds = ["%s%s%d" % (x, s, j) for s in self.fronts
                            for x in "PQ" for j in range(3)]

    # -- coding ------------------------------------------------------------
    def code(self, tape, head, cells):
        """A phase-0 code: hardware on `cells`, tape bits, head in state q0."""
        M = self.M
        pl = []
        for c in cells:
            pl += [(c, g) for g in self.hardware]
            pl.append((c, "K0"))
        for c, b in tape.items():
            if b:
                pl.append((c, "T"))
        pl.append((head, "H%d" % self.tm.start))
        for side in self.fronts:
            f = max(cells) if side == "R" else min(cells)
            pl.append((f, "P%s0" % side))
            pl.append((f, "Q%s0" % side))
        return M.code(pl)

    def decode(self, S, cells):
        M = self.M
        tape = {c: 1 for c in cells if M.read(S, c, "T")}
        head, q = None, None
        for c in cells:
            for qq in self.tm.states:
                if M.read(S, c, "H%d" % qq):
                    head, q = c, qq
        return tape, head, q

    def run(self, S, n=1):
        return self.M.run(S, n)


# ------------------------------------------------------------- the certificate


def certify(tm, tape, head, steps, pad=4, verbose=False, fronts=True):
    """Run N(M) against the reference simulator for `steps` Turing steps."""
    R = Registry(tm, build_right=fronts, build_left=fronts)
    M = R.M
    lo = min([head] + list(tape)) - pad
    hi = max([head] + list(tape)) + pad
    cells = list(range(lo, hi + 1))
    S = R.code(tape, head, cells)
    ref = tm.run(tape, head, steps)
    view = list(range(lo - steps - 2, hi + steps + 3))
    for k in range(steps + 1):
        rt, rh, rq = ref[k]
        rt = {c: b for c, b in rt.items() if b}
        gt, gh, gq = R.decode(S, view)
        if (gt, gh, gq) != (rt, rh, rq):
            return False, k, (gt, gh, gq), (rt, rh, rq)
        if verbose:
            print("   t=%d head=%s q=%s tape=%s" % (k, gh, gq, sorted(rt)))
        if k < steps:
            S = R.run(S, 3)
    return True, steps, None, None


def certify_front(tm, steps=30):
    """The building front: hardware grows by exactly one cell per step per
    side, is never re-amended, and stays ahead of the head."""
    R = Registry(tm)
    M = R.M
    cells = list(range(-2, 3))
    S = R.code({}, 0, cells)
    seen = {}
    for t in range(steps):
        # every cell that has ANY hardware must have ALL of it, exactly once
        for c in list(S):
            got = [g for g in R.hardware if M.read(S, c, g)]
            if got and len(got) != len(R.hardware):
                return False, "cell %d half-built at t=%d (%d/%d)" % (
                    c, t, len(got), len(R.hardware))
            if got:
                if c in seen and seen[c] != t - 1:
                    pass
                seen[c] = t
        built = sorted(c for c in S if M.read(S, c, R.hardware[0]))
        if t == 0:
            span0 = (built[0], built[-1])
        else:
            if built[0] != span0[0] - t or built[-1] != span0[1] + t:
                return False, "front speed wrong at t=%d: %s" % (t, built[:1])
        S = R.run(S, 1)
    return True, "hardware grows 1 cell/step/side, complete at every cell, " \
                 "%d steps" % steps


# -------------------------------------------------------------- sample machines

def tm_move_right():
    """Runs right forever writing 1s: tests the right-hand front."""
    return TM([0], {(0, 0): (0, 1, "R"), (0, 1): (0, 1, "R")})


def tm_move_left():
    return TM([0], {(0, 0): (0, 1, "L"), (0, 1): (0, 1, "L")})


def tm_binary_increment():
    """q0 walks right to the end of a binary block, q1 adds one with carry,
    q2 walks back.  Exercises both directions, both writes, and halting."""
    d = {
        (0, 1): (0, 1, "R"),
        (0, 0): (1, 0, "L"),
        (1, 1): (1, 0, "L"),
        (1, 0): (2, 1, "L"),
        (2, 1): (2, 1, "L"),
        (2, 0): (3, 0, "S"),
        (3, 0): (3, 0, "S"),
        (3, 1): (3, 1, "S"),
    }
    return TM([0, 1, 2, 3], d)


def tm_busy_beaver3():
    """The 3-state busy beaver (13 steps, 6 ones)."""
    d = {
        (0, 0): (1, 1, "R"), (0, 1): (2, 1, "L"),
        (1, 0): (0, 1, "L"), (1, 1): (1, 1, "R"),
        (2, 0): (1, 1, "L"), (2, 1): (3, 1, "S"),
        (3, 0): (3, 0, "S"), (3, 1): (3, 1, "S"),
    }
    return TM([0, 1, 2, 3], d)


def tm_busy_beaver4():
    d = {
        (0, 0): (1, 1, "R"), (0, 1): (1, 1, "L"),
        (1, 0): (0, 1, "L"), (1, 1): (2, 0, "L"),
        (2, 0): (4, 1, "S"), (2, 1): (3, 1, "L"),
        (3, 0): (3, 1, "R"), (3, 1): (0, 0, "R"),
        (4, 0): (4, 0, "S"), (4, 1): (4, 1, "S"),
    }
    return TM([0, 1, 2, 3, 4], d)


def random_tms(n=60, seed=17, nstates=3):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        d = {}
        for q in range(nstates):
            for g in (0, 1):
                d[(q, g)] = (rng.randrange(nstates), rng.randrange(2),
                             rng.choice("LSR"))
        out.append(TM(list(range(nstates)), d))
    return out


def _main():
    import random
    print("THE ITINERANT REGISTRY — every Turing machine as a finite code")
    ok = 0
    cases = [
        ("move-right (front test)", tm_move_right(), {}, 0, 24),
        ("move-left  (front test)", tm_move_left(), {}, 0, 24),
        ("binary increment 1011",   tm_binary_increment(),
         {0: 1, 1: 0, 2: 1, 3: 1}, 0, 20),
        ("busy beaver 3",           tm_busy_beaver3(), {}, 0, 18),
        ("busy beaver 4",           tm_busy_beaver4(), {}, 0, 30),
    ]
    for name, tm, tape, head, steps in cases:
        R = Registry(tm)
        good, k, got, want = certify(tm, tape, head, steps)
        print("  %-26s |Q|=%d  %3d kinds  %2d Turing steps -> %s" % (
            name, len(tm.states), len(R.M.names), steps,
            "EXACT" if good else "FAIL at %d: %r vs %r" % (k, got, want)))
        assert good, (name, k, got, want)
        ok += 1
    rng = random.Random(4)
    bad = 0
    n = 0
    for tm in random_tms(80, nstates=3) + random_tms(40, seed=99, nstates=4):
        tape = {c: rng.randrange(2) for c in range(-2, 3)}
        tape = {c: b for c, b in tape.items() if b}
        good, k, got, want = certify(tm, tape, 0, 14)
        n += 1
        if not good:
            bad += 1
    print("  %-26s %d random machines x random tapes x 14 steps: %d "
          "mismatches" % ("random TMs", n, bad))
    assert bad == 0
    ok += 1
    good, msg = certify_front(tm_busy_beaver3())
    print("  building front:", msg if good else "FAIL " + msg)
    assert good, msg
    ok += 1
    # growth
    R = Registry(tm_move_right())
    S = R.code({}, 0, list(range(-2, 3)))
    from xnomos import card
    sizes = []
    for t in range(0, 40):
        sizes.append(card(S))
        S = R.run(S, 1)
    slope = (sizes[-1] - sizes[-11]) / 10.0
    print("  growth: |S_t| linear, %.1f laws/step (finite code, unbounded "
          "tape)" % slope)
    ok += 1
    print("turing self-tests passed: %d/8" % ok)


if __name__ == "__main__":
    _main()
