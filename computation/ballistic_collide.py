"""Collision resolution machinery for the ballistic sector.

THE SEPARATION LEMMA (machine-checked, exact).
Let S = A u B with supp(A) entirely left of supp(B).  Write A_t, B_t for the
ISOLATED evolutions.  If for every t in [0,N]

        min(supp B_t) - max(supp A_t) >= 3,                              (*)

then Phi^t(A u B) = A_t u B_t for all t in [0,N].
  Proof.  Induction.  Every offset a,b,c lies in {-1,0,1}, so a law at cell i
  reads and writes only inside [i-1,i+1].  Under (*) at time t, no cell of
  [min A_t - 1, max A_t + 1] holds a law of B_t and no cell of
  [min B_t - 1, max B_t + 1] holds a law of A_t; hence every guard evaluates on
  its own component and every toggle lands on its own component.  QED.

EXTENSION TO t = infinity.  If A is a certified (p,d)-glider and B a certified
(q,e)-glider, put P = lcm(p,q), dA = d*P/p, dB = e*P/q.  Then
f(t) = min(supp B_t) - max(supp A_t) satisfies f(t+P) = f(t) + (dB - dA).
So if dB >= dA and (*) holds for every t in [0, P + t0), it holds for all t.
Both halves are checked by `sep_forever`.
"""
import sys, itertools
from math import gcd
sys.path.insert(0, "/Users/lukacs/claude/math/program/phase6/computation")
from ballistic_lib import *


def clusters(S, gapmin=3):
    """Split a state into maximal groups separated by >= gapmin empty cells."""
    if not S:
        return []
    cs = sorted(S)
    out, cur = [], [cs[0]]
    for x in cs[1:]:
        if x - cur[-1] >= gapmin + 1:
            out.append(cur); cur = [x]
        else:
            cur.append(x)
    out.append(cur)
    return [{c: S[c] for c in g} for g in out]


def lcm(a, b):
    return a * b // gcd(a, b)


