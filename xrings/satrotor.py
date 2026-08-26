#!/usr/bin/env python3
"""
satrotor.py — DECIDE (not sample) the existence of ring rotors, by SAT.

For a fixed constitution, ring size m, rotation r and period p, the statement

    exists X != 0 :  Phi^p(X) = rot_r(X)  and  rot_r(X) != X

is a propositional formula in p*n*m variables with only local clauses, so z3
settles it in milliseconds — for ring sizes far beyond any enumeration.  Note
that such an X is automatically recurrent (Phi^{p*ord(r)}(X) = X), so this
decides rotor existence exactly.

  python3 satrotor.py odd      # the odd-ring question, complete for the stated
                               # scope: UNSAT everywhere is a theorem for that
                               # scope, not a sample
  python3 satrotor.py control  # the same procedure on even rings (sanity)
"""
import itertools
import sys
import time

from z3 import Bool, Solver, Xor, Or, And, Not, unsat, sat

OFF = (-1, 0, 1)
RULES27 = [(a, b, c) for a in OFF for b in OFF for c in OFF]
RULES12 = [r for r in RULES27 if r[1] != 0 and r[0] != r[1]]


def xor_list(ls):
    if not ls:
        return False
    v = ls[0]
    for z in ls[1:]:
        v = Xor(v, z)
    return v


def build(s, rules, targets, mode, m, p, tag):
    n = len(rules)
    X = [[[Bool("%s_%d_%d_%d" % (tag, t, k, i)) for i in range(m)]
          for k in range(n)] for t in range(p + 1)]
    for t in range(p):
        cur, nxt = X[t], X[t + 1]
        occ = [Or([cur[k][i] for k in range(n)]) for i in range(m)]
        act = [[And(cur[k][i], occ[(i + rules[k][0]) % m],
                    Not(occ[(i + rules[k][1]) % m])) for i in range(m)]
               for k in range(n)]
        emit = [[act[k][(j - rules[k][2]) % m] for j in range(m)]
                for k in range(n)]
        if mode in ("parity", "or"):
            for tt in range(n):
                src = [k for k in range(n) if targets[k] == tt]
                for j in range(m):
                    e = (xor_list([emit[k][j] for k in src]) if mode == "parity"
                         else Or([emit[k][j] for k in src]) if src else False)
                    s.add(nxt[tt][j] == Xor(cur[tt][j], e))
        else:
            for j in range(m):
                allе = [emit[k][j] for k in range(n)]
                votes = (xor_list(allе) if mode == "super" else Or(allе))
                cleared = And(votes, occ[j])
                for k in range(n):
                    s.add(nxt[k][j] == Or(And(cur[k][j], Not(cleared)),
                                          And(emit[k][j], Not(occ[j]))))
    return X


def has_rotor(rules, targets, mode, m, p, r=None, timeout_ms=60000):
    """r=None: let the SOLVER choose the rotation (one call covers all r)."""
    s = Solver()
    s.set("timeout", timeout_ms)
    n = len(rules)
    X = build(s, rules, targets, mode, m, p, "a")
    rs = [r] if r is not None else list(range(1, m))
    sel = [Bool("sel_%d" % rr) for rr in rs]
    s.add(Or(sel))
    for si, rr in zip(sel, rs):
        cond = [X[p][k][i] == X[0][k][(i - rr) % m]          # Phi^p = rot_rr
                for k in range(n) for i in range(m)]
        cond.append(Or([X[0][k][i] != X[0][k][(i - rr) % m]  # genuinely moves
                        for k in range(n) for i in range(m)]))
        s.add(Or(Not(si), And(cond)))
    s.add(Or([X[0][k][i] for k in range(n) for i in range(m)]))  # nonempty
    res = s.check()
    if res == sat:
        mdl = s.model()
        rr = next(rs[i] for i in range(len(rs))
                  if mdl.evaluate(sel[i], model_completion=True))
        return (rr, [[1 if mdl.evaluate(X[0][k][i], model_completion=True)
                      else 0 for i in range(m)] for k in range(n)])
    if res == unsat:
        return None
    return "TIMEOUT"


def campaign(ms, n, pmax, pool, modes, tmaps, tag, shard=0, nshard=1):
    t0 = time.time()
    calls = 0
    hits = []
    todo = list(itertools.product(pool, repeat=n))
    todo = todo[shard::nshard]
    for rules in todo:
        for targets in tmaps:
            for mode in modes:
                if mode in ("super", "super_or") and targets != tmaps[0]:
                    continue                        # targets ignored there
                for m in ms:
                    for p in range(1, pmax + 1):
                        calls += 1
                        w = has_rotor(list(rules), list(targets), mode, m, p)
                        if w == "TIMEOUT":
                            print("  TIMEOUT %s %s %s m=%d p=%d"
                                  % (rules, targets, mode, m, p), flush=True)
                            hits.append(("TIMEOUT",))
                        elif w is not None:
                            hits.append((rules, targets, mode, m, p, w))
                            print("  ROTOR: %s %s %s m=%d p=%d r=%d X=%s"
                                  % (rules, targets, mode, m, p, w[0], w[1]),
                                  flush=True)
    print("  [%s shard %d/%d] %d SAT calls, %d rotors, %.1f s"
          % (tag, shard, nshard, calls, len(hits), time.time() - t0),
          flush=True)
    return calls, hits


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "odd1"
    shard = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    nshard = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    ODD = lambda hi: list(range(3, hi + 1, 2))       # noqa: E731
    EVEN = lambda hi: list(range(4, hi + 1, 2))      # noqa: E731
    jobs = {
        "control": (EVEN(10), 1, 3, RULES27, ["parity"], [(0,)], "even 1-kind"),
        "odd1": (ODD(31), 1, 6, RULES27, ["parity", "super"], [(0,)],
                 "1 kind, all 27 rules, odd m<=31, p<=6"),
        "odd2": (ODD(17), 2, 3, RULES12,
                 ["parity", "super", "or", "super_or"],
                 [(1, 0), (0, 1), (0, 0)], "2 live kinds, odd m<=17, p<=3"),
        "odd3": (ODD(13), 3, 2, RULES12, ["parity"],
                 [(1, 2, 0), (0, 1, 2), (0, 0, 0)],
                 "3 live kinds, odd m<=13, p<=2"),
        "even2": (EVEN(12), 2, 3, RULES12, ["parity"], [(1, 0)],
                  "CONTROL 2 live kinds even m<=12"),
    }
    ms, n, pmax, pool, modes, tmaps, tag = jobs[what]
    print("== %s ==" % tag, flush=True)
    campaign(ms, n, pmax, pool, modes, tmaps, tag, shard, nshard)


if __name__ == "__main__":
    main()
