#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator45; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
for k in p1 p2 p3 p4; do
  d=$(ls -d $B/ks_1868_o45_${k}_*)
  nice -n 10 bash $S/spark/round.sh $d --control >$O/ctl_$k.out 2>$O/ctl_$k.err; rc=$?; echo "$k control rc=$rc" >> $O/rounds2.log
  [ $rc -ne 0 ] && continue
  nice -n 10 bash $S/spark/round.sh $d --dry-run >$O/pre_$k.out 2>$O/pre_$k.err; rc=$?; echo "$k predry rc=$rc" >> $O/rounds2.log
  [ $rc -ne 0 ] && continue
  nice -n 10 bash $S/spark/round.sh $d >$O/rnd_$k.out 2>$O/rnd_$k.err; echo "$k round rc=$?" >> $O/rounds2.log
done
echo ALLDONE >> $O/rounds2.log
