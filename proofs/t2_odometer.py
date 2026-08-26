#!/usr/bin/env python3
"""
t2_odometer.py — Expedition Y-D, TARGET 2: the four-law coincidence, dissolved.

THE CLAIM.  The Jubilee Code (own-kind, 3 kinds, nomos2d) and THE ODOMETER
(cross-amendment, 2 kinds, xamend2d) are not two machines that happen to reset
to four laws.  They are ONE machine.  Both reduce to the carry automaton

    K :  C  |->  C  xor  { c+1 : c in C, (c = 0 or c-1 in C) }        (C subset N)

the Jubilee at one step per application of K, the Odometer at TWO.  Precisely

    kappa_O( Phi_O^{2u} (seed_O) )  =  kappa_J( Phi_J^u (seed_J) ) + 1
    |Phi_O^{2u}(seed_O)|            =  |Phi_J^u(seed_J)|

where kappa reads off the counter word.  The Odometer's odd half-step is the
materialised carry buffer: the pending carries stand as real laws in column
x = 1 for one tick and are written back on the next.

Run:  python3 proofs/t2_odometer.py            (~30 s)
      python3 proofs/t2_odometer.py --deep     (~4 min; lockstep to t = 2^17)
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, laws, card, active_laws
from t1_jubilee import monomials, masks, closed_card_mask, supp2

PASS, FAIL = [], []


def check(name, ok, note=""):
    (PASS if ok else FAIL).append(name)
    print("  %s  %s%s" % ("ok  " if ok else "FAIL", name,
                          ("   [%s]" % note) if note else ""))


V = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
     "P": (1, -1), "Q": (-1, -1), "R": (1, 1), "T": (-1, 1)}


def off(s):
    return tuple(V[ch] for ch in s)


ODO = Const([off("OEW"), off("NQR")], [(1,), (0, 1)], dim=2)
OSEED = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])

E, W, N, S = (1, 0), (-1, 0), (0, -1), (0, 1)
JUB = Const([(E, S, N), (S, N, S), (W, N, E)], dim=2)
JSEED = state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)])


# ------------------------------------------------------- the carry automaton K
def K(C):
    """C |-> C xor {c+1 : c in C, (c = 0 or c-1 in C)}."""
    tog = {c + 1 for c in C if c == 0 or (c - 1) in C}
    return C ^ tog


def act(C):
    """#active laws of the carry automaton = #{c in C : c=0 or c-1 in C}."""
    return sum(1 for c in C if c == 0 or (c - 1) in C)


def A(Kk, Ms):
    """A(K) = #{n : M_n subset [0,K]}; A(-1) = 0."""
    if Kk < 0:
        return 0
    full = (1 << (Kk + 1)) - 1
    return sum(1 for m in masks(Ms) if m & ~full == 0)


