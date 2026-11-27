#!/bin/bash
W=/private/tmp/claude-501/qpb
bash $W/h/run_diff.sh base 0xc4ecb0b0000a $W/out/smoke_base.jsonl 1 QPB_N2=100 QPB_N3=200 QPB_ROWS=$W/rows/rows_items.jsonl
bash $W/h/run_diff.sh head 0xc4ecb0b0000a $W/out/smoke_head.jsonl 0 QPB_N2=100 QPB_N3=200 QPB_ROWS=$W/rows/rows_items.jsonl
python3 -B -I $W/h/cmp_qpb.py $W/out/smoke_base.jsonl $W/out/smoke_head.jsonl smoke > $W/out/cmp_smoke.txt; echo "cmp rc $?"
