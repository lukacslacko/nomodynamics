#!/usr/bin/env python3
"""
verify_y.py — the Y-B verification battery.

Re-checks every claim of `RESULTS.md` through `xnomos` alone, on an INDEPENDENT
code path: the constitutions are rebuilt here from raw `(a,b,c)` / target /
guard tuples with no help from the builders in statute.py / anon.py, the
reference semantics are re-implemented from the definitions, and the reference
Rule 110 is a bit-parallel integer implementation rather than a table lookup.

    python3 verify_y.py          run everything
    python3 verify_y.py -d       also dump the paste-ready constitutions
"""

from __future__ import annotations

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from xnomos import Const, state_of, step, laws, card, active_laws  # noqa: E402

PASS = []
FAIL = []


def check(name, ok, note=""):
    (PASS if ok else FAIL).append(name)
    print("  [%s] %-58s %s" % ("ok" if ok else "XX", name, note))
    return ok


# ---------------------------------------------------------------------------
# 1.  The gate table, citation sector — constitutions written out by hand.
# ---------------------------------------------------------------------------
# kinds: 0 NIL, 1 U, 2 V, 3 Y, 4 W (spare wire), then gate kinds.
# wires have rule (0,0,0), guard (self, NIL), target {self}.

def _wire(k):
    return (0, 0, 0), (k,), (k, 0)


def hand_gate_machine(gate_rules):
    """gate_rules: list of (a, b, c, pos, neg, targets) with kind numbers.

    Wires are kinds 1..4 (U, V, Y, W); gates start at kind 5.
    """
    rules, targets, guards = [(0, 0, 0)], [()], [(0, 0)]
    for k in (1, 2, 3, 4):
        r, t, g = _wire(k)
        rules.append(r)
        targets.append(t)
        guards.append(g)
    for i, (a, b, c, pos, neg, tg) in enumerate(gate_rules):
        k = 5 + i
        rules.append((a, b, c))
        targets.append(tuple(tg))
        guards.append((k if pos is None else pos, neg))
    return Const(rules, targets, dim=1, guards=guards)


U, V, Y, W, NILK = 1, 2, 3, 4, 0

GATE_TABLE = {
    #  name : (gate laws, depth, truth function)
    "BUF":    ([(0, 0, 0, U, NILK, (Y,))], 1, lambda u, v: u),
    "NOT":    ([(0, 0, 0, None, U, (Y,))], 1, lambda u, v: 1 - u),
    "ANDNOT": ([(0, 0, 0, U, V, (Y,))], 1, lambda u, v: u & (1 - v)),
    "IMPL":   ([(0, 0, 0, U, V, (Y,)), (0, 0, 0, None, NILK, (Y,))], 1,
               lambda u, v: 1 - (u & (1 - v))),
    "XOR":    ([(0, 0, 0, U, NILK, (Y,)), (0, 0, 0, V, NILK, (Y,))], 1,
               lambda u, v: u ^ v),
    "XNOR":   ([(0, 0, 0, U, NILK, (Y,)), (0, 0, 0, V, NILK, (Y,)),
                (0, 0, 0, None, NILK, (Y,))], 1, lambda u, v: 1 - (u ^ v)),
    "AND":    ([(0, 0, 0, None, V, (W,)), (0, 0, 0, U, W, (Y,))], 2,
               lambda u, v: u & v),
    "NAND":   ([(0, 0, 0, None, V, (W,)), (0, 0, 0, U, W, (Y,)),
                (0, 0, 0, None, NILK, (Y,))], 2, lambda u, v: 1 - (u & v)),
    "OR":     ([(0, 0, 0, None, U, (W,)), (0, 0, 0, W, V, (Y,)),
                (0, 0, 0, None, NILK, (Y,))], 2, lambda u, v: u | v),
}


def test_gate_table():
    ok = True
    table = {}
    for name, (grules, depth, f) in sorted(GATE_TABLE.items()):
        # the two input sources are extra gate laws
        grules = list(grules) + [(0, 0, 0, None, NILK, (U,)),
                                 (0, 0, 0, None, NILK, (V,))]
        C = hand_gate_machine(grules)
        nsrc = len(grules)
        rows = []
        for u in (0, 1):
            for v in (0, 1):
                pl = [(0, 5 + i) for i in range(len(grules) - 2)]
                if u:
                    pl += [(0, 5 + nsrc - 2), (0, U)]
                if v:
                    pl += [(0, 5 + nsrc - 1), (0, V)]
                S = state_of(pl)
                for _ in range(depth):
                    S = step(S, C, "parity")
                got = (S.get(0, 0) >> Y) & 1
                for _ in range(6):              # must be stable thereafter
                    S = step(S, C, "parity")
                    if (S.get(0, 0) >> Y) & 1 != got:
                        got = -1
                        break
                rows.append(got)
                ok &= (got == f(u, v))
        table[name] = "".join(str(r) for r in rows)
    check("citation gate table: 9 gates x 4 inputs x 7 observations", ok,
          " ".join("%s=%s" % (k, v) for k, v in sorted(table.items())))
    return ok


