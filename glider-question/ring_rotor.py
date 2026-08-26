#!/usr/bin/env python3
"""Sharpness of the ORDER hypothesis: on the nomic ring Z/m the Anchor
Theorem's extremal argument is unavailable (no leftmost law), and
F2[s]/(s^m - 1) is not a domain.  Search all small ring seeds for ROTORS:
states with Phi^p(S) = rot_d(S), d != 0 mod m — the compact analog of a
glider.  Parity semantics (== OR by Lemma 1, which holds on rings too).
"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nomos_lib import build_tables

def make_ring_step(W, m):
    TYPES, NT, ACTIVE, CLIST = build_tables(W)
    R = 2 * W + 1
    def step(S):
        tog = {}
        for i, mm in S.items():
            nu = 0
            for k in range(R):
                if ((i - W + k) % m) in S:
                    nu |= 1 << k
            act = mm & ACTIVE[nu]
            if not act:
                continue
            for c, cm in CLIST:
                x = act & cm
                if x:
                    j = (i + c) % m
                    tog[j] = tog.get(j, 0) ^ x
        out = dict(S)
        for j, x in tog.items():
            nm = out.get(j, 0) ^ x
            if nm:
                out[j] = nm
            else:
                out.pop(j, None)
        return out
    return step

def canon(S, m):
    """Lexicographic minimum over rotations; returns (key, rotation)."""
    best = None; bestr = 0
    for r in range(m):
        key = tuple(sorted(((i - r) % m, v) for i, v in S.items()))
        if best is None or key < best:
            best, bestr = key, r
    return best, bestr

def classify_ring(S0, step, m, max_steps=4000):
    S = dict(S0)
    seen = {}
    for t in range(max_steps):
        if not S:
            return ("extinct", t, None)
        key, r = canon(S, m)
        if key in seen:
            t0, r0 = seen[key]
            p, d = t - t0, (r - r0) % m
            if d == 0:
                return (("fixed" if p == 1 else "cycle"), t0, {"period": p})
            return ("ROTOR", t0, {"period": p, "rot": d, "m": m})
        seen[key] = (t, r)
        S = step(S)
    return ("holdout", max_steps, None)

def verify_rotor(S, step, m, p, d, reps=3):
    T = dict(S)
    for _ in range(reps):
        U = dict(T)
        for _ in range(p):
            U = step(U)
        if sorted(((i + d) % m, v) for i, v in T.items()) != sorted(U.items()):
            return False
        T = U
    return True

def main():
    W = 1
    TYPES, NT, _, _ = build_tables(W)
    finds = Counter(); examples = {}
    for m in range(3, 13):
        step = make_ring_step(W, m)
        # all 1-law and 2-law seeds up to rotation (fix first law at cell 0)
        seeds = []
        for k1 in range(NT):
            seeds.append({0: 1 << k1})
            for pos in range(m):
                for k2 in range(NT):
                    if pos == 0 and k2 <= k1:
                        continue
                    S = {0: 1 << k1}
                    S[pos] = S.get(pos, 0) | (1 << k2)
                    seeds.append(S)
        tally = Counter()
        for S in seeds:
            v, t, info = classify_ring(S, step, m)
            tally[v] += 1
            if v == "ROTOR":
                # confirm by 3-period re-simulation from the recurrent state
                T = dict(S)
                ok = verify_rotor(T, step, m, info["period"] * 1, info["rot"])
                # simplest verification from t=0 state after transient:
                for _ in range(t):
                    T = step(T)
                ok = verify_rotor(T, step, m, info["period"], info["rot"])
                key = (m, info["period"], info["rot"])
                finds[key] += 1
                if key not in examples and ok:
                    examples[key] = (sorted(S.items()), t)
        print(f"ring m={m}: {len(seeds)} seeds -> {dict(tally)}", flush=True)
    print("\nROTOR classes (m, period, rotation): count")
    for k in sorted(finds):
        print(f"  {k}: {finds[k]}   example seed {examples.get(k)}")

if __name__ == "__main__":
    main()
