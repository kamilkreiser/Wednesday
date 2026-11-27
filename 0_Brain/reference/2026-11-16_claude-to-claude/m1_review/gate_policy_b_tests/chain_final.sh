#!/bin/bash
# QA-POLICY-B: after the mutants: margins (head debug, nocapture), by-hand reds, t29 at the base, timing, base test list.
W=/private/tmp/claude-501/qpb
waitc() { until [ "$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh | tr -dc 0-9)" -lt 3 ] 2>/dev/null; do echo "heavy FULL $(date +%T)"; sleep 120; done; }
. $W/h/envx.sh
run1() { # tree target-dir args...
  local T=$1 TD=$2; shift 2
  CARGO_TARGET_DIR=$TD COAGENT_TEST_TMP=$W/tt_$T/testtmp RED_CONTROLS_LOG=$W/tt_$T/red-normal.log python3 -B $W/h/inroot.py $W/$T cargo test -p coagent-policy --locked --offline "$@" 2>&1
}
echo "== G. margins at the head (debug) $(date +%T) heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh)"
for t in t29_free_text t28_at_names t14_gate_return; do run1 head $W/tt_head/debug --test $t -- --nocapture > $W/out/margin_$t.txt; grep -E "test result|T29-COST|T29-CORPUS.*WebFetch \"prose, no|T28-BOUND|m6|REACH|T29-MILLION|panicked" $W/out/margin_$t.txt | head -40; done
echo "== H. by-hand reds $(date +%T)"; waitc
run1 hw3 $W/tt_hw3/debug --test t25_owner_allow > $W/out/hw3.txt; grep -E "test result|panicked" -A1 $W/out/hw3.txt | head -6
run1 hw4 $W/tt_hw4/debug --test t27_owner_dark > $W/out/hw4.txt; grep -E "test result|panicked" -A1 $W/out/hw4.txt | head -6
run1 hw5 $W/tt_hw5/debug --test t25_owner_allow > $W/out/hw5.txt; grep -E "test result|panicked" -A1 $W/out/hw5.txt | head -6
run1 t29base $W/tt_t29base/debug --test t29_free_text > $W/out/t29base.txt; grep -E "test result|panicked" -A1 $W/out/t29base.txt | head -16
echo "== I. timing $(date +%T)"; waitc
EB=$(ls $W/tt_base/debug/debug/build/coagent-policy/*/out/zz_qpb-* 2>/dev/null | head -1); [ -z "$EB" ] && EB=$(ls $W/tt_base/debug/debug/deps/zz_qpb-* | grep -v '\.d$' | head -1)
EH=$(ls $W/tt_head/debug/debug/build/coagent-policy/*/out/zz_qpb-* 2>/dev/null | head -1); [ -z "$EH" ] && EH=$(ls $W/tt_head/debug/debug/deps/zz_qpb-* | grep -v '\.d$' | head -1)
ET=$(ls $W/tt_mu_T70/debug/debug/build/coagent-policy/*/out/zz_qpb-* 2>/dev/null | head -1); [ -z "$ET" ] && ET=$(ls $W/tt_mu_T70/debug/debug/deps/zz_qpb-* | grep -v '\.d$' | head -1)
echo "exes $EB $EH $ET"
python3 -B $W/h/time_drive.py $EB $EH $W/rows/rows_time.jsonl $W/out/time_debug.tsv def,env,long debug-bh
python3 -B $W/h/time_drive.py $EB $EB $W/rows/rows_time.jsonl $W/out/time_debug_aa.tsv def debug-aa
python3 -B $W/h/time_drive.py $EB $ET $W/rows/rows_time.jsonl $W/out/time_debug_t70.tsv def debug-t70 0:120
python3 -B $W/h/time_drive.py $EB $EH $W/rows/rows_time_million.jsonl $W/out/time_debug_million.tsv def debug-million
waitc
RB=$(ls $W/tt_base/release/release/build/coagent-policy/*/out/zz_qpb-* | head -1); RH=$(ls $W/tt_head/release/release/build/coagent-policy/*/out/zz_qpb-* | head -1)
bash $W/h/build.sh base release zz_qpb; bash $W/h/build.sh head release zz_qpb
RB=$(ls -t $W/tt_base/release/release/build/coagent-policy/*/out/zz_qpb-* | head -1); RH=$(ls -t $W/tt_head/release/release/build/coagent-policy/*/out/zz_qpb-* | head -1)
python3 -B $W/h/time_drive.py $RB $RH $W/rows/rows_time.jsonl $W/out/time_release.tsv def,env,long release-bh
python3 -B $W/h/time_drive.py $RB $RB $W/rows/rows_time.jsonl $W/out/time_release_aa.tsv def release-aa
python3 -B $W/h/time_drive.py $RB $RH $W/rows/rows_time_million.jsonl $W/out/time_release_million.tsv def release-million
echo "== J. base test list $(date +%T)"; waitc
CARGO_TARGET_DIR=$W/tt_list_base python3 -B $W/h/inroot.py $W/listbase cargo test -p coagent-policy --locked --offline --no-run > /dev/null 2>&1
bash $W/h/list_tests.sh listbase $W/tt_list_base $W/logs/list_base.txt
echo "== END $(date +%T)"
