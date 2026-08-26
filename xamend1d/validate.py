#!/usr/bin/env python3
"""
validate.py — soundness battery for the SAT instrument (xsat.py).

NOTHING in this expedition may cite an UNSAT until this passes.  Three kinds
of test, all against the independent engine `xnomos.py`:

  T1 FIDELITY.  Pin the constitution AND the seed inside the CNF; unit
     propagation then *computes* the trajectory.  Compare all p+1 frames to
     xnomos.step, cell by cell, kind by kind.  Random constitutions and seeds,
     all four modes, plus rings.
  T2 COMPLETENESS ON KNOWN SPECIMENS.  The encoder must FIND the Z/6 ring
     rotor, and known oscillators, from a blank slate (constitution free).
  T3 AGREEMENT WITH ESTABLISHED THEORY.  Own-kind targeting on Z must come
     back UNSAT (Anchor Theorem) for every (p,d) tried; and every SAT model
     the instrument ever produces is re-verified by xnomos.verify_glider.
"""
from __future__ import annotations

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import xnomos
import xsat
from xsat import Spec, build, val


# --------------------------------------------------------------------- T1


def pin_and_run(n, W, N, p, mode, rules, targets, seed, modulus=None):
    """Build the CNF with constitution+seed pinned; return the frames it forces."""
    sp = Spec(n=n, W=W, N=N, p=p, d=0, mode=mode, targets=targets,
              fixed_rules=rules, modulus=modulus,
              assert_glider=False, symbreak=False)
    C, meta = build(sp)
    for i in range(N):
        for k in range(n):
            s = meta["x"][0][i][k]
            want = bool(seed.get(i, 0) >> k & 1)
            if isinstance(s, bool):
                if s != want:
                    return None                  # seed hits the forced margin
            else:
                C.add(s if want else -s)
    from pysat.solvers import Solver
    with Solver(name="cadical195", bootstrap_with=C.cls) as S:
        if not S.solve():
            return "UNSAT"
        model = set(l for l in S.get_model() if l > 0)
        out = xsat.extract(meta, model)
        # determinism check: no second model may exist
        blk = []
        for s in range(p + 1):
            for i in range(N):
                for k in range(n):
                    sig = meta["x"][s][i][k]
                    if isinstance(sig, bool):
                        continue
                    blk.append(-sig if val(sig, model) else sig)
        S.add_clause(blk)
        assert not S.solve(), "trajectory not determined by seed+constitution!"
    return out["frames"]


def t1_fidelity(trials=400, seed0=20260826):
    rng = random.Random(seed0)
    modes = ["parity", "or", "super", "super_or"]
    checked = 0
    escapes = [0]
    for _ in range(trials):
        mode = rng.choice(modes)
        n = rng.randrange(1, 4)
        W = rng.choice([1, 1, 2])
        ring = rng.random() < 0.25
        m = rng.randrange(4, 10) if ring else None
        N = m if ring else rng.randrange(2 * W + 4, 2 * W + 11)
        p = rng.randrange(1, 7)
        offs = list(range(-W, W + 1))
        rules = [tuple(rng.choice(offs) for _ in range(3)) for _ in range(n)]
        targets = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                   for _ in range(n)]
        lo, hi = (0, N - 1) if ring else (W, N - 1 - W)
        seed = {}
        for _ in range(rng.randrange(1, 7)):
            i = rng.randrange(lo, hi + 1)
            seed[i] = seed.get(i, 0) | (1 << rng.randrange(n))
        # reference: xnomos on all of Z (or the ring)
        Cn = xnomos.Const(rules, list(targets), dim=1, modulus=m)
        S = dict(seed)
        want = [{c: v for c, v in S.items() if v}]
        for _ in range(p):
            S = xnomos.step(S, Cn, mode)
            want.append({c: v for c, v in S.items() if v})
        escaped = (not ring) and any(c < W or c > N - 1 - W
                                     for fr in want for c in fr)
        got = pin_and_run(n, W, N, p, mode, rules, targets, seed, modulus=m)
        if got is None:
            continue
        if escaped:
            # EXACTNESS TEST: the true Z-trajectory leaves the interior, so the
            # bounded model MUST refuse it (else UNSAT would not be a Z no-go).
            assert got == "UNSAT", ("EXACTNESS FAIL — model accepted an escaping"
                                    " trajectory", mode, n, W, N, p, rules,
                                    targets, seed, want)
            escapes[0] += 1
            continue
        assert got != "UNSAT", ("FIDELITY FAIL — pinned instance UNSAT", mode,
                                n, W, N, p, m, rules, targets, seed, want)
        for t in range(p + 1):
            assert want[t] == got[t], ("FIDELITY FAIL", mode, n, W, N, p, m,
                                       rules, targets, seed, t, want[t], got[t])
        checked += 1
    print("T1 fidelity: %d/%d random universes match xnomos frame-for-frame "
          "(all four modes, Z and rings); %d further universes escaped the "
          "interior and were correctly REFUSED by the bounded model"
          % (checked, trials, escapes[0]))
    return checked


