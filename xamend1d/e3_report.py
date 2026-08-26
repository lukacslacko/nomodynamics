#!/usr/bin/env python3
"""
e3_report.py — analyse data/e3_census.pkl.

Every glider cycle recorded by the census is INDEPENDENTLY re-verified here by
xnomos.classify + xnomos.verify_glider (3 full periods) before it is counted.
"""
from __future__ import annotations

import pickle
import sys
from collections import Counter, defaultdict
from fractions import Fraction

sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6/xamend1d')

import xnomos                                                   # noqa: E402
from e3_census import TSETS, key_to_state, card_key             # noqa: E402

DATA = '/Users/lukacs/claude/math/program/phase6/xamend1d/data/e3_census.pkl'


def reflect_universe(u):
    r0, r1, s0, s1 = u
    return (tuple(-x for x in r0), tuple(-x for x in r1), s0, s1)


def swap_universe(u):
    """Relabel kind 0 <-> kind 1."""
    r0, r1, s0, s1 = u
    def sw(s):
        return tuple(sorted(1 - k for k in s))
    return (r1, r0, sw(s1), sw(s0))


def canon(u):
    orbit = set()
    for f in (lambda x: x, reflect_universe):
        for g in (lambda x: x, swap_universe):
            orbit.add(g(f(u)))
            orbit.add(f(g(u)))
    return min(orbit)


def ulabel(u):
    r0, r1, s0, s1 = u
    return ('rules=[%s,%s] targets=[%s,%s]'
            % (r0, r1, '{%s}' % ','.join(map(str, s0)),
               '{%s}' % ','.join(map(str, s1))))


def kindof(u):
    """own / perm / many-to-one / multi (E3)."""
    r0, r1, s0, s1 = u
    if len(s0) > 1 or len(s1) > 1:
        return 'E3 multi-target'
    t = (s0[0], s1[0])
    if t == (0, 1):
        return 'own-kind'
    if t == (1, 0):
        return 'permutation'
    return 'many-to-one'


def main():
    with open(DATA, 'rb') as f:
        res = pickle.load(f)
    report = {}
    for mode in ('parity', 'or'):
        R = res[mode]
        gl_us = {u: v for u, v in R.items() if v[0]}
        # ---- re-verify every distinct glider cycle with xnomos -----------
        ncyc = 0
        bad = 0
        speeds = Counter()
        pcount = Counter()
        cards = Counter()
        best = {}
        specimens = []
        for u, (cycles, stats) in sorted(gl_us.items()):
            r0, r1, s0, s1 = u
            C = xnomos.Const([r0, r1], [s0, s1])
            bb = None
            for cid, (p, d, mc, wit) in sorted(cycles.items()):
                ncyc += 1
                S = key_to_state(wit)
                cl = xnomos.classify(S, C, mode)
                ok = (cl['kind'] == xnomos.GLIDER and cl['period'] == p
                      and cl['displacement'] == d and cl['t'] == 0
                      and xnomos.verify_glider(S, C, p, d, mode))
                if not ok:
                    bad += 1
                    print('  !! UNVERIFIED', mode, u, p, d, wit, cl)
                    continue
                speeds[Fraction(abs(d), p)] += 1
                pcount[p] += 1
                cards[mc] += 1
                cand = (p, abs(d), mc, d, wit)
                if bb is None or cand[:3] < bb[:3]:
                    bb = cand
            best[u] = bb
            specimens.append((u, bb))
        report[mode] = dict(gl_us=gl_us, ncyc=ncyc, bad=bad, speeds=speeds,
                            pcount=pcount, cards=cards, best=best)
        print('== mode=%s ==' % mode)
        print('universes with a glider: %d / 6561' % len(gl_us))
        print('distinct glider cycles : %d   (xnomos-verified: %d, failed %d)'
              % (ncyc, ncyc - bad, bad))
        print('by universe class      : %s'
              % dict(Counter(kindof(u) for u in gl_us)))
        print('speeds |d|/p realised  : %s'
              % {str(k): v for k, v in sorted(speeds.items())})
        print('periods p realised     : %s' % dict(sorted(pcount.items())))
        print('glider law-counts      : %s' % dict(sorted(cards.items())))
        print('minimum law count      : %d' % min(cards))
        # symmetry orbits of the glider-admitting universes
        orb = defaultdict(list)
        for u in gl_us:
            orb[canon(u)].append(u)
        print('symmetry orbits (refl x kind-swap): %d' % len(orb))
        for c in sorted(orb):
            p, ad, mc, d, wit = best[c] if best.get(c) else best[orb[c][0]]
            print('   %-46s |orbit|=%d   best p=%d d=%+d laws=%d seed=%s'
                  % (ulabel(c), len(orb[c]), p, d, mc,
                     sorted(xnomos.laws(key_to_state(wit)))))
        print()
    with open('/Users/lukacs/claude/math/program/phase6/xamend1d/data/'
              'e3_report.pkl', 'wb') as f:
        pickle.dump(report, f)


if __name__ == '__main__':
    main()
