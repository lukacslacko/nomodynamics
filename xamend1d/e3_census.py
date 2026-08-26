#!/usr/bin/env python3
"""
e3_census.py — COMPLETE census of the n=2, W=1 universes of nomodynamics.

THE BOX (exact).
  kinds      n = 2
  offsets    a,b,c in {-1,0,1}          -> 27 rules per kind, 729 rule pairs
  targets    T_k in { {0}, {1}, {0,1} } -> 9 target matrices
  universes  729 * 9 = 6561, enumerated EXHAUSTIVELY, for each of the two
             resolution modes 'parity' and 'or'  (13122 universe-runs).
  seeds      every nonempty subset of (cell,kind) with cell in a 5-cell window
             (2^10 - 1 = 1023 raw masks), translation-normalised so the
             leftmost occupied cell is 0  ->  768 distinct seeds, ALL of them.
  budget     a trajectory is abandoned as GROWING when card > MAX_CARD or
             span > MAX_SPAN, and as UNRESOLVED after MAX_STEPS steps.

The simulator here is an independent bitmask reimplementation of xnomos.step;
it is checked against xnomos.step on random universes/states by --selftest, and
every glider it reports is re-verified by xnomos.verify_glider downstream.
"""

from __future__ import annotations

import itertools
import os
import pickle
import sys

sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6/xamend1d')

OFFS = (-1, 0, 1)
RULES = [(a, b, c) for a in OFFS for b in OFFS for c in OFFS]      # 27
TSETS = [(0,), (1,), (0, 1)]                                       # 3

MAX_STEPS = 2000
MAX_CARD = 64
MAX_SPAN = 64
WINDOW = 5

DATA = '/Users/lukacs/claude/math/program/phase6/xamend1d/data'


# ----------------------------------------------------------------- seeds

def seeds_window(w=WINDOW):
    """All translation-normalised nonempty seeds inside a w-cell window."""
    out = set()
    for msk in range(1, 1 << (2 * w)):
        m0 = m1 = 0
        for i in range(w):
            if msk >> (2 * i) & 1:
                m0 |= 1 << i
            if msk >> (2 * i + 1) & 1:
                m1 |= 1 << i
        occ = m0 | m1
        lo = (occ & -occ).bit_length() - 1
        out.add((m0 >> lo, m1 >> lo))
    return sorted(out)


def key_to_state(key):
    """(m0, m1) bitmasks -> xnomos state dict {cell: kindmask}."""
    m0, m1 = key
    S = {}
    for i in range((m0 | m1).bit_length()):
        msk = ((m0 >> i) & 1) | (((m1 >> i) & 1) << 1)
        if msk:
            S[i] = msk
    return S


def card_key(key):
    return bin(key[0]).count('1') + bin(key[1]).count('1')


# ----------------------------------------------------------------- census

def universe_census(rules, tsets, mode, seeds):
    """Walk every seed; return (cycles, stats).

    cycles : dict canonical_state -> (p, d, mincard, witness_key)
             one entry per distinct GLIDER cycle in normalised-state space
             (p = its minimal period, d = its displacement per period).
    """
    (a0, b0, c0) = rules[0]
    (a1, b1, c1) = rules[1]
    T0, T1 = tsets
    t00, t01 = (0 in T0), (1 in T0)
    t10, t11 = (0 in T1), (1 in T1)
    par = (mode == 'parity')

    memo = {}
    cycles = {}
    stats = dict(EXT=0, FIX=0, CYC=0, GLI=0, BIG=0, UNR=0)

    for sd in seeds:
        path = []
        idx = {}
        disps = []
        disp = 0
        st = sd
        out = None
        while True:
            o = memo.get(st)
            if o is not None:
                out = o
                break
            j = idx.get(st)
            if j is not None:
                p = len(path) - j
                d = disp - disps[j]
                cyc = path[j:]
                if d != 0:
                    mc = min(card_key(s) for s in cyc)
                    wit = min((s for s in cyc if card_key(s) == mc))
                    cid = min(cyc)
                    if cid not in cycles:
                        cycles[cid] = (p, d, mc, wit)
                    out = ('GLI',)
                else:
                    out = ('CYC',) if p > 1 else ('FIX',)
                for s in cyc:
                    memo[s] = out
                break
            m0, m1 = st
            if bin(m0).count('1') + bin(m1).count('1') > MAX_CARD:
                out = ('BIG',)
                break
            if (m0 | m1).bit_length() > MAX_SPAN:
                out = ('BIG',)
                break
            if len(path) >= MAX_STEPS:
                out = ('UNR',)
                break
            idx[st] = len(path)
            path.append(st)
            disps.append(disp)
            # ---- one step of Phi (bitmask reimplementation) --------------
            m0 <<= 1
            m1 <<= 1
            occ = m0 | m1
            sa = occ >> a0 if a0 >= 0 else occ << -a0
            sb = occ >> b0 if b0 >= 0 else occ << -b0
            act0 = m0 & sa & ~sb
            sa = occ >> a1 if a1 >= 0 else occ << -a1
            sb = occ >> b1 if b1 >= 0 else occ << -b1
            act1 = m1 & sa & ~sb
            e0 = (act0 << c0) if c0 >= 0 else (act0 >> -c0)
            e1 = (act1 << c1) if c1 >= 0 else (act1 >> -c1)
            if par:
                g0 = (e0 if t00 else 0) ^ (e1 if t10 else 0)
                g1 = (e0 if t01 else 0) ^ (e1 if t11 else 0)
            else:
                g0 = (e0 if t00 else 0) | (e1 if t10 else 0)
                g1 = (e0 if t01 else 0) | (e1 if t11 else 0)
            n0 = m0 ^ g0
            n1 = m1 ^ g1
            occ2 = n0 | n1
            if not occ2:
                out = ('EXT',)
                break
            lo = (occ2 & -occ2).bit_length() - 1
            st = (n0 >> lo, n1 >> lo)
            disp += lo - 1
        if out[0] != 'UNR':
            for s in path:
                memo.setdefault(s, out)
        stats[out[0]] += 1
    return cycles, stats