# --------------------------------------------------------------------- T2


def t2_ring_rotor():
    """The instrument must FIND the Z/6 rotor with the constitution free."""
    sp = Spec(n=1, W=1, N=6, p=1, d=3, mode="parity", targets=[(0,)],
              modulus=6, max_laws=3, nonfixed=True)
    st, info = xsat.solve(sp)
    assert st == "SAT", "instrument failed to find the Z/6 rotor: %s" % st
    rules, frames = info["rules"], info["frames"]
    Cn = xnomos.Const(rules, [(0,)], modulus=6)
    S = {c: m for c, m in frames[0].items() if m}
    T = xnomos.step(S, Cn)
    want = {(c + 3) % 6: m for c, m in S.items()}
    assert T == want, (rules, S, T, want)
    print("T2a ring rotor found from scratch: rule %s, cells %s, rot 3 "
          "(re-verified by xnomos)" % (rules[0], sorted(S)))

    # and the known specimen must be accepted
    got = pin_and_run(1, 1, 6, 2, "parity", [(0, 1, -1)], [(0,)],
                      {1: 1, 2: 1, 5: 1}, modulus=6)
    assert set(got[1]) == {2, 4, 5} and set(got[2]) == {1, 2, 5}, got
    print("T2b published rotor {1,2,5} on Z/6 reproduced by the encoder")


def t2_oscillator():
    """With d = 0 the instrument is an oscillator finder; check p=2 and p=3."""
    for p in (2, 3, 4):
        sp = Spec(n=2, W=1, N=9, p=p, d=0, mode="parity",
                  nonfixed=True, prime_period=True, max_laws=4)
        st, info = xsat.solve(sp)
        assert st == "SAT", (p, st)
        Cn = xnomos.Const(info["rules"], list(info["targets"]))
        S = {c: m for c, m in info["frames"][0].items() if m}
        T = dict(S)
        for _ in range(p):
            T = xnomos.step(T, Cn, "parity")
        assert T == S, (p, info["rules"], info["targets"], S, T)
        print("T2c period-%d oscillator found & xnomos-verified: %s tgt=%s S=%s"
              % (p, info["rules"], info["targets"], sorted(S.items())))


# --------------------------------------------------------------------- T3


def t3_ownkind_unsat():
    """Own-kind targeting on Z: the Anchor Theorem says UNSAT.  Check it."""
    bad = []
    for n in (1, 2):
        for p in range(1, 5):
            for d in range(1, 4):
                sp = Spec(n=n, W=1, N=12, p=p, d=d, mode="parity",
                          targets=[(k,) for k in range(n)])
                st, _ = xsat.solve(sp)
                if st != "UNSAT":
                    bad.append((n, p, d, st))
    assert not bad, bad
    print("T3 own-kind on Z: UNSAT for n<=2, p<=4, d<=3, N=12 "
          "— agrees with the Anchor Theorem")


def certify(info, mode, reps=3):
    """Independent re-verification of a SAT glider by xnomos.verify_glider."""
    sp = info["spec"]
    Cn = xnomos.Const(info["rules"], list(info["targets"]),
                      modulus=sp.modulus)
    S = {c: m for c, m in info["frames"][0].items() if m}
    return xnomos.verify_glider(S, Cn, sp.p, sp.d, mode) and bool(S)


if __name__ == "__main__":
    t1_fidelity(int(sys.argv[1]) if len(sys.argv) > 1 else 400)
    t2_ring_rotor()
    t2_oscillator()
    t3_ownkind_unsat()
    print("\nALL VALIDATION PASSED — the instrument may be trusted.")
