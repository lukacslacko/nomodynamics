#!/usr/bin/env python3
"""
cite.py — the citation engine of chapter three, and its census machinery.

THE OBJECT.  A *constitution* is a finite kind set K = {0..n-1}.  Each kind k
carries offsets (a_k, b_k, c_k), a target set T_k subset of K, and a pair of
CITATIONS (g_k, h_k) in (K union {ANY})^2.  A placed law (i,k) is ACTIVE iff a
law of kind g_k stands at i+a_k and no law of kind h_k stands at i+b_k, where
ANY means "some law of any kind".  Every active law toggles each kind of T_k at
i+c_k; simultaneous toggles resolve by parity or by OR.

g = h = ANY recovers chapters one and two.

This module carries a bitfield engine (one big int per kind, bit i = cell i)
which is ~50x faster than the reference dict engine in ../xnomos.py, plus:

  * bulk_map      -- the interior map beta : 2^K -> 2^K of the Plenum theory
  * gridlocked    -- the exact epitaph of Gridlock: h_k in {ANY, k, g_k} forall k
  * classify      -- certified classification (extinct/fixed/balanced/cycle/
                     glider/growing/unresolved)
  * canon         -- canonical form under mirror x kind-relabelling
  * cross-checks against ../xnomos.py (`python3 cite.py` runs them)
"""

from __future__ import annotations

import itertools

ANY = None

EXTINCT, FIXED, BALANCED, CYCLE, GLIDER, GROWING, UNRESOLVED = (
    "EXTINCT", "FIXED", "BALANCED", "CYCLE", "GLIDER", "GROWING", "UNRESOLVED")
CLASSES = (EXTINCT, FIXED, BALANCED, CYCLE, GLIDER, GROWING, UNRESOLVED)


# ----------------------------------------------------------------- constitution

class Cit:
    """rules[k] = (a,b,c); targets[k] = frozenset/tuple of kinds;
       guards[k] = (g,h) with None = ANY."""

    __slots__ = ("n", "rules", "targets", "guards", "tmask")

    def __init__(self, rules, targets, guards):
        self.rules = [tuple(r) for r in rules]
        self.n = len(rules)
        self.targets = [tuple(sorted(set(t))) for t in targets]
        self.guards = [tuple(g) for g in guards]
        self.tmask = [sum(1 << t for t in T) for T in self.targets]

    # -- presentation ------------------------------------------------------
    def key(self):
        """Sortable encoding (ANY -> -1) — used for canonical forms."""
        return (tuple(self.rules), tuple(self.targets),
                tuple((-1 if g is None else g, -1 if h is None else h)
                      for g, h in self.guards))

    def label(self):
        out = []
        for k in range(self.n):
            a, b, c = self.rules[k]
            g, h = self.guards[k]
            gs = "*" if g is None else str(g)
            hs = "*" if h is None else str(h)
            T = "{" + ",".join(map(str, self.targets[k])) + "}"
            out.append("%d:(%d,%d,%d) cite(%s,%s) ->%s" % (k, a, b, c, gs, hs, T))
        return " | ".join(out)

    def to_xnomos(self, dim=1, modulus=None):
        """The same constitution as an xnomos.Const, for independent checking."""
        import xnomos
        tg = [t if t else () for t in self.targets]
        return xnomos.Const(self.rules, targets=tg, dim=dim, modulus=modulus,
                            guards=self.guards)

    # -- structure ---------------------------------------------------------
    def outdeg(self):
        return max(len(t) for t in self.targets)

    def indeg(self, t):
        return sum(1 for k in range(self.n) if t in self.targets[k])

    def cited(self):
        return {x for g in self.guards for x in g if x is not None}


# --------------------------------------------------------- the bulk (plenum) map

