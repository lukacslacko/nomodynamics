#!/bin/sh
set -e
cd /Users/lukacs/claude/math/program/phase6/xamend2d
python3 refine_alpha.py 1.05 > alpha_stage1.txt 2> /dev/null
python3 refine2.py > alpha_stage2.txt 2> /dev/null
echo REFINEDONE
