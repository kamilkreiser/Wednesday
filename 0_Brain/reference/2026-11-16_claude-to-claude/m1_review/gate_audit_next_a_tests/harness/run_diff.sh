#!/bin/bash
# QA-AUDIT-NEXT-A (c): qa_diff.py twice per build, switch absent and --audit-a
W=/private/tmp/claude-501/qana
for mode in off on; do
  for b in base head; do
    case $b in base) BIN=$W/tb/debug ;; head) BIN=$W/t/debug ;; esac
    for n in 1 2; do
      extra=""; [ $mode = on ] && extra="--audit-a"
      date "+%T $mode $b $n"
      python3 -B $W/h/qa_diff.py $BIN $W/d/${mode}_${b}_$n $W/logs/diff/${mode}_${b}_$n.json $extra > $W/logs/diff/${mode}_${b}_$n.out 2>&1; echo "rc=$?"
    done
  done
done
date +%T
