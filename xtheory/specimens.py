#!/usr/bin/env python3
"""specimens.py — the certified specimen gallery of Expedition X-D.

Each specimen is printed as (constitution, seed) in a paste-ready form and
re-verified through the independent reference engine of xlib.

Run: python3 specimens.py
"""
import itertools
import json
import random
from collections import Counter, defaultdict

from xlib import (RULES1, Const, ref_step, to_pairs, all_seeds, seeds_span,
                  is_balanced, active_alphabet, target_image, entrenched_kinds,
                  in_degrees, components_cycles, cycle_offset_sum, reach_set)
import xnomos as X
from xnomos import state_of, active_laws, laws, card, classify, spacetime, render

OUT = {}


def show(name, C, S, mode="parity", steps=6, note=""):
    """Print + certify a specimen."""
    T = dict(S)
    lo, hi = min(T) - 1, max(T) + 2
    rows = spacetime(dict(T), C, steps, mode, lo, hi)
    r = classify(dict(S), C, mode, max_steps=400)
    # independent re-verification through the reference engine
    P = to_pairs(S)
    hist = [P]
    for _ in range(steps):
        P = ref_step(P, C, mode)
        hist.append(P)
    agree = all(to_pairs(x) == y for x, y in
                zip([dict(S)] + [None] * steps, [hist[0]]))
    T2 = dict(S)
    ok = True
    for h in hist:
        ok = ok and to_pairs(T2) == h
        T2 = X.step(T2, C, mode)
    print("\n--- %s ---" % name)
    if note:
        print("    %s" % note)
    print("    constitution : %s" % C.label())
    print("    seed         : %s   (mode=%s)" % (sorted(S.items()), mode))
    print("    verdict      : %s" % {k: v for k, v in r.items() if k != "history"})
    print("    ref-engine agreement over %d steps: %s" % (steps, ok))
    for row in rows:
        print("      " + row)
    OUT[name] = {"rules": C.rules, "targets": [list(t) for t in C.targets],
                 "seed": sorted(S.items()), "mode": mode,
                 "verdict": {k: v for k, v in r.items() if k != "history"},
                 "certified": bool(ok)}
    return r


