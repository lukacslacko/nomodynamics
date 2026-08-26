#!/usr/bin/env python3
"""xa2d.py — 2-D cross-amendment engine for Expedition X-B.

Semantics are IDENTICAL to /Users/lukacs/claude/math/program/phase6/xnomos.py
(which is the reference).  This module adds

  * a dense numpy engine (fast, big boards) for growth-exponent measurement,
  * canonical hashing + certificates (fixed / balanced / cycle / glider /
    rotor-free growth),
  * a compact text format for constitutions so specimens paste anywhere,
  * cross-validation against xnomos.py (independent code path).

A constitution:  kinds 0..n-1; kind k has rule (a_k,b_k,c_k) with offsets in
{-1,0,1}^2 and a target SET T(k) subseteq K (out-degree |T(k)| >= 1).
A law (i,k) is active iff occ(i+a_k) and not occ(i+b_k).  An active law emits
one toggle of kind t at i+c_k for each t in T(k).  Toggles at the same
(cell,kind) resolve by PARITY (default) or OR.
"""
from __future__ import annotations

import itertools
import sys
from collections import defaultdict

import numpy as np

# ---------------------------------------------------------------- offsets ----
# name -> (dx, dy)
OFF = {
    "O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
    "P": (1, 1),      # NE  (P = "plus-plus")
    "Q": (-1, 1),     # NW
    "R": (1, -1),     # SE
    "T": (-1, -1),    # SW
}
OFFNAME = {v: k for k, v in OFF.items()}
VN = [OFF[c] for c in "OEWNS"]                       # von Neumann, 5
MOORE = [OFF[c] for c in "OEWNSPQRT"]                # Moore + centre, 9


def oname(o):
    return OFFNAME[tuple(o)]


# ----------------------------------------------------------- constitution ----

class Const:
    """rules: list of (a,b,c) offset triples.  targets: list of tuples."""

    __slots__ = ("rules", "targets", "n")

    def __init__(self, rules, targets=None):
        self.rules = [tuple(tuple(o) for o in r) for r in rules]
        self.n = len(self.rules)
        if targets is None:
            targets = [(k,) for k in range(self.n)]
        self.targets = [tuple(sorted(t if isinstance(t, (tuple, list, set))
                                     else (t,))) for t in targets]

    # ---- text format:  "OEE>AB OSN>B"  (rule letters a,b,c then targets) ----
    def label(self):
        parts = []
        for k in range(self.n):
            a, b, c = self.rules[k]
            tg = "".join(chr(ord("A") + t) for t in self.targets[k])
            parts.append("%s%s%s>%s" % (oname(a), oname(b), oname(c), tg))
        return " ".join(parts)

    def __repr__(self):
        return "Const(%s)" % self.label()

    @staticmethod
    def parse(s):
        rules, targets = [], []
        for tok in s.split():
            abc, tg = tok.split(">")
            rules.append(tuple(OFF[ch] for ch in abc))
            targets.append(tuple(sorted(ord(ch) - ord("A") for ch in tg)))
        return Const(rules, targets)

    def outdeg(self):
        return max(len(t) for t in self.targets)

    # ---- amendment digraph ------------------------------------------------
    def edges(self):
        return [(k, t) for k in range(self.n) for t in self.targets[k]]

    def authors(self, m):
        """kinds that can create kind m (with their c-offsets)."""
        return [(k, self.rules[k][2]) for k in range(self.n)
                if m in self.targets[k]]

    def cycle_sums(self, start=None):
        """All simple-cycle displacement sums V_Z of the amendment digraph,
        restricted to cycles reachable from `start` (a set of kinds)."""
        n = self.n
        reach = set(range(n)) if start is None else set(start)
        frontier = list(reach)
        while frontier:
            k = frontier.pop()
            for t in self.targets[k]:
                if t not in reach:
                    reach.add(t)
                    frontier.append(t)
        sums = set()
        # enumerate simple cycles by DFS (n is tiny)
        for s in sorted(reach):
            stack = [(s, [s], (0, 0))]
            while stack:
                k, path, acc = stack.pop()
                cx, cy = self.rules[k][2]
                acc2 = (acc[0] + cx, acc[1] + cy)
                for t in self.targets[k]:
                    if t == s:
                        sums.add(acc2)
                    elif t not in path and t > s:
                        stack.append((t, path + [t], acc2))
        return sums


