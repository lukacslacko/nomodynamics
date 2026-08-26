#!/usr/bin/env python3
"""
unroll.py — the ring<->line correspondence for cross-amendment rotors.

Three experiments, all machine-checked:

(T) TILING LIFT.  A rotor on Z/m lifts to Z/(qm) by q-fold tiling with the
    SAME period p and the SAME rotation r.  (Window-1 locality: the tiled code
    has the same local neighbourhoods everywhere.)  Checked for every rotor in
    the gallery, q = 2, 3.

(Z) THE WAVE TRAIN.  The m-periodic states of Z are a Phi_Z-invariant set on
    which Phi_Z IS Phi_{Z/m} (locality, m >= 3).  So every ring rotor unrolls
    to a genuine TRAVELLING WAVE on Z of infinite support and speed r/p — the
    Anchor Theorem is not contradicted because it needs finite support.
    Checked by simulating a long tiling and reading off the displacement.

(F) THE FINITE CHUNK.  Release the rotor's laws as a finite code on Z.  This
    is the honest 'unrolling'.  Classify with xnomos on Z (glider / fixed /
    cycle / growing) — the Anchor Theorem predicts no glider.
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
from certify import to_dict, rot_tau, MODENAME       # noqa: E402


def gallery(tags):
    """Deduplicated rotor witnesses across the raw censuses."""
    seen = {}
    for tag in tags:
        path = os.path.join(RAW, tag + ".jsonl")
        if not os.path.exists(path):
            continue
        for line in open(path):
            rec = json.loads(line)
            for (p, r, j, card, rep) in rec["rotors"]:
                key = (rec["m"], p, r, j, tuple(map(tuple, rec["rules"])),
                       tuple(rec["targets"]), rec["mode"])
                if key not in seen or card < seen[key][0]:
                    seen[key] = (card, rep)
    return [(k, v) for k, v in sorted(seen.items())]


def tile(X, m, q):
    out = []
    for x in X:
        y = 0
        for t in range(q):
            y |= x << (t * m)
        out.append(y)
    return tuple(out)


def main():
    tags = sys.argv[1:] or ["own", "recip", "noninj", "cyc3", "cyc3all",
                            "super2", "own2", "own3", "super3", "big2"]
    G = gallery(tags)
    print("rotor gallery: %d distinct (m, p, rot, screw, constitution) classes"
          % len(G))

    # ---------------------------------------------------------------- (T)
    lift_ok = lift_bad = 0
    for (m, p, r, j, rules, tg, mode), (card, rep) in G:
        n = len(rules)
        X = decode(rep, n, m)
        for q in (2, 3):
            R2 = Ring(list(rules), list(tg), q * m, MODENAME[mode])
            Y = tile(X, m, q)
            Z = Y
            for _ in range(p):
                Z = R2.step(Z)
            if Z == R2.rot_state(tuple(
                    Y[(k - j) % n] for k in range(n)), r):
                lift_ok += 1
            else:
                lift_bad += 1
    print("(T) tiling lift to Z/2m and Z/3m: %d confirmed, %d failed"
          % (lift_ok, lift_bad))

    # ---------------------------------------------------------------- (Z)
    print("(Z) wave-train check on a 6-fold tiling (a proxy for Z):")
    shown = 0
    for (m, p, r, j, rules, tg, mode), (card, rep) in G:
        if r == 0 or shown >= 6 or MODENAME[mode] != "parity":
            continue
        n = len(rules)
        X = decode(rep, n, m)
        q = 6
        R2 = Ring(list(rules), list(tg), q * m, MODENAME[mode])
        Y = tile(X, m, q)
        Z = Y
        for _ in range(p):
            Z = R2.step(Z)
        want = R2.rot_state(tuple(Y[(k - j) % n] for k in range(n)), r)
        print("    m=%-3d p=%d rot=%d screw=%d speed=%s  %s  wave: %s"
              % (m, p, r, j, "%d/%d" % (r, p), rules,
                 "TRAVELS" if Z == want else "differs"))
        shown += 1

    # ---------------------------------------------------------------- (F)
    print("(F) the same laws released as a FINITE code on Z:")
    tally = Counter()
    examples = {}
    for (m, p, r, j, rules, tg, mode), (card, rep) in G:
        n = len(rules)
        X = decode(rep, n, m)
        S = to_dict(X, m)
        C = xnomos.Const(list(rules), list(tg), dim=1, modulus=None)
        res = xnomos.classify(S, C, MODENAME[mode], max_steps=600,
                              max_card=300, max_span=300)
        tally[res["kind"]] += 1
        if res["kind"] == xnomos.GLIDER:
            print("    *** GLIDER ON Z *** ", m, rules, tg, MODENAME[mode],
                  sorted(S.items()), res)
        examples.setdefault(res["kind"], (m, rules, tg, MODENAME[mode],
                                          sorted(S.items())))
    print("    ", dict(tally))
    for k, v in examples.items():
        print("      %-8s e.g. m=%d %s->%s [%s] laws %s" % (k, v[0], v[1],
                                                            v[2], v[3], v[4]))

    # ------------------------------------------------- the wrapping lemma
    print("(W) wrapping: a line code and its ring image agree until the "
          "support reaches the seam")
    import random
    rng = random.Random(4242)
    agree = 0
    for _ in range(4000):
        n = rng.randrange(1, 3)
        m = rng.randrange(8, 16)
        rules = [(rng.choice((-1, 0, 1)), rng.choice((-1, 0, 1)),
                  rng.choice((-1, 0, 1))) for _ in range(n)]
        tg = [(k + 1) % n for k in range(n)] if rng.random() < .5 else \
             [rng.randrange(n) for _ in range(n)]
        mode = rng.choice(["parity", "or", "super", "super_or"])
        S = {}
        for _ in range(rng.randrange(1, 5)):
            i = rng.randrange(2, m - 2)
            S[i] = S.get(i, 0) | (1 << rng.randrange(n))
        Cz = xnomos.Const(rules, tg, dim=1, modulus=None)
        Cr = xnomos.Const(rules, tg, dim=1, modulus=m)
        A, B = dict(S), dict(S)
        for t in range(40):
            if A and (min(A) < 1 or max(A) > m - 2):
                break
            assert {i % m: v for i, v in A.items()} == B, (rules, tg, mode, t)
            A = xnomos.step(A, Cz, mode)
            B = xnomos.step(B, Cr, mode)
        agree += 1
    print("    4000 random (constitution, code) pairs: line orbit == ring "
          "orbit at every step before the support touches the seam — %d/4000"
          % agree)


if __name__ == "__main__":
    main()
