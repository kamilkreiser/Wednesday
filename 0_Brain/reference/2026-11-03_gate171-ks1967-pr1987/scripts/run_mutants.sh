#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate171-ks1967-pr1987
: > $W/runs/mutants_raw.tsv
for m in $W/mut/m*.ts; do
  id=$(basename $m .ts)
  bash $W/scripts/run_new.sh "mut_$id" $m "--hookTimeout=120000 --reporter=json --outputFile=$W/runs/mut_$id.json" > /dev/null
  python3 -I -c "
import json;d=json.load(open('$W/runs/mut_$id.json'));print('$id', d['numFailedTests'], d['numPassedTests'], d['numTotalTests'], sep='\t')" >> $W/runs/mutants_raw.tsv
done
