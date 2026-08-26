#!/usr/bin/env python3
"""
sunset.py — nomodynamics under IMPERMANENCE.

Chapters one to three all assume a law stays in force until something repeals
it.  That assumption is doing more work than anyone noticed: the semantic sweep
of chapter two found that *what forbids motion on the line is permanence*, not
own-kind targeting.  Here permanence is dropped.

    SUNSET-BY-DEFAULT.  A law lapses unless it is re-enacted.  Formally, with
    lifetime tau >= 1: a placed law survives a step if it is enacted by some
    active law this step, or if it has been standing for fewer than tau steps
    since its last enactment.  tau = 1 is the pure form: only what is enacted
    now stands next.

Effects are ENACTMENTS, not toggles: an active law of kind k at i enacts every
kind of T_k at i + c_k.  (Repeal has no separate meaning here — to repeal is to
stop re-enacting.)  Guards are as in `xnomos`: occupancy or citation.

Reading it aloud: *every provision carries a sunset clause, and the only way a
statute book persists is by continually re-enacting itself.*
"""

from __future__ import annotations

import itertools
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xnomos import Const, state_of, laws, card, enabled, RULES1   # noqa: E402


# ------------------------------------------------------------------ the update

def step_sunset(S, C, tau=1, ages=None):
    """One step under sunset-by-default.

    S    : {cell: bitmask}
    ages : {(cell, kind): steps since last enactment}; None starts them at 0.
    Returns (S', ages').
    """
    if ages is None:
        ages = {(cell, k): 0 for cell, k in laws(S)}
    enacted = {}
    for cell, k in laws(S):
        if not enabled(S, C, cell, k):
            continue
        j = C.add(cell, C.rules[k][2])
        for t in C.targets[k]:
            enacted[(j, t)] = True
    out, new_ages = {}, {}
    for (j, t) in enacted:
        out[j] = out.get(j, 0) | (1 << t)
        new_ages[(j, t)] = 0
    for cell, k in laws(S):                     # survivors still within tau
        if (cell, k) in enacted:
            continue
        age = ages.get((cell, k), 0) + 1
        if age < tau:
            out[cell] = out.get(cell, 0) | (1 << k)
            new_ages[(cell, k)] = age
    return out, new_ages


def run(S, C, steps, tau=1):
    S, ages = dict(S), None
    hist = [dict(S)]
    for _ in range(steps):
        S, ages = step_sunset(S, C, tau, ages)
        hist.append(dict(S))
    return hist


# ------------------------------------------------------------- classification

EXTINCT, FIXED, CYCLE, GLIDER, GROWING, UNRESOLVED = (
    "EXTINCT", "FIXED", "CYCLE", "GLIDER", "GROWING", "UNRESOLVED")


def _norm(S):
    if not S:
        return (), None
    lo = min(S)
    return tuple(sorted((c - lo, m) for c, m in S.items())), lo


def classify_sunset(S0, C, tau=1, max_steps=400, max_card=300, max_span=300):
    """Run and certify.  tau > 1 states carry ages, so recurrence is checked on
    the (state, ages) pair; for tau = 1 the age map is always empty."""
    S, ages = dict(S0), None
    seen, seen_norm = {}, {}
    for t in range(max_steps):
        if not S:
            return {"kind": EXTINCT, "t": t}
        key = (tuple(sorted(S.items())),
               tuple(sorted(ages.items())) if (tau > 1 and ages) else ())
        if key in seen:
            p = t - seen[key]
            return {"kind": FIXED if p == 1 else CYCLE, "period": p,
                    "t": seen[key], "card": card(S)}
        seen[key] = t
        # translation certificate: normalise the AGE map along with the state,
        # or a glider with tau > 1 (whose tail carries ages) is invisible.
        nm, anchor = _norm(S)
        if anchor is not None:
            am = tuple(sorted(((c - anchor, k), v)
                              for (c, k), v in (ages or {}).items()
                              if c in S and (S[c] >> k) & 1))
            nmk = (nm, am)
            if nmk in seen_norm:
                t0, a0 = seen_norm[nmk]
                if anchor != a0:
                    return {"kind": GLIDER, "period": t - t0,
                            "displacement": anchor - a0, "t": t0,
                            "card": card(S)}
            else:
                seen_norm[nmk] = (t, anchor)
        if card(S) > max_card or (S and max(S) - min(S) > max_span):
            return {"kind": GROWING, "t": t, "card": card(S)}
        S, ages = step_sunset(S, C, tau, ages)
    return {"kind": UNRESOLVED, "t": max_steps, "card": card(S)}


def verify_glider_sunset(S0, C, p, d, tau=1, reps=3):
    """Re-check Phi^p(S) = sigma^d(S) over three full periods, independently."""
    S, ages = dict(S0), None
    for rep in range(1, reps + 1):
        for _ in range(p):
            S, ages = step_sunset(S, C, tau, ages)
        want = {c + d * rep: m for c, m in S0.items()}
        if S != want:
            return False
    return True


def render(S, lo, hi, sym="ABCDEFGH"):
    out = []
    for i in range(lo, hi + 1):
        m = S.get(i, 0)
        if not m:
            out.append(".")
        elif bin(m).count("1") > 1:
            out.append("#")
        else:
            out.append(sym[(m & -m).bit_length() - 1])
    return "".join(out)


def spacetime_sunset(S, C, steps, lo, hi, tau=1):
    return [render(h, lo, hi) for h in run(S, C, steps, tau)]


# ------------------------------------------------------------------ self-tests

def _tests():
    # 1. THE WALKING CLAUSE.  Under permanence the colonizer (0,1,1) fills the
    #    line; under sunset the same single law simply walks.
    C = Const([(0, 1, 1)])
    S = state_of([(0, 0)])
    rows = spacetime_sunset(S, C, 4, 0, 5)
    assert rows == ["A.....", ".A....", "..A...", "...A..", "....A."], rows
    assert verify_glider_sunset(S, C, 1, 1)
    r = classify_sunset(S, C)
    assert r["kind"] == GLIDER and r["period"] == 1 and r["displacement"] == 1, r

    # 2. Nothing is permanent: an isolated blocked law dies at once.
    C = Const([(0, 0, 1)])                  # guard: occupied at i+0 AND empty
    S = state_of([(0, 0)])                  # at i+0 -> never active
    assert classify_sunset(S, C)["kind"] == EXTINCT

    # 3. A solid block under sunset is not frozen (Gridlock needs permanence
    #    too: with nothing re-enacting the interior, it evaporates).
    C = Const([(0, 1, 1)])
    S = state_of([(i, 0) for i in range(6)])
    h = run(S, C, 1)
    assert card(h[1]) < card(h[0]), (h[0], h[1])

    print("sunset self-tests passed: 3/3")


if __name__ == "__main__":
    _tests()
