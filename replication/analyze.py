#!/usr/bin/env python3
"""
analyze.py — full dossier on one candidate replicator.

For a (constitution, mode, seed) it reports
  * the causal-component / copy trajectory (rung 1, 2, 3 evidence),
  * the independent certificate from replib.pstep,
  * the guard audit: how many laws are blocked, and when,
  * the additivity audit:
        (i)  Phi^t vs L^t, L = the unconditional linear map,
        (ii) superposition Phi^p(A u B) =? Phi^p(A) xor Phi^p(B) over every
             splitting of the seed into two nonempty parts,
        (iii) far-apart superposition (must hold, Lemma S -- a control),
  * ASCII frames.
"""

from __future__ import annotations

import os
import sys
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from xnomos import Const, state_of, step, card, active_laws, laws   # noqa
from replib import (to_p, from_p, pstep, radius, shift,               # noqa
                    frame1d, frame2d, contains, diff, dist_inf, supp)


def linear_map(S, C):
    """L: every law fires, guards ignored, parity resolution."""
    tog = {}
    for cell, k in laws(S):
        j = C.add(cell, C.rules[k][2])
        for t in C.targets[k]:
            tog[j] = tog.get(j, 0) ^ (1 << t)
    out = dict(S)
    for j, x in tog.items():
        m = out.get(j, 0) ^ x
        if m:
            out[j] = m
        elif j in out:
            del out[j]
    return out


def comps2d(S, R):
    cells = list(S)
    par = list(range(len(cells)))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            if all(abs(a - b) <= 2 * R for a, b in zip(cells[i], cells[j])):
                ri, rj = find(i), find(j)
                if ri != rj:
                    par[ri] = rj
    g = {}
    for i in range(len(cells)):
        g.setdefault(find(i), []).append(cells[i])
    return list(g.values())


def comps1d(S, R):
    cells = sorted(S)
    out, cur = [], [cells[0]]
    for c in cells[1:]:
        if c - cur[-1] > 2 * R:
            out.append(cur)
            cur = [c]
        else:
            cur.append(c)
    out.append(cur)
    return out


def copy_census(S, S0, C, R):
    """(#components that are exact translates of S0, #components, debris)."""
    dim = C.dim
    gs = comps2d(S, R) if dim == 2 else comps1d(S, R)
    if dim == 1:
        base0 = min(S0)
        rel = {c - base0: m for c, m in S0.items()}
    else:
        base0 = min(S0, key=lambda c: (c[1], c[0]))
        rel = {(c[0] - base0[0], c[1] - base0[1]): m for c, m in S0.items()}
    ncopy, deb = 0, 0
    anchors = []
    for cs in gs:
        if len(cs) == len(rel):
            b = min(cs) if dim == 1 else min(cs, key=lambda c: (c[1], c[0]))
            if dim == 1:
                ok = all(S[c] == rel.get(c - b, -1) for c in cs)
            else:
                ok = all(S[c] == rel.get((c[0] - b[0], c[1] - b[1]), -1)
                         for c in cs)
            if ok:
                ncopy += 1
                anchors.append(b)
                continue
        deb += sum(bin(S[c]).count("1") for c in cs)
    return ncopy, len(gs), deb, anchors