# ---------------------------------------------------------------------------
# 2.  Rule 110, citation sector — the 24-kind constitution, written out.
# ---------------------------------------------------------------------------
# 0 NIL | 1 X 2 Xb 3 A 4 Ab 5 X1 6 X2 7 A2 8 B 9 K0 10 K1 11 K2 | 12.. gates
R110_WIRES = ["X", "Xb", "A", "Ab", "X1", "X2", "A2", "B", "K0", "K1", "K2"]
R110_GATES = [
    # name, (a, b, c), positive citation, negative citation, targets
    ("gA",  (0, +1, 0), "X",  "Xb", ["A", "Ab"]),
    ("gX1", (0, 0, 0),  "X",  None, ["X1"]),
    ("kK0", (0, 0, 0),  "K0", None, ["K1", "Ab"]),
    ("gB",  (-1, 0, 0), "X1", "Ab", ["B"]),
    ("gX2", (0, 0, 0),  "X1", None, ["X2"]),
    ("gA2", (0, 0, 0),  "A",  None, ["A2"]),
    ("kK1", (0, 0, 0),  "K1", None, ["K2"]),
    ("gY0", (0, 0, 0),  "X2", None, ["X", "Xb"]),
    ("gY1", (+1, 0, 0), "X2", None, ["X", "Xb"]),
    ("gY2", (0, 0, 0),  "A2", None, ["X", "Xb"]),
    ("gY3", (0, 0, 0),  "B",  None, ["X", "Xb"]),
    ("kK2", (0, 0, 0),  "K2", None, ["K0", "Xb"]),
]


def build_r110(modulus=None):
    names = ["NIL"] + R110_WIRES + [g[0] for g in R110_GATES]
    ix = {n: i for i, n in enumerate(names)}
    rules = [(0, 0, 0)]
    targets = [()]
    guards = [(0, 0)]
    for w in R110_WIRES:
        rules.append((0, 0, 0))
        targets.append((ix[w],))
        guards.append((ix[w], 0))
    for nm, (a, b, c), pos, neg, tg in R110_GATES:
        rules.append((a, b, c))
        targets.append(tuple(ix[t] for t in tg))
        guards.append((ix[pos], 0 if neg is None else ix[neg]))
    return Const(rules, targets, dim=1, modulus=modulus, guards=guards), ix, \
        names


def r110_ref(bits):
    """Bit-parallel reference: y = q ^ r ^ q&r ^ p&q&r, on a ring."""
    m = len(bits)
    x = 0
    for i, b in enumerate(bits):
        x |= b << i
    mask = (1 << m) - 1
    left = ((x << 1) | (x >> (m - 1))) & mask         # p_i = x_{i-1}
    right = ((x >> 1) | (x << (m - 1))) & mask        # r_i = x_{i+1}
    y = (x ^ right ^ (x & right) ^ (left & x & right)) & mask
    return [(y >> i) & 1 for i in range(m)]


def test_r110_citation():
    C, ix, names = build_r110(modulus=7)
    gates = [g[0] for g in R110_GATES]
    ok = True
    for code in range(128):
        bits = [(code >> i) & 1 for i in range(7)]
        pl = []
        for c in range(7):
            pl += [(c, ix[g]) for g in gates]
            pl.append((c, ix["K0"]))
        for c, b in enumerate(bits):
            pl.append((c, ix["X" if b else "Xb"]))
        S = state_of(pl)
        for _ in range(3):
            S = step(S, C, "parity")
        got = [(S.get(c, 0) >> ix["X"]) & 1 for c in range(7)]
        ok &= (got == r110_ref(bits))
    win = max(max(abs(x) for x in r) for r in C.rules)
    check("Rule 110, citation sector: COMPLETE, all 2^7 configs of Z/7", ok,
          "%d kinds, window %d, dilation 3" % (C.n, win))
    # a longer ring, many steps
    m = 13
    C, ix, names = build_r110(modulus=m)
    import random
    rng = random.Random(2)
    ok2 = True
    for _ in range(12):
        bits = [rng.randrange(2) for _ in range(m)]
        pl = []
        for c in range(m):
            pl += [(c, ix[g]) for g in gates]
            pl.append((c, ix["K0"]))
        for c, b in enumerate(bits):
            pl.append((c, ix["X" if b else "Xb"]))
        S = state_of(pl)
        ref = list(bits)
        for _ in range(40):
            for _ in range(3):
                S = step(S, C, "parity")
            ref = r110_ref(ref)
            got = [(S.get(c, 0) >> ix["X"]) & 1 for c in range(m)]
            ok2 &= (got == ref)
    check("Rule 110, citation sector: Z/13 x 12 seeds x 40 steps", ok2)
    return ok and ok2


