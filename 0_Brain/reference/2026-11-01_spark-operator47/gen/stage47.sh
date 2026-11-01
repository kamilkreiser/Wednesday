#!/bin/bash
# usage: stage47.sh <p1..p5> <lint|dry|control|round> [suffix]
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator47; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
k=$1; st=$2; sfx=$3
d=$(ls -d $B/ks_1868_o47_${k}_*)
case $st in
 lint) python3 $S/spark/brief_lint.py $d >$O/lint${sfx}_$k.out 2>$O/lint${sfx}_$k.err ;;
 dry) nice -n 10 bash $S/spark/round.sh $d --dry-run >$O/dry${sfx}_$k.out 2>$O/dry${sfx}_$k.err ;;
 control) nice -n 10 bash $S/spark/round.sh $d --control >$O/ctl${sfx}_$k.out 2>$O/ctl${sfx}_$k.err ;;
 round) nice -n 10 bash $S/spark/round.sh $d >$O/rnd${sfx}_$k.out 2>$O/rnd${sfx}_$k.err ;;
esac
echo "$k $st$sfx rc=$?" | tee -a $O/stages.log