def active_bulk(C, U):
    """Kinds active in a region every cell of which carries exactly the set U.

    A kind-k law there is active iff its precedent clause is met (kind g_k is
    present, or ANY and the cell is nonempty) and its exception clause is met
    (kind h_k is absent, and ANY fails since the cell is nonempty).
    """
    if not U:
        return frozenset()
    out = []
    for k in sorted(U):
        g, h = C.guards[k]
        if g is not None and g not in U:
            continue
        if h is None or h in U:          # exception cell is blocked
            continue
        out.append(k)
    return frozenset(out)


def bulk_map(C, U, mode="parity"):
    """beta(U): the next kind-set of a homogeneous region carrying U."""
    A = active_bulk(C, U)
    if mode == "or":
        add = set()
        for k in A:
            add |= set(C.targets[k])
        return frozenset(set(U) ^ add) if False else frozenset(set(U) ^ add)
    m = 0
    for k in A:
        m ^= C.tmask[k]
    u = sum(1 << k for k in U) ^ m
    return frozenset(k for k in range(C.n) if (u >> k) & 1)


def bulk_orbit(C, U, mode="parity"):
    """(preperiod, period, orbit list) of beta from U."""
    seen, seq = {}, []
    V = frozenset(U)
    while V not in seen:
        seen[V] = len(seq)
        seq.append(V)
        V = bulk_map(C, V, mode)
    t0 = seen[V]
    return t0, len(seq) - t0, seq


def gridlocked(C):
    """Does chapter one's Gridlock survive for C?

    Gridlock = "every occupancy-solid region is interior-frozen".  Equivalent
    (Theorem G3 of RESULTS.md) to: for every kind k, h_k in {ANY, k, g_k}.
    """
    for k in range(C.n):
        g, h = C.guards[k]
        if h is None or h == k or h == g:
            continue
        return False
    return True


def gridlocked_bruteforce(C):
    """Same predicate, by direct check over all nonempty U (for the proof test)."""
    for r in range(1, C.n + 1):
        for U in itertools.combinations(range(C.n), r):
            if active_bulk(C, frozenset(U)):
                return False
    return True


# ------------------------------------------------------------ bitfield dynamics
# Fields: F[k] is an int, bit (cell + BIAS) set iff a kind-k law stands there.

def _sr(x, s):
    """bit i of result = bit (i+s) of x."""
    return x >> s if s >= 0 else x << (-s)


def _sl(x, s):
    """bit (i+s) of result = bit i of x."""
    return x << s if s >= 0 else x >> (-s)


def step_fields(F, C, mode="parity"):
    n = C.n
    occ = 0
    for f in F:
        occ |= f
    tog = [0] * n
    for k in range(n):
        fk = F[k]
        if not fk:
            continue
        a, b, c = C.rules[k]
        g, h = C.guards[k]
        prec = _sr(occ if g is None else F[g], a)
        act = fk & prec
        if not act:
            continue
        exc = _sr(occ if h is None else F[h], b)
        act &= ~exc
        if not act:
            continue
        sh = _sl(act, c)
        if mode == "or":
            for t in C.targets[k]:
                tog[t] |= sh
        else:
            for t in C.targets[k]:
                tog[t] ^= sh
    return [F[k] ^ tog[k] for k in range(n)]


def active_fields(F, C):
    """Bitfield of active laws per kind."""
    occ = 0
    for f in F:
        occ |= f
    out = []
    for k in range(C.n):
        a, b, c = C.rules[k]
        g, h = C.guards[k]
        prec = _sr(occ if g is None else F[g], a)
        exc = _sr(occ if h is None else F[h], b)
        out.append(F[k] & prec & ~exc)
    return out


def card_fields(F):
    return sum(bin(f).count("1") for f in F)


def norm_fields(F):
    """Translate so the leftmost occupied cell is at bit 0; return (key, shift)."""
    occ = 0
    for f in F:
        occ |= f
    if occ == 0:
        return (), None
    lo = (occ & -occ).bit_length() - 1
    return tuple(f >> lo for f in F), lo


BIAS = 512
WIDTH = 4096


