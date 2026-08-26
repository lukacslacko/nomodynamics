#!/usr/bin/env python3
"""
e3_sweep.py — parallel SAT sweeps for E3 (multi-target) nomodynamics.

Each job is one bounded question  "is there a glider of period exactly p and
displacement d over ANY constitution in the stated class whose t=0..p
trajectory fits in N - 2W cells?".  UNSAT is a genuine no-go for that box
(see xsat.py docstring).  Every SAT model is certified inside xsat.solve and
RE-certified here by an independent xnomos.verify_glider over 3 periods.
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time

sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6/xamend1d')

DATA = '/Users/lukacs/claude/math/program/phase6/xamend1d/data'


def worker(job):
    import xnomos
    import xsat
    from xsat import Spec
    kw = dict(job['spec'])
    sp = Spec(**kw)
    t = time.time()
    rec = dict(job['meta'])
    rec.update({k: v for k, v in kw.items()
                if k in ('n', 'N', 'p', 'd', 'mode', 'max_laws',
                         'allow_self_target', 'prime_period')})
    if kw.get('targets') is not None:
        rec['fixed_targets'] = [list(t_) for t_ in kw['targets']]
    try:
        st, info = xsat.solve(sp, timeout=job.get('timeout', 300))
    except AssertionError as e:
        rec.update(status='BUG', err=str(e)[:400])
        return rec
    rec['secs'] = round(time.time() - t, 2)
    rec['status'] = st
    if st == 'SAT':
        C = xnomos.Const(info['rules'], list(info['targets']))
        S = {c: m for c, m in info['frames'][0].items() if m}
        p, d = kw['p'], info['d']
        ok = xnomos.verify_glider(S, C, p, d, kw['mode'])
        cl = xnomos.classify(S, C, kw['mode'])
        rec.update(rules=[list(r) for r in info['rules']],
                   targets=[list(t_) for t_ in info['targets']],
                   d=d, laws=sorted(xnomos.laws(S)),
                   ncard=xnomos.card(S),
                   recertified=bool(ok),
                   classify=[cl['kind'], cl.get('period'),
                             cl.get('displacement'), cl.get('t')])
    return rec


# ------------------------------------------------------------------ job sets

def js_n2(timeout=300):
    """n=2, W=1, FREE target matrix (incl. multi-target), exact period p."""
    jobs = []
    for mode in ('parity', 'or'):
        for N in (16, 20):
            for p in range(1, 9):
                for d in range(1, p + 1):
                    jobs.append(dict(
                        meta=dict(set='n2'),
                        timeout=timeout,
                        spec=dict(n=2, W=1, N=N, p=p, d=d, mode=mode,
                                  prime_period=True)))
    return jobs


def js_crossfree(timeout=300):
    """Fully-cross (k not in T_k), FREE target matrix, n = 3,4,5."""
    jobs = []
    for mode in ('parity', 'or'):
        for n in (3, 4, 5):
            for N in (12, 14):
                for p in range(1, 5):
                    for d in range(1, p + 1):
                        jobs.append(dict(
                            meta=dict(set='crossfree'),
                            timeout=timeout,
                            spec=dict(n=n, W=1, N=N, p=p, d=d, mode=mode,
                                      allow_self_target=False,
                                      prime_period=True)))
    return jobs


def js_crossmulti(timeout=300):
    """Fully-cross AND every kind genuinely multi-target: T_k = K \\ {k}."""
    jobs = []
    for mode in ('parity', 'or'):
        for n in (3, 4):
            tg = [tuple(m for m in range(n) if m != k) for k in range(n)]
            for N in (12, 14):
                for p in range(1, 7):
                    for d in range(1, p + 1):
                        jobs.append(dict(
                            meta=dict(set='crossmulti'),
                            timeout=timeout,
                            spec=dict(n=n, W=1, N=N, p=p, d=d, mode=mode,
                                      targets=tg, prime_period=True)))
    return jobs


def js_crosstgt(timeout=300):
    """n=3: every one of the 27 fully-cross target matrices, p<=4."""
    jobs = []
    opts = {0: [(1,), (2,), (1, 2)], 1: [(0,), (2,), (0, 2)],
            2: [(0,), (1,), (0, 1)]}
    for mode in ('parity', 'or'):
        for t0 in opts[0]:
            for t1 in opts[1]:
                for t2 in opts[2]:
                    tg = [t0, t1, t2]
                    for p in range(1, 5):
                        for d in range(1, p + 1):
                            jobs.append(dict(
                                meta=dict(set='crosstgt'),
                                timeout=timeout,
                                spec=dict(n=3, W=1, N=12, p=p, d=d, mode=mode,
                                          targets=tg, prime_period=True)))
    return jobs


SPEEDS = [(2, 1), (3, 1), (3, 2), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3),
          (5, 4), (6, 1), (6, 5), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
          (7, 6), (8, 1), (8, 3), (8, 5), (8, 7), (9, 2), (9, 4), (10, 3)]


def js_speed(timeout=600):
    jobs = []
    for mode in ('parity', 'or'):
        for n in (2, 3):
            for N in (14, 18):
                for (p, d) in SPEEDS:
                    jobs.append(dict(
                        meta=dict(set='speed'),
                        timeout=timeout,
                        spec=dict(n=n, W=1, N=N, p=p, d=d, mode=mode,
                                  prime_period=True)))
    return jobs


def js_period(timeout=600):
    """Largest certifiable MINIMAL period, n = 3, 4."""
    jobs = []
    for mode in ('parity', 'or'):
        for n in (3, 4):
            for p in range(2, 17):
                for d in range(1, p + 1):
                    jobs.append(dict(
                        meta=dict(set='period'),
                        timeout=timeout,
                        spec=dict(n=n, W=1, N=14, p=p, d=d, mode=mode,
                                  prime_period=True)))
    return jobs


def js_minlaws(timeout=300):
    """Smallest seeds: cap the placed-law count."""
    jobs = []
    for mode in ('parity', 'or'):
        for n in (2, 3, 4):
            for ml in (1, 2, 3):
                for p in range(1, 5):
                    for d in range(1, p + 1):
                        for cross in (True, False):
                            if cross and n == 2:
                                continue
                            jobs.append(dict(
                                meta=dict(set='minlaws', cross=cross),
                                timeout=timeout,
                                spec=dict(n=n, W=1, N=12, p=p, d=d, mode=mode,
                                          max_laws=ml, prime_period=True,
                                          allow_self_target=not cross)))
    return jobs


SETS = dict(n2=js_n2, crossfree=js_crossfree, crossmulti=js_crossmulti,
            crosstgt=js_crosstgt, speed=js_speed, period=js_period,
            minlaws=js_minlaws)


def main():
    import multiprocessing as mp
    names = sys.argv[1].split(',')
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    tmo = float(sys.argv[3]) if len(sys.argv) > 3 else None
    jobs = []
    for nm in names:
        jobs += (SETS[nm]() if tmo is None else SETS[nm](tmo))
    print('%d jobs, %d workers' % (len(jobs), nproc), flush=True)
    os.makedirs(DATA, exist_ok=True)
    out = []
    t0 = time.time()
    with mp.Pool(nproc) as pool:
        for i, rec in enumerate(pool.imap_unordered(worker, jobs)):
            out.append(rec)
            if rec['status'] in ('SAT', 'BUG') or (i % 25 == 0):
                print('[%5.0fs] %4d/%d %s' % (time.time() - t0, i + 1,
                                              len(jobs), json.dumps(
                                                  {k: v for k, v in rec.items()
                                                   if k not in ('laws',)})[:220]),
                      flush=True)
    fn = os.path.join(DATA, 'e3_sweep_%s.json' % '_'.join(names))
    with open(fn, 'w') as f:
        json.dump(out, f, indent=1)
    from collections import Counter
    print('status:', dict(Counter(r['status'] for r in out)))
    print('-> %s' % fn)


if __name__ == '__main__':
    main()