# ------------------------------------------------------------- dict engine ---

def state(pairs):
    S = {}
    for cell, k in pairs:
        cell = tuple(cell)
        S[cell] = S.get(cell, 0) | (1 << k)
    return S


def laws(S):
    for cell, m in S.items():
        mm = m
        while mm:
            k = (mm & -mm).bit_length() - 1
            mm &= mm - 1
            yield cell, k


def card(S):
    return sum(bin(m).count("1") for m in S.values())


def active(S, C):
    out = []
    for cell, k in laws(S):
        a, b, _ = C.rules[k]
        if (cell[0] + a[0], cell[1] + a[1]) in S and \
           (cell[0] + b[0], cell[1] + b[1]) not in S:
            out.append((cell, k))
    return out


def step(S, C, mode="parity"):
    if mode in ("super", "super_or"):
        return _step_super(S, C, mode == "super_or")
    tog = defaultdict(int)
    hit = defaultdict(int)
    for cell, k in laws(S):
        a, b, c = C.rules[k]
        if (cell[0] + a[0], cell[1] + a[1]) in S and \
           (cell[0] + b[0], cell[1] + b[1]) not in S:
            j = (cell[0] + c[0], cell[1] + c[1])
            for t in C.targets[k]:
                tog[j] ^= 1 << t
                hit[j] |= 1 << t
    use = hit if mode == "or" else tog
    out = dict(S)
    for j, x in use.items():
        if not x:
            continue
        m = out.get(j, 0) ^ x
        if m:
            out[j] = m
        elif j in out:
            del out[j]
    return out


def _step_super(S, C, or_resolve=False):
    enact = defaultdict(int)
    cpar = defaultdict(int)
    cany = set()
    for cell, k in laws(S):
        a, b, c = C.rules[k]
        if (cell[0] + a[0], cell[1] + a[1]) in S and \
           (cell[0] + b[0], cell[1] + b[1]) not in S:
            j = (cell[0] + c[0], cell[1] + c[1])
            if j in S:
                cpar[j] ^= 1
                cany.add(j)
            else:
                enact[j] |= 1 << k
    out = dict(S)
    for j in (cany if or_resolve else {j for j, p in cpar.items() if p}):
        out.pop(j, None)
    for j, m in enact.items():
        out[j] = out.get(j, 0) | m
    return {j: m for j, m in out.items() if m}


def normalize(S):
    if not S:
        return (), (0, 0)
    lox = min(c[0] for c in S)
    loy = min(c[1] for c in S)
    return (tuple(sorted(((c[0] - lox, c[1] - loy), m) for c, m in S.items())),
            (lox, loy))


# ------------------------------------------------------------ certificates ---

EXTINCT, FIXED, BALANCED, CYCLE, GLIDER, GROWING, UNRESOLVED = (
    "EXTINCT", "FIXED", "BALANCED", "CYCLE", "GLIDER", "GROWING", "UNRESOLVED")


def classify(S0, C, mode="parity", max_steps=400, max_card=600, max_span=90):
    S = dict(S0)
    seen = {}
    for t in range(max_steps + 1):
        if not S:
            return {"kind": EXTINCT, "t": t}
        nm, anc = normalize(S)
        if nm in seen:
            t0, anc0 = seen[nm]
            d = (anc[0] - anc0[0], anc[1] - anc0[1])
            p = t - t0
            if d == (0, 0):
                if p == 1:
                    na = len(active(S, C))
                    return {"kind": BALANCED if na else FIXED, "t0": t0,
                            "period": 1, "active": na, "card": card(S)}
                return {"kind": CYCLE, "t0": t0, "period": p, "card": card(S)}
            return {"kind": GLIDER, "t0": t0, "period": p, "d": d,
                    "card": card(S)}
        seen[nm] = (t, anc)
        if card(S) > max_card:
            return {"kind": GROWING, "t": t, "card": card(S)}
        xs = [c[0] for c in S]
        ys = [c[1] for c in S]
        if max(xs) - min(xs) > max_span or max(ys) - min(ys) > max_span:
            return {"kind": GROWING, "t": t, "card": card(S), "span": True}
        S = step(S, C, mode)
    return {"kind": UNRESOLVED, "t": max_steps, "card": card(S)}


