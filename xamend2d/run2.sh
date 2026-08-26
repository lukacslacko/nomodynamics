#!/bin/sh
set -e
cd /Users/lukacs/claude/math/program/phase6/xamend2d
rm -f data/ap2.[0-9]*
./xcensus --mode 0 --sem 0 --steps 300 --alpha 1 --dump data/ap2 > cen_moore_parity_alpha.txt 2>/dev/null
for f in data/ap2.[0-9]*; do cat "$f"; echo; done > data/moore_alpha_raw.txt
rm -f data/ap2.[0-9]*
echo ALPHADONE
