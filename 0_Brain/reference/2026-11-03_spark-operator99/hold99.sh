#!/bin/bash
# hold99.sh <pN-dirkey> <KEY-ROWID> <LABEL>: hold via hold_ready.py (now with the strict-apply leg)
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator99; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
k=$1; rowid=$2; t=$3
br=$(ls -d $B/ks_*_o99_${k}_*)
ctl=$(/usr/bin/grep "o99_${k}_" $S/spark/done.md | /usr/bin/grep -i "CONTROL-PASS" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
run=$(/usr/bin/grep "o99_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep "PASS (7/7)" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
echo "ctl=$ctl run=$run"
echo "nice -n 10 python3 $S/night/hold_ready.py $run $ctl $rowid $t --brief $br/KS-1868.md --model-tag spark-dsv4flash" > $R/hold_cmd_$k.txt
nice -n 10 python3 $S/night/hold_ready.py $run $ctl $rowid $t --brief $br/KS-1868.md --model-tag spark-dsv4flash >$R/hold_$k.out 2>$R/hold_$k.err; echo "$k hold rc=$?"; cat $R/hold_$k.out $R/hold_$k.err | cut -c1-500