def state_fields(pairs, n):
    F = [0] * n
    for cell, k in pairs:
        F[k] |= 1 << (cell + BIAS)
    return F


def fields_to_pairs(F):
    out = []
    for k, f in enumerate(F):
        while f:
            b = (f & -f).bit_length() - 1
            out.append((b - BIAS, k))
            f &= f - 1
    return sorted(out)


# ------------------------------------------------------------- classification

def classify(F0, C, mode="parity", max_steps=200, max_card=200, max_span=120):
    """Certified classification of the orbit of F0.  Returns a dict."""
    F = list(F0)
    seen_exact, seen_norm = {}, {}
    for t in range(max_steps):
        occ = 0
        for f in F:
            occ |= f
        if occ == 0:
            return {"kind": EXTINCT, "t": t}
        fe = tuple(F)
        if fe in seen_exact:
            t0 = seen_exact[fe]
            p = t - t0
            if p == 1:
                act = card_fields(active_fields(F, C))
                return {"kind": BALANCED if act else FIXED, "t": t0,
                        "period": 1, "active": act, "card": card_fields(F)}
            return {"kind": CYCLE, "t": t0, "period": p, "card": card_fields(F)}
        seen_exact[fe] = t
        nm, lo = norm_fields(F)
        if nm in seen_norm:
            t0, lo0 = seen_norm[nm]
            d = lo - lo0
            if d:
                return {"kind": GLIDER, "t": t0, "period": t - t0,
                        "displacement": d, "card": card_fields(F)}
        else:
            seen_norm[nm] = (t, lo)
        if card_fields(F) > max_card:
            return {"kind": GROWING, "t": t, "card": card_fields(F)}
        span = occ.bit_length() - ((occ & -occ).bit_length() - 1)
        if span > max_span:
            return {"kind": GROWING, "t": t, "span": span}
        F = step_fields(F, C, mode)
    return {"kind": UNRESOLVED, "t": max_steps, "card": card_fields(F)}


def verify_glider(F0, C, p, d, mode="parity", reps=3):
    """Independent re-check of Phi^p = sigma^d over `reps` full periods."""
    F = list(F0)
    for r in range(1, reps + 1):
        for _ in range(p):
            F = step_fields(F, C, mode)
        want = [_sl(f, d * r) for f in F0]
        if F != want:
            return False
    return True


def verify_cycle(F0, C, p, mode="parity"):
    F = list(F0)
    for _ in range(p):
        F = step_fields(F, C, mode)
    return F == list(F0)


# --------------------------------------------------------------------- rings

def step_ring(mask, C, m, mode="parity"):
    """State on Z/m as a tuple of n ints, bit i = cell i.  Cyclic shifts."""
    n = C.n
    full = (1 << m) - 1

    def rot(x, s):                       # bit i of result = bit (i+s) of x
        s %= m
        return ((x >> s) | (x << (m - s))) & full

    occ = 0
    for f in mask:
        occ |= f
    tog = [0] * n
    for k in range(n):
        fk = mask[k]
        if not fk:
            continue
        a, b, c = C.rules[k]
        g, h = C.guards[k]
        act = fk & rot(occ if g is None else mask[g], a)
        if not act:
            continue
        act &= ~rot(occ if h is None else mask[h], b) & full
        if not act:
            continue
        sh = rot(act, -c)
        if mode == "or":
            for t in C.targets[k]:
                tog[t] |= sh
        else:
            for t in C.targets[k]:
                tog[t] ^= sh
    return tuple(mask[k] ^ tog[k] for k in range(n))


def ring_orbit(mask, C, m, mode="parity", max_steps=4096):
    seen, seq = {}, []
    S = tuple(mask)
    while S not in seen and len(seq) < max_steps:
        seen[S] = len(seq)
        seq.append(S)
        S = step_ring(S, C, m, mode)
    if S not in seen:
        return None, None, seq
    t0 = seen[S]
    return t0, len(seq) - t0, seq


