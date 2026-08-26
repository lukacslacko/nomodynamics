#!/usr/bin/env python3
"""Deep probe of one holdout: frontier burst record, size stats, recurrence
hashing over a long run."""
import sys, json
from engine2d import (to_state, step_p, decode_state, sizeof, canon_cells,
                      tname, state_hw)

def probe(spec, T, hash_all=True, report_every=None):
    S = to_state(spec)
    seen = {}
    bursts = []
    hw = -1
    szmax = 0
    szsum = 0
    rec = None
    for t in range(T + 1):
        if not S:
            print(f"extinct at {t}")
            return
        sz = sizeof(S)
        szsum += sz
        if sz > szmax:
            szmax = sz
        w = state_hw(S)
        if w > hw:
            hw = w
            bursts.append((t, w, sz))
        if hash_all and sz <= 300:
            key, cx, cy = canon_cells(decode_state(S))
            hit = seen.get(key)
            if hit is not None:
                rec = (hit, t, cx - hit[1], cy - hit[2])
                print(f"RECURRENCE: t0={hit[0]} t={t} p={t-hit[0]} d=({cx-hit[1]},{cy-hit[2]})")
                break
            seen[key] = (t, cx, cy)
        S = step_p(S)
    print(f"T={T}: no recurrence" if rec is None else "")
    print(f"max size {szmax}, mean size {szsum/(T+1):.1f}, final hw {hw}")
    print(f"{len(bursts)} frontier advances; (t, hw, sz) at each advance (last 40):")
    comp = []
    for i, (t, w, sz) in enumerate(bursts):
        comp.append(f"{t}:{w}")
    print("  " + " ".join(comp[-60:]))
    return bursts, szmax

if __name__ == "__main__":
    spec = [((-1, 0), 48), ((-1, 1), 119), ((0, 1), 66)]
    if len(sys.argv) > 1:
        spec = [(tuple(p), k) for p, k in json.loads(sys.argv[1])]
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 300000
    print("spec:", [(p, tname(k)) for p, k in spec])
    probe(spec, T)
