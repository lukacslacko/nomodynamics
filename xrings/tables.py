#!/usr/bin/env python3
"""tables.py — emit the markdown tables of RESULTS.md from the raw censuses."""
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("XR_RAW", os.path.join(HERE, "raw"))
sys.path.insert(0, HERE)
from xring import Ring, decode                       # noqa: E402

MODENAME = {0: "parity", 1: "or", 2: "super", 3: "super_or"}


def spectra(tag, filt=None):
    """m -> (set of periods, maxp, witness)"""
    out = defaultdict(lambda: [set(), 0, None, 0, 0, 0])
    path = os.path.join(RAW, tag + ".jsonl")
    if not os.path.exists(path):
        return {}
    for line in open(path):
        r = json.loads(line)
        if filt and not filt(r):
            continue
        d = out[r["m"]]
        d[3] += 1
        d[4] += r["nbal"]
        for p, (cnt, mc, rep) in r["periods"].items():
            p = int(p)
            d[0].add(p)
            if p > d[1]:
                d[1] = p
                d[2] = (mc, rep, r["rules"], r["targets"], r["mode"])
        for (p, rr, j, card, rep) in r["rotors"]:
            if rr != 0:
                d[5] += 1
    return out


def line(tag, name, filt=None):
    S = spectra(tag, filt)
    rows = []
    for m in sorted(S):
        ps, mx, w, nc, nb, nrot = S[m]
        odd = sorted(p for p in ps if p > 1 and p % 2)
        rows.append((m, sorted(ps), mx, odd, nc, nb, nrot))
    return name, rows


def main():
    classes = [
        line("own", "own-kind, 1 kind (27 kinds)"),
        line("own2", "own-kind, 2 kinds (729)"),
        line("own3", "own-kind, 3 live kinds (1728)"),
        line("recip", "2-cycle permutation (729)"),
        line("noninj", "2 kinds, both amend kind 0 (729)"),
        line("cyc3", "3-cycle permutation, live (1728)"),
        line("cyc3all", "3-cycle permutation, all (19683)"),
        line("super1", "supersession, 1 kind",
             lambda r: r["mode"] == 2),
        line("super2", "supersession, 2 kinds (729)",
             lambda r: r["mode"] == 2),
        line("super2or", "supersession-OR, 2 kinds (729)"),
        line("super3", "supersession, 3 live kinds (1728)"),
    ]
    print("### maximal period attained (complete state-space enumeration)\n")
    ms = list(range(3, 21))
    print("| class | " + " | ".join("m=%d" % m for m in ms) + " |")
    print("|" + "---|" * (len(ms) + 1))
    for name, rows in classes:
        d = {m: mx for m, ps, mx, odd, nc, nb, nrot in rows}
        print("| %s | " % name + " | ".join(str(d.get(m, "")) for m in ms)
              + " |")

    print("\n### full period sets\n")
    for name, rows in classes:
        if not rows:
            continue
        print("**%s**" % name)
        for m, ps, mx, odd, nc, nb, nrot in rows:
            print("  - m=%2d : %s%s" % (m, ps,
                                        "   [odd>1: %s]" % odd if odd else ""))
        print()

    print("\n### spatial rotor classes (r != 0) per ring size\n")
    print("| class | " + " | ".join("m=%d" % m for m in ms) + " |")
    print("|" + "---|" * (len(ms) + 1))
    for name, rows in classes:
        d = {m: nrot for m, ps, mx, odd, nc, nb, nrot in rows}
        print("| %s | " % name + " | ".join(str(d.get(m, "")) for m in ms)
              + " |")

    print("\n### balanced (fixed-yet-active) states, summed over the class\n")
    print("| class | " + " | ".join("m=%d" % m for m in ms) + " |")
    print("|" + "---|" * (len(ms) + 1))
    for name, rows in classes:
        d = {m: nb for m, ps, mx, odd, nc, nb, nrot in rows}
        print("| %s | " % name + " | ".join(str(d.get(m, "")) for m in ms)
              + " |")


if __name__ == "__main__":
    main()
