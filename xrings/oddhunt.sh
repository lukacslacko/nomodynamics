#!/bin/zsh
# Broad sampled rotor hunt on ODD rings.  Any hit is printed as JSON to
# odd_rotors.jsonl; per-batch summaries go to odd_hunt.log.
cd "$(dirname "$0")"
: > odd_rotors.jsonl
: > odd_hunt.log
seed=1
for n in 2 3 4; do
  for m in 5 7 9 11 13 15 17 19 21; do
    for mode in 0 1 2 3; do
      seed=$((seed+7919))
      ./hunt $n $m $mode 400 250 $seed 1 >> odd_rotors.jsonl 2>> odd_hunt.log
      seed=$((seed+7919))
      ./hunt $n $m $mode 400 250 $seed 0 >> odd_rotors.jsonl 2>> odd_hunt.log
    done
  done
done
# control: the SAME budget on even rings, to prove the hunt can see rotors
for n in 2 3 4; do
  for m in 6 8 10 12 14 16 18 20; do
    for mode in 0 1 2 3; do
      seed=$((seed+7919))
      ./hunt $n $m $mode 200 200 $seed 1 >> even_rotors.jsonl 2>> odd_hunt.log
    done
  done
done
