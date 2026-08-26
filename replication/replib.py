#!/usr/bin/env python3
"""
replib.py — replication detection for nomodynamics (Expedition Y-C).

Two things live here.

(1) An INDEPENDENT re-implementation of the nomodynamic update, `pstep`, whose
    state is a frozenset of placed laws (cell, kind) rather than the engine's
    dict {cell: bitmask}.  Every certificate in RESULTS.md is checked against
    `xnomos.step` AND against `pstep`; they were written from the definition
    separately and share no code.

(2) The replication detector.  Given a seed S0 and a later state S_t, it finds
    every translation d with sigma^d(S0) contained in S_t, then extracts a
    maximum family of pairwise CAUSALLY SEPARATED copies (see `sep_ok`) and
    reports the debris.

Definitions used (see RESULTS.md sec. 2 for the pre-registered statement):

  R(C)          = max sup-norm over every offset a_k, b_k, c_k of the
                  constitution.  Two law-sets separated by more than 2R cannot
                  read, block or write onto each other in one step (Lemma S).
  copy          = a translate sigma^d(S0) whose placed laws all occur in S_t.
  free copies   = a set of copies that are pairwise separated by > 2R.
  debris        = S_t minus the chosen copies.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from xnomos import Const, state_of, card, step, laws          # noqa: E402


# --------------------------------------------------------------- independent
# A "pstate" is a frozenset of (cell, kind).  Nothing below touches xnomos.

def to_p(S):
    """dict-of-bitmask state  ->  frozenset of (cell, kind)."""
    out = []
    for cell, m in S.items():
        for k in range(m.bit_length()):
            if (m >> k) & 1:
                out.append((cell, k))
    return frozenset(out)


def from_p(P):
    """frozenset of (cell, kind)  ->  dict-of-bitmask state."""
    S = {}
    for cell, k in P:
        S[cell] = S.get(cell, 0) | (1 << k)
    return S


def _padd(C, cell, off):
    if C.dim == 1:
        j = cell + off
        return j % C.modulus if C.modulus is not None else j
    return tuple(x + y for x, y in zip(cell, off))


def pstep(P, C, mode="parity"):
    """One step, written from the definition on frozensets of placed laws."""
    occupied = {cell for cell, _ in P}
    kinds_at = defaultdict(set)
    for cell, k in P:
        kinds_at[cell].add(k)

    fired = []                                     # (target cell, kind) writes
    clears = []                                    # supersession clear votes
    enacts = []                                    # supersession enact votes
    for cell, k in P:
        a, b, c = C.rules[k]
        g, h = C.guards[k]
        pa = _padd(C, cell, a)
        if g is None:
            if pa not in occupied:
                continue
        elif g not in kinds_at.get(pa, ()):
            continue
        pb = _padd(C, cell, b)
        if h is None:
            if pb in occupied:
                continue
        elif h in kinds_at.get(pb, ()):
            continue
        j = _padd(C, cell, c)
        if mode in ("super", "super_or"):
            if j in occupied:
                clears.append(j)
            else:
                enacts.append((j, k))
        else:
            for t in C.targets[k]:
                fired.append((j, t))

    if mode in ("super", "super_or"):
        if mode == "super_or":
            gone = set(clears)
        else:
            cnt = defaultdict(int)
            for j in clears:
                cnt[j] ^= 1
            gone = {j for j, v in cnt.items() if v}
        out = {(cell, k) for cell, k in P if cell not in gone}
        out |= set(enacts)
        return frozenset(out)

    if mode == "or":
        flips = set(fired)
    else:
        cnt = defaultdict(int)
        for x in fired:
            cnt[x] ^= 1
        flips = {x for x, v in cnt.items() if v}
    return frozenset(P) ^ flips


def cross_check(S0, C, mode, steps):
    """Run both engines in lockstep; return True iff they agree throughout."""
    S = dict(S0)
    P = to_p(S0)
    for _ in range(steps):
        S = step(S, C, mode)
        P = pstep(P, C, mode)
        if to_p(S) != P:
            return False
    return True


# ------------------------------------------------------------------ geometry

def radius(C):
    """R(C): the sup-norm interaction radius of the constitution."""
    r = 0
    for a, b, c in C.rules:
        for off in (a, b, c):
            if C.dim == 1:
                r = max(r, abs(off))
            else:
                r = max(r, max(abs(x) for x in off))
    return r


def shift(S, d, dim=1):
    if dim == 1:
        return {c + d: m for c, m in S.items()}
    return {tuple(x + y for x, y in zip(c, d)): m for c, m in S.items()}


def supp(S):
    return set(S.keys())


def dist_inf(A, B, dim=1):
    """min sup-norm distance between two nonempty cell sets (brute force)."""
    best = None
    for p in A:
        for q in B:
            if dim == 1:
                v = abs(p - q)
            else:
                v = max(abs(x - y) for x, y in zip(p, q))
            if best is None or v < best:
                best = v
                if best == 0:
                    return 0
    return best


def contains(T, U):
    """Is every placed law of U present in T?  (bitmask containment)"""
    for c, m in U.items():
        if (T.get(c, 0) & m) != m:
            return False
    return True


def diff(T, U):
    """T minus U as placed laws."""
    out = {}
    for c, m in T.items():
        r = m & ~U.get(c, 0)
        if r:
            out[c] = r
    return out


# ----------------------------------------------------------------- detection

def copy_offsets(St, S0, dim=1):
    """All d with sigma^d(S0) contained in St.  Anchored on one law of S0."""
    if not S0 or not St:
        return []
    anchor_cell = min(S0)
    anchor_mask = S0[anchor_cell]
    out = []
    for cell, m in St.items():
        if (m & anchor_mask) != anchor_mask:
            continue
        d = cell - anchor_cell if dim == 1 else tuple(
            x - y for x, y in zip(cell, anchor_cell))
        if contains(St, shift(S0, d, dim)):
            out.append(d)
    return out


def max_disjoint(St, S0, ds, dim=1, sep=0):
    """Greedy-then-exact max family of copies pairwise separated by > sep.

    sep = 0 means only support-disjointness is required.
    Exact for small |ds| (<= 16) by bitmask DP, greedy above.
    """
    if not ds:
        return []
    sups = [supp(shift(S0, d, dim)) for d in ds]
    n = len(ds)
    ok = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if sups[i] & sups[j]:
                good = False
            elif sep == 0:
                good = True
            else:
                good = dist_inf(sups[i], sups[j], dim) > sep
            ok[i][j] = ok[j][i] = good
    if n <= 18:                                       # exact max clique
        best = []
        adj = [0] * n
        for i in range(n):
            for j in range(n):
                if ok[i][j]:
                    adj[i] |= 1 << j

        def expand(chosen, cand):
            nonlocal best
            if bin(cand).count("1") + len(chosen) <= len(best):
                return
            if not cand:
                if len(chosen) > len(best):
                    best = list(chosen)
                return
            m = cand
            while m:
                i = (m & -m).bit_length() - 1
                m &= m - 1
                expand(chosen + [i], cand & adj[i] & ~((1 << (i + 1)) - 1))
            if len(chosen) > len(best):
                best = list(chosen)
        expand([], (1 << n) - 1)
        return [ds[i] for i in best]
    chosen = []
    for i in range(n):
        if all(ok[i][j] for j in chosen):
            chosen.append(i)
    return [ds[i] for i in chosen]


def scan(S0, C, mode="parity", T=64, max_card=4000, sep=None, min_copies=2):
    """Run S0 for T steps; report every time with >= min_copies free copies.

    Yields dicts with t, the chosen offsets, the debris and whether the
    decomposition is EXACT (debris empty).
    """
    dim = C.dim
    R = radius(C)
    sep = 2 * R if sep is None else sep
    S = dict(S0)
    hits = []
    for t in range(1, T + 1):
        S = step(S, C, mode)
        if not S or card(S) > max_card:
            break
        ds = copy_offsets(S, S0, dim)
        if len(ds) < min_copies:
            continue
        fam = max_disjoint(S, S0, ds, dim, sep)
        if len(fam) < min_copies:
            continue
        cov = {}
        for d in fam:
            for c, m in shift(S0, d, dim).items():
                cov[c] = cov.get(c, 0) | m
        deb = diff(S, cov)
        hits.append({"t": t, "offsets": sorted(fam), "n_copies": len(fam),
                     "debris_card": card(deb), "debris": deb,
                     "exact": not deb, "card": card(S), "R": R, "sep": sep})
    return hits


# ---------------------------------------------------------------- certificate

def certify(S0, C, mode, p, offsets, verbose=False):
    """Independent re-check of one replication event.

    Re-runs p steps with `pstep` (the frozenset engine), then verifies
      * every sigma^d(S0), d in offsets, occurs in the result,
      * the copies' supports are pairwise separated by > 2R,
      * reports the debris.
    Returns (ok, info).
    """
    dim = C.dim
    R = radius(C)
    P = to_p(S0)
    for _ in range(p):
        P = pstep(P, C, mode)
    St = from_p(P)
    info = {"card": card(St), "R": R}
    sups = []
    for d in offsets:
        U = shift(S0, d, dim)
        if not contains(St, U):
            return False, dict(info, fail="copy %s missing" % (d,))
        sups.append(supp(U))
    for i in range(len(sups)):
        for j in range(i + 1, len(sups)):
            if sups[i] & sups[j]:
                return False, dict(info, fail="copies %d,%d overlap" % (i, j))
            g = dist_inf(sups[i], sups[j], dim)
            if g <= 2 * R:
                return False, dict(info, fail="copies %d,%d gap %d <= 2R=%d"
                                   % (i, j, g, 2 * R))
            info.setdefault("gaps", []).append(g)
    cov = {}
    for d in offsets:
        for c, m in shift(S0, d, dim).items():
            cov[c] = cov.get(c, 0) | m
    deb = diff(St, cov)
    info["debris"] = deb
    info["debris_card"] = card(deb)
    info["exact"] = not deb
    info["state"] = St
    return True, info


# ------------------------------------------------------------- superposition

def superposes(C, mode, A, B):
    """Does Phi(A xor B) = Phi(A) xor Phi(B)?  (states as placed-law sets)"""
    PA, PB = to_p(A), to_p(B)
    lhs = pstep(PA ^ PB, C, mode)
    rhs = pstep(PA, C, mode) ^ pstep(PB, C, mode)
    return lhs == rhs


def linearity_report(C, mode, dim=1, span=4, trials=4000, seed=1):
    """Count superposition failures over random small pairs (overlapping)."""
    import random
    rng = random.Random(seed)
    n = C.n
    fails = 0
    for _ in range(trials):
        A, B = {}, {}
        for _ in range(rng.randrange(1, 4)):
            c = (rng.randrange(-span, span + 1) if dim == 1 else
                 (rng.randrange(-span, span + 1), rng.randrange(-span, span + 1)))
            A[c] = A.get(c, 0) | (1 << rng.randrange(n))
        for _ in range(rng.randrange(1, 4)):
            c = (rng.randrange(-span, span + 1) if dim == 1 else
                 (rng.randrange(-span, span + 1), rng.randrange(-span, span + 1)))
            B[c] = B.get(c, 0) | (1 << rng.randrange(n))
        if not superposes(C, mode, A, B):
            fails += 1
    return fails, trials


# --------------------------------------------------------------- ascii frames

def frame1d(S, lo, hi, sym="ABCDEFGH"):
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


def frame2d(S, box=None, sym="ABCDEFGH"):
    if not S:
        return ["."]
    xs = [c[0] for c in S]
    ys = [c[1] for c in S]
    x0, x1 = (min(xs), max(xs)) if box is None else (box[0], box[1])
    y0, y1 = (min(ys), max(ys)) if box is None else (box[2], box[3])
    rows = []
    for y in range(y1, y0 - 1, -1):
        r = []
        for x in range(x0, x1 + 1):
            m = S.get((x, y), 0)
            if not m:
                r.append(".")
            elif bin(m).count("1") > 1:
                r.append("#")
            else:
                r.append(sym[(m & -m).bit_length() - 1])
        rows.append("".join(r))
    return rows


if __name__ == "__main__":
    # engine agreement on a battery of random constitutions and seeds
    import random
    rng = random.Random(11)
    OFF = (-1, 0, 1)
    bad = 0
    for trial in range(400):
        n = rng.randrange(1, 4)
        rules = [(rng.choice(OFF), rng.choice(OFF), rng.choice(OFF))
                 for _ in range(n)]
        tg = []
        for _ in range(n):
            s = tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
            tg.append(s)
        gd = [(rng.choice([None] + list(range(n))),
               rng.choice([None] + list(range(n)))) for _ in range(n)]
        C = Const(rules, tg, dim=1, guards=gd)
        S = {}
        for _ in range(rng.randrange(1, 6)):
            S[rng.randrange(-4, 5)] = rng.randrange(1, 1 << n)
        for mode in ("parity", "or", "super", "super_or"):
            if not cross_check(S, C, mode, 12):
                bad += 1
                print("MISMATCH", mode, C.label(), S)
    print("replib: independent engine agrees with xnomos on 400x4 runs"
          if not bad else "replib: %d MISMATCHES" % bad)
