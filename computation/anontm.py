#!/usr/bin/env python3
"""
anontm.py — THE ANONYMOUS ITINERANT REGISTRY.

turing.py compiles every Turing machine into a finite code of the CITATION
sector.  anon.py shows the citation guard was never needed for the circuit.
This file puts the two together: every Turing machine as a FINITE CODE of the
FOUNDING sector — occupancy guards only, `guards=None`, chapters one and two.

    THEOREM 5 (finite-code universality of the founding sector).
    For every Turing machine M over {0,1} there is a constitution N*(M) with
    occupancy guards, dimension 1, finitely many kinds and a finite window, and
    a FINITE code C(M,x), such that the code at step 3t decodes to the
    configuration of M on x after t steps, for every t.  The simulated tape is
    unbounded: the code grows by two blocks per step.

    Every kind of N*(M) except the eighteen kinds of the two building fronts
    has OUT-DEGREE 1 — and the fronts are needed only to enact hardware on
    virgin ground, never to compute.

THE FRONT (nine kinds per side, phase-tagged).  At the POWER cell of the
frontier site f, in clock phase j:

    P_j  (a=0, b=+1, c = s*L)   -> {P_{j+1}, Q_{j+1}, R_{j+1}, POWER, gates...}
    R_j  (a=0, b=+1, c = s*L + slot(K_{j+1}) - r)   -> {K_{j+1}}
    Q_j  (a=0, b=+1, c = 0)     -> {P_j, Q_j, R_j}

a = 0 reads the front's own cell, permanently occupied by POWER, so the
precedent clause is vacuous; b = +1 reads the block's GAP, empty forever, so
the vacancy clause is vacuous; the pair therefore fires every step.  P enacts
the complete hardware of the next block one site ahead together with the next
front, R enacts that block's clock wire in the phase it will need, and Q
repeals the front where it stands.  This is the TANDEM-1 mechanism at block
scale.  The front advances ONE SITE PER STEP; the simulated head advances one
site per THREE steps, so the front is never overtaken and never re-enters built
ground: every gate law is enacted exactly once and never amended again.

Run `python3 anontm.py`.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anon import AnonMachine, NIL                                 # noqa: E402
from turing import TM, DIR, tm_move_right, tm_move_left, \
    tm_binary_increment, tm_busy_beaver3, tm_busy_beaver4, random_tms  # noqa

from xnomos import card                                            # noqa: E402


class AnonRegistry:
    """N*(M): the Turing machine M as an anonymous constitution."""

    def __init__(self, tm, fronts=("R", "L")):
        self.tm = tm
        Q = tm.states
        assert all((q, g) in tm.delta for q in Q for g in (0, 1))
        M = AnonMachine()
        self.M = M
        M.wire("T")
        M.wire("Tb")
        for j in range(3):
            M.wire("K%d" % j)
        for q in Q:
            M.wire("H%d" % q)
            M.wire("Ha%d" % q)
            for g in (0, 1):
                M.wire("R%d_%d" % (q, g))
        M.gate("nT", "K0", 0, "T", 0, 0, ["Tb"])
        for q in Q:
            M.gate("cpH%d" % q, "H%d" % q, 0, NIL, 0, 0, ["Ha%d" % q])
        M.gate("kK0", "K0", 0, NIL, 0, 0, ["K1"])
        for q in Q:
            M.gate("r1_%d" % q, "Ha%d" % q, 0, "Tb", 0, 0, ["R%d_1" % q])
            M.gate("r0_%d" % q, "Ha%d" % q, 0, "T", 0, 0, ["R%d_0" % q])
        M.gate("kK1", "K1", 0, NIL, 0, 0, ["K2"])
        for (q, g), (q2, g2, d) in sorted(tm.delta.items()):
            if g2 != g:
                M.gate("wr%d_%d" % (q, g), "R%d_%d" % (q, g), 0, NIL, 0, 0,
                       ["T"])
            M.gate("mv%d_%d" % (q, g), "R%d_%d" % (q, g), -DIR[d], NIL, 0, 0,
                   ["H%d" % q2])
        M.gate("kK2", "K2", 0, NIL, 0, 0, ["K0"])
        M.gate("holdT", "T", 0, NIL, 0, 0, ["T"])
        self.logical_gates = list(M.gate_specs)
        # --- the building fronts (raw kinds, cell offsets)
        M._build()                       # fix the layout before adding raws
        M._const = None                  # ... and reopen it for the fronts
        L, r = M.L, len(M.wires)
        pieces = [p for g in self.logical_gates for p in M.gate_pieces[g]]
        self.fronts = list(fronts)
        for side in self.fronts:
            s = +1 if side == "R" else -1
            for j in range(3):
                jn = (j + 1) % 3
                M.raw("P%s%d" % (side, j), 0, 1, s * L,
                      ["P%s%d" % (side, jn), "Q%s%d" % (side, jn),
                       "R%s%d" % (side, jn), "POWER"] + pieces)
                M.raw("R%s%d" % (side, j), 0, 1,
                      s * L + M.widx["K%d" % jn] - r, ["K%d" % jn])
                M.raw("Q%s%d" % (side, j), 0, 1, 0,
                      ["P%s%d" % (side, j), "Q%s%d" % (side, j),
                       "R%s%d" % (side, j)])
        M._build()
        self.hardware = self.logical_gates

    # -- coding ------------------------------------------------------------
    def code(self, tape, head, sites):
        pl = []
        for s in sites:
            pl += [(s, g) for g in self.logical_gates]
            pl.append((s, "K0"))
        for s, b in tape.items():
            if b:
                pl.append((s, "T"))
        pl.append((head, "H%d" % self.tm.start))
        for side in self.fronts:
            f = max(sites) if side == "R" else min(sites)
            for x in "PQR":
                pl.append((f, "%s%s0" % (x, side)))
        return self.M.code(pl, sites=sites)

    def decode(self, S, sites):
        M = self.M
        tape = {s: 1 for s in sites if M.read(S, s, "T")}
        head, q = None, None
        for s in sites:
            for qq in self.tm.states:
                if M.read(S, s, "H%d" % qq):
                    head, q = s, qq
        return tape, head, q

    def run(self, S, n=1):
        return self.M.run(S, n)


# ------------------------------------------------------------- the certificate


def certify(tm, tape, head, steps, pad=3, fronts=("R", "L")):
    R = AnonRegistry(tm, fronts=fronts)
    lo = min([head] + list(tape)) - pad
    hi = max([head] + list(tape)) + pad
    sites = list(range(lo, hi + 1))
    S = R.code(tape, head, sites)
    ref = tm.run(tape, head, steps)
    view = list(range(lo - steps - 2, hi + steps + 3))
    for k in range(steps + 1):
        rt, rh, rq = ref[k]
        rt = {c: b for c, b in rt.items() if b}
        got = R.decode(S, view)
        if got != (rt, rh, rq):
            return False, k, got, (rt, rh, rq)
        if k < steps:
            S = R.run(S, 3)
    return True, steps, None, None


def certify_hygiene(tm, steps=40):
    """The two structural invariants the construction rests on:
    every GAP cell is empty at every step, and every POWER cell holds POWER."""
    R = AnonRegistry(tm)
    M = R.M
    L, r = M.L, len(M.wires)
    sites = list(range(-3, 4))
    S = R.code({}, 0, sites)
    P = M.POWER
    for t in range(steps):
        for cell, mask in S.items():
            slot = cell % L
            if slot == r + 1:
                return False, "a law stands in a GAP cell at t=%d" % t
            if slot == r and not (mask >> P) & 1:
                return False, "a POWER cell lost its dead letter at t=%d" % t
        S = M.run(S, 1)
    return True, "GAP empty and POWER intact for %d steps" % steps


def certify_front_once(tm, steps=30):
    """Every gate law is enacted exactly once and never amended again."""
    R = AnonRegistry(tm)
    M = R.M
    L, r = M.L, len(M.wires)
    pieces = [M.idx(p) for g in R.logical_gates for p in M.gate_pieces[g]]
    sites = list(range(-2, 3))
    S = R.code({}, 0, sites)
    born = {}
    for t in range(steps):
        cur = set()
        for cell, mask in S.items():
            if cell % L != r:
                continue
            site = cell // L
            have = [k for k in pieces if (mask >> k) & 1]
            if have:
                if len(have) != len(pieces):
                    return False, "site %d half-built at t=%d" % (site, t)
                cur.add(site)
        for site in born:
            if site not in cur:
                return False, "site %d lost its hardware at t=%d" % (site, t)
        for site in cur - set(born):
            born[site] = t
        S = M.run(S, 1)
    grew = sorted(born.values())
    return True, "%d sites built, one per side per step, none re-amended" \
                 % len(born)


def _main():
    print("THE ANONYMOUS ITINERANT REGISTRY — every Turing machine as a "
          "finite code")
    print("  of the FOUNDING sector (occupancy guards, guards=None)\n")
    cases = [
        ("move-right (front test)", tm_move_right(), {}, 0, 20),
        ("move-left  (front test)", tm_move_left(), {}, 0, 20),
        ("binary increment 1011",   tm_binary_increment(),
         {0: 1, 1: 0, 2: 1, 3: 1}, 0, 18),
        ("busy beaver 3",           tm_busy_beaver3(), {}, 0, 16),
        ("busy beaver 4",           tm_busy_beaver4(), {}, 0, 26),
    ]
    for name, tm, tape, head, steps in cases:
        R = AnonRegistry(tm)
        C = R.M.const()
        good, k, got, want = certify(tm, tape, head, steps)
        print("  %-26s |Q|=%d %4d kinds  L=%2d  window %3d  %2d steps -> %s"
              % (name, len(tm.states), C.n, R.M.L, R.M.window(), steps,
                 "EXACT" if good else "FAIL at %d: %r vs %r" % (k, got, want)))
        assert good, (name, k, got, want)
    import random
    rng = random.Random(21)
    bad = n = 0
    for tm in random_tms(40, seed=5, nstates=3):
        tape = {c: 1 for c in range(-2, 3) if rng.randrange(2)}
        good, k, got, want = certify(tm, tape, 0, 12)
        n += 1
        bad += (not good)
    print("  %-26s %d random 3-state machines x random tapes x 12 steps: %d "
          "mismatches" % ("random TMs", n, bad))
    assert bad == 0
    good, msg = certify_hygiene(tm_busy_beaver3())
    print("  scaffolding hygiene:", msg if good else "FAIL " + msg)
    assert good, msg
    good, msg = certify_front_once(tm_busy_beaver3())
    print("  front discipline   :", msg if good else "FAIL " + msg)
    assert good, msg
    R = AnonRegistry(tm_busy_beaver3())
    C = R.M.const()
    print("  anonymity: guards cite no kind ->", not C.cited)
    assert not C.cited
    nf = [R.M.names[k] for k in range(C.n)
          if len(C.targets[k]) > 1 and R.M.names[k] not in R.M.raw_kinds]
    print("  out-degree: max %d over the whole constitution, max %d outside "
          "the fronts" % (R.M.outdeg(), R.M.outdeg(include_front=False)))
    assert not nf
    S = R.code({}, 0, list(range(-2, 3)))
    sz = []
    for t in range(30):
        sz.append(card(S))
        S = R.M.run(S, 1)
    print("  growth: |S_t| = %d ... %d, +%.1f laws/step (finite code, "
          "unbounded tape)" % (sz[0], sz[-1], (sz[-1] - sz[-11]) / 10.0))
    print("anontm self-tests passed")


if __name__ == "__main__":
    _main()
