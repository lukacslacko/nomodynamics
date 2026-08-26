#!/usr/bin/env python3
"""
balwitness.py — the ring census of BALANCED constitutions: which two-kind
constitutions admit them, the minimal balanced code, and exact counts B(m).

A code is BALANCED if Phi(S) = S while at least one law is still active:
a constitution that is alive but permanently deadlocked.  Own-kind
nomodynamics forbids these (Dead Letter Theorem); here we locate them exactly.
"""
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from xring import Ring, RULES27, decode              # noqa: E402
import xnomos                                        # noqa: E402
from balance import counts                           # noqa: E402
from certify import to_dict                          # noqa: E402


def balanced_states(rules, targets, mode, m, want=None):
    R = Ring(rules, targets, m, mode)
    out = []
    for v in range(1 << (2 * m)):
        X = decode(v, 2, m)
        if R.step(X) == X and any(R.active(X)):
            out.append(X)
            if want and len(out) >= want:
                break
    return out


def verify_via_xnomos(rules, targets, mode, m, X):
    C = xnomos.Const(rules, targets, dim=1, modulus=m)
    S = to_dict(X, m)
    return xnomos.verify_balanced(S, C, mode)


def main():
    print("=== 1. which two-kind constitutions admit balance? "
          "(targets [0,0], parity) ===")
    admits = []
    for r1, r2 in itertools.product(RULES27, repeat=2):
        c = counts([r1, r2], [0, 0], "parity", 2, [8])
        if c[8][2] > 0:
            admits.append((r1, r2))
    print("  %d of 729 rule pairs admit balanced codes on Z/8" % len(admits))
    from collections import Counter
    live = Counter()
    for r1, r2 in admits:
        live[(r1[1] != 0 and r1[0] != r1[1], r2[1] != 0 and r2[0] != r2[1])] += 1
    print("  both rules live / other:", dict(live))
    ceq = Counter((r1[2] - r2[2]) % 3 for r1, r2 in admits)
    print("  distribution of c_0 - c_1 over the admitting pairs:", dict(ceq))
    guards = Counter(((r1[0], r1[1]), (r2[0], r2[1])) for r1, r2 in admits)
    print("  distinct guard pairs (a,b) among them: %d" % len(guards))
    print("  guard pairs:", sorted(guards)[:12])

    print("\n=== 2. the minimal balanced code on a ring ===")
    best = None
    for (r1, r2) in admits:
        for m in (4, 5, 6):
            for X in balanced_states([r1, r2], [0, 0], "parity", m, want=400):
                card = bin(X[0]).count("1") + bin(X[1]).count("1")
                if best is None or (card, m) < (best[0], best[1]):
                    best = (card, m, r1, r2, X)
    card, m, r1, r2, X = best
    R = Ring([r1, r2], [0, 0], m, "parity")
    print("  minimum law count = %d, smallest ring m = %d" % (card, m))
    print("  constitution: kind0=%s kind1=%s, both amending kind 0" % (r1, r2))
    print("  code: %s   active laws: %d"
          % (R.render(X), sum(bin(a).count("1") for a in R.active(X))))
    assert verify_via_xnomos([r1, r2], [0, 0], "parity", m, X)
    print("  re-verified by xnomos.verify_balanced: OK")

    print("\n  all 2-law balanced codes with 2 kinds on Z/5 (complete):")
    shown = 0
    for (r1, r2) in admits:
        for X in balanced_states([r1, r2], [0, 0], "parity", 5, want=200):
            if bin(X[0]).count("1") + bin(X[1]).count("1") == 2 and shown < 8:
                R = Ring([r1, r2], [0, 0], 5, "parity")
                print("    %s  kind0=%s kind1=%s -> both amend kind 0"
                      % (R.render(X), r1, r2))
                shown += 1

    print("\n=== 3. exact B(m) for representative balanced constitutions ===")
    ms = list(range(4, 21))
    for rules, tg, mode, name in [
            ([(0, 1, 1), (0, -1, -1)], [0, 0], "parity", "two-chamber veto"),
            ([(0, 1, 1), (0, 1, 1)], [0, 0], "parity", "twin chambers"),
            ([(0, -1, 1), (0, 1, -1)], [0, 1], "super", "supersession pair")]:
        c = counts(rules, tg, mode, 2, ms)
        print("  %-18s %s -> %s [%s]" % (name, rules, tg, mode))
        print("     m :  " + "".join("%12d" % m for m in ms[:8]))
        print("     F :  " + "".join("%12d" % c[m][0] for m in ms[:8]))
        print("     Z :  " + "".join("%12d" % c[m][1] for m in ms[:8]))
        print("     B :  " + "".join("%12d" % c[m][2] for m in ms[:8]))
        print("     B(20) = %d   B/F(20) = %.4f"
              % (c[20][2], c[20][2] / c[20][0]))

    print("\n=== 4. balance is impossible under OR / super_or / permutation "
          "targeting: 4 x 729 x m=4..12 exact counts, done in balance.py ===")


if __name__ == "__main__":
    main()
