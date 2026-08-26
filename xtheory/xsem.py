#!/usr/bin/env python3
"""xsem.py — the semantic lattice of nomodynamics (Expedition X-D).

A *semantics* is a choice on five independent axes:

  GUARD    what makes a law active            occ | quorum(m)
  TARGET   whose kind the effect edits        own | functional t | state-dependent
  EFFECT   what the effect does               toggle | enact | repeal | override
  RESOLVE  how many effects at one slot combine   parity | or
  PERSIST  what happens to an untouched law   keep (H3) | sunset(tau)

`xnomos` implements (occ, functional, toggle, parity|or, keep) and
(occ, own, super, parity|or, keep).  This module adds the rest, in one engine,
so that a theorem can be re-run against every point of the lattice.

Everything is exact.  `battery(claim)` is the section-7 verification run of
theorems.py.
"""
from __future__ import annotations

import itertools
import random
from collections import Counter, defaultdict

from xlib import RULES1, Const, all_seeds, seeds_span
import xnomos as X
from xnomos import state_of, laws, card

# --------------------------------------------------------------- semantics


class Sem:
    """A point of the semantic lattice."""
    __slots__ = ("effect", "resolve", "immune", "sunset", "quorum")

    def __init__(self, effect="toggle", resolve="parity", immune=(),
                 sunset=None, quorum=None):
        self.effect = effect        # toggle | enact | repeal | override
        self.resolve = resolve      # parity | or
        self.immune = frozenset(immune)
        self.sunset = sunset        # None, or int tau >= 1 (grace period)
        self.quorum = quorum        # None, or a set of allowed neighbour counts

    def name(self):
        p = [self.effect, self.resolve]
        if self.immune:
            p.append("immune%s" % sorted(self.immune))
        if self.sunset:
            p.append("sunset%d" % self.sunset)
        if self.quorum is not None:
            p.append("quorum%s" % sorted(self.quorum))
        return "+".join(p)


def actives(S, C, sem):
    out = []
    for cell, k in laws(S):
        a, b, _ = C.rules[k]
        if sem.quorum is None:
            if C.add(cell, a) in S and C.add(cell, b) not in S:
                out.append((cell, k))
        else:
            n = (C.add(cell, -1) in S) + (C.add(cell, 1) in S)
            if n in sem.quorum:
                out.append((cell, k))
    return out


def xstep(S, C, sem):
    """One synchronous step under an arbitrary point of the lattice.

    `S` is an xnomos state (dict cell -> kind bitmask).  Sunset semantics need
    ages; use `sunset_step` for those.
    """
    votes = defaultdict(list)                     # slot -> list of source kinds
    for cell, k in actives(S, C, sem):
        j = C.add(cell, C.rules[k][2])
        if sem.effect == "override":
            votes[(j, None)].append(k)
        else:
            for t in C.targets[k]:
                votes[(j, t)].append(k)

    out = dict(S)
    if sem.effect == "override":
        # lex posterior: the enacting law displaces the whole cell content.
        for (j, _), ks in votes.items():
            m = 0
            for k in ks:
                for t in C.targets[k]:
                    m |= 1 << t
            out[j] = m
        return {j: m for j, m in out.items() if m}

    for (j, t), ks in votes.items():
        n = len(ks)
        cur = (out.get(j, 0) >> t) & 1
        if sem.effect == "toggle":
            fires = (n % 2 == 1) if sem.resolve == "parity" else (n >= 1)
            new = cur ^ 1 if fires else cur
        elif sem.effect == "enact":
            new = 1
        elif sem.effect == "repeal":
            new = 0
        else:
            raise ValueError(sem.effect)
        if new == 0 and t in sem.immune and cur == 1:
            new = 1                                # entrenchment clause
        m = out.get(j, 0)
        m = (m | (1 << t)) if new else (m & ~(1 << t))
        if m:
            out[j] = m
        elif j in out:
            del out[j]
    return out


# ------------------------------------------------- sunset (decay) semantics

