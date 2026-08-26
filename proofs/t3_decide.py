#!/usr/bin/env python3
"""
t3_decide.py -- width-unbounded glider decisions for the single-field W=1
sector, written independently of xspeed/sft.py.

A (p,d)-glider is a finite non-empty S with Phi^p(S) = S + d.  Its space-time
diagram, read as a bi-infinite sequence of COLUMNS v_x in {0,1}^p (bit t =
occ(t,x), t = 0..p-1), is exactly a bi-infinite path, quiescent at both ends,
of a finite transition system: the CA has radius 2, so the constraint

    C(y):   occ(t+1, y) = tab[ occ(t, y-2..y+2) ]   for t = 0..p-1,
            with occ(p, y) := occ(0, y-d) = bit0(v_{y-d})

is decidable from v_{y-2..y+2} plus bit0(v_{y-d}).  Scanning left to right and
checking C(x-1) when column v_{x+1} is appended, the carried state is

    cols = (v_{x-3}, v_{x-2}, v_{x-1}, v_x)        four full columns
    olds = bit0 of v_{x-4}, ..., v_{x-3-E}         E = max(0, d-2) extra bits

and a glider exists IFF the quiescent state lies on a cycle carrying a
non-zero column.  No bound whatsoever on the width (span) of the pattern.

Speed note: for fixed t only bit t of the appended column enters C(x-1), so
the legal successors factor bitwise; we never enumerate all 2^p columns.
"""
from __future__ import annotations

import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from t3_core import rule_table, step_set          # noqa: E402


def _succ_columns(tab, p, d, cols, olds, E):
    """All legal appended columns `new`, as a list of ints."""
    v3, v2, v1, v0 = cols                      # v_{x-3}, v_{x-2}, v_{x-1}, v_x
    allowed = []                               # per t: list of legal bit values
    for t in range(p):
        b = (((v3 >> t) & 1)
             | (((v2 >> t) & 1) << 1)
             | (((v1 >> t) & 1) << 2)
             | (((v0 >> t) & 1) << 3))
        if t + 1 < p:
            want = (v1 >> (t + 1)) & 1
        elif d <= 2:
            want = (v2 if d == 1 else v3) & 1   # bit0 of v_{x-1-d}
        else:
            want = olds[0]
        ok = [x for x in (0, 1) if tab[b | (x << 4)] == want]
        if not ok:
            return []
        allowed.append(ok)
    out = [0]
    for t in range(p):
        a = allowed[t]
        if len(a) == 1:
            if a[0]:
                out = [x | (1 << t) for x in out]
        else:
            out = out + [x | (1 << t) for x in out]
    return out


def decide(cls, p, d, mode="parity", cap=3_000_000):
    """('GLIDER', columns) | ('NONE', None) | ('CAP', None).

    `cls` is a parity class (u,v,w) or an OR class (U,V,W); see t3_core.
    """
    assert 1 <= d
    tab = rule_table(cls, mode)
    if tab[0] != 0:
        raise AssertionError("non-quiescent vacuum")
    E = max(0, d - 2)
    q0 = ((0, 0, 0, 0), (0,) * E)

    def step(st, new):
        cols, olds = st
        ncols = (cols[1], cols[2], cols[3], new)
        nolds = (olds[1:] + (cols[0] & 1,)) if E else ()
        return (ncols, nolds)

    # BFS from every state reached from q0 by first appending a NON-ZERO column.
    seen = {q0: None}
    start = []
    for new in _succ_columns(tab, p, d, q0[0], q0[1], E):
        if new == 0:
            continue
        ns = step(q0, new)
        if ns == q0:
            continue
        if ns not in seen:
            seen[ns] = (q0, new)
            start.append(ns)
    dq = deque(start)
    while dq:
        st = dq.popleft()
        for new in _succ_columns(tab, p, d, st[0], st[1], E):
            ns = step(st, new)
            if ns == q0:
                # reconstruct the column word
                path = [new]
                cur = st
                while seen[cur] is not None:
                    par, col = seen[cur]
                    path.append(col)
                    cur = par
                path.reverse()
                return "GLIDER", path
            if ns in seen:
                continue
            seen[ns] = (st, new)
            if len(seen) > cap:
                return "CAP", None
            dq.append(ns)
    return "NONE", None


def witness_seed(cols):
    """t = 0 occupied cells of a witness column word."""
    return sorted(x for x, c in enumerate(cols) if c & 1)


