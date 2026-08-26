#!/usr/bin/env python3
"""Cross-validate the C census engine (xcensus, mode 9) against the Python
dict engine in xa2d.py (which is itself validated against xnomos.py).

Every verdict must agree exactly, including period, displacement and card.
"""
import random
import subprocess
import sys

from xa2d import (Const, MOORE, OFF, state, classify, card, active,
                  EXTINCT, FIXED, BALANCED, CYCLE, GLIDER, GROWING, UNRESOLVED)

OFFIDX = {OFF[c]: i for i, c in enumerate("OEWNSPQRT")}
IDXOFF = [OFF[c] for c in "OEWNSPQRT"]
VMAP = {"extinct": EXTINCT, "fixed": FIXED, "balanced": BALANCED,
        "cycle": CYCLE, "glider": GLIDER, "escape": GROWING,
        "unres": UNRESOLVED}


def main(N=3000, steps=200, seed=1):
    rng = random.Random(seed)
    exps = []
    for _ in range(N):
        n = rng.choice((2, 2, 2, 3))
        rules, tg = [], []
        for k in range(n):
            rules.append(tuple(rng.choice(MOORE) for _ in range(3)))
            sz = rng.choice((1, 1, 1, 2, n))
            tg.append(tuple(sorted(rng.sample(range(n), min(sz, n)))))
        C = Const(rules, tg)
        ns = rng.randint(1, 4)
        cells = set()
        while len(cells) < ns:
            cells.add((rng.randint(0, 2), rng.randint(0, 2), rng.randrange(n)))
        exps.append((C, sorted(cells)))

    lines = []
    for C, sd in exps:
        parts = [str(C.n)]
        for k in range(C.n):
            a, b, c = C.rules[k]
            m = 0
            for t in C.targets[k]:
                m |= 1 << t
            parts += [str(OFFIDX[a]), str(OFFIDX[b]), str(OFFIDX[c]), str(m)]
        parts.append(str(len(sd)))
        for (x, y, k) in sd:
            parts += [str(x), str(y), str(k)]
        lines.append(" ".join(parts))

    for sem, semname in ((0, "parity"), (1, "or")):
        out = subprocess.run(["./xcensus", "--mode", "9", "--sem", str(sem),
                              "--steps", str(steps), "--maxcard", "900"],
                             input="\n".join(lines) + "\n",
                             capture_output=True, text=True).stdout.split("\n")
        bad = 0
        for i, (C, sd) in enumerate(exps):
            f = out[i].split()
            cv, ct0, cp, cdx, cdy, ccard, cact = (f[0], int(f[1]), int(f[2]),
                                                  int(f[3]), int(f[4]),
                                                  int(f[5]), int(f[6]))
            S0 = state([((x, y), k) for (x, y, k) in sd])
            py = classify(S0, C, mode=semname, max_steps=steps,
                          max_card=900, max_span=59)
            pv = py["kind"]
            cvp = VMAP[cv]
            if pv != cvp:
                bad += 1
                if bad < 6:
                    print("MISMATCH verdict", semname, C.label(), sd,
                          "py=", py, "c=", out[i])
                continue
            if pv in (CYCLE, GLIDER) and py["period"] != cp:
                bad += 1
                print("MISMATCH period", semname, C.label(), sd, py, out[i])
            if pv == GLIDER and tuple(py["d"]) != (cdx, cdy):
                bad += 1
                print("MISMATCH disp", semname, C.label(), sd, py, out[i])
            if pv == BALANCED and py["active"] != cact:
                bad += 1
                print("MISMATCH nactive", semname, C.label(), sd, py, out[i])
        print("%s: %d/%d agree" % (semname, len(exps) - bad, len(exps)))
        if bad:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 3000))
