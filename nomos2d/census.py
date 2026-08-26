#!/usr/bin/env python3
"""Task 2: single-law census, all 125 types, both semantics.
Growth types get a 300-step dense run: shape metrics + growth exponent +
t=60 gallery snapshot; distinct shapes deduped modulo D4."""
import json, math
import numpy as np
from engine2d import (K, TYPES, tname, classify, np_run, canon_cells,
                      transform_cells, render_occ, enc)

def census_one(k, sem):
    v = classify([((0, 0), k)], sem=sem, max_steps=3000, growth_cap=1500,
                 hash_cap=80, d4_cap=60)
    return v

def shape_metrics(occ_cells):
    xs = [x for x, y in occ_cells]; ys = [y for x, y in occ_cells]
    w = max(xs) - min(xs) + 1; h = max(ys) - min(ys) + 1
    n = len(occ_cells)
    aspect = max(w, h) / min(w, h)
    fill = n / (w * h)
    st = set(occ_cells)
    bnd = sum(1 for (x, y) in st
              if (x+1, y) not in st or (x-1, y) not in st
              or (x, y+1) not in st or (x, y-1) not in st)
    return dict(bboxw=w, bboxh=h, aspect=round(aspect, 2),
                fill=round(fill, 3), boundary_ratio=round(bnd / n, 3), n=n)

def alpha_fit(sizes, t0=30):
    ts = np.arange(len(sizes))
    m = (ts >= t0) & (np.array(sizes) > 0)
    lt = np.log(ts[m]); ls = np.log(np.array(sizes)[m])
    A = np.vstack([lt, np.ones_like(lt)]).T
    (a, b), res, *_ = np.linalg.lstsq(A, ls, rcond=None)
    return round(float(a), 3)

def main():
    rows = []
    tallies = {"p": {}, "o": {}}
    for k in range(K):
        vp = census_one(k, "p")
        vo = census_one(k, "o")
        assert vp["v"] == vo["v"], (k, vp, vo)
        for sem, v in (("p", vp), ("o", vo)):
            key = v["v"] if v["v"] != "cycle" else f"cycle-{v['p']}"
            tallies[sem][key] = tallies[sem].get(key, 0) + 1
        rows.append((k, tname(k), vp))
    print("== SINGLE-LAW CENSUS (125 types) ==")
    print("parity tally:", dict(sorted(tallies["p"].items())))
    print("OR     tally:", dict(sorted(tallies["o"].items())))
    nontrivial = [(k, nm, v) for (k, nm, v) in rows if v["v"] not in ("fixed",)]
    print(f"\nnon-fixed types ({len(nontrivial)}):")
    for k, nm, v in nontrivial:
        print(f"  {nm} (k={k}): {v['v']}", {kk: v[kk] for kk in ("t", "t0", "p", "sz", "hw") if v.get(kk) is not None})

    # dense runs for all live (non-fixed, non-extinct) types
    growers = [(k, nm) for (k, nm, v) in rows
               if v["v"] in ("growth", "unresolved")]
    print(f"\ndense 300-step runs for {len(growers)} growth types:")
    gallery = {}
    ginfo = []
    for k, nm in growers:
        res = np_run([((0, 0), k)], 300, snaps=(60,))
        occ = [(x, y) for k2, cl in res["snaps"][60].items() for (x, y) in cl]
        occ300 = [(int(i) - res["R"], int(j) - res["R"])
                  for i, j in np.argwhere(res["occ"])]
        met = shape_metrics(occ300)
        al = alpha_fit(res["sizes"])
        s = res["sizes"]
        ginfo.append(dict(k=k, name=nm, alpha=al, size300=s[300],
                          maxsize=max(s), minsize_late=min(s[150:]), **met))
        # dedupe shape at t=60 modulo D4
        cells = [(x, y, 1) for (x, y) in occ]
        ck = min(canon_cells(transform_cells(cells, g))[0] for g in range(8))
        gallery.setdefault(ck, []).append((nm, occ))
        print(f"  {nm}: alpha={al} size300={s[300]} max={max(s)} "
              f"bbox={met['bboxw']}x{met['bboxh']} fill={met['fill']} "
              f"bnd={met['boundary_ratio']}")

    print(f"\n== GROWTH-SHAPE GALLERY: {len(gallery)} distinct shapes mod D4 ==")
    out = []
    for i, (ck, members) in enumerate(gallery.items()):
        names = [nm for nm, _ in members]
        occ = members[0][1]
        art = render_occ(occ, maxw=44, maxh=44)
        blk = f"--- shape class {i+1}: types {', '.join(names)}  (t=60) ---\n{art}"
        print(blk)
        out.append(blk)

    json.dump(dict(tally_p=tallies["p"], tally_o=tallies["o"],
                   nontrivial=[(k, nm, {a: b for a, b in v.items() if a != 'sizes'})
                               for k, nm, v in nontrivial],
                   growth_info=ginfo),
              open("census_out.json", "w"), indent=1)
    with open("census_gallery.txt", "w") as f:
        f.write("\n\n".join(out))
    print("\nwrote census_out.json, census_gallery.txt")

if __name__ == "__main__":
    main()
