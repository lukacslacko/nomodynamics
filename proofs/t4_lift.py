#!/usr/bin/env python3
"""
t4_lift.py -- TARGET 4 (b): the Wrapping Lemma and the Lift Theorem, with
machine checks; the O-15 certificate; and the dense (gap-free) counterexample
that shows the vacancy hypothesis cannot be dropped.

  Lemma W (wrapping).   C window-W, any local resolution.  T a finite code on Z
    with supp(T) inside an interval I, |I| + 2W <= m.  Then pi: Z -> Z/m is
    injective on I^{+W}, occupancy/guards/emissions correspond cell for cell,
    supp(Phi_Z T) is inside I^{+W}, and pi(Phi_Z T) = Phi_{Z/m}(pi T).

  Theorem B (lift).     S a ring rotor, Phi^p(S) = rot_d(S), with a vacant arc
    of length g >= 2pW and a representative d* of d with |d*| <= pW.  Then the
    cut-lift T of S is a finite code on Z with Phi_Z^p(T) = sigma^{d*}(T):
    a genuine glider (free traveller when d* != 0).

  Corollary.  By the Out-Degree Law such a T needs a law amending >= 2 kinds.

Everything below is recomputed through xnomos.Const/step on the Z side and
through the independent bitmask engine t4_ring on the ring side.
"""

from __future__ import annotations

import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xnomos
from t4_ring import (Ring, rotor_certificate, verify_rotation_recurrence,
                     verify_via_xnomos, vacant_arc, support_arc_start, rep)

OFFS = (-1, 0, 1)
W = 1


# --------------------------------------------------------------- Lemma W check

def zconst(R):
    return xnomos.Const(R.rules, [tuple(t) for t in R.targets], dim=1,
                        modulus=None)


def push(S, m):
    """pi_* of a Z code onto Z/m (assumes pi injective on supp(S))."""
    out = {}
    for cell, mask in S.items():
        j = cell % m
        assert j not in out, "pi not injective on the support"
        out[j] = mask
    return out


