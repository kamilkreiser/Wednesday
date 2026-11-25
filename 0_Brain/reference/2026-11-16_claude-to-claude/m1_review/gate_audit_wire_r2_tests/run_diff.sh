#!/bin/bash
# R2 task 4: qa_diff.py (the first check's scripted session) twice per build, switch absent and --audit-a
W=/private/tmp/claude-501/qaw2
mkdir -p $W/logs/diff
for mode in off on; do
  for b in old head; do
    case $b in old) BIN=$W/to/debug ;; head) BIN=$W/t/debug ;; esac
    for n in 1 2; do
      extra=""; [ $mode = on ] && extra="--audit-a"
      date "+%T $mode $b $n"
      python3 -B $W/qa/qa_diff.py $BIN $W/d_${mode}_${b}_$n $W/logs/diff/${mode}_${b}_$n.json $extra > $W/logs/diff/${mode}_${b}_$n.out 2>&1; echo "rc=$?"
    done
  done
done
date +%T
