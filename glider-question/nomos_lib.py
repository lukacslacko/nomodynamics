#!/usr/bin/env python3
"""nomos_lib.py — Expedition N-A (glider question) engines.

State: dict {position(int) -> bitmask over kinds}.  Kind index for window W:
    k = (a+W)*(2W+1)^2 + (b+W)*(2W+1) + (c+W),   offsets a,b,c in {-W..W}.
Law (i,k) is ACTIVE iff cell i+a is occupied (any kind) and cell i+b is empty.
Each active law emits one toggle of ITS OWN KIND at cell i+c.  Synchronous.

Resolution semantics:
  parity : per-(cell,kind) toggle counts accumulate by XOR.
  or     : per-(cell,kind) target flips once regardless of actor count (OR).
  (Lemma: two same-kind actors at i != i' have targets i+c != i'+c, so the
   per-(cell,kind) actor count is always <= 1 and the two semantics coincide
   identically.  The duel classifier machine-checks this step-for-step.)

Variant engine (for the sharpness section):
  supersession : active law with target j=i+c ENACTS its own kind if j is
  empty, and CLEARS THE ENTIRE CELL (all kinds) if j is occupied.  This is the
  minimal cross-kind-effect variant; the anchor argument does not apply to it.
"""
import itertools
from collections import Counter

# ---------------------------------------------------------------- tables

def build_tables(W):
    R = 2 * W + 1
    TYPES = [(a, b, c) for a in range(-W, W + 1)
             for b in range(-W, W + 1) for c in range(-W, W + 1)]
    NT = len(TYPES)
    ACTIVE = [0] * (1 << R)          # nu bit k  <->  occ(i - W + k); center always set
    for nu in range(1 << R):
        if not (nu >> W) & 1:
            continue
        m = 0
        for k, (a, b, c) in enumerate(TYPES):
            if (nu >> (a + W)) & 1 and not ((nu >> (b + W)) & 1):
                m |= 1 << k
        ACTIVE[nu] = m
    CLIST = []
    for c in range(-W, W + 1):
        cm = 0
        for k, (a, b, cc) in enumerate(TYPES):
            if cc == c:
                cm |= 1 << k
        CLIST.append((c, cm))
    return TYPES, NT, ACTIVE, CLIST


# ---------------------------------------------------------------- steppers

def make_step(W, mode):
    """mode in {'parity','or'}.  Returns step(S)->S'. May return S itself if fixed."""
    TYPES, NT, ACTIVE, CLIST = build_tables(W)
    R = 2 * W + 1
    xor = (mode == "parity")

    if W == 1:
        CMn = CLIST[0][1]; CM0 = CLIST[1][1]; CMp = CLIST[2][1]
        ACT = ACTIVE
        def step(S):
            tog = {}
            g = tog.get
            for i, m in S.items():
                nu = 2
                if (i - 1) in S: nu |= 1
                if (i + 1) in S: nu |= 4
                act = m & ACT[nu]
                if not act:
                    continue
                x = act & CMn
                if x:
                    j = i - 1
                    tog[j] = (g(j, 0) ^ x) if xor else (g(j, 0) | x)
                x = act & CM0
                if x:
                    tog[i] = (g(i, 0) ^ x) if xor else (g(i, 0) | x)
                x = act & CMp
                if x:
                    j = i + 1
                    tog[j] = (g(j, 0) ^ x) if xor else (g(j, 0) | x)
            if not tog:
                return S
            out = dict(S)
            for j, x in tog.items():
                nm = out.get(j, 0) ^ x
                if nm:
                    out[j] = nm
                else:
                    out.pop(j, None)
            return out
        return step

    ACT = ACTIVE
    def step(S):
        tog = {}
        g = tog.get
        for i, m in S.items():
            nu = 0
            base = i - W
            for k in range(R):
                if (base + k) in S:
                    nu |= 1 << k
            act = m & ACT[nu]
            if not act:
                continue
            for c, cm in CLIST:
                x = act & cm
                if x:
                    j = i + c
                    tog[j] = (g(j, 0) ^ x) if xor else (g(j, 0) | x)
        if not tog:
            return S
        out = dict(S)
        for j, x in tog.items():
            nm = out.get(j, 0) ^ x
            if nm:
                out[j] = nm
            else:
                out.pop(j, None)
        return out
    return step