def sunset_step(A, C, sem):
    """A is a dict (cell,kind) -> remaining life.  Laws decay unless re-enacted.

    An active law of kind k enacts kind t(k) at i+c_k, resetting its life to
    tau.  Every other law loses one unit of life; at 0 it lapses.
    """
    S = {}
    for (cell, k) in A:
        S[cell] = S.get(cell, 0) | (1 << k)
    tau = sem.sunset
    fresh = {}
    for cell, k in actives(S, C, sem):
        j = C.add(cell, C.rules[k][2])
        for t in C.targets[k]:
            fresh[(j, t)] = tau
    out = {}
    for s, life in A.items():
        if s in fresh:
            continue
        if life > 1:
            out[s] = life - 1
    out.update(fresh)
    return out


def sunset_classify(A0, C, sem, max_steps=300, max_card=400, max_span=200):
    A = dict(A0)
    seen_exact, seen_norm = {}, {}
    for t in range(max_steps):
        if not A:
            return {"kind": "EXTINCT", "t": t}
        fe = tuple(sorted(A.items()))
        if fe in seen_exact:
            p = t - seen_exact[fe]
            return {"kind": "FIXED" if p == 1 else "CYCLE", "t": seen_exact[fe],
                    "period": p}
        seen_exact[fe] = t
        lo = min(c for c, _ in A)
        nm = tuple(sorted(((c - lo, k), v) for (c, k), v in A.items()))
        if nm in seen_norm:
            t0, lo0 = seen_norm[nm]
            if lo != lo0:
                return {"kind": "GLIDER", "t": t0, "period": t - t0,
                        "displacement": lo - lo0}
        else:
            seen_norm[nm] = (t, lo)
        cells = [c for c, _ in A]
        if len(A) > max_card or max(cells) - min(cells) > max_span:
            return {"kind": "GROWING", "t": t}
        A = sunset_step(A, C, sem)
    return {"kind": "UNRESOLVED", "t": max_steps}


def verify_sunset_glider(A0, C, sem, p, d):
    A = dict(A0)
    for rep in range(1, 4):
        for _ in range(p):
            A = sunset_step(A, C, sem)
        want = {(c + d * rep, k): v for (c, k), v in A0.items()}
        if A != want:
            return False
    return True


# ------------------------------------------------------------ the battery

TMAPS4 = [[0, 1], [1, 0], [0, 0], [1, 1]]


def _fauna(sem, span=4, nk=2, tmaps=TMAPS4, rules=None, budget=200):
    """Classify the whole nk-kind box under `sem`; return a Counter + extras."""
    rules = rules or RULES1
    cnt = Counter()
    periods = set()
    gliders = []
    for r0 in rules:
        for r1 in rules:
            for tm in tmaps:
                C = Const([r0, r1], list(tm))
                for S in all_seeds(span, nk):
                    r = _classify(S, C, sem, budget)
                    cnt[r["kind"]] += 1
                    if r["kind"] in ("CYCLE", "GLIDER"):
                        periods.add(r["period"])
                    if r["kind"] == "GLIDER":
                        gliders.append((r0, r1, tuple(tm),
                                        tuple(sorted(S.items())), r))
    return cnt, periods, gliders


def _classify(S0, C, sem, budget=200, max_span=120, max_card=200):
    S = dict(S0)
    seen_exact, seen_norm = {}, {}
    for t in range(budget):
        if not S:
            return {"kind": "EXTINCT", "t": t}
        fe = X.freeze(S)
        if fe in seen_exact:
            p = t - seen_exact[fe]
            if p == 1:
                return {"kind": "BALANCED" if actives(S, C, sem) else "FIXED",
                        "t": seen_exact[fe], "period": 1}
            return {"kind": "CYCLE", "t": seen_exact[fe], "period": p}
        seen_exact[fe] = t
        lo = min(S)
        nm = tuple(sorted((c - lo, m) for c, m in S.items()))
        if nm in seen_norm:
            t0, lo0 = seen_norm[nm]
            if lo != lo0:
                return {"kind": "GLIDER", "t": t0, "period": t - t0,
                        "displacement": lo - lo0}
        else:
            seen_norm[nm] = (t, lo)
        if card(S) > max_card or max(S) - min(S) > max_span:
            return {"kind": "GROWING", "t": t}
        S = xstep(S, C, sem)
    return {"kind": "UNRESOLVED", "t": budget}


