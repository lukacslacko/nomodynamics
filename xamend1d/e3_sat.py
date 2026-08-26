#!/usr/bin/env python3
"""
e3_sat.py — SAT sweeps for Expedition X-A / E3 (multi-target nomodynamics).

Sub-commands
  cross    Task 2: fully-cross constitutions (k not in T_k), n = 3, 4.
  speed    Task 3: prescribed non-unit speeds |d|/p < 1.
  period   Task 3: largest certifiable minimal period.
  n2       Task 1 cross-check: is the 5-cell census box complete for n=2?

Every SAT hit is certified inside xsat.solve() (which raises on an uncertified
model) and RE-certified here by an independent xnomos.verify_glider call.
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6/xamend1d')

import xnomos                                                     # noqa: E402
import xsat                                                       # noqa: E402
from xsat import Spec                                             # noqa: E402

DATA = '/Users/lukacs/claude/math/program/phase6/xamend1d/data'


def recertify(info, mode, p):
    """Independent re-verification, ignoring everything xsat computed."""
    C = xnomos.Const(info['rules'], list(info['targets']))
    S = {c: m for c, m in info['frames'][0].items() if m}
    d = info['d']
    ok = xnomos.verify_glider(S, C, p, d, mode)
    cl = xnomos.classify(S, C, mode)
    return ok, cl, C, S


def show(info, mode, p, tag=''):
    ok, cl, C, S = recertify(info, mode, p)
    print('   %s rules=%s targets=%s' % (tag, info['rules'], info['targets']))
    print('   seed=%s  d=%+d  p=%d' % (sorted(xnomos.laws(S)), info['d'], p))
    print('   xnomos.verify_glider(3 periods) = %s ; classify -> %s p=%s d=%s'
          % (ok, cl['kind'], cl.get('period'), cl.get('displacement')))
    lo = min(S) - 2
    hi = max(S) + p * abs(info['d']) + 3
    for row in xnomos.spacetime(S, C, 2 * p + 2, mode, lo=lo, hi=hi):
        print('     |' + row)
    return ok


def run(sp, timeout, verbose=False):
    t = time.time()
    try:
        st, info = xsat.solve(sp, timeout=timeout, verbose=verbose)
    except AssertionError as e:
        return 'BUG', None, time.time() - t, str(e)
    return st, info, time.time() - t, None


# ------------------------------------------------------------------ task 2

def task_cross(argv):
    out = []
    ns = [int(x) for x in (argv[0].split(',') if argv else ['3', '4'])]
    Ns = [int(x) for x in (argv[1].split(',') if len(argv) > 1 else ['12', '14'])]
    pmax = int(argv[2]) if len(argv) > 2 else 8
    tmo = float(argv[3]) if len(argv) > 3 else 600
    for mode in ('parity', 'or'):
        for n in ns:
            for N in Ns:
                for p in range(1, pmax + 1):
                    sp = Spec(n=n, W=1, N=N, p=p, d=list(range(1, p + 1)),
                              mode=mode, allow_self_target=False)
                    st, info, dt, err = run(sp, tmo)
                    print('cross n=%d N=%d p=%d %-6s : %-7s (%.1fs)'
                          % (n, N, p, mode, st, dt), flush=True)
                    rec = dict(task='cross', n=n, N=N, p=p, mode=mode,
                               status=st, secs=round(dt, 2))
                    if st == 'SAT':
                        print('   *** FULLY-CROSS GLIDER ***')
                        ok = show(info, mode, p)
                        rec['rules'] = [list(r) for r in info['rules']]
                        rec['targets'] = [list(t) for t in info['targets']]
                        rec['d'] = info['d']
                        rec['seed'] = sorted(xnomos.laws(
                            {c: m for c, m in info['frames'][0].items() if m}))
                        rec['recertified'] = ok
                    if st == 'BUG':
                        rec['err'] = err
                        print('   BUG:', err)
                    out.append(rec)
    dump(out, 'e3_sat_cross.json')


# ------------------------------------------------------------------ task 3

SPEEDS = [(2, 1), (3, 1), (3, 2), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3),
          (5, 4), (6, 1), (6, 5), (7, 2), (7, 3), (8, 3), (8, 5)]


def task_speed(argv):
    out = []
    ns = [int(x) for x in (argv[0].split(',') if argv else ['2', '3'])]
    Ns = [int(x) for x in (argv[1].split(',') if len(argv) > 1 else ['12', '16'])]
    tmo = float(argv[2]) if len(argv) > 2 else 600
    for mode in ('parity', 'or'):
        for n in ns:
            for N in Ns:
                for (p, d) in SPEEDS:
                    sp = Spec(n=n, W=1, N=N, p=p, d=d, mode=mode,
                              prime_period=True)
                    st, info, dt, err = run(sp, tmo)
                    print('speed n=%d N=%d p=%d d=%d (%d/%d) %-6s : %-7s (%.1fs)'
                          % (n, N, p, d, d, p, mode, st, dt), flush=True)
                    rec = dict(task='speed', n=n, N=N, p=p, d=d, mode=mode,
                               status=st, secs=round(dt, 2))
                    if st == 'SAT':
                        ok = show(info, mode, p)
                        rec['rules'] = [list(r) for r in info['rules']]
                        rec['targets'] = [list(t) for t in info['targets']]
                        rec['seed'] = sorted(xnomos.laws(
                            {c: m for c, m in info['frames'][0].items() if m}))
                        rec['recertified'] = ok
                    out.append(rec)
    dump(out, 'e3_sat_speed.json')


def task_period(argv):
    """Largest minimal period certifiable, free d."""
    out = []
    ns = [int(x) for x in (argv[0].split(',') if argv else ['2', '3'])]
    N = int(argv[1]) if len(argv) > 1 else 14
    pmax = int(argv[2]) if len(argv) > 2 else 12
    tmo = float(argv[3]) if len(argv) > 3 else 600
    for mode in ('parity', 'or'):
        for n in ns:
            for p in range(2, pmax + 1):
                for d in range(1, p + 1):
                    sp = Spec(n=n, W=1, N=N, p=p, d=d, mode=mode,
                              prime_period=True)
                    st, info, dt, err = run(sp, tmo)
                    tag = 'period n=%d N=%d p=%d d=%d %-6s : %-7s (%.1fs)' % (
                        n, N, p, d, mode, st, dt)
                    print(tag, flush=True)
                    rec = dict(task='period', n=n, N=N, p=p, d=d, mode=mode,
                               status=st, secs=round(dt, 2))
                    if st == 'SAT':
                        ok = show(info, mode, p)
                        rec['rules'] = [list(r) for r in info['rules']]
                        rec['targets'] = [list(t) for t in info['targets']]
                        rec['seed'] = sorted(xnomos.laws(
                            {c: m for c, m in info['frames'][0].items() if m}))
                        rec['recertified'] = ok
                    out.append(rec)
    dump(out, 'e3_sat_period.json')


def task_n2(argv):
    """Is the 5-cell census box complete for n=2, W=1?  Free targets, free d."""
    out = []
    Ns = [int(x) for x in (argv[0].split(',') if argv else ['12', '16'])]
    pmax = int(argv[1]) if len(argv) > 1 else 6
    tmo = float(argv[2]) if len(argv) > 2 else 600
    for mode in ('parity', 'or'):
        for N in Ns:
            for p in range(2, pmax + 1):
                for d in range(1, p + 1):
                    sp = Spec(n=2, W=1, N=N, p=p, d=d, mode=mode,
                              prime_period=True)
                    st, info, dt, err = run(sp, tmo)
                    print('n2 N=%d p=%d d=%d %-6s : %-7s (%.1fs)'
                          % (N, p, d, mode, st, dt), flush=True)
                    rec = dict(task='n2', n=2, N=N, p=p, d=d, mode=mode,
                               status=st, secs=round(dt, 2))
                    if st == 'SAT':
                        ok = show(info, mode, p)
                        rec['rules'] = [list(r) for r in info['rules']]
                        rec['targets'] = [list(t) for t in info['targets']]
                        rec['seed'] = sorted(xnomos.laws(
                            {c: m for c, m in info['frames'][0].items() if m}))
                        rec['recertified'] = ok
                    out.append(rec)
    dump(out, 'e3_sat_n2.json')


def dump(out, name):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), 'w') as f:
        json.dump(out, f, indent=1)
    print('-> %s (%d records)' % (name, len(out)))


if __name__ == '__main__':
    cmd = sys.argv[1]
    {'cross': task_cross, 'speed': task_speed, 'period': task_period,
     'n2': task_n2}[cmd](sys.argv[2:])
