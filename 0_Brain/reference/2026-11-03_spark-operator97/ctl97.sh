#!/bin/bash
# controls one by one (round.sh --control), retrying while BUSY (rc 3); bound 3h via STOP file / pass list
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator97; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
echo started $(date) pid $$ >> $O/ctl97.log
for k in p1 p2 p3 p4 p5 p6 p7 p8 p9; do
  d=$(ls -d $S/night/briefs/ks_1868_o97_${k}_*); tries=0
  while [ ! -e $O/STOP ] && [ $tries -lt 40 ]; do
    bash $S/spark/round.sh $d --control > $O/ctlrun_$k.out 2>&1; rc=$?
    echo "$(date +%T) $k control rc=$rc" >> $O/ctl97.log
    [ $rc -ne 3 ] && break
    tries=$((tries+1)); sleep 30
  done
done
echo exited $(date) >> $O/ctl97.log
