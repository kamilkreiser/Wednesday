#!/bin/bash
# QA-POLICY-B: everything after the main seeds, one heavy job of the check at a time.
W=/private/tmp/claude-501/qpb; S=0x9b17c4ec0001
waitc() { until [ "$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh | tr -dc 0-9)" -lt 3 ] 2>/dev/null; do echo "heavy FULL $(date +%T)"; sleep 120; done; }
echo "== A. corrected late rows $(date +%T)"
bash $W/h/run_diff.sh base $S $W/out/items2_base.jsonl 1 QPB_N2=0 QPB_N3=0 QPB_ROWS=$W/rows/rows_items2.jsonl
bash $W/h/run_diff.sh head $S $W/out/items2_head.jsonl 0 QPB_N2=0 QPB_N3=0 QPB_ROWS=$W/rows/rows_items2.jsonl
echo "== B. plants: base at a fifth $(date +%T)"; waitc
bash $W/h/run_diff.sh base $S $W/out/fifth_base.jsonl 1 QPB_FRAC=5
bash $W/h/run_diff.sh head $S $W/out/fifth_head.jsonl 0 QPB_FRAC=5
python3 -B -I $W/h/cmp_qpb.py $W/out/fifth_base.jsonl $W/out/fifth_head.jsonl fifth-head > $W/out/cmp_fifth_head.txt; echo "cmp fifth head rc $?"
for P in P1 P2 P3 P4 P5 P6 L1 L2 L3; do
  waitc; bash $W/h/build.sh pl_$P release zz_qpb
  bash $W/h/run_diff.sh pl_$P $S $W/out/fifth_$P.jsonl 0 QPB_FRAC=5
  python3 -B -I $W/h/cmp_qpb.py $W/out/fifth_base.jsonl $W/out/fifth_$P.jsonl plant-$P > $W/out/cmp_plant_$P.txt; echo "cmp plant $P rc $?"
done
echo "== C. guard-lowered control G1 $(date +%T)"; waitc
bash $W/h/build.sh mu_G1 release zz_qpb
for T in head mu_G1; do
  . $W/h/envx.sh; export CARGO_TARGET_DIR=$W/tt_$T/release QPB_MODE=scanb QPB_ROWS=$W/rows/rows_items.jsonl QPB_OUT=$W/out/scanb_items_$T.jsonl QPB_FIX=$W/fix/scanb_$T
  python3 -B $W/h/inroot.py $W/$T cargo test -p coagent-policy --locked --offline --release --test zz_qpb -- --nocapture 2>&1 | grep -E "QPB|test result"
done
echo "== D. sliding real corpus at the head $(date +%T)"
. $W/h/envx.sh; export CARGO_TARGET_DIR=$W/tt_head/release QPB_MODE=scanb QPB_ROWS=$W/rows/rows_sliding.jsonl QPB_OUT=$W/out/scanb_sliding_head.jsonl QPB_FIX=$W/fix/scanb_sl
python3 -B $W/h/inroot.py $W/head cargo test -p coagent-policy --locked --offline --release --test zz_qpb -- --nocapture 2>&1 | grep -E "QPB|test result"
unset QPB_MODE QPB_ROWS QPB_OUT QPB_FIX
echo "== E. debug builds for timing $(date +%T)"; waitc
for T in base head mu_T70; do bash $W/h/build.sh $T debug zz_qpb; done
echo "== F. mutants $(date +%T)"
for M in mu_M1 mu_M2 mu_M3 mu_M4 mu_M5 mu_M6 mu_M7 mu_M8 mu_M9 mu_M10 pl_L3 mu_M12 mu_M13 mu_M14; do waitc; python3 -B $W/h/mut_run.py $M $W/out/mut_$M.txt; done
echo "== END $(date +%T)"
