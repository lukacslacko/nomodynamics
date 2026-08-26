#!/usr/bin/env python3
"""CROSS-AMENDMENT teaser (coordinator correction, 2026-08-26): extend law
types with a target-kind component.  Two-kind universe: an experiment is
E = (Ta, ea, Tb, eb): kind A has guard/effect triple Ta=(a,b,c) and target
flag ea (0 = toggles kind A, 1 = toggles kind B) at p+c; kind B likewise.
Now two authors (one A-law, one B-law) CAN toggle the same (cell, kind):
multi-author interference exists and PARITY vs OR genuinely differ.

Random survey of experiments+seeds under both semantics; verdict-diff count;
dense alpha checks on growth seeds (is plane-filling now possible?); plus a
designed quadrant-filler demo.
"""
import json, random, sys, time
from collections import Counter
from multiprocessing import Pool
import numpy as np
from engine2d import (M, enc, dec, OFFI, TYPES, tname, tparse, _sh, render,
                      canon_cells)

DOFF = [0, M, -M, 1, -1]

def xstep(S, exp, sem):
    Ta, ea, Tb, eb = exp
    (iaa, iab, iac), (iba, ibb, ibc) = TYPES[Ta], TYPES[Tb]
    dAa, dAb, dAc = DOFF[iaa], DOFF[iab], DOFF[iac]
    dBa, dBb, dBc = DOFF[iba], DOFF[ibb], DOFF[ibc]
    tA = 1 << ea            # target bit of an A-law: 1 if self else 2
    tB = 2 >> eb            # target bit of a B-law: 2 if self else 1
    tog = {}
    tg = tog.get
    for p, mk in S.items():
        if mk & 1 and (p + dAa) in S and (p + dAb) not in S:
            q = p + dAc
            if sem == "p":
                tog[q] = tg(q, 0) ^ tA
            else:
                tog[q] = tg(q, 0) | tA
        if mk & 2 and (p + dBa) in S and (p + dBb) not in S:
            q = p + dBc
            if sem == "p":
                tog[q] = tg(q, 0) ^ tB
            else:
                tog[q] = tg(q, 0) | tB
    if not any(tog.values()):
        return S
    out = dict(S)
    for q, m in tog.items():
        if not m:
            continue
        nm = out.get(q, 0) ^ m
        if nm:
            out[q] = nm
        else:
            del out[q]
    return out

def xsize(S):
    return sum(v.bit_count() for v in S.values())