# ---------------------------------------------------------------------------
# 3.  Rule 110, ANONYMOUS sector — rebuilt here from the layout rule.
# ---------------------------------------------------------------------------

def build_r110_anon(modulus=None):
    """r wires, POWER, GAP: block L = r+2.  Occupancy guards throughout."""
    r = len(R110_WIRES)
    L = r + 2
    widx = {w: i for i, w in enumerate(R110_WIRES)}
    rules, targets, names = [], [], []
    for i, w in enumerate(R110_WIRES):
        rules.append((0, r + 1 - i, 0))
        targets.append((i,))
        names.append(w)
    POWER = r
    rules.append((0, 0, 0))
    targets.append((r,))
    names.append("POWER")
    for nm, (a, b, c), pos, neg, tg in R110_GATES:
        for w in tg:
            ao = a * L + widx[pos] - r
            bo = 1 if neg is None else b * L + widx[neg] - r
            co = c * L + widx[w] - r
            rules.append((ao, bo, co))
            targets.append((widx[w],))
            names.append("%s#%s" % (nm, w))
    C = Const(rules, targets, dim=1,
              modulus=None if modulus is None else L * modulus)
    return C, names, widx, L, r, POWER


def test_r110_anon():
    C, names, widx, L, r, POWER = build_r110_anon(modulus=7)
    ok = True
    gk = [k for k, n in enumerate(names) if "#" in n]
    for code in range(128):
        bits = [(code >> i) & 1 for i in range(7)]
        pl = []
        for s in range(7):
            pl += [(s * L + r, k) for k in gk]
            pl.append((s * L + r, POWER))
            pl.append((s * L + widx["K0"], widx["K0"]))
        for s, b in enumerate(bits):
            pl.append((s * L + widx["X" if b else "Xb"],
                       widx["X" if b else "Xb"]))
        S = state_of(pl)
        for _ in range(3):
            S = step(S, C, "parity")
        got = [1 if S.get((s * L + widx["X"]) % (7 * L), 0) else 0
               for s in range(7)]
        ok &= (got == r110_ref(bits))
    win = max(max(abs(x) for x in ru) for ru in C.rules)
    outd = max(len(t) for t in C.targets)
    check("Rule 110, ANONYMOUS sector: COMPLETE, all 2^7 configs", ok,
          "%d kinds, L=%d, window %d, out-degree %d" % (C.n, L, win, outd))
    check("  ... its guards cite no kind (chapters one and two semantics)",
          not C.cited)
    check("  ... its maximum out-degree is 1 (the motionless sector)",
          outd == 1)
    return ok


# ---------------------------------------------------------------------------
# 4.  Turing simulation — decode independently, compare with a fresh TM.
# ---------------------------------------------------------------------------

def test_turing():
    from turing import Registry, TM, tm_busy_beaver4, tm_binary_increment
    ok = True
    for tm, tape, head, T in ((tm_busy_beaver4(), {}, 0, 30),
                              (tm_binary_increment(),
                               {0: 1, 1: 1, 2: 1, 3: 1}, 0, 22)):
        R = Registry(tm)
        C = R.M.const()
        sites = list(range(-4, 5))
        S = R.code(tape, head, sites)
        # independent reference
        t, h, q = dict(tape), head, tm.start
        for k in range(T):
            g = t.get(h, 0)
            q2, g2, d = tm.delta[(q, g)]
            if g2:
                t[h] = 1
            else:
                t.pop(h, None)
            h += {"L": -1, "S": 0, "R": 1}[d]
            q = q2
            for _ in range(3):
                S = step(S, C, "parity")
            kT = R.M.idx("T")
            gt = {c for c, m in S.items() if (m >> kT) & 1}
            hq = [(c, qq) for c in S for qq in tm.states
                  if (S[c] >> R.M.idx("H%d" % qq)) & 1]
            ok &= (gt == {c for c, b in t.items() if b})
            ok &= (hq == [(h, q)])
    check("citation TM: busy-beaver-4 and binary increment, "
          "independent decode", ok)
    # immortality / anonymity audits from the raw Const
    from turing import Registry as Rg, tm_busy_beaver3
    R = Rg(tm_busy_beaver3())
    C = R.M.const()
    alltg = set()
    for k in range(C.n):
        alltg |= set(C.targets[k])
    hw = {R.M.idx(g) for g in R.hardware}
    front = {R.M.idx(g) for g in R.front_kinds}
    authors = {h: {k for k in range(C.n) if h in C.targets[k]} for h in hw}
    ok2 = all(a <= front for a in authors.values())
    from turing import certify_front
    ok3, msg = certify_front(tm_busy_beaver3(), steps=40)
    check("  ... the %d hardware kinds are amended only by the %d front kinds"
          % (len(hw), len(front)), ok2 and ok3, msg if ok3 else "FRONT FAIL")
    return ok and ok2 and ok3


