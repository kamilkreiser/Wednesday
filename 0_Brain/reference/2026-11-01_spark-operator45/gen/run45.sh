#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator45; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
for k in p1 p2 p3 p4; do
  d=$(ls -d $B/ks_1868_o45_${k}_*)
  nice -n 10 bash $S/spark/round.sh $d --control >$O/control_$k.out 2>$O/control_$k.err; echo "$k control rc=$?" >> $O/rounds.log
  nice -n 10 bash $S/spark/round.sh $d --dry-run >$O/predry_$k.out 2>$O/predry_$k.err; echo "$k predry rc=$?" >> $O/rounds.log
  nice -n 10 bash $S/spark/round.sh $d >$O/round_$k.out 2>$O/round_$k.err; echo "$k round rc=$?" >> $O/rounds.log
done
echo ALLDONE >> $O/rounds.log
