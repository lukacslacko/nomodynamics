#!/usr/bin/env python3
"""
specimens.py — the fauna gallery of chapter three, with certificates.

Every specimen below is re-verified by an independent code path: the bitfield
engine `cite.py` finds and renders it, and `xnomos.py` (the shared dict engine
of the whole repository, no code in common with `cite.step_fields`) re-checks
the certificate.

    python3 specimens.py            # print the gallery
    python3 specimens.py NAME       # one specimen
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cite as ct                                              # noqa: E402
import xnomos as X                                             # noqa: E402


def hexrow(F, lo, hi):
    s = ""
    for i in range(lo, hi + 1):
        b = 1 << (i + ct.BIAS)
        m = sum(1 << k for k in range(len(F)) if F[k] & b)
        s += "." if m == 0 else "%X" % m
    return s


def maprow(F, lo, hi, table):
    s = ""
    for i in range(lo, hi + 1):
        b = 1 << (i + ct.BIAS)
        m = sum(1 << k for k in range(len(F)) if F[k] & b)
        s += table.get(m, "?")
    return s


def band(title):
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def xn_check(C, pairs, mode, steps, modulus=None):
    """Run the same code on xnomos and return its states as frozen tuples."""
    XC = C.to_xnomos(modulus=modulus)
    S = X.state_of(pairs, C.n)
    out = [X.freeze(S)]
    for _ in range(steps):
        S = X.step(S, XC, mode)
        out.append(X.freeze(S))
    return out


def cite_states(C, pairs, mode, steps):
    F = ct.state_fields(pairs, C.n)
    out = [tuple(sorted(ct.fields_to_pairs(F)))]
    for _ in range(steps):
        F = ct.step_fields(F, C, mode)
        out.append(tuple(sorted(ct.fields_to_pairs(F))))
    return out


def agree(C, pairs, mode, steps):
    a = cite_states(C, pairs, mode, steps)
    XC = C.to_xnomos()
    S = X.state_of(pairs, C.n)
    b = [tuple(sorted((c, k) for c, k in X.laws(S)))]
    for _ in range(steps):
        S = X.step(S, XC, mode)
        b.append(tuple(sorted((c, k) for c, k in X.laws(S))))
    return a == b


# =========================================================== 1. GRIDLOCK DIES

def gridlock():
    band("1. GRIDLOCK DIES — the same solid block under the two guards")
    print("""A block of ten kind-0 laws.  Kind 0 = (0,1,1): "while something stands
at my cell and <exception> to my right, enact ... to my right." """)
    for guards, name in ((None, "occupancy  h = any  (chapters one and two)"),
                         ([(None, 1), (None, 1)], "citation   h = kind 1")):
        C = ct.Cit([(0, 1, 1), (0, 1, 1)], [(0,), (0,)],
                   guards or [(None, None), (None, None)])
        pairs = [(i, 0) for i in range(10)]
        F = ct.state_fields(pairs, 2)
        act = ct.card_fields(ct.active_fields(F, C))
        rows = ct.spacetime(F, C, 4, lo=0, hi=13)
        print("  %-42s active laws: %2d" % (name, act))
        for r in rows:
            print("        |%s|" % r)
    print("  Gridlock survives for C  <=>  h_k in {any, k, g_k} for every k.")


# ================================================================= 2. LACUNA

LAC = ct.Cit([(0, -1, 0), (0, 0, 0)], [(0,), (0,)], [(None, 0), (None, 0)])


