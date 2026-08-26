#!/usr/bin/env python3
"""nomos2d/engine2d.py -- 2D nomodynamics core engine (Expedition N-B).

State: finite set of placed laws (p, T), p in Z^2, T=(a,b,c) in N^3 with
N = von Neumann offset set {O,E,W,N,S} = {(0,0),(1,0),(-1,0),(0,1),(0,-1)}.
125 law-types.  Law (p,(a,b,c)) is ACTIVE iff cell p+a is occupied (by any
law) and cell p+b is empty.  Every active law toggles the presence of ITS
OWN KIND at p+c.  Synchronous update.  Two resolution semantics requested:
PARITY (xor of toggle multiplicities) and OR-toggle (any toggle -> one flip).

LEMMA 1 (single-author lemma): the only law that can ever toggle the pair
(q, T) is the law (q - c_T, T); a type has one c-offset and at most one law
of a given type stands at a given cell, so every toggle multiplicity is 0
or 1 and PARITY and OR semantics are *identical* dynamics.  Both are
implemented and cross-checked anyway (see selftest).

THEOREM 2 (type conservation): laws only toggle their own kind, so the set
of types present never grows: types(S_t) subseteq types(S_0).

Positions are encoded as single ints p = x*M + y (M = 2^21) in the hot path.
"""
import sys
from collections import defaultdict

M = 1 << 21
H = M >> 1

OFFI = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]   # O E W N S
LET = "OEWNS"
DOFF = [0, M, -M, 1, -1]                              # encoded deltas
K = 125
TYPES = [(ia, ib, ic) for ia in range(5) for ib in range(5) for ic in range(5)]
# k = 25*ia + 5*ib + ic

def tname(k):
    ia, ib, ic = TYPES[k]
    return LET[ia] + LET[ib] + LET[ic]

def tparse(name):
    ia, ib, ic = (LET.index(ch) for ch in name.upper())
    return 25 * ia + 5 * ib + ic

# ACT[pat]: 125-bit mask of active types given 5-bit neighborhood occupancy
# pattern (bit i = OFFI[i] occupied; bit 0 (self) always 1 for a law cell).
ACT = []
for pat in range(32):
    m = 0
    for k, (ia, ib, ic) in enumerate(TYPES):
        if (pat >> ia) & 1 and not ((pat >> ib) & 1):
            m |= 1 << k
    ACT.append(m)

# c-dispatch groups
CG = [0] * 5
for k, (ia, ib, ic) in enumerate(TYPES):
    CG[ic] |= 1 << k
CG0, CG1, CG2, CG3, CG4 = CG


def enc(x, y):
    return x * M + y

def dec(p):
    q, r = divmod(p + H, M)
    return q, r - H

def to_state(spec):
    """spec: iterable of ((x,y), k) -> encoded state dict p->mask."""
    S = {}
    for (x, y), k in spec:
        p = enc(x, y)
        S[p] = S.get(p, 0) | (1 << k)
    return S

def spec_str(spec):
    return " ".join(f"({x},{y}){tname(k)}" for (x, y), k in spec)


def step_p(S):
    """Parity semantics.  Returns the SAME object if nothing is active."""
    tog = {}
    tg = tog.get
    A = ACT
    for p, mask in S.items():
        pat = 1
        if p + M in S: pat |= 2
        if p - M in S: pat |= 4
        if p + 1 in S: pat |= 8
        if p - 1 in S: pat |= 16
        act = mask & A[pat]
        if not act:
            continue
        m = act & CG0
        if m: tog[p] = tg(p, 0) ^ m
        m = act & CG1
        if m:
            q = p + M; tog[q] = tg(q, 0) ^ m
        m = act & CG2
        if m:
            q = p - M; tog[q] = tg(q, 0) ^ m
        m = act & CG3
        if m:
            q = p + 1; tog[q] = tg(q, 0) ^ m
        m = act & CG4
        if m:
            q = p - 1; tog[q] = tg(q, 0) ^ m
    if not tog:
        return S
    out = dict(S)
    for q, m in tog.items():
        nm = out.get(q, 0) ^ m
        if nm:
            out[q] = nm
        else:
            del out[q]
    return out


