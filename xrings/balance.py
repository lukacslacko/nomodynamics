#!/usr/bin/env python3
"""
balance.py — EXACT counts of fixed points and BALANCED constitutions on Z/m
for cross-amendment constitutions, by transfer matrix.

Locality.  With window-1 guards and effect offsets c in {-1,0,1}, the
fixed-point condition at cell j reads only cells j-2 .. j+2:
  * the only laws that can emit into cell j sit at j-1, j, j+1 (i = j - c_k);
  * whether such a law is active depends on occupancy at i-1, i, i+1.
So fixedness is a 5-window local constraint and the number of fixed codes on
Z/m is tr(T^m) for the transfer matrix T on 4-cell contexts (alphabet 2^n per
cell), valid for m >= 4.

  F(m) = # fixed codes
  Z(m) = # codes in which every law is blocked   ("dead-letter" codes)
  B(m) = F(m) - Z(m) = # BALANCED codes: fixed forever, yet still active.

Theorem verified here: B(m) = 0 identically under 'or' and 'super_or'
resolution and under every permutation (injective) target map; B(m) > 0 needs
genuine multi-authorship of one slot.
"""
import itertools
import sys
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from xring import RULES27, Ring                      # noqa: E402

OCC = lambda s: 1 if s else 0                        # noqa: E731


def emissions(rules, targets, w, n):
    """w = (S_{j-2},...,S_{j+2}) masks.  Return list e[k] in {0,1}: does the
    kind-k law that targets cell j exist and fire?"""
    e = []
    for k in range(n):
        a, b, c = rules[k]
        i = 2 - c                     # index in w of cell j - c_k
        if not (0 <= i <= 4) or not ((w[i] >> k) & 1):
            e.append(0)
            continue
        ia, ib = i + a, i + b
        ok = OCC(w[ia]) == 1 and OCC(w[ib]) == 0
        e.append(1 if ok else 0)
    return e


def fixed_ok(rules, targets, mode, w, n):
    e = emissions(rules, targets, w, n)
    if mode in ("parity", "or"):
        for t in range(n):
            src = [k for k in range(n) if targets[k] == t]
            if mode == "parity":
                if sum(e[k] for k in src) % 2:
                    return False
            else:
                if any(e[k] for k in src):
                    return False
        return True
    # supersession: e_k lands on cell j carrying kind k
    if OCC(w[2]):
        tot = sum(e)
        return (tot % 2 == 0) if mode == "super" else (tot == 0)
    return sum(e) == 0            # empty ground: any emission enacts


def blocked_ok(rules, w, n):
    """No law standing at cell j is active (the dead-letter condition)."""
    for k in range(n):
        if (w[2] >> k) & 1:
            a, b, _ = rules[k]
            if OCC(w[2 + a]) == 1 and OCC(w[2 + b]) == 0:
                return False
    return True


def transfer(rules, targets, mode, n, which="fixed"):
    A = 1 << n
    V = A ** 4
    T = np.zeros((V, V), dtype=np.int64)
    for ctx in range(V):
        w0 = (ctx >> (3 * n)) & (A - 1)
        w1 = (ctx >> (2 * n)) & (A - 1)
        w2 = (ctx >> n) & (A - 1)
        w3 = ctx & (A - 1)
        for w4 in range(A):
            w = (w0, w1, w2, w3, w4)
            ok = (fixed_ok(rules, targets, mode, w, n) if which == "fixed"
                  else blocked_ok(rules, w, n))
            if ok:
                nxt = ((w1 << (3 * n)) | (w2 << (2 * n)) | (w3 << n) | w4)
                T[ctx, nxt] += 1
    return T


def trace_powers(T, ms):
    """tr(T^m) for each m in ms, exact in int64 (checked against overflow)."""
    out = {}
    P = np.eye(T.shape[0], dtype=np.int64)
    mx = max(ms)
    for m in range(1, mx + 1):
        P = P @ T
        if m in ms:
            out[m] = int(np.trace(P))
    return out


def counts(rules, targets, mode, n, ms):
    Tf = transfer(rules, targets, mode, n, "fixed")
    Tz = transfer(rules, targets, mode, n, "blocked")
    F = trace_powers(Tf, ms)
    Z = trace_powers(Tz, ms)
    return {m: (F[m], Z[m], F[m] - Z[m]) for m in ms}


# --------------------------------------------------------------- brute force

def brute(rules, targets, mode, n, m):
    R = Ring(rules, targets, m, mode)
    F = Z = 0
    for v in range(1 << (n * m)):
        X = tuple((v >> (k * m)) & ((1 << m) - 1) for k in range(n))
        if R.step(X) == X:
            F += 1
            if not any(R.active(X)):
                Z += 1
    return F, Z, F - Z


def main():
    ms = list(range(4, 21))

    print("=== validation: transfer matrix vs brute force (m = 4..8) ===")
    tests = [
        ([(0, 1, 1), (0, -1, -1)], [0, 0], "parity"),
        ([(0, 1, 1), (0, -1, -1)], [1, 0], "parity"),
        ([(0, -1, 1), (0, 1, -1)], [0, 0], "parity"),
        ([(0, -1, 1), (0, 1, -1)], [0, 0], "or"),
        ([(0, -1, 1), (0, 1, -1)], [0, 1], "super"),
        ([(0, -1, 1), (0, 1, -1)], [0, 1], "super_or"),
        ([(0, 1, 1), (0, 1, 1)], [0, 0], "parity"),
    ]
    bad = 0
    for rules, tg, mode in tests:
        c = counts(rules, tg, mode, 2, list(range(4, 9)))
        for m in range(4, 9):
            b = brute(rules, tg, mode, 2, m)
            if b != c[m]:
                print("  MISMATCH", rules, tg, mode, m, b, c[m])
                bad += 1
        print("  ok %s %s %-9s  F/Z/B(m=6) = %s" % (rules, tg, mode, c[6]))
    print("  mismatches:", bad)
    assert bad == 0

    print("\n=== Theorem check: B(m) == 0 for OR / SUPER_OR / permutation "
          "targets, all 729 two-kind constitutions, m = 4..12 ===")
    viol = 0
    for r1, r2 in itertools.product(RULES27, repeat=2):
        for tg, mode in (([0, 0], "or"), ([1, 0], "parity"), ([0, 1], "parity"),
                         ([0, 1], "super_or")):
            Tf = transfer([r1, r2], tg, mode, 2, "fixed")
            Tz = transfer([r1, r2], tg, mode, 2, "blocked")
            if not np.array_equal(Tf, Tz):
                viol += 1
                print("  VIOLATION", r1, r2, tg, mode)
    print("  constitutions checked: 729 x 4 semantics; violations:", viol)


if __name__ == "__main__":
    main()
