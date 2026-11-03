#!/bin/bash
# chk88.sh <pN>: compare the model patch of the PASS (7/7) run with the brief's golden.diff; print the checker verdict lines
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
k=$1
br=$(ls -d $S/night/briefs/ks_*_o98_${k}_*)
run=$(/usr/bin/grep "o98_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep "PASS (7/7)" | awk -F'|' '{gsub(/ /,"",$9); print $9}' | tail -1)
echo "run=$run"
diff $run/out.md.checker/patch.diff $br/golden.diff > /dev/null; echo "patch-vs-golden diff rc=$? (0 = byte-identical)"
/usr/bin/grep -E '^(PASS A|FAIL A|SUMMARY|tests added|baseline suite|after suite)' $run/checker.out | cut -c1-170
