#!/usr/bin/env python3
"""
t3_growth.py -- does the displacement per MINIMAL period grow with the span of
the code?  (The evidence that |d0| is unbounded already at window W = 1.)

For a fixed single-field class, sample codes of each span and report the
largest |d0| found.  Lower bounds only; every record is re-certified through
xnomos by t3_specimens.py.
"""
from __future__ import annotations

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from t3_fast import compile_rule, glider                       # noqa: E402
from t3_core import uvw_to_channels                            # noqa: E402


def ladder(cls, mode="parity", lmax=28, nsample=700, seed=3, step=2):
    rng = random.Random(seed)
    mt = compile_rule(cls, mode)
    for L in range(4, lmax + 1, step):
        best, arg = 0, None
        for _ in range(nsample):
            m = rng.getrandbits(L - 2)
            S = {0, L - 1} | {i + 1 for i in range(L - 2) if (m >> i) & 1}
            k, p, d, sp = glider(S, mt, max_steps=3000, max_span=400,
                                 max_card=400)
            if k == "GLIDER" and abs(d) > best:
                best, arg = abs(d), sorted(S)
        print("   span %2d : max |d0| = %5d   seed %s" % (L, best, arg),
              flush=True)


if __name__ == "__main__":
    lmax = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    for cls, mode in [((5, 7, 2), "parity"), ((5, 2, 7), "parity"),
                      ((1, 3, 2), "or")]:
        print("class %s  mode=%s  (a %d-kind constitution)"
              % (str(cls), mode, len(uvw_to_channels(*cls))), flush=True)
        ladder(cls, mode, lmax=lmax)
