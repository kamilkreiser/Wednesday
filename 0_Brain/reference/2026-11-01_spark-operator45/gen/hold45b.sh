#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator45; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
for kt in "p1 NFT-CERTIFICATE-LOAD-FROM-DB" "p2 NFT-CERTIFICATE-DB-SAVE-CERTIFICATE" "p3 NFT-CERTIFICATE-GET-NFT-CERTIFICATE" "p4 NFT-CERTIFICATE-GET-USER-NFT-CERTIFICATES"; do
 set -- $kt; k=$1; t=$2
 run=$(tail -1 $O/rnd4_$k.out | sed 's/.*· //'); ctl=$(tail -1 $O/ctl4_$k.out | sed 's/.*· //'); br=$(ls -d $B/ks_1868_o45_${k}_*); K=$(echo $k | tr p P)
 nice -n 10 python3 $S/night/hold_ready.py $run $ctl KS-1868-O45-$K $t --brief $br/KS-1868.md --model-tag spark-dsv4flash >$O/hold4_$k.out 2>$O/hold4_$k.err; echo "$k hold rc=$?"; cat $O/hold4_$k.out $O/hold4_$k.err | cut -c1-600
done
