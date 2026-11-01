#!/bin/bash
# retries round.sh --dry-run / --control until it is not BUSY (never touches the lock itself)
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator56
k=$1; d=$2; mode=$3
for i in $(seq 1 120); do
  bash $L/spark/round.sh $L/night/briefs/$d $mode > $O/${mode#--}_$k.out 2> $O/${mode#--}_$k.err
  rc=$?
  [ $rc -ne 3 ] && break
  sleep 5
done
echo "rc=$rc tries=$i" > $O/${mode#--}_$k.rc
