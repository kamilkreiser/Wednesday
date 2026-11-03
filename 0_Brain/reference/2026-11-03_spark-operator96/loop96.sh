#!/bin/bash
# advance96 every 30 s until STOP or 300 polls (~2.5 h); restarts the drainer if the queue has lines and no drainer is live (queue.lock guards duplicates)
N=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator96; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark; i=0
echo started $(date) pid $$ >> $N/loop96.log
while [ $i -lt 300 ] && [ ! -e $N/STOP ]; do
  bash $N/advance96.sh 2>&1 | /usr/bin/grep -- '->' >> $N/loop96.log
  if [ -n "$(/usr/bin/grep -v -e '^#' -e '^[[:space:]]*$' $S/queue.md)" ]; then nohup bash $S/queue.sh >> $S/state/queue.log 2>&1 & fi
  sleep 30; i=$((i+1))
done
echo exited $(date) >> $N/loop96.log
