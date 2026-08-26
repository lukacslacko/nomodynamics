#!/usr/bin/env python3
"""
t3_core.py -- TARGET 3: the single-field sector of nomodynamics, reduced.

INDEPENDENT code path (written from the definition, not from xspeed/*.py).

THE SINGLE-FIELD SECTOR.  A constitution is *single-field* when T_k = K for
every kind k: every law amends every kind.  Then

  (SF1)  the increment  supp_m(t+1) - supp_m(t)  is the SAME set for every kind
         m, so  supp_m(t) \\Delta supp_{m'}(t)  is a constant of the motion;
  (SF2)  in a GLIDER that constant is a finite set equal to its own translate
         by d != 0, hence empty: every occupied cell carries ALL kinds.

So a single-field glider is a subset S of Z, and the update is a ONE-BIT
cellular automaton.  With window W = 1 (offsets in {-1,0,1}) we reduce further:

  A law (a,b,c) placed at i in S is active iff occ(i+a) and not occ(i+b).
  Writing  lam = occ(i-1),  rho = occ(i+1)  (and occ(i) = 1):

      (a,b) = (0,-1)  "L"  active iff lam = 0
      (a,b) = (0,+1)  "R"  active iff rho = 0
      (a,b) = (-1,+1) "P"  active iff lam = 1 and rho = 0
      (a,b) = (+1,-1) "Q"  active iff rho = 1 and lam = 0
      (a,b) = (-1,0) or (+1,0)  : never active (b = 0 demands occ(i) = 0)
      a = b                     : never active

  So a cell of S is one of four TYPES and its whole emission is determined by
  the type:

      type I  (isolated,  lam=0,rho=0):  active pairs {L,R}   -> vector  u
      type V  (left end,  lam=0,rho=1):  active pairs {L,Q}   -> vector  v
      type W  (right end, lam=1,rho=0):  active pairs {R,P}   -> vector  w
      type .  (interior,  lam=1,rho=1):  none                 -> 0   (GRIDLOCK)

  where, with L_c,R_c,P_c,Q_c the multiplicities of the channels (0,-1,c),
  (0,1,c), (-1,1,c), (1,-1,c),

      u_c = L_c + R_c,   v_c = L_c + Q_c,   w_c = R_c + P_c        (parity: mod 2)
      U_c = L_c | R_c,   V_c = L_c | Q_c,   W_c = R_c | P_c        (OR: as sets)

  and the toggle count at cell j is

      N(j) = E_{+1}(j-1) + E_0(j) + E_{-1}(j+1),      E(i) = u/v/w/0 by type,

  Phi(S) = S \\Delta {j : N(j) odd}          (parity)
  Phi(S) = S \\Delta {j : N(j) >= 1}         (OR)

CONSEQUENCE (the enumeration collapse).  The parity dynamics depends ONLY on
(u,v,w) in F_2^9: exactly 512 dynamics, ALL realisable, for ANY number of
kinds.  The OR dynamics depends only on (U,V,W) with U subset V u W: exactly
343 dynamics.  So a sweep over these classes settles the sector for EVERY n.

Bit convention throughout: a 3-bit vector x has bit 0 = component c=-1,
bit 1 = c=0, bit 2 = c=+1.
"""
from __future__ import annotations

import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

CM1, C0, CP1 = 1, 2, 4          # bit masks for c = -1, 0, +1

# ---------------------------------------------------------------- channels

def live_channels(W=1):
    """All (a,b,c) with |a|,|b|,|c| <= W.  (Dead ones included; see below.)"""
    rng = range(-W, W + 1)
    return [(a, b, c) for a in rng for b in rng for c in rng]


def is_ever_active(a, b, W=1):
    """Can a law (a,b,*) at an occupied cell ever be active at window W=1?"""
    if a == b:
        return False
    return b != 0                      # b = 0 demands occ(i) = 0, impossible


