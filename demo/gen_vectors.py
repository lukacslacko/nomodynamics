#!/usr/bin/env python3
"""Emit differential-test vectors for demo/xengine.js from the Python engine."""
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from xnomos import Const, state_of, step                              # noqa: E402

OFF1 = (-1, 0, 1)
OFF2 = [(dx, dy) for dx in OFF1 for dy in OFF1]


def key(cell, dim):
    return "%d,%d" % cell if dim == 2 else str(cell)


def trace(C, seed_pairs, mode, n):
    S = state_of(seed_pairs)
    out = []
    for _ in range(n):
        out.append(sorted(([key(c, C.dim), m] for c, m in S.items()),
                          key=lambda r: r[0]))
        S = step(S, C, mode)
    return out


def emit(vecs, name, C, seed_pairs, mode, n=12):
    js_seed = [[c[0], c[1], k] if C.dim == 2 else [c, k]
               for c, k in seed_pairs]
    vecs.append({
        "name": name,
        "mode": mode,
        "const": {"rules": [[list(o) if C.dim == 2 else o for o in r]
                            for r in C.rules],
                  "targets": [list(t) if len(t) > 1 else t[0]
                              for t in C.targets],
                  "dim": C.dim, "mod": C.modulus},
        "seed": js_seed,
        "trace": trace(C, seed_pairs, mode, n),
    })


def main():
    rng = random.Random(20260826)
    vecs = []

    # named specimens
    emit(vecs, "colonizer", Const([(0, 1, 1)]), [(0, 0)], "parity")
    emit(vecs, "ring rotor", Const([(0, 1, -1)], modulus=6),
         [(1, 0), (2, 0), (5, 0)], "parity")
    emit(vecs, "two-chamber deadlock",
         Const([(0, 1, 1), (0, -1, -1), (0, 1, 0)], targets=[2, 2, 2]),
         [(0, 0), (2, 1)], "parity")
    emit(vecs, "two-chamber, OR",
         Const([(0, 1, 1), (0, -1, -1), (0, 1, 0)], targets=[2, 2, 2]),
         [(0, 0), (2, 1)], "or")
    emit(vecs, "jubilee",
         Const([((1, 0), (0, 1), (0, -1)), ((0, 1), (0, -1), (0, 1)),
                ((-1, 0), (0, -1), (1, 0))], dim=2),
         [((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)], "parity", n=40)

    # randomised universes: 1-D, 2-D, rings, every mode, own/cross targeting
    for i in range(120):
        dim = 1 if i % 3 else 2
        n = rng.randrange(1, 4)
        pool = OFF2 if dim == 2 else OFF1
        rules = [tuple(rng.choice(pool) for _ in range(3)) for _ in range(n)]
        targets = [rng.randrange(n) for _ in range(n)]
        if i % 7 == 0:                       # multi-target
            targets = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                       for _ in range(n)]
        mod = 7 if (dim == 1 and i % 5 == 0) else None
        C = Const(rules, targets, dim=dim, modulus=mod)
        cells = []
        for _ in range(rng.randrange(1, 7)):
            if dim == 2:
                cells.append(((rng.randrange(-2, 3), rng.randrange(-2, 3)),
                              rng.randrange(n)))
            else:
                c = rng.randrange(-3, 4)
                cells.append((c % 7 if mod else c, rng.randrange(n)))
        mode = ["parity", "or", "super", "super_or"][i % 4]
        emit(vecs, "rand%03d" % i, C, cells, mode)

    # impermanence vectors: {"sunset": tau} alongside the ordinary ones
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent
                           / "sunset"))
    from sunset import step_sunset                                # noqa: E402

    def strace(C, seed_pairs, tau, n):
        S, ages = state_of(seed_pairs), None
        out = []
        for _ in range(n):
            out.append(sorted(([key(c, C.dim), m] for c, m in S.items()),
                              key=lambda r: r[0]))
            S, ages = step_sunset(S, C, tau, ages)
        return out

    for i in range(60):
        n = rng.randrange(1, 4)
        rules = [tuple(rng.choice(OFF1) for _ in range(3)) for _ in range(n)]
        targets = [rng.randrange(n) for _ in range(n)]
        if i % 5 == 0:
            targets = [tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                       for _ in range(n)]
        C = Const(rules, targets)
        cells = [(rng.randrange(-3, 4), rng.randrange(n))
                 for _ in range(rng.randrange(1, 5))]
        tau = rng.randrange(1, 5)
        vecs.append({
            "name": "sun%03d" % i, "mode": "parity", "sunset": tau,
            "const": {"rules": [list(r) for r in C.rules],
                      "targets": [list(x) if len(x) > 1 else x[0]
                                  for x in C.targets],
                      "dim": 1, "mod": None},
            "seed": [[c, k] for c, k in cells],
            "trace": strace(C, cells, tau, 12),
        })

    json.dump(vecs, sys.stdout)


if __name__ == "__main__":
    main()
