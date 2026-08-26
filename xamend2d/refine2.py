#!/usr/bin/env python3
"""refine2.py — honest asymptotic growth exponents.

A least-squares slope of log|S_t| vs log t over a short window can exceed the
trivial bound alpha <= dim, because a pattern confined to a *bounded* box can
still be densifying: |S_t| rises steeply for a while and then saturates.  The
stage-2 refinement therefore reports, for each candidate run at T = 300 on a
640 x 650 board:

    e1 = log2( |S_150| / |S_75|  )      first octave
    e2 = log2( |S_300| / |S_150| )      second octave
    powerlaw   |e1 - e2| <= 0.15        the growth really is a power law
    expanding  max(bbox) >= 150         the support really is spreading
    fill       cells / bounding-box area at T

Only runs that are BOTH power-law and expanding carry an asymptotic alpha.
Everything else is transient densification inside a bounded region and is
reported separately (those are the cryptid candidates, not the growers).
"""
import json
import math
import subprocess
import sys
from collections import Counter

from refine_alpha import encode, SEEDS


def batch(items, exe="./xalpha2", sem=0):
    inp = "\n".join(encode(l, s) for l, s in items) + "\n"
    out = subprocess.run([exe, "--mode", "9", "--sem", str(sem),
                          "--steps", "1", "--alpha", "1"],
                         input=inp, capture_output=True, text=True).stdout
    res = []
    for ln in out.split("\n"):
        if not ln.startswith("ALPHA "):
            continue
        f = ln.split()
        j = f.index("sizes:")
        sizes = [int(v) for v in f[j + 1:]]
        w, h = (int(v) for v in f[4].split("x"))
        res.append((sizes, float(f[2]), w, h))
    return res


def analyse(sizes, fill, w, h):
    T = len(sizes) - 1
    d = dict(T=T, fill=fill, w=w, h=h, size=sizes[T])
    def oc(a, b):
        if a >= len(sizes) or sizes[a] <= 0 or sizes[b] <= 0:
            return float("nan")
        return math.log(sizes[b] / sizes[a]) / math.log(2)
    d["e1"] = oc(75, 150)
    d["e2"] = oc(150, 300)
    d["e0"] = oc(37, 75)
    d["powerlaw"] = (d["e1"] == d["e1"] and d["e2"] == d["e2"]
                     and abs(d["e1"] - d["e2"]) <= 0.15)
    # geometry at T = 300: a genuine area-filler must be spreading in BOTH
    # directions.  A long thin slab (302 x 58) can look like alpha = 2 while
    # its width saturates -- asymptotically it is a ray, alpha = 1.
    d["expanding"] = max(w, h) >= 150
    d["twod"] = min(w, h) >= 100
    return d


def main():
    src = json.load(open("data/alpha_refined.json"))
    items, keys = [], []
    for r in src:
        items.append((r["label"], [tuple(c) for c in r["seed"]]))
        keys.append((r["label"], tuple(tuple(c) for c in r["seed"])))
    print("stage-2 refinement of %d candidates (T=300, 640x650 board)"
          % len(items))
    recs = []
    B = 4000
    for i in range(0, len(items), B):
        ch = items[i:i + B]
        for it, r in zip(ch, batch(ch)):
            d = analyse(*r)
            d["label"], d["seed"] = it[0], it[1]
            recs.append(d)
        print("   ...%d" % min(i + B, len(items)), file=sys.stderr)

    good = [r for r in recs if r["powerlaw"] and r["twod"]]
    slab = [r for r in recs if r["powerlaw"] and r["expanding"]
            and not r["twod"]]
    trans = [r for r in recs if not (r["powerlaw"] and r["expanding"])]
    print("\npower-law AND 2-D expanding (both bbox sides >= 100) : %d" % len(good))
    print("power-law but 1-D (a slab: one side < 100)             : %d" % len(slab))
    print("not a power law / bounded box (cryptid candidates)     : %d" % len(trans))
    if slab:
        sl = sorted(slab, key=lambda r: -r["e2"])
        print("  slabs: max transient e2 = %.3f (bbox %dx%d, U=%s) -- these are"
              " rays whose width is still filling in" % (sl[0]["e2"],
              sl[0]["w"], sl[0]["h"], sl[0]["label"]))
    print("\nasymptotic alpha (e2) histogram over the power-law expanders:")
    h = Counter(round(r["e2"] * 20) / 20 for r in good)
    for k in sorted(h):
        print("   %.2f  %d" % (k, h[k]))
    good.sort(key=lambda r: -r["e2"])
    print("\nmax e2 = %.4f  (count with e2 > 2.02: %d)"
          % (good[0]["e2"], sum(1 for r in good if r["e2"] > 2.02)))
    print("\ntop 12 by asymptotic alpha:")
    for r in good[:12]:
        print("   a=%.3f (e1=%.3f) fill=%.3f |S300|=%d bbox=%dx%d U=%s"
              % (r["e2"], r["e1"], r["fill"], r["size"], r["w"], r["h"],
                 r["label"]))
    sol = sorted([r for r in good if r["e2"] > 1.8], key=lambda r: -r["fill"])
    print("\n(fill is measured inside the pattern's own bounding box at t=300)")
    print("\ntop 12 by FILL among asymptotic alpha > 1.8 (%d such):" % len(sol))
    for r in sol[:12]:
        print("   fill=%.4f a=%.3f |S300|=%d bbox=%dx%d U=%s"
              % (r["fill"], r["e2"], r["size"], r["w"], r["h"], r["label"]))
    band = [r for r in good if 1.05 < r["e2"] < 1.9]
    print("\nintermediate band 1.05 < alpha < 1.9 : %d universes" % len(band))
    hb = Counter(round(r["e2"] * 10) / 10 for r in band)
    for k in sorted(hb):
        print("   %.1f  %d" % (k, hb[k]))
    print("\nsample of the intermediate band:")
    seen = set()
    for r in sorted(band, key=lambda r: r["e2"]):
        k = round(r["e2"], 1)
        if k in seen:
            continue
        seen.add(k)
        print("   a=%.3f fill=%.3f bbox=%dx%d U=%s" % (r["e2"], r["fill"],
                                                       r["w"], r["h"],
                                                       r["label"]))
    json.dump([{k: v for k, v in r.items() if k != "seed"} for r in recs],
              open("data/alpha_stage2.json", "w"))
    print("\nwrote data/alpha_stage2.json")


if __name__ == "__main__":
    main()
