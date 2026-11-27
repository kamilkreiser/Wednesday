#!/bin/bash
# QA-POLICY-B chain 1 (one heavy job of the check at a time): release builds of base and head, then a smoke run.
W=/private/tmp/claude-501/qpb
until [ "$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh 2>/dev/null | tr -dc 0-9)" != "" ] && [ "$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh | tr -dc 0-9)" -lt 3 ]; do echo "heavy FULL $(date +%T)"; sleep 120; done
bash $W/h/build.sh base release zz_qpb
bash $W/h/build.sh head release zz_qpb
mkdir -p $W/out
bash $W/h/run_diff.sh base 0xc4ecb0b0000a $W/out/smoke_base.jsonl 1 QPB_N2=100 QPB_N3=200 QPB_ROWS=$W/rows/rows_items.jsonl
bash $W/h/run_diff.sh head 0xc4ecb0b0000a $W/out/smoke_head.jsonl 0 QPB_N2=100 QPB_N3=200 QPB_ROWS=$W/rows/rows_items.jsonl
python3 -B -I $W/h/cmp_qpb.py $W/out/smoke_base.jsonl $W/out/smoke_head.jsonl smoke > $W/out/cmp_smoke.txt; echo "cmp rc $?"
