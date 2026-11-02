#!/bin/bash
# advance89 every 30 s until the stop file exists or 180 polls
N=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator89; i=0
echo started $(date) >> $N/loop89.log
while [ $i -lt 180 ] && [ ! -e $N/STOP ]; do bash $N/advance89.sh 2>&1 | /usr/bin/grep -- '->' >> $N/loop89.log; sleep 30; i=$((i+1)); done
echo exited $(date) >> $N/loop89.log
