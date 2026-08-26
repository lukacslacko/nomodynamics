#!/usr/bin/env python3
"""tables.py — render every X-E frontier table from the raw .jsonl data."""
from __future__ import annotations

import collections
import json
import os
import sys
from math import gcd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(name):
    path = os.path.join(D, name)
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path) if l.strip()]


def red(p, d):
    g = gcd(p, d)
    return (p // g, d // g)


def sat_map():
    """Box-fixed SAT map over ALL constitutions (interior 14) + box audit."""
    rows = load("map.jsonl") + load("box.jsonl")
    best = {}
    for r in rows:
        k = (r["n"], r["W"], r["p"], r["d"])
        interior = r["N"] - 2 * r["W"]
        cur = best.get(k)
        if r["status"] == "SAT":
            if cur is None or cur[0] != "SAT":
                best[k] = ("SAT", interior)
        elif cur is None or (cur[0] == "UNSAT" and interior > cur[1]):
            best[k] = ("UNSAT", interior)
    return best


def print_sat_map():
    best = sat_map()
    print("### Box-fixed SAT map (ALL constitutions; interior = N-2W)\n")
    print("Entry `d` = displacement realised; `x` = decided UNSAT; "
          "number after = largest interior decided.\n")
    for n in (2, 3, 4):
        for W in (1, 2, 3):
            ks = [k for k in best if k[0] == n and k[1] == W]
            if not ks:
                continue
            sat = sorted((k[2], k[3]) for k in ks if best[k][0] == "SAT")
            uns = sorted((k[2], k[3]) for k in ks if best[k][0] == "UNSAT")
            spd = sorted({red(p, d) for p, d in sat}, key=lambda x: x[1] / x[0])
            print("n=%d W=%d  realised (p,d): %s" % (n, W, sat))
            print("           reduced speeds d'/p': %s"
                  % ", ".join("%d/%d" % (d, p) for p, d in spd))
            print("           max reduced numerator: %d"
                  % (max([d for p, d in spd], default=0)))
            print("           UNSAT: %s\n" % uns)


def print_width_scan():
    for f in ("width1.jsonl", "spdA.jsonl"):
        rows = load(f)
        if not rows:
            continue
        print("### Width scan `%s` (ALL constitutions, interiors escalated)\n" % f)
        for r in sorted(rows, key=lambda r: (r["mode"], r["n"], r["p"], r["d"])):
            mx = r["steps"][-1][0]
            print("  n=%d W=%d %-6s p=%-2d d=%-2d  %-5s  %s"
                  % (r["n"], r["W"], r["mode"], r["p"], r["d"], r["status"],
                     ("wmin=%d" % r["wmin"]) if r["status"] == "SAT"
                     else "no glider to interior %d" % mx))
        print()


def print_sft():
    for n, W, f in ((2, 1, "sft2_n2W1.jsonl"), (3, 1, "sft2_n3W1.jsonl"),
                    (4, 1, "sft2_n4W1.jsonl"), (2, 2, "sft2_n2W2.jsonl")):
        rows = load(f)
        if not rows:
            continue
        print("### WIDTH-UNBOUNDED, full-target constitutions: n=%d, W=%d\n" % (n, W))
        by = {}
        for r in rows:
            by[(r["p"], r["d"], r["mode"])] = r
        for mode in ("parity", "or"):
            g = sorted((p, d) for (p, d, m) in by if m == mode
                       and by[(p, d, m)]["verdict"] == "GLIDER")
            no = sorted((p, d) for (p, d, m) in by if m == mode
                        and by[(p, d, m)]["verdict"] == "NONE")
            cp = sorted((p, d) for (p, d, m) in by if m == mode
                        and by[(p, d, m)]["verdict"] == "CAP")
            spd = sorted({red(p, d) for p, d in g}, key=lambda x: x[1] / x[0])
            print("  %-7s GLIDER: %s" % (mode, g))
            print("          speeds: %s   max reduced numerator: %s"
                  % (", ".join("%d/%d" % (d, p) for p, d in spd),
                     max([d for p, d in spd], default=0)))
            print("          NONE at any width: %s" % no)
            if cp:
                print("          UNDECIDED (state cap): %s" % cp)
        pmax = max(p for (p, d, m) in by)
        print("  decided for p <= %d, every d in 1..pW, both resolutions\n" % pmax)


def print_specimens():
    rows = [r for r in load("sft2_n2W1.jsonl") + load("sft2_n3W1.jsonl")
            + load("sft2_n4W1.jsonl") + load("sft2_n2W2.jsonl")
            if r["verdict"] == "GLIDER"]
    print("### Width-unbounded specimens (channels = rules; targets = all kinds)\n")
    seen = set()
    for r in sorted(rows, key=lambda r: (r["n"], r["W"], r["p"], r["d"])):
        key = (r["n"], r["W"], red(r["p"], r["d"]), r["mode"])
        if key in seen:
            continue
        seen.add(key)
        print("  n=%d W=%d p=%d d=%d %-6s rules=%s  seed cells=%s  verified=%s"
              % (r["n"], r["W"], r["p"], r["d"], r["mode"],
                 r["chans"], r["cells"], r.get("verified")))
    print()


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "sat"):
        print_sat_map()
    if what in ("all", "width"):
        print_width_scan()
    if what in ("all", "sft"):
        print_sft()
    if what in ("all", "spec"):
        print_specimens()
