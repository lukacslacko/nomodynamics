#!/usr/bin/env python3
"""
sft.py — WIDTH-UNBOUNDED glider decisions for full-target constitutions.

The SAT instrument decides a *box*: "no glider whose trajectory fits in N-2W
cells".  After the n=2/W=1/p=5/d=2 specimen turned up only at interior 26, box
results stopped being trustworthy as no-goes.  This module removes the box.

REDUCTION.  If every kind amends every kind (T_k = K for all k) then, by X-A's
Twin-Kind Lemma, a glider has supp_m identical for all m: the state is a single
set S subseteq Z, and the constitution acts as n independent *channels*

    channel k = (a_k, b_k, c_k):   i in S is k-active iff  i+a_k in S  and
                                   i+b_k not in S;  it toggles cell i + c_k.

  parity: cell j flips iff an ODD number of channels toggle it
  or    : cell j flips iff at least one channel toggles it

so the dynamics is a one-bit CA of radius r = 2W (a channel at i = j - c_k
reads i + a_k, i + b_k, both within W of i, hence within 2W of j).

DECISION.  Glider space-time diagrams with F^p = sigma^d are exactly the
bi-infinite paths, quiescent at both ends, of a subshift of finite type whose
letters are the *columns* v_x = (c_0(x), ..., c_{p-1}(x)) in {0,1}^p, with
c_p(x) := c_0(x-d) supplied by the glider condition itself.  Scanning columns
left to right, every constraint centred on column y is decidable once columns
y-r .. y+r and the row-0 bit of column y-d are known.  So the reachable part
of the transition graph is searched by BFS from the quiescent state, and

    a glider of period p, displacement d exists  <=>  the quiescent state lies
    on a cycle that carries at least one non-zero column

— with NO bound on the width of the pattern.  A returned witness is handed to
`xnomos.verify_glider` before it is believed.
"""
from __future__ import annotations

import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "xamend1d"))
sys.path.insert(0, os.path.dirname(HERE))


def step_table(channels, W, mode="parity"):
    """Lookup table: window of 2r+1 cells (bit i = cell offset i-r) -> new centre bit.

    channels = [(a,b,c), ...].  Returns a list of length 2**(2r+1).
    """
    r = 2 * W
    n_in = 2 * r + 1
    tab = []
    for w in range(1 << n_in):
        def occ(off):                      # occupancy at centre + off, |off| <= r
            return (w >> (off + r)) & 1
        hits = 0
        for (a, b, c) in channels:
            i = -c                          # author cell relative to centre
            if occ(i) and occ(i + a) and not occ(i + b):
                hits += 1
        tog = (hits & 1) if mode == "parity" else (1 if hits else 0)
        tab.append(occ(0) ^ tog)
    return tab


def decide(channels, W, p, d, mode="parity", cap=4_000_000):
    """Exact, width-unbounded decision of 'is there a glider with F^p = sigma^d?'.

    Returns (verdict, witness) with verdict in {'GLIDER', 'NONE', 'CAP'}.
    'CAP' means the reachable state space exceeded `cap` and nothing is decided.
    witness = list of columns (ints, bit t = time t) for x = 0 .. L-1.
    """
    r = 2 * W
    tab = step_table(channels, W, mode)
    K = 2 * r                                # full columns carried in the state
    extra = max(0, d - r)                    # extra row-0 bits for the shift
    full = (1 << p) - 1

    def bit(col, t):
        return (col >> t) & 1

    # state = (tuple of K columns  v_{x-K+1..x},  tuple of `extra` row-0 bits
    #          for columns v_{x-K-extra+1 .. x-K})
    q0 = ((0,) * K, (0,) * extra)
    # BFS forward; parent map for witness reconstruction
    seen = {q0: None}
    order = deque([q0])
    found = None
    while order:
        st = order.popleft()
        cols, olds = st
        for new in range(1 << p):
            win = cols + (new,)              # v_{x-K+1 .. x+1}; centre y = x+1-r
            # centre column index inside `win`: win has K+1 = 2r+1 entries,
            # centre is win[r].
            centre = win[r]
            ok = True
            for t in range(p):
                idx = 0
                for j in range(2 * r + 1):
                    idx |= bit(win[j], t) << j
                    # win[j] is cell (centre-r + j)  ->  bit j of the window
                nb = tab[idx]
                if t + 1 < p:
                    want = bit(centre, t + 1)
                else:
                    # c_p(y) must equal c_0(y-d); y = index r inside win,
                    # so y-d is index r-d, which is >= 0 iff d <= r.
                    if d <= r:
                        want = bit(win[r - d], 0)
                    else:
                        want = olds[extra - (d - r)]
                if nb != want:
                    ok = False
                    break
            if not ok:
                continue
            ncols = cols[1:] + (new,)
            nolds = (olds[1:] + (cols[0] & 1,)) if extra else ()
            nst = (ncols, nolds)
            if nst in seen:
                continue
            seen[nst] = (st, new)
            if len(seen) > cap:
                return "CAP", None
            order.append(nst)
    # reconstruct: any path q0 -> ... -> q0 with a non-zero column.
    # BFS above stops at q0 being re-seen (it is the start).  Redo with an
    # explicit search for a return to q0.
    return _search_cycle(tab, W, p, d, cap)


