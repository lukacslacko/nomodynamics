#!/usr/bin/env python3
"""
t3_dilation.py -- the Dilation "tension", resolved and machine-checked.

THE APPARENT TENSION.  The Dilation Theorem sends a (W,p,d) glider to an
(rW, p, rd) glider, so displacement is unbounded; yet the single-field sector
carries a cap "|d| <= 2 ... at any width".  Three escapes were on the table:

   (E1) dilation does not preserve the single-field sector;
   (E2) the dilated object is not a glider of the same kind;
   (E3) the "three kinds at W=2 reaching |d|=5" specimen is not single-field.

This script checks all three.  ALL THREE ARE FALSE.  The real resolution is an
EQUIVOCATION ON THE WORD "WIDTH":

   * in "window width W" it means the offset radius of the rules;
   * in "at any width", "width-unbounded decider", "the box is too narrow"
     it means the SPAN of the pattern.

The published cap is a statement at FIXED WINDOW W = 1, over patterns of
UNBOUNDED SPAN.  The Dilation Theorem moves the window, so it never bears on
that statement at all.  It is only Corollary D1's phrasing
("no W-independent cap on |d| can hold") that collides with the loose reading
of the cap, and D1 is about a family of DIFFERENT windows.

Everything below is executed against the reference engine xnomos.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import xnomos                                                # noqa: E402
from t3_core import uvw_to_channels, to_xnomos               # noqa: E402


def dilate_const(rules, targets, r):
    return ([tuple(r * x for x in ru) for ru in rules], list(targets))


def window(rules):
    return max(max(abs(x) for x in ru) for ru in rules)


def is_single_field(targets, n):
    return all(tuple(sorted(t)) == tuple(range(n)) for t in targets)


def report(title):
    print("\n" + title)
    print("-" * len(title))


def main():
    ok = 0

    # ---------------------------------------------------------------- (E1)
    report("(E1)  Does dilation preserve the single-field sector?")
    mirror = [(0, 1, -1), (0, -1, 1)]
    tgt = [(0, 1), (0, 1)]
    seed25 = {c: 3 for c in [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16,
                             18, 19, 20, 21]}
    C = xnomos.Const(mirror, tgt)
    assert xnomos.verify_glider(seed25, C, 5, 2, "parity")
    print("  MIRROR-2/5 at W=%d: single-field=%s, (p,d)=(5,2) verified"
          % (window(mirror), is_single_field(tgt, 2)))
    for r in (2, 3, 4):
        ru, tg = dilate_const(mirror, tgt, r)
        Cr = xnomos.Const(ru, tg)
        Sr = {r * c: 3 for c in seed25}
        v = xnomos.verify_glider(Sr, Cr, 5, 2 * r, "parity")
        cl = xnomos.classify(dict(Sr), Cr, "parity", max_steps=200)
        print("  r=%d -> W=%d, single-field=%s, (p,d)=(5,%d) verified=%s, "
              "classify: %s p=%s d=%s"
              % (r, window(ru), is_single_field(tg, 2), 2 * r, v,
                 cl["kind"], cl.get("period"), cl.get("displacement")))
        assert v and is_single_field(tg, 2) and window(ru) == r
        assert cl["kind"] == "GLIDER" and cl["period"] == 5 \
            and cl["displacement"] == 2 * r
        ok += 1
    print("  VERDICT: dilation PRESERVES single-fieldness (targets untouched)")
    print("           and MULTIPLIES the window: W -> rW.  (E1) is FALSE.")

    # ---------------------------------------------------------------- (E2)
    report("(E2)  Is the dilated object a glider of the same kind, with the "
           "same MINIMAL period?")
    print("  xnomos.classify reports the minimal period of the normalised")
    print("  orbit; every row above returned period 5 and displacement 2r,")
    print("  so the generator of G(S) goes (p0,d0) -> (p0, r*d0) exactly.")
    print("  VERDICT: (E2) is FALSE -- dilation is a faithful d0-multiplier.")

    # ---------------------------------------------------------------- (E3)
    report("(E3)  Is TRIAD (n=3, W=2, |d|=5) single-field?")
    rules3 = [(1, -1, 0), (0, -2, 1), (0, -2, 2)]
    tg3 = [(0, 1, 2)] * 3
    C3 = xnomos.Const(rules3, tg3)
    v1 = xnomos.verify_glider({0: 7}, C3, 3, 5, "parity")
    v2 = xnomos.verify_glider({0: 7}, C3, 2, 3, "or")
    cl1 = xnomos.classify({0: 7}, C3, "parity", max_steps=200)
    cl2 = xnomos.classify({0: 7}, C3, "or", max_steps=200)
    print("  TRIAD  W=%d  single-field=%s" % (window(rules3),
                                              is_single_field(tg3, 3)))
    print("  parity: (3,5) verified=%s   classify: %s p=%s d=%s"
          % (v1, cl1["kind"], cl1.get("period"), cl1.get("displacement")))
    print("  or    : (2,3) verified=%s   classify: %s p=%s d=%s"
          % (v2, cl2["kind"], cl2.get("period"), cl2.get("displacement")))
    assert v1 and v2 and is_single_field(tg3, 3) and window(rules3) == 2
    print("  VERDICT: TRIAD IS single-field, at W=2.  (E3) is FALSE.")
    ok += 1

    # ------------------------------------------------- the real resolution
    report("THE RESOLUTION: 'width' is used for two different things")
    print("  The cap was decided by a subshift-of-finite-type decider whose")
    print("  own docstring says: 'with NO bound on the width of the PATTERN'.")
    print("  Every table carrying the cap is headed 'W = 1'.  So the claim is")
    print("      for the FIXED window W = 1, over patterns of ANY SPAN.")
    print("  Dilation changes the window, so it cannot contradict it:")
    print("      Corollary D1  maxdisp(n, rW) >= r * maxdisp(n, W)")
    print("  relates DIFFERENT windows.  There is no tension, only two senses")
    print("  of one word.")

    # -------------------------------------------- and the cap itself is false
    report("BUT: the W=1 cap |d| <= 2 is itself FALSE (see t3_sweep.py)")
    specs = [((4, 6, 5), [0, 1], 3, 3, "4 kinds, one field"),
             ((1, 6, 7), [1], 5, 3, "5 kinds, one field, ONE-CELL seed"),
             ((4, 6, 7), [0], 5, 5, "5 kinds, one field, ONE-CELL seed"),
             ((5, 6, 7), [0, 6], 7, 7, "5 kinds, one field, TWO-CELL seed")]
    for cls, seed, p, d, note in specs:
        ch = uvw_to_channels(*cls)
        n = len(ch)
        Cn = to_xnomos(ch, n)
        S = {c: (1 << n) - 1 for c in seed}
        v = xnomos.verify_glider(S, Cn, p, d, "parity")
        cl = xnomos.classify(dict(S), Cn, "parity", max_steps=300)
        assert v and cl["kind"] == "GLIDER" and cl["period"] == p \
            and cl["displacement"] == d, (cls, cl)
        print("  W=1 %-42s (p0,d0)=(%d,%d)  rules=%s  seed=%s  OK"
              % (note, p, d, ch, seed))
        ok += 1

    report("Dilating the W=1 record raises every window's lower bound")
    cls, seed, p, d = (5, 6, 7), [0, 6], 7, 7
    ch = uvw_to_channels(*cls)
    n = len(ch)
    for r in (2, 3):
        ru = [tuple(r * x for x in c) for c in ch]
        Cr = xnomos.Const(ru, [tuple(range(n))] * n)
        Sr = {r * c: (1 << n) - 1 for c in seed}
        v = xnomos.verify_glider(Sr, Cr, p, r * d, "parity")
        cl = xnomos.classify(dict(Sr), Cr, "parity", max_steps=300)
        print("  r=%d: W=%d, n=%d single field, (p0,d0)=(%d,%d) verified=%s "
              "classify p=%s d=%s"
              % (r, r, n, p, r * d, v, cl.get("period"),
                 cl.get("displacement")))
        assert v and cl["period"] == p and cl["displacement"] == r * d
        ok += 1
    print("  => single-field maxdisp >= 7 (W=1), >= 14 (W=2), >= 21 (W=3),")
    print("     which already dominates the previously reported")
    print("     'n=3 reaches |d|=5 at W=2' and '|d|=14 at W=3'.")

    print("\nall %d dilation checks passed" % ok)


if __name__ == "__main__":
    main()
