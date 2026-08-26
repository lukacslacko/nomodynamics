"""Shared helpers for the BALLISTIC (glider-collision) sector, Expedition Y-B.

Chapter-two semantics only: occupancy guards (guards=None), 1-D, modes
'parity' and 'or'.  Everything routes through xnomos.
"""
import sys, os, itertools
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6")
from xnomos import (Const, state_of, step, classify, verify_glider, render,
                    spacetime, card, laws, active_laws, normalize, freeze,
                    EXTINCT, FIXED, BALANCED, CYCLE, GLIDER, GROWING,
                    UNRESOLVED)


def mirror_const(C):
    """Negate every offset of every rule; keep targets/kinds.  The reflection
    x -> -x of the universe."""
    return Const([(-a, -b, -c) for (a, b, c) in C.rules],
                 targets=[t for t in C.targets], dim=C.dim, modulus=C.modulus)


def mirror_state(S):
    """Reflect a state through 0."""
    return {-c: m for c, m in S.items()}


def shift(S, d):
    return {c + d: m for c, m in S.items()}


def union(*states):
    out = {}
    for S in states:
        for c, m in S.items():
            out[c] = out.get(c, 0) | m
    return out


def disjoint_union(A, B):
    """Union, but reports whether supports overlapped."""
    ov = set(A) & set(B)
    return union(A, B), bool(ov)


def orbit(S0, C, mode, p):
    """The p states of a period-p orbit (phases 0..p-1)."""
    out, S = [], dict(S0)
    for _ in range(p):
        out.append(dict(S))
        S = step(S, C, mode)
    return out


def span(S):
    return (max(S) - min(S)) if S else -1


def find_gliders(C, mode, max_kinds=None, max_cells=4, cell_range=range(0, 5),
                 max_steps=200, max_card=60, max_span=120):
    """Complete sweep of seeds with support inside cell_range, up to max_cells
    placed laws.  Returns list of (seed_pairs, result_dict)."""
    n = C.n if max_kinds is None else max_kinds
    slots = [(c, k) for c in cell_range for k in range(n)]
    found = []
    for r in range(1, max_cells + 1):
        for combo in itertools.combinations(slots, r):
            cells = [c for c, _ in combo]
            if min(cells) != min(cell_range):
                continue            # canonical: anchored at left edge
            S = state_of(combo)
            res = classify(S, C, mode, max_steps=max_steps,
                           max_card=max_card, max_span=max_span)
            if res["kind"] == GLIDER:
                found.append((combo, res))
    return found


def bucket_name(res, C, mode):
    return res["kind"]
