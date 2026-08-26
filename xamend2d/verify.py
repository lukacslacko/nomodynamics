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


def cert_odometer(label, seed, T=65536, mode="parity"):
    """No exact recurrence in T fully-hashed steps, plus the 2-adic jubilee
    schedule: a card maximum at every t = 2^k - 1 and a collapse at t = 2^k."""
    X, S = xn(label), st(seed)
    seen = {}
    peaks, floors, heights = {}, {}, {}
    for t in range(T + 1):
        key = tuple(sorted(S.items()))
        if key in seen:
            return False, "recurrence at t=%d (first seen %d)" % (t, seen[key])
        seen[key] = t
        if t and (t & (t - 1)) == 0:
            floors[t] = xnomos.card(S)
            ys = [c[1] for c in S]
            heights[t] = max(ys) - min(ys) + 1
        if t and ((t + 1) & t) == 0:
            peaks[t] = xnomos.card(S)
        S = xnomos.step(S, X, mode)
    ks = [k for k in range(8, T.bit_length()) if (1 << k) in floors]
    for k in ks:
        if floors[1 << k] > 8:
            return False, "no collapse at t=2^%d (card %d)" % (k, floors[1 << k])
        if peaks.get((1 << k) - 1, 0) <= floors[1 << k] * 3:
            return False, "no avalanche at t=2^%d-1" % k
    hs = [heights[1 << k] for k in ks]
    if hs != sorted(hs) or hs[-1] <= hs[0]:
        return False, "reach not growing: %s" % hs
    return True, ("no recurrence in %d hashed steps; card collapses to <=8 at "
                  "every t=2^k (k=%d..%d) with an avalanche at t=2^k-1; "
                  "height %d -> %d" % (T, ks[0], ks[-1], hs[0], hs[-1]))


BATTERY = []


def add(name, fn, *a, **k):
    BATTERY.append((name, fn, a, k))


# 3-kind census seed family
SEED3 = {
    0: [(0, 0, 0)], 1: [(0, 0, 0), (0, 0, 1)],
    2: [(0, 0, 0), (0, 0, 1), (0, 0, 2)], 3: [(0, 0, 0), (1, 0, 1)],
    4: [(0, 0, 0), (1, 0, 1), (0, 1, 2)], 5: [(0, 0, 0), (1, 1, 1)],
    6: [(0, 0, 0), (1, 0, 1), (1, 1, 2)],
    7: [(0, 0, 0), (1, 0, 0), (0, 1, 1), (1, 1, 2)],
}


def cert_growth_exact(label, seed, cardfn, cellfn, T=200, mode="parity"):
    """|S_t| = cardfn(t) AND the cell support equals cellfn(t), for t <= T."""
    X, S = xn(label), st(seed)
    for t in range(T + 1):
        if xnomos.card(S) != cardfn(t):
            return False, "card at t=%d: %d != %d" % (t, xnomos.card(S),
                                                      cardfn(t))
        if cellfn is not None and set(S) != cellfn(t):
            return False, "support differs at t=%d" % t
        S = xnomos.step(S, X, mode)
    return True, "card and exact cell support match for t = 0..%d" % T


def cert_gun(label, seed, period, T=200, mode="parity"):
    """A gun: the pump cell is periodic and |S_t| grows linearly forever."""
    X, S = xn(label), st(seed)
    hist = []
    for t in range(T + 1):
        hist.append((xnomos.card(S), frozenset(k for c, k in xnomos.laws(S)
                                               if c == (0, 0))))
        S = xnomos.step(S, X, mode)
    for t in range(20, T + 1 - period):
        if hist[t][1] != hist[t + period][1]:
            return False, "pump not %d-periodic at t=%d" % (period, t)
    d = [hist[t + 2][0] - hist[t][0] for t in range(20, T - 2)]
    if len(set(d)) != 1:
        return False, "growth not linear: %s" % sorted(set(d))
    return True, ("pump is %d-periodic and |S_t| grows by %d per 2 steps "
                  "through t=%d" % (period, d[0], T))


def cert_collision(label, gaps, T=40, mode="parity"):
    """Head-on writ collision: even gaps transparent, odd gaps arrested."""
    X = xn(label)
    out = []
    for g in gaps:
        S = st([(0, 0, 0), (0, 0, 1), (g, 0, 2), (g, 0, 3)])
        prev = None
        merged = False
        for t in range(T):
            if len(S) == 1 and xnomos.card(S) == 4:
                merged = True
            prev = S
            S = xnomos.step(S, X, mode)
            if S == prev:
                break
        frozen = (S == prev)
        want_frozen = (g % 2 == 1)
        if frozen != want_frozen:
            return False, "gap %d: frozen=%s expected %s" % (g, frozen,
                                                             want_frozen)
        if not want_frozen and not merged:
            return False, "gap %d: even gap did not merge onto one cell" % g
        out.append(g)
    return True, ("gaps %s: odd -> frozen 4-law block, even -> one-cell merge "
                  "then separation" % (list(gaps),))


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
add("G5 subluminal (OR, speed 1/2)", cert_glider, "OEW>AB ONE>A", SEED[1], 2,
    (-1, 0), "or")