def make_step_supersession(W):
    """Cross-kind variant: enact own kind into empty target; clear occupied target cell."""
    TYPES, NT, ACTIVE, CLIST = build_tables(W)
    R = 2 * W + 1
    def step(S):
        clear = set()
        enact = {}
        for i, m in S.items():
            nu = 0
            base = i - W
            for k in range(R):
                if (base + k) in S:
                    nu |= 1 << k
            act = m & ACTIVE[nu]
            if not act:
                continue
            for c, cm in CLIST:
                x = act & cm
                if not x:
                    continue
                j = i + c
                if j in S:
                    clear.add(j)
                else:
                    enact[j] = enact.get(j, 0) | x
        if not clear and not enact:
            return S
        out = {}
        for j, m in S.items():
            if j not in clear:
                out[j] = m
        for j, x in enact.items():
            out[j] = x            # j was empty; no conflict with clear
        return out
    return step


# ---------------------------------------------------------------- classify

def _size(S):
    n = 0
    for v in S.values():
        n += v.bit_count()
    return n


def verify_glider(S, step, p, d, reps=3):
    """Check Phi^p == shift-by-d, applied reps times starting from S."""
    T = dict(S)
    for _ in range(reps):
        U = dict(T)
        for _ in range(p):
            U = step(U)
        want = sorted((i + d, v) for i, v in T.items())
        if want != sorted(U.items()):
            return False
        T = U
    return True


def classify(S0, step, step2=None, max_steps=2000, hash_cap=150,
             growth_cap=3000, width_stop=320, verify_gliders=True):
    """Certified classification.  If step2 given: lockstep duel — advance both
    engines, assert state equality every step (machine check parity==OR).
    Returns (verdict, t, info).  Verdicts:
      extinct, fixed, cycle, glider, big-growth, slow-holdout,
      anomaly (glider recurrence failed 3-period re-verify — engine bug),
      divergence (duel states differed — refutes the collision lemma).
    big-growth 'why': 'size-cap' (size>growth_cap, certificate by cutoff) or
    'sustained-width' (evidence: 3 consecutive 100-step blocks with strictly
    increasing block-min width, current width>width_stop; a pattern of bounded
    width can never satisfy this).
    """
    S = dict(S0)
    T = dict(S0) if step2 is not None else None
    seen = {}
    blocks = []
    cur_bw = None
    sz = width = 0
    for t in range(max_steps):
        if not S:
            return ("extinct", t, None)
        sz = _size(S)
        if sz > growth_cap:
            return ("big-growth", t, {"size": sz, "why": "size-cap"})
        mn = min(S); mx = max(S); width = mx - mn + 1
        if cur_bw is None or width < cur_bw:
            cur_bw = width
        if t % 100 == 99:
            blocks.append(cur_bw)
            cur_bw = None
            if (width > width_stop and len(blocks) >= 3
                    and blocks[-1] > blocks[-2] > blocks[-3]):
                return ("big-growth", t,
                        {"size": sz, "width": width, "why": "sustained-width",
                         "blocks": blocks[-3:]})
        if sz <= hash_cap:
            key = tuple(sorted((i - mn, v) for i, v in S.items()))
            hit = seen.get(key)
            if hit is not None:
                t0, mn0 = hit
                p, d = t - t0, mn - mn0
                if d == 0:
                    return (("fixed" if p == 1 else "cycle"), t0,
                            {"period": p, "transient": t0})
                cert = {"period": p, "disp": d, "size": sz, "onset": t0}
                if verify_gliders:
                    cert["verified3p"] = verify_glider(S, step, p, d, 3)
                    if not cert["verified3p"]:
                        return ("anomaly", t, cert)
                return ("glider", t0, cert)
            seen[key] = (t, mn)
        S = step(S)
        if T is not None:
            T = step2(T)
            if S != T:
                return ("divergence", t + 1,
                        {"parity": sorted(S.items()), "or": sorted(T.items())})
    return ("slow-holdout", max_steps, {"size": sz, "width": width})


