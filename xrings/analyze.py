#!/usr/bin/env python3
"""
analyze.py — read the raw census JSONL and produce the report tables.

  python3 analyze.py <tag> [<tag> ...]

Rotor bookkeeping: `sweep` reports classes (p, r, j) with Phi^p(X) =
rot_r(tau^j(X)).  We split them into
  * SPATIAL rotors  r != 0   — the law-packet genuinely travels round the ring
  * SCREW rotors    r == 0, j != 0 — the packet stands still but its kind
    labels advance one notch per p steps (only possible for homogeneous cyclic
    constitutions, where tau is an automorphism)
and record, per (m, p, r, j), a minimum-cardinality witness.
"""
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("XR_RAW", os.path.join(HERE, "raw"))
sys.path.insert(0, HERE)
from xring import Ring, decode                       # noqa: E402


def load(tag):
    with open(os.path.join(RAW, tag + ".jsonl")) as f:
        for line in f:
            yield json.loads(line)


def show(v, n, m, rules, targets, mode="parity"):
    R = Ring(rules, targets, m, mode)
    return R.render(decode(v, n, m))


MODENAME = {0: "parity", 1: "or", 2: "super", 3: "super_or"}


def report(tag, split_mode=False):
    per = defaultdict(lambda: defaultdict(lambda: [10 ** 9, None]))
    rot = defaultdict(lambda: defaultdict(lambda: [10 ** 9, None]))
    bal = defaultdict(lambda: [0, 0, 10 ** 9, None])
    nconst = defaultdict(int)
    fixtot = defaultdict(int)
    ntot = defaultdict(int)
    overflow = 0
    for r in load(tag):
        key = (r["m"], MODENAME[r["mode"]]) if split_mode else r["m"]
        nconst[key] += 1
        fixtot[key] += r["nfix"]
        ntot[key] += r["N"]
        overflow += r["overflow"]
        meta = (r["rules"], r["targets"], MODENAME[r["mode"]])
        for p, (cnt, mc, rep) in r["periods"].items():
            p = int(p)
            e = per[key][p]
            if mc < e[0]:
                per[key][p] = [mc, (rep,) + meta]
        for (p, rr, j, card, rep) in r["rotors"]:
            e = rot[key][(p, rr, j)]
            if card < e[0]:
                rot[key][(p, rr, j)] = [card, (rep,) + meta]
        if r["nbal"]:
            bal[key][0] += r["nbal"]
            bal[key][1] += 1

    print("\n########## %s ##########" % tag)
    for key in sorted(nconst):
        m = key[0] if split_mode else key
        ps = sorted(per[key])
        odd = [p for p in ps if p > 1 and p % 2]
        npow2 = [p for p in ps if p & (p - 1)]
        sp = sorted(k for k in rot[key] if k[1] != 0)
        sc = sorted(k for k in rot[key] if k[1] == 0)
        print("  m=%-3s %-9s consts=%-6d  maxp=%-5d  |periods|=%d"
              % (m, key[1] if split_mode else "", nconst[key],
                 max(ps) if ps else 0, len(ps)))
        print("        periods      : %s" % ps)
        if odd:
            print("        ODD >1       : %s   (min odd witness card=%d %s)"
                  % (odd, per[key][min(odd)][0], per[key][min(odd)][1][1:]))
        if npow2:
            print("        non-pow-2    : %s" % npow2)
        if sp:
            print("        SPATIAL rotors (p,r,j): %s" % (sp,))
            for k in sp[:6]:
                card, (rep, rules, tg, md) = rot[key][k]
                print("            p=%d rot=%d screw=%d card=%d  %s  %s->%s [%s]"
                      % (k[0], k[1], k[2], card,
                         show(rep, len(rules), m, rules, tg, md),
                         rules, tg, md))
        if sc:
            print("        SCREW-only rotors (p,0,j): %s" % (sc,))
            for k in sc[:4]:
                card, (rep, rules, tg, md) = rot[key][k]
                print("            p=%d screw=%d card=%d  %s  %s->%s [%s]"
                      % (k[0], k[2], card,
                         show(rep, len(rules), m, rules, tg, md),
                         rules, tg, md))
        if bal[key][0]:
            print("        BALANCED states: %d  in %d constitutions"
                  % (bal[key][0], bal[key][1]))
        pmax = max(ps) if ps else 0
        if pmax > 4:
            card, (rep, rules, tg, md) = per[key][pmax]
            print("        maxp witness : p=%d card=%d %s  %s->%s [%s]"
                  % (pmax, card, show(rep, len(rules), m, rules, tg, md),
                     rules, tg, md))
    if overflow:
        print("  !! %d cycles exceeded the period table (>=4096)" % overflow)
    return per, rot, bal


if __name__ == "__main__":
    for tag in sys.argv[1:]:
        report(tag, split_mode=tag.startswith("super"))
