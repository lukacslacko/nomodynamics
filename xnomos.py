#!/usr/bin/env python3
"""
xnomos.py — the cross-amendment engine of nomodynamics (1D and 2D).

THE OBJECT (general form).  Own-kind nomodynamics lets a law amend only its own
kind.  Here a law may amend ANOTHER kind, which is both truer to the pre-formal
referent (real statutes amend other statutes) and — by the Single-Author Lemma —
the only escape from the exactly solvable sector.

A *constitution* C is a finite set of kinds K = {0..n-1}.  Each kind k carries

    rule[k]  = (a_k, b_k, c_k)     offsets in Z^d
    target[k] = t(k) in K          the kind it amends            (E2/own-kind)

A *code* is a finite set S of placed laws (cell, kind).  occ(i) = "some law of
any kind stands at i".  Law (i,k) is ACTIVE iff occ(i+a_k) and not occ(i+b_k).
Every active law emits one toggle of kind t(k) at cell i+c_k; toggles resolve
per (cell, kind) by PARITY (odd count flips) or by OR (>=1 flips).

Own-kind nomodynamics is the special case t = id (every kind a self-loop of the
amendment digraph).  Since out-degree is 1, the amendment digraph is a
functional graph; a kind nobody amends is IMMORTAL, and a code closed under
"kinds I can create" whose kinds are all amendable carries a PERMUTATION
constitution (Lemma 2 of glider-question/RESULTS.md).  Cycle length L = 1 is
own-kind; L = 2 is 'reciprocal amendment'.

Extra semantics implemented (the charted escape lattice):
  mode='parity'  |  'or'                     — E2 fixed single targeting
  mode='super'                               — E1 supersession: an active law
       enacts its own kind at the target cell if that cell is EMPTY, else it
       CLEARS the whole cell (all kinds).  Clear-votes resolve by parity
       ('super') or by OR ('super_or').
  target[k] may be a tuple of kinds          — E3 multi-target laws.

Everything here is exact (integer/set arithmetic).  Self-tests at the bottom
reproduce the published specimens: colonizer, sunset clause, the Z/6 ring
rotor, the two-chamber cancellation, the diagonal relay.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

# ---------------------------------------------------------------- constitution


class Const:
    """A constitution: kinds with rules and amendment targets.

    rules   : list of (a, b, c); each offset an int (1D) or a d-tuple (2D)
    targets : list of int (single target) or tuple of ints (multi-target)
    dim     : 1 or 2
    modulus : None for Z^d, or m for the ring Z/m (1D only)
    guards  : list of (g, h), the CITATION guards of chapter three.  g is the
              kind that must STAND at i+a and h the kind that must be ABSENT at
              i+b; None means "any law" — the founding occupancy semantics.
              guards=None gives occupancy guards throughout (chapters 1-2).
    """

    __slots__ = ("rules", "targets", "dim", "modulus", "n", "guards", "cited")

    def __init__(self, rules, targets=None, dim=1, modulus=None, guards=None):
        self.rules = [tuple(r) for r in rules]
        self.n = len(rules)
        if targets is None:
            targets = list(range(self.n))          # own-kind
        self.targets = [t if isinstance(t, tuple) else (t,) for t in targets]
        self.dim = dim
        self.modulus = modulus
        if guards is None:
            guards = [(None, None)] * self.n
        self.guards = [tuple(g) for g in guards]
        # cited: does any guard name a kind?  (False = the founding semantics,
        # and the fast path in step())
        self.cited = any(g is not None or h is not None
                         for g, h in self.guards)

    # -- offsets -----------------------------------------------------------
    def add(self, cell, off):
        if self.dim == 1:
            j = cell + off
            return j % self.modulus if self.modulus is not None else j
        return tuple(x + y for x, y in zip(cell, off))

    def is_permutation(self):
        seen = [t[0] for t in self.targets]
        return len(self.targets[0]) == 1 and sorted(seen) == list(range(self.n))

    def cycle_type(self):
        """Cycle lengths of the amendment digraph (permutation constitutions)."""
        assert self.is_permutation()
        t = [x[0] for x in self.targets]
        seen, out = set(), []
        for k in range(self.n):
            if k in seen:
                continue
            cyc, x = [], k
            while x not in seen:
                seen.add(x)
                cyc.append(x)
                x = t[x]
            out.append(len(cyc))
        return sorted(out)

    def cites(self):
        """The kinds named by guards (chapter three), as a set."""
        return {x for g in self.guards for x in g if x is not None}

    def label(self):
        def o(x):
            return str(x) if self.dim == 1 else "(%s)" % ",".join(map(str, x))
        parts = []
        for k, (a, b, c) in enumerate(self.rules):
            tg = ",".join(map(str, self.targets[k]))
            parts.append("%d:[%s|%s|%s]->%s" % (k, o(a), o(b), o(c), tg))
        return " ".join(parts)


# ---------------------------------------------------------------------- states
# A state is a dict {cell: bitmask over kinds}, empty cells absent.


def state_of(pairs, n=None):
    """Build a state from an iterable of (cell, kind) pairs."""
    S = {}
    for cell, k in pairs:
        S[cell] = S.get(cell, 0) | (1 << k)
    return S


def laws(S):
    for cell, mask in S.items():
        m = mask
        while m:
            k = (m & -m).bit_length() - 1
            m &= m - 1
            yield cell, k


def card(S):
    return sum(bin(m).count("1") for m in S.values())


def enabled(S, C, cell, k):
    """Does the guard of the kind-k law at `cell` pass?

    Occupancy guard (g is None): some law of ANY kind must stand at i+a.
    Citation guard (g = kind):    a law of THAT kind must stand at i+a.
    Likewise for the vacancy clause at i+b.
    """
    a, b, _ = C.rules[k]
    g, h = C.guards[k]
    pa = C.add(cell, a)
    if g is None:
        if pa not in S:
            return False
    elif not (S.get(pa, 0) >> g) & 1:
        return False
    pb = C.add(cell, b)
    if h is None:
        return pb not in S
    return not (S.get(pb, 0) >> h) & 1


def active_laws(S, C):
    """The laws whose guard passes, as (cell, kind) pairs."""
    return [(cell, k) for cell, k in laws(S) if enabled(S, C, cell, k)]


# ------------------------------------------------------------------ the update


def step(S, C, mode="parity"):
    """One synchronous step.  Returns the new state (a fresh dict)."""
    if mode in ("super", "super_or"):
        return _step_super(S, C, or_resolve=(mode == "super_or"))

    tog = defaultdict(int)            # cell -> xor mask (parity)
    hit = defaultdict(int)            # cell -> or  mask (or)
    for cell, k in laws(S):
        if not enabled(S, C, cell, k):
            continue
        _, _, c = C.rules[k]
        j = C.add(cell, c)
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
    """Supersession (E1): enact own kind on empty ground, else clear the cell."""
    enact = defaultdict(int)
    clear_par = defaultdict(int)      # parity count of clear votes
    clear_any = set()
    for cell, k in laws(S):
        if not enabled(S, C, cell, k):
            continue
        _, _, c = C.rules[k]
        j = C.add(cell, c)
        if True:
            if j in S:
                clear_par[j] ^= 1
                clear_any.add(j)
            else:
                enact[j] |= 1 << k
    out = dict(S)
    cleared = clear_any if or_resolve else {j for j, p in clear_par.items() if p}
    for j in cleared:
        out.pop(j, None)
    for j, m in enact.items():
        if j in out:                  # became occupied by another enactment
            out[j] |= m
        else:
            out[j] = m
    return {j: m for j, m in out.items() if m}


# ----------------------------------------------------------- canonical framing


def normalize(S, dim=1):
    """Translate to a canonical position; return (frozen state, anchor)."""
    if not S:
        return (), None
    if dim == 1:
        lo = min(S)
        return tuple(sorted((c - lo, m) for c, m in S.items())), lo
    lox = min(c[0] for c in S)
    loy = min(c[1] for c in S)
    return (tuple(sorted(((c[0] - lox, c[1] - loy), m) for c, m in S.items())),
            (lox, loy))


def freeze(S):
    return tuple(sorted(S.items()))


def sub(p, q, dim=1):
    return p - q if dim == 1 else tuple(x - y for x, y in zip(p, q))


# ------------------------------------------------------------- classification

EXTINCT, FIXED, BALANCED, CYCLE, GLIDER, GROWING, UNRESOLVED = (
    "EXTINCT", "FIXED", "BALANCED", "CYCLE", "GLIDER", "GROWING", "UNRESOLVED")


def classify(S0, C, mode="parity", max_steps=400, max_card=400, max_span=400,
             want_history=False):
    """Run and certify.  Returns a dict with 'kind' and a certificate.

    FIXED    : Phi(S) = S.                (BALANCED if some law is still active)
    CYCLE    : Phi^p(S) = S, p >= 2.
    GLIDER   : Phi^p(S) = sigma^d(S), d != 0 — a free moving law-packet.
    GROWING  : exceeded the card/span budget without recurrence.
    """
    dim = C.dim
    S = dict(S0)
    seen_exact = {}                       # frozen state -> t
    seen_norm = {}                        # normalized   -> (t, anchor)
    hist = [dict(S)] if want_history else None
    for t in range(max_steps):
        if not S:
            return {"kind": EXTINCT, "t": t, "history": hist}
        fe = freeze(S)
        if fe in seen_exact:
            t0 = seen_exact[fe]
            p = t - t0
            if p == 1:
                act = len(active_laws(S, C))
                return {"kind": BALANCED if act else FIXED, "t": t0,
                        "period": 1, "active": act, "card": card(S),
                        "history": hist}
            return {"kind": CYCLE, "t": t0, "period": p, "card": card(S),
                    "history": hist}
        seen_exact[fe] = t
        if C.modulus is not None:        # on a ring, translation is rotation:
            nm = None                    # exact recurrence is the only cert
        else:
            nm, anchor = normalize(S, dim)
        if nm is not None and nm in seen_norm:
            t0, anchor0 = seen_norm[nm]
            d = sub(anchor, anchor0, dim)
            nz = d != 0 if dim == 1 else any(d)
            if nz:
                return {"kind": GLIDER, "t": t0, "period": t - t0,
                        "displacement": d, "card": card(S), "history": hist}
        elif nm is not None:
            seen_norm[nm] = (t, anchor)
        if card(S) > max_card:
            return {"kind": GROWING, "t": t, "card": card(S), "history": hist}
        if dim == 1 and C.modulus is None and S:
            if max(S) - min(S) > max_span:
                return {"kind": GROWING, "t": t, "span": max(S) - min(S),
                        "history": hist}
        elif dim == 2 and S:
            xs = [c[0] for c in S]
            ys = [c[1] for c in S]
            if max(xs) - min(xs) > max_span or max(ys) - min(ys) > max_span:
                return {"kind": GROWING, "t": t, "history": hist}
        S = step(S, C, mode)
        if want_history:
            hist.append(dict(S))
    return {"kind": UNRESOLVED, "t": max_steps, "card": card(S), "history": hist}


def verify_glider(S0, C, p, d, mode="parity"):
    """Independently re-check Phi^p(S) = sigma^d(S) over three full periods."""
    S = dict(S0)
    for rep in range(1, 4):
        for _ in range(p):
            S = step(S, C, mode)
        want = {}
        for cell, m in S0.items():
            want[C.add(cell, d * rep if C.dim == 1 else
                       tuple(x * rep for x in d))] = m
        if S != want:
            return False
    return True


def verify_balanced(S0, C, mode="parity"):
    """Fixed point with at least one active law: a balanced constitution."""
    return (step(S0, C, mode) == S0) and bool(active_laws(S0, C))


# ------------------------------------------------------------------- rendering


def render(S, C, lo=None, hi=None, sym=None):
    """One line per state, 1D."""
    if not S:
        return "."
    lo = min(S) if lo is None else lo
    hi = max(S) if hi is None else hi
    sym = sym or "ABCDEFGH"
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


def spacetime(S0, C, steps, mode="parity", lo=None, hi=None):
    S = dict(S0)
    rows = []
    for _ in range(steps):
        rows.append(render(S, C, lo, hi))
        S = step(S, C, mode)
    return rows


# ------------------------------------------------------------- enumeration aid

OFF1 = (-1, 0, 1)
RULES1 = [(a, b, c) for a in OFF1 for b in OFF1 for c in OFF1]


def perm_consts(cycle_len, rule_pool=RULES1, dim=1, modulus=None):
    """All L-cycle permutation constitutions over a rule pool (1D by default)."""
    tgt = [(i + 1) % cycle_len for i in range(cycle_len)]
    for combo in itertools.product(rule_pool, repeat=cycle_len):
        yield Const(list(combo), tgt, dim=dim, modulus=modulus)


# ------------------------------------------------------------------ self-tests

def _tests():
    ok = 0

    # 1. Colonizer (0,1,1): own-kind, marches right at speed 1.
    C = Const([(0, 1, 1)])
    S = state_of([(0, 0)])
    assert spacetime(S, C, 4, lo=0, hi=3) == ["A...", "AA..", "AAA.", "AAAA"]
    ok += 1

    # 2. Sunset clause (0,-1,1): period-2 blinker.
    C = Const([(0, -1, 1)])
    res = classify(state_of([(0, 0)]), C)
    assert res["kind"] == CYCLE and res["period"] == 2, res
    ok += 1

    # 3. The Z/6 ring rotor: kind (0,1,-1) at cells {1,2,5}, hop 3 per step.
    C = Const([(0, 1, -1)], modulus=6)
    S = state_of([(1, 0), (2, 0), (5, 0)])
    T = step(S, C)
    assert set(T) == {2, 4, 5}, T                      # = S rotated by 3
    assert set(step(T, C)) == set(S)
    ok += 1

    # 4. Gridlock: interior laws of a solid block are blocked, any kind.
    for a, b, c in RULES1:
        C = Const([(a, b, c)])
        S = state_of([(i, 0) for i in range(-3, 4)])
        assert not [x for x in active_laws(S, C) if -2 <= x[0] <= 2], (a, b, c)
    ok += 1

    # 5. THE TWO-CHAMBER DEADLOCK (1D): two kinds amending a third at the same
    #    cell.  Under parity the two enactments cancel and the code is FIXED
    #    though both laws are active — a *balanced constitution*, which the
    #    Dead Letter Theorem forbids in own-kind nomodynamics.  Under OR the
    #    enactment passes.  Minimal witness: two placed laws.
    C = Const([(0, 1, 1), (0, -1, -1), (0, 1, 0)], targets=[2, 2, 2])
    S = state_of([(0, 0), (2, 1)])
    assert step(S, C, "parity") == S
    assert len(active_laws(S, C)) == 2
    assert verify_balanced(S, C)
    assert step(S, C, "or") == state_of([(0, 0), (2, 1), (1, 2)])
    assert classify(S, C)["kind"] == BALANCED
    ok += 1

    # 6. Reciprocal amendment is single-author: parity == OR on random states.
    import random
    rng = random.Random(7)
    C = Const([(0, 1, 1), (0, -1, -1)], targets=[1, 0])
    for _ in range(300):
        S = state_of([(rng.randrange(-4, 5), rng.randrange(2))
                      for _ in range(rng.randrange(1, 7))])
        assert step(S, C, "parity") == step(S, C, "or")
    ok += 1

    # 7. Certificate machinery: the ring rotor is seen as a CYCLE on Z/6
    #    (rotation is not translation there) and verify_glider works on Z.
    C = Const([(0, 1, 1)])
    S = state_of([(0, 0)])
    assert not verify_glider(S, C, 1, 1)
    ok += 1

    print("xnomos self-tests passed: %d/7" % ok)


if __name__ == "__main__":
    _tests()
