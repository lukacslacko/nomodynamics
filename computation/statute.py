#!/usr/bin/env python3
"""
statute.py — the STATUTE MACHINE: synchronous Boolean circuits inside the
citation sector of nomodynamics (chapter three).

THE IDEA.  A citation guard reads

        "a law of kind g stands at i+a   AND   no law of kind h stands at i+b"

which is a two-input AND-NOT over kind-fields at fixed offsets, and the target
cell is *toggled*, so several authors of the same provision XOR together.
AND-NOT + XOR + a constant is functionally complete.  What is missing is
ASSIGNMENT: toggling accumulates.  The fix is a *self-clearing kind*

        rule (0,0,0), guard (v, NIL), target {v}

— a provision that repeals itself every step.  A cell holding such a law
contributes its own toggle, so  x(t+1) = x(t) XOR x(t) XOR f(t) = f(t).
The wire is written, not amended.

THE NORMAL FORM.  A constitution is in *statute-machine normal form* if its
kinds split as  K = V (wires) + G (gates) + {NIL}  with

  (W)  every v in V:  rule (0,0,0), guard (v,NIL), target {v};
  (G)  every g in G:  rule (a,b,c), guard (p,n) with p in V+{g}, n in V+{NIL},
                      target T subset of V;
  (N)  NIL is in no target set and is never placed;
  (I)  no g in G is in any target set  (so gate laws are IMMORTAL: the
       hardware is a permanent statute book and only the data moves).

THEOREM 1 (Assignment / Statute-Circuit Theorem).  For a constitution in
normal form, under PARITY resolution, for every cell j and wire v:

  x[j,v](t+1)  =  XOR over gates g and cells i with i + c_g = j and v in T_g
                  of   [g stands at i] AND [p_g at i+a_g] AND NOT [n_g at i+b_g]

and the G-laws never move or vanish.  Proof: step() adds, per (cell,kind), the
parity of all toggles; the only toggles of kind v at cell j come from the
self-clearing v-law at j (contributing x[j,v]) and from the gates above; and
x XOR x = 0.  Gates are never targeted, so their placement is constant.  QED

So a normal-form constitution *is* a synchronous network of AND-NOT gates with
free XOR fan-in, free fan-out (guards are read-only, so any number of gates may
cite the same (cell,kind)) and unit delay.  Everything below is an application.

Run `python3 statute.py` for the self-tests.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xnomos import Const, state_of, step, laws, card, active_laws  # noqa: E402

NIL = "NIL"


# --------------------------------------------------------------------- machine


class Machine:
    """A constitution in statute-machine normal form, built by name."""

    def __init__(self, dim=1, modulus=None):
        self.dim = dim
        self.modulus = modulus
        self.names = [NIL]                     # kind 0 is always NIL
        self.rules = [self._z()]
        self.targets = [()]
        self.guards = [(0, 0)]
        self.wires = []
        self.gates = []
        self._const = None

    def _z(self):
        return (0, 0, 0) if self.dim == 1 else ((0, 0), (0, 0), (0, 0))

    def _off(self, o):
        if self.dim == 1:
            return o
        return tuple(o)

    def idx(self, name):
        return self.names.index(name)

    # -- declarations ------------------------------------------------------
    def wire(self, name):
        """A self-clearing data kind: rule (0,0,0), guard (v,NIL), target {v}."""
        assert name not in self.names, name
        k = len(self.names)
        self.names.append(name)
        self.rules.append(self._z())
        self.targets.append((k,))
        self.guards.append((k, 0))
        self.wires.append(name)
        self._const = None
        return name

    def gate(self, name, pos, a, neg, b, c, out):
        """An immortal gate law.

        pos : wire cited positively (must STAND at i+a); may be `name` itself
              (with a = 0) for an unconditional gate, i.e. a constant source.
        neg : wire cited negatively (must be ABSENT at i+b); NIL = always true.
        c   : offset of the target cell.
        out : list of wire names toggled there.
        """
        assert name not in self.names, name
        k = len(self.names)
        self.names.append(name)
        self.rules.append((self._off(a), self._off(b), self._off(c)))
        pk = k if pos == name else self.idx(pos)
        self.targets.append(tuple(self.idx(w) for w in out))
        self.guards.append((pk, self.idx(neg)))
        self.gates.append(name)
        self._const = None
        return name

    # -- the constitution --------------------------------------------------
    def const(self):
        if self._const is None:
            self._const = Const(self.rules, self.targets, dim=self.dim,
                                modulus=self.modulus, guards=self.guards)
        return self._const

    # -- normal-form audit -------------------------------------------------
    def check_normal_form(self):
        """Re-derive (W),(G),(N),(I) from the raw Const, not from the builder."""
        C = self.const()
        z = self._z()
        errs = []
        widx = {self.idx(w) for w in self.wires}
        gidx = {self.idx(g) for g in self.gates}
        alltg = set()
        for k in range(C.n):
            alltg |= set(C.targets[k])
        for w in self.wires:
            k = self.idx(w)
            if C.rules[k] != z:
                errs.append("wire %s rule != 0" % w)
            if C.targets[k] != (k,):
                errs.append("wire %s target != self" % w)
            if C.guards[k] != (k, 0):
                errs.append("wire %s guard != (self,NIL)" % w)
        for g in self.gates:
            k = self.idx(g)
            if k in alltg:
                errs.append("gate %s is amendable (not immortal)" % g)
            if not set(C.targets[k]) <= widx:
                errs.append("gate %s targets a non-wire" % g)
            p, n = C.guards[k]
            if p not in widx and p != k:
                errs.append("gate %s cites a non-wire positively" % g)
            if n not in widx and n != 0:
                errs.append("gate %s cites a non-wire negatively" % g)
        if 0 in alltg:
            errs.append("NIL is amendable")
        if widx & gidx:
            errs.append("wire/gate overlap")
        return errs

    # -- coding ------------------------------------------------------------
    def code(self, placements):
        """placements: iterable of (cell, name)."""
        return state_of([(c, self.idx(n)) for c, n in placements])

    def read(self, S, cell, name):
        k = self.idx(name)
        if self.dim == 1 and self.modulus is not None:
            cell = cell % self.modulus
        return (S.get(cell, 0) >> k) & 1

    def write(self, S, cell, name, v):
        k = self.idx(name)
        if self.dim == 1 and self.modulus is not None:
            cell = cell % self.modulus
        m = S.get(cell, 0)
        m = (m | (1 << k)) if v else (m & ~(1 << k))
        if m:
            S[cell] = m
        else:
            S.pop(cell, None)
        return S

    def run(self, S, n=1):
        for _ in range(n):
            S = step(S, self.const(), "parity")
        return S

    def label(self):
        out = []
        for k, nm in enumerate(self.names):
            a, b, c = self.rules[k]
            g, h = self.guards[k]
            out.append("%2d %-8s (%s,%s,%s) cite(%s,%s) -> {%s}" % (
                k, nm, a, b, c, self.names[g], self.names[h],
                ",".join(self.names[t] for t in self.targets[k])))
        return "\n".join(out)


# ------------------------------------------------------ the elementary gadgets
# Each returns (Machine, description).  These are the GATE TABLE of the
# citation sector; `gate_table()` certifies every one of them by exhaustion.


def gadget(spec):
    """Build a one-gate machine computing `spec` on wires U,V -> Y at one cell.

    spec is a name from GATES below.
    """
    M = Machine()
    M.wire("U")
    M.wire("V")
    M.wire("Y")
    if spec == "ANDNOT":                      # u & ~v            1 law
        M.gate("g", "U", 0, "V", 0, 0, ["Y"])
    elif spec == "BUF":                       # u                 1 law
        M.gate("g", "U", 0, NIL, 0, 0, ["Y"])
    elif spec == "NOT":                       # ~u                2 laws
        M.gate("g", "g", 0, "U", 0, 0, ["Y"])
    elif spec == "AND":                       # u & v             2 laws
        M.wire("Vb")
        M.gate("nv", "nv", 0, "V", 0, 0, ["Vb"])   # Vb <- ~v      (stage 1)
        M.gate("g", "U", 0, "Vb", 0, 0, ["Y"])     # needs U held  (stage 2)
    elif spec == "OR":                        # u | v = ~(~u & ~v)
        M.wire("Ub")
        M.wire("Vb")
        M.gate("nu", "nu", 0, "U", 0, 0, ["Ub"])
        M.gate("nv", "nv", 0, "V", 0, 0, ["Vb"])
        M.gate("g", "Ub", 0, "Vb", 0, 0, ["Y"])    # ~u & ~v
        M.gate("one", "one", 0, NIL, 0, 0, ["Y"])  # XOR 1  ->  ~(~u&~v)
    elif spec == "XOR":                       # u ^ v             2 laws
        M.gate("gu", "U", 0, NIL, 0, 0, ["Y"])
        M.gate("gv", "V", 0, NIL, 0, 0, ["Y"])
    elif spec == "NAND":                      # ~(u & v)
        M.wire("Vb")
        M.gate("nv", "nv", 0, "V", 0, 0, ["Vb"])
        M.gate("g", "U", 0, "Vb", 0, 0, ["Y"])
        M.gate("one", "one", 0, NIL, 0, 0, ["Y"])
    elif spec == "FANOUT":                    # y1 = y2 = y3 = u
        M.wire("Y2")
        M.wire("Y3")
        M.gate("g1", "U", 0, NIL, 0, 0, ["Y"])
        M.gate("g2", "U", 0, NIL, 0, 0, ["Y2"])
        M.gate("g3", "U", 0, NIL, 0, 0, ["Y3"])
    elif spec == "FANOUT1":                   # one law, three sinks
        M.wire("Y2")
        M.wire("Y3")
        M.gate("g1", "U", 0, NIL, 0, 0, ["Y", "Y2", "Y3"])
    else:
        raise ValueError(spec)
    return M


TRUTH = {
    "ANDNOT": lambda u, v: u & (1 - v),
    "BUF":    lambda u, v: u,
    "NOT":    lambda u, v: 1 - u,
    "AND":    lambda u, v: u & v,
    "OR":     lambda u, v: u | v,
    "XOR":    lambda u, v: u ^ v,
    "NAND":   lambda u, v: 1 - (u & v),
}
DEPTH = {"ANDNOT": 1, "BUF": 1, "NOT": 1, "AND": 2, "OR": 2, "XOR": 1,
         "NAND": 2}


def certify_gate(spec, verbose=False):
    """Exhaustive truth-table certificate for a one-cell gadget."""
    M = gadget(spec)
    assert not M.check_normal_form(), M.check_normal_form()
    f = TRUTH[spec]
    d = DEPTH[spec]
    rows = []
    for u in (0, 1):
        for v in (0, 1):
            S = M.code([(0, g) for g in M.gates])
            if u:
                M.write(S, 0, "U", 1)
            if v:
                M.write(S, 0, "V", 1)
            # inputs must be HELD for depth-2 gadgets: re-assert every step
            for t in range(d):
                S = M.run(S, 1)
                if t < d - 1:
                    M.write(S, 0, "U", u)
                    M.write(S, 0, "V", v)
            got = M.read(S, 0, "Y")
            rows.append((u, v, got, f(u, v)))
            if got != f(u, v):
                return False, rows
    if verbose:
        for r in rows:
            print("   u=%d v=%d -> %d (want %d)" % r)
    return True, rows


def certify_fanout():
    for spec in ("FANOUT", "FANOUT1"):
        M = gadget(spec)
        assert not M.check_normal_form()
        for u in (0, 1):
            S = M.code([(0, g) for g in M.gates])
            if u:
                M.write(S, 0, "U", 1)
            S = M.run(S, 1)
            for w in ("Y", "Y2", "Y3"):
                if M.read(S, 0, w) != u:
                    return False
    return True


def certify_wire(length=12, steps=10):
    """A signal track: hardware laid at every cell, one cell per step."""
    M = Machine()
    M.wire("S")
    M.gate("mv", "S", -1, NIL, 0, 0, ["S"])
    assert not M.check_normal_form()
    S = M.code([(i, "mv") for i in range(length)] + [(0, "S")])
    pos = []
    for t in range(steps):
        p = [c for c, k in laws(S) if k == M.idx("S")]
        pos.append(p)
        S = M.run(S, 1)
    return pos == [[t] if t < length else [] for t in range(steps)], pos


def certify_selfclear(trials=2000, seed=11):
    """Fuzz Theorem 1 on random normal-form machines and random codes."""
    import random
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        nw = rng.randrange(1, 5)
        ng = rng.randrange(1, 6)
        M = Machine()
        ws = ["W%d" % i for i in range(nw)]
        for w in ws:
            M.wire(w)
        gs = []
        for i in range(ng):
            nm = "g%d" % i
            pos = rng.choice(ws + [nm])
            a = 0 if pos == nm else rng.randrange(-1, 2)
            neg = rng.choice(ws + [NIL])
            b = rng.randrange(-1, 2)
            c = rng.randrange(-1, 2)
            out = rng.sample(ws, rng.randrange(1, nw + 1))
            M.gate(nm, pos, a, neg, b, c, out)
            gs.append((nm, pos, a, neg, b, c, out))
        assert not M.check_normal_form()
        # random code
        pl = []
        for cell in range(-3, 4):
            for w in ws:
                if rng.random() < 0.4:
                    pl.append((cell, w))
            for nm, *_ in gs:
                if rng.random() < 0.5:
                    pl.append((cell, nm))
        S = M.code(pl)
        T = M.run(S, 1)
        # independent prediction straight from Theorem 1
        pred = {}
        for cell in range(-5, 6):
            for w in ws:
                acc = 0
                for nm, pos, a, neg, b, c, out in gs:
                    if w not in out:
                        continue
                    i = cell - c
                    if not M.read(S, i, nm):
                        continue
                    pv = 1 if pos == nm else M.read(S, i + a, pos)
                    nv = 0 if neg == NIL else M.read(S, i + b, neg)
                    if pv and not nv:
                        acc ^= 1
                pred[(cell, w)] = acc
            for nm, *_ in gs:                      # gates must be immortal
                if M.read(S, cell, nm) != M.read(T, cell, nm):
                    bad += 1
        for (cell, w), v in pred.items():
            if M.read(T, cell, w) != v:
                bad += 1
    return bad


# ------------------------------------------------------------------ self-tests

def _main():
    ok = 0
    print("STATUTE MACHINE — gate certificates (citation sector, W=1, parity)")
    for spec in ("BUF", "NOT", "ANDNOT", "XOR", "AND", "OR", "NAND"):
        good, rows = certify_gate(spec)
        M = gadget(spec)
        print("  %-7s depth %d, %d gate laws, %d kinds : %s   %s" % (
            spec, DEPTH[spec], len(M.gates), len(M.names),
            "".join(str(r[2]) for r in rows), "OK" if good else "FAIL"))
        assert good
        ok += 1
    assert certify_fanout()
    print("  FANOUT  free (read-only guards): 1->3 by 3 laws and by 1 law  OK")
    ok += 1
    good, pos = certify_wire()
    assert good, pos
    print("  WIRE    signal track: 1 cell/step through static hardware   OK")
    ok += 1
    bad = certify_selfclear()
    assert bad == 0, bad
    print("  THM 1   2000 random normal-form machines x random codes: "
          "0 deviations from the predicted circuit semantics             OK")
    ok += 1
    print("statute self-tests passed: %d/%d" % (ok, 10))


if __name__ == "__main__":
    _main()
