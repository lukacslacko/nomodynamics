#!/usr/bin/env python3
"""sweep2.py — width-unbounded frontier, organised by (p,d).

  python3 sweep2.py n W pmax out.jsonl [workers] [cap] [maxsecs]

For each (p, d, mode) it scans EVERY full-target constitution with n live
channels and reports:
   GLIDER  — a certified specimen exists (no width bound)
   NONE    — no glider of that (p,d) exists for ANY full-target constitution
             with n channels, at ANY width          <-- the strong statement
   CAP     — at least one constitution exceeded the state cap: undecided
"""
import itertools, json, os, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "xamend1d"))
sys.path.insert(0, os.path.dirname(HERE))
import sft

def live(W):
    return [(a,b,c) for a in range(-W,W+1) for b in range(-W,W+1)
            for c in range(-W,W+1) if a != b]

def one(arg):
    chans, W, p, d, mode, cap = arg
    cmax = max(c for _,_,c in chans); cmin = min(c for _,_,c in chans)
    if cmax < 1 or cmin > 0 or d > p*cmax:
        return ("PRUNED", None, chans, 0.0)
    t0 = time.time()
    v, w = sft._search_cycle(sft.step_table(list(chans), W, mode), W, p, d, cap)
    return (v, w, chans, round(time.time()-t0, 2))

def main():
    n, W, pmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    outfile = sys.argv[4]
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else 1_500_000
    cons = list(itertools.combinations_with_replacement(live(W), n))
    done = set()
    if os.path.exists(outfile):
        for l in open(outfile):
            r = json.loads(l); done.add((r['p'], r['d'], r['mode']))
    print("n=%d W=%d: %d constitutions" % (n, W, len(cons)), flush=True)
    fh = open(outfile, "a")
    pool = Pool(workers)
    for p in range(1, pmax+1):
        for d in range(1, p*W+1):
            for mode in ("parity", "or"):
                if (p, d, mode) in done: continue
                t0 = time.time(); caps = 0; hit = None
                args = [(c, W, p, d, mode, cap) for c in cons]
                for v, w, chans, secs in pool.imap_unordered(one, args, chunksize=8):
                    if v == "CAP": caps += 1
                    elif v == "GLIDER" and hit is None:
                        hit = (chans, sft.witness_state(w, p),
                               sft.verify(list(chans), w, p, d, mode, n))
                rec = dict(n=n, W=W, p=p, d=d, mode=mode,
                           verdict=("GLIDER" if hit else ("CAP" if caps else "NONE")),
                           caps=caps, secs=round(time.time()-t0, 1))
                if hit:
                    rec["chans"] = [list(x) for x in hit[0]]
                    rec["cells"] = hit[1]; rec["verified"] = hit[2]
                fh.write(json.dumps(rec)+"\n"); fh.flush()
                print("p=%d d=%d %-6s %-7s caps=%d %.0fs %s"
                      % (p, d, mode, rec["verdict"], caps, rec["secs"],
                         rec.get("chans","")), flush=True)

if __name__ == "__main__":
    main()
