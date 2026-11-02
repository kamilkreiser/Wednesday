#!/bin/bash
# hold76.sh <tag e.g. o76_p1> <KS-n> <label> : run dirs from spark/done.md rows (control-PASS row dir; model PASS row dir)
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator76; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
k=$1; ks=$2; t=$3; K=$(echo $k | tr 'op' 'OP' | sed 's/o76_p/O76-P/')
br=$(ls -d $B/ks_*_${k}_*)
ctl=$(/usr/bin/grep "_${k}_" $S/spark/done.md | /usr/bin/grep -i "CONTROL-PASS" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
run=$(/usr/bin/grep "_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep "PASS (PASS" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
echo "ctl=$ctl run=$run"
nice -n 10 python3 $S/night/hold_ready.py $run $ctl ${ks}-$K $t --brief $br/${ks}.md --model-tag spark-dsv4flash >$R/hold_$k.out 2>$R/hold_$k.err; echo "$k hold rc=$?"; cat $R/hold_$k.out $R/hold_$k.err | cut -c1-500