# ---------------------------------------------------------------- symmetries

OFFS = (-1, 0, 1)


def mirror(C):
    return Cit([(-a, -b, -c) for a, b, c in C.rules], C.targets, C.guards)


def relabel(C, perm):
    """perm[k] = new index of kind k."""
    n = C.n
    inv = [0] * n
    for k, p in enumerate(perm):
        inv[p] = k
    rules = [C.rules[inv[j]] for j in range(n)]
    targets = [tuple(sorted(perm[t] for t in C.targets[inv[j]])) for j in range(n)]
    guards = []
    for j in range(n):
        g, h = C.guards[inv[j]]
        guards.append((None if g is None else perm[g],
                       None if h is None else perm[h]))
    return Cit(rules, targets, guards)


def orbit_of(C):
    seen = {}
    for perm in itertools.permutations(range(C.n)):
        D = relabel(C, list(perm))
        for E in (D, mirror(D)):
            seen[E.key()] = E
    return seen


def canon(C):
    """Canonical representative and orbit size under mirror x relabelling."""
    o = orbit_of(C)
    kmin = min(o)
    return kmin, len(o)


# ------------------------------------------------------------ enumeration aid

RULES = [(a, b, c) for a in OFFS for b in OFFS for c in OFFS]


def all_kinds(n, targets_nonempty=False):
    """All (rule, targetset, guard) triples for one kind of an n-kind universe."""
    tsets = [t for r in range(0 if not targets_nonempty else 1, n + 1)
             for t in itertools.combinations(range(n), r)]
    gs = [None] + list(range(n))
    return [(rule, T, (g, h))
            for rule in RULES for T in tsets for g in gs for h in gs]


def seeds_span(span, n):
    """All nonempty seeds inside `span` cells whose leftmost cell is occupied."""
    out = []
    for masks in itertools.product(range(1 << n), repeat=span):
        if masks[0] == 0:
            continue
        F = [0] * n
        for i, m in enumerate(masks):
            for k in range(n):
                if (m >> k) & 1:
                    F[k] |= 1 << (i + BIAS)
        out.append(tuple(F))
    return out


# -------------------------------------------------------------------- render

SYM = "ABCDEFGHIJKLMNOP"


def render_fields(F, lo, hi, n=None):
    n = n or len(F)
    out = []
    for i in range(lo, hi + 1):
        bit = 1 << (i + BIAS)
        ks = [k for k in range(len(F)) if F[k] & bit]
        if not ks:
            out.append(".")
        elif len(ks) == 1:
            out.append(SYM[ks[0]])
        else:
            out.append("#")
    return "".join(out)


def spacetime(F0, C, steps, mode="parity", lo=None, hi=None, pad=0):
    F = list(F0)
    rows, states = [], []
    for _ in range(steps):
        states.append(list(F))
        F = step_fields(F, C, mode)
    if lo is None or hi is None:
        occ = 0
        for st in states:
            for f in st:
                occ |= f
        if occ == 0:
            return ["."] * steps
        a = (occ & -occ).bit_length() - 1 - BIAS - pad
        b = occ.bit_length() - 1 - BIAS + pad
        lo = a if lo is None else lo
        hi = b if hi is None else hi
    return [render_fields(st, lo, hi) for st in states]


# ---------------------------------------------------------------- self-tests

