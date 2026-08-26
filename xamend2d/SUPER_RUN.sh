#!/bin/sh
set -e
cd /Users/lukacs/claude/math/program/phase6/xamend2d
./xcensus --mode 0 --sem 2 --steps 300 > cen_moore_super.txt 2>/dev/null
./xcensus --mode 2 --n 1000000 --seeds 2 --sem 2 --steps 300 > cen_3kind_super.txt 2>/dev/null
echo SUPERDONE
