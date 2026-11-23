#!/bin/bash
W=/private/tmp/claude-501/qla2; R=$W/dg; O=$W/dg_out
for run in main head plant; do
  case $run in main) B=$W/tmain/debug; X="";; head) B=$W/thead/debug; X="";; plant) B=$W/thead/debug; X="--plant";; esac
  s=$(date +%s); python3 -B $W/s/diff_gate.py $B $R $O/$run.jsonl $X > $O/$run.log 2>&1; echo "$run exit $? $(( $(date +%s)-s ))s" >> $O/runs.txt
  mv $R $W/dg_root_$run
done
python3 -B $W/s/cmp.py $O/main.jsonl $O/head.jsonl > $O/cmp_main_head.txt 2>&1; echo "cmp main/head exit $?" >> $O/runs.txt
python3 -B $W/s/cmp.py $O/main.jsonl $O/plant.jsonl > $O/cmp_main_plant.txt 2>&1; echo "cmp main/plant exit $?" >> $O/runs.txt
