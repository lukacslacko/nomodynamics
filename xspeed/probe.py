#!/usr/bin/env python3
"""
probe.py — X-E's extensions of X-A's instrument.

Everything here goes THROUGH `xsat.build` / `xsat.solve` unchanged; the only
addition is the ability to give the three offset slots of a rule *different*
windows.  X-A's `W` sets one common window for `a`, `b` and `c`; here

    Wa  — the window of the enabling guard offset a
    Wb  — the window of the disabling guard offset b
    Wc  — the window of the emission offset c

can be set independently (each <= W).  Implementation: build the CNF with the
larger window W, then add unit clauses forbidding the one-hot trits outside the
smaller per-slot window.  Nothing in the semantics changes, so UNSAT is still a
complete decision for the restricted class, and every SAT model still passes
through `xsat.certify` (`xnomos.verify_glider`).
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
XA = os.path.join(os.path.dirname(HERE), "xamend1d")
sys.path.insert(0, XA)
sys.path.insert(0, os.path.dirname(HERE))

import xsat            # noqa: E402
from xsat import Spec  # noqa: E402


def build_restricted(sp: Spec, Wa=None, Wb=None, Wc=None):
    C, meta = xsat.build(sp)
    offs = meta["offs"]
    for arr_name, lim in (("A", Wa), ("B", Wb), ("Cc", Wc)):
        if lim is None:
            continue
        arr = meta[arr_name]
        for k in range(sp.n):
            for vi, v in enumerate(offs):
                if abs(v) > lim:
                    lit = arr[k][vi]
                    if lit is True:
                        C.add()          # unsatisfiable: pinned outside window
                    elif lit is not False:
                        C.add(-lit)
    return C, meta


def solve_restricted(sp: Spec, Wa=None, Wb=None, Wc=None, solver="cadical195"):
    return xsat.solve(sp, solver=solver,
                      built=build_restricted(sp, Wa, Wb, Wc))


def job(kw):
    """Job entry for run.py-style pools.  kw carries _label, _Wa/_Wb/_Wc."""
    import time
    kw = dict(kw)
    lab = kw.pop("_label", "")
    Wa, Wb, Wc = kw.pop("_Wa", None), kw.pop("_Wb", None), kw.pop("_Wc", None)
    t0 = time.time()
    try:
        sp = Spec(**kw)
        st, info = solve_restricted(sp, Wa, Wb, Wc)
    except AssertionError as e:
        return dict(label=lab, status="BUG", note=str(e)[:600])
    except Exception as e:                                   # pragma: no cover
        return dict(label=lab, status="ERR", note=repr(e)[:400])
    out = dict(label=lab, status=st, secs=round(time.time() - t0, 2),
               n=sp.n, W=sp.W, N=sp.N, p=sp.p, d=sp.d, mode=sp.mode,
               Wa=Wa, Wb=Wb, Wc=Wc)
    if st == "SAT":
        out["rules"] = info["rules"]
        out["tgt"] = [list(x) for x in info["targets"]]
        out["seed"] = {str(k): v for k, v in info["frames"][0].items() if v}
        out["certified"] = info["certified"]
    return out


if __name__ == "__main__":
    import json
    from multiprocessing import Pool
    jobs = json.load(open(sys.argv[1]))
    outfile = sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    done = set()
    if os.path.exists(outfile):
        for line in open(outfile):
            if line.strip():
                done.add(json.loads(line)["label"])
    jobs = [j for j in jobs if j["_label"] not in done]
    print("%d jobs, %d workers" % (len(jobs), workers))
    with open(outfile, "a") as fh, Pool(workers) as pool:
        for i, r in enumerate(pool.imap_unordered(job, jobs, chunksize=1)):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print("[%3d/%3d] %-40s %-6s %6.1fs"
                  % (i + 1, len(jobs), r["label"], r["status"],
                     r.get("secs", 0)), flush=True)