def main():
    print("=" * 74)
    print("SPECIMEN GALLERY — Expedition X-D")
    print("=" * 74)

    # 1. the minimal balanced constitution: 2 laws in ONE cell
    C = Const([(0, -1, -1), (0, -1, -1)], targets=[0, 0])
    S = state_of([(0, 0), (0, 1)])
    show("BAL-1  the co-signed repeal (minimal balanced code)", C, S, steps=3,
         note="two kinds, two laws, ONE cell: both active forever, both repeal "
              "the (absent) kind-0 law at cell -1, and cancel.")

    # 2. the two-chamber deadlock (xnomos self-test 5) — 2 cells, 3 kinds
    C = Const([(0, 1, 1), (0, -1, -1), (0, 1, 0)], targets=[2, 2, 2])
    S = state_of([(0, 0), (2, 1)])
    show("BAL-2  the two-chamber deadlock", C, S, steps=3,
         note="kinds 0 and 1 both enact kind 2 into the gap at cell 1; under "
              "parity the two enactments cancel; under OR the code ignites.")
    show("BAL-2' the same code under OR", C, S, mode="or", steps=3)

    # 3. balance with NO in-degree-0 present kind (refutes the seed duality)
    C = Const([(0, 1, 1), (0, -1, -1), (0, 1, 0), (0, 1, 0)], targets=[2, 2, 0, 1])
    S = state_of([(0, 0), (2, 1)])
    show("BAL-3  balance without a graph-immortal kind", C, S, steps=3,
         note="every PRESENT kind has in-degree >= 1 in the amendment graph; "
              "entrenchment is dynamic (kinds 2,3 are absent), not structural.")

    # 4. the balance champion: near-universal balance
    C = Const([(0, -1, 0), (0, -1, 0)], targets=[0, 0])
    S = state_of([(0, 0), (0, 1), (1, 0), (3, 0), (3, 1), (4, 1)])
    show("BAL-4  the doubled frontier (balance champion)", C, S, steps=3,
         note="both kinds are the rule (0,-1,0) amending kind 0.  A code is "
              "balanced iff every run-start cell carries BOTH kinds.  Exact "
              "count of balanced codes of span s: a(s)=4a(s-1)-2a(s-2).")

    # 5. multi-target balance with no entrenched kind
    C = Const([(1, -1, -1), (0, -1, -1)], targets=[(0, 1), (0, 1)])
    S = state_of([(2, 0), (2, 1), (3, 1)])
    show("BAL-5  multi-target balance, nothing entrenched", C, S, steps=3,
         note="out-degree 2 defeats Theorem B: here A = t(A) = {0,1} and no "
              "present kind is unamendable, yet the code is balanced.")

    # 6. balance under SUPERSESSION (parity clear-votes cancel)
    best = None
    for r0 in RULES1:
        for r1 in RULES1:
            C2 = Const([r0, r1], [0, 1])
            for S2 in all_seeds(4, 2):
                if X.step(dict(S2), C2, "super") == S2 and active_laws(S2, C2):
                    k = (card(S2), max(S2) - min(S2))
                    if best is None or k < best[0]:
                        best = (k, r0, r1, tuple(sorted(S2.items())))
    _, r0, r1, S6 = best
    show("BAL-6  supersession balance (two clear-votes cancel)",
         Const([r0, r1], [0, 1]), dict(S6), mode="super", steps=3,
         note="under 'super' an active law CLEARS an occupied target cell; two "
              "clear-votes on one cell cancel under parity.  Own-kind targets: "
              "supersession makes balance possible without cross-amendment.")

    # 7. anchor death: the eldest law repealed, code survives
    C = Const([(-1, 1, -1), (0, 1, 1)], targets=[1, 0])
    S = state_of([(0, 1)])
    show("ANC-1  the self-repealing seed (anchor death from ONE law)", C, S,
         steps=6,
         note="kind 1 legislates kind 0 ahead of it; kind 0 turns round and "
              "repeals kind 1.  The eldest law CAN be repealed.")
    C = Const([(-1, 1, -1), (0, -1, 1)], targets=[1, 0])
    show("ANC-2  minimal anchor death (mutual annihilation)", C,
         state_of([(0, 1)]), steps=4)

    # 8. the zero-sum cryptic clock: constant occupancy, period 3
    C = Const([(0, -1, 1), (0, 1, -1), (-1, 1, 0)], targets=[2, 0, 1])
    S = state_of([(-2, 2), (2, 0), (2, 2), (3, 0), (3, 1)])
    show("CRY-1  the zero-sum cryptic clock (period 3, frozen occupancy)",
         C, S, steps=4,
         note="amendment 3-cycle 0->2->1->0 with offsets (+1,0,-1), sum 0.  "
              "Occupancy is constant forever: the code looks gridlocked from "
              "outside while its kinds rotate with period 3 — the only way to "
              "beat the 2-adic clock at constant occupancy.")

    # 9. the period-30 reciprocal cycle
    C = Const([(-1, 1, 0), (0, -1, 1)], targets=[1, 0])
    S = state_of([(0, 1), (2, 0), (4, 1), (5, 0), (6, 0)])
    show("PER-30  the longest 2-kind cycle in the box", C, S, steps=8,
         note="reciprocal amendment; period 30, the maximum over all "
              "143,327,232 runs of the span-8 census.")

    # 10. own-kind period 6 (refutes the {2,4} regularity of the own-kind census)
    C = Const([(0, -1, 1), (0, 1, -1)])
    S = state_of([(0, 0), (2, 0), (2, 1), (3, 1), (4, 1)])
    show("OWN-6  own-kind W=1 period 6", C, S, steps=7,
         note="OWN-KIND, window 1: 5 laws in 5 cells, period 6.  The own-kind "
              "census reported 'every cycle has period 2 or 4' across 9.07M "
              "seeds; that regularity is false — its 5-law stratum was sampled.")

    # 10b. own-kind period 8 from ONE kind
    C = Const([(0, -1, 1)])
    S = state_of([(0, 0), (2, 0), (4, 0), (6, 0)])
    show("OWN-8  the eight-fold sunset (one kind, own-kind, period 8)", C, S,
         steps=9,
         note="the sunset clause (0,-1,1) alone, four laws at {0,2,4,6}: "
              "period 8.  Smallest single-kind (0,-1,1) code with a period "
              "outside {2,4} (complete search of all such codes of span <= 9).")

    # 11. the cohort construction: balance of any even width, any kind count
    def cohort(m):
        n = 2 * m + 1
        C = Const([(0, -1, 1)] * m + [(0, 1, -1)] * m + [(0, 1, 0)], [n - 1] * n)
        S = {0: (1 << m) - 1, 2: ((1 << m) - 1) << m}
        return C, S
    C, S = cohort(3)
    show("COH-6  the six-fold co-signature", C, S, steps=3,
         note="six distinct kinds, all amending the (absent) kind 6 at cell 1: "
              "six toggles on one slot, even, cancel.  Works for every even "
              "cohort width 2m -- balanced codes with arbitrarily many "
              "distinct active kinds.  Delete one actor and the amendment "
              "passes.")
    ok = all(is_balanced(cohort(m)[1], cohort(m)[0]) for m in (1, 2, 3, 4, 6, 10))
    Cx, Sx = cohort(3)
    Sx[0] &= ~1                                   # odd cohort
    print("\n  cohort balanced for m=1,2,3,4,6,10: %s ; odd cohort balanced: %s"
          % (ok, is_balanced(Sx, Cx)))

    # ---- the exact balance count recurrence, verified
    print("\n" + "=" * 74)
    print("EXACT BALANCE COUNT (constitution BAL-4)")
    C = Const([(0, -1, 0), (0, -1, 0)], targets=[0, 0])
    a = []
    for span in range(1, 13):
        if span <= 8:
            n = sum(1 for S in seeds_span(span, 2) if is_balanced(S, C))
        else:
            n = 4 * a[-1] - 2 * a[-2]
        a.append(n)
    print("  balanced codes of span s (s=1..8 by brute force, then recurrence):")
    print("   ", a)
    print("  recurrence a(s) = 4a(s-1) - 2a(s-2) verified for s=3..8: %s"
          % all(a[i] == 4 * a[i - 1] - 2 * a[i - 2] for i in range(2, 8)))
    print("  growth rate 2+sqrt(2) = %.6f ; entropy %.4f bits/cell (of 2)"
          % (2 + 2 ** .5, __import__("math").log2(2 + 2 ** .5)))
    print("  => balanced codes are an exponentially large, positive-entropy set:")
    print("     balance is NOT measure zero in law-space.")

    # ---- richest balanced code found in a wider search
    print("\n" + "=" * 74)
    print("RICHEST BALANCED CODE (search over 4-kind constitutions)")
    rng = random.Random(99)
    best = None
    for _ in range(300000):
        n = 4
        C = Const([rng.choice(RULES1) for _ in range(n)],
                  [rng.randrange(n) for _ in range(n)])
        S = {}
        for _ in range(rng.randrange(3, 9)):
            c = rng.randrange(0, 6)
            S[c] = S.get(c, 0) | (1 << rng.randrange(n))
        if is_balanced(S, C):
            A = active_alphabet(S, C)
            score = (len(active_laws(S, C)), len(A), len(S))
            if best is None or score > best[0]:
                best = (score, C, dict(S))
    score, C, S = best
    print("  active laws %d, distinct active kinds %d, cells %d" % score)
    show("BAL-RICH  a large balanced constitution", C, S, steps=3)

    json.dump(OUT, open("data/specimens.json", "w"), indent=1, default=str)
    print("\nwrote data/specimens.json (%d specimens)" % len(OUT))


if __name__ == "__main__":
    main()
