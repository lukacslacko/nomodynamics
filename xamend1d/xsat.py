#!/usr/bin/env python3
"""
xsat.py — the SAT instrument of Expedition X-A.

Encodes the QUESTION, not a seed: variables for the seed AND for the
constitution (offsets a_k, b_k, c_k as one-hot trits; the amendment target
matrix as free Booleans), unrolled p steps, asserting

        Phi^p(S) = sigma^d(S),   S != empty,   d != 0.

EXACTNESS.  We model N cells 0..N-1 and force the W outermost cells on each
side to be EMPTY OF EVERY KIND AT EVERY TIME t = 0..p.  Then

  * every law sits in [W, N-1-W], so its guard reads (i +- W) and its emission
    (i + c) land inside [0, N-1] — no truncation of the rule;
  * a toggle landing in the forced-empty margin would *create* a law there
    (a toggle into an empty slot is an enactment), contradicting the forcing;
    so the solver is compelled to reproduce exactly the Z-dynamics of any
    pattern whose whole trajectory fits in the interior.

Hence UNSAT is a genuine no-go over Z for the stated box:
  "no glider of period p and displacement d, over ANY constitution in the
   class, whose t=0..p trajectory spans at most N - 2W cells."

Translation symmetry is broken exactly (no loss) by forcing the leftmost cell
ever occupied during t = 0..p to be cell W.

SEMANTICS COVERED
  mode='parity' / 'or'   — free target matrix tgt[k][m] (>=1 target per kind).
                           Subsumes own-kind, E2 permutation targeting and E3
                           multi-target in ONE encoding.
  mode='super'/'super_or'— E1 supersession: an active law enacts its own kind
                           on empty ground, else clears the whole target cell.
Rings (modulus m) are supported for validation (the Z/6 rotor).
"""

from __future__ import annotations

import itertools

# ------------------------------------------------------------------ circuit


class Circ:
    """Tseitin circuit builder.  A *signal* is a bool constant or an int literal."""

    def __init__(self):
        self.nv = 0
        self.cls = []
        self._memo = {}

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, *lits):
        self.cls.append(list(lits))

    # -- gates ------------------------------------------------------------
    def AND(self, xs):
        xs = list(xs)
        out = []
        for x in xs:
            if x is True:
                continue
            if x is False:
                return False
            out.append(x)
        if not out:
            return True
        s = set(out)
        for l in s:
            if -l in s:
                return False
        out = sorted(s)
        if len(out) == 1:
            return out[0]
        key = ("&",) + tuple(out)
        if key in self._memo:
            return self._memo[key]
        z = self.new()
        for l in out:
            self.add(-z, l)
        self.add(z, *[-l for l in out])
        self._memo[key] = z
        return z

    def OR(self, xs):
        return self.NOT(self.AND([self.NOT(x) for x in xs]))

    @staticmethod
    def NOT(x):
        return (not x) if isinstance(x, bool) else -x

    def XOR2(self, a, b):
        if a is True:
            return self.NOT(b)
        if a is False:
            return b
        if b is True:
            return self.NOT(a)
        if b is False:
            return a
        if a == b:
            return False
        if a == -b:
            return True
        key = ("^",) + tuple(sorted((a, b), key=abs))
        # note: XOR is sign-sensitive; canonicalise sign onto the output
        neg = False
        aa, bb = a, b
        if aa < 0:
            aa, neg = -aa, not neg
        if bb < 0:
            bb, neg = -bb, not neg
        key = ("^", min(aa, bb), max(aa, bb))
        if key in self._memo:
            z = self._memo[key]
        else:
            z = self.new()
            self.add(-z, aa, bb)
            self.add(-z, -aa, -bb)
            self.add(z, -aa, bb)
            self.add(z, aa, -bb)
            self._memo[key] = z
        return -z if neg else z

    def XOR(self, xs):
        acc = False
        for x in xs:
            acc = self.XOR2(acc, x)
        return acc

    def ITE(self, c, t, e):
        return self.OR([self.AND([c, t]), self.AND([self.NOT(c), e])])

    def IFF(self, a, b):
        """Assert a <-> b as hard clauses."""
        if a is True:
            self.assert_(b)
            return
        if a is False:
            self.assert_(self.NOT(b))
            return
        if b is True:
            self.assert_(a)
            return
        if b is False:
            self.assert_(self.NOT(a))
            return
        self.add(-a, b)
        self.add(a, -b)

    def assert_(self, x):
        if x is True:
            return
        if x is False:
            self.add()          # empty clause = UNSAT
            return
        self.add(x)

    def exactly_one(self, xs):
        self.add(*xs)
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                self.add(-xs[i], -xs[j])