def step_o(S):
    """OR-toggle semantics (provably identical to parity; kept as cross-check)."""
    tog = {}
    tg = tog.get
    A = ACT
    for p, mask in S.items():
        pat = 1
        if p + M in S: pat |= 2
        if p - M in S: pat |= 4
        if p + 1 in S: pat |= 8
        if p - 1 in S: pat |= 16
        act = mask & A[pat]
        if not act:
            continue
        m = act & CG0
        if m: tog[p] = tg(p, 0) | m
        m = act & CG1
        if m:
            q = p + M; tog[q] = tg(q, 0) | m
        m = act & CG2
        if m:
            q = p - M; tog[q] = tg(q, 0) | m
        m = act & CG3
        if m:
            q = p + 1; tog[q] = tg(q, 0) | m
        m = act & CG4
        if m:
            q = p - 1; tog[q] = tg(q, 0) | m
    if not tog:
        return S
    out = dict(S)
    for q, m in tog.items():
        nm = out.get(q, 0) ^ m
        if nm:
            out[q] = nm
        else:
            del out[q]
    return out


STEP = {"p": step_p, "o": step_o}

def sizeof(S):
    return sum(v.bit_count() for v in S.values())

def cellsof(S):
    return len(S)

def decode_state(S):
    return [(*dec(p), m) for p, m in S.items()]

def state_hw(S):
    hw = 0
    for p in S:
        x, y = dec(p)
        r = abs(x)
        if abs(y) > r:
            r = abs(y)
        if r > hw:
            hw = r
    return hw


# ---------------- D4 symmetry machinery ----------------------------------
# Group elements g = (r, m): position map z -> rot90ccw^r ( mirror^m (z) ),
# mirror = (x,y)->(x,-y), rot = (x,y)->(-y,x).  Types transform alongside.
RPERM = [0, 3, 4, 2, 1]   # OFF index perm under rot90 ccw
MPERM = [0, 1, 2, 4, 3]   # under mirror y->-y
GROUP = [(r, m) for m in (0, 1) for r in range(4)]  # gi = m*4 + r
GID = {g: i for i, g in enumerate(GROUP)}

def _offperm(gi):
    r, m = GROUP[gi]
    perm = list(MPERM) if m else list(range(5))
    for _ in range(r):
        perm = [RPERM[i] for i in perm]
    return perm

OFFPERM = [_offperm(gi) for gi in range(8)]
TPERM = []
for gi in range(8):
    P = OFFPERM[gi]
    TPERM.append([25 * P[ia] + 5 * P[ib] + P[ic] for (ia, ib, ic) in TYPES])

def posmap(gi, x, y):
    r, m = GROUP[gi]
    if m:
        y = -y
    for _ in range(r):
        x, y = -y, x
    return x, y

def maskperm(mask, gi):
    T = TPERM[gi]
    out = 0
    while mask:
        low = mask & -mask
        out |= 1 << T[low.bit_length() - 1]
        mask ^= low
    return out

def g_compose(g1, g2):
    """Element of g1 o g2 (apply g2 first)."""
    r1, m1 = GROUP[g1]
    r2, m2 = GROUP[g2]
    if m1 == 0:
        return GID[((r1 + r2) % 4, m2)]
    return GID[((r1 - r2) % 4, 1 ^ m2)]

def g_inv(g):
    r, m = GROUP[g]
    if m == 0:
        return GID[((-r) % 4, 0)]
    return g

def transform_cells(cells, gi):
    return [(*posmap(gi, x, y), maskperm(mk, gi)) for (x, y, mk) in cells]

def canon_cells(cells):
    cx = min(c[0] for c in cells)
    cy = min(c[1] for c in cells)
    key = tuple(sorted((x - cx, y - cy, mk) for (x, y, mk) in cells))
    return key, cx, cy

def transform_state(S, gi, v=(0, 0)):
    """Apply group element gi then translate by v; re-encode."""
    out = {}
    vx, vy = v
    for p, mk in S.items():
        x, y = dec(p)
        x2, y2 = posmap(gi, x, y)
        q = enc(x2 + vx, y2 + vy)
        out[q] = out.get(q, 0) | maskperm(mk, gi)
    return out


# ---------------- classification with certificates ------------------------

