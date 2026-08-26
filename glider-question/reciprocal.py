#!/usr/bin/env python3
"""Reciprocal-amendment universe R_W — the minimal cross-amendment semantics
that escapes the Anchor Theorem while keeping fixed targeting.

WHY THIS CONVENTION (the coordinator's (a,b,c,e) made precise): in any
fixed-single-target semantics, kind k toggles one kind phi(k) at one offset
c_k.  Multi-authorship of a (slot, kind) pair requires phi non-injective; but
finite kind space + out-degree 1 + "every kind amendable" (in-degree >= 1)
forces phi to be a bijection — so single-authorship (parity == OR) is a
THEOREM in this whole class, and kinds outside im(phi) would be immortal and
pin any pattern containing them.  The canonical choice is therefore a
fixed-point-breaking permutation: kinds are PAIRS (g, h) of chassis
g,h in T0 = {-W..W}^3; law (i,(g,h)) uses g's guards (a,b) and offset c;
when active it toggles kind (h, g) at i + c_g.  Diagonal kinds (g,g) reproduce
the own-kind system exactly (conservative extension); off-diagonal kinds are
amended by a DIFFERENT kind, so H1 fails and the anchor argument does not
apply — this is the smallest fixed-target universe where gliders are not
excluded a priori.  (Genuine multi-authorship/OR-vs-parity divergence needs
state-dependent targets — supersession, see super_divergence.py — or
multi-target laws, which die by a two-case anchor argument.)

Kind index: k = 27*gi + hi (W=1), gi = TIDX[g], hi = TIDX[h]; 729 kinds.
"""
import itertools, json, os, random, sys, time
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nomos_lib import build_tables, classify, count_canonical

W = 1
T0, NT0, ACT0, CLIST0 = build_tables(W)
NK = NT0 * NT0                      # 729
BLOCK = (1 << NT0) - 1

def make_step_reciprocal(mode="parity"):
    R = 2 * W + 1
    # ACTIVE for pair-kinds depends only on g: expand chassis table
    ACTIVE = [0] * (1 << R)
    for nu in range(1 << R):
        a0 = ACT0[nu]
        m = 0
        for gi in range(NT0):
            if (a0 >> gi) & 1:
                m |= BLOCK << (NT0 * gi)
        ACTIVE[nu] = m
    # c-class masks by g's c-component
    CM = {}
    for c, cm0 in CLIST0:
        m = 0
        for gi in range(NT0):
            if (cm0 >> gi) & 1:
                m |= BLOCK << (NT0 * gi)
        CM[c] = m
    CLIST = [(c, CM[c]) for c, _ in CLIST0]
    xor = (mode == "parity")

    def transpose(m):
        """bit (gi,hi) -> (hi,gi) on a 729-bit mask."""
        out = 0
        gi = 0
        while m:
            block = m & BLOCK
            while block:
                b = block & -block
                hi = b.bit_length() - 1
                block ^= b
                out |= 1 << (hi * NT0 + gi)
            m >>= NT0
            gi += 1
        return out

    def step(S):
        tog = {}
        g = tog.get
        for i, m in S.items():
            nu = 2
            if (i - 1) in S: nu |= 1
            if (i + 1) in S: nu |= 4
            act = m & ACTIVE[nu]
            if not act:
                continue
            for c, cm in CLIST:
                x = act & cm
                if x:
                    j = i + c
                    tx = transpose(x)
                    tog[j] = (g(j, 0) ^ tx) if xor else (g(j, 0) | tx)
        if not tog:
            return S
        out = dict(S)
        for j, x in tog.items():
            nm = out.get(j, 0) ^ x
            if nm:
                out[j] = nm
            else:
                out.pop(j, None)
        return out
    return step

def seed_from_slots(slots):
    S = {}
    for s in slots:
        p, k = divmod(s, NK)
        S[p] = S.get(p, 0) | (1 << k)
    return S

# ------------------------------------------------------------ sweeps

_G = {}
def _init():
    _G["p"] = make_step_reciprocal("parity")
    _G["o"] = make_step_reciprocal("or")

def _run(chunk):
    stepP, stepO = _G["p"], _G["o"]
    tally = Counter(); cyc = Counter(); spec = {}
    for slots in chunk:
        S = seed_from_slots(slots)
        v, t, info = classify(S, stepP, step2=stepO)
        tally[v] += 1
        if v == "cycle":
            cyc[info["period"]] += 1
        if v in ("glider", "anomaly", "divergence", "slow-holdout") or \
           (v not in ("extinct", "fixed") and len(spec.get(v, [])) < 40):
            spec.setdefault(v, []).append({"slots": list(slots), "t": t, "info": info})
    return tally, cyc, spec, len(chunk)