def check_witness(cls, cols, p, d, mode="parity"):
    """Re-run the witness through the plain CA (independent of the decider)."""
    S = set(witness_seed(cols))
    if not S:
        return False
    tab = rule_table(cls, mode)
    T = set(S)
    for _ in range(p):
        T = step_set(T, tab)
    if T != {x + d for x in S}:
        return False
    # three full periods, for good measure
    T = set(S)
    for r in range(1, 4):
        for _ in range(p):
            T = step_set(T, tab)
        if T != {x + r * d for x in S}:
            return False
    return True


def check_witness_xnomos(cls, cols, p, d, mode="parity"):
    """Re-run the witness through the reference engine xnomos, with kinds."""
    import xnomos
    from t3_core import uvw_to_channels, UVW_to_channels, to_xnomos
    chans = (uvw_to_channels(*cls) if mode == "parity"
             else UVW_to_channels(*cls))
    if not chans:
        return None
    n = len(chans)
    cells = witness_seed(cols)
    if not cells:
        return False
    C = to_xnomos(chans, n)
    S = {c: (1 << n) - 1 for c in cells}
    return xnomos.verify_glider(S, C, p, d, mode)


def minimal_pd(cls, cols, p, d, mode="parity"):
    """The minimal (p0,d0) of a witness: the generator of its symmetry group."""
    S = set(witness_seed(cols))
    tab = rule_table(cls, mode)
    T = set(S)
    for q in range(1, p + 1):
        T = step_set(T, tab)
        # is Phi^q(S) a translate of S?
        if len(T) == len(S) and T:
            sh = min(T) - min(S)
            if T == {x + sh for x in S}:
                return (q, sh)
    return None


# ----------------------------------------------------- brute-force validator

def brute_force(cls, p, d, mode="parity", span=None, cells=None):
    """Complete search over all seeds inside a box of `span` cells.

    Returns a witness seed (list of cells) or None.  Exponential -- for tests.
    """
    tab = rule_table(cls, mode)
    n = span
    for mask in range(1, 1 << n):
        S = {i for i in range(n) if (mask >> i) & 1}
        T = set(S)
        for _ in range(p):
            T = step_set(T, tab)
        if T == {x + d for x in S}:
            return sorted(S)
    return None


def _selftest():
    from t3_core import channels_to_uvw, channels_to_UVW
    ok = 0
    # 1. MIRROR (n=2, W=1): rules (0,1,-1) and (0,-1,1), single field.
    mir = [(0, 1, -1), (0, -1, 1)]
    cls = channels_to_uvw(mir)
    for (p, d, want) in [(5, 2, "GLIDER"), (4, 2, "GLIDER"), (3, 2, "NONE"),
                         (4, 3, "NONE"), (3, 1, "NONE"), (2, 1, "NONE")]:
        v, w = decide(cls, p, d, "parity")
        assert v == want, (p, d, v, want)
        if v == "GLIDER":
            assert check_witness(cls, w, p, d, "parity")
            assert check_witness_xnomos(cls, w, p, d, "parity")
        ok += 1
    # under OR MIRROR has no d=2 glider at all
    clso = channels_to_UVW(mir)
    for p in (4, 5, 6):
        v, _ = decide(clso, p, 2, "or")
        assert v == "NONE", (p, v)
        ok += 1
    # 2. TANDEM-1: (0,-1,1),(0,-1,0)  ->  p=1, d=1
    tan = [(0, -1, 1), (0, -1, 0)]
    ct = channels_to_uvw(tan)
    v, w = decide(ct, 1, 1, "parity")
    assert v == "GLIDER" and check_witness_xnomos(ct, w, 1, 1, "parity"), v
    ok += 1
    # 3. brute force cross-check on random classes, small p,d, box 12
    import random
    rng = random.Random(5)
    from t3_core import all_parity_classes
    cl = all_parity_classes()
    agree = 0
    for _ in range(400):
        c = rng.choice(cl)
        p = rng.randrange(1, 5)
        d = rng.randrange(1, p + 1)
        v, wcols = decide(c, p, d, "parity")
        bf = brute_force(c, p, d, "parity", span=12)
        if v == "NONE":
            assert bf is None, ("decider NONE but brute force found", c, p, d, bf)
        agree += 1
    ok += 1
    print("t3_decide self-tests passed (%d groups, %d brute-force cross-checks)"
          % (ok, agree))


if __name__ == "__main__":
    _selftest()
