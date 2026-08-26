#!/usr/bin/env python3
"""t3_gensweep.py -- EXACT census of realisable generators (p0,d0).

decide_generator settles, for each class and each (p,d), whether some glider
has generator exactly (p,d) -- with no bound on the pattern width.  Sweeping
all 512 parity / 343 OR classes settles the single-field W=1 sector for EVERY
number of kinds.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from t3_core import all_parity_classes, all_or_classes
from t3_decide import decide_generator, check_witness, minimal_pd, witness_seed

def main():
    mode = sys.argv[1]; pmax = int(sys.argv[2])
    classes = all_parity_classes() if mode == "parity" else all_or_classes()
    out = os.path.join(HERE, "t3_gen_%s_p%d.jsonl" % (mode, pmax))
    t0 = time.time(); ncap = 0; gens = {}
    with open(out, "w") as fh:
        for i, cls in enumerate(classes):
            for p in range(1, pmax + 1):
                for d in range(1, p + 1):
                    v, cols = decide_generator(cls, p, d, mode)
                    rec = {"cls": list(cls), "p": p, "d": d, "verdict": v}
                    if v == "GLIDER":
                        assert check_witness(cls, cols, p, d, mode)
                        m = minimal_pd(cls, cols, p, d, mode)
                        assert m == (p, d), (cls, p, d, m)
                        rec["seed"] = witness_seed(cols)
                        gens.setdefault((p, d), (cls, rec["seed"]))
                    if v == "CAP":
                        ncap += 1
                    fh.write(json.dumps(rec) + "\n")
            if (i + 1) % 64 == 0:
                print("  %d/%d  %.0fs  CAP=%d  maxd0=%d"
                      % (i + 1, len(classes), time.time() - t0, ncap,
                         max((d for _, d in gens), default=0)), flush=True)
    print("\nmode=%s  pmax=%d  CAP=%d" % (mode, pmax, ncap))
    print("REALISABLE GENERATORS (p0,d0), p0 <= %d, ANY number of kinds, "
          "ANY pattern width:" % pmax)
    for k in sorted(gens):
        cls, seed = gens[k]
        print("   (p0,d0)=%-8s  e.g. class=%s seed=%s" % (str(k), cls, seed))
    print("   max d0 = %d" % max((d for _, d in gens), default=0))
    print("NOT realisable as a generator (p0<=%d): %s"
          % (pmax, [ (p,d) for p in range(1,pmax+1) for d in range(1,p+1)
                     if (p,d) not in gens ]))
    print("wrote", out)

if __name__ == "__main__":
    main()