def _search_cycle(tab, W, p, d, cap):
    """DFS/BFS for a non-trivial path q0 -> q0 (the glider itself)."""
    r = 2 * W
    K = 2 * r
    extra = max(0, d - r)
    q0 = ((0,) * K, (0,) * extra)

    def bit(col, t):
        return (col >> t) & 1

    def succs(st):
        cols, olds = st
        out = []
        for new in range(1 << p):
            win = cols + (new,)
            centre = win[r]
            ok = True
            for t in range(p):
                idx = 0
                for j in range(2 * r + 1):
                    idx |= bit(win[j], t) << j
                nb = tab[idx]
                if t + 1 < p:
                    want = bit(centre, t + 1)
                elif d <= r:
                    want = bit(win[r - d], 0)
                else:
                    want = olds[extra - (d - r)]
                if nb != want:
                    ok = False
                    break
            if ok:
                out.append((new, (cols[1:] + (new,),
                                  (olds[1:] + (cols[0] & 1,)) if extra else ())))
        return out

    # forward BFS from q0 through states reached by placing at least one
    # non-zero column, looking for a return to q0.
    start = []
    for new, ns in succs(q0):
        if new != 0:
            start.append((ns, [new]))
    seen = {q0: 0}
    dq = deque(start)
    for ns, path in start:
        seen[ns] = 1
    while dq:
        st, path = dq.popleft()
        for new, ns in succs(st):
            if ns == q0:
                return "GLIDER", path + [new]
            if ns in seen:
                continue
            seen[ns] = 1
            if len(seen) > cap:
                return "CAP", None
            dq.append((ns, path + [new]))
    return "NONE", None


def witness_state(cols, p):
    """Turn a witness column list into the t=0 occupied-cell set."""
    return sorted(x for x, col in enumerate(cols) if col & 1)


def verify(channels, cols, p, d, mode="parity", n=None):
    """Re-verify a witness with the reference engine."""
    import xnomos
    n = n or len(channels)
    cells = witness_state(cols, p)
    if not cells:
        return False
    mask = (1 << n) - 1
    S = {c: mask for c in cells}
    Cn = xnomos.Const([tuple(ch) for ch in channels],
                      [tuple(range(n))] * n)
    return xnomos.verify_glider(S, Cn, p, d, mode)


if __name__ == "__main__":
    # self-test: the n=2, W=1 speed-2/5 glider must be found, and TANDEM-1.
    for chans, p, d, mode, want in [
            ([(0, 1, -1), (0, -1, 1)], 5, 2, "parity", "GLIDER"),
            ([(0, -1, 1), (0, -1, 0)], 1, 1, "parity", "GLIDER"),
            ([(0, 1, -1), (0, -1, 1)], 5, 2, "or", "NONE"),
            ([(0, 1, -1), (0, -1, 1)], 3, 1, "parity", None),
            ([(0, 1, -1), (0, -1, 1)], 4, 3, "parity", None)]:
        v, w = _search_cycle(step_table(chans, 1, mode), 1, p, d, 4_000_000)
        ok = verify(chans, w, p, d, mode) if v == "GLIDER" else None
        print(chans, "p=%d d=%d %s" % (p, d, mode), "->", v,
              "cells=%s" % (witness_state(w, p) if w else None),
              "verified=%s" % ok, "(want %s)" % want)
