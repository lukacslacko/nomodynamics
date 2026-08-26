#!/usr/bin/env python3
"""
gallery.py — the rotor gallery with ASCII frames, plus the two structural
tests the pre-registration asked for:

  (P5) the natural rotation speed of an L-cycle constitution is s = sum of the
       c's around the cycle, per L steps: does r/p == s/L?
  (LC) LIGHT CONE.  With window-1 guards and |c| <= 1 the state at cell j at
       time t+1 depends only on cells j-2..j+2 at time t, so information moves
       at most 2 cells/step.  A rotor with min(r, m-r) > 2p therefore carries
       NO causal transport: it is a *barber pole* — the orbit has a rotational
       symmetry that no signal realises.  Rotors with min(r, m-r) <= 2p are
       TRANSPORTING.
"""
import json
import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("XR_RAW", os.path.join(HERE, "raw"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from xring import Ring, decode                       # noqa: E402
from certify import MODENAME, certify_rotor          # noqa: E402
from unroll import gallery                           # noqa: E402


def frames(rules, targets, m, mode, X, steps):
    R = Ring(list(rules), list(targets), m, mode)
    out = []
    Y = X
    for t in range(steps):
        out.append("t=%-2d %s" % (t, R.render(Y)))
        Y = R.step(Y)
    return out


def main():
    tags = sys.argv[1:] or ["own", "own2", "own3", "recip", "noninj", "cyc3",
                            "cyc3all", "super2", "super3", "big2"]
    G = gallery(tags)
    print("gallery size: %d classes" % len(G))

    # -------------------------------------------------------------- (P5)
    ok = bad = na = 0
    for (m, p, r, j, rules, tg, mode), (card, rep) in G:
        L = len(rules)
        perm = sorted(tg) == list(range(L))
        cyclic = all(tg[k] == (k + 1) % L for k in range(L))
        if not (perm and cyclic and L > 1):
            na += 1
            continue
        s = sum(rr[2] for rr in rules) % m
        # prediction: rotation s per L steps, i.e. r/p == s/L mod m
        if (r * L - s * p) % m == 0:
            ok += 1
        else:
            bad += 1
    print("(P5) sum-of-c prediction on L-cycle constitutions: "
          "%d rotors match r*L == s*p (mod m), %d do not, %d not applicable"
          % (ok, bad, na))

    # -------------------------------------------------------------- (LC)
    lc = Counter()
    for (m, p, r, j, rules, tg, mode), (card, rep) in G:
        d = min(r % m, (-r) % m)
        lc["transporting" if d <= 2 * p else "barber-pole"] += 1
    print("(LC) light cone: %s" % dict(lc))
    print("     (a transporting rotor really carries its packet round the "
          "ring; a barber pole cannot — no signal moves that fast)")

    # ------------------------------------------------------------ gallery
    print("\n=== ROTOR GALLERY (minimum-cardinality witness per class) ===")
    picks = []
    seenkey = set()
    for (m, p, r, j, rules, tg, mode), (card, rep) in G:
        L = len(rules)
        perm = sorted(tg) == list(range(L))
        crossed = not all(tg[k] == k for k in range(L))
        d = min(r % m, (-r) % m)
        key = (m, p, r, j, L, crossed, MODENAME[mode])
        if key in seenkey:
            continue
        seenkey.add(key)
        picks.append((card, m, p, r, j, rules, tg, mode, rep, crossed,
                      d <= 2 * p))
    picks.sort(key=lambda x: (x[1], x[0], x[2]))
    shown = 0
    for card, m, p, r, j, rules, tg, mode, rep, crossed, transp in picks:
        if not crossed or shown >= 22:
            continue
        X = decode(rep, len(rules), m)
        assert certify_rotor(list(rules), list(tg), m, MODENAME[mode], X,
                             p, r, j)
        print("\n-- m=%d  period=%d  rot=%d  screw=%d  laws=%d  %s  %s"
              % (m, p, r, j, card, MODENAME[mode],
                 "TRANSPORTING" if transp else "barber-pole"))
        print("   constitution: %s" % " ".join(
            "%s:(%d,%d,%d)->%s" % ("XYZW"[k], *rules[k], "XYZW"[tg[k]])
            for k in range(len(rules))))
        for line in frames(rules, tg, m, MODENAME[mode], X,
                           min(2 * p * (m // math.gcd(r, m) if r else 1) + 1,
                               9)):
            print("   " + line)
        shown += 1


if __name__ == "__main__":
    main()