# ---------------------------------------------------------------- seeds

def seed_from_slots(slots, NT):
    S = {}
    for s in slots:
        p, k = divmod(s, NT)
        m = S.get(p, 0)
        S[p] = m | (1 << k)
    return S


def gen_canonical(NT, npos, k, first_lo=0, first_hi=None):
    """All k-subsets of slot-space (npos positions x NT kinds, position-major)
    whose minimum position is 0, i.e. first slot < NT.  Optionally restrict the
    first slot to [first_lo, first_hi) for work-unit splitting."""
    nslots = npos * NT
    if first_hi is None:
        first_hi = NT
    for first in range(first_lo, min(first_hi, NT)):
        if k == 1:
            yield (first,)
        else:
            for rest in itertools.combinations(range(first + 1, nslots), k - 1):
                yield (first,) + rest


def count_canonical(NT, npos, k):
    import math
    return math.comb(npos * NT, k) - math.comb((npos - 1) * NT, k)


# ---------------------------------------------------------------- verification

def check_anchor_invariants(S0, step, TYPES, steps=300):
    """Machine check of the Anchor Theorem invariants along one trajectory:
      c>0: leftmost cell of the kind's support is constant while kind lives;
      c<0: rightmost constant;  c=0: support never gains a cell;
      any kind, once extinct, never reappears.
    Returns None if all hold, else a violation record."""
    S = dict(S0)
    mins = {}; maxs = {}; supp0 = {}; dead = set()
    for t in range(steps):
        if not S:
            break
        cur = {}
        for i, m in S.items():
            mm = m
            while mm:
                k = (mm & -mm).bit_length() - 1
                mm &= mm - 1
                lo, hi = cur.get(k, (i, i))
                cur[k] = (min(lo, i), max(hi, i))
        for k, (lo, hi) in cur.items():
            if k in dead:
                return {"violation": "kind-reborn", "kind": TYPES[k], "t": t}
            a, b, c = TYPES[k]
            if k not in mins:
                mins[k] = lo; maxs[k] = hi
                if c == 0:
                    supp0[k] = {i for i, m in S.items() if (m >> k) & 1}
            else:
                if c > 0 and lo != mins[k]:
                    return {"violation": "left-anchor-moved", "kind": TYPES[k],
                            "t": t, "was": mins[k], "now": lo}
                if c < 0 and hi != maxs[k]:
                    return {"violation": "right-anchor-moved", "kind": TYPES[k],
                            "t": t, "was": maxs[k], "now": hi}
                if c == 0:
                    cs = {i for i, m in S.items() if (m >> k) & 1}
                    if not cs <= supp0[k]:
                        return {"violation": "c0-support-grew", "kind": TYPES[k],
                                "t": t}
                    supp0[k] = cs
        for k in list(mins):
            if k not in cur:
                dead.add(k)
        S = step(S)
    return None


def max_actor_multiplicity(S, W):
    """Instrumented single step: per-(target,kind) actor count. Lemma says <=1."""
    TYPES, NT, ACTIVE, CLIST = build_tables(W)
    R = 2 * W + 1
    mult = Counter()
    for i, m in S.items():
        nu = 0
        for k in range(R):
            if (i - W + k) in S:
                nu |= 1 << k
        act = m & ACTIVE[nu]
        mm = act
        while mm:
            k = (mm & -mm).bit_length() - 1
            mm &= mm - 1
            c = TYPES[k][2]
            mult[(i + c, k)] += 1
    return max(mult.values()) if mult else 0


# ---------------------------------------------------------------- display

def spacetime(S0, step, steps, lo, hi, kind_letter=None):
    """ASCII spacetime diagram; kind_letter: optional {kindindex: char}."""
    rows = []
    S = dict(S0)
    for t in range(steps):
        row = []
        for i in range(lo, hi + 1):
            v = S.get(i, 0)
            n = v.bit_count()
            if n == 0:
                row.append(".")
            elif kind_letter and n == 1:
                k = (v & -v).bit_length() - 1
                row.append(kind_letter.get(k, "1"))
            else:
                row.append(str(n) if n < 10 else "#")
        rows.append("".join(row))
        S = step(S)
    return rows