def dossier(name, C, S0, mode, T=200, frames=0, framebox=None, quiet=False):
    R = radius(C)
    out = {"name": name, "R": R}
    # ---- trajectory
    S = dict(S0)
    L = dict(S0)
    traj = []
    bite_first = None
    lin_first = None
    blocked_total = 0
    best = None
    for t in range(1, T + 1):
        nb = card(S) - len(active_laws(S, C))
        blocked_total += nb
        if nb and bite_first is None:
            bite_first = (t - 1, nb)
        S = step(S, C, mode)
        L = linear_map(L, C)
        if S != L and lin_first is None:
            lin_first = t
        if not S:
            traj.append((t, 0, 0, 0, 0))
            break
        nc, ng, deb, anch = copy_census(S, S0, C, R)
        traj.append((t, card(S), nc, ng, deb))
        if nc >= 2:
            cand = (deb, -nc, t, anch)
            if best is None or cand < best:
                best = cand
    out["traj"] = traj
    out["bite_first"] = bite_first
    out["blocked_total"] = blocked_total
    out["lin_first"] = lin_first
    out["additive"] = lin_first is None
    out["best"] = best
    out["max_copies"] = max((x[2] for x in traj), default=0)
    out["max_copies_exact"] = max((x[2] for x in traj if x[4] == 0), default=0)

    # ---- independent certificate at the best event
    if best is not None:
        deb, nc, p, anch = best
        P = to_p(S0)
        for _ in range(p):
            P = pstep(P, C, mode)
        St = from_p(P)
        ok = True
        cells = []
        for a in anch:
            d = (a - min(S0)) if C.dim == 1 else \
                tuple(x - y for x, y in
                      zip(a, min(S0, key=lambda c: (c[1], c[0]))))
            U = shift(S0, d, C.dim)
            if not contains(St, U):
                ok = False
            cells.append(sorted(U))
        gaps = []
        for i in range(len(anch)):
            for j in range(i + 1, len(anch)):
                A = supp(shift(S0, (anch[i] - min(S0)) if C.dim == 1 else
                               tuple(x - y for x, y in zip(anch[i], min(
                                   S0, key=lambda c: (c[1], c[0])))), C.dim))
                B = supp(shift(S0, (anch[j] - min(S0)) if C.dim == 1 else
                               tuple(x - y for x, y in zip(anch[j], min(
                                   S0, key=lambda c: (c[1], c[0])))), C.dim))
                gaps.append(dist_inf(A, B, C.dim))
        out["cert_ok"] = ok and all(g > 2 * R for g in gaps)
        out["cert_gaps"] = gaps
        out["cert_cells"] = cells
        out["cert_p"] = p
        out["cert_debris"] = deb
        out["cert_ncopies"] = -nc

    # ---- superposition over splittings of the seed
    pl = list(laws(S0))
    fails = tot = 0
    if best is not None and len(pl) >= 2:
        p = best[2]
        for r in range(1, len(pl) // 2 + 1):
            for A in itertools.combinations(pl, r):
                Ad, Bd = {}, {}
                for c, k in A:
                    Ad[c] = Ad.get(c, 0) | (1 << k)
                for c, k in pl:
                    if (c, k) not in A:
                        Bd[c] = Bd.get(c, 0) | (1 << k)
                if not Bd:
                    continue
                PA, PB = to_p(Ad), to_p(Bd)
                for _ in range(p):
                    PA = pstep(PA, C, mode)
                    PB = pstep(PB, C, mode)
                Q = to_p(S0)
                for _ in range(p):
                    Q = pstep(Q, C, mode)
                tot += 1
                if Q != (PA ^ PB):
                    fails += 1
    out["split_fails"] = (fails, tot)

    if not quiet:
        print("=" * 72)
        print(name, " | mode =", mode, " | R =", R, " | dim =", C.dim)
        print("  rules   :", C.rules)
        print("  targets :", C.targets)
        print("  guards  :", C.guards)
        print("  seed    :", sorted(S0.items()))
        print("  first blocked law at t=%s ; total blocked-law-steps in %d "
              "steps: %d" % (bite_first, T, blocked_total))
        print("  Phi == L (unconditional linear map)? %s%s"
              % (out["additive"], "" if out["additive"]
                 else "   FIRST DIVERGENCE t=%d" % lin_first))
        print("  seed-splitting superposition failures: %d/%d"
              % out["split_fails"])
        print("  max exact free copies over t<=%d : %d   (max copies with "
              "debris: %d)" % (T, out["max_copies_exact"], out["max_copies"]))
        if best is not None:
            print("  BEST EVENT p=%d copies=%d debris=%d gaps=%s cert=%s"
                  % (out["cert_p"], out["cert_ncopies"], out["cert_debris"],
                     out["cert_gaps"], out["cert_ok"]))
            for i, cs in enumerate(out["cert_cells"]):
                print("     copy %d : %s" % (i, cs))
        head = [x for x in traj[:24]]
        print("  t,card,copies,comps,debris:", head)
    if frames:
        S = dict(S0)
        for t in range(frames):
            print("  --- t=%d card=%d" % (t, card(S)))
            if C.dim == 1:
                lo, hi = min(S) - 1, max(S) + 1
                print("     " + frame1d(S, lo, hi))
            else:
                for r in frame2d(S, framebox):
                    print("     " + r)
            S = step(S, C, mode)
    return out


if __name__ == "__main__":
    O = (0, 0)
    # the additive control: the Pascal column of chapter one
    dossier("PASCAL COLUMN (own-kind, 1 kind)",
            Const([((0, 0), (1, 0), (0, 1))], dim=2),
            state_of([((0, 0), 0)]), "parity", T=70)
