#!/bin/bash
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator96
k=$1; d=$(ls -d $S/night/briefs/ks_1868_o96_${k}_*)
python3 $S/spark/brief_lint.py $d > $W/lint_$k.out 2> $W/lint_$k.err; echo "$k lint rc=$?"; /usr/bin/grep -i REFUSED $W/lint_$k.err | cut -c1-300
bash $S/spark/round.sh $d --dry-run > $W/dry_$k.out 2> $W/dry_$k.err; echo "$k dry rc=$?"; tail -1 $W/dry_$k.out | cut -c1-200; /usr/bin/grep -i -E 'REFUSED|HARNESS|BUSY' $W/dry_$k.err $W/dry_$k.out | cut -c1-300
