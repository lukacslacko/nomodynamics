#!/usr/bin/env python3
"""
campaign.py — drive the complete state-space censuses of cross-amendment
nomic rings.  Every run enumerates the ENTIRE state space 2^(n*m) for every
constitution in the stated class: these are complete enumerations, not samples.

Usage:  python3 campaign.py <run>  where <run> in
   own      n=1 own-kind baseline, all 27 kinds, m=3..20 (parity == OR)
   recip    n=2 permutation (2-cycle) targets, all 729 rule pairs, m=3..11
   recip12  n=2 permutation, the 144 live-live pairs, m=12
   noninj   n=2 non-injective targets [0,0], all 729 pairs, m=3..11, parity
   noninjor n=2 non-injective targets [0,0], all 729 pairs, m=3..10, OR
   super1   n=1 supersession, all 27 kinds, m=3..20, both clear resolutions
   super2   n=2 supersession, all 729 rule pairs, m=3..10, both resolutions
   cyc3     n=3 cyclic permutation, live rules only (12^3), m=3..7
   cyc3all  n=3 cyclic permutation, all 27^3, m=3..5
   tgt3     n=3, every target map up to relabelling, live rules, m=3..6
Raw JSONL goes to $XR_RAW (default: ./raw); aggregates to ./data.
"""
import itertools
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("XR_RAW", os.path.join(HERE, "raw"))
DATA = os.path.join(HERE, "data")
os.makedirs(RAW, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

OFF = (-1, 0, 1)
RULES27 = [(a, b, c) for a in OFF for b in OFF for c in OFF]
RULES12 = [r for r in RULES27 if r[1] != 0 and r[0] != r[1]]
MODE = {"parity": 0, "or": 1, "super": 2, "super_or": 3}


def jobline(rules, targets, m, mode):
    parts = [str(len(rules)), str(m), str(MODE[mode])]
    for r, t in zip(rules, targets):
        parts += [str(r[0]), str(r[1]), str(r[2]), str(t)]
    return " ".join(parts)


def run(jobs, tag, goe=False):
    t0 = time.time()
    inp = "\n".join(jobs) + "\n"
    args = [os.path.join(HERE, "sweep")] + (["goe"] if goe else [])
    p = subprocess.run(args, input=inp, capture_output=True, text=True)
    if p.returncode:
        sys.exit("sweep failed: " + p.stderr[-800:])
    path = os.path.join(RAW, tag + ".jsonl")
    with open(path, "w") as f:
        f.write(p.stdout)
    n = p.stdout.count("\n")
    print("  [%s] %d jobs, %.1fs -> %s" % (tag, n, time.time() - t0, path),
          flush=True)
    return [json.loads(l) for l in p.stdout.splitlines()]


# ------------------------------------------------------------------ aggregate

def aggregate(recs, tag):
    """Per ring size: period set, max period, rotor classes, balance counts."""
    by_m = {}
    for r in recs:
        m = r["m"]
        d = by_m.setdefault(m, {"periods": {}, "rotors": {}, "nbal": 0,
                                "nbal_consts": 0, "consts": 0, "maxp": 0,
                                "maxp_const": None, "overflow": 0})
        d["consts"] += 1
        d["overflow"] += r["overflow"]
        for p, (cnt, mc, rep) in r["periods"].items():
            p = int(p)
            cur = d["periods"].get(p)
            if cur is None or mc < cur[0]:
                d["periods"][p] = [mc, rep, r["rules"], r["targets"]]
            if p > d["maxp"]:
                d["maxp"] = p
                d["maxp_const"] = [r["rules"], r["targets"], mc, rep]
        if r["nbal"]:
            d["nbal"] += r["nbal"]
            d["nbal_consts"] += 1
        for (p, rr, j, card, rep) in r["rotors"]:
            key = "%d,%d,%d" % (p, rr, j)
            cur = d["rotors"].get(key)
            if cur is None or card < cur[0]:
                d["rotors"][key] = [card, rep, r["rules"], r["targets"]]
    out = {}
    for m in sorted(by_m):
        d = by_m[m]
        out[str(m)] = {
            "consts": d["consts"], "overflow": d["overflow"],
            "period_set": sorted(d["periods"]),
            "maxp": d["maxp"], "maxp_const": d["maxp_const"],
            "period_min_witness": {str(k): v for k, v in
                                   sorted(d["periods"].items())},
            "rotor_classes": d["rotors"],
            "balanced_states": d["nbal"], "balanced_consts": d["nbal_consts"],
        }
    with open(os.path.join(DATA, tag + ".json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for m in sorted(by_m):
        d = out[str(m)]
        print("   m=%-3d consts=%-6d periods=%s maxp=%d rotor_classes=%d "
              "balanced=%d" % (m, d["consts"], d["period_set"][:14], d["maxp"],
                               len(d["rotor_classes"]), d["balanced_states"]),
              flush=True)
    return out


# ----------------------------------------------------------------- the runs

def do_own():
    jobs = [jobline([r], [0], m, "parity")
            for m in range(3, 21) for r in RULES27]
    aggregate(run(jobs, "own"), "own")


def do_recip():
    tgt = [1, 0]
    jobs = [jobline([r1, r2], tgt, m, "parity")
            for m in range(3, 12) for r1 in RULES27 for r2 in RULES27]
    aggregate(run(jobs, "recip"), "recip")


def do_recip12():
    tgt = [1, 0]
    jobs = [jobline([r1, r2], tgt, m, "parity")
            for m in (12,) for r1 in RULES12 for r2 in RULES12]
    aggregate(run(jobs, "recip12"), "recip12")


def do_noninj(mode="parity", hi=12, tag="noninj"):
    tgt = [0, 0]
    jobs = [jobline([r1, r2], tgt, m, mode)
            for m in range(3, hi) for r1 in RULES27 for r2 in RULES27]
    aggregate(run(jobs, tag), tag)


def do_super1():
    jobs = [jobline([r], [0], m, md)
            for md in ("super", "super_or")
            for m in range(3, 21) for r in RULES27]
    aggregate(run(jobs, "super1"), "super1")


def do_super2():
    jobs = [jobline([r1, r2], [0, 1], m, md)
            for md in ("super", "super_or")
            for m in range(3, 11) for r1 in RULES27 for r2 in RULES27]
    aggregate(run(jobs, "super2"), "super2")


def do_cyc3():
    tgt = [1, 2, 0]
    jobs = [jobline(list(c), tgt, m, "parity")
            for m in range(3, 8) for c in itertools.product(RULES12, repeat=3)]
    aggregate(run(jobs, "cyc3"), "cyc3")


def do_cyc3all():
    tgt = [1, 2, 0]
    jobs = [jobline(list(c), tgt, m, "parity")
            for m in range(3, 6) for c in itertools.product(RULES27, repeat=3)]
    aggregate(run(jobs, "cyc3all"), "cyc3all")


def do_tgt3():
    """All target maps on 3 kinds up to relabelling (5 classes), live rules."""
    maps = [(1, 2, 0),            # 3-cycle          (permutation)
            (1, 0, 2),            # transposition + fixed point (permutation)
            (0, 0, 1),            # non-injective, image {0,1}
            (1, 1, 0),            # non-injective, image {0,1}
            (0, 0, 0)]            # non-injective, image {0}
    jobs = [jobline(list(c), list(t), m, "parity")
            for t in maps for m in range(3, 7)
            for c in itertools.product(RULES12, repeat=3)]
    recs = run(jobs, "tgt3")
    for t in maps:
        sub = [r for r in recs if tuple(r["targets"]) == t]
        print("  target map %s:" % (t,))
        aggregate(sub, "tgt3_%d%d%d" % t)


def do_own2():
    """CONTROL: two kinds, own-kind targeting — same state space as `recip`
    and `noninj`, no cross-amendment.  Isolates what cross-amendment buys."""
    jobs = [jobline([r1, r2], [0, 1], m, "parity")
            for m in range(3, 12) for r1 in RULES27 for r2 in RULES27]
    aggregate(run(jobs, "own2"), "own2")


def do_own3():
    """CONTROL: three own-kind kinds, live rules — matches `cyc3`."""
    jobs = [jobline(list(c), [0, 1, 2], m, "parity")
            for m in range(3, 8) for c in itertools.product(RULES12, repeat=3)]
    aggregate(run(jobs, "own3"), "own3")


def do_super3():
    jobs = [jobline(list(c), [0, 1, 2], m, "super")
            for m in range(3, 8) for c in itertools.product(RULES12, repeat=3)]
    aggregate(run(jobs, "super3"), "super3")


def do_big2():
    """m = 12, 13 for the live-live two-kind classes (permutation + non-inj)."""
    jobs = [jobline([r1, r2], tg, m, "parity")
            for m in (12, 13) for tg in ([1, 0], [0, 0], [0, 1])
            for r1 in RULES12 for r2 in RULES12]
    aggregate(run(jobs, "big2"), "big2")


def do_goe():
    """Garden-of-Eden census on the live-live two-kind classes, m = 3..9."""
    jobs = [jobline([r1, r2], tg, m, md)
            for m in range(3, 10)
            for (tg, md) in (([0, 1], "parity"), ([1, 0], "parity"),
                             ([0, 0], "parity"), ([0, 1], "super"))
            for r1 in RULES12 for r2 in RULES12]
    aggregate(run(jobs, "goe", goe=True), "goe")


RUNS = {"own": do_own, "recip": do_recip, "recip12": do_recip12,
        "own2": do_own2, "own3": do_own3, "super3": do_super3,
        "big2": do_big2, "goe": do_goe,
        "noninj": do_noninj,
        "noninjor": lambda: do_noninj("or", 11, "noninjor"),
        "super1": do_super1, "super2": do_super2,
        "cyc3": do_cyc3, "cyc3all": do_cyc3all, "tgt3": do_tgt3}

if __name__ == "__main__":
    for name in sys.argv[1:]:
        print("== run %s ==" % name, flush=True)
        RUNS[name]()