def _tests():
    import random
    import xnomos as X
    rng = random.Random(11)
    ok = 0

    # 1. bitfield engine == reference dict engine, on random citation universes
    for trial in range(400):
        n = rng.randrange(1, 4)
        kinds = []
        for _ in range(n):
            rule = (rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
            T = tuple(sorted(rng.sample(range(n), rng.randrange(0, n + 1))))
            g = rng.choice([None] + list(range(n)))
            h = rng.choice([None] + list(range(n)))
            kinds.append((rule, T, (g, h)))
        C = Cit([k[0] for k in kinds], [k[1] for k in kinds],
                [k[2] for k in kinds])
        XC = C.to_xnomos()
        pairs = [(rng.randrange(-4, 5), rng.randrange(n))
                 for _ in range(rng.randrange(1, 8))]
        F = state_fields(pairs, n)
        S = X.state_of(pairs, n)
        for mode in ("parity", "or"):
            Ff, Ss = list(F), dict(S)
            for _ in range(6):
                Ff = step_fields(Ff, C, mode)
                Ss = X.step(Ss, XC, mode)
                assert sorted(fields_to_pairs(Ff)) == sorted(
                    (c, k) for c, k in X.laws(Ss)), (C.label(), mode, trial)
    ok += 1

    # 2. Gridlock epitaph: closed form == brute force over all U
    for trial in range(3000):
        n = rng.randrange(1, 5)
        C = Cit([(0, 0, 0)] * n, [()] * n,
                [(rng.choice([None] + list(range(n))),
                  rng.choice([None] + list(range(n)))) for _ in range(n)])
        assert gridlocked(C) == gridlocked_bruteforce(C), C.label()
    ok += 1

    # 3. the bulk map is exact on homogeneous ring codes, every modulus
    for trial in range(400):
        n = rng.randrange(1, 4)
        C = Cit([(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                 for _ in range(n)],
                [tuple(sorted(rng.sample(range(n), rng.randrange(0, n + 1))))
                 for _ in range(n)],
                [(rng.choice([None] + list(range(n))),
                  rng.choice([None] + list(range(n)))) for _ in range(n)])
        for m in (1, 2, 3, 5, 7):
            U = frozenset(k for k in range(n) if rng.random() < .5)
            full = (1 << m) - 1
            mask = tuple(full if k in U else 0 for k in range(n))
            for mode in ("parity", "or"):
                nxt = step_ring(mask, C, m, mode)
                V = bulk_map(C, U, mode)
                want = tuple(full if k in V else 0 for k in range(n))
                assert nxt == want, (C.label(), m, U, mode)
    ok += 1

    # 4. the PLENUM theorem: beta(K) = K, always
    for trial in range(3000):
        n = rng.randrange(1, 5)
        C = Cit([(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                 for _ in range(n)],
                [tuple(sorted(rng.sample(range(n), rng.randrange(0, n + 1))))
                 for _ in range(n)],
                [(rng.choice([None] + list(range(n))),
                  rng.choice([None] + list(range(n)))) for _ in range(n)])
        K = frozenset(range(n))
        assert not active_bulk(C, K)
        assert bulk_map(C, K) == K and bulk_map(C, K, "or") == K
    ok += 1

    # 5. citation is inert at n = 1: guard alphabet collapses
    for rule in RULES:
        for T in ((), (0,)):
            base = Cit([rule], [T], [(None, None)])
            for g in (None, 0):
                for h in (None, 0):
                    D = Cit([rule], [T], [(g, h)])
                    for _ in range(40):
                        pairs = [(rng.randrange(-3, 4), 0)
                                 for _ in range(rng.randrange(1, 6))]
                        F = state_fields(pairs, 1)
                        assert step_fields(F, base) == step_fields(F, D)
    ok += 1

    # 6. canonical forms: orbit size divides 2*n! and canon is invariant
    for trial in range(300):
        n = 2
        C = Cit([(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                 for _ in range(n)],
                [tuple(sorted(rng.sample(range(n), rng.randrange(0, n + 1))))
                 for _ in range(n)],
                [(rng.choice([None] + list(range(n))),
                  rng.choice([None] + list(range(n)))) for _ in range(n)])
        kc, sz = canon(C)
        assert (2 * 2) % sz == 0
        for D in orbit_of(C).values():
            assert canon(D)[0] == kc
    ok += 1

    print("cite.py self-tests passed: %d/6" % ok)


if __name__ == "__main__":
    _tests()
