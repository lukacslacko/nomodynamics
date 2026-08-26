#!/bin/sh
set -e
cd /Users/lukacs/claude/math/program/phase6/xamend2d
./escalate.sh
./SUPER_RUN.sh
rm -f data/ap2.0 data/ap2.1 data/ap2.2 data/ap2.3 data/ap2.4 data/ap2.5 data/ap2.6 data/ap2.7 data/ap2.8 data/ap2.9 data/ap2.10 data/ap2.11
./xcensus --mode 0 --sem 0 --steps 300 --alpha 1 --dump data/ap2 > cen_moore_parity_alpha.txt 2>/dev/null
cat data/ap2.0 data/ap2.1 data/ap2.2 data/ap2.3 data/ap2.4 data/ap2.5 data/ap2.6 data/ap2.7 data/ap2.8 data/ap2.9 data/ap2.10 data/ap2.11 > data/moore_alpha_raw.txt
rm -f data/ap2.0 data/ap2.1 data/ap2.2 data/ap2.3 data/ap2.4 data/ap2.5 data/ap2.6 data/ap2.7 data/ap2.8 data/ap2.9 data/ap2.10 data/ap2.11
echo RUNALLDONE
