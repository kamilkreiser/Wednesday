#!/bin/bash
W=/private/tmp/claude-501/qpb
for t in base head pl_P1 pl_P2 pl_P3 pl_P4 pl_P5 pl_P6 pl_L1 pl_L2 pl_L3 mu_G1 mu_T70; do cp $W/h/zz_qpb.rs $W/$t/crates/coagent-policy/tests/zz_qpb.rs; cmp -s $W/h/zz_qpb.rs $W/$t/crates/coagent-policy/tests/zz_qpb.rs || echo "SYNC FAIL $t"; done; echo "harness synced (URL-escape oracle rule) $(date +%T)"
python3 -B $W/h/mk_recheck.py $W/rows/rows_recheck.jsonl 0x9b17c4ec0001 0x9b17c4ec0002
bash $W/h/run_diff.sh base 0x9b17c4ec0001 $W/out/recheck_base.jsonl 1 QPB_N2=0 QPB_N3=0 QPB_ROWS=$W/rows/rows_recheck.jsonl
bash $W/h/run_diff.sh head 0x9b17c4ec0001 $W/out/recheck_head.jsonl 0 QPB_N2=0 QPB_N3=0 QPB_ROWS=$W/rows/rows_recheck.jsonl
python3 -B -I $W/h/cmp_qpb.py $W/out/recheck_base.jsonl $W/out/recheck_head.jsonl recheck > $W/out/cmp_recheck.txt; echo "cmp recheck rc $?"
bash $W/h/chain_after.sh