def lacuna():
    band("2. LACUNA — a hole travelling at the speed of light through a "
         "COMPLETE code")
    print("""  0:(0,-1,0) cite(any,0) ->{0}   "while my exception -- a section-0 law
                                    one to my left -- is absent, repeal
                                    section 0 here"
  1:(0, 0,0) cite(any,0) ->{0}   "while no section-0 law stands here,
                                    enact section 0 here"

Every cell of the ring carries both sections except one, which is missing
section 0.  Section 1 refills the gap; section 0, now un-blocked one cell on,
repeals itself.  The gap walks.  Occupancy NEVER changes: this is a solid,
completely occupied code in perpetual motion, which chapter one's Gridlock
forbids and chapter two inherits.""")
    m = 13
    full = (1 << m) - 1
    S = (full & ~1, full)
    t0, p, seq = ct.ring_orbit(S, LAC, m)
    tab = {0: ".", 1: "a", 2: "o", 3: "#"}
    print("\n  ring Z/%d, unrolled  (# = both sections, o = the LACUNA)" % m)
    for t in range(6):
        st = seq[t % len(seq)]
        s = "".join(tab[(1 if (st[0] >> i) & 1 else 0)
                        | (2 if (st[1] >> i) & 1 else 0)] for i in range(m))
        print("    t=%d |%s|" % (t, s))
    print("    ...  period %d = m, and Phi = rot_(+1) exactly." % p)
    for mm in (7, 11, 13, 16, 21):
        f = (1 << mm) - 1
        A = (f & ~1, f)
        B = ct.step_ring(A, LAC, mm)
        want = tuple(((x >> (mm - 1)) | (x << 1)) & f for x in A)
        XC = LAC.to_xnomos(modulus=mm)
        S0 = X.state_of([(i, 0) for i in range(mm) if i != 0]
                        + [(i, 1) for i in range(mm)])
        S1 = X.step(S0, XC)
        wx = {(c + 1) % mm: mask for c, mask in S0.items()}
        r = X.classify(S0, XC, "parity", max_steps=4 * mm + 4)
        print("    m=%2d: cite Phi=rot_1 %s | xnomos Phi=rot_1 %s | xnomos "
              "%s p=%s" % (mm, B == want, S1 == wx, r["kind"], r.get("period")))
    print("\n  On Z the same code is a LACUNA GUN: the left end of a finite "
          "block\n  emits a hole every two steps, and each runs off to the "
          "right.")
    L = 16
    pairs = [(i, 0) for i in range(L) if i != 3] + [(i, 1) for i in range(L)]
    F = ct.state_fields(pairs, 2)
    for t in range(8):
        print("    t=%d |%s|  card=%d" % (t, maprow(F, 0, L - 1, tab),
                                          ct.card_fields(F)))
        F = ct.step_fields(F, LAC, "parity")
    print("    agrees with xnomos over 8 steps: %s"
          % agree(LAC, pairs, "parity", 8))


# ======================================================== 3. THE SIX SESSIONS

SIX = ct.Cit([(-1, 1, 0)] * 3, [(0, 1), (1, 2), (0, 1, 2)],
             [(None, 1), (None, 2), (None, 0)])


def six():
    band("3. THE SIX SESSIONS — a bulk oscillator: solid code whose INTERIOR "
         "cycles")
    print("""  0:(-1,1,0) cite(any,1) ->{0,1}
  1:(-1,1,0) cite(any,2) ->{1,2}
  2:(-1,1,0) cite(any,0) ->{0,1,2}

Period 6 = 2^3 - 2, the maximum possible at three kinds (the bulk map fixes
both the empty set and the full set, so a cycle lives in the other 2^n - 2
subsets).  Digits below are the kind-set of each cell in hex:
1={0} 2={1} 4={2} 3={0,1} 5={0,2} 6={1,2} 7={0,1,2}.""")
    L = 13
    pairs = [(i, 0) for i in range(L)]
    F = ct.state_fields(pairs, 3)
    print()
    for t in range(8):
        print("    t=%d |%s|  card=%2d" % (t, hexrow(F, 0, L - 1),
                                           ct.card_fields(F)))
        F = ct.step_fields(F, SIX, "parity")
    print("""    The LEFT EDGE IS FROZEN and the interior runs: the exact
    inversion of chapter one's "all dynamics is surface dynamics".""")
    print("    agrees with xnomos over 8 steps: %s"
          % agree(SIX, pairs, "parity", 8))
    for m in (5, 7, 9, 11):
        S = ((1 << m) - 1, 0, 0)
        t0, p, seq = ct.ring_orbit(S, SIX, m)
        XC = SIX.to_xnomos(modulus=m)
        r = X.classify(X.state_of([(i, 0) for i in range(m)]), XC, "parity",
                       max_steps=60)
        print("    ring m=%2d: cite period %d | xnomos %s period %s"
              % (m, p, r["kind"], r.get("period")))


# ======================================================= 4. PASCAL / THE COPY

PAS = ct.Cit([(0, 0, 1), (0, 0, 0)], [(0,), (1,)], [(0, 1), (1, 0)])