def sep_forever(comps, C, mode, N=200):
    """Check (*) for the whole list of components (left to right), for all
    t in [0, N] AND, when every component is a glider, for a full common
    period so that the conclusion extends to t = infinity.

    Returns (ok_finite, ok_forever, certs) where certs is the per-component
    classification."""
    # cheap screen first: interleave stepping with the (*) test and bail on
    # the first violation, so an approaching pair costs O(1) not O(N).
    cur = [dict(X) for X in comps]
    ok_fin = True
    for t in range(N + 1):
        for i in range(len(cur) - 1):
            A, B = cur[i], cur[i + 1]
            if not A or not B:
                continue
            if min(B) - max(A) < 3:
                ok_fin = False
                break
        if not ok_fin:
            break
        if t < N:
            cur = [step(X, C, mode) if X else X for X in cur]
    if not ok_fin:
        return False, False, [{"kind": UNRESOLVED} for _ in comps]
    certs = [classify(dict(X), C, mode, max_steps=400, max_card=400,
                      max_span=1500) for X in comps]
    ok_all = ok_fin
    if ok_fin and all(c["kind"] == GLIDER for c in certs):
        P = 1
        for c in certs:
            P = lcm(P, c["period"])
        # per-P displacement of each component, left to right must be
        # non-decreasing
        ds = [c["displacement"] * P // c["period"] for c in certs]
        mono = all(ds[i] <= ds[i + 1] for i in range(len(ds) - 1))
        t0 = max(c["t"] for c in certs)
        ok_all = mono and N >= P + t0
    elif ok_fin and all(c["kind"] in (EXTINCT, FIXED, BALANCED, CYCLE, GLIDER)
                        for c in certs):
        # mixture of gliders and stationary things: same argument with
        # displacement 0 for the stationary ones
        P = 1
        for c in certs:
            P = lcm(P, c.get("period", 1) or 1)
        ds = [(c["displacement"] * P // c["period"]) if c["kind"] == GLIDER
              else 0 for c in certs]
        mono = all(ds[i] <= ds[i + 1] for i in range(len(ds) - 1))
        t0 = max(c.get("t", 0) for c in certs)
        ok_all = mono and N >= P + t0
    return ok_fin, ok_all, certs


RESOLVED = (EXTINCT, FIXED, BALANCED, CYCLE, GLIDER)


def resolve(S0, C, mode, T_max=260, N_sep=140, gapmin=3,
            max_card=400, max_span=1200):
    """Run the collision and certify the outcome.

    Returns dict with
      out    : 'EXTINCT' | 'SINGLE:<kind>' | 'SPLIT'
      parts  : list of (kind, period, displacement, card) left to right
      t_res  : the time at which the outcome was certified
      forever: True if the separation certificate extends to t = infinity
    """
    # global shortcut.  classify() already certifies EXTINCT / FIXED /
    # BALANCED / CYCLE / GLIDER for the whole state, transients included, so
    # the decomposition loop below only has to handle the multi-packet case.
    g = classify(dict(S0), C, mode, max_steps=T_max, max_card=max_card,
                 max_span=max_span)
    if g["kind"] == GLIDER:
        return {"out": "SINGLE", "parts": [(GLIDER, g["period"],
                                            g["displacement"], g["card"])],
                "t_res": g["t"], "forever": True, "global": GLIDER}
    if g["kind"] in (EXTINCT, FIXED, BALANCED, CYCLE):
        return {"out": "SINGLE", "parts": [(g["kind"], g.get("period", 0), 0,
                                            g.get("card", 0))],
                "t_res": g["t"], "forever": True, "global": g["kind"],
                "active": g.get("active", 0)}
    S = dict(S0)
    merged = len(clusters(S0, gapmin)) <= 1
    for t in range(T_max):
        if not S:
            return {"out": "SINGLE", "parts": [(EXTINCT, 0, 0, 0)],
                    "t_res": t, "forever": True, "global": EXTINCT}
        comps = clusters(S, gapmin)
        # The inputs start apart.  Testing separation before they have ever
        # touched is pure waste, so wait until the packets have merged into a
        # single cluster at least once, then look for a clean re-split.
        if not merged:
            if len(comps) <= 1:
                merged = True
        if merged and len(comps) >= 2:
            ok_fin, ok_all, certs = sep_forever(comps, C, mode, N=N_sep)
            if ok_fin and all(c["kind"] in RESOLVED for c in certs):
                parts = [(c["kind"], c.get("period", 0),
                          c.get("displacement", 0), c.get("card", 0))
                         for c in certs]
                return {"out": "SPLIT" if len(comps) > 1 else "SINGLE",
                        "parts": parts, "t_res": t, "forever": ok_all,
                        "global": g["kind"], "ncomp": len(comps)}
        S = step(S, C, mode)
        if card(S) > max_card or (S and max(S) - min(S) > max_span):
            return {"out": "GROWING", "parts": [], "t_res": t,
                    "forever": False, "global": g["kind"]}
    return {"out": "UNRESOLVED", "parts": [], "t_res": T_max,
            "forever": False, "global": g["kind"]}


def bucket(res, nin_left, nin_right):
    """Name the collision outcome.  nin_* = 1 if that input glider was
    present.  Buckets follow the expedition brief."""
    if res["out"] in ("GROWING", "UNRESOLVED"):
        return "EXPLOSION" if res["out"] == "GROWING" else "UNRESOLVED"
    parts = res["parts"]
    movers = [p for p in parts if p[0] == GLIDER]
    right = [p for p in movers if p[2] > 0]
    left = [p for p in movers if p[2] < 0]
    stat = [p for p in parts if p[0] in (FIXED, BALANCED, CYCLE)]
    nin = nin_left + nin_right
    nout = len(movers)
    if not parts or all(p[0] == EXTINCT for p in parts):
        return "ANNIHILATION"
    if nout == 0:
        return "ARREST"
    if nout > nin:
        return "FAN-OUT"
    if nout == nin and len(right) == nin_right and len(left) == nin_left:
        return "TRANSPARENCY" if not stat else "TRANSPARENCY+DEBRIS"
    if nout == nin:
        return "REFLECTION"          # same count, wrong directions
    if nout < nin:
        if len(right) > 0 or len(left) > 0:
            if (nin_right and nin_left and
                    ((len(right) and not len(left)) or
                     (len(left) and not len(right)))):
                return "ABSORPTION"
            return "ABSORPTION"
    return "OTHER"


def fmt_parts(res):
    s = []
    for k, p, d, c in res["parts"]:
        if k == GLIDER:
            s.append("G(p%d,d%+d,c%d)" % (p, d, c))
        elif k == EXTINCT:
            s.append("0")
        elif k == CYCLE:
            s.append("O(p%d,c%d)" % (p, c))
        else:
            s.append("%s(c%d)" % (k[:3], c))
    return "+".join(s) if s else "-"
