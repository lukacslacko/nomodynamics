#!/bin/bash
cd /Users/lukacs/claude/math/program/phase6/glider-question
for phase in w1core w2core super verify w1ext4 hunt56; do
  echo "=== PHASE $phase start $(date) ==="
  python3 sweep_all.py $phase
  echo "=== PHASE $phase end $(date) ==="
done
echo "CAMPAIGN COMPLETE"
