#!/usr/bin/env python3
"""
circuit.py — an arbitrary Boolean circuit as a constitution, and the
P-completeness of nomodynamic prediction.

THE PREDICTION PROBLEM.
    PREDICT :  given a constitution C, a finite code S0, a step count t in
               unary, a cell j and a kind k, decide whether a law of kind k
               stands at j at time t.

Upper bound: one step costs O(|S| . n) and |S| grows by at most n per cell of
frontier, so t steps cost poly(|C| + |S0| + t).  PREDICT is in P.

Lower bound (this file): the CIRCUIT VALUE PROBLEM reduces to PREDICT in
log space.  A citation constitution can hold one WIRE KIND per circuit wire and
one GATE KIND per circuit gate, and put every gate law in a SINGLE CELL — a
statute book of one cell that computes.  Kinds are the wires; no routing, no
geometry, no window at all (every offset is 0).  The transcription is a direct
syntactic copy of the circuit, so it is computable in log space.

    THEOREM 2.  PREDICT is P-complete under log-space reductions, already for
    dim = 1, window 0, parity resolution, and codes supported on ONE CELL.

For a *fixed* constitution the same conclusion follows from turing.py: the
Generic Machine Simulation Problem is P-complete, and N(U) simulates the
universal machine U with time dilation 3 and a log-space-computable code.

Run `python3 circuit.py`.
"""

from __future__ import annotations

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from statute import Machine, NIL                                  # noqa: E402


# --------------------------------------------------------------------- circuits
# A circuit is a list of ("op", out, in1, in2) in topological order, with
# op in {AND, OR, XOR, NOT, NAND, NOR, XNOR, ANDNOT, BUF}, plus a list of
# input wire names.


OPS = {
    "AND":    lambda a, b: a & b,
    "OR":     lambda a, b: a | b,
    "XOR":    lambda a, b: a ^ b,
    "NAND":   lambda a, b: 1 - (a & b),
    "NOR":    lambda a, b: 1 - (a | b),
    "XNOR":   lambda a, b: 1 - (a ^ b),
    "ANDNOT": lambda a, b: a & (1 - b),
    "NOT":    lambda a, b: 1 - a,
    "BUF":    lambda a, b: a,
}


def eval_circuit(inputs, gates, values):
    """Reference evaluator."""
    v = dict(values)
    for op, out, i1, i2 in gates:
        v[out] = OPS[op](v[i1], v.get(i2, 0))
    return v


def levels(inputs, gates):
    """Longest-path level of every wire; inputs are level 0."""
    lv = {w: 0 for w in inputs}
    for op, out, i1, i2 in gates:
        d = lv[i1] if op in ("NOT", "BUF") else max(lv[i1], lv[i2])
        lv[out] = d + 1
    return lv


# --------------------------------------------------------------------- compiler


def compile_circuit(inputs, gates):
    """One wire kind per wire, one-or-more gate kinds per gate, all at cell 0.

    Every gate is expanded into AND-NOT / XOR / constant pieces.  Levels are
    equalised with BUF chains so that all inputs of a gate arrive together;
    the depth of the resulting statute machine is `depth` micro-steps.
    """
    lv = levels(inputs, gates)
    # each op costs `cost` micro-steps
    cost = {"AND": 2, "NAND": 2, "OR": 2, "NOR": 2, "XOR": 1, "XNOR": 1,
            "ANDNOT": 1, "NOT": 1, "BUF": 1}
    # recompute levels with real costs, and insert delay buffers
    depth = {w: 0 for w in inputs}
    for op, out, i1, i2 in gates:
        d = depth[i1] if op in ("NOT", "BUF") else max(depth[i1], depth[i2])
        depth[out] = d + cost[op]

    M = Machine(dim=1)
    for w in inputs:
        M.wire(w)
    for op, out, i1, i2 in gates:
        M.wire(out)
    # sources hold the inputs forever
    for w in inputs:
        M.gate("src_" + w, "src_" + w, 0, NIL, 0, 0, [w])
    # delay lines: wire w must still be readable at time depth[out]-cost
    delay = {}

    def at(w, t):
        """A wire carrying the value of w at micro-time t (delay line if needed)."""
        assert t >= depth[w], (w, t, depth[w])
        cur = w
        for s in range(depth[w], t):
            nxt = delay.get((w, s + 1))
            if nxt is None:
                nxt = "%s@%d" % (w, s + 1)
                M.wire(nxt)
                M.gate("d_" + nxt, cur, 0, NIL, 0, 0, [nxt])
                depth[nxt] = s + 1
                delay[(w, s + 1)] = nxt
            cur = nxt
        return cur

    for gi, (op, out, i1, i2) in enumerate(gates):
        d = depth[out] - cost[op]                 # when both inputs are ready
        g = "g%d:" % gi
        if op == "BUF":
            M.gate(g, at(i1, d), 0, NIL, 0, 0, [out])
        elif op == "NOT":
            M.gate(g, g, 0, at(i1, d), 0, 0, [out])
        elif op == "ANDNOT":
            M.gate(g, at(i1, d), 0, at(i2, d), 0, 0, [out])
        elif op in ("XOR", "XNOR"):
            M.gate(g + "u", at(i1, d), 0, NIL, 0, 0, [out])
            M.gate(g + "v", at(i2, d), 0, NIL, 0, 0, [out])
            if op == "XNOR":
                M.gate(g + "1", g + "1", 0, NIL, 0, 0, [out])
        elif op in ("AND", "NAND"):
            nb = g + "nb"
            M.wire(nb)
            depth[nb] = d + 1
            M.gate(g + "n", g + "n", 0, at(i2, d), 0, 0, [nb])       # ~b
            M.gate(g, at(i1, d + 1), 0, nb, 0, 0, [out])             # a & b
            if op == "NAND":
                M.gate(g + "1", g + "1", 0, NIL, 0, 0, [out])
        elif op in ("OR", "NOR"):
            na = g + "na"
            M.wire(na)
            depth[na] = d + 1
            M.gate(g + "n", g + "n", 0, at(i1, d), 0, 0, [na])       # ~a
            M.gate(g, na, 0, at(i2, d + 1), 0, 0, [out])             # ~a & ~b
            if op == "OR":
                M.gate(g + "1", g + "1", 0, NIL, 0, 0, [out])
        else:
            raise ValueError(op)
    return M, depth


