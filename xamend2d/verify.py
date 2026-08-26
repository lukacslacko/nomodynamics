#!/usr/bin/env python3
"""verify.py — the verification battery.

Every positive claim of Expedition X-B is re-checked here by an INDEPENDENT
code path: /Users/lukacs/claude/math/program/phase6/xnomos.py, the shared
reference engine written by a different expedition.  The C census engine and
xa2d.py are never trusted for a positive claim.

Certificates issued:
  GLIDER    Phi^p(S) = sigma^d(S) re-verified over >= 3 (default 5) periods
  CYCLE     Phi^p(S) = S and Phi^q(S) != S for 0 < q < p
  BALANCED  Phi(S) = S and the active-law set is nonempty
  GROWTH    |S_t| matches a claimed closed form for all t <= T
"""
import sys

sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6")
import xnomos                                                   # noqa: E402

from xa2d import Const                                          # noqa: E402

# the six canonical census seeds (index -> list of (x,y,kind))
SEED = {
    0: [(0, 0, 0)],
    1: [(0, 0, 0), (0, 0, 1)],
    2: [(0, 0, 0), (1, 0, 1)],
    3: [(0, 0, 0), (0, 1, 1)],
    4: [(0, 0, 0), (1, 1, 1)],
    5: [(0, 0, 0), (1, 0, 0), (0, 1, 1)],
}


def xn(label):
    """xnomos Const from the compact label, e.g. 'OEO>AB OEE>AB'."""
    C = Const.parse(label)
    return xnomos.Const(C.rules,
                        [t if len(t) > 1 else t[0] for t in C.targets], dim=2)


def st(seed):
    return xnomos.state_of([((x, y), k) for (x, y, k) in seed])


def core(label, seed, mode="parity", maxt=1200):
    """Evolve to the periodic core; return (S_{t0}, t0, period, displacement)."""
    X, S = xn(label), st(seed)
    seen = {}
    for t in range(maxt):
        n, a = _norm(S)
        if n in seen:
            t0, a0 = seen[n]
            return S, t0, t - t0, (a[0] - a0[0], a[1] - a0[1])
        seen[n] = (t, a)
        S = xnomos.step(S, X, mode)
    return None, None, None, None


def cert_glider(label, seed, p, d, mode="parity", reps=5):
    X, _ = xn(label), None
    S0, t0, pp, dd = core(label, seed, mode)
    if S0 is None:
        return False, "no recurrence found"
    if (pp, dd) != (p, tuple(d)):
        return False, "core is p=%s d=%s, not p=%s d=%s" % (pp, dd, p, d)
    S = dict(S0)
    for r in range(1, reps + 1):
        for _ in range(p):
            S = xnomos.step(S, X, mode)
        want = {(c[0] + d[0] * r, c[1] + d[1] * r): m for c, m in S0.items()}
        if S != want:
            return False, "failed at rep %d" % r
    # also confirm it is not a shorter-period glider
    for q in range(1, p):
        S = dict(S0)
        for _ in range(q):
            S = xnomos.step(S, X, mode)
        if _norm(S0)[0] == _norm(S)[0]:
            return False, "shorter period %d" % q
    return True, ("Phi^%d = sigma^%s over %d periods (core at t0=%d, card %d)"
                  % (p, d, reps, t0, xnomos.card(S0)))


def _norm(S):
    if not S:
        return (), (0, 0)
    lo = (min(c[0] for c in S), min(c[1] for c in S))
    return (tuple(sorted(((c[0] - lo[0], c[1] - lo[1]), m)
                         for c, m in S.items())), lo)