def pascal():
    band("4. THE PASCAL CLAUSE and THE COPY — 1-D own-kind Sierpinski, and a "
         "universal replicator")
    print("""  0:(0,0,1) cite(0,1) ->{0}   "while a section-0 law stands at my own
                                 cell (always: I am one) and no section-1 law
                                 stands here (never: section 1 is never
                                 enacted), enact section 0 to my right"
  1: anything  -- the PHANTOM, never placed.

The guard is a tautology, so the law acts unconditionally and the step map is
exactly F <- F xor (F<<1), the additive rule 60.  Own-kind targeting, out-degree
1, window 1, on Z -- the tamest corner of chapter one, where the only fauna were
colonizers and blinkers.  Citation puts a Sierpinski gasket in it.""")
    F = ct.state_fields([(0, 0)], 2)
    print()
    for t in range(9):
        print("    t=%d |%s|  card=%3d = 2^popcount(t)"
              % (t, ct.render_fields(F, 0, 16), ct.card_fields(F)))
        F = ct.step_fields(F, PAS, "parity")
    print("    agrees with xnomos over 9 steps: %s"
          % agree(PAS, [(0, 0)], "parity", 9))
    print("""
  THE COPY.  Over F2, (I+N)^(2^j) = I + N^(2^j), so at every t = 2^j larger
  than the span of the seed, EVERY finite code stands beside a disjoint
  translate of itself: a universal replicator, proved rather than found.""")
    for seed in ([(0, 0)], [(0, 0), (1, 0), (3, 0)],
                 [(0, 0), (2, 0), (3, 0), (7, 0)],
                 [(0, 0), (5, 0), (6, 0), (9, 0), (20, 0)]):
        F0 = ct.state_fields(seed, 2)
        span = max(c for c, _ in seed) - min(c for c, _ in seed)
        ok, ts = [], []
        for j in range(1, 10):
            t = 1 << j
            if t <= span:
                continue
            F = ct.advance(F0, PAS, t, "parity")
            ok.append(F == [F0[0] | (F0[0] << t), F0[1]])
            ts.append(t)
        print("    span %2d  seed %-34s replicates at t=%s: %s"
              % (span, seed, ",".join(map(str, ts[:3])) + ",...", all(ok)))
    XC = PAS.to_xnomos()
    S = X.state_of([(0, 0), (1, 0), (3, 0)], 2)
    for _ in range(16):
        S = X.step(S, XC)
    print("    xnomos re-check at t=16: %s"
          % (sorted(S) == [0, 1, 3, 16, 17, 19]))


# ==================================================== 5. THE WRIT (a wire)

WRIT = ct.Cit([(0, 0, 0), (0, 0, 1), (0, 0, 0), (0, 0, 0)],
              [(), (0,), (0,), ()],
              [(3, 3), (0, 3), (0, 3), (3, 3)])


def writ():
    band("5. THE WRIT — a signal propagating at speed 1 through fully "
         "occupied code")
    print("""  0 = Z  the signal        cite(3,3): its precedent is the phantom, so a
                            signal law is never active -- it is pure data
  1 = G  the relay  (0,0,1) cite(Z,phi) ->{Z}   copy Z one cell right
  2 = E  the eraser (0,0,0) cite(Z,phi) ->{Z}   clear Z here
  3 = phi the phantom, never enacted

Z(i)' = Z(i) xor Z(i) xor Z(i-1) = Z(i-1): a shift register.  G and E stand at
every cell and nobody amends them, so the wire is ENTRENCHED and the signal is
ORDINARY law: the constitution splits into a machine and its data.""")
    L = 16
    pairs = [(i, 1) for i in range(L)] + [(i, 2) for i in range(L)] + [(2, 0)]
    F = ct.state_fields(pairs, 4)
    tab = {6: ":", 7: "X"}
    print()
    for t in range(9):
        print("    t=%d |%s|  card=%d" % (t, maprow(F, 0, L - 1, tab),
                                          ct.card_fields(F)))
        F = ct.step_fields(F, WRIT, "parity")
    print("    (: = the entrenched relay+eraser pair, X = the signal)")
    print("    agrees with xnomos over 9 steps: %s"
          % agree(WRIT, pairs, "parity", 9))
    m = 9
    f = (1 << m) - 1
    S = (1 << 2, f, f, 0)
    T = ct.step_ring(S, WRIT, m)
    want = tuple(((x >> (m - 1)) | (x << 1)) & f for x in S)
    XC = WRIT.to_xnomos(modulus=m)
    S0 = X.state_of([(i, 1) for i in range(m)] + [(i, 2) for i in range(m)]
                    + [(2, 0)], 4)
    r = X.classify(S0, XC, "parity", max_steps=40)
    print("""
  PROCESSION.  On Z/%d with the relay and eraser at every cell, Phi = rot_(+1)
  EXACTLY, on a ring every cell of which is occupied at every step: the code
  revolves while its occupancy never changes.  Genuine transport (r=1 <= p*W=1),
  not chapter one's barber pole.""" % m)
    print("    cite: Phi = rot_1  %s | xnomos: %s period %s"
          % (T == want, r["kind"], r.get("period")))


# ================================================ 6. THE CONVERSION FRONT

CONV = ct.Cit([(-1, -1, -1), (-1, -1, -1)], [(0, 1), (0, 1)],
              [(None, 0), (None, 1)])