def run_compiled(M, depth, inputs, values, out_wire):
    pl = [(0, g) for g in M.gates
          if not (g.startswith("src_") and not values.get(g[4:], 0))]
    pl += [(0, w) for w in inputs if values.get(w, 0)]
    S = M.code(pl)
    S = M.run(S, depth[out_wire])
    return M.read(S, 0, out_wire)


# --------------------------------------------------------------------- testing


def random_circuit(rng, n_in=5, n_gates=25):
    inputs = ["x%d" % i for i in range(n_in)]
    pool = list(inputs)
    gates = []
    for i in range(n_gates):
        op = rng.choice(list(OPS))
        out = "w%d" % i
        i1 = rng.choice(pool)
        i2 = rng.choice(pool)
        gates.append((op, out, i1, i2))
        pool.append(out)
    return inputs, gates


def certify_circuits(trials=120, seed=2, n_in=5, n_gates=22, verbose=False):
    rng = random.Random(seed)
    bad = 0
    tot = 0
    stats = []
    for _ in range(trials):
        inputs, gates = random_circuit(rng, n_in, n_gates)
        M, depth = compile_circuit(inputs, gates)
        assert not M.check_normal_form(), M.check_normal_form()
        out = gates[-1][1]
        stats.append((len(M.names), depth[out]))
        for code in range(1 << n_in):
            vals = {w: (code >> i) & 1 for i, w in enumerate(inputs)}
            want = eval_circuit(inputs, gates, vals)[out]
            got = run_compiled(M, depth, inputs, vals, out)
            tot += 1
            if got != want:
                bad += 1
                if verbose:
                    print("  MISMATCH", vals, got, want)
    return bad, tot, stats


def certify_all_functions(k=3):
    """COMPLETE: every one of the 2^(2^k) Boolean functions of k variables,
    compiled from its DNF and checked on all 2^k inputs."""
    inputs = ["x%d" % i for i in range(k)]
    bad = 0
    for f in range(1 << (1 << k)):
        # DNF over the minterms of f
        gates = []
        n = 0
        acc = None
        for m in range(1 << k):
            if not (f >> m) & 1:
                continue
            term = None
            for i in range(k):
                lit = inputs[i]
                if not (m >> i) & 1:
                    gates.append(("NOT", "n%d_%d" % (m, i), lit, lit))
                    lit = "n%d_%d" % (m, i)
                if term is None:
                    gates.append(("BUF", "t%d_%d" % (m, i), lit, lit))
                else:
                    gates.append(("AND", "t%d_%d" % (m, i), term, lit))
                term = "t%d_%d" % (m, i)
            if acc is None:
                gates.append(("BUF", "a%d" % n, term, term))
            else:
                gates.append(("OR", "a%d" % n, acc, term))
            acc = "a%d" % n
            n += 1
        if acc is None:                       # the constant 0
            gates.append(("ANDNOT", "a0", inputs[0], inputs[0]))
            acc = "a0"
        M, depth = compile_circuit(inputs, gates)
        for code in range(1 << k):
            vals = {w: (code >> i) & 1 for i, w in enumerate(inputs)}
            want = (f >> code) & 1
            got = run_compiled(M, depth, inputs, vals, acc)
            if got != want:
                bad += 1
    return bad, 1 << (1 << k)


def _main():
    print("CIRCUITS AS CONSTITUTIONS  (dim 1, window 0, ONE CELL, parity)")
    bad, tot, stats = certify_circuits()
    ks = [s[0] for s in stats]
    ds = [s[1] for s in stats]
    print("  120 random circuits (5 inputs, 22 gates) x all 32 input "
          "assignments")
    print("     = %d evaluations, %d mismatches;  kinds %d..%d, depth %d..%d"
          % (tot, bad, min(ks), max(ks), min(ds), max(ds)))
    assert bad == 0
    bad, n = certify_all_functions(3)
    print("  COMPLETE: all %d Boolean functions of 3 variables, compiled from "
          "DNF" % n)
    print("     and checked on all 8 inputs -> %d mismatches" % bad)
    assert bad == 0
    bad, n = certify_all_functions(2)
    print("  COMPLETE: all %d Boolean functions of 2 variables -> %d mismatches"
          % (n, bad))
    assert bad == 0
    # the window-0 claim
    inputs, gates = random_circuit(random.Random(1))
    M, depth = compile_circuit(inputs, gates)
    C = M.const()
    assert all(all(x == 0 for x in r) for r in C.rules)
    print("  every offset of every compiled constitution is 0: the whole "
          "computation")
    print("     happens inside a SINGLE CELL — kinds are the wires.")
    print("circuit self-tests passed")


if __name__ == "__main__":
    _main()
