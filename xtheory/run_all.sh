#!/bin/sh
# run_all.sh — full reproduction of Expedition X-D.  ~25 min on one core.
set -u
cd "$(dirname "$0")"
mkdir -p data

echo "== 0. engines =="
python3 ../xnomos.py                          # the shared engine's own self-tests
python3 xlib.py                               # reference engine duel smoke test
clang -O2 -o census2    census2.c
sed -e 's/#define NW      3  /#define NW      5  /' \
    -e 's/#define MARGIN  20/#define MARGIN  28/' \
    -e 's/#define BASE    88/#define BASE    150/' \
    -e 's/#define MAXT    512/#define MAXT    1024/' census2.c > census2big.c
clang -O2 -o census2big census2big.c
python3 validate_c.py 4000 | tee data/validate_c.log

echo "== 1. the two-kind census (complete) =="
./census2    6 0 > data/census_parity.csv
./census2    6 1 > data/census_or.csv
./census2big 8 0 > data/census8_parity.csv
./census2big 8 1 > data/census8_or.csv

echo "== 2. analysis =="
python3 analyze.py _parity    > data/analyze6_parity.log
python3 analyze.py _or        > data/analyze6_or.log
python3 analyze.py 8_parity   > data/analyze8_parity.log
python3 analyze.py 8_or       > data/analyze8_or.log
python3 periodic_table.py 8_parity > data/ptable8_parity.log
python3 periodic_table.py 8_or     > data/ptable8_or.log

echo "== 3. theorem battery =="
python3 theorems.py > data/battery.log 2>&1 || true
tail -1 data/battery.log

echo "== 4. specimens and the sunset probe =="
python3 specimens.py > data/specimens.log
python3 sunset.py    > data/sunset.log

echo "== done =="