def battery(claim):
    # -- (a) engine agreement: xstep(toggle,parity/or) == xnomos.step
    rng = random.Random(31)
    bad = 0
    for mode, sem in (("parity", Sem("toggle", "parity")),
                      ("or", Sem("toggle", "or"))):
        for _ in range(3000):
            n = rng.randrange(1, 4)
            C = Const([rng.choice(RULES1) for _ in range(n)],
                      [rng.randrange(n) for _ in range(n)])
            S = {}
            for _ in range(rng.randrange(1, 6)):
                c = rng.randrange(-4, 5)
                S[c] = S.get(c, 0) | (1 << rng.randrange(n))
            if xstep(S, C, sem) != X.step(dict(S), C, mode):
                bad += 1
    claim("xsem reproduces xnomos on (toggle, parity) and (toggle, or)",
          bad == 0, "6000 states, %d mismatches" % bad)

    # -- (b) GRIDLOCK across the lattice
    solid = {i: 3 for i in range(5)}
    bad = 0
    tot = 0
    for eff in ("toggle", "enact", "repeal", "override"):
        for res in ("parity", "or"):
            for imm in ((), (0,)):
                sem = Sem(eff, res, imm)
                for r0 in RULES1:
                    for r1 in RULES1:
                        C = Const([r0, r1], [1, 0])
                        tot += 1
                        if [x for x in actives(solid, C, sem) if 1 <= x[0] <= 3]:
                            bad += 1
    claim("Gridlock survives every effect/resolve/entrenchment choice",
          bad == 0, "%d (semantics, constitution) pairs, %d live interiors" % (tot, bad))

    # quorum guards: Gridlock survives iff 2 is not an allowed neighbour count
    lives = []
    for q in itertools.chain.from_iterable(
            itertools.combinations((0, 1, 2), r) for r in (1, 2, 3)):
        sem = Sem(quorum=set(q))
        C = Const([(0, 1, 1), (0, -1, -1)], [1, 0])
        live = bool([x for x in actives(solid, C, sem) if 1 <= x[0] <= 3])
        lives.append((tuple(q), live))
    claim("Gridlock under quorum guards: alive iff 2 in the quorum set",
          all(live == (2 in set(q)) for q, live in lives), str(lives))

    # -- (c) DEAD LETTER across the lattice: which semantics admit balance?
    bal = {}
    for sem in (Sem("toggle", "parity"), Sem("toggle", "or"),
                Sem("enact", "parity"), Sem("repeal", "parity"),
                Sem("override", "parity"), Sem("toggle", "parity", immune=(0,))):
        n = 0
        for r0 in RULES1:
            for r1 in RULES1:
                for tm in TMAPS4:
                    C = Const([r0, r1], list(tm))
                    for S in all_seeds(3, 2):
                        if xstep(S, C, sem) == S and actives(S, C, sem):
                            n += 1
        bal[sem.name()] = n
    claim("Dead Letter is exactly the cancellation-free semantics",
          bal["toggle+or"] == 0 and bal["toggle+parity"] > 0
          and bal["enact+parity"] > 0 and bal["repeal+parity"] > 0
          and bal["override+parity"] > 0, str(bal))

    # -- (d) SUNSET: the semantics that breaks H3.  Is it alive?
    sem = Sem(sunset=1)
    cnt = Counter()
    gl = []
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C = Const([r0, r1], list(tm))
                for S in all_seeds(3, 2):
                    A = {(c, k): 1 for c, k in laws(S)}
                    r = sunset_classify(A, C, sem, 200)
                    cnt[r["kind"]] += 1
                    if r["kind"] == "GLIDER":
                        gl.append((r0, r1, tuple(tm), tuple(sorted(S.items())), r))
    ok = False
    if gl:
        r0, r1, tm, S, r = gl[0]
        C = Const([r0, r1], list(tm))
        A = {(c, k): 1 for c, k in laws(dict(S))}
        for _ in range(r["t"]):
            A = sunset_step(A, C, sem)
        ok = verify_sunset_glider(A, C, sem, r["period"], r["displacement"])
    claim("SUNSET semantics (tau=1) admits FREE GLIDERS on Z",
          bool(gl) and ok,
          "%d codes: %s ; %d gliders; first re-verified over 3 periods: %s"
          % (sum(cnt.values()), dict(cnt), len(gl), ok))
    if gl:
        print("      first glider:", gl[0][:4], gl[0][4])
    return bal, cnt, gl


if __name__ == "__main__":
    def c(n, ok, d=""):
        print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", n, d))
    battery(c)
