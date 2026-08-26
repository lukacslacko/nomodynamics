#!/usr/bin/env python3
"""specimens.py — the curated gallery for RESULTS.md, each with a certificate.

Every specimen is re-verified here through the independent xnomos.py reference
engine (dict of cell -> kind-mask) over three full periods before it is
printed, so frames and certificate come from the same run.  Witnesses are
pulled out of the raw census files by (m, p, rot, screw, constitution) so that
nothing is hand-transcribed.
"""
import ast
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("XR_RAW", os.path.join(HERE, "raw"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from xring import Ring, decode                       # noqa: E402
from certify import certify_rotor                    # noqa: E402

SYM = "XYZW"
MODENUM = {"parity": 0, "or": 1, "super": 2, "super_or": 3}


def lookup(tags, m, p, r, j, rules, targets, mode):
    for tag in tags:
        path = os.path.join(RAW, tag + ".jsonl")
        if not os.path.exists(path):
            continue
        for line in open(path):
            rec = json.loads(line)
            if (rec["m"] != m or rec["mode"] != MODENUM[mode]
                    or [tuple(x) for x in rec["rules"]] != list(rules)
                    or rec["targets"] != list(targets)):
                continue
            for (pp, rr, jj, card, rep) in rec["rotors"]:
                if (pp, rr, jj) == (p, r, j):
                    return decode(rep, len(rules), m)
    raise KeyError((m, p, r, j, rules, targets, mode))


def render(R, X):
    out = []
    for i in range(R.m):
        ks = [SYM[k] for k in range(R.n) if (X[k] >> i) & 1]
        out.append("".join(ks) if ks else ".")
    w = max(len(c) for c in out)
    return "|" + " ".join(c.ljust(w) for c in out) + "|"


def show(name, rules, targets, mode, m, X, p, r, j=0, nframes=None, note=""):
    R = Ring(list(rules), list(targets), m, mode)
    ok = certify_rotor(list(rules), list(targets), m, mode, X, p, r, j)
    d = min(r % m, (-r) % m) if r else 0
    lc = ("no spatial motion" if r == 0 else
          "TRANSPORTING (%d <= 2p = %d)" % (d, 2 * p) if d <= 2 * p else
          "barber pole (%d > 2p = %d)" % (d, 2 * p))
    print("\n### %s" % name)
    print("constitution: " + "   ".join(
        "%s:(%d,%d,%d)->%s" % (SYM[k], *rules[k], SYM[targets[k]])
        for k in range(len(rules))) + "     [%s, ring Z/%d]" % (mode, m))
    print("Phi^%d(S) = rot_%d%s(S)   laws = %d   %s"
          % (p, r, "" if j == 0 else " o tau^%d" % j, R.card(X), lc))
    print("certificate: %s" % ("VERIFIED over 3 full periods by the xnomos "
                               "reference engine" if ok else "FAILED"))
    if note:
        print(note)
    nf = nframes or (2 * p + 1)
    Y = X
    for t in range(nf):
        print("  t=%-2d %s" % (t, render(R, Y)))
        Y = R.step(Y)
    assert ok, name
    return X


def main():
    T = ["own", "own2", "own3", "recip", "noninj", "cyc3", "cyc3all",
         "super2", "super3", "big2", "goe"]

    X = lookup(T, 4, 1, 2, 0, [(-1, 1, -1), (0, -1, 0)], [1, 0], "parity")
    show("Q-4 — the smallest rotor ring in nomodynamics "
         "(own-kind needs m >= 6)",
         [(-1, 1, -1), (0, -1, 0)], [1, 0], "parity", 4, X, 1, 2,
         note="Three laws on four cells; every step the whole code half-turns.")

    X = lookup(T, 4, 3, 2, 0, [(0, -1, 0), (0, -1, 1)], [1, 0], "parity")
    show("Q-4b — the same ring, a three-step relay (period-6 orbit)",
         [(0, -1, 0), (0, -1, 1)], [1, 0], "parity", 4, X, 3, 2)

    X = lookup(T, 6, 1, 2, 0, [(-1, -1, -1), (0, 1, -1)], [1, 0], "parity")
    show("R-6 — a four-law wave at rot 2 per step",
         [(-1, -1, -1), (0, 1, -1)], [1, 0], "parity", 6, X, 1, 2)

    X = lookup(T, 6, 1, 2, 1, [(0, 1, -1)] * 3, [1, 2, 0], "parity")
    show("K-6 — THE KIND RELAY: three kinds hand the packet forward",
         [(0, 1, -1)] * 3, [1, 2, 0], "parity", 6, X, 1, 2, 1, nframes=4,
         note="Phi = rot_2 o tau.  Each step the packet advances two cells AND\n"
              "every law becomes the next kind in the amendment cycle; after\n"
              "three steps tau^3 = id and rot_6 = id, so the code has gone\n"
              "once round the ring and is back.  Two cells per step is exactly\n"
              "the light-cone speed: this packet is really carried, not a\n"
              "phase illusion.  Own-kind nomodynamics has no such object.")

    X = lookup(T, 3, 1, 0, 2, [(0, -1, 0)] * 3, [1, 2, 0], "parity")
    show("D-3 — the doctrinal rotor: the code stands still, the KINDS rotate",
         [(0, -1, 0)] * 3, [1, 2, 0], "parity", 3, X, 1, 0, 2, nframes=4,
         note="c = 0 everywhere, so nothing can move in space; what circulates\n"
              "is which KIND of law holds the seat.  Exists on every ring, odd\n"
              "or even, from two laws.")

    for line in open(os.path.join(HERE, "sat_odd.log")):
        if "ROTOR:" not in line:
            continue
        b = line.split("ROTOR:", 1)[1].strip()
        mm = re.match(r"(\(\(.*?\)\)) (\(.*?\)) (\w+) m=(\d+) p=(\d+) "
                      r"r=(\d+) X=(\[\[.*\]\])", b)
        rules = list(ast.literal_eval(mm.group(1)))
        tg = list(ast.literal_eval(mm.group(2)))
        mode = mm.group(3)
        m, p, r = int(mm.group(4)), int(mm.group(5)), int(mm.group(6))
        Xl = ast.literal_eval(mm.group(7))
        X = tuple(sum(bb << i for i, bb in enumerate(row)) for row in Xl)
        if p == 1:
            show("O-15 — THE FIRST ROTOR ON AN ODD RING",
                 rules, tg, mode, m, X, p, r,
                 note="Both kinds amend kind X (non-injective targeting).\n"
                      "Phi is exactly the rotation by m/3 = 5, so the whole\n"
                      "orbit is the rotation orbit of one code: a 3-cycle that\n"
                      "is a rigid turn of the ring.  Own-kind nomodynamics has\n"
                      "no rotor on any odd ring at all (complete m <= 19; SAT\n"
                      "decision m <= 31).")
            break
    for line in open(os.path.join(HERE, "sat_odd.log")):
        if "ROTOR:" not in line:
            continue
        b = line.split("ROTOR:", 1)[1].strip()
        mm = re.match(r"(\(\(.*?\)\)) (\(.*?\)) (\w+) m=(\d+) p=(\d+) "
                      r"r=(\d+) X=(\[\[.*\]\])", b)
        rules = list(ast.literal_eval(mm.group(1)))
        tg = list(ast.literal_eval(mm.group(2)))
        mode = mm.group(3)
        m, p, r = int(mm.group(4)), int(mm.group(5)), int(mm.group(6))
        if tg != [1, 0] or mode != "parity":
            continue
        Xl = ast.literal_eval(mm.group(7))
        X = tuple(sum(bb << i for i, bb in enumerate(row)) for row in Xl)
        show("O-15b — the reciprocal-amendment odd-ring rotor",
             rules, tg, mode, m, X, p, r)
        break


if __name__ == "__main__":
    main()
