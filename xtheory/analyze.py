#!/usr/bin/env python3
"""analyze.py — turn the raw C census into the periodic table.

Reads data/census_<mode>.csv, applies the symmetry quotient, prints the
aggregate census, the per-target-map blocks, the period spectrum, and the
interesting residue.

Run: python3 analyze.py [parity|or]
"""
import csv
import sys
from collections import Counter, defaultdict

CLS = ["extinct", "fixed", "balanced", "cycle", "glider", "growing", "unresolved"]
TNAME = {(0, 1): "id (own-kind)", (1, 0): "swap (reciprocal)",
         (0, 0): "const-0 (both->0)", (1, 1): "const-1 (both->1)"}


def load(mode):
    rows = []
    with open("data/census_%s.csv" % mode) as f:
        for d in csv.DictReader(f):
            d = {k: int(v) for k, v in d.items()}
            rows.append(d)
    return rows


def key(d):
    return ((d["r0a"], d["r0b"], d["r0c"]), (d["r1a"], d["r1b"], d["r1c"]),
            (d["t0"], d["t1"]))


def mirror(k):
    (r0, r1, t) = k
    return (tuple(-x for x in r0), tuple(-x for x in r1), t)


def relabel(k):
    """swap kind 0 and 1: rules swap, target map conjugated by the swap."""
    (r0, r1, t) = k
    s = {0: 1, 1: 0}
    return (r1, r0, (s[t[1]], s[t[0]]))


def orbit(k):
    o = set()
    for f in (lambda x: x, mirror):
        for g in (lambda x: x, relabel):
            o.add(f(g(k)))
            o.add(g(f(k)))
    return frozenset(o)


def main(mode="parity"):
    rows = load(mode)
    by = {key(d): d for d in rows}
    assert len(by) == 2916, len(by)
    nseed = sum(by[next(iter(by))][c] for c in CLS)

    # ---- symmetry soundness: the census vector must be constant on orbits
    orbits, bad = {}, 0
    for k in by:
        o = orbit(k)
        orbits.setdefault(o, []).append(k)
    for o, ks in orbits.items():
        v0 = tuple(by[ks[0]][c] for c in CLS)
        for k in ks[1:]:
            if tuple(by[k][c] for c in CLS) != v0:
                bad += 1
    print("== symmetry quotient ==")
    print("constitutions %d -> orbits %d ; orbit-size histogram %s"
          % (len(by), len(orbits), dict(Counter(len(o) for o in orbits))))
    print("census vector constant on every orbit: %s (%d violations)"
          % (bad == 0, bad))

    tot = Counter()
    for d in rows:
        for c in CLS:
            tot[c] += d[c]
    N = sum(tot.values())
    print("\n== aggregate census (%s, 2916 constitutions x %d seeds = %d runs) =="
          % (mode, nseed, N))
    for c in CLS:
        print("  %-11s %10d  %6.2f%%" % (c, tot[c], 100.0 * tot[c] / N))

    print("\n== by target map ==")
    print("  %-20s %8s %8s %8s %8s %8s %8s %8s" % ("target map", *CLS))
    blocks = defaultdict(Counter)
    for d in rows:
        blocks[(d["t0"], d["t1"])].update({c: d[c] for c in CLS})
    for t, cnt in sorted(blocks.items()):
        n = sum(cnt.values())
        print("  %-20s " % TNAME[t] + " ".join("%7.2f%%" % (100.0 * cnt[c] / n)
                                               for c in CLS))
    print("  %-20s " % "(raw counts, id)" +
          " ".join("%8d" % blocks[(0, 1)][c] for c in CLS))

    print("\n== period spectrum (from the per-constitution period bitmask) ==")
    for t, _ in sorted(blocks.items()):
        m = 0
        for d in rows:
            if (d["t0"], d["t1"]) == t:
                m |= d["periodmask"]
        ps = [i for i in range(64) if m >> i & 1]
        print("  %-20s %s" % (TNAME[t], ps))
    allm = 0
    mx = 0
    for d in rows:
        allm |= d["periodmask"]
        mx = max(mx, d["maxperiod"])
    print("  %-20s %s   (max period seen: %d)"
          % ("ALL", [i for i in range(64) if allm >> i & 1], mx))
    np2 = sum(d["nonpow2"] for d in rows)
    print("  runs with non-power-of-2 period: %d" % np2)

    print("\n== interesting residue ==")
    g = [d for d in rows if d["glider"]]
    print("  constitutions with a GLIDER          : %d" % len(g))
    u = [d for d in rows if d["unresolved"]]
    print("  constitutions with an UNRESOLVED seed: %d (total %d seeds)"
          % (len(u), sum(d["unresolved"] for d in u)))
    b = [d for d in rows if d["balanced"]]
    print("  constitutions with a BALANCED seed   : %d (total %d seeds, max active %d)"
          % (len(b), sum(d["balanced"] for d in b), max([d["maxactive"] for d in b] or [0])))
    n2 = [d for d in rows if d["nonpow2"]]
    print("  constitutions with a non-2-power p   : %d" % len(n2))
    for d in sorted(n2, key=lambda d: -d["nonpow2"])[:8]:
        print("      %s  n=%d  periodmask=%s"
              % (fmt(d), d["nonpow2"],
                 [i for i in range(64) if d["periodmask"] >> i & 1]))
    print("  longest transient: %d" % max(d["maxtransient"] for d in rows))
    for d in sorted(rows, key=lambda d: -d["maxtransient"])[:5]:
        print("      %s  transient=%d" % (fmt(d), d["maxtransient"]))
    print("  extinction champions:")
    for d in sorted(rows, key=lambda d: -d["extinct"])[:5]:
        print("      %s  extinct=%d/%d" % (fmt(d), d["extinct"], nseed))
    print("  balance champions:")
    for d in sorted(rows, key=lambda d: -d["balanced"])[:5]:
        print("      %s  balanced=%d/%d maxactive=%d"
              % (fmt(d), d["balanced"], nseed, d["maxactive"]))


def fmt(d):
    return "0:(%d,%d,%d)->%d 1:(%d,%d,%d)->%d" % (
        d["r0a"], d["r0b"], d["r0c"], d["t0"],
        d["r1a"], d["r1b"], d["r1c"], d["t1"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "parity")
