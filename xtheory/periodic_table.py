#!/usr/bin/env python3
"""periodic_table.py — the periodic table of 1-D two-kind constitutions.

Reads the raw C census, quotients by the symmetry group, joins the structural
invariants of the amendment graph, writes data/periodic_table.csv, and prints
the digest tables used in RESULTS.md — including the census-scale tests of

  * Theorem A   (balance requires a non-injective target map)
  * Zero-Sum No-Go  (all cycle offset-sums zero  =>  no growth, ever)
  * the parity/OR collapse on injective target maps.

Run: python3 periodic_table.py [suffix]     e.g. 8_parity
"""
import csv
import sys
from collections import Counter, defaultdict

CLS = ["extinct", "fixed", "balanced", "cycle", "glider", "growing", "unresolved"]
TNAME = {(0, 1): "id", (1, 0): "swap", (0, 0): "const0", (1, 1): "const1"}


def load(suf):
    return [{k: int(v) for k, v in d.items()}
            for d in csv.DictReader(open("data/census%s.csv" % suf))]


def key(d):
    return ((d["r0a"], d["r0b"], d["r0c"]), (d["r1a"], d["r1b"], d["r1c"]),
            (d["t0"], d["t1"]))


def mirror(k):
    r0, r1, t = k
    return (tuple(-x for x in r0), tuple(-x for x in r1), t)


def relabel(k):
    r0, r1, t = k
    s = {0: 1, 1: 0}
    return (r1, r0, (s[t[1]], s[t[0]]))


def orbit(k):
    o = {k}
    for _ in range(3):
        o |= {mirror(x) for x in o} | {relabel(x) for x in o}
    return frozenset(o)


def cycle_sums(k):
    """Offset-sums of the cycles of the amendment functional graph, and the
    set of cycle-sums REACHABLE from each kind (both kinds may be seeded)."""
    r0, r1, t = k
    c = [r0[2], r1[2]]
    if t == (0, 1):                      # two self-loops
        return {0: c[0], 1: c[1]}
    if t == (1, 0):                      # one 2-cycle
        s = c[0] + c[1]
        return {0: s, 1: s}
    if t == (0, 0):                      # self-loop at 0; 1 -> 0
        return {0: c[0], 1: c[0]}
    return {0: c[1], 1: c[1]}            # self-loop at 1; 0 -> 1


def main(suf="8_parity"):
    rows = load(suf)
    by = {key(d): d for d in rows}
    orbs = {}
    for k in by:
        orbs.setdefault(orbit(k), []).append(k)
    reps = sorted(min(v) for v in orbs.values())
    nseed = sum(by[reps[0]][c] for c in CLS)

    # ------- write the full table
    with open("data/periodic_table%s.csv" % suf, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rule0", "rule1", "targets", "orbit_size", "cycle_sums"]
                   + CLS + ["maxperiod", "periods", "maxtransient",
                            "balanced_at_t0", "maxactive"])
        for k in reps:
            d = by[k]
            cs = cycle_sums(k)
            w.writerow([str(k[0]), str(k[1]), TNAME[k[2]],
                        len(orbs[orbit(k)]), str(sorted(set(cs.values())))]
                       + [d[c] for c in CLS]
                       + [d["maxperiod"],
                          str([i for i in range(64) if d["periodmask"] >> i & 1]),
                          d["maxtransient"], d.get("balanced0", -1), d["maxactive"]])
    print("wrote data/periodic_table%s.csv : %d orbit representatives" % (suf, len(reps)))

    # ------- Theorem A at census scale
    binj = sum(d["balanced"] for d in rows if len({d["t0"], d["t1"]}) == 2)
    bnon = sum(d["balanced"] for d in rows if len({d["t0"], d["t1"]}) == 1)
    print("\n[Theorem A, census scale]  balanced runs with INJECTIVE target map: "
          "%d ; with NON-injective: %d" % (binj, bnon))

    # ------- Zero-Sum No-Go at census scale
    bad = 0
    zn = 0
    zg = 0
    for k, d in by.items():
        cs = set(cycle_sums(k).values())
        if cs == {0}:
            zn += 1
            zg += d["growing"]
            if d["growing"]:
                bad += 1
    print("[Zero-Sum No-Go, census scale]  %d constitutions have every cycle "
          "offset-sum 0 ; total GROWING runs among them: %d (violations %d)"
          % (zn, zg, bad))
    nz = [d for k, d in by.items() if set(cycle_sums(k).values()) != {0}]
    print("                                the other %d constitutions produce "
          "%d GROWING runs" % (len(nz), sum(d["growing"] for d in nz)))

    # ------- behaviour classes
    print("\n== behaviour classes of the 757 orbits (span<=8, %s) ==" % suf)
    cls = Counter()
    for k in reps:
        d = by[k]
        sig = []
        sig.append("bal" if d["balanced"] else "-")
        sig.append("grow" if d["growing"] else "-")
        sig.append("odd" if d["nonpow2"] else "-")
        sig.append("ext" if d["extinct"] else "-")
        cls[tuple(sig)] += 1
    for s, n in cls.most_common():
        print("   %-28s %4d" % ("/".join(s), n))

    # ------- the interesting residue: orbits that are NOT generic
    print("\n== non-generic orbits ==")
    print("  (a) totally extinct universes (every seed dies):")
    for k in reps:
        if by[k]["extinct"] == nseed:
            print("      %s %s %s" % (k[0], k[1], TNAME[k[2]]))
    print("  (b) universes with NO growth at all:")
    ng = [k for k in reps if by[k]["growing"] == 0]
    print("      %d orbits; cycle-sum profile: %s"
          % (len(ng), Counter(str(sorted(set(cycle_sums(k).values())))
                              for k in ng)))
    print("  (c) universes whose period spectrum contains an ODD period > 1:")
    odd = [k for k in reps
           if any((by[k]["periodmask"] >> i) & 1 for i in (3, 5, 7, 9, 11))]
    print("      %d orbits" % len(odd))
    for k in odd[:10]:
        d = by[k]
        print("      %s %s %-6s periods %s"
              % (k[0], k[1], TNAME[k[2]],
                 [i for i in range(64) if d["periodmask"] >> i & 1]))
    print("  (d) longest cycles:")
    for k in sorted(reps, key=lambda k: -by[k]["maxperiod"])[:6]:
        d = by[k]
        print("      %s %s %-6s maxperiod %d  periods %s"
              % (k[0], k[1], TNAME[k[2]], d["maxperiod"],
                 [i for i in range(64) if d["periodmask"] >> i & 1]))
    print("  (e) balance: seeds already balanced vs seeds that REACH balance:")
    tb = sum(d["balanced"] for d in rows)
    t0 = sum(d.get("balanced0", 0) for d in rows)
    print("      %d balanced verdicts, of which %d were balanced at t=0 "
          "(%.1f%%) and %d CONVERGED to balance (%.1f%%)"
          % (tb, t0, 100.0 * t0 / tb, tb - t0, 100.0 * (tb - t0) / tb))
    for k in sorted(reps, key=lambda k: -(by[k]["balanced"] - by[k].get("balanced0", 0)))[:5]:
        d = by[k]
        print("      %s %s %-6s reached %d / balanced %d / seeds %d"
              % (k[0], k[1], TNAME[k[2]], d["balanced"] - d.get("balanced0", 0),
                 d["balanced"], nseed))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "8_parity")
