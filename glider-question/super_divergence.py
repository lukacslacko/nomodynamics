#!/usr/bin/env python3
"""Demonstrates: once cross-kind effects exist (supersession variant), the
resolution axis (parity vs OR) genuinely bifurcates — at configuration size 2,
the provable minimum — whereas in own-kind nomodynamics it is vacuous at every
size (Collision Lemma).  Also measures divergence frequency on random states.

Supersession-parity: an occupied target cell is cleared iff the number of
actors targeting it is ODD.  Supersession-OR: cleared iff >= 1 (canonical).
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nomos_lib import build_tables, make_step_supersession, spacetime

def make_step_supersession_parity(W):
    TYPES, NT, ACTIVE, CLIST = build_tables(W)
    R = 2 * W + 1
    def step(S):
        votes = {}
        enact = {}
        for i, m in S.items():
            nu = 0
            for k in range(R):
                if (i - W + k) in S:
                    nu |= 1 << k
            act = m & ACTIVE[nu]
            if not act:
                continue
            for c, cm in CLIST:
                x = act & cm
                if not x:
                    continue
                j = i + c
                if j in S:
                    votes[j] = votes.get(j, 0) + x.bit_count()
                else:
                    enact[j] = enact.get(j, 0) | x
        out = {}
        for j, m in S.items():
            if not (votes.get(j, 0) % 2):
                out[j] = m
        for j, x in enact.items():
            out[j] = x
        return out
    return step

def main():
    TYPES, NT, ACTIVE, CLIST = build_tables(1)
    TIDX = {t: k for k, t in enumerate(TYPES)}
    stepO = make_step_supersession(1)
    stepP = make_step_supersession_parity(1)

    # THE minimal divergence witness: 2 laws.
    # A=(0,-1,1) at 0 (active: self occupied, rear empty; targets cell 1)
    # B=(0, 1,0) at 1 (active: self occupied, front empty; targets itself)
    # Cell 1 receives 2 clear-votes -> OR clears it, parity does not.
    S0 = {0: 1 << TIDX[(0, -1, 1)], 1: 1 << TIDX[(0, 1, 0)]}
    o1, p1 = stepO(dict(S0)), stepP(dict(S0))
    print("witness seed: A=(0,-1,1)@0, B=(0,1,0)@1   (2 placed laws)")
    print("  supersession-OR     step 1:", sorted(o1.items()))
    print("  supersession-parity step 1:", sorted(p1.items()))
    assert o1 != p1, "expected divergence"
    print("  DIVERGE at t=1 (cell 1: 2 clear-votes; OR clears, parity keeps)")

    # size-1 seeds can never diverge: one actor max per target.
    div1 = 0
    for k in range(NT):
        S = {0: 1 << k}
        a, b = dict(S), dict(S)
        for _ in range(50):
            a, b = stepO(a), stepP(b)
            if a != b:
                div1 += 1
                break
    print(f"  all 27 single-law supersession seeds: divergences = {div1} (expected 0)")

    # divergence frequency on random supersession states
    rng = random.Random(9)
    div = 0; n = 20000
    for _ in range(n):
        S = {}
        for i in range(-4, 5):
            if rng.random() < 0.5:
                S[i] = 1 << rng.randrange(NT)
        if not S:
            continue
        a, b = dict(S), dict(S)
        for _ in range(30):
            a2, b2 = stepO(a), stepP(b)
            if a2 != b2:
                div += 1
                break
            if a2 == a and b2 == b:
                break
            a, b = a2, b2
    print(f"  random supersession states: {div}/{n} trajectories diverge within 30 steps")

if __name__ == "__main__":
    main()
