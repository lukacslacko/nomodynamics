#!/usr/bin/env python3
"""
xlib.py — Expedition X-D support library.

Two things live here:

  (A) An INDEPENDENT reference engine (`ref_step`) written in a deliberately
      different style from `xnomos.step`: states are *sets of (cell, kind)
      pairs*, toggles are accumulated in an explicit multiset, and resolution
      is applied by counting.  Every positive claim in RESULTS.md is
      re-verified through this path.

  (B) Structure-theory predicates: the amendment functional graph, its cycle
      offset-sums, the path-sum reach set, entrenchment/amendability of a code,
      and the checkers for the theorems of the survival audit.

Import path assumes the parent directory (which holds xnomos.py) is on sys.path.
"""

from __future__ import annotations

import itertools
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xnomos as X                                                    # noqa: E402
from xnomos import Const, state_of, laws, card, active_laws           # noqa: E402

OFF1 = (-1, 0, 1)
RULES1 = [(a, b, c) for a in OFF1 for b in OFF1 for c in OFF1]


# ============================================================ (A) reference engine

def to_pairs(S):
    """xnomos state (dict cell->mask) -> frozenset of (cell, kind)."""
    return frozenset(laws(S))


def from_pairs(P):
    return state_of(P)


def ref_step(P, C, mode="parity"):
    """Independent step.  P is a frozenset of (cell, kind).  Returns frozenset.

    Deliberately different implementation: explicit toggle multiset, explicit
    resolution by counting, sets rather than bitmasks.
    """
    occ = {cell for cell, _ in P}
    act = []
    for (cell, k) in P:
        a, b, _ = C.rules[k]
        if C.add(cell, a) in occ and C.add(cell, b) not in occ:
            act.append((cell, k))

    if mode in ("super", "super_or"):
        clears = []          # list of cells voted clear
        enacts = set()       # (cell, kind) enacted
        for (cell, k) in act:
            j = C.add(cell, C.rules[k][2])
            if j in occ:
                clears.append(j)
            else:
                enacts.add((j, k))
        cnt = defaultdict(int)
        for j in clears:
            cnt[j] += 1
        if mode == "super_or":
            killed = set(cnt)
        else:
            killed = {j for j, n in cnt.items() if n % 2 == 1}
        out = {(c, k) for (c, k) in P if c not in killed}
        return frozenset(out | enacts)

    mult = defaultdict(int)                      # (cell, kind) -> toggle count
    for (cell, k) in act:
        j = C.add(cell, C.rules[k][2])
        for t in C.targets[k]:
            mult[(j, t)] += 1
    if mode == "or":
        flip = {s for s, n in mult.items() if n >= 1}
    elif mode == "parity":
        flip = {s for s, n in mult.items() if n % 2 == 1}
    else:
        raise ValueError(mode)
    return frozenset(P.symmetric_difference(flip))


def duel(S, C, steps, mode="parity"):
    """Advance xnomos and the reference engine in lockstep; assert equality."""
    P = to_pairs(S)
    T = dict(S)
    for n in range(steps):
        if to_pairs(T) != P:
            return False, n
        T = X.step(T, C, mode)
        P = ref_step(P, C, mode)
    return to_pairs(T) == P, steps


def max_multiplicity(S, C):
    """Largest number of toggles any single (cell, kind) slot receives."""
    mult = defaultdict(int)
    for (cell, k) in active_laws(S, C):
        j = C.add(cell, C.rules[k][2])
        for t in C.targets[k]:
            mult[(j, t)] += 1
    return max(mult.values()) if mult else 0


# ==================================================== (B) the amendment graph

def single_targets(C):
    return [t[0] for t in C.targets]


def in_degrees(C):
    d = [0] * C.n
    for k in range(C.n):
        for t in C.targets[k]:
            d[t] += 1
    return d


def rho(C, k):
    """Forward orbit of kind k in the functional graph: (tail, cycle)."""
    t = single_targets(C)
    seen, path = {}, []
    x = k
    while x not in seen:
        seen[x] = len(path)
        path.append(x)
        x = t[x]
    i = seen[x]
    return path[:i], path[i:]


def components_cycles(C):
    """All distinct cycles of the functional graph, as lists of kinds."""
    out, done = [], set()
    for k in range(C.n):
        _, cyc = rho(C, k)
        key = frozenset(cyc)
        if key not in done:
            done.add(key)
            out.append(cyc)
    return out


def _vadd(u, v):
    if isinstance(u, tuple):
        return tuple(x + y for x, y in zip(u, v))
    return u + v


def _vzero(dim):
    return 0 if dim == 1 else tuple([0] * dim)


def cycle_offset_sum(C, cyc):
    s = _vzero(C.dim)
    for k in cyc:
        s = _vadd(s, C.rules[k][2])
    return s


