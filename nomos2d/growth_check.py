#!/usr/bin/env python3
"""Dense-run analysis of survey growth seeds: growth exponent alpha,
shape metrics, 2D-ness; dedupe distinct shape classes; render examples."""
import json, sys
import numpy as np
from multiprocessing import Pool
from engine2d import np_run, tname, render_occ

def analyze(args):
    i, spec = args
    T = 250
    res = np_run(spec, T, snaps=(60,))
    s = res["sizes"]
    T2 = len(s) - 1
    occ = res["occ"]; R = res["R"]
    pts = np.argwhere(occ)
    if len(pts) == 0:
        return i, dict(v="died")
    x0, y0 = pts.min(axis=0) - R; x1, y1 = pts.max(axis=0) - R
    w, h = int(x1 - x0 + 1), int(y1 - y0 + 1)
    n = int(len(pts))
    ts = np.arange(len(s))
    m = (ts >= max(20, T2 // 4)) & (np.array(s) > 0)
    lt, ls = np.log(ts[m]), np.log(np.array(s)[m])
    A = np.vstack([lt, np.ones_like(lt)]).T
    (al, _), *_ = np.linalg.lstsq(A, ls, rcond=None)
    st = set(map(tuple, (pts - R).tolist()))
    bnd = sum(1 for (x, y) in st
              if (x+1, y) not in st or (x-1, y) not in st
              or (x, y+1) not in st or (x, y-1) not in st)
    snap = sorted((x, y) for cl in res["snaps"].get(60, {}).values()
                  for (x, y) in cl) if res["snaps"] else []
    return i, dict(v="ok", alpha=round(float(al), 3), size=s[T2], T=T2,
                   bbox=(w, h), mindim=min(w, h), fill=round(n / (w * h), 3),
                   bnd=round(bnd / n, 3), snap60=snap,
                   truncated=res["truncated"])

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "survey_main.json"
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    d = json.load(open(src))
    pool_specs = [tuple((tuple(p), k) for p, k in s)
                  for s, v in d["keep"]["unres-grow"]][:nmax]
    print(f"{len(pool_specs)} growth seeds from {src}")
    out = [None] * len(pool_specs)
    with Pool(10) as pool:
        for i, r in pool.imap_unordered(analyze, enumerate(pool_specs), chunksize=4):
            out[i] = r
    ok = [(s, r) for s, r in zip(pool_specs, out) if r["v"] == "ok"]
    als = sorted(r["alpha"] for _, r in ok)
    print(f"alpha distribution over {len(ok)}: "
          f"min={als[0]} p25={als[len(als)//4]} med={als[len(als)//2]} "
          f"p75={als[3*len(als)//4]} max={als[-1]}")
    wide = [(s, r) for s, r in ok if r["mindim"] > 6]
    print(f"2D-ish (bbox min dim > 6): {len(wide)} of {len(ok)}")
    hi = [(s, r) for s, r in ok if r["alpha"] > 1.3]
    print(f"alpha > 1.3: {len(hi)}")
    for s, r in sorted(hi, key=lambda x: -x[1]["alpha"])[:12]:
        print("  ", [(p, tname(k)) for p, k in s],
              {a: r[a] for a in ("alpha", "size", "bbox", "fill", "bnd")})
    for s, r in sorted(wide, key=lambda x: -x[1]["mindim"])[:12]:
        print("  wide:", [(p, tname(k)) for p, k in s],
              {a: r[a] for a in ("alpha", "size", "bbox", "fill", "bnd")})
    json.dump([( [list(x) for x in s], {a: b for a, b in r.items() if a != "snap60"})
               for s, r in ok],
              open("growth_check_" + src, "w"))
    # render the 3 most 2D examples
    for s, r in sorted(ok, key=lambda x: -x[1]["mindim"])[:3]:
        print("---", [(p, tname(k)) for p, k in s], "t=60, metrics",
              {a: r[a] for a in ("alpha", "bbox", "fill")})
        print(render_occ(r["snap60"], maxw=60, maxh=44))
    print("wrote growth_check_" + src)

if __name__ == "__main__":
    main()
