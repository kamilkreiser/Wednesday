#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator50; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
n=$1; shift
for k in "$@"; do d=$(ls -d $B/ks_1868_o50_${k}_*); nice -n 10 bash $S/spark/round.sh $d --control > $O/ctl${n}_$k.out 2> $O/ctl${n}_$k.err; echo "$k ctl$n rc=$?" >> $O/stages.log; done
echo CTL${n}DONE >> $O/stages.log
