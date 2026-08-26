#!/usr/bin/env python3
"""Engine validation: fast engines vs (a) the original nomos2.py engine (W=1
parity) and (b) a naive per-law reference implementation straight from the
definition (W=1,2; parity and OR).  Also: known-specimen regression tests and
the actor-multiplicity instrument."""
import random, sys
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6")
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/glider-question")
import nomos2
from nomos_lib import (build_tables, make_step, make_step_supersession,
                       classify, max_actor_multiplicity, spacetime,
                       verify_glider)

def naive_step(S, W, mode):
    TYPES, NT, ACTIVE, CLIST = build_tables(W)
    from collections import defaultdict
    cnt = defaultdict(int)
    for i, m in S.items():
        for k in range(NT):
            if (m >> k) & 1:
                a, b, c = TYPES[k]
                if (i + a) in S and (i + b) not in S:
                    cnt[(i + c, k)] += 1
    out = dict(S)
    for (j, k), n in cnt.items():
        flip = (n % 2 == 1) if mode == "parity" else (n >= 1)
        if flip:
            nm = out.get(j, 0) ^ (1 << k)
            if nm:
                out[j] = nm
            else:
                out.pop(j, None)
    return out

def rand_state(rng, W, span=8, fill=0.5, maxbits=4):
    NT = (2 * W + 1) ** 3
    S = {}
    for i in range(-span, span + 1):
        if rng.random() < fill:
            m = 0
            for _ in range(rng.randint(1, maxbits)):
                m |= 1 << rng.randrange(NT)
            S[i] = m
    return S

def main():
    rng = random.Random(12345)
    # (a) vs original nomos2 engine, W=1 parity
    stepP1 = make_step(1, "parity")
    for trial in range(3000):
        S = rand_state(rng, 1)
        assert stepP1(dict(S)) == nomos2.step(dict(S)), f"nomos2 mismatch {S}"
    print("OK: W1 parity fast engine == nomos2.step on 3000 random states")

    # (b) vs naive reference, all four engine configs
    for W in (1, 2):
        for mode in ("parity", "or"):
            st = make_step(W, mode)
            for trial in range(600):
                S = rand_state(rng, W, span=6, maxbits=5)
                assert st(dict(S)) == naive_step(S, W, mode), (W, mode, S)
            print(f"OK: W{W} {mode} fast engine == naive reference on 600 random states")

    # actor multiplicity instrument: lemma says always <= 1
    worst = 0
    for trial in range(20000):
        W = rng.choice((1, 2))
        S = rand_state(rng, W, span=10, fill=0.6, maxbits=6)
        worst = max(worst, max_actor_multiplicity(S, W))
    print(f"OK: max per-(target,kind) actor multiplicity over 20000 random states = {worst} (lemma: <=1)")
    assert worst <= 1

    # known specimens, W=1 parity
    TYPES, NT, ACTIVE, CLIST = build_tables(1)
    TIDX = {t: k for k, t in enumerate(TYPES)}
    colon = {0: 1 << TIDX[(0, 1, 1)]}
    v, t, info = classify(colon, stepP1, max_steps=2000)
    print(f"colonizer (0,1,1): {v} @ {t} {info}")
    assert v == "big-growth" or v == "slow-holdout"
    sunset = {0: 1 << TIDX[(0, -1, 1)]}
    v, t, info = classify(sunset, stepP1)
    print(f"sunset clause (0,-1,1): {v} {info}")
    assert v == "cycle" and info["period"] == 2
    selfrep = {0: 1 << TIDX[(0, 1, 0)]}
    v, t, info = classify(selfrep, stepP1)
    print(f"self-repealer (0,1,0): {v} @ t={t}")
    assert v == "extinct"

    # duel mode: parity vs or lockstep on 5000 random small seeds
    stepO1 = make_step(1, "or")
    stepP2, stepO2 = make_step(2, "parity"), make_step(2, "or")
    div = 0
    for trial in range(5000):
        W = rng.choice((1, 2))
        S = rand_state(rng, W, span=3, fill=0.5, maxbits=2)
        if not S:
            continue
        sp, so = (stepP1, stepO1) if W == 1 else (stepP2, stepO2)
        v, t, info = classify(S, sp, step2=so, max_steps=300)
        if v == "divergence":
            div += 1
            print("DIVERGENCE:", S, info)
    print(f"OK: duel classifier, divergences = {div} / 5000")
    assert div == 0

    # glider verifier self-test on a hand-built translation map (sanity of the checker):
    # fake dynamics: pure shift by +1 each step
    fake = lambda S: {i + 1: v for i, v in S.items()}
    assert verify_glider({0: 3, 1: 1}, fake, p=2, d=2, reps=3)
    assert not verify_glider({0: 3, 1: 1}, fake, p=2, d=1, reps=1)
    print("OK: glider verifier sanity")

    # supersession engine smoke test: single (0,-1,1) is a blinker there (not colonizer)
    sup = make_step_supersession(1)
    v, t, info = classify({0: 1 << TIDX[(0, -1, 1)]}, sup)
    print(f"supersession (0,-1,1): {v} {info}")
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    main()
