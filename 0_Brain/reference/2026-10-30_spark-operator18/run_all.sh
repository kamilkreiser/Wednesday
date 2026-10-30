#!/bin/bash
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark
B=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator18
for d in "$@"; do
  git -C /Volumes/DevMASTER/'!CODING'/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop > $R/lsremote_$d.txt 2>&1
  python3 -I $S/brief_lint.py $B/$d > $R/lint_$d.log 2>&1; echo "lint rc=$?" >> $R/lint_$d.log
  bash $S/round.sh $B/$d --dry-run > $R/dry_$d.log 2>&1; echo "dry rc=$?" >> $R/dry_$d.log
  bash $S/round.sh $B/$d --control > $R/control_$d.log 2>&1; echo "control rc=$?" >> $R/control_$d.log
done
echo DONE > $R/run_all_18.done
