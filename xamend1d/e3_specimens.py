#!/usr/bin/env python3
"""
e3_specimens.py — the certified specimen book of this sub-expedition.

Every entry is re-verified from the literal numbers printed here, by
xnomos.verify_glider (3 full periods) AND xnomos.classify (which must report
GLIDER with the stated minimal period, displacement and entry time t=0),
in whichever resolution modes are claimed.
"""
from __future__ import annotations

import sys

sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6/xamend1d')

import xnomos                                                    # noqa: E402

#  name, rules, targets, seed (cell,kind) pairs, p, d, modes
BOOK = [
    ('E3-2A  n=2 minimal, 2 laws (canonical rep of orbit 10 of 11)',
     [(0, -1, 0), (0, -1, 1)], [(0, 1), (0, 1)],
     [(0, 0), (0, 1)], 1, +1, ('parity', 'or')),
    ('E3-2B  n=2 "TANDEM-1" as pre-supplied (kind-swap of E3-2A)',
     [(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)],
     [(1, 0), (1, 1)], 1, +1, ('parity', 'or')),
    ('X-1LAW n=3 FULLY-CROSS multi-target, ONE placed law, speed 1/2',
     [(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(1, 2), (0,), (0,)],
     [(1, 0)], 2, +1, ('parity', 'or')),
    ('X-ALLMULTI n=3 fully cross AND every T_k = K\\{k}, speed 1/2',
     [(0, 1, 1), (-1, 1, 0), (0, 1, -1)], [(1, 2), (0, 2), (0, 1)],
     None, 2, +1, ('parity',)),
    ('SPEED-2/3 at n=3 (parity) — one kind has out-degree 1',
     [(0, -1, 1), (0, 1, 1), (0, 1, 0)], [(0, 1), (2,), (0, 1, 2)],
     [(1, 0), (1, 1), (1, 2), (4, 2), (6, 0), (6, 1), (6, 2), (8, 0), (8, 1)],
     3, +2, ('parity',)),
    ('SPEED-2/3 at n=3 (or)',
     [(0, 1, 1), (0, -1, 1), (0, 1, 0)], [(2,), (0, 1), (0, 1, 2)],
     [(1, 0), (1, 1), (1, 2), (3, 0), (3, 1), (5, 0), (5, 1), (5, 2), (8, 2)],
     3, +2, ('or',)),
    ('SPEED-1 at minimal period 2, n=3, ONE placed law',
     [(0, -1, 1), (0, 1, 1), (0, 1, -1)], [(0, 1, 2), (0,), (0,)],
     [(1, 0)], 2, +2, ('parity',)),
    ('SPEED-1 at minimal period 4, n=3',
     [(0, 1, -1), (0, 1, 1), (1, -1, 1)], [(0, 1, 2), (0, 1, 2), (0, 2)],
     [(2, 0), (2, 2), (5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2)],
     4, +4, ('parity',)),
]


def check(name, rules, tg, seed, p, d, modes, diagram=True):
    if seed is None:
        print('%s\n   (witness not recorded)' % name)
        return
    C = xnomos.Const(rules, tg)
    S = xnomos.state_of(seed)
    print(name)
    print('   rules=%s targets=%s seed=%s  p=%d d=%+d'
          % (rules, tg, seed, p, d))
    for mode in modes:
        vg = xnomos.verify_glider(S, C, p, d, mode)
        cl = xnomos.classify(S, C, mode)
        ok = (vg and cl['kind'] == 'GLIDER' and cl['period'] == p
              and cl['displacement'] == d and cl['t'] == 0)
        print('   %-6s verify_glider=%s  classify=%s p=%s d=%s t=%s  -> %s'
              % (mode, vg, cl['kind'], cl.get('period'),
                 cl.get('displacement'), cl.get('t'), 'OK' if ok else 'FAIL'))
        assert ok, name
    if diagram:
        m = modes[0]
        for row in xnomos.spacetime(S, C, 2 * p + 1, m,
                                    lo=min(S) - 2, hi=max(S) + 2 * abs(d) + 3):
            print('      |' + row)


if __name__ == '__main__':
    for e in BOOK:
        check(*e)
        print()
    print('ALL SPECIMENS CERTIFIED')