# ------------------------------------------------------------------ encoding


class Spec:
    """A bounded glider-existence question."""

    def __init__(self, n, W, N, p, d, mode="parity",
                 targets=None, perm_cycle=None, modulus=None,
                 max_laws=None, fixed_rules=None, fixed_targets=None,
                 min_laws=None, allow_self_target=True, kinds_used=None,
                 assert_glider=True, symbreak=True, nonfixed=False,
                 prime_period=False):
        self.assert_glider = assert_glider
        self.symbreak = symbreak
        self.nonfixed = nonfixed          # forbid Phi(S) = S
        self.prime_period = prime_period  # forbid S_s == S_0 for 0 < s < p
        self.n = n                    # number of kinds
        self.W = W                    # offsets range over -W..W
        self.N = N                    # cells 0..N-1 (margins W on each side)
        self.p = p                    # period
        self.d = d                    # displacement
        self.mode = mode
        self.modulus = modulus        # ring Z/m (then N == m, no margins)
        self.max_laws = max_laws
        self.min_laws = min_laws
        self.allow_self_target = allow_self_target
        # target structure: None = free Boolean matrix;
        # perm_cycle = L  -> fixed single L-cycle t(k) = k+1 mod n (needs n==L);
        # targets = list of tuples -> fixed
        self.targets = targets
        self.perm_cycle = perm_cycle
        self.fixed_rules = fixed_rules        # list of (a,b,c) or None
        self.fixed_targets = fixed_targets
        self.kinds_used = kinds_used

    def label(self):
        t = ("free" if self.targets is None and self.perm_cycle is None
             else ("cyc%d" % self.perm_cycle if self.perm_cycle else "fix"))
        return ("n=%d W=%d N=%d p=%d d=%d %s tgt=%s%s"
                % (self.n, self.W, self.N, self.p, self.d, self.mode, t,
                   "" if self.max_laws is None else " <=%dlaws" % self.max_laws))


