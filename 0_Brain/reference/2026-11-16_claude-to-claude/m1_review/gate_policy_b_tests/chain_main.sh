#!/bin/bash
# QA-POLICY-B: the main differential, two seeds, base then head per seed (one heavy job at a time), then compare.
W=/private/tmp/claude-501/qpb
for SEED in 0x9b17c4ec0001 0x9b17c4ec0002; do
  until [ "$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh | tr -dc 0-9)" -lt 3 ] 2>/dev/null; do echo "heavy FULL $(date +%T)"; sleep 120; done
  bash $W/h/run_diff.sh base $SEED $W/out/main_${SEED}_base.jsonl 1 QPB_N2=2000 QPB_N3=3000
  bash $W/h/run_diff.sh head $SEED $W/out/main_${SEED}_head.jsonl 0 QPB_N2=2000 QPB_N3=3000
  python3 -B -I $W/h/cmp_qpb.py $W/out/main_${SEED}_base.jsonl $W/out/main_${SEED}_head.jsonl main-$SEED > $W/out/cmp_main_$SEED.txt; echo "cmp $SEED rc $?"
done
