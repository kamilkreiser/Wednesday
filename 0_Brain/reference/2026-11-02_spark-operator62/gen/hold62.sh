#!/bin/bash
# hold61.sh <p1|p2|p3> <LABEL>: run dirs read from spark/done.md rows (control row = '-control' dir, model row = the other)
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator62; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
k=$1; t=$2; K=$(echo $k | tr p P)
br=$(ls -d $B/ks_1868_o62_${k}_*)
ctl=$(/usr/bin/grep "o62_${k}_" $S/spark/done.md | /usr/bin/grep -i "CONTROL-PASS" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
run=$(/usr/bin/grep "o62_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-PASS" | /usr/bin/grep "PASS (7/7)" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
echo "ctl=$ctl run=$run"
nice -n 10 python3 $S/night/hold_ready.py $run $ctl KS-1868-O62-$K $t --brief $br/KS-1868.md --model-tag spark-dsv4flash >$R/hold_$k.out 2>$R/hold_$k.err; echo "$k hold rc=$?"; cat $R/hold_$k.out $R/hold_$k.err | cut -c1-500
