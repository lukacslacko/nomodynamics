#!/usr/bin/env python3
"""refine_alpha.py — long-baseline growth-exponent refinement.

Stage 1 (in xcensus --alpha) measured alpha on a 256x256 board over 120 steps;
short-window fits can overshoot the trivial bound alpha <= 2.  Here every
candidate with a stage-1 alpha >= 1.05 is re-run on a 640x650 board for 300
steps by `xalpha2`, and the exponent is reported three ways:

  alpha_fit    least-squares slope of log|S_t| vs log t over the last 2/3
  alpha_oct    log2( |S_T| / |S_{T/2}| )          -- local exponent, one octave
  fill         |cells(S_T)| / area(bounding box)  -- how solid the growth is

alpha_oct is the honest asymptotic estimator: for |S_t| ~ C t^a it converges
to a with no window bias.
"""
import subprocess
import sys
from collections import Counter

from xa2d import Const, OFF

OFFIDX = {OFF[c]: i for i, c in enumerate("OEWNSPQRT")}
SEEDS = {
    0: [(0, 0, 0)], 1: [(0, 0, 0), (0, 0, 1)], 2: [(0, 0, 0), (1, 0, 1)],
    3: [(0, 0, 0), (0, 1, 1)], 4: [(0, 0, 0), (1, 1, 1)],
    5: [(0, 0, 0), (1, 0, 0), (0, 1, 1)],
}


def encode(label, seed):
    C = Const.parse(label)
    parts = [str(C.n)]
    for k in range(C.n):
        a, b, c = C.rules[k]
        m = 0
        for t in C.targets[k]:
            m |= 1 << t
        parts += [str(OFFIDX[a]), str(OFFIDX[b]), str(OFFIDX[c]), str(m)]
    parts.append(str(len(seed)))
    for (x, y, k) in seed:
        parts += [str(x), str(y), str(k)]
    return " ".join(parts)


def run_batch(items, sem=0, exe="./xalpha2"):
    """items: list of (label, seedlist).  Returns list of dicts."""
    inp = "\n".join(encode(l, s) for l, s in items) + "\n"
    out = subprocess.run([exe, "--mode", "9", "--sem", str(sem),
                          "--steps", "1", "--alpha", "1"],
                         input=inp, capture_output=True, text=True).stdout
    lines = [x for x in out.split("\n") if x.startswith("ALPHA ")]
    res = []
    for ln in lines:
        f = ln.split()
        j = f.index("sizes:")
        sizes = [int(v) for v in f[j + 1:]]
        T = len(sizes) - 1
        a_oct = float("nan")
        if T >= 16 and sizes[T] > 0 and sizes[T // 2] > 0:
            import math
            a_oct = math.log(sizes[T] / sizes[T // 2]) / math.log(2)
        res.append(dict(alpha_fit=float(f[1]), fill=float(f[2]),
                        size=int(f[3]), bbox=f[4], T=T, alpha_oct=a_oct,
                        sizes=sizes))
    return res


def main():
    thresh = float(sys.argv[1]) if len(sys.argv) > 1 else 1.05
    cands = {}
    for ln in open("data/moore_alpha_raw.txt"):
        f = ln.split()
        if not f or f[0] != "ALPHA" or len(f) < 9:
            continue
        try:
            a = float(f[1])
        except ValueError:
            continue
        if a < thresh:
            continue
        seed = int(f[6])
        lab = " ".join(f[8:])
        if lab.count(">") != 2:
            continue
        cands[(lab, seed)] = a
    items = [(lab, SEEDS[sd]) for (lab, sd) in cands]
    print("refining %d stage-1 candidates (alpha >= %.2f) on a 640x650 board, "
          "300 steps" % (len(items), thresh))
    res = []
    B = 4000
    for i in range(0, len(items), B):
        chunk = items[i:i + B]
        r = run_batch(chunk)
        for it, rr in zip(chunk, r):
            rr["label"] = it[0]
            rr["seed"] = it[1]
            res.append(rr)
        print("  ...%d/%d" % (min(i + B, len(items)), len(items)),
              file=sys.stderr)
    good = [r for r in res if r["alpha_oct"] == r["alpha_oct"]]
    good.sort(key=lambda r: -r["alpha_oct"])
    print("\nrefined alpha_oct histogram (bin 0.05):")
    h = Counter(round(r["alpha_oct"] * 20) / 20 for r in good)
    for k in sorted(h):
        print("   %.2f  %d" % (k, h[k]))
    print("\nmax alpha_oct = %.4f ; number with alpha_oct > 2.02 = %d"
          % (good[0]["alpha_oct"], sum(1 for r in good if r["alpha_oct"] > 2.02)))
    print("\ntop 20 by alpha_oct:")
    for r in good[:20]:
        print("   a_oct=%.3f a_fit=%.3f fill=%.3f |S_300|=%d bbox=%s U=%s "
              "seedcells=%s" % (r["alpha_oct"], r["alpha_fit"], r["fill"],
                                r["size"], r["bbox"], r["label"], r["seed"]))
    solid = [r for r in good if r["alpha_oct"] > 1.7]
    solid.sort(key=lambda r: -r["fill"])
    print("\ntop 20 by FILL among alpha_oct > 1.7 (%d such):" % len(solid))
    for r in solid[:20]:
        print("   fill=%.4f a_oct=%.3f |S_300|=%d bbox=%s U=%s"
              % (r["fill"], r["alpha_oct"], r["size"], r["bbox"], r["label"]))
    import json
    with open("data/alpha_refined.json", "w") as fh:
        json.dump([{k: v for k, v in r.items() if k != "sizes"}
                   for r in good], fh)
    print("\nwrote data/alpha_refined.json (%d records)" % len(good))


if __name__ == "__main__":
    main()
