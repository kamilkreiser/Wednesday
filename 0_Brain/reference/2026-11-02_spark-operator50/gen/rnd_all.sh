#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator50; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
for k in "$@"; do d=$(ls -d $B/ks_1868_o50_${k}_*); nice -n 10 bash $S/spark/round.sh $d > $O/rnd1_$k.out 2> $O/rnd1_$k.err; echo "$k rnd rc=$?" >> $O/stages.log; done
echo RNDDONE >> $O/stages.log