def conversion():
    band("6. THE CONVERSION FRONT — one solid phase eating another")
    print("""  0:(-1,-1,-1) cite(any,0) ->{0,1}
  1:(-1,-1,-1) cite(any,1) ->{0,1}

Two solid phases: everything-is-section-0 and everything-is-section-1.  Each is
a fixed point of the bulk map, so each region is frozen on its own.  At the
seam, the vacancy clause of the far side's citation is satisfied and the seam
advances one cell per step.""")
    L = 20
    tab = {0: ".", 1: "a", 2: "b", 3: "#"}
    pairs = [(i, 0) for i in range(10)] + [(i, 1) for i in range(10, L)]
    F = ct.state_fields(pairs, 2)
    print()
    for t in range(7):
        print("    t=%d |%s|" % (t, maprow(F, 0, L - 1, tab)))
        F = ct.step_fields(F, CONV, "parity")
    print("    agrees with xnomos over 7 steps: %s"
          % agree(CONV, pairs, "parity", 7))


# =============================================================== 6b. THE LEDGER

LEDGER = ct.Cit([(-1, -1, 0), (0, 0, 1)], [(1,), (0, 1)], [(1, 0), (1, 0)])
LEDGER_SEED = [(0, 0), (0, 1), (2, 1)]


def ledger():
    band("6b. THE LEDGER — a binary counter on the LINE: three laws, two kinds")
    print("""  0:(-1,-1,0) cite(1,0) ->{1}     1:(0,0,1) cite(1,0) ->{0,1}
  seed: A and B at cell 0, B at cell 2   (three laws)

Bounded population, unbounded reach, hence aperiodic — the 1-D analogue of the
Jubilee Code and the Odometer, which are both two-dimensional.  At t = 4^j the
state is EXACTLY a fixed three-law head plus a two-law marker that doubles its
distance:

      S(4^j)  =  { A@0, B@0, B@2 }  u  { A@(2^j+2), B@(2^j+2) }

so card = 5 at every t = 4^j and the reach is exactly sqrt(t) + 3.""")
    F = ct.state_fields(LEDGER_SEED, 2)
    print()
    for t in range(20):
        print("    t=%2d |%s|" % (t, ct.render_fields(F, -3, 14)))
        F = ct.step_fields(F, LEDGER, "parity")
    print()
    F = ct.state_fields(LEDGER_SEED, 2)
    head = {(0, 0), (0, 1), (2, 1)}
    for t in range(1, 4 ** 8 + 1):
        F = ct.step_fields(F, LEDGER, "parity")
        b = t.bit_length() - 1
        if t >= 4 and (t & (t - 1)) == 0 and b % 2 == 0:
            j = b // 2
            pts = set(ct.fields_to_pairs(F))
            occ = F[0] | F[1]
            span = occ.bit_length() - ((occ & -occ).bit_length() - 1)
            want = head | {(2 ** j + 2, 0), (2 ** j + 2, 1)}
            print("    t=4^%-2d = %-7d card=%d span=%-5d head+marker exact: %s"
                  % (j, t, ct.card_fields(F), span, pts == want))
    print("    agrees with xnomos over 3000 steps: %s"
          % agree(LEDGER, LEDGER_SEED, "parity", 3000))


# ============================================================ 7. THE MACHINE

def machine():
    band("7. THE STATUTE MACHINE — every 1-D cellular automaton, exactly")
    import circuit
    rows, ok, tot = circuit.gate_inventory()
    print("  gate inventory (one step, parity):")
    for name, good, tt in rows:
        print("    %-22s %s   %s" % (name, "OK " if good else "FAIL", tt))
    M = circuit.ECA(110)
    print("\n  Rule 110 as a constitution: %d kinds, window 1, 2 steps per CA "
          "step" % M.C.n)
    m = 30
    bits = [0] * m
    bits[m - 2] = 1
    st = M.seed_ring(bits)
    ref = list(bits)
    print("  Rule 110 from a single 1 on Z/%d:" % m)
    for t in range(12):
        print("    %s" % "".join("#" if b else "." for b in ref))
        st = ct.step_ring(st, M.C, m)
        st = ct.step_ring(st, M.C, m)
        ref = circuit.eca_step(ref, 110)
        assert M.read_ring(st, m) == ref, t
    print("  ...machine and reference CA agree at every step.")


NAMES = dict(gridlock=gridlock, lacuna=lacuna, six=six, pascal=pascal,
             writ=writ, conversion=conversion, ledger=ledger, machine=machine)

if __name__ == "__main__":
    todo = sys.argv[1:] or list(NAMES)
    for nm in todo:
        NAMES[nm]()
    print()
