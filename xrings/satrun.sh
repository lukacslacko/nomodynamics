#!/bin/zsh
cd "$(dirname "$0")"
: > sat_odd.log
python3 satrotor.py odd1 0 1 >> sat_odd.log 2>&1 &
for s in 0 1 2 3; do python3 satrotor.py odd2 $s 4 >> sat_odd.log 2>&1 & done
wait
for s in 0 1 2 3 4 5; do python3 satrotor.py odd3 $s 6 >> sat_odd.log 2>&1 & done
python3 satrotor.py even2 0 1 >> sat_odd.log 2>&1 &
wait
echo DONE >> sat_odd.log
