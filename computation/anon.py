#!/usr/bin/env python3
"""
anon.py — THE ANONYMOUS STATUTE MACHINE: computation without citation.

Chapter three predicted (CITATION.md, Y3) that the first universality
construction would need CITATION, because "kind A here and kind B absent there"
is an explicit AND-NOT.  That prediction is wrong, and this file is why.

The FOUNDING guard already is an AND-NOT:

        "some law stands at i+a   AND   no law stands at i+b"

— an AND-NOT over the OCCUPANCY field.  What citation buys is only that several
independent bits can share one cell.  Give up that convenience and spend CELLS
instead of kinds, and the whole circuit substrate reappears in the anonymous
sector of chapters one and two, with `guards=None`.

THE LAYOUT.  Each logical SITE is a block of L = r + 2 consecutive cells:

        [ w_0 | w_1 | ... | w_{r-1} | POWER | GAP ]

  * `w_i` is a WIRE cell: OCCUPIED means the bit is 1, EMPTY means 0.  Its kind
    has rule (0, r+1-i, 0) and targets itself — the a-clause reads its own cell,
    which is occupied whenever the law stands there, so the guard's precedent is
    vacuously satisfied; the b-clause reads the block's GAP, which is empty
    forever.  The law is therefore always active and repeals itself every step:
    a SELF-CLEARING wire, exactly as in the citation sector.
  * `POWER` carries one law of a kind with rule (0,0,0) — a == b, so its guard
    is self-contradictory and it never acts, and nobody amends it, so it stands
    forever.  An unenforceable statute used as scaffolding: the field's own
    "dead letter" (xrings, P9).  Every GATE law is placed in this cell, which is
    thus permanently occupied, so a gate whose a-offset is 0 is always enabled.
  * `GAP` is never targeted by anything, so it is empty forever: the constant
    FALSE that every vacancy clause needs.

A GATE is then one law with rule (a, b, c) reading two wire cells and toggling
the wire kind of a third.  ITS OUT-DEGREE IS 1.

    THEOREM 4.  The anonymous (occupancy-guard) sector of chapters one and two
    is computation-universal, at OUT-DEGREE 1 — inside the sector the
    Out-Degree Law proves incapable of motion.  Nothing travels; information
    does.

Run `python3 anon.py`.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xnomos import Const, state_of, step, laws                    # noqa: E402

NIL = "NIL"


class AnonMachine:
    """Same builder API as statute.Machine, but compiled to OCCUPANCY guards.

    Offsets passed to `gate` are in SITES; the layout turns them into cells.
    A gate with several output wires is split into one law-kind per output,
    because a single kind toggles at exactly one cell.
    """

    def __init__(self, dim=1, modulus=None):
        assert dim == 1
        self.modulus = modulus            # sites; the ring is L*modulus cells
        self.dim = 1
        self.wires = []
        self.gate_specs = {}              # logical name -> list of piece names
        self._pieces = []                 # (name, a, b, c, target-wire-index)
        self._const = None
        self._L = None

    # -- declarations ------------------------------------------------------
    def wire(self, name):
        assert self._const is None, "declare all wires before building"
        assert name not in self.wires
        self.wires.append(name)
        return name

    def gate(self, name, pos, a, neg, b, c, out):
        assert name not in self.gate_specs
        self.gate_specs[name] = (pos, a, neg, b, c, list(out))
        return name

    def raw(self, name, a, b, c, targets, slot=None):
        """A kind outside the wire/gate discipline, with CELL offsets.

        Used only for the BUILDING FRONT, which must amend gate laws (and so
        breaks the immortality clause) in order to enact them at virgin sites.
        `slot` is the slot the law is placed in (default: POWER).  Offsets a, b,
        c are in cells, measured from that slot.  `targets` are kind names,
        resolved after the layout is fixed (forward references allowed).
        """
        if not hasattr(self, "_raw"):
            self._raw = []
        self._raw.append((name, a, b, c, list(targets), slot))
        self._const = None
        return name

    # -- layout ------------------------------------------------------------
    def _build(self):
        if self._const is not None:
            return
        r = len(self.wires)
        L = r + 2
        self._L = L
        self._pieces = []
        self.POWER_OFF = r
        self.GAP_OFF = r + 1
        widx = {w: i for i, w in enumerate(self.wires)}
        self.widx = widx
        rules, targets, names = [], [], []
        # wire kinds 0..r-1
        for i, w in enumerate(self.wires):
            rules.append((0, r + 1 - i, 0))
            targets.append((i,))
            names.append(w)
        # POWER kind: a == b, an unconditional dead letter
        self.POWER = r
        rules.append((0, 0, 0))
        targets.append((r,))
        names.append("POWER")
        # gate kinds: one per (logical gate, output wire)
        self.pieces = {}
        for gname, (pos, a, neg, b, c, out) in self.gate_specs.items():
            ps = []
            for w in out:
                # a-offset: from the POWER cell of the gate's own site
                if pos == gname:
                    ao = 0                                   # own cell: occupied
                else:
                    ao = a * L + widx[pos] - r
                if neg == NIL:
                    bo = 1                                   # the block's GAP
                else:
                    bo = b * L + widx[neg] - r
                co = c * L + widx[w] - r
                k = len(rules)
                rules.append((ao, bo, co))
                targets.append((widx[w],))
                nm = gname if len(out) == 1 else "%s#%s" % (gname, w)
                names.append(nm)
                self.pieces[nm] = k
                ps.append(nm)
            self.gate_specs[gname] = (pos, a, neg, b, c, out)
            self.pieces.setdefault(gname, None)
            self._pieces.append((gname, ps))
        self.gate_pieces = {g: ps for g, ps in self._pieces}
        self.gates = list(self.gate_specs)
        # raw kinds (the building front): two passes for forward references
        self.raw_kinds = {}
        self.raw_slot = {}
        for nm, a, b, c, tg, slot in getattr(self, "_raw", []):
            self.raw_kinds[nm] = len(rules)
            self.raw_slot[nm] = self.POWER_OFF if slot is None else slot
            rules.append((a, b, c))
            targets.append(())
            names.append(nm)
        self.names = names
        for nm, a, b, c, tg, slot in getattr(self, "_raw", []):
            k = self.raw_kinds[nm]
            targets[k] = tuple(names.index(t) for t in tg)
        self.rules = rules
        self.targets = targets
        self._const = Const(rules, targets, dim=1,
                            modulus=None if self.modulus is None
                            else L * self.modulus)

    def const(self):
        self._build()
        return self._const

    def idx(self, name):
        self._build()
        return self.names.index(name)

    @property
    def L(self):
        self._build()
        return self._L

    # -- coding ------------------------------------------------------------
    def cell(self, site, name):
        """The cell of a wire (or of the POWER slot, for a gate) at `site`."""
        self._build()
        if name in self.widx:
            return site * self._L + self.widx[name]
        return site * self._L + self.POWER_OFF

    def code(self, placements, sites=None):
        """placements: (site, name).  POWER is added at every site used."""
        self._build()
        used = set()
        pl = []
        for site, name in placements:
            used.add(site)
            if name in self.widx:
                pl.append((self.cell(site, name), self.idx(name)))
            elif name in self.gate_pieces:
                for p in self.gate_pieces[name]:
                    pl.append((site * self._L + self.POWER_OFF, self.idx(p)))
            else:
                pl.append((site * self._L + self.raw_slot[name],
                           self.raw_kinds[name]))
        for site in (used if sites is None else sites):
            pl.append((site * self._L + self.POWER_OFF, self.POWER))
        return state_of(pl)

    def read(self, S, site, name):
        self._build()
        c = self.cell(site, name)
        if self.modulus is not None:
            c %= self._L * self.modulus
        return 1 if S.get(c, 0) else 0

    def run(self, S, n=1):
        C = self.const()
        for _ in range(n):
            S = step(S, C, "parity")
        return S

    # -- audit -------------------------------------------------------------
    def check(self):
        """Verify the claims the construction rests on, from the raw Const."""
        C = self.const()
        errs = []
        if C.cited:
            errs.append("guards are not anonymous!")
        for k in range(C.n):
            if self.names[k] in self.raw_kinds:
                continue                      # the front is exempt by design
            if len(C.targets[k]) != 1:
                errs.append("kind %s has out-degree %d" %
                            (self.names[k], len(C.targets[k])))
        # POWER: never active, never targeted
        a, b, _ = C.rules[self.POWER]
        if a != b:
            errs.append("POWER is not a dead letter")
        for k in range(C.n):
            if k != self.POWER and self.POWER in C.targets[k]:
                errs.append("POWER is amendable")
        # wires: self-targeting
        for i, w in enumerate(self.wires):
            if C.targets[i] != (i,):
                errs.append("wire %s not self-clearing" % w)
        return errs

    def window(self):
        C = self.const()
        return max(max(abs(x) for x in r) for r in C.rules)

    def site_locality(self):
        """Machine-check the SITE-LOCALITY lemma from the raw Const.

        Reads every rule of every kind, resolves each offset to (site, slot)
        relative to the law's own site, and certifies:
          * every wire law reads only its own site and writes only its own cell;
          * every gate law reads slots that are WIRE slots (or its own POWER
            cell / the GAP) at site offsets in {-1,0,+1}, and writes a WIRE slot
            at site offset 0.
        Returns (radius_in_sites, errors).  A radius-1 certificate means the
        3-step map is site-local of radius 3, so the 2^7 configurations of the
        7-site ring exhaust its inputs.
        """
        C = self.const()
        L, r = self._L, len(self.wires)
        errs = []
        rad = 0

        def resolve(base_slot, off):
            p = base_slot + off
            return (p // L, p % L)          # (site offset, slot)

        for k in range(C.n):
            a, b, c = C.rules[k]
            if k < r:                                          # a wire law
                base = k
                for off, why in ((a, "a"), (b, "b"), (c, "c")):
                    s, sl = resolve(base, off)
                    if s != 0:
                        errs.append("wire %s %s leaves its site" %
                                    (self.names[k], why))
                if (a, c) != (0, 0) or resolve(base, b)[1] != r + 1:
                    errs.append("wire %s not (own cell, GAP, self)"
                                % self.names[k])
            elif k == self.POWER or self.names[k] in self.raw_kinds:
                pass
            else:                                              # a gate law
                base = r
                sa, sla = resolve(base, a)
                sb, slb = resolve(base, b)
                sc, slc = resolve(base, c)
                for s, sl, why in ((sa, sla, "a"), (sb, slb, "b")):
                    if sl >= r and not (s == 0 and sl in (r, r + 1)):
                        errs.append("gate %s reads a non-wire slot %d at site "
                                    "%+d" % (self.names[k], sl, s))
                    rad = max(rad, abs(s))
                if sc != 0 or slc >= r:
                    errs.append("gate %s writes outside its own site's wires"
                                % self.names[k])
        return rad, errs

    def outdeg(self, include_front=True):
        C = self.const()
        return max(len(t) for k, t in enumerate(C.targets)
                   if include_front or self.names[k] not in self.raw_kinds)


# ---------------------------------------------------------------- the gate table

def anon_gadget(spec):
    """The same gate table as statute.gadget, in the anonymous sector."""
    M = AnonMachine()
    M.wire("U")
    M.wire("V")
    M.wire("Y")
    M.gate("srcU", "srcU", 0, NIL, 0, 0, ["U"])
    M.gate("srcV", "srcV", 0, NIL, 0, 0, ["V"])
    if spec == "ANDNOT":
        M.gate("g", "U", 0, "V", 0, 0, ["Y"])
    elif spec == "BUF":
        M.gate("g", "U", 0, NIL, 0, 0, ["Y"])
    elif spec == "NOT":
        M.gate("g", "g", 0, "U", 0, 0, ["Y"])
    elif spec == "XOR":
        M.gate("gu", "U", 0, NIL, 0, 0, ["Y"])
        M.gate("gv", "V", 0, NIL, 0, 0, ["Y"])
    elif spec == "AND":
        M.wire("Vb")
        M.gate("nv", "nv", 0, "V", 0, 0, ["Vb"])
        M.gate("g", "U", 0, "Vb", 0, 0, ["Y"])
    elif spec == "NAND":
        M.wire("Vb")
        M.gate("nv", "nv", 0, "V", 0, 0, ["Vb"])
        M.gate("g", "U", 0, "Vb", 0, 0, ["Y"])
        M.gate("one", "one", 0, NIL, 0, 0, ["Y"])
    elif spec == "OR":
        M.wire("Ub")
        M.gate("nu", "nu", 0, "U", 0, 0, ["Ub"])
        M.gate("g", "Ub", 0, "V", 0, 0, ["Y"])
        M.gate("one", "one", 0, NIL, 0, 0, ["Y"])
    elif spec == "XNOR":
        M.gate("gu", "U", 0, NIL, 0, 0, ["Y"])
        M.gate("gv", "V", 0, NIL, 0, 0, ["Y"])
        M.gate("one", "one", 0, NIL, 0, 0, ["Y"])
    elif spec == "IMPL":
        M.gate("g", "U", 0, "V", 0, 0, ["Y"])
        M.gate("one", "one", 0, NIL, 0, 0, ["Y"])
    elif spec == "ONE":
        M.gate("one", "one", 0, NIL, 0, 0, ["Y"])
    elif spec == "ZERO":
        pass
    elif spec == "FANOUT":
        M.wire("Y2")
        M.wire("Y3")
        M.gate("g1", "U", 0, NIL, 0, 0, ["Y", "Y2", "Y3"])
    else:
        raise ValueError(spec)
    return M


TRUTH = {
    "ANDNOT": lambda u, v: u & (1 - v), "BUF": lambda u, v: u,
    "NOT": lambda u, v: 1 - u, "AND": lambda u, v: u & v,
    "OR": lambda u, v: u | v, "XOR": lambda u, v: u ^ v,
    "XNOR": lambda u, v: 1 - (u ^ v), "NAND": lambda u, v: 1 - (u & v),
    "IMPL": lambda u, v: 1 - (u & (1 - v)), "ZERO": lambda u, v: 0,
    "ONE": lambda u, v: 1,
}
DEPTH = {"ANDNOT": 1, "BUF": 1, "NOT": 1, "XOR": 1, "IMPL": 1, "ZERO": 0,
         "ONE": 1, "AND": 2, "OR": 2, "NAND": 2, "XNOR": 1}


def certify_gate(spec):
    M = anon_gadget(spec)
    assert not M.check(), M.check()
    rows = []
    for u in (0, 1):
        for v in (0, 1):
            pl = [(0, g) for g in M.gates
                  if not (g == "srcU" and not u) and not (g == "srcV" and not v)]
            pl += [(0, "U")] * u + [(0, "V")] * v
            S = M.code(pl)
            S = M.run(S, DEPTH[spec])
            got = M.read(S, 0, "Y")
            T = dict(S)
            for _ in range(6):
                T = M.run(T, 1)
                if M.read(T, 0, "Y") != got:
                    return False, rows
            rows.append(got)
            if got != TRUTH[spec](u, v):
                return False, rows
    return True, rows


def certify_fanout():
    M = anon_gadget("FANOUT")
    for u in (0, 1):
        pl = [(0, "g1")] + ([(0, "srcU"), (0, "U")] if u else [])
        S = M.code(pl)
        for _ in range(6):
            S = M.run(S, 1)
            for w in ("Y", "Y2", "Y3"):
                if M.read(S, 0, w) != u:
                    return False
    return True


# ------------------------------------------------------------------ Rule 110


def build110(modulus=None):
    """The SAME circuit as rule110.build(), compiled anonymously."""
    M = AnonMachine(modulus=modulus)
    for w in ("X", "Xb", "A", "Ab", "X1", "X2", "A2", "B", "K0", "K1", "K2"):
        M.wire(w)
    M.gate("gA",  "X",  0, "Xb", +1, 0, ["A", "Ab"])
    M.gate("gX1", "X",  0, NIL,   0, 0, ["X1"])
    M.gate("kK0", "K0", 0, NIL,   0, 0, ["K1", "Ab"])
    M.gate("gB",  "X1", -1, "Ab", 0, 0, ["B"])
    M.gate("gX2", "X1", 0, NIL,   0, 0, ["X2"])
    M.gate("gA2", "A",  0, NIL,   0, 0, ["A2"])
    M.gate("kK1", "K1", 0, NIL,   0, 0, ["K2"])
    M.gate("gY0", "X2", 0,  NIL, 0, 0, ["X", "Xb"])
    M.gate("gY1", "X2", +1, NIL, 0, 0, ["X", "Xb"])
    M.gate("gY2", "A2", 0,  NIL, 0, 0, ["X", "Xb"])
    M.gate("gY3", "B",  0,  NIL, 0, 0, ["X", "Xb"])
    M.gate("kK2", "K2", 0,  NIL, 0, 0, ["K0", "Xb"])
    return M


GATES110 = list(build110().gate_specs)


def encode110(M, bits, sites):
    pl = []
    for s in sites:
        pl += [(s, g) for g in GATES110]
        pl.append((s, "K0"))
    for s, b in zip(sites, bits):
        pl.append((s, "X" if b else "Xb"))
    return M.code(pl, sites=sites)


def rule110_step(bits):
    n = len(bits)
    T = {(1, 1, 1): 0, (1, 1, 0): 1, (1, 0, 1): 1, (1, 0, 0): 0,
         (0, 1, 1): 1, (0, 1, 0): 1, (0, 0, 1): 1, (0, 0, 0): 0}
    return [T[(bits[(i - 1) % n], bits[i], bits[(i + 1) % n])]
            for i in range(n)]


def certify110_local():
    """COMPLETE: all 2^7 configurations of the 7-site ring."""
    M = build110(modulus=7)
    sites = list(range(7))
    bad = []
    for code in range(128):
        bits = [(code >> i) & 1 for i in range(7)]
        S = encode110(M, bits, sites)
        T = M.run(S, 3)
        got = [M.read(T, s, "X") for s in sites]
        if got != rule110_step(bits):
            bad.append((bits, got))
    return len(bad) == 0, bad, 128


def certify110_ring(m, steps=12):
    M = build110(modulus=m)
    sites = list(range(m))
    for code in range(1 << m):
        bits = [(code >> i) & 1 for i in range(m)]
        S = encode110(M, bits, sites)
        ref = list(bits)
        for _ in range(steps):
            S = M.run(S, 3)
            ref = rule110_step(ref)
            if [M.read(S, s, "X") for s in sites] != ref:
                return False, code
    return True, 1 << m


def _main():
    print("THE ANONYMOUS STATUTE MACHINE — occupancy guards only "
          "(guards=None, chapters one and two)")
    print("  %-7s %5s %5s  %-6s %s" % ("gate", "depth", "kinds", "table",
                                       "verdict"))
    for spec in ("ZERO", "ONE", "BUF", "NOT", "ANDNOT", "IMPL", "XOR", "XNOR",
                 "AND", "NAND", "OR"):
        good, rows = certify_gate(spec)
        M = anon_gadget(spec)
        print("  %-7s %5d %5d  %-6s %s" % (spec, DEPTH[spec],
                                           len(M.const().rules),
                                           "".join(map(str, rows)),
                                           "OK" if good else "FAIL"))
        assert good, (spec, rows)
    assert certify_fanout()
    print("  FANOUT  free                                        OK")
    print()
    M = build110()
    C = M.const()
    print("  Rule 110, anonymously: %d kinds, block L = %d cells/site, "
          "window %d," % (C.n, M.L, M.window()))
    print("     max out-degree %d, guards anonymous: %s" %
          (M.outdeg(), not C.cited))
    print("  audit:", M.check() or "clean")
    rad, errs = M.site_locality()
    print("  site-locality lemma (read off the raw Const): radius %d site%s, "
          "%s" % (rad, "" if rad == 1 else "s", errs or "no violations"))
    assert not errs and rad == 1
    ok, bad, n = certify110_local()
    print("  COMPLETE local certificate: all %d configurations of the 7-site "
          "ring -> %s" % (n, "EXACT" if ok else "FAIL %r" % bad[:2]))
    assert ok
    for m in (8, 9, 10):
        good, cnt = certify110_ring(m)
        print("  %d-site ring: all %d configurations x 12 Rule-110 steps -> %s"
              % (m, cnt, "EXACT" if good else "FAIL"))
        assert good
    print("anon self-tests passed")


if __name__ == "__main__":
    _main()
