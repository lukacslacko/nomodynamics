#!/bin/sh
set -e
cd /Users/lukacs/claude/math/program/phase6/xamend2d
rm -f data/k3p.[0-9]* data/mp2.[0-9]* data/mo2.[0-9]*
./xcensus --mode 0 --sem 0 --steps 300 --dump data/mp2 > cen_moore_parity.txt 2>/dev/null
./xcensus --mode 0 --sem 1 --steps 300 --dump data/mo2 > cen_moore_or.txt 2>/dev/null
./xcensus --mode 2 --n 2000000 --seeds 2 --sem 0 --steps 300 --dump data/k3p > cen_3kind_parity.txt 2>/dev/null
./xcensus --mode 2 --n 2000000 --seeds 2 --sem 1 --steps 300 > cen_3kind_or.txt 2>/dev/null
./xcensus --mode 1 --sem 0 --steps 300 --seeds 1 > cen_vn255_parity.txt 2>/dev/null
./xcensus --mode 1 --sem 1 --steps 300 --seeds 1 > cen_vn255_or.txt 2>/dev/null
echo ALLDONE
