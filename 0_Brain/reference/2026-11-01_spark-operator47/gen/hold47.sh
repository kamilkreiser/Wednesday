#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator47; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
for kt in "p1 4 3 KYC-SAVE-VERIFICATION" "p2 4 3 KYC-GET-VERIFICATION" "p3 4 3 KYC-GET-VERIFICATIONS-BY-USER" "p4 6 5 KYC-GET-VERIFICATION-STATS" "p5 4 3 KYC-SAVE-CONSENT"; do
 set -- $kt; k=$1; r=$2; c=$3; t=$4
 run=$(tail -1 $O/rnd${r}_$k.out | sed 's/.*· //'); ctl=$(tail -1 $O/ctl${c}_$k.out | sed 's/.*· //'); br=$(ls -d $B/ks_1868_o47_${k}_*); K=$(echo $k | tr p P)
 nice -n 10 python3 $S/night/hold_ready.py $run $ctl KS-1868-O47-$K $t --brief $br/KS-1868.md --model-tag spark-dsv4flash >$O/hold_$k.out 2>$O/hold_$k.err; echo "$k hold rc=$?"; cat $O/hold_$k.out $O/hold_$k.err | cut -c1-700
done
