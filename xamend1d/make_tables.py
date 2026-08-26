#!/usr/bin/env python3
"""make_tables.py — render the SAT frontier tables from data/frontier*.json."""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))

rows = []
for f in ("frontier.json", "frontier_big.json"):
    p = os.path.join(HERE, "data", f)
    if os.path.exists(p):
        try:
            rows += json.load(open(p))
        except Exception:
            pass

st = collections.Counter(r["status"] for r in rows)
print("## SAT frontier — %d bounded existence questions, %s\n"
      % (len(rows), " ".join("%s %d" % (k, v) for k, v in st.items())))
print("Each row: for that class, semantics and window, EVERY constitution and "
      "EVERY seed whose t=0..p trajectory fits the interior was decided at "
      "once.  UNSAT = complete no-go for the box.\n")

# one row per (class, semantics, W): max kinds, and the pareto frontier of
# (interior cells, period bound) over all UNSAT jobs.
fam = collections.defaultdict(list)
kinds = collections.defaultdict(set)
names = collections.defaultdict(set)
for r in rows:
    if r["status"] != "UNSAT":
        continue
    parts = r["label"].split("-")
    cls = {"E1": "E1 supersession", "E2": "E2 permutation targeting",
           "OWN": "own-kind (control)"}[parts[0]]
    if parts[0] == "E2":
        names[(cls, r["mode"], r["W"])].add(parts[1])
    fam[(cls, r["mode"], r["W"])].append((r["N"] - 2 * r["W"], r["p"]))
    kinds[(cls, r["mode"], r["W"])].add(r["n"])

print("| class | semantics | W | kinds n | box decided (interior cells / period) | verdict |")
print("|---|---|---|---|---|---|")
for k in sorted(fam):
    pts = fam[k]
    par = []
    for (c, p) in sorted(set(pts)):
        if not any(c2 >= c and p2 >= p and (c2, p2) != (c, p) for (c2, p2) in pts):
            par.append((c, p))
    cell = "; ".join("%d cells, p\u2264%d" % (c, p) for (c, p) in par)
    nk = "1\u2013%d" % max(kinds[k]) if len(kinds[k]) > 1 else str(max(kinds[k]))
    extra = ""
    if names.get(k):
        extra = " (cycle types " + ", ".join(sorted(names[k])) + ")"
    print("| %s%s | %s | %d | %s | %s | **UNSAT** |" % (k[0], extra, k[1], k[2], nk, cell))

tot = sum(r.get("secs", 0) for r in rows)
print("\nTotal solver time: %.0f CPU-seconds over %d jobs. "
      "Non-UNSAT results: %d." % (tot, len(rows), len(rows) - st["UNSAT"]))