def channels_to_uvw(channels):
    """(u,v,w) in (F_2^3)^3, as three 3-bit ints -- the PARITY class at W=1."""
    u = v = w = 0
    for (a, b, c) in channels:
        assert max(abs(a), abs(b), abs(c)) <= 1, "W=1 only"
        bit = 1 << (c + 1)
        if a == b or b == 0:
            continue                       # never active
        if (a, b) == (0, -1):              # L : lam = 0  -> types I, V
            u ^= bit
            v ^= bit
        elif (a, b) == (0, 1):             # R : rho = 0  -> types I, W
            u ^= bit
            w ^= bit
        elif (a, b) == (-1, 1):            # P : lam=1,rho=0 -> type W
            w ^= bit
        elif (a, b) == (1, -1):            # Q : rho=1,lam=0 -> type V
            v ^= bit
        else:
            raise AssertionError((a, b))
    return (u, v, w)


def channels_to_UVW(channels):
    """(U,V,W) as three 3-bit masks -- the OR class at W=1."""
    U = V = Wm = 0
    for (a, b, c) in channels:
        assert max(abs(a), abs(b), abs(c)) <= 1, "W=1 only"
        bit = 1 << (c + 1)
        if a == b or b == 0:
            continue
        if (a, b) == (0, -1):
            U |= bit
            V |= bit
        elif (a, b) == (0, 1):
            U |= bit
            Wm |= bit
        elif (a, b) == (-1, 1):
            Wm |= bit
        elif (a, b) == (1, -1):
            V |= bit
    return (U, V, Wm)


def uvw_to_channels(u, v, w):
    """A channel multiset realising the parity class (u,v,w).  L=0,R=u,Q=v,P=w^u."""
    out = []
    for c in (-1, 0, 1):
        bit = 1 << (c + 1)
        if u & bit:
            out.append((0, 1, c))          # R_c
        if v & bit:
            out.append((1, -1, c))         # Q_c
        if (w ^ u) & bit:
            out.append((-1, 1, c))         # P_c
    return out


def UVW_to_channels(U, V, Wm):
    """A channel SET realising the OR class (U,V,W); requires U subset V|W."""
    assert U & ~(V | Wm) == 0, "unrealisable OR class"
    L = U & V
    R = U & ~V
    out = []
    for c in (-1, 0, 1):
        bit = 1 << (c + 1)
        if L & bit:
            out.append((0, -1, c))
        if R & bit:
            out.append((0, 1, c))
        if V & bit:
            out.append((1, -1, c))
        if Wm & bit:
            out.append((-1, 1, c))
    return out


def all_parity_classes():
    return [(u, v, w) for u in range(8) for v in range(8) for w in range(8)]


def all_or_classes():
    return [(U, V, W) for U in range(8) for V in range(8) for W in range(8)
            if U & ~(V | W) == 0]


# ------------------------------------------------------------- the CA rule

def _emission(l, m, r, u, v, w):
    if not m:
        return 0
    if not l and not r:
        return u
    if not l and r:
        return v
    if l and not r:
        return w
    return 0


def rule_table(cls, mode="parity"):
    """32-entry table: 5-cell window (bit k = cell j-2+k) -> new bit at j."""
    x, y, z = cls
    tab = []
    for win in range(32):
        b = [(win >> k) & 1 for k in range(5)]      # cells j-2 .. j+2
        em = _emission(b[0], b[1], b[2], x, y, z)   # cell j-1
        e0 = _emission(b[1], b[2], b[3], x, y, z)   # cell j
        ep = _emission(b[2], b[3], b[4], x, y, z)   # cell j+1
        if mode == "parity":
            tog = (((em >> 2) & 1) ^ ((e0 >> 1) & 1) ^ (ep & 1))
        else:
            tog = 1 if (((em >> 2) & 1) or ((e0 >> 1) & 1) or (ep & 1)) else 0
        tab.append(b[2] ^ tog)
    return tab


def step_set(S, tab):
    """One CA step on a finite set of ints."""
    if not S:
        return set()
    lo, hi = min(S) - 2, max(S) + 2
    out = set()
    for j in range(lo, hi + 1):
        win = 0
        for k in range(5):
            if (j - 2 + k) in S:
                win |= 1 << k
        if tab[win]:
            out.add(j)
    return out


def orbit(S, tab, steps):
    cur = set(S)
    out = [set(cur)]
    for _ in range(steps):
        cur = step_set(cur, tab)
        out.append(set(cur))
    return out


# ------------------------------------------------------ reference agreement

def to_xnomos(channels, n=None):
    import xnomos
    n = n or len(channels)
    return xnomos.Const([tuple(c) for c in channels], [tuple(range(n))] * n)


