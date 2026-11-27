#!/bin/bash
# QA-POLICY-B: one differential run of one tree. usage: run_diff.sh <tree> <seed hex> <out> <twin 0|1> [VAR=value ...]
W=/private/tmp/claude-501/qpb; T=$1; SEED=$2; OUT=$3; TWIN=$4; shift 4
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_$T/release COAGENT_TEST_TMP=$W/tt_$T/testtmp RED_CONTROLS_LOG=$W/tt_$T/red-normal.log
export QPB_MODE=diff QPB_OUT=$OUT QPB_SEED=$SEED QPB_ROWS=$W/rows/rows_c1.jsonl,$W/rows/rows_items.jsonl QPB_FIX=$W/fix/root QPB_TWIN=$TWIN
for kv in "$@"; do export "$kv"; done
mkdir -p $COAGENT_TEST_TMP $W/fix
echo "diff tree $T head $(git -C $W/$T rev-parse HEAD) dirty-files $(git -C $W/$T status --porcelain | wc -l | tr -d ' ') heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) seed $SEED twin $TWIN start $(date '+%T') CARGO_TARGET_DIR=$CARGO_TARGET_DIR COAGENT_TEST_TMP=$COAGENT_TEST_TMP extra: $*"
python3 -B $W/h/inroot.py $W/$T cargo test -p coagent-policy --locked --offline --release --test zz_qpb -- --nocapture 2>&1 | grep -E 'QPB|test result|panicked|error\[|Compiling coagent'
echo "rc ${PIPESTATUS[0]} end $(date '+%T') out $(wc -c < $OUT) bytes sha256 $(shasum -a 256 $OUT | cut -c1-16)"