def build(sp: Spec):
    C = Circ()
    n, W, N, p, d = sp.n, sp.W, sp.N, sp.p, sp.d
    offs = list(range(-W, W + 1))
    ring = sp.modulus is not None
    margin = 0 if ring else W

    def cell(i):
        """Return normalised cell index, or None if outside the model."""
        if ring:
            return i % sp.modulus
        return i if 0 <= i < N else None

    # ---- constitution variables -----------------------------------------
    A = [[None] * len(offs) for _ in range(n)]
    B = [[None] * len(offs) for _ in range(n)]
    Cc = [[None] * len(offs) for _ in range(n)]
    for k in range(n):
        for arr, idx in ((A, 0), (B, 1), (Cc, 2)):
            if sp.fixed_rules is not None:
                val = sp.fixed_rules[k][idx]
                for vi, v in enumerate(offs):
                    arr[k][vi] = (v == val)
            else:
                vs = [C.new() for _ in offs]
                C.exactly_one(vs)
                for vi in range(len(offs)):
                    arr[k][vi] = vs[vi]

    # ---- target matrix ---------------------------------------------------
    # tgt[k][m] : an active law of kind k toggles kind m at i + c_k
    tgt = [[False] * n for _ in range(n)]
    if sp.perm_cycle is not None:
        assert n == sp.perm_cycle
        for k in range(n):
            tgt[k][(k + 1) % n] = True
    elif sp.targets is not None:
        for k in range(n):
            for m in sp.targets[k]:
                tgt[k][m] = True
    else:
        for k in range(n):
            row = []
            for m in range(n):
                if m == k and not sp.allow_self_target:
                    tgt[k][m] = False
                    continue
                v = C.new()
                tgt[k][m] = v
                row.append(v)
            C.add(*row)                    # every kind amends something

    # ---- state variables -------------------------------------------------
    x = [[[None] * n for _ in range(N)] for _ in range(p + 1)]
    for s in range(p + 1):
        for i in range(N):
            inside = ring or (margin <= i < N - margin)
            for k in range(n):
                if not inside:
                    x[s][i][k] = False
                elif sp.kinds_used is not None and k not in sp.kinds_used:
                    x[s][i][k] = False
                elif s == 0:
                    x[s][i][k] = C.new()
                else:
                    x[s][i][k] = C.new()

    occ = [[None] * N for _ in range(p + 1)]
    for s in range(p + 1):
        for i in range(N):
            occ[s][i] = C.OR([x[s][i][k] for k in range(n)])

    def occ_at(s, i):
        j = cell(i)
        return False if j is None else occ[s][j]

    # ---- dynamics --------------------------------------------------------
    for s in range(p):
        # activity
        act = [[None] * n for _ in range(N)]
        for i in range(N):
            for k in range(n):
                if x[s][i][k] is False:
                    act[i][k] = False
                    continue
                ga = C.OR([C.AND([A[k][vi], occ_at(s, i + v)])
                           for vi, v in enumerate(offs)])
                gb = C.OR([C.AND([B[k][vi], occ_at(s, i + v)])
                           for vi, v in enumerate(offs)])
                act[i][k] = C.AND([x[s][i][k], ga, C.NOT(gb)])

        # hit[j][k] : kind k's (unique) law targeting cell j is active
        hit = [[None] * n for _ in range(N)]
        for j in range(N):
            for k in range(n):
                terms = []
                for vi, v in enumerate(offs):
                    src = cell(j - v)
                    if src is None:
                        continue
                    terms.append(C.AND([Cc[k][vi], act[src][k]]))
                hit[j][k] = C.OR(terms)

        if sp.mode in ("parity", "or"):
            for j in range(N):
                for m in range(n):
                    contrib = [C.AND([tgt[k][m], hit[j][k]]) for k in range(n)]
                    tog = (C.XOR(contrib) if sp.mode == "parity"
                           else C.OR(contrib))
                    C.IFF(x[s + 1][j][m], C.XOR2(x[s][j][m], tog))
        else:                                   # supersession
            oresolve = (sp.mode == "super_or")
            for j in range(N):
                votes = [hit[j][k] for k in range(n)]
                agg = C.OR(votes) if oresolve else C.XOR(votes)
                clr = C.AND([occ[s][j], agg])
                for k in range(n):
                    keep = C.AND([x[s][j][k], C.NOT(clr)])
                    born = C.AND([C.NOT(occ[s][j]), hit[j][k]])
                    C.IFF(x[s + 1][j][k], C.OR([keep, born]))

    # ---- the glider assertion -------------------------------------------
    dsel = None
    if sp.assert_glider:
        C.assert_(C.OR([x[0][i][k] for i in range(N) for k in range(n)]))
        if isinstance(d, (list, tuple)):          # displacement is a variable
            dsel = {dd: C.new() for dd in d}
            C.exactly_one(list(dsel.values()))
            for dd, sel in dsel.items():
                for j in range(N):
                    src = cell(j - dd)
                    o = False if src is None else x[0][src][k := 0]
                    for k in range(n):
                        o = False if src is None else x[0][src][k]
                        u, v = x[p][j][k], o
                        if u is False and v is False:
                            continue
                        if u is False:
                            C.add(-sel, *( [-v] if v is not True else []))
                            if v is True:
                                C.add(-sel)
                            continue
                        if v is False:
                            C.add(-sel, -u)
                            continue
                        if v is True:
                            C.add(-sel, u)
                            continue
                        C.add(-sel, -u, v)
                        C.add(-sel, u, -v)
        else:
            for j in range(N):
                src = cell(j - d)
                for k in range(n):
                    C.IFF(x[p][j][k], False if src is None else x[0][src][k])

    # ---- non-degeneracy --------------------------------------------------
    def differ(s1, s2, sh=0):
        ds = []
        for j in range(N):
            src = cell(j - sh)
            for k in range(n):
                other = False if src is None else x[s2][src][k]
                ds.append(C.XOR2(x[s1][j][k], other))
        return C.OR(ds)

    if sp.nonfixed and p >= 1:
        C.assert_(differ(1, 0))
    if sp.prime_period:
        for s in range(1, p):
            if p % s == 0:
                C.assert_(differ(s, 0, (d * s) // p if p and d * s % p == 0 else 0))

    # ---- translation symmetry break (exact) ------------------------------
    if not ring and sp.symbreak:
        ever = [C.OR([x[s][i][k] for s in range(p + 1) for k in range(n)])
                for i in range(N)]
        C.assert_(ever[margin])

    # ---- optional cardinality on the seed --------------------------------
    lits = [x[0][i][k] for i in range(N) for k in range(n)
            if x[0][i][k] is not True and x[0][i][k] is not False]
    if sp.max_laws is not None and lits:
        _atmost(C, lits, sp.max_laws)
    if sp.min_laws is not None and lits:
        _atmost(C, [-l for l in lits], len(lits) - sp.min_laws)

    meta = dict(A=A, B=B, Cc=Cc, tgt=tgt, x=x, offs=offs, spec=sp, dsel=dsel)
    return C, meta


def _atmost(C, lits, k):
    """Sequential counter at-most-k."""
    m = len(lits)
    if k >= m:
        return
    if k == 0:
        for l in lits:
            C.add(-l)
        return
    s = [[C.new() for _ in range(k)] for _ in range(m)]
    C.add(-lits[0], s[0][0])
    for j in range(1, k):
        C.add(-s[0][j])
    for i in range(1, m):
        C.add(-lits[i], s[i][0])
        C.add(-s[i - 1][0], s[i][0])
        for j in range(1, k):
            C.add(-lits[i], -s[i - 1][j - 1], s[i][j])
            C.add(-s[i - 1][j], s[i][j])
        C.add(-lits[i], -s[i - 1][k - 1])


# ------------------------------------------------------------------ solving


def solve(sp: Spec, solver="cadical195", timeout=None, verbose=False,
          built=None):
    """Returns (status, model_info).  status in {'SAT','UNSAT','TIMEOUT'}."""
    from pysat.solvers import Solver
    C, meta = build(sp) if built is None else built
    if verbose:
        print("  vars=%d clauses=%d" % (C.nv, len(C.cls)))
    with Solver(name=solver, bootstrap_with=C.cls) as S:
        if timeout is not None:
            import threading
            timer = threading.Timer(timeout, S.interrupt)
            timer.start()
            try:
                r = S.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel()
        else:
            r = S.solve()
        if r is None:
            return "TIMEOUT", None
        if not r:
            return "UNSAT", dict(nv=C.nv, nc=len(C.cls))
        model = set(l for l in S.get_model() if l > 0)
    return "SAT", extract(meta, model)


def val(sig, model):
    if sig is True:
        return True
    if sig is False:
        return False
    return (sig in model) if sig > 0 else (-sig not in model)


def extract(meta, model):
    sp = meta["spec"]
    offs = meta["offs"]
    n, N, p = sp.n, sp.N, sp.p
    rules, targets = [], []
    for k in range(n):
        r = []
        for arr in (meta["A"], meta["B"], meta["Cc"]):
            hits = [offs[vi] for vi in range(len(offs)) if val(arr[k][vi], model)]
            assert len(hits) == 1, hits
            r.append(hits[0])
        rules.append(tuple(r))
        targets.append(tuple(m for m in range(n) if val(meta["tgt"][k][m], model)))
    frames = []
    for s in range(p + 1):
        st = {}
        for i in range(N):
            msk = 0
            for k in range(n):
                if val(meta["x"][s][i][k], model):
                    msk |= 1 << k
            if msk:
                st[i] = msk
        frames.append(st)
    return dict(rules=rules, targets=targets, frames=frames, spec=sp)
