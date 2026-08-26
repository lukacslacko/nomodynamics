#!/bin/sh
# Cryptid escalation: the census's UNRESOLVED pool, deeper and deeper.
set -e
cd /Users/lukacs/claude/math/program/phase6/xamend2d
echo "stage B: 3000 steps on $(wc -l < data/unres_batch.txt) experiments"
./xcensus --mode 10 --sem 0 --steps 3000 --threads 12 < data/unres_batch.txt > data/escB.txt
paste -d' ' data/escB.txt data/unres_batch.txt | awk '$1=="unres"' | cut -d' ' -f10- > data/escB_survivors.txt
echo "stage B survivors: $(wc -l < data/escB_survivors.txt)"
echo "stage C: 30000 steps"
./xdeep --mode 10 --sem 0 --steps 30000 --threads 12 < data/escB_survivors.txt > data/escC.txt
paste -d' ' data/escC.txt data/escB_survivors.txt | awk '$1=="unres"' | cut -d' ' -f10- > data/escC_survivors.txt
echo "stage C survivors: $(wc -l < data/escC_survivors.txt)"
head -3000 data/escC_survivors.txt > data/escD_in.txt
echo "stage D: 300000 steps on $(wc -l < data/escD_in.txt) sampled survivors"
./xdeep --mode 10 --sem 0 --steps 300000 --threads 12 < data/escD_in.txt > data/escD.txt
echo "stage D verdicts:"; cut -d' ' -f1 data/escD.txt | sort | uniq -c
echo ESCDONE
