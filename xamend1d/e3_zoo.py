#!/usr/bin/env python3
"""
e3_zoo.py — generic-n bitmask census, used to trawl the E3 glider zoo at
n = 3, 4 for large MINIMAL periods and unusual speeds.

Same machinery as e3_census.py but for any n: a state is an n-tuple of cell
bitmasks; the functional graph on translation-normalised states is walked with
memoisation, so a glider CYCLE is detected exactly (its length in normalised
state space IS its minimal period, and the accumulated shift IS d).

Modes: 'sample' walks random universes; 'exhaust' enumerates all rule tuples
for one fixed target matrix.  Every glider is re-verified by xnomos downstream
(see the --verify pass).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6/xamend1d')

OFF = (-1, 0, 1)
RULES = [(a, b, c) for a in OFF for b in OFF for c in OFF]
MAX_STEPS = 3000
MAX_CARD = 48
MAX_SPAN = 48
DATA = '/Users/lukacs/claude/math/program/phase6/xamend1d/data'


def seeds_window(n, w):
    out = set()
    for msk in range(1, 1 << (n * w)):
        ms = [0] * n
        for i in range(w):
            for k in range(n):
                if msk >> (n * i + k) & 1:
                    ms[k] |= 1 << i
        occ = 0
        for m in ms:
            occ |= m
        lo = (occ & -occ).bit_length() - 1
        out.add(tuple(m >> lo for m in ms))
    return sorted(out)


def key_to_state(key):
    n = len(key)
    occ = 0
    for m in key:
        occ |= m
    S = {}
    for i in range(occ.bit_length()):
        msk = 0
        for k in range(n):
            if (key[k] >> i) & 1:
                msk |= 1 << k
        if msk:
            S[i] = msk
    return S


def card_key(key):
    return sum(bin(m).count('1') for m in key)


def census(rules, tsets, mode, seeds, n):
    par = (mode == 'parity')
    memo = {}
    cycles = {}
    for sd in seeds:
        path = []
        idx = {}
        disps = []
        disp = 0
        st = sd
        out = None
        while True:
            if st in memo:
                out = memo[st]
                break
            j = idx.get(st)
            if j is not None:
                p = len(path) - j
                d = disp - disps[j]
                cyc = path[j:]
                out = ('GLI',) if d else ('CYC',)
                if d:
                    mc = min(card_key(s) for s in cyc)
                    wit = min(s for s in cyc if card_key(s) == mc)
                    cid = min(cyc)
                    cycles.setdefault(cid, (p, d, mc, wit))
                for s in cyc:
                    memo[s] = out
                break
            if card_key(st) > MAX_CARD:
                out = ('BIG',)
                break
            occ = 0
            for m in st:
                occ |= m
            if occ.bit_length() > MAX_SPAN:
                out = ('BIG',)
                break
            if len(path) >= MAX_STEPS:
                out = ('UNR',)
                break
            idx[st] = len(path)
            path.append(st)
            disps.append(disp)
            ms = [m << 1 for m in st]
            occ = 0
            for m in ms:
                occ |= m
            T = [0] * n
            for k in range(n):
                a, b, c = rules[k]
                sa = occ >> a if a >= 0 else occ << -a
                sb = occ >> b if b >= 0 else occ << -b
                act = ms[k] & sa & ~sb
                if not act:
                    continue
                em = (act << c) if c >= 0 else (act >> -c)
                if par:
                    for t in tsets[k]:
                        T[t] ^= em
                else:
                    for t in tsets[k]:
                        T[t] |= em
            new = [ms[k] ^ T[k] for k in range(n)]
            occ2 = 0
            for m in new:
                occ2 |= m
            if not occ2:
                out = ('EXT',)
                break
            lo = (occ2 & -occ2).bit_length() - 1
            st = tuple(m >> lo for m in new)
            disp += lo - 1
        if out[0] != 'UNR':
            for s in path:
                memo.setdefault(s, out)
    return cycles


def tsets_all(n):
    ks = list(range(n))
    per_kind = [tuple(s) for r in range(1, n + 1)
                for s in itertools.combinations(ks, r)]
    return per_kind


def sample(n, w, trials, seed, modes=('parity', 'or'), cross=False):
    rng = random.Random(seed)
    sds = seeds_window(n, w)
    pool = tsets_all(n)
    best = {}
    speeds = {}
    zoo = []
    for _ in range(trials):
        rules = [rng.choice(RULES) for _ in range(n)]
        tg = []
        for k in range(n):
            while True:
                t = rng.choice(pool)
                if cross and k in t:
                    continue
                break
            tg.append(t)
        for mode in modes:
            cyc = census(rules, tg, mode, sds, n)
            for cid, (p, d, mc, wit) in cyc.items():
                sp = Fraction(abs(d), p)
                key = (mode, p, d)
                rec = (p, d, mc, [list(r) for r in rules],
                       [list(t) for t in tg], mode, wit)
                if p > best.get(mode, (0,))[0]:
                    best[mode] = (p, d, mc, [list(r) for r in rules],
                                  [list(t) for t in tg], wit)
                if sp not in speeds or p < speeds[sp][0]:
                    speeds[sp] = rec
    return best, speeds


def verify(rec, mode):
    import xnomos
    p, d, mc, rules, tg, md, wit = rec
    C = xnomos.Const([tuple(r) for r in rules], [tuple(t) for t in tg])
    S = key_to_state(wit)
    cl = xnomos.classify(S, C, md)
    ok = (cl['kind'] == 'GLIDER' and cl['period'] == p
          and cl['displacement'] == d and cl['t'] == 0
          and xnomos.verify_glider(S, C, p, d, md))
    return ok, S, C, cl


def main():
    n = int(sys.argv[1])
    w = int(sys.argv[2])
    trials = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    cross = '--cross' in sys.argv
    import xnomos
    best, speeds = sample(n, w, trials, seed, cross=cross)
    print('n=%d seedwindow=%d trials=%d cross=%s' % (n, w, trials, cross))
    print('--- largest minimal period found ---')
    for mode, b in sorted(best.items()):
        p, d, mc, rules, tg, wit = b
        ok, S, C, cl = verify((p, d, mc, rules, tg, mode, wit), mode)
        print('  %-6s p=%d d=%+d laws=%d rules=%s targets=%s seed=%s verified=%s'
              % (mode, p, d, mc, rules, tg, sorted(xnomos.laws(S)), ok))
        if ok:
            for row in xnomos.spacetime(S, C, 2 * p + 1, mode,
                                        lo=min(S) - 2,
                                        hi=max(S) + 2 * abs(d) + 4):
                print('      |' + row)
    print('--- speed spectrum observed (minimal p per speed) ---')
    rows = []
    for sp in sorted(speeds):
        rec = speeds[sp]
        ok, S, C, cl = verify(rec, rec[5])
        rows.append(dict(speed=str(sp), p=rec[0], d=rec[1], laws=rec[2],
                         rules=rec[3], targets=rec[4], mode=rec[5],
                         seed=sorted(xnomos.laws(S)), verified=bool(ok)))
        print('  %-6s p=%2d d=%+d %-6s laws=%2d verified=%s rules=%s T=%s seed=%s'
              % (sp, rec[0], rec[1], rec[5], rec[2], ok, rec[3], rec[4],
                 sorted(xnomos.laws(S))))
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, 'e3_zoo_n%d%s.json'
                           % (n, '_cross' if cross else '')), 'w') as f:
        json.dump(rows, f, indent=1)


if __name__ == '__main__':
    main()
