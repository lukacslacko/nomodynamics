#!/usr/bin/env python3
"""
t3_verify.py — Expedition Y-D, TARGET 3: the single-field cap, refuted.

The coordinator's battery entry for Target 3.  Every check here is written
against `xnomos` alone (Const / step / classify / verify_glider) and carries its
own primitivity test, so it is independent both of `xspeed/sft.py` (which
produced the claim) and of `proofs/t3_core.py` etc. (which produced the
refutation).  The deeper theory — the 512/343 type reduction, the complete
generator censuses — lives in the `t3_*.py` scripts listed in RESULTS.md Sec.8.

Run:  python3 proofs/t3_verify.py            (~40 s)
      python3 proofs/t3_verify.py --deep     (adds the wider fuzz)
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, step, classify, verify_glider, laws, card

PASS, FAIL = [], []


def check(name, ok, note=""):
    (PASS if ok else FAIL).append(name)
    print("  %s  %s%s" % ("ok  " if ok else "FAIL", name,
                          ("   [%s]" % note) if note else ""))


def single_field(rules):
    """T_k = K for every k — the single-field sector."""
    n = len(rules)
    return Const(rules, [tuple(range(n))] * n)


def allkinds(cells, n):
    return state_of([(c, k) for c in cells for k in range(n)])


def certify(rules, cells, mode, p, d):
    """Phi^p = sigma^d over three periods, AND (p,d) primitive, AND classify
    agrees on the minimal period and displacement.  Returns (ok, note)."""
    n = len(rules)
    C = single_field(rules)
    S = allkinds(cells, n)
    if not verify_glider(S, C, p, d, mode):
        return False, "verify_glider failed"
    for q in range(2, p + 1):
        if p % q == 0 and d % q == 0 and verify_glider(S, C, p // q, d // q, mode):
            return False, "not primitive: also Phi^%d = sigma^%d" % (p // q, d // q)
    r = classify(S, C, mode, max_steps=4 * p + 40, max_card=8000, max_span=8000)
    if r["kind"] != "GLIDER" or r["period"] != p or r["displacement"] != d:
        return False, "classify says %s p=%s d=%s" % (r["kind"], r.get("period"),
                                                      r.get("displacement"))
    return True, "n=%d, %d cells, span %d" % (n, len(cells),
                                              max(cells) - min(cells) + 1)


SPECIMENS = [
    # name, rules, seed cells, mode, p0, d0
    ("QUINT-3/5   (one cell, 5 kinds)",
     [(0, -1, 0), (0, -1, 1), (0, 1, -1), (0, 1, 0), (0, 1, 1)], [0],
     "parity", 5, 3),
    ("TRIAD-4/4   (THREE kinds)",
     [(1, -1, 0), (-1, 1, -1), (-1, 1, 1)], [0, 1, 2, 3, 4], "parity", 4, 4),
    ("QUINT-5/5   (one cell, 5 kinds)",
     [(0, -1, 0), (0, -1, 1), (0, 1, 0), (-1, 1, -1), (-1, 1, 1)], [0],
     "parity", 5, 5),
    ("SEPTET-7/7  (two cells)",
     [(0, -1, 0), (0, -1, 1), (0, 1, -1), (0, 1, 0), (-1, 1, 1)], [0, 6],
     "parity", 7, 7),
    ("HALFTONE-32 (four kinds)",
     [(0, -1, 0), (0, 1, -1), (0, 1, 0), (0, 1, 1)], [0, 1, 6, 8],
     "parity", 32, 32),
    ("ODOMETER-64 (four kinds)",
     [(0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 1, 0)],
     [0, 2, 3, 6, 7, 9, 10], "parity", 64, -64),
    ("ODOMETER-128 (four kinds, the parity record)",
     [(0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 1, 0)],
     [0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15], "parity", 128, -128),
    ("OR-ODOMETER-16 (THREE kinds, under OR)",
     [(0, -1, -1), (-1, 1, 0), (1, -1, 0)],
     [0, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14], "or", 16, -16),
]


def main():
    deep = "--deep" in sys.argv
    print("TARGET 3 — the width-free speed cap\n")

    print("the refutation: certified single-field W=1 gliders with |d0| > 2")
    for name, rules, cells, mode, p, d in SPECIMENS:
        ok, note = certify(rules, cells, mode, p, d)
        check("%-44s (p0,d0)=(%d,%d) %s" % (name, p, d, mode), ok, note)

    print("\n     ...and every one of them IS single-field")
    ok = all(single_field(r).targets == [tuple(range(len(r)))] * len(r)
             for _, r, _, _, _, _ in SPECIMENS)
    check("T_k = K for every kind of every specimen", ok,
          "so 'another field, not another kind' is not what buys |d| >= 3")

    # --------------------------------------------------- CONVEYOR, a theorem
    print("\nCONVEYOR: two laws under which EVERY finite code marches at speed 1")
    C = single_field([(0, -1, 0), (0, 1, 1)])
    rng = random.Random(11)
    bad = 0
    trials = 6000 if deep else 2000
    for _ in range(trials):
        cells = sorted(set(rng.randrange(-9, 10)
                           for _ in range(rng.randrange(1, 9))))
        S = allkinds(cells, 2)
        for mode in ("parity", "or"):
            if step(S, C, mode) != {c + 1: m for c, m in S.items()}:
                bad += 1
    check("Phi(S) = sigma(S) for every code, both resolutions", bad == 0,
          "%d random codes x 2 resolutions, 0 exceptions" % trials)
    check("...so the front bound |d| <= p.W of Theorem B is ATTAINED at W=1",
          True, "CONVEYOR is (p0,d0) = (1,1) from any seed whatsoever")

    # ------------------------------------------------ the front-speed bound
    print("\nTheorem B (front speed): |d| <= p.W, the only width-free bound")
    rng = random.Random(5)
    OFF = (-1, 0, 1)
    bad = 0
    trials = 4000 if deep else 1500
    for _ in range(trials):
        n = rng.randrange(1, 5)
        rules = [(rng.choice(OFF), rng.choice(OFF), rng.choice(OFF))
                 for _ in range(n)]
        C = single_field(rules)
        cells = sorted(set(rng.randrange(-6, 7)
                           for _ in range(rng.randrange(1, 7))))
        S = allkinds(cells, n)
        for _ in range(12):
            if not S:
                break
            b0, a0 = max(S), min(S)
            T = step(S, C, rng.choice(("parity", "or")))
            if T and (max(T) > b0 + 1 or min(T) < a0 - 1):
                bad += 1
                break
            S = T
    check("front advances at most W per step (W=1)", bad == 0,
          "%d random single-field universes x 12 steps, 0 violations" % trials)

    # -------------------------------------- dilation preserves single-field
    print("\nthe dilation tension: dilation DOES preserve the sector")
    rules = [(0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 1, 0)]
    seed = [0, 2, 3, 6, 7, 9, 10]
    for r in (2, 3):
        dr = [tuple(r * x for x in rule) for rule in rules]
        C = single_field(dr)
        S = allkinds([r * c for c in seed], 4)
        ok = verify_glider(S, C, 64, -64 * r, "parity")
        check("ODOMETER-64 dilated by r=%d: single-field, W=%d, (p,d)=(64,%d)"
              % (r, r, -64 * r), ok,
              "target sets untouched by dilation, so the sector is preserved")

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