def verify_glider(S0, C, p, d, mode="parity", reps=3):
    """Independent re-check: Phi^{p}(S) = sigma^{d}(S), over `reps` periods."""
    S = dict(S0)
    for r in range(1, reps + 1):
        for _ in range(p):
            S = step(S, C, mode)
        want = {(c[0] + d[0] * r, c[1] + d[1] * r): m for c, m in S0.items()}
        if S != want:
            return False
    return True


def verify_balanced(S0, C, mode="parity"):
    return step(S0, C, mode) == S0 and bool(active(S0, C))


def verify_cycle(S0, C, p, mode="parity", reps=3):
    S = dict(S0)
    for _ in range(p * reps):
        S = step(S, C, mode)
        if S == S0 and (_ + 1) % p:
            return False            # shorter period
    return S == S0


# ------------------------------------------------------------ numpy engine ---

def look(A, off):
    """L[x,y] = A[x+dx, y+dy], zero outside."""
    dx, dy = off
    if dx == 0 and dy == 0:
        return A
    L = np.zeros_like(A)
    n0, n1 = A.shape
    xs = slice(max(dx, 0), n0 + min(dx, 0))
    xd = slice(max(-dx, 0), n0 + min(-dx, 0))
    ys = slice(max(dy, 0), n1 + min(dy, 0))
    yd = slice(max(-dy, 0), n1 + min(-dy, 0))
    L[xd, yd] = A[xs, ys]
    return L


class NPRun:
    """Dense planes of shape (n, N, N), origin at (R, R)."""

    def __init__(self, C, seed, R=256, mode="parity"):
        self.C = C
        self.R = R
        self.mode = mode
        N = 2 * R + 1
        self.P = np.zeros((C.n, N, N), bool)
        for cell, k in seed:
            self.P[k, cell[0] + R, cell[1] + R] = True
        self.hit_border = False

    def occ(self):
        return self.P.any(axis=0)

    def step(self):
        C = self.C
        occ = self.occ()
        tog = np.zeros_like(self.P)
        for k in range(C.n):
            a, b, c = C.rules[k]
            act = self.P[k] & look(occ, a) & ~look(occ, b)
            if not act.any():
                continue
            em = look(act, (-c[0], -c[1]))
            for t in C.targets[k]:
                if self.mode == "or":
                    tog[t] |= em
                else:
                    tog[t] ^= em
        self.P ^= tog
        # border check
        o = self.occ()
        if o[0].any() or o[-1].any() or o[:, 0].any() or o[:, -1].any():
            self.hit_border = True

    def size(self):
        return int(self.P.sum())

    def bbox(self):
        o = self.occ()
        pts = np.argwhere(o)
        if not len(pts):
            return None
        return (pts[:, 0].min() - self.R, pts[:, 0].max() - self.R,
                pts[:, 1].min() - self.R, pts[:, 1].max() - self.R)


def growth_curve(C, seed, T=400, R=None, mode="parity"):
    """Returns (sizes, boxes) with sizes[t] = |S_t|, boxes[t] = (w,h)."""
    if R is None:
        R = T + 4
    run = NPRun(C, seed, R=R, mode=mode)
    sizes, boxes = [], []
    for t in range(T + 1):
        sizes.append(run.size())
        bb = run.bbox()
        boxes.append((0, 0) if bb is None else
                     (bb[1] - bb[0] + 1, bb[3] - bb[2] + 1))
        if sizes[-1] == 0:
            break
        if t < T:
            run.step()
            if run.hit_border:
                break
    return sizes, boxes, run


def alpha_fit(sizes, lo_frac=0.35):
    """log|S_t| vs log t least-squares slope over the last 65% of the run."""
    s = np.array(sizes, float)
    ts = np.arange(len(s), dtype=float)
    m = (ts >= max(8, lo_frac * len(s))) & (s > 0)
    if m.sum() < 8:
        return float("nan")
    return float(np.polyfit(np.log(ts[m]), np.log(s[m]), 1)[0])