def chunks(it, n):
    buf = []
    for x in it:
        buf.append(x)
        if len(buf) >= n:
            yield buf; buf = []
    if buf:
        yield buf

def gen_complete(npos, k):
    nslots = npos * NK
    for first in range(NK):
        if k == 1:
            yield (first,)
        else:
            for rest in itertools.combinations(range(first + 1, nslots), k - 1):
                yield (first,) + rest

def main():
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    t0 = time.time()
    out = {}
    # sanity: diagonal embedding reproduces own-kind system
    stepP = make_step_reciprocal("parity")
    from nomos_lib import make_step
    old = make_step(1, "parity")
    rng = random.Random(5)
    for _ in range(400):
        S0 = {}
        for i in range(-3, 4):
            if rng.random() < .5:
                ki = rng.randrange(NT0)
                S0[i] = S0.get(i, 0) | (1 << ki)
        Sd = {}
        for i, m in S0.items():
            mm = 0
            k = m
            while k:
                b = k & -k; ki = b.bit_length() - 1; k ^= b
                mm |= 1 << (NT0 * ki + ki)
            Sd[i] = mm
        A, B = old(dict(S0)), stepP(dict(Sd))
        BB = {}
        for i, m in B.items():
            mm = 0
            k = m
            while k:
                b = k & -k; kk = b.bit_length() - 1; k ^= b
                gi, hi = divmod(kk, NT0)
                assert gi == hi, "diagonal not preserved!"
                mm |= 1 << gi
            BB[i] = mm
        assert A == BB, "diagonal embedding mismatch"
    print("OK: diagonal kinds reproduce the own-kind system (400 random states)")

    # complete <=2-law / 5-cell duel sweep
    total = count_canonical(NK, 5, 1) + count_canonical(NK, 5, 2)
    print(f"[reciprocal] complete <=2-law/5-cell: {total} canonical seeds, duel mode")
    agg = Counter(); cy = Counter(); sp = {}
    done = 0
    def genall():
        yield from gen_complete(5, 1)
        yield from gen_complete(5, 2)
    with Pool(procs, initializer=_init) as pool:
        for tally, cyc, spec, n in pool.imap_unordered(_run, chunks(genall(), 3000)):
            agg.update(tally); cy.update(cyc); done += n
            for v, lst in spec.items():
                cur = sp.setdefault(v, [])
                if len(cur) < 100000:
                    cur.extend(lst)
            if done // 200000 != (done - n) // 200000:
                print(f"[reciprocal] {done}/{total} {dict(agg)} {round(time.time()-t0)}s", flush=True)
    out["le2_complete"] = {"n": done, "tally": dict(agg),
                           "cycles": dict(sorted(cy.items())), "specimens": sp}
    print(f"[reciprocal] le2 DONE {done}: {dict(agg)} cycles={dict(sorted(cy.items()))}")

    # sampled 3-law
    NS = 400000
    space = count_canonical(NK, 5, 3)
    rng = random.Random(20260901)
    seen = set(); samples = []
    nslots = 5 * NK
    while len(samples) < NS:
        s = tuple(sorted(rng.sample(range(nslots), 3)))
        if s[0] >= NK or s in seen:
            continue
        seen.add(s); samples.append(s)
    agg = Counter(); cy = Counter(); done = 0
    with Pool(procs, initializer=_init) as pool:
        for tally, cyc, spec, n in pool.imap_unordered(_run, chunks(iter(samples), 3000)):
            agg.update(tally); cy.update(cyc); done += n
            for v, lst in spec.items():
                cur = sp.setdefault(v, [])
                if len(cur) < 100000:
                    cur.extend(lst)
            if done // 100000 != (done - n) // 100000:
                print(f"[reciprocal3] {done}/{NS} {dict(agg)} {round(time.time()-t0)}s", flush=True)
    out["3law_sample"] = {"n": done, "space": space, "tally": dict(agg),
                          "cycles": dict(sorted(cy.items())), "rng": 20260901}
    print(f"[reciprocal] 3law sample DONE {done}/{space}: {dict(agg)}")
    out["specimens_all"] = sp
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "data", "reciprocal_w1.json"), "w") as f:
        json.dump(out, f)
    print(f"[reciprocal] wall {round(time.time()-t0)}s -> data/reciprocal_w1.json")

if __name__ == "__main__":
    main()
