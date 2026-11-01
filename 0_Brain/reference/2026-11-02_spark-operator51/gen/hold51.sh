#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator51; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
for kt in "p1 NFT-CERTIFICATE-GET-CERTIFICATION-DATA" "p2 NFT-CERTIFICATE-GET-WALLET-NFT-CERTIFICATES"; do set -- $kt; k=$1; t=$2
 run=$(tail -1 $O/rnd1_$k.out | sed 's/.*· //'); ctl=$(tail -1 $O/ctl1_$k.out | sed 's/.*· //'); br=$(ls -d $B/ks_1868_o51_${k}_*); K=$(echo $k | tr p P)
 nice -n 10 python3 $S/night/hold_ready.py $run $ctl KS-1868-O51-$K $t --brief $br/KS-1868.md --model-tag spark-dsv4flash >$O/hold_$k.out 2>$O/hold_$k.err; echo "$k hold rc=$?"; cat $O/hold_$k.out $O/hold_$k.err | cut -c1-500; done
ls $S/night | /usr/bin/grep O51 | tee $O/held_files.txt
