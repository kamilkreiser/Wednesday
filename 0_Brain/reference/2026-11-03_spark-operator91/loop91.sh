#!/bin/bash
# advance91 every 30 s until the stop file exists or 300 polls; model lines are queued only for passes with an OKQ_<pN> marker file
N=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator91; i=0
echo started $(date) pid $$ >> $N/loop91.log
while [ $i -lt 300 ] && [ ! -e $N/STOP ]; do bash $N/advance91.sh 2>&1 | /usr/bin/grep -- '->' >> $N/loop91.log; sleep 30; i=$((i+1)); done
echo exited $(date) >> $N/loop91.log