def path_sums(C, k, R):
    """C_r(k) = c_k + c_{t(k)} + ... for r = 0..R, plus the kind reached."""
    t = single_targets(C)
    out, s, x = [], _vzero(C.dim), k
    for _ in range(R + 1):
        out.append((x, s))
        s = _vadd(s, C.rules[x][2])
        x = t[x]
    return out


def reach_set(C, S0, R):
    """Path-sum over-approximation of every (cell, kind) ever occupied."""
    out = set()
    for cell, k in laws(S0):
        for kind, off in path_sums(C, k, R):
            out.add((C.add(cell, off), kind))
    return out


# -------------------------------------------------- code-level predicates

def active_alphabet(S, C):
    return {k for _, k in active_laws(S, C)}


def present_alphabet(S):
    return {k for _, k in laws(S)}


def target_image(C, ks):
    out = set()
    for k in ks:
        out.update(C.targets[k])
    return out


def entrenched_kinds(S, C):
    """Kinds present in S that NO active law of S targets: unamendable now."""
    return present_alphabet(S) - target_image(C, active_alphabet(S, C))


def toggled_slots(S, C):
    mult = defaultdict(int)
    for (cell, k) in active_laws(S, C):
        j = C.add(cell, C.rules[k][2])
        for t in C.targets[k]:
            mult[(j, t)] += 1
    return mult


def is_balanced(S, C, mode="parity"):
    """Fixed point with >= 1 active law, verified through BOTH engines."""
    a = X.step(dict(S), C, mode) == dict(S)
    P = to_pairs(S)
    b = ref_step(P, C, mode) == P
    assert a == b, "engine disagreement on fixedness"
    return a and bool(active_laws(S, C))


def occupancy(S):
    return frozenset(S)


def is_cryptic(S, C, mode="parity", max_steps=64):
    """Constant occupancy, non-constant state: a 'cryptic' code.

    Returns (True, period) if occ(S_n) is constant over a full recurrence and
    the state actually changes; else (False, None).
    """
    occ0 = occupancy(S)
    T = dict(S)
    seen = {X.freeze(T): 0}
    for n in range(1, max_steps + 1):
        T = X.step(T, C, mode)
        if occupancy(T) != occ0:
            return False, None
        f = X.freeze(T)
        if f in seen:
            p = n - seen[f]
            return (seen[f] == 0 and p >= 2), p
        seen[f] = n
    return False, None


# ------------------------------------------------------------ enumeration

def seeds_span(span, nkinds=2):
    """All codes whose support spans exactly `span` cells, leftmost cell 0.

    Every cell carries a nonempty-or-empty subset of kinds; cells 0 and
    span-1 must be nonempty.  Canonical (translation-normalised).
    """
    full = 1 << nkinds
    if span == 1:
        for m in range(1, full):
            yield {0: m}
        return
    for first in range(1, full):
        for mid in itertools.product(range(full), repeat=span - 2):
            for last in range(1, full):
                S = {0: first, span - 1: last}
                for i, m in enumerate(mid):
                    if m:
                        S[i + 1] = m
                yield S


def all_seeds(max_span, nkinds=2):
    for s in range(1, max_span + 1):
        yield from seeds_span(s, nkinds)


# ------------------------------------------------------------- symmetries

def mirror_rule(r):
    a, b, c = r
    return (-a, -b, -c)


def mirror_const(C):
    return Const([mirror_rule(r) for r in C.rules],
                 [t if len(t) > 1 else t[0] for t in C.targets],
                 dim=C.dim, modulus=C.modulus)


def relabel_const(C, perm):
    """perm: list, new kind i is old kind perm[i].  inv[old] = new."""
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    rules = [C.rules[perm[i]] for i in range(len(perm))]
    tg = []
    for i in range(len(perm)):
        old = C.targets[perm[i]]
        new = tuple(sorted(inv[t] for t in old))
        tg.append(new if len(new) > 1 else new[0])
    return Const(rules, tg, dim=C.dim, modulus=C.modulus)


def const_key(C):
    return (tuple(C.rules), tuple(tuple(t) for t in C.targets))


def orbit(C, perms):
    out = set()
    for P in perms:
        D = relabel_const(C, P)
        out.add(const_key(D))
        out.add(const_key(mirror_const(D)))
    return out


if __name__ == "__main__":
    # smoke test: reference engine agrees with xnomos on the published specimens
    import random
    rng = random.Random(2026)
    bad = 0
    for mode in ("parity", "or", "super", "super_or"):
        for _ in range(400):
            n = rng.randrange(1, 4)
            C = Const([rng.choice(RULES1) for _ in range(n)],
                      [rng.randrange(n) for _ in range(n)])
            S = state_of([(rng.randrange(-4, 5), rng.randrange(n))
                          for _ in range(rng.randrange(1, 6))])
            ok, at = duel(S, C, 40, mode)
            if not ok:
                bad += 1
                print("DIVERGENCE", mode, C.label(), S, at)
    print("xlib duel smoke test: %d divergences in 1600 trajectories" % bad)