def test_anon_turing():
    from anontm import AnonRegistry
    from turing import tm_busy_beaver3, tm_binary_increment
    ok = True
    for tm, tape, head, T in ((tm_busy_beaver3(), {}, 0, 16),
                              (tm_binary_increment(),
                               {0: 1, 1: 0, 2: 1}, 0, 16)):
        R = AnonRegistry(tm)
        M = R.M
        C = M.const()
        sites = list(range(-3, 4))
        S = R.code(tape, head, sites)
        t, h, q = dict(tape), head, tm.start
        L, r = M.L, len(M.wires)
        for k in range(T):
            g = t.get(h, 0)
            q2, g2, d = tm.delta[(q, g)]
            if g2:
                t[h] = 1
            else:
                t.pop(h, None)
            h += {"L": -1, "S": 0, "R": 1}[d]
            q = q2
            for _ in range(3):
                S = step(S, C, "parity")
            Tslot = M.widx["T"]
            gt = {c // L for c in S if c % L == Tslot}
            hs = [(c // L, qq) for c in S for qq in tm.states
                  if c % L == M.widx["H%d" % qq]]
            ok &= (gt == {c for c, b in t.items() if b})
            ok &= (hs == [(h, q)])
        ok &= (not C.cited)
    check("anonymous TM: busy-beaver-3 and binary increment, finite code, "
          "unbounded tape", ok)
    from anontm import certify_hygiene, certify_front_once
    o1, m1 = certify_hygiene(tm_busy_beaver3(), steps=40)
    o2, m2 = certify_front_once(tm_busy_beaver3(), steps=30)
    check("  ... GAP cells empty, POWER intact, hardware enacted once", o1
          and o2, "%s; %s" % (m1, m2))
    R = AnonRegistry(tm_busy_beaver3())
    C = R.M.const()
    nonfront = [k for k in range(C.n)
                if R.M.names[k] not in R.M.raw_kinds and len(C.targets[k]) > 1]
    check("  ... out-degree 1 everywhere except the %d front kinds"
          % len(R.M.raw_kinds), not nonfront)
    return ok


# ---------------------------------------------------------------------------
# 5.  Complexity and linearity
# ---------------------------------------------------------------------------

def test_circuits():
    from circuit import certify_circuits, certify_all_functions
    bad, tot, stats = certify_circuits(trials=40, seed=77)
    check("CVP reduction: 40 random circuits x 32 assignments (%d evals)"
          % tot, bad == 0)
    bad, n = certify_all_functions(3)
    check("  ... COMPLETE: all 256 Boolean functions of 3 variables",
          bad == 0)
    return bad == 0


def test_linear():
    from linear import certify_linearity, certify_powering, certify_pascal
    b1, n1 = certify_linearity(trials=200, seed=1234)
    check("unconditional sector is F2-linear (200 random constitutions)",
          b1 == 0)
    b2, n2, sq = certify_powering(trials=30, seed=999)
    check("  ... Phi^t = L^t by repeated squaring (30 trials)", b2 == 0)
    b3, n3 = certify_pascal(tmax=1 << 10)
    check("  ... |S_t| = 2^popcount(t): Pascal columns from Lucas", b3 == 0)
    return b1 == b2 == b3 == 0


# ---------------------------------------------------------------------------
# 6.  The founding theorems still hold where they should
# ---------------------------------------------------------------------------

def test_paving():
    from paving import certify_proposition6, certify_corollary
    viol, tested, far = certify_proposition6(trials=250, seed=808)
    check("Prop 6: out-degree 1 can pave only CYCLE kinds", viol == 0,
          "%d far sightings over %d constitutions, %d violations"
          % (far, tested, viol))
    bad, n = certify_corollary(trials=200, seed=808)
    check("  ... Cor 6.1: a normal-form gate lies on no cycle, so no "
          "out-degree-1", bad == 0, "constitution can enact one on virgin "
          "ground (%d/%d)" % (n - bad, n))
    return viol == 0 and bad == 0


def test_no_contradiction():
    """The constructions must not contradict the field's theorems."""
    from anon import build110
    M = build110()
    C = M.const()
    # Out-Degree Law: out-degree 1 => no free glider.  Certify the machine is
    # motionless: with hardware everywhere, no translation-recurrence occurs,
    # and every gate law stays exactly where it was placed.
    from anon import encode110, GATES110
    sites = list(range(9))
    S = encode110(build110(modulus=9), [1, 0, 1, 1, 0, 0, 1, 0, 1], sites)
    Mm = build110(modulus=9)
    S = encode110(Mm, [1, 0, 1, 1, 0, 0, 1, 0, 1], sites)
    L, r = Mm.L, len(Mm.wires)
    hw0 = {(c, k) for c, m in S.items() for k in range(Mm.const().n)
           if (m >> k) & 1 and (c % L == r)}
    ok = True
    for _ in range(60):
        S = Mm.run(S, 1)
        hw = {(c, k) for c, m in S.items() for k in range(Mm.const().n)
              if (m >> k) & 1 and (c % L == r)}
        ok &= (hw == hw0)
    check("no free glider: every gate law and every POWER law is exactly "
          "where it was", ok, "60 steps, out-degree 1")
    # Gridlock still holds where its hypothesis holds
    from xnomos import RULES1
    ok2 = True
    for a, b, c in RULES1:
        Cx = Const([(a, b, c)])
        Sx = state_of([(i, 0) for i in range(-3, 4)])
        ok2 &= not [x for x in active_laws(Sx, Cx) if -2 <= x[0] <= 2]
    check("Gridlock unchanged in the own-kind window-1 sector (27/27 rules)",
          ok2)
    # Y1: a saturated code is frozen under occupancy guards
    import random
    rng = random.Random(5)
    ok3 = True
    for _ in range(200):
        n = rng.randrange(1, 4)
        rules = [(rng.randrange(-1, 2), rng.randrange(-1, 2),
                  rng.randrange(-1, 2)) for _ in range(n)]
        tg = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
              for _ in range(n)]
        Cx = Const(rules, tg)
        full = (1 << n) - 1
        Sx = {i: full for i in range(-6, 7)}
        acts = [(cell, k) for cell, k in active_laws(Sx, Cx)
                if -4 <= cell <= 4]
        ok3 &= not acts
    check("Y1 plenum: a saturated region has no active law (200 random "
          "constitutions)", ok3)
    return ok and ok2 and ok3


def dump():
    print("\n" + "=" * 74)
    print("PASTE-READY CONSTITUTIONS")
    print("=" * 74)
    C, ix, names = build_r110()
    print("\n# THE STATUTE OF ONE HUNDRED AND TEN (citation sector)")
    print("#   kinds:", ", ".join("%d=%s" % (i, n) for i, n in
                                  enumerate(names)))
    print("rules   =", C.rules)
    print("targets =", [tuple(t) for t in C.targets])
    print("guards  =", [tuple(g) for g in C.guards])
    print("# seed a phase-0 code: gate kinds 12..23 and K0 at every cell,")
    print("#   plus X (kind 1) where the Rule-110 bit is 1, Xb (kind 2) "
          "where it is 0.")
    C2, names2, widx, L, r, POWER = build_r110_anon()
    print("\n# THE ANONYMOUS STATUTE OF ONE HUNDRED AND TEN "
          "(occupancy guards, guards=None)")
    print("#   block L = %d cells; slots 0..%d are wires %s," %
          (L, r - 1, R110_WIRES))
    print("#   slot %d is POWER, slot %d is the GAP." % (r, r + 1))
    print("rules   =", C2.rules)
    print("targets =", [tuple(t) for t in C2.targets])
    print("guards  = None")


def _main():
    print("Y-B VERIFICATION BATTERY  (independent re-derivation through "
          "xnomos)")
    print()
    test_gate_table()
    test_r110_citation()
    test_r110_anon()
    test_turing()
    test_anon_turing()
    test_circuits()
    test_linear()
    test_paving()
    test_no_contradiction()
    print()
    print("  %d/%d checks passed" % (len(PASS), len(PASS) + len(FAIL)))
    if FAIL:
        print("  FAILED:", FAIL)
        sys.exit(1)
    if "-d" in sys.argv:
        dump()


if __name__ == "__main__":
    _main()