def cert_cycle(label, seed, p, mode="parity", reps=3):
    X = xn(label)
    S0, t0, pp, dd = core(label, seed, mode)
    if S0 is None:
        return False, "no recurrence found"
    if dd != (0, 0):
        return False, "core drifts by %s (glider, not cycle)" % (dd,)
    if pp != p:
        return False, "core period is %s, not %s" % (pp, p)
    S = base = dict(S0)
    for q in range(1, p * reps + 1):
        S = xnomos.step(S, X, mode)
        if S == base and q % p:
            return False, "shorter period %d" % q
    if S != base:
        return False, "not periodic with p=%d" % p
    return True, ("Phi^%d(S_%d) = S_%d over %d periods (card %d)"
                  % (p, t0, t0, reps, xnomos.card(S0)))


def cert_balanced(label, seed, mode="parity"):
    X, S0 = xn(label), st(seed)
    if xnomos.step(S0, X, mode) != S0:
        return False, "not fixed"
    act = xnomos.active_laws(S0, X)
    if not act:
        return False, "no active law (plain gridlock, not balance)"
    return True, "fixed with %d active laws (card %d)" % (len(act),
                                                          xnomos.card(S0))


def cert_growth(label, seed, formula, T=200, mode="parity"):
    X, S = xn(label), st(seed)
    for t in range(T + 1):
        if xnomos.card(S) != formula(t):
            return False, "card mismatch at t=%d: %d vs %d" % (
                t, xnomos.card(S), formula(t))
        S = xnomos.step(S, X, mode)
    return True, "|S_t| = formula for t = 0..%d" % T


BATTERY = []


def add(name, fn, *a, **k):
    BATTERY.append((name, fn, a, k))


# ---- gliders -------------------------------------------------------------
add("G1 Writ of Removal (E)", cert_glider, "OEO>AB OEE>AB", SEED[1], 1, (1, 0))
add("G1' Writ of Removal (OR)", cert_glider, "OEO>AB OEE>AB", SEED[1], 1,
    (1, 0), "or")
add("G2 diagonal Writ (NE)", cert_glider, "OEO>AB OEP>AB", SEED[1], 1, (1, 1))
add("G2' diagonal Writ (NW)", cert_glider, "OEO>AB OEQ>AB", SEED[1], 1, (-1, 1))
add("G3 4-law glider", cert_glider, "OEE>AB EWO>AB",
    [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0, 1)], 1, (1, 0))
add("G4 p=4 card-7 glider", cert_glider, "OQW>B ORE>AB", SEED[4], 4, (4, 0))
add("G4' p=4 card-7 mirror", cert_glider, "ORS>B OQN>AB", SEED[4], 4, (0, 4))

# ---- non-2-adic clocks ---------------------------------------------------
add("C1 own-kind period 3", cert_cycle, "EQN>A TQS>B", SEED[4], 3)
add("C2 reciprocal period 3", cert_cycle, "OPE>B OSQ>A", SEED[0], 3)
add("C3 period 5", cert_cycle, "EWP>AB SWT>AB", SEED[5], 5)
add("C4 period 7", cert_cycle, "ORP>B WES>B", SEED[5], 7)
add("C5 period 192", cert_cycle, "OQP>B RTW>AB", SEED[5], 192)
add("C6 period 112 (card 111)", cert_cycle, "NTR>AB SPN>AB", SEED[5], 112)

# ---- balance -------------------------------------------------------------
add("B1 two-chamber (2 laws)", cert_balanced, "OSS>A OES>A",
    [(0, 0, 0), (0, 0, 1)])

# ---- area-filling growth -------------------------------------------------
add("A1 the Sower", cert_growth, "OEE>AB ONN>B", SEED[0],
    lambda t: (t + 1) * (t + 2) // 2, 200)


def main():
    ok = 0
    for name, fn, a, k in BATTERY:
        good, msg = fn(*a, **k)
        print("[%s] %-30s %s" % ("PASS" if good else "FAIL", name, msg))
        ok += good
    print("\nverification battery: %d/%d PASS (independent engine: xnomos.py)"
          % (ok, len(BATTERY)))
    return 0 if ok == len(BATTERY) else 1


if __name__ == "__main__":
    sys.exit(main())