def xnomos_state(S, n):
    return {c: (1 << n) - 1 for c in S}


def check_agreement(trials=4000, seed=11, verbose=False):
    """Fuzz: xnomos single-field dynamics == the (u,v,w) / (U,V,W) CA."""
    import random
    import xnomos
    rng = random.Random(seed)
    pool = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]
    bad = 0
    checks = 0
    for _ in range(trials):
        n = rng.randrange(1, 7)
        chans = [rng.choice(pool) for _ in range(n)]
        C = to_xnomos(chans, n)
        cells = sorted({rng.randrange(-6, 7) for _ in range(rng.randrange(1, 9))})
        if not cells:
            continue
        for mode in ("parity", "or"):
            cls = (channels_to_uvw(chans) if mode == "parity"
                   else channels_to_UVW(chans))
            tab = rule_table(cls, mode)
            S = set(cells)
            X = xnomos_state(S, n)
            for _t in range(6):
                X = xnomos.step(X, C, mode)
                S = step_set(S, tab)
                checks += 1
                if set(X) != S:
                    bad += 1
                    if verbose:
                        print("MISMATCH", chans, mode, sorted(X), sorted(S))
                    break
                # all-kinds-everywhere must be preserved
                if any(m != (1 << n) - 1 for m in X.values()):
                    bad += 1
                    if verbose:
                        print("FIELD SPLIT", chans, mode, X)
                    break
    return checks, bad


def check_class_collapse(trials=3000, seed=17):
    """Fuzz: two constitutions with the same class have identical dynamics."""
    import random
    rng = random.Random(seed)
    pool = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]
    checks = bad = 0
    for _ in range(trials):
        chans = [rng.choice(pool) for _ in range(rng.randrange(1, 8))]
        for mode in ("parity", "or"):
            cls = (channels_to_uvw(chans) if mode == "parity"
                   else channels_to_UVW(chans))
            alt = (uvw_to_channels(*cls) if mode == "parity"
                   else UVW_to_channels(*cls))
            cls2 = (channels_to_uvw(alt) if mode == "parity"
                    else channels_to_UVW(alt))
            checks += 1
            if cls2 != cls or rule_table(cls, mode) != rule_table(cls2, mode):
                bad += 1
    return checks, bad


def check_realisability():
    """Every parity class is realisable; OR classes are exactly U subset V|W."""
    n_par = 0
    for u, v, w in all_parity_classes():
        ch = uvw_to_channels(u, v, w)
        assert channels_to_uvw(ch) == (u, v, w), (u, v, w, ch)
        n_par += 1
    n_or = 0
    reach = set()
    for chan_set in itertools.chain.from_iterable(
            itertools.combinations(
                [(a, b, c) for (a, b) in [(0, -1), (0, 1), (-1, 1), (1, -1)]
                 for c in (-1, 0, 1)], k) for k in range(13)):
        reach.add(channels_to_UVW(list(chan_set)))
    for U, V, W in all_or_classes():
        assert (U, V, W) in reach, (U, V, W)
        n_or += 1
    assert len(reach) == n_or, (len(reach), n_or)
    return n_par, n_or


def min_kinds_parity(u, v, w):
    """Fewest channels realising a parity class (search over all 12-channel
    multisets is infinite, but parity only cares mod 2, so subsets suffice)."""
    base = [(a, b, c) for (a, b) in [(0, -1), (0, 1), (-1, 1), (1, -1)]
            for c in (-1, 0, 1)]
    for k in range(0, 13):
        for combo in itertools.combinations(base, k):
            if channels_to_uvw(list(combo)) == (u, v, w):
                return k
    return None


if __name__ == "__main__":
    print("t3_core self-tests")
    n_par, n_or = check_realisability()
    print("  parity classes realisable : %d (expect 512)" % n_par)
    print("  OR classes realisable     : %d (expect 343)" % n_or)
    ch, bad = check_agreement()
    print("  agreement with xnomos     : %d checks, %d mismatches" % (ch, bad))
    ch2, bad2 = check_class_collapse()
    print("  class collapse            : %d checks, %d mismatches" % (ch2, bad2))
    assert bad == 0 and bad2 == 0 and n_par == 512 and n_or == 343
    print("  OK")