def _resolve_d4(cands1, cands0):
    """cands: list of (gi, cx, cy) with T_g(S)-corner equal as canonical reps.
    S1 = h(S0) + v with h = g1^-1 g0, v = L_{g1^-1}(corner1 - corner0)."""
    hs = {}
    for (g1, ax, ay) in cands1:
        gi1 = g_inv(g1)
        for (g0, bx, by) in cands0:
            h = g_compose(gi1, g0)
            vx, vy = posmap(gi1, ax - bx, ay - by)
            hs.setdefault(h, (vx, vy))
    return hs


def classify(spec, sem="p", max_steps=256, growth_cap=1200, hash_cap=240,
             d4_cap=96, want_sizes=False, hw_cap=None, light_hash=False):
    """Run with certificate detection.

    Verdicts:
      extinct(t) | fixed(t) | cycle(t0,p) | glider(t0,p,d) |
      rotor(t0,p,dr)  [recurs modulo 90/180/270 rotation] |
      glide(t0,p,g,v,net) [recurs modulo reflection; net = drift per 2p] |
      growth(t,sz,hw) | unresolved(t,sz,hw,trend)
    """
    step = STEP[sem]
    S = to_state(spec)
    seen = {}
    seend4 = {}
    sizes = []
    hw = 0
    t = 0
    while True:
        if not S:
            return dict(v="extinct", t=t, hw=hw,
                        sizes=sizes if want_sizes else None)
        sz = sizeof(S)
        sizes.append(sz)
        if (t & 15) == 0:
            w = state_hw(S)
            if w > hw:
                hw = w
            if hw_cap is not None and hw > hw_cap:
                return dict(v="sprawl", t=t, sz=sz, hw=hw,
                            sizes=sizes if want_sizes else None)
        if sz > growth_cap:
            return dict(v="growth", t=t, sz=sz, hw=max(hw, state_hw(S)),
                        sizes=sizes if want_sizes else None)
        if sz <= hash_cap:
            cells = decode_state(S)
            key, cx, cy = canon_cells(cells)
            if light_hash:
                key = hash(key)
            hit = seen.get(key)
            if hit is not None:
                t0, cx0, cy0 = hit
                p = t - t0
                dx, dy = cx - cx0, cy - cy0
                if dx == 0 and dy == 0:
                    return dict(v="cycle", t0=t0, p=p, sz=sz,
                                sizes=sizes if want_sizes else None)
                return dict(v="glider", t0=t0, p=p, d=(dx, dy), sz=sz,
                            sizes=sizes if want_sizes else None)
            seen[key] = (t, cx, cy)
            if sz <= d4_cap:
                reps = []
                for gi in range(8):
                    k2, a, b = canon_cells(transform_cells(cells, gi))
                    reps.append((k2, gi, a, b))
                mkey = min(r[0] for r in reps)
                cands = [(gi, a, b) for (k2, gi, a, b) in reps if k2 == mkey]
                hit = seend4.get(mkey)
                if hit is not None:
                    t0, cands0 = hit
                    hs = _resolve_d4(cands, cands0)
                    p = t - t0
                    if 0 in hs:  # identity (should have been caught above)
                        vx, vy = hs[0]
                        if (vx, vy) != (0, 0):
                            return dict(v="glider", t0=t0, p=p, d=(vx, vy),
                                        sz=sz, sizes=sizes if want_sizes else None)
                        return dict(v="cycle", t0=t0, p=p, sz=sz,
                                    sizes=sizes if want_sizes else None)
                    rots = sorted(GROUP[h][0] for h in hs if GROUP[h][1] == 0)
                    if rots:
                        dr = rots[0]
                        h = GID[(dr, 0)]
                        return dict(v="rotor", t0=t0, p=p, dr=dr, vv=hs[h],
                                    sz=sz, sizes=sizes if want_sizes else None)
                    h = min(hs)
                    vx, vy = hs[h]
                    lx, ly = posmap(h, vx, vy)
                    net = (vx + lx, vy + ly)
                    return dict(v="glide", t0=t0, p=p, g=GROUP[h], vv=(vx, vy),
                                net=net, sz=sz,
                                sizes=sizes if want_sizes else None)
                else:
                    seend4[mkey] = (t, cands)
        if t >= max_steps:
            n = len(sizes)
            a, b = sizes[-1], max(1, sizes[n // 2])
            trend = "grow" if (a >= 60 and a >= 1.6 * b) else "flat"
            return dict(v="unresolved", t=t, sz=sz, hw=max(hw, state_hw(S)),
                        trend=trend, sizes=sizes if want_sizes else None)
        S2 = step(S)
        if S2 is S:
            return dict(v="fixed", t=t, sz=sz,
                        sizes=sizes if want_sizes else None)
        S = S2
        t += 1


def run_state(spec, sem="p", T=0):
    step = STEP[sem]
    S = to_state(spec)
    for _ in range(T):
        S = step(S)
    return S


def verify_recurrence(spec, sem, t0, p, gi, v):
    """Exact certificate check: S_{t0+p} == g(S_{t0}) + v."""
    S0 = run_state(spec, sem, t0)
    S1 = S0
    step = STEP[sem]
    for _ in range(p):
        S1 = step(S1)
    return S1 == transform_state(S0, gi, v)


# ---------------- numpy dense engine --------------------------------------
import numpy as np

def _sh(a, dx, dy):
    """out[i,j] = a[i+dx, j+dy], zero-filled (i~x, j~y)."""
    if dx == 0 and dy == 0:
        return a
    n0, n1 = a.shape
    out = np.zeros_like(a)
    i0, i1 = max(0, -dx), min(n0, n0 - dx)
    j0, j1 = max(0, -dy), min(n1, n1 - dy)
    if i0 < i1 and j0 < j1:
        out[i0:i1, j0:j1] = a[i0 + dx:i1 + dx, j0 + dy:j1 + dy]
    return out


def np_run(spec, T, sem="p", R=None, snaps=(), stop_at_edge=True):
    """Dense multi-plane run.  Returns dict with sizes[t], snapshot states
    (decoded to sparse dicts) at requested times, final planes and extent.
    sem is accepted for interface parity; dynamics identical (Lemma 1)."""
    ks = sorted({k for _, k in spec})
    ext = max((max(abs(x), abs(y)) for (x, y), _ in spec), default=0)
    if R is None:
        R = T + ext + 3
    n = 2 * R + 1
    planes = {k: np.zeros((n, n), dtype=bool) for k in ks}
    for (x, y), k in spec:
        planes[k][x + R, y + R] = True
    sizes = []
    snapd = {}
    snaps = set(snaps)
    truncated = None
    for t in range(T + 1):
        occ = None
        for pl in planes.values():
            occ = pl.copy() if occ is None else (occ | pl)
        sizes.append(int(sum(int(pl.sum()) for pl in planes.values())))
        if t in snaps:
            snapd[t] = {k: [(int(i) - R, int(j) - R)
                            for i, j in np.argwhere(pl)]
                        for k, pl in planes.items()}
        if t == T:
            break
        if stop_at_edge:
            edge = (occ[0, :].any() or occ[-1, :].any() or
                    occ[:, 0].any() or occ[:, -1].any())
            if edge:
                truncated = t
                break
        new = {}
        for k, pl in planes.items():
            ia, ib, ic = TYPES[k]
            act = pl & _sh(occ, *OFFI[ia]) & ~_sh(occ, *OFFI[ib])
            cdx, cdy = OFFI[ic]
            new[k] = pl ^ _sh(act, -cdx, -cdy)
        planes = new
    occ = None
    for pl in planes.values():
        occ = pl.copy() if occ is None else (occ | pl)
    return dict(sizes=sizes, snaps=snapd, planes=planes, occ=occ, R=R,
                truncated=truncated)


def np_state(res):
    """Final dense state -> sparse spec-state dict (encoded)."""
    R = res["R"]
    S = {}
    for k, pl in res["planes"].items():
        for i, j in np.argwhere(pl):
            p = enc(int(i) - R, int(j) - R)
            S[p] = S.get(p, 0) | (1 << k)
    return S


# ---------------- rendering ------------------------------------------------

def render(S, legend=None, pad=1, maxw=78, maxh=48, scale=None):
    """ASCII render of sparse state dict (north = up).  legend: k->char."""
    if not S:
        return "(empty)"
    cells = decode_state(S)
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    x0, x1 = min(xs) - pad, max(xs) + pad
    y0, y1 = min(ys) - pad, max(ys) + pad
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if scale is None:
        scale = max(1, (w + maxw - 1) // maxw, (h + maxh - 1) // maxh)
    if legend is None:
        ks = sorted({k for (_, _, mk) in cells for k in bits(mk)})
        legend = {}
        for i, k in enumerate(ks):
            legend[k] = "#" if len(ks) == 1 else "ABCDEFGHJKLMNPQR"[i % 16]
    gw = (w + scale - 1) // scale
    gh = (h + scale - 1) // scale
    grid = [["." for _ in range(gw)] for _ in range(gh)]
    for (x, y, mk) in cells:
        gx = (x - x0) // scale
        gy = (y - y0) // scale
        row = gh - 1 - gy
        ch = grid[row][gx]
        kk = list(bits(mk))
        c = legend[kk[0]] if len(kk) == 1 else "&"
        if ch == ".":
            grid[row][gx] = c
        elif ch != c:
            grid[row][gx] = "&"
    hdr = f"[x {x0}..{x1}, y {y0}..{y1}" + (f", 1 char = {scale}x{scale}]" if scale > 1 else "]")
    return "\n".join("".join(r) for r in grid) + "\n" + hdr


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def render_occ(occ_cells, maxw=78, maxh=48, pad=1):
    S = {enc(x, y): 1 for x, y in occ_cells}
    return render(S, legend={0: "#"}, pad=pad, maxw=maxw, maxh=maxh)


# ---------------- self-test ------------------------------------------------

def _selftest():
    import random
    rng = random.Random(1)
    print("selftest: group algebra ...", end=" ")
    for g1 in range(8):
        for g2 in range(8):
            g12 = g_compose(g1, g2)
            for _ in range(4):
                x, y = rng.randint(-9, 9), rng.randint(-9, 9)
                assert posmap(g12, x, y) == posmap(g1, *posmap(g2, x, y))
            for k in (rng.randrange(125), rng.randrange(125)):
                m = 1 << k
                assert maskperm(maskperm(m, g2), g1) == maskperm(m, g12)
    for g in range(8):
        assert g_compose(g, g_inv(g)) == 0 and g_compose(g_inv(g), g) == 0
    print("ok")

    print("selftest: parity == OR on 400 random seeds x 120 steps ...", end=" ")
    for _ in range(400):
        spec = [((rng.randint(-1, 1), rng.randint(-1, 1)), rng.randrange(125))
                for _ in range(rng.randint(2, 3))]
        Sp = to_state(spec)
        So = to_state(spec)
        for _ in range(120):
            Sp = step_p(Sp)
            So = step_o(So)
            assert Sp == So
            if not Sp:
                break
    print("ok  (Lemma 1 confirmed empirically)")

    print("selftest: D4 equivariance of step ...", end=" ")
    for _ in range(200):
        spec = [((rng.randint(-2, 2), rng.randint(-2, 2)), rng.randrange(125))
                for _ in range(rng.randint(1, 4))]
        S = to_state(spec)
        for _ in range(rng.randint(1, 12)):
            S = step_p(S)
        g = rng.randrange(8)
        assert step_p(transform_state(S, g)) == transform_state(step_p(S), g) \
            or (step_p(transform_state(S, g)) == transform_state(S, g) and step_p(S) == S)
    print("ok")

    print("selftest: dict vs numpy engine on 60 seeds x 30 steps ...", end=" ")
    for _ in range(60):
        spec = [((rng.randint(-1, 1), rng.randint(-1, 1)), rng.randrange(125))
                for _ in range(rng.randint(1, 3))]
        S = to_state(spec)
        for _ in range(30):
            S = step_p(S)
        res = np_run(spec, 30, R=40)
        assert np_state(res) == S
    print("ok")

    print("selftest: known single-law behaviors ...", end=" ")
    v = classify([((0, 0), tparse("OEE"))], max_steps=100, growth_cap=90)
    assert v["v"] in ("growth", "unresolved")
    v = classify([((0, 0), tparse("OEW"))])
    assert v["v"] == "cycle" and v["p"] == 2
    v = classify([((0, 0), tparse("OEO"))])
    assert v["v"] == "extinct" and v["t"] == 1
    v = classify([((0, 0), tparse("EOO"))])
    assert v["v"] == "fixed"
    S = to_state([((0, 0), tparse("OEN"))])
    for _ in range(64):
        S = step_p(S)
    ys = sorted(dec(p)[1] for p in S)
    assert ys == [0, 64], ys   # Pascal: size 2^popcount(t), top cell at t
    print("ok")
    print("ALL SELFTESTS PASS")


if __name__ == "__main__":
    _selftest()
