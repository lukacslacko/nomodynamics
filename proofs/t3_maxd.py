#!/usr/bin/env python3
"""t3_maxd.py -- lower bounds on max |d0| in the single-field W=1 sector.

For every class (512 parity / 343 OR -- i.e. for EVERY number of kinds) run
the CA from a fixed seed battery and record the generator (p0,d0) of every
glider found.  Lower bounds only; upper bounds come from t3_decide.py.
"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from t3_core import all_parity_classes, all_or_classes
from t3_fast import compile_rule, glider

def run(mode, nrand, span, steps, mspan):
    classes = all_parity_classes() if mode == "parity" else all_or_classes()
    rng = random.Random(4242)
    battery = [{i for i in range(12) if (m >> i) & 1} for m in range(1, 1 << 12)]
    for _ in range(nrand):
        sp = rng.randrange(2, span + 1)
        m = rng.getrandbits(sp) | 1 | (1 << (sp - 1))
        battery.append({i for i in range(sp) if (m >> i) & 1})
    best, per = {}, {}
    for i, cls in enumerate(classes):
        mt = compile_rule(cls, mode)
        mx = 0
        for S in battery:
            k, p, d, sp2 = glider(S, mt, max_steps=steps, max_span=mspan,
                                  max_card=mspan)
            if k == "GLIDER":
                mx = max(mx, abs(d))
                key = (p, d)
                if key not in best or sp2 < best[key][2]:
                    best[key] = (cls, sorted(S), sp2)
        per[cls] = mx
        if (i + 1) % 32 == 0:
            print("  %d/%d  max|d0| so far %d" % (i + 1, len(classes),
                                                  max(per.values())), flush=True)
    return best, per

if __name__ == "__main__":
    mode = sys.argv[1]
    nrand = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    best, per = run(mode, nrand, 20, 700, 260)
    mx = max(per.values())
    print("\nmode=%s  MAX |d0| found = %d" % (mode, mx))
    print("classes with some glider: %d/%d" % (sum(1 for v in per.values() if v), len(per)))
    from collections import Counter
    print("distribution of per-class max |d0|:", sorted(Counter(per.values()).items()))
    print("\nall minimal (p0,d0) found (%d):" % len(best))
    for k in sorted(best, key=lambda k: (-abs(k[1]), k[0])):
        cls, S, sp = best[k]
        print("   p0=%3d d0=%+4d class=%s seed=%s span=%d" % (k[0], k[1], cls, S, sp))
    json.dump({"best": {str(k): [list(v[0]), v[1], v[2]] for k, v in best.items()},
               "per_class": {str(k): v for k, v in per.items()}},
              open(os.path.join(HERE, "t3_maxd_%s.json" % mode), "w"))
