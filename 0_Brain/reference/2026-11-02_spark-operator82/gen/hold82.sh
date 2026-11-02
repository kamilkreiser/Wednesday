#!/bin/bash
# hold81.sh <a1|b1..> <KEY> <LABEL>: run dirs read from spark/done.md rows (control row = CONTROL-PASS, model row = the PASS (7/7))
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator82; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
k=$1; key=$2; t=$3; K=$(echo $k | tr a-z A-Z)
br=$(ls -d $B/ks_*_o82_${k}_*)
ctl=$(/usr/bin/grep "o82_${k}_" $S/spark/done.md | /usr/bin/grep -i "CONTROL-PASS" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
run=$(/usr/bin/grep "o82_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep "PASS (7/7)" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
echo "ctl=$ctl run=$run"
nice -n 10 python3 $S/night/hold_ready.py $run $ctl ${key}-O82-$K $t --brief $br/${key}.md --model-tag spark-dsv4flash >$R/hold_$k.out 2>$R/hold_$k.err; echo "$k hold rc=$?"; cat $R/hold_$k.out $R/hold_$k.err | cut -c1-500
