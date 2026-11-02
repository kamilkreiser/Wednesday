#!/usr/bin/env bash
# usage: run_all.sh <tree> <label>
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937
T=$1; L=$2
OUT=$W/logs/suites_$L; mkdir -p $OUT
TD=$W/logs/tmp_$L; mkdir -p $TD
export TMPDIR=$TD
: > $OUT/summary.txt
for f in $T/Blockchain/Dev/scripts/__tests__/*.test.sh; do
  n=$(basename $f)
  bash $f > $OUT/$n.log 2>&1 < /dev/null; rc=$?
  echo "$n rc=$rc $(grep -E 'passed|SKIP' $OUT/$n.log | tail -1 | cut -c1-120)" >> $OUT/summary.txt
done
echo DONE >> $OUT/summary.txt