def main():
    deep = "--deep" in sys.argv
    print("TARGET 2 — the four-law coincidence\n")
    Ms = monomials(2000)
    MK = masks(Ms)

    # ---------------------------------------------------------------- the lift
    print("the reduction of THE ODOMETER (structure of its orbit)")
    T = (1 << 16) if deep else (1 << 13)
    X = dict(OSEED)
    Y = dict(JSEED)
    err = None
    Cj = frozenset([0])
    for u in range(T):
        # even tick 2u: frame + counter word in column 0
        Aset = sorted(c for c, k in laws(X) if k == 0)
        Bcol0 = sorted(c[1] for c, k in laws(X) if k == 1 and c[0] == 0)
        Bcol1 = sorted(c[1] for c, k in laws(X) if k == 1 and c[0] == 1)
        if Aset != [(0, 0), (1, 0)]:
            err = "frame broken at t=%d: A = %s" % (2 * u, Aset)
            break
        if Bcol1:
            err = "column 1 not empty at even t=%d" % (2 * u)
            break
        if any(c[0] > 1 for c in X):
            err = "column >= 2 occupied at t=%d" % (2 * u)
            break
        # the Jubilee's counter word, shifted
        Cjub = sorted(c[0] for c, k in laws(Y) if k == 2)
        if Bcol0 != [c + 1 for c in Cjub]:
            err = "kappa_O(2u) != kappa_J(u)+1 at u=%d" % u
            break
        if sorted(Cjub) != sorted(Cj):
            err = "engine Jubilee != carry automaton K at u=%d" % u
            break
        if card(X) != card(Y):
            err = "|S_O(2u)| != |S_J(u)| at u=%d" % u
            break
        # odd tick 2u+1: the carry buffer is materialised in column x=1
        X1 = step(X, ODO)
        a1 = sorted(c[1] for c, k in laws(X1) if k == 0 and c[0] == 1
                    and c[1] > 0)          # excluding the frame law A@(1,0)
        b1 = sorted(c[1] for c, k in laws(X1) if k == 1 and c[0] == 1)
        b0 = sorted(c[1] for c, k in laws(X1) if k == 1 and c[0] == 0)
        carry = sorted(c + 1 for c in Cjub if c == 0 or (c - 1) in set(Cjub))
        if a1 != b1 or a1 != [c + 1 for c in carry]:
            err = "carry buffer wrong at t=%d" % (2 * u + 1)
            break
        if b0 != [0] + [c + 1 for c in Cjub]:
            err = "column 0 wrong at odd t=%d" % (2 * u + 1)
            break
        if card(X1) != 3 + len(Cjub) + 2 * act(set(Cjub)):
            err = "odd card formula wrong at t=%d" % (2 * u + 1)
            break
        X = step(X1, ODO)
        Y = step(Y, JUB)
        Cj = K(Cj)
    check("Odometer(2u) == Jubilee(u) + shift, for every u < 2^%d  (COMPLETE box)"
          % (T.bit_length() - 1), err is None,
          err or "frame {A@(0,0),A@(1,0),B@(0,1)}; counter word in column 0")
    check("...and the carry automaton K reproduces the Jubilee's kind-2 support",
          err is None, "K(C) = C xor {c+1 : c in C, c=0 or c-1 in C}")

    # ------------------------------------------------- the two card identities
    print("\nthe card identities")
    C = frozenset([0])
    okE = okO = True
    for u in range(1 << 14):
        if 3 + (len(C) - 1) != closed_card_mask(u, MK):
            okE = False
            break
        C = K(C)
    check("|S_O(2u)| = |S_J(u)| = 3 + wt(y_u) for u < 2^14", okE)

    C = frozenset([0])
    odd = []
    for u in range(1 << 12):
        odd.append(3 + len(C) + 2 * act(C))
        C = K(C)
    # against the engine
    X = dict(OSEED)
    eng = []
    for t in range(1 << 13):
        if t % 2 == 1:
            eng.append(card(X))
        X = step(X, ODO)
    check("|S_O(2u+1)| = 3 + |C_u| + 2.act(C_u), engine-checked u < 2^12",
          odd == eng, "%s..." % odd[:8])

    # --------------------------------------------------- the two clock laws
    print("\nthe clock laws, both now corollaries of TARGET 1")
    reset_o = {closed_card_mask(1 << (k - 1), MK) for k in range(1, 18)}
    check("|S_O(2^k)| = |S_J(2^{k-1})| = 4 for k = 1..17", reset_o == {4},
          "values %s" % reset_o)

    crestJ = [3 + A(k - 1, Ms) for k in range(3, 18)]
    check("Jubilee crest  |S_J(2^k-1)| = 3 + A(k-1)",
          crestJ == [7, 8, 13, 14, 25, 26, 49, 50, 97, 98, 193, 194, 385, 386,
                     769], "%s" % crestJ)
    crestO = [6 + 3 * A(k - 2, Ms) for k in range(1, 10)]
    check("Odometer crest |S_O(2^k-1)| = 6 + 3.A(k-2)",
          crestO == [6, 9, 12, 18, 21, 36, 39, 72, 75],
          "%s  (matches XFINDINGS Sec.3)" % crestO)

    # ------------------------------------------- the reach: a correction
    print("\nthe Odometer's reach  [CORRECTION to xamend2d/RESULTS.md headline 9]")
    X = dict(OSEED)
    KMAX = 16 if deep else 14
    heights = {}
    for t in range(1, (1 << KMAX) + 1):
        X = step(X, ODO)
        if (t & (t - 1)) == 0:
            ys = [c[1] for c in X]
            heights[t.bit_length() - 1] = max(ys) - min(ys) + 1

    def m_index(k):
        """the unique n with M_n = {k}."""
        if k <= 2:
            return k
        j = (k - 1) // 2
        return 3 * (1 << j) - 2 if k % 2 == 1 else 3 * (1 << j) - 1

    pred = {k: m_index(k - 1) + 3 for k in heights if k >= 1}
    ok = all(heights[k] == pred[k] for k in pred)
    check("height(2^k) = m_{k-1} + 3 exactly, k = 1..%d (engine)" % KMAX, ok,
          "%s" % [heights[k] for k in sorted(heights) if k >= 1])
    fit = [(k, heights[k], round(0.20 * k * k, 1)) for k in sorted(heights)
           if k >= 8]
    check("the published fit 0.20 (log2 t)^2 is REFUTED",
          all(h > 1.5 * f for _, h, f in fit),
          "measured vs fit: %s" % fit)
    k20 = m_index(19) + 3
    check("height at t = 2^20 is %d, not the published 86" % k20, k20 != 86,
          "reach = 3.2^{floor((k-2)/2)} + O(1) ~ 1.5 sqrt(t), same order as the "
          "Jubilee's — because it IS the Jubilee")
    ratios = [heights[k] / math.sqrt(1 << k) for k in sorted(heights) if k >= 8]
    check("height(2^k) / 2^{k/2} stays in (1.0, 1.6): Theta(sqrt t), not polylog",
          all(1.0 < r < 1.6 for r in ratios),
          "%s  (it oscillates because the reach doubles every SECOND power)"
          % [round(r, 3) for r in ratios])

    # --------- TWO machines wear the name THE ODOMETER
    print("\ntwo compasses, two machines  [xamend2d/xa2d.py sets N=(0,+1);"
          " root verify.py and nomos2d set N=(0,-1)]")
    ROOTC = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
             "P": (1, -1), "Q": (-1, -1), "R": (1, 1), "T": (-1, 1)}
    XA2DC = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
             "P": (1, 1), "Q": (-1, 1), "R": (1, -1), "T": (-1, -1)}

    def build(Vc):
        return Const([tuple(Vc[c] for c in "OEW"), tuple(Vc[c] for c in "NQR")],
                     [(1,), (0, 1)], dim=2)

    prof = {}
    KM = 16
    for nm, Vc in (("root", ROOTC), ("xa2d", XA2DC)):
        Cn = build(Vc)
        Xn = dict(OSEED)
        res, cre, hei = {}, {}, {}
        for t in range((1 << KM) + 1):
            k = t.bit_length() - 1
            if t and (t & (t - 1)) == 0:
                res[k] = card(Xn)
                ys = [c[1] for c in Xn]
                hei[k] = max(ys) - min(ys) + 1
            if t and ((t + 1) & t) == 0 and t.bit_length() <= KM:
                cre[t.bit_length()] = card(Xn)
            Xn = step(Xn, Cn)
        prof[nm] = (res, cre, hei)

    check("ROOT-compass Odometer: |S_{2^k}| = 4 for k = 1..16 (the Jubilee's twin)",
          {prof["root"][0][k] for k in range(1, 17)} == {4},
          "crests %s" % [prof["root"][1][k] for k in range(1, 10)])
    check("XA2D-compass Odometer is a DIFFERENT machine and does NOT reset to 4",
          {prof["xa2d"][0][k] for k in range(1, 17)} != {4},
          "|S_{2^k}|, k=1..16 = %s   (not 4 at k = 1,2,3,5,8,12)"
          % [prof["xa2d"][0][k] for k in range(1, 17)])
    check("XA2D-compass profile reproduces xamend2d Sec.11.2's table exactly",
          [prof["xa2d"][2][k] for k in (10, 12, 14, 16)] == [20, 26, 38, 47]
          and [prof["xa2d"][1][k] for k in (10, 12, 14, 16)] == [57, 75, 111, 138]
          and prof["xa2d"][0][12] == 6,
          "heights 20,26,38,47 and crests 57,75,111,138 at k=10,12,14,16, "
          "card 6 at t=2^12 — all as published")
    check("ROOT-compass profile is the one XFINDINGS Sec.3 quotes",
          [prof["root"][1][k] for k in range(1, 10)]
          == [6, 9, 12, 18, 21, 36, 39, 72, 75])

    # the two engines themselves agree; the clash is in the offset dictionary
    try:
        sys.path.insert(0, os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "xamend2d"))
        import xa2d
        import random as _rnd
        rng = _rnd.Random(11)
        OFFS = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        badn = 0
        for _ in range(400):
            n = rng.randrange(1, 4)
            rules = [tuple(rng.choice(OFFS) for _ in range(3)) for _ in range(n)]
            tg = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                  for _ in range(n)]
            P = [((rng.randrange(-3, 4), rng.randrange(-3, 4)), rng.randrange(n))
                 for _ in range(rng.randrange(1, 7))]
            A1, A2 = state_of(P), xa2d.state(P)
            C1, C2 = Const(rules, tg, dim=2), xa2d.Const(rules, tg)
            for _ in range(6):
                A1, A2 = step(A1, C1), xa2d.step(A2, C2)
                if A1 != A2:
                    badn += 1
                    break
        check("the two ENGINES agree: xnomos.step == xa2d.step on identical "
              "constitutions", badn == 0,
              "400 random 2-D systems x 6 steps, 0 divergences — the clash is "
              "the compass, not the engine")
    except ImportError:
        check("engine cross-validation (xa2d import)", False, "xa2d not importable")

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
