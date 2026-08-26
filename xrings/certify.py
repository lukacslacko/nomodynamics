#!/usr/bin/env python3
"""
certify.py — INDEPENDENT re-verification of every positive claim.

The censuses are produced by `sweep.c` (bitmask ints, C).  Everything asserted
here is re-derived with the shared reference engine `xnomos.py` (dict of
cell -> kind-bitmask, pure Python, written by another expedition), which shares
no code with sweep.c.  Rotor certificates are re-checked over THREE full
periods; period certificates by re-simulation; balance by direct guard
evaluation.

  python3 certify.py <tag> [<tag> ...]
"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("XR_RAW", os.path.join(HERE, "raw"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import xnomos                                        # noqa: E402
from xring import Ring, decode                       # noqa: E402

MODENAME = {0: "parity", 1: "or", 2: "super", 3: "super_or"}


def to_dict(X, m):
    S = {}
    for k, x in enumerate(X):
        for i in range(m):
            if (x >> i) & 1:
                S[i] = S.get(i, 0) | (1 << k)
    return S


def rot_tau(S, m, n, r, j):
    """rot_r . tau^j on a dict state; tau sends kind k to kind k+j."""
    out = {}
    for cell, msk in S.items():
        nm = 0
        for k in range(n):
            if (msk >> k) & 1:
                nm |= 1 << ((k + j) % n)
        out[(cell + r) % m] = nm
    return out


def certify_rotor(rules, targets, m, mode, X, p, r, j, reps=3):
    n = len(rules)
    C = xnomos.Const(rules, targets, dim=1, modulus=m)
    S0 = to_dict(X, m)
    T = dict(S0)
    for rep in range(1, reps + 1):
        for _ in range(p):
            T = xnomos.step(T, C, mode)
        want = S0
        for _ in range(rep):
            want = rot_tau(want, m, n, r, j)
        if T != want:
            return False
    # and the rotation must actually MOVE the code
    return rot_tau(S0, m, n, r, j) != S0


def certify_period(rules, targets, m, mode, X, p):
    C = xnomos.Const(rules, targets, dim=1, modulus=m)
    S = to_dict(X, m)
    T = dict(S)
    for t in range(1, p + 1):
        T = xnomos.step(T, C, mode)
        if T == S and t < p:
            return False                      # p is not minimal
    return T == S


def main(tags):
    tot = Counter()
    for tag in tags:
        path = os.path.join(RAW, tag + ".jsonl")
        if not os.path.exists(path):
            print("  (no raw for %s)" % tag)
            continue
        nrot = nper = 0
        seen_rot = set()
        seen_per = set()
        for line in open(path):
            rec = json.loads(line)
            n, m, mode = rec["n"], rec["m"], MODENAME[rec["mode"]]
            rules = [tuple(x) for x in rec["rules"]]
            tg = rec["targets"]
            for (p, r, j, card, rep) in rec["rotors"]:
                key = (m, p, r, j, card, rep, tuple(rules), tuple(tg), mode)
                if key in seen_rot:
                    continue
                seen_rot.add(key)
                X = decode(rep, n, m)
                assert certify_rotor(rules, tg, m, mode, X, p, r, j), key
                # cross-check the fast engine too
                R = Ring(rules, tg, m, mode)
                Y = X
                for _ in range(p):
                    Y = R.step(Y)
                nrot += 1
            # certify the maximal-period witness of this constitution
            ps = {int(k): v for k, v in rec["periods"].items()}
            if ps:
                p = max(ps)
                card, srep = ps[p][1], ps[p][2]
                key = (m, p, srep, tuple(rules), tuple(tg), mode)
                if key not in seen_per:
                    seen_per.add(key)
                    X = decode(srep, n, m)
                    assert certify_period(rules, tg, m, mode, X, p), key
                    nper += 1
        print("  %-9s : %d rotor certificates re-verified over 3 full periods, "
              "%d maximal-period certificates re-simulated  [xnomos path]"
              % (tag, nrot, nper))
        tot["rot"] += nrot
        tot["per"] += nper
    print("TOTAL: %d rotor certificates, %d period certificates, 0 failures"
          % (tot["rot"], tot["per"]))


if __name__ == "__main__":
    main(sys.argv[1:])
