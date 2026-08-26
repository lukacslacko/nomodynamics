#!/usr/bin/env python3
"""sunset.py — deep probe of SUNSET semantics (laws lapse unless re-enacted).

This is the one point of the semantic lattice where the Anchor Theorem's
hypothesis (H3) locality of amendment fails: an untouched (cell, kind) slot is
NOT unchanged, it decays.  Everything the field has proved about motion on Z
rests on H3, so this is the axis to probe hardest.

Run: python3 sunset.py
"""
from collections import Counter, defaultdict

from xlib import RULES1, Const, all_seeds, seeds_span
from xsem import Sem, sunset_step, sunset_classify, verify_sunset_glider, actives
from xnomos import state_of, laws

TMAPS4 = [[0, 1], [1, 0], [0, 0], [1, 1]]


def render(A, lo, hi, sym="AB"):
    S = defaultdict(int)
    for (c, k), _ in A.items():
        S[c] |= 1 << k
    out = []
    for i in range(lo, hi + 1):
        m = S.get(i, 0)
        out.append("." if not m else ("#" if bin(m).count("1") > 1
                                      else sym[(m & -m).bit_length() - 1]))
    return "".join(out)


def survey(tau, span=3, budget=200):
    sem = Sem(sunset=tau)
    cnt = Counter()
    gl = []
    for r0 in RULES1:
        for r1 in RULES1:
            for tm in TMAPS4:
                C = Const([r0, r1], list(tm))
                for S in all_seeds(span, 2):
                    A = {(c, k): tau for c, k in laws(S)}
                    r = sunset_classify(A, C, sem, budget)
                    cnt[r["kind"]] += 1
                    if r["kind"] == "GLIDER":
                        gl.append((r0, r1, tuple(tm), tuple(sorted(S.items())),
                                   r["period"], r["displacement"], r["t"]))
    return sem, cnt, gl


def main():
    print("== SUNSET census: complete 2-kind box, all 2916 constitutions, "
          "seeds of span <= 3 (48 seeds) = 139,968 codes per tau ==")
    store = {}
    for tau in (1, 2, 3):
        sem, cnt, gl = survey(tau)
        store[tau] = (sem, cnt, gl)
        n = sum(cnt.values())
        print("\n-- tau = %d --" % tau)
        for k in ("EXTINCT", "FIXED", "CYCLE", "GLIDER", "GROWING", "UNRESOLVED"):
            print("   %-11s %8d  %6.2f%%" % (k, cnt[k], 100.0 * cnt[k] / n))
        if gl:
            ps = Counter(g[4] for g in gl)
            ds = Counter(g[5] for g in gl)
            print("   glider periods     %s" % dict(sorted(ps.items())))
            print("   glider displacem.  %s" % dict(sorted(ds.items())))
            print("   speeds |d|/p       %s"
                  % sorted({abs(g[5]) / g[4] for g in gl}))

    # ---- the non-trivial gliders: period > 1, i.e. NOT a bare marching law
    print("\n== non-trivial sunset gliders (period >= 2) ==")
    for tau in (1, 2, 3):
        sem, cnt, gl = store[tau]
        nt = [g for g in gl if g[4] >= 2]
        print(" tau=%d : %d of %d gliders have period >= 2" % (tau, len(nt), len(gl)))
        seen = set()
        shown = 0
        for g in sorted(nt, key=lambda g: (-g[4], abs(g[5]))):
            key = (g[4], g[5])
            if key in seen:
                continue
            seen.add(key)
            r0, r1, tm, S, p, d, t0 = g
            C = Const([r0, r1], list(tm))
            A = {(c, k): tau for c, k in laws(dict(S))}
            for _ in range(t0):
                A = sunset_step(A, C, sem)
            ok = verify_sunset_glider(A, C, sem, p, d)
            print("   %s  seed %s  p=%d d=%+d speed %s  verified=%s"
                  % (C.label(), list(S), p, d,
                     "%d/%d" % (abs(d), p), ok))
            cells = [c for (c, k) in A]
            for step in range(p + 1):
                print("        " + render(A, min(cells) - 1, max(cells) + 3))
                A = sunset_step(A, C, sem)
            shown += 1
            if shown >= 3:
                break

    # ---- skeleton check: for every sunset glider, is P contained in t(A)?
    print("\n== glider-skeleton check on sunset gliders ==")
    bad = 0
    tot = 0
    for tau in (1, 2, 3):
        sem, cnt, gl = store[tau]
        for g in gl[:4000]:
            r0, r1, tm, S, p, d, t0 = g
            C = Const([r0, r1], list(tm))
            A = {(c, k): tau for c, k in laws(dict(S))}
            for _ in range(t0):
                A = sunset_step(A, C, sem)
            P, Astar = set(), set()
            for _ in range(p):
                Sd = {}
                for (c, k) in A:
                    Sd[c] = Sd.get(c, 0) | (1 << k)
                P |= {k for _, k in laws(Sd)}
                Astar |= {k for _, k in actives(Sd, C, sem)}
                A = sunset_step(A, C, sem)
            tA = set()
            for k in Astar:
                tA.update(C.targets[k])
            tot += 1
            if not P <= tA:
                bad += 1
    print("   P subset t(A*) over the whole period: %d gliders, %d violations"
          % (tot, bad))


if __name__ == "__main__":
    main()