def xclassify(spec, exp, sem, max_steps=256, growth_cap=1500, hash_cap=240):
    S = {}
    for (x, y), kind in spec:
        p = enc(x, y)
        S[p] = S.get(p, 0) | (1 << kind)
    seen = {}
    sizes = []
    t = 0
    while True:
        if not S:
            return dict(v="extinct", t=t)
        sz = xsize(S)
        sizes.append(sz)
        if sz > growth_cap:
            return dict(v="growth", t=t, sz=sz)
        if sz <= hash_cap:
            cells = [(*dec(p), m) for p, m in S.items()]
            key, cx, cy = canon_cells(cells)
            hit = seen.get(key)
            if hit is not None:
                t0, cx0, cy0 = hit
                p_, dx, dy = t - t0, cx - hit[1], cy - hit[2]
                if dx == 0 and dy == 0:
                    return dict(v=("fixed" if p_ == 1 else "cycle"), t0=t0, p=p_, sz=sz)
                return dict(v="glider", t0=t0, p=p_, d=(dx, dy), sz=sz)
            seen[key] = (t, cx, cy)
        if t >= max_steps:
            a, b = sizes[-1], max(1, sizes[len(sizes) // 2])
            return dict(v="unresolved", sz=sz,
                        trend=("grow" if (a >= 60 and a >= 1.6 * b) else "flat"))
        S2 = xstep(S, exp, sem)
        if S2 is S:
            return dict(v="fixed", t=t, sz=sz)
        S = S2
        t += 1

def np_xrun(spec, exp, T, sem="p", R=None):
    Ta, ea, Tb, eb = exp
    if R is None:
        R = T + 4
    n = 2 * R + 1
    A = np.zeros((n, n), bool); B = np.zeros((n, n), bool)
    for (x, y), kind in spec:
        (A if kind == 0 else B)[x + R, y + R] = True
    sizes = []
    for t in range(T + 1):
        occ = A | B
        sizes.append(int(A.sum()) + int(B.sum()))
        if t == T:
            break
        (iaa, iab, iac) = TYPES[Ta]; (iba, ibb, ibc) = TYPES[Tb]
        actA = A & _sh(occ, *OFFI[iaa]) & ~_sh(occ, *OFFI[iab])
        actB = B & _sh(occ, *OFFI[iba]) & ~_sh(occ, *OFFI[ibb])
        ca, cb = OFFI[iac], OFFI[ibc]
        sA = _sh(actA, -ca[0], -ca[1])   # toggle field from A-laws
        sB = _sh(actB, -cb[0], -cb[1])   # from B-laws
        # route by target kind
        toA = [];  toB = []
        (toA if ea == 0 else toB).append(sA)
        (toB if eb == 0 else toA).append(sB)
        def comb(lst):
            if not lst:
                return None
            if len(lst) == 1:
                return lst[0]
            return (lst[0] ^ lst[1]) if sem == "p" else (lst[0] | lst[1])
        fA, fB = comb(toA), comb(toB)
        if fA is not None:
            A = A ^ fA
        if fB is not None:
            B = B ^ fB
    return A, B, sizes, R

def sample_survey(nexp=4000, seed=7):
    rng = random.Random(seed)
    tally = {"p": Counter(), "o": Counter()}
    diffs = 0
    finds = {"glider": [], "cycle>8": [], "diff": [], "growth": []}
    for i in range(nexp):
        Ta, Tb = rng.randrange(125), rng.randrange(125)
        ea, eb = rng.choice(((0, 1), (1, 0), (1, 1)))
        exp = (Ta, ea, Tb, eb)
        nl = rng.choice((2, 2, 3, 3))
        spec = set()
        while len(spec) < nl:
            spec.add(((rng.randint(-1, 1), rng.randint(-1, 1)), rng.randint(0, 1)))
        spec = sorted(spec)
        vs = {}
        for sem in ("p", "o"):
            v = xclassify(spec, exp, sem)
            vs[sem] = v
            key = v["v"] if v["v"] != "unresolved" else "unres-" + v["trend"]
            if v["v"] == "cycle":
                key = "cycle>8" if v["p"] > 8 else f"cycle-{v['p']}"
            tally[sem][key] += 1
            if v["v"] == "glider" and len(finds["glider"]) < 40:
                finds["glider"].append((exp, spec, sem, v))
            if v["v"] == "cycle" and v["p"] > 8 and len(finds["cycle>8"]) < 40:
                finds["cycle>8"].append((exp, spec, sem, v))
            if (v["v"] == "growth" or (v["v"] == "unresolved"
                                       and v["trend"] == "grow")) \
                    and len(finds["growth"]) < 600:
                finds["growth"].append((exp, spec, sem, v))
        if vs["p"]["v"] != vs["o"]["v"] or \
           (vs["p"]["v"] == "cycle" and vs["p"].get("p") != vs["o"].get("p")):
            diffs += 1
            if len(finds["diff"]) < 60:
                finds["diff"].append((exp, spec, vs["p"], vs["o"]))
    return tally, diffs, finds

def main():
    print("== CROSS-AMENDMENT SURVEY: 4000 experiments x both semantics ==")
    t0 = time.time()
    tally, diffs, finds = sample_survey(4000)
    print(f"({time.time()-t0:.0f}s)")
    print("parity tally:", dict(tally["p"].most_common()))
    print("OR     tally:", dict(tally["o"].most_common()))
    print(f"semantics-DIVERGENT seeds: {diffs} / 4000  "
          "(multi-author interference is real)")
    for kind in ("glider", "cycle>8"):
        print(f"{kind}: {len(finds[kind])}")
        for exp, spec, sem, v in finds[kind][:8]:
            Ta, ea, Tb, eb = exp
            print(f"   A={tname(Ta)}->{'AB'[ea]} B={tname(Tb)}->{'BA'[eb]} "
                  f"seed={spec} sem={sem} {v}")
    print("example divergent seeds:")
    for exp, spec, vp, vo in finds["diff"][:6]:
        Ta, ea, Tb, eb = exp
        print(f"   A={tname(Ta)}->{'AB'[ea]} B={tname(Tb)}->{'BA'[eb]} seed={spec}")
        print(f"      parity: {vp}   OR: {vo}")

    # alpha check on growth finds
    print("\n== alpha check on cross-amendment growth seeds ==")
    best = []
    for exp, spec, sem, v in finds["growth"][:120]:
        A, B, sizes, R = np_xrun(spec, exp, 220, sem=sem)
        ts = np.arange(len(sizes))
        msk = (ts >= 40) & (np.array(sizes) > 0)
        if msk.sum() < 20:
            continue
        al = float(np.polyfit(np.log(ts[msk]), np.log(np.array(sizes)[msk]), 1)[0])
        best.append((al, exp, spec, sem, sizes[-1]))
    best.sort(reverse=True)
    print("top alphas:")
    for al, exp, spec, sem, szT in best[:10]:
        Ta, ea, Tb, eb = exp
        print(f"   alpha={al:.3f} size220={szT} A={tname(Ta)}->{'AB'[ea]} "
              f"B={tname(Tb)}->{'BA'[eb]} seed={spec} sem={sem}")

    # designed quadrant-filler: A=(O,N,E)->B, B=(O,E,N)->A
    print("\n== DESIGNED QUADRANT TEST: A=ONE->B, B=OEN->A, seed A@(0,0) ==")
    exp = (tparse("ONE"), 1, tparse("OEN"), 1)
    for sem in ("p", "o"):
        A, B, sizes, R = np_xrun([((0, 0), 0)], exp, 200, sem=sem)
        ts = np.arange(len(sizes))
        msk = ts >= 40
        al = float(np.polyfit(np.log(ts[msk]), np.log(np.array(sizes)[msk]), 1)[0])
        print(f" sem={sem}: size(200)={sizes[-1]} alpha={al:.3f}")
        occ = A | B
        pts = np.argwhere(occ)
        print(f"   bbox x {pts[:,0].min()-R}..{pts[:,0].max()-R} "
              f"y {pts[:,1].min()-R}..{pts[:,1].max()-R}")
    # render small version at t=40
    exp_render = []
    A, B, s2, R = np_xrun([((0, 0), 0)], exp, 40, sem="p")
    Sd = {}
    for i, j in np.argwhere(A):
        Sd[enc(int(i)-R, int(j)-R)] = Sd.get(enc(int(i)-R, int(j)-R), 0) | 1
    for i, j in np.argwhere(B):
        Sd[enc(int(i)-R, int(j)-R)] = Sd.get(enc(int(i)-R, int(j)-R), 0) | 2
    print(" parity t=40 (A / B / & = both):")
    print(render(Sd, legend={0: "A", 1: "B"}, maxw=60, maxh=50))

if __name__ == "__main__":
    main()