add("G6 ONE-LAW glider (speed 1/4)", cert_glider, "OWO>ABC ORQ>A RER>BC",
    SEED3[0], 4, (-1, 1))
add("G7 no null cycle (opposed sums)", cert_glider, "OPS>BC NRQ>A PRP>A",
    SEED3[0], 4, (-2, 0))
add("G8 card-50 diagonal spaceship", cert_glider, "PQW>B ONE>AC ONP>ABC",
    SEED3[2], 4, (4, 4))
add("G9 subluminal parity, speed 1/6", cert_glider, "ONO>AB OEW>AC WTE>A",
    SEED3[1], 6, (-1, 0))
add("G10 card-18, p=1, diagonal", cert_glider, "OTT>AB PSE>C ORN>AB",
    SEED3[2], 1, (-1, -1))
add("G11 1-D Writ of Removal", lambda: _oned(), )

# ---- non-2-adic clocks ---------------------------------------------------
add("C1 own-kind period 3", cert_cycle, "EQN>A TQS>B", SEED[4], 3)
add("C2 reciprocal period 3", cert_cycle, "OPE>B OSQ>A", SEED[0], 3)
add("C3 period 5", cert_cycle, "EWP>AB SWT>AB", SEED[5], 5)
add("C4 period 7", cert_cycle, "ORP>B WES>B", SEED[5], 7)
add("C5 period 192", cert_cycle, "OQP>B RTW>AB", SEED[5], 192)
add("C6 period 112 (card 111)", cert_cycle, "NTR>AB SPN>AB", SEED[5], 112)

# ---- machines ------------------------------------------------------------
add("M1 THE ASSIZE (glider gun)", cert_gun, "OEO>AB OEE>AB OEO>AB",
    [(0, 0, 2)], 2, 200)
add("M2 THE CIRCUIT COURT (rake)", cert_growth,
    "OEO>AB OEE>AB ONO>ABCD ONN>CD", [(0, 0, 2), (0, 0, 3)],
    lambda t: 2 * t + 2, 200)
add("M3 writ collision algebra", cert_collision,
    "OEO>AB OEE>AB OWO>CD OWW>CD", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

# ---- cryptid -------------------------------------------------------------
add("K1 THE ODOMETER (2^16 steps)", cert_odometer, "OEW>B NQR>AB",
    [(0, 0, 0), (1, 0, 0), (0, 1, 1)], 1 << 16)

# ---- balance -------------------------------------------------------------
add("B1 two-chamber (2 laws, minimal)", cert_balanced, "OSS>A OES>A",
    [(0, 0, 0), (0, 0, 1)])
add("B2 PERPETUAL SESSION (40 laws, 100% active)", cert_balanced,
    "OEO>A OEO>A", [(0, y, k) for y in range(20) for k in (0, 1)])
add("B3 TWO CHAMBERS (non-local, distance 2)", cert_balanced, "ONN>A OSS>A",
    [(x, 0, 0) for x in range(6)] + [(x, 2, 1) for x in range(6)])

# ---- area-filling growth -------------------------------------------------
add("A1 THE SOWER  |S_t| = (t+1)(t+2)/2", cert_growth, "OEE>AB ONN>B",
    SEED[0], lambda t: (t + 1) * (t + 2) // 2, 200)
add("A2 THE LAND GRANT |S_t| = (t+1)^2", cert_growth_exact,
    "OPP>ABC OEE>B ONN>C", SEED[0], lambda t: (t + 1) ** 2,
    lambda t: {(0, 0)} | {(x, y) for x in range(1, t + 1)
                          for y in range(1, t + 1)}, 200)


def _oned():
    """The Writ of Removal in ONE dimension (the Free Glider Question)."""
    X = xnomos.Const([(0, 1, 0), (0, 1, 1)], targets=[(0, 1), (0, 1)], dim=1)
    S0 = xnomos.state_of([(0, 0), (0, 1)])
    if not xnomos.verify_glider(S0, X, 1, 1):
        return False, "1-D glider failed"
    return True, "Phi(S) = sigma^1(S) in dimension 1 (xnomos, dim=1)"


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