def lemma_W_trials(trials=4000, seed=771, modes=("parity", "or", "super",
                                                 "super_or")):
    """One step of Z dynamics pushes forward to one step of ring dynamics,
    whenever the support fits in an interval of length m - 2W."""
    rng = random.Random(seed)
    bad = spread_bad = 0
    for _ in range(trials):
        n = rng.randrange(1, 4)
        m = rng.randrange(5, 16)
        ell = rng.randrange(1, m - 2 * W + 1)          # |I| <= m - 2W
        mode = rng.choice(list(modes))
        rules = [(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                 for _ in range(n)]
        targets = [tuple(k for k in range(n) if rng.random() < 0.5)
                   for _ in range(n)]
        R = Ring(rules, targets, m, mode if mode in ("parity", "or")
                 else "parity")
        CZ = zconst(R)
        CR = R.xconst()
        pairs = []
        for j in range(ell):
            for k in range(n):
                if rng.random() < 0.5:
                    pairs.append((j, k))
        if not pairs:
            continue
        T = xnomos.state_of(pairs, n)
        T1 = xnomos.step(T, CZ, mode)
        S1 = xnomos.step(push(T, m), CR, mode)
        if T1 and (max(T1) > ell - 1 + W or min(T1) < -W):
            spread_bad += 1
        if push(T1, m) != S1:
            bad += 1
    print("Lemma W: %d random (constitution, code, mode) trials, "
          "%d correspondence failures, %d support-spread violations"
          % (trials, bad, spread_bad))
    return bad, spread_bad


def speed_cap_trials(trials=4000, seed=99):
    """supp(Phi_Z T) is inside supp(T)^{+W}: the support grows by at most W per
    step, hence any Z glider has |d| <= pW."""
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        n = rng.randrange(1, 4)
        mode = rng.choice(["parity", "or", "super", "super_or"])
        rules = [(rng.choice(OFFS), rng.choice(OFFS), rng.choice(OFFS))
                 for _ in range(n)]
        targets = [tuple(k for k in range(n) if rng.random() < 0.5)
                   for _ in range(n)]
        C = xnomos.Const(rules, targets)
        pairs = [(rng.randrange(-5, 6), rng.randrange(n))
                 for _ in range(rng.randrange(1, 9))]
        S = xnomos.state_of(pairs, n)
        for _ in range(6):
            if not S:
                break
            lo, hi = min(S), max(S)
            S = xnomos.step(S, C, mode)
            if S and (min(S) < lo - W or max(S) > hi + W):
                bad += 1
                break
    print("Speed cap: %d random Z runs x 6 steps, %d support-growth violations"
          % (trials, bad))
    return bad


# --------------------------------------------------------------- the cut lift

def cut_lift(R, X0):
    """Lift a ring code to Z by cutting in the middle of its longest vacant arc.

    Returns (T, alpha, ell) where T is an xnomos Z-code supported in [0, ell-1]
    and cell j of T is ring cell (alpha + j) mod m.
    """
    m = R.m
    occ = R.occ(X0)
    alpha = support_arc_start(occ, m)
    if alpha is None:
        return None, None, None
    g = vacant_arc(occ, m)
    ell = m - g
    pairs = []
    for j in range(ell):
        i = (alpha + j) % m
        for k in range(R.n):
            if (X0[k] >> i) & 1:
                pairs.append((j, k))
    return xnomos.state_of(pairs, R.n), alpha, ell


def lift_report(R, X0, p, d):
    """Attempt Theorem B on a ring rotor; report exactly what happens."""
    m = R.m
    occ = R.occ(X0)
    g = vacant_arc(occ, m)
    ell = m - g
    T, alpha, _ = cut_lift(R, X0)
    out = {"m": m, "p": p, "d": d, "g": g, "ell": ell,
           "hyp_gap": g >= 2 * p * W, "hyp_lc": abs(d) <= p * W}
    if T is None:
        out["verdict"] = "FULL-RING (no cut)"
        return out
    CZ = zconst(R)
    CR = R.xconst()
    # (1) step-by-step correspondence pi(Phi_Z^t T) = Phi^t(S), t = 0..p
    S = R.to_xnomos(X0)
    Sr = {(c - alpha) % m: v for c, v in S.items()}     # ring in cut coords
    U, corr = dict(T), True
    Sc = dict(Sr)
    for t in range(p):
        U = xnomos.step(U, CZ, R.mode)
        Sc = xnomos.step(Sc, CR, R.mode)
        try:
            if push(U, m) != Sc:
                corr = False
        except AssertionError:
            corr = False
        if not corr:
            break
    out["correspondence"] = corr
    # (2) is the lift a Z glider with displacement d?
    want = {c + d: v for c, v in T.items()}
    out["glides"] = corr and (U == want)
    # (3) independent xnomos certificate over three full periods
    out["verify_glider"] = xnomos.verify_glider(T, CZ, p, d) if d else None
    res = xnomos.classify(T, CZ, R.mode, max_steps=600, max_card=600,
                          max_span=600)
    out["classify"] = (res["kind"], res.get("period"), res.get("displacement"))
    return out


# ------------------------------------------------------------------- specimens

def o15():
    """O-15, the first odd-ring rotor (xrings/RESULTS.md 3.3): exact (p, r)."""
    rules = [(-1, 1, 1), (0, 1, -1)]
    targets = [(0,), (0,)]                              # both amend kind X
    m = 15
    R = Ring(rules, targets, m, "parity")
    Xc = [1, 5, 6, 10, 11, 12]                          # kind 0 = X
    Yc = [1, 3, 6, 8, 11, 13]                           # kind 1 = Y
    X0 = (sum(1 << i for i in Xc), sum(1 << i for i in Yc))
    cert = rotor_certificate(X0, R)
    print("O-15  constitution X:(-1,1,1)->X  Y:(0,1,-1)->X  [parity, Z/15]")
    print("      laws = %d   %s" % (R.card(X0), R.render(X0)))
    print("      certificate: p=%d  d=%+d  rot_d(S)=S? %s"
          % (cert["p"], cert["d"], cert["sym"]))
    print("      ring re-check (3 laps): %s ; xnomos re-check: %s"
          % (verify_rotation_recurrence(X0, R, cert["p"], cert["d"]),
             verify_via_xnomos(X0, R, cert["p"], cert["d"])))
    r = abs(cert["d"]) % m
    r = min(r, m - r)
    print("      min(r,m-r) = %d ;  pW = %d  -> glider-admissible: %s"
          % (r, cert["p"] * W, r <= cert["p"] * W))
    print("      2pW = %d -> X-C information-admissible: %s"
          % (2 * cert["p"] * W, r <= 2 * cert["p"] * W))
    print("      vacant arc g = %d ; Theorem B needs g >= 2pW = %d -> %s"
          % (vacant_arc(R.occ(X0), m), 2 * cert["p"] * W,
             vacant_arc(R.occ(X0), m) >= 2 * cert["p"] * W))
    print("      out-degree of every used kind = 1")
    return cert


DENSE = ([(0, -1, 0), (0, -1, -1)], [(0, 1), (0, 1)])


def dense_family(ms=(3, 4, 5, 6, 7, 8, 9, 11, 13, 15, 21)):
    """The HOLE ROTOR: every cell full but one; the hole advances one cell per
    step.  Light-cone-admissible (p=1, d=+1) with vacant arc g = 1 < 2pW = 2."""
    rules, targets = DENSE
    print("HOLE ROTOR  X:(0,-1,0)->{X,Y}   Y:(0,-1,-1)->{X,Y}   [parity]")
    rows = []
    for m in ms:
        R = Ring(rules, targets, m, "parity")
        full = (1 << m) - 1
        X0 = (full ^ 1, full ^ 1)                      # cell 0 vacant
        cert = rotor_certificate(X0, R)
        ok1 = verify_rotation_recurrence(X0, R, cert["p"], cert["d"])
        ok2 = verify_via_xnomos(X0, R, cert["p"], cert["d"])
        rep_ = lift_report(R, X0, cert["p"], cert["d"])
        print("  m=%-3d laws=%-3d p=%d d=%+d sym=%s | ring=%s xnomos=%s | "
              "g=%d < 2pW=%d | cut-lift: corr=%s glides=%s classify=%s"
              % (m, R.card(X0), cert["p"], cert["d"], cert["sym"], ok1, ok2,
                 rep_["g"], 2 * cert["p"] * W, rep_.get("correspondence"),
                 rep_.get("glides"), rep_["classify"]))
        rows.append((m, cert, rep_))
    R = Ring(rules, targets, 7, "parity")
    full = (1 << 7) - 1
    X = (full ^ 1, full ^ 1)
    print("  spacetime, Z/7:")
    for _ in range(4):
        print("    " + R.render(X))
        X = R.step(X)
    return rows


def dense_all_lifts(m=7):
    """No injective lift of the HOLE ROTOR into a window of length < m glides.
    (There are exactly m cut positions; the code occupies m-1 of the m cells,
    so a window-lift is determined by which cell is left out -- i.e. by the
    hole -- and the hole is where the cut must be.)"""
    rules, targets = DENSE
    R = Ring(rules, targets, m, "parity")
    CZ = zconst(R)
    full = (1 << m) - 1
    X0 = (full ^ 1, full ^ 1)
    hits = 0
    for cut in range(m):
        pairs = []
        for j in range(m):
            i = (cut + j) % m
            for k in range(R.n):
                if (X0[k] >> i) & 1:
                    pairs.append((j, k))
        T = xnomos.state_of(pairs, R.n)
        for d in (-1, 0, 1):
            if xnomos.verify_glider(T, CZ, 1, d):
                hits += 1
    print("  all %d cut-lifts x d in {-1,0,+1}: %d that satisfy "
          "Phi_Z(T) = sigma^d(T)" % (m, hits))
    return hits


# ------------------------------------------------------------ Theorem B checks

def theorem_B_tandem(ms=range(3, 41)):
    rules = [(0, -1, 1), (0, -1, 0)]
    targets = [(0, 1), (0, 1)]
    bad = []
    for m in ms:
        R = Ring(rules, targets, m, "parity")
        X0 = (1, 1)
        c = rotor_certificate(X0, R)
        r = lift_report(R, X0, c["p"], c["d"])
        if not (r["hyp_gap"] and r["hyp_lc"] and r["correspondence"]
                and r["glides"] and r["verify_glider"]
                and r["classify"][0] == "GLIDER"):
            bad.append((m, r))
    print("Theorem B on TANDEM-1, m = %d..%d: %d rings, %d failures"
          % (min(ms), max(ms), len(list(ms)), len(bad)))
    for m, r in bad[:5]:
        print("   FAIL", m, r)
    return bad


if __name__ == "__main__":
    print("=== machine checks of the two lemmas ===")
    lemma_W_trials()
    speed_cap_trials()
    print()
    print("=== Theorem B: TANDEM-1 lifts to a Z glider on every ring ===")
    theorem_B_tandem()
    print()
    print("=== O-15 ===")
    o15()
    print()
    print("=== the gap hypothesis is necessary ===")
    dense_family()
    dense_all_lifts(7)
    dense_all_lifts(9)