def universe_index(u):
    r0, r1, s0, s1 = u
    return ((RULES.index(r0) * 27 + RULES.index(r1)) * 3
            + TSETS.index(s0)) * 3 + TSETS.index(s1)


def all_universes():
    for r0 in RULES:
        for r1 in RULES:
            for s0 in TSETS:
                for s1 in TSETS:
                    yield (r0, r1, s0, s1)


def job(args):
    lo, hi, mode = args
    seeds = seeds_window()
    us = list(all_universes())[lo:hi]
    out = []
    for u in us:
        r0, r1, s0, s1 = u
        cycles, stats = universe_census([r0, r1], [s0, s1], mode, seeds)
        out.append((u, cycles, stats))
    return out


# ----------------------------------------------------------------- selftest

def selftest(trials=4000):
    """Check the bitmask stepper against xnomos.step on random universes."""
    import random
    import xnomos
    rng = random.Random(20260826)
    bad = 0
    for _ in range(trials):
        r0 = rng.choice(RULES)
        r1 = rng.choice(RULES)
        s0 = rng.choice(TSETS)
        s1 = rng.choice(TSETS)
        mode = rng.choice(['parity', 'or'])
        m0 = rng.randrange(1 << 8)
        m1 = rng.randrange(1 << 8)
        if not (m0 | m1):
            continue
        occ = m0 | m1
        lo = (occ & -occ).bit_length() - 1
        key = (m0 >> lo, m1 >> lo)
        # -- bitmask step
        a0, b0, c0 = r0
        a1, b1, c1 = r1
        t00, t01 = (0 in s0), (1 in s0)
        t10, t11 = (0 in s1), (1 in s1)
        x0, x1 = key[0] << 1, key[1] << 1
        oc = x0 | x1
        sa = oc >> a0 if a0 >= 0 else oc << -a0
        sb = oc >> b0 if b0 >= 0 else oc << -b0
        act0 = x0 & sa & ~sb
        sa = oc >> a1 if a1 >= 0 else oc << -a1
        sb = oc >> b1 if b1 >= 0 else oc << -b1
        act1 = x1 & sa & ~sb
        e0 = (act0 << c0) if c0 >= 0 else (act0 >> -c0)
        e1 = (act1 << c1) if c1 >= 0 else (act1 >> -c1)
        if mode == 'parity':
            g0 = (e0 if t00 else 0) ^ (e1 if t10 else 0)
            g1 = (e0 if t01 else 0) ^ (e1 if t11 else 0)
        else:
            g0 = (e0 if t00 else 0) | (e1 if t10 else 0)
            g1 = (e0 if t01 else 0) | (e1 if t11 else 0)
        n0, n1 = x0 ^ g0, x1 ^ g1
        mine = {}
        for i in range((n0 | n1).bit_length()):
            msk = ((n0 >> i) & 1) | (((n1 >> i) & 1) << 1)
            if msk:
                mine[i - 1] = msk
        # -- xnomos step
        C = xnomos.Const([r0, r1], [s0, s1])
        S = key_to_state(key)
        T = xnomos.step(S, C, mode)
        if T != mine:
            bad += 1
            if bad < 4:
                print('MISMATCH', r0, r1, s0, s1, mode, key, T, mine)
    print('stepper selftest: %d/%d agree with xnomos.step'
          % (trials - bad, trials))
    assert bad == 0
    sd = seeds_window()
    print('seeds in %d-cell window: %d (raw masks %d)'
          % (WINDOW, len(sd), (1 << (2 * WINDOW)) - 1))
    assert len(sd) == 768


# ----------------------------------------------------------------- driver

def main():
    if '--selftest' in sys.argv:
        selftest()
        return
    import multiprocessing as mp
    os.makedirs(DATA, exist_ok=True)
    total = 27 * 27 * 3 * 3
    assert total == 6561
    chunks = []
    step = 60
    for mode in ('parity', 'or'):
        for lo in range(0, total, step):
            chunks.append((lo, min(lo + step, total), mode))
    res = {'parity': {}, 'or': {}}
    with mp.Pool(11) as pool:
        done = 0
        for out, ch in zip(pool.imap(job, chunks), chunks):
            mode = ch[2]
            for u, cycles, stats in out:
                res[mode][u] = (cycles, stats)
            done += 1
            if done % 20 == 0:
                print('  %d/%d chunks' % (done, len(chunks)), flush=True)
    with open(os.path.join(DATA, 'e3_census.pkl'), 'wb') as f:
        pickle.dump(res, f)
    for mode in ('parity', 'or'):
        ng = sum(1 for u in res[mode] if res[mode][u][0])
        print('%s: %d/%d universes admit a glider' % (mode, ng, total))


if __name__ == '__main__':
    main()