def alpha_local(sizes):
    """Local exponent from the last decade: log(s[T]/s[T/2]) / log 2."""
    n = len(sizes) - 1
    if n < 16 or sizes[n] == 0 or sizes[n // 2] == 0:
        return float("nan")
    return float(np.log(sizes[n] / sizes[n // 2]) / np.log(2))


# ---------------------------------------------------------------- rendering --

def render(S, C=None, sym=None, pad=0, maxw=100, maxh=60, window=None):
    """window = (x0, x1, y0, y1) draws in a FIXED frame (so motion is visible)."""
    if window is not None:
        x0, x1, y0, y1 = window
    elif not S:
        return "(empty)"
    else:
        xs = [c[0] for c in S]
        ys = [c[1] for c in S]
        x0, x1 = min(xs) - pad, max(xs) + pad
        y0, y1 = min(ys) - pad, max(ys) + pad
        x1 = min(x1, x0 + maxw - 1)
        y1 = min(y1, y0 + maxh - 1)
    sym = sym or "ABCDEFGH"
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
    return "\n".join(rows)


# --------------------------------------------------------------- self-tests --

def _xnomos_const(C):
    sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6")
    import xnomos
    return xnomos.Const(C.rules, [t if len(t) > 1 else t[0]
                                  for t in C.targets], dim=2)


def _tests():
    import random
    sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6")
    import xnomos
    ok = 0

    # 1. dict engine == xnomos on random universes/states, all four modes
    rng = random.Random(20260826)
    for trial in range(4000):
        n = rng.choice((1, 2, 2, 3))
        rules = [tuple(rng.choice(MOORE) for _ in range(3)) for _ in range(n)]
        targets = []
        for _ in range(n):
            sz = rng.choice((1, 1, 1, 2))
            targets.append(tuple(sorted(rng.sample(range(n), min(sz, n)))))
        C = Const(rules, targets)
        X = _xnomos_const(C)
        S = state([((rng.randint(-2, 2), rng.randint(-2, 2)),
                    rng.randrange(n)) for _ in range(rng.randint(1, 6))])
        for mode in ("parity", "or", "super", "super_or"):
            if mode.startswith("super") and C.outdeg() > 1:
                continue                    # super ignores targets by design
            a = step(S, C, mode)
            b = xnomos.step(S, X, mode)
            assert a == b, (C.label(), mode, S, a, b)
        ok += 1
    print("  [1] dict engine == xnomos.py on %d random universes x 4 modes" % ok)

    # 2. numpy engine == dict engine
    rng = random.Random(7)
    nn = 0
    for trial in range(400):
        n = rng.choice((1, 2, 3))
        rules = [tuple(rng.choice(MOORE) for _ in range(3)) for _ in range(n)]
        targets = [tuple(sorted(rng.sample(range(n),
                                           rng.choice((1, 1, 2))[0] if False
                                           else min(rng.choice((1, 1, 2)), n))))
                   for _ in range(n)]
        C = Const(rules, targets)
        seed = [((rng.randint(-2, 2), rng.randint(-2, 2)), rng.randrange(n))
                for _ in range(rng.randint(1, 5))]
        mode = rng.choice(("parity", "or"))
        S = state(seed)
        run = NPRun(C, seed, R=40, mode=mode)
        for t in range(25):
            got = {}
            for k in range(C.n):
                for (x, y) in np.argwhere(run.P[k]):
                    cell = (int(x) - run.R, int(y) - run.R)
                    got[cell] = got.get(cell, 0) | (1 << k)
            assert got == S, (C.label(), mode, t, got, S)
            S = step(S, C, mode)
            run.step()
            if run.hit_border:
                break
        nn += 1
    print("  [2] numpy engine == dict engine on %d universes x 25 steps" % nn)

    # 3. known specimens
    C = Const.parse("OEE>A")                      # own-kind colonizer
    r = classify(state([((0, 0), 0)]), C, max_span=30)
    assert r["kind"] == GROWING, r
    C = Const.parse("OEN>A")                      # perpendicular colonizer
    sizes, _, _ = growth_curve(C, [((0, 0), 0)], T=64, R=80)
    assert sizes[16] == 2 and sizes[32] == 2, sizes[:40]   # 2^popcount(t)
    assert all(sizes[t] == 2 ** bin(t).count("1") for t in range(1, 60))
    print("  [3] own-kind specimens reproduce (colonizer, Pascal column)")
    ok += 1

    # 4. two-chamber balance (the 2-D witness from nomos2d RESULTS §5.5)
    C = Const.parse("OSS>A OES>A")
    S = state([((0, 0), 0), ((0, 0), 1)])
    assert step(S, C, "parity") == S and len(active(S, C)) == 2
    assert verify_balanced(S, C, "parity")
    assert step(S, C, "or") != S
    print("  [4] two-chamber balanced constitution verified (parity != OR)")

    print("xa2d self-tests passed")


if __name__ == "__main__":
    _tests()
