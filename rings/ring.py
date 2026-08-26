#!/usr/bin/env python3
"""Nomic ring engine (Expedition N-C).

State on ring Z/m: tuple of m ints, each a 27-bit mask of law-kinds present.
Kind index k = 9*(a+1) + 3*(b+1) + (c+1), offsets a,b,c in {-1,0,1}.
Law (i,k) ACTIVE iff occ(i+a) and not occ(i+b) (mod m); active law toggles
bit k at position i+c (mod m). Parity resolution.

STRUCTURAL FACT (Single-Author Lemma, proved in RESULTS.md): the toggle
multiset never has multiplicity > 1 -- kind determines c, so the only law
that can ever toggle slot (j,k) is the kind-k law at j-c.  Hence parity
resolution == OR resolution, and a state is fixed iff NO law is active.
step_ref() asserts multiplicity <= 1 on every call.
"""
from collections import defaultdict
import random

TYPES = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]
TIDX = {t: k for k, t in enumerate(TYPES)}

# kind masks by effect offset c
KC = {c: sum(1 << k for k, (a, b, cc) in enumerate(TYPES) if cc == c) for c in (-1, 0, 1)}
KCn1, KC0, KCp1 = KC[-1], KC[0], KC[1]

# ACT3[(L<<2)|(C<<1)|R] = mask of kinds active at a cell with local occupancy
# (left,self,right) = (L,C,R).  Only meaningful when C=1 (a law must sit there).
ACT3 = [0] * 8
for L in (0, 1):
    for C in (0, 1):
        for R in (0, 1):
            occ = {-1: L, 0: C, 1: R}
            msk = 0
            for k, (a, b, c) in enumerate(TYPES):
                if occ[a] == 1 and occ[b] == 0:
                    msk |= 1 << k
            ACT3[(L << 2) | (C << 1) | R] = msk


def step(s):
    """One synchronous step. s: tuple of m ints. Returns new tuple."""
    m = len(s)
    act = [0] * m
    for i in range(m):
        v = s[i]
        if v:
            loc = ((1 if s[i - 1] else 0) << 2) | 2 | (1 if s[(i + 1) % m] else 0)
            act[i] = v & ACT3[loc]
    return tuple(
        s[j] ^ ((act[(j + 1) % m] & KCn1) ^ (act[j] & KC0) ^ (act[j - 1] & KCp1))
        for j in range(m)
    )


def step_ref(s):
    """Reference step: per-law loop, mod-m, checks toggle multiplicity <= 1."""
    m = len(s)
    occ = [1 if v else 0 for v in s]
    contrib = defaultdict(int)
    for i in range(m):
        v = s[i]
        k = 0
        while v:
            if v & 1:
                a, b, c = TYPES[k]
                if occ[(i + a) % m] and not occ[(i + b) % m]:
                    contrib[((i + c) % m, k)] += 1
            v >>= 1
            k += 1
    assert all(x == 1 for x in contrib.values()), "multiplicity>1: Single-Author Lemma violated!"
    out = list(s)
    for (j, k), _ in contrib.items():
        out[j] ^= 1 << k
    return tuple(out)


def active_count(s):
    m = len(s)
    n = 0
    for i in range(m):
        if s[i]:
            loc = ((1 if s[i - 1] else 0) << 2) | 2 | (1 if s[(i + 1) % m] else 0)
            n += bin(s[i] & ACT3[loc]).count("1")
    return n


def nlaws(s):
    return sum(bin(v).count("1") for v in s)


def occ_count(s):
    return sum(1 for v in s if v)


def run_to_attractor(s, budget=50000):
    """Iterate with full hashing. Returns (kind, transient, period, attr_state, steps_used)
    kind in {'extinct','fixed','cycle','holdout'};  attr_state = first state of attractor."""
    seen = {}
    t = 0
    cur = s
    while t <= budget:
        if cur in seen:
            t0 = seen[cur]
            period = t - t0
            if period == 1 or cur == step(cur):
                pass
            if all(v == 0 for v in cur):
                return ("extinct", t0, 1, cur, t)
            if period == 1:
                return ("fixed", t0, 1, cur, t)
            return ("cycle", t0, period, cur, t)
        if all(v == 0 for v in cur):
            return ("extinct", t, 1, cur, t)
        seen[cur] = t
        cur = step(cur)
        t += 1
    return ("holdout", budget, 0, cur, t)


def cycle_states(s, period):
    """Return the list of states of the cycle through s."""
    out = [s]
    cur = step(s)
    while cur != s:
        out.append(cur)
        cur = step(cur)
    assert len(out) == period
    return out


def random_state(m, lam, rng):
    """Each of the 27m slots present independently with prob lam/27."""
    p = lam / 27.0
    s = []
    for _ in range(m):
        v = 0
        for k in range(27):
            if rng.random() < p:
                v |= 1 << k
        s.append(v)
    return tuple(s)


def render(s):
    """One-line render: per cell '.' or law count (hex-ish)."""
    out = []
    for v in s:
        n = bin(v).count("1")
        out.append("." if n == 0 else (str(n) if n < 10 else "#"))
    return "".join(out)


def state_repr(s):
    """Explicit law list [(pos,(a,b,c)),...]."""
    laws = []
    for i, v in enumerate(s):
        k = 0
        while v:
            if v & 1:
                laws.append((i, TYPES[k]))
            v >>= 1
            k += 1
    return laws


def from_laws(m, laws):
    s = [0] * m
    for i, t in laws:
        s[i % m] |= 1 << TIDX[t]
    return tuple(s)


if __name__ == "__main__":
    # self-test: fast step == reference step on random states, all m
    rng = random.Random(1)
    for m in (1, 2, 3, 4, 5, 8, 13):
        for trial in range(300):
            lam = rng.choice([0.1, 0.5, 1, 3, 9, 27])
            s = random_state(m, lam, rng)
            assert step(s) == step_ref(s), (m, s)
    # fixed <=> no active law (Dead Letter theorem, empirical spot check)
    for m in (2, 3, 4, 6):
        for trial in range(2000):
            s = random_state(m, rng.choice([0.2, 1, 5, 20]), rng)
            fixed = step(s) == s
            assert fixed == (active_count(s) == 0), (m, s)
    # gridlock: full occupancy is frozen
    for m in (1, 2, 5, 9):
        for trial in range(200):
            s = tuple(rng.randrange(1, 1 << 27) for _ in range(m))
            assert step(s) == s
    print("ring.py self-tests OK: fast==ref, multiplicity<=1 everywhere,")
    print("fixed <=> zero active laws, full occupancy frozen.")
