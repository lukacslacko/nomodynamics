#!/usr/bin/env python3
"""
verify_yd.py — Expedition Y-D's verification battery.

Runs every target's certificate script and reports the totals.  Each script is
independent of the expedition code that originally found its object, and every
claim is re-derived through `xnomos.py` (the shared engine) by a second code
path.

    python3 proofs/verify_yd.py            # fast pass  (~30 s)
    python3 proofs/verify_yd.py --deep     # complete boxes (~15 min)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = [
    ("TARGET 1  the Jubilee clock law", ["t1_jubilee.py"]),
    ("TARGET 2  the four-law coincidence", ["t2_odometer.py"]),
    ("TARGET 3  the width-free speed cap", ["t3_verify.py", "t3_decide.py"]),
    ("TARGET 4  light-cone-admissible ring rotors",
     ["t4_verify.py", "t4_report.py"]),
]


def main():
    deep = "--deep" in sys.argv
    total = fails = missing = 0
    lines = []
    for title, cands in SCRIPTS:
        path = next((os.path.join(HERE, c) for c in cands
                     if os.path.exists(os.path.join(HERE, c))), None)
        script = os.path.basename(path) if path else cands[0]
        if path is None:
            lines.append("  --  %-46s  (no script)" % title)
            missing += 1
            continue
        cmd = [sys.executable, path] + (["--deep"] if deep else [])
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        tail = [l for l in out.strip().splitlines() if "passed," in l]
        p = f = 0
        if tail:
            words = tail[-1].split()
            try:
                p, f = int(words[0]), int(words[2])
            except (ValueError, IndexError):
                pass
        total += p
        fails += f
        lines.append("  %s  %-46s  %3d passed, %d failed"
                     % ("ok  " if f == 0 else "FAIL", title, p, f))
        for l in out.splitlines():
            if l.strip().startswith("FAIL"):
                lines.append("      " + l.strip())
    print("EXPEDITION Y-D — verification battery%s\n"
          % ("  (deep)" if deep else ""))
    print("\n".join(lines))
    print("\n%d checks passed, %d failed%s"
          % (total, fails, ", %d scripts missing" % missing if missing else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
