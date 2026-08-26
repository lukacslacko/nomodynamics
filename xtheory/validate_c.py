#!/usr/bin/env python3
"""validate_c.py — certify the C census engine against xnomos + the xlib
reference engine.  Random constitutions x random seeds, verdict-by-verdict.

Run: python3 validate_c.py [ntrials]
"""
import random
import subprocess
import sys

from xlib import RULES1, duel
import xnomos as X
from xnomos import Const, state_of, classify

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
TMAPS = [[0, 1], [1, 0], [0, 0], [1, 1]]
BASE, MARGIN, WBITS, MAXT = 88, 20, 192, 512


def py_classify(C, S, mode):
    """Re-implement the C classifier's exact budget so verdicts are comparable."""
    dim = 1
    T = dict(S)
    seen = {}
    for t in range(MAXT):
        if not T:
            return ("EXTINCT", 0, t, 0, 0)
        lo, hi = min(T), max(T)
        if lo + BASE < MARGIN or hi + BASE >= WBITS - MARGIN:
            return ("GROWING", 0, t, 0, 0)
        nm = tuple(sorted((c - lo, m) for c, m in T.items()))
        if nm in seen:
            t0, lo0 = seen[nm]
            d, p = lo - lo0, t - t0
            if d != 0:
                return ("GLIDER", p, t0, d, 0)
            if p == 1:
                na = len(X.active_laws(T, C))
                return ("BALANCED" if na else "FIXED", 1, t0, 0, na)
            return ("CYCLE", p, t0, 0, 0)
        seen[nm] = (t, lo)
        T = X.step(T, C, mode)
    return ("UNRESOLVED", 0, MAXT, 0, 0)


def main(n=4000):
    rng = random.Random(20260826)
    cases, want = [], []
    for _ in range(n):
        r0, r1 = rng.choice(RULES1), rng.choice(RULES1)
        tm = rng.choice(TMAPS)
        span = rng.randrange(1, 7)
        masks = [rng.randrange(4) for _ in range(span)]
        masks[0] = rng.randrange(1, 4)
        masks[-1] = rng.randrange(1, 4)
        mode = rng.randrange(2)
        C = Const([r0, r1], list(tm))
        S = {i: m for i, m in enumerate(masks) if m}
        cases.append((r0, r1, tm, mode, span, masks))
        want.append(py_classify(C, S, "or" if mode else "parity"))
    inp = "\n".join(
        " ".join(map(str, list(r0) + list(r1) + list(tm) + [mode, span] + masks))
        for (r0, r1, tm, mode, span, masks) in cases)
    out = subprocess.run([HERE + "/census2", "-v"], input=inp, text=True,
                         capture_output=True).stdout.strip().split("\n")
    bad = 0
    for i, line in enumerate(out):
        p = line.split()
        got = (p[0], int(p[1]), int(p[2]), int(p[3]), int(p[4]))
        w = want[i]
        # UNRESOLVED/GROWING carry no period; compare only the class + period
        if got[0] != w[0] or (got[0] in ("CYCLE", "GLIDER") and got[1] != w[1]) \
           or (got[0] == "BALANCED" and got[4] != w[4]) \
           or (got[0] == "GLIDER" and got[3] != w[3]):
            bad += 1
            if bad <= 5:
                print("MISMATCH", cases[i], "C:", got, "PY:", w)
    print("validate_c: %d cases, %d mismatches" % (len(out), bad))

    # and a lockstep duel of xnomos vs the xlib reference engine on the same cases
    d = 0
    for (r0, r1, tm, mode, span, masks) in cases[:1200]:
        C = Const([r0, r1], list(tm))
        S = {i: m for i, m in enumerate(masks) if m}
        ok, _ = duel(S, C, 60, "or" if mode else "parity")
        if not ok:
            d += 1
    print("xnomos vs xlib reference: %d divergences in 1200 trajectories" % d)
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(int(sys.argv[1]) if len(sys.argv) > 1 else 4000) else 0)
