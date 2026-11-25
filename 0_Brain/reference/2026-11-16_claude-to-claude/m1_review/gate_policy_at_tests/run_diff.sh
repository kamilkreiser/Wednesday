#!/bin/bash
# QA-POLICY-AT: run the differential harness in one tree. usage: run_diff.sh <tree> <seed hex> <out.jsonl> <twin 0|1> [extra env assignments...]
# Base and head of one seed run ONE AFTER THE OTHER on the same fixed fixture root ($W/fix), own test tmp per tree.
W=/private/tmp/claude-501/qpa; T=$1; SEED=$2; OUT=$3; TWIN=$4; shift 4
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_$T${TT:-}/target COAGENT_TEST_TMP=$W/tt_$T/testtmp RED_CONTROLS_LOG=$W/tt_$T/red-normal.log
export QPA_OUT=$OUT QPA_SEED=$SEED QPA_ROWS=$W/h/rows.jsonl QPA_FIX=$W/fix/root QPA_O2=$W/outside2 QPA_TWIN=$TWIN
for kv in "$@"; do export "$kv"; done
mkdir -p $COAGENT_TEST_TMP $W/fix
echo "tree $T head $(git -C $W/$T rev-parse HEAD) status $(git -C $W/$T status --porcelain | tr '\n' ' ') heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) seed $SEED twin $TWIN start $(date '+%T') CARGO_TARGET_DIR=$CARGO_TARGET_DIR COAGENT_TEST_TMP=$COAGENT_TEST_TMP extra: $*"
python3 -B $W/h/inroot.py $W/$T cargo test -p coagent-policy --locked --offline --release --test zz_qpa_diff -- --nocapture 2>&1 | grep -E 'QPA|test result|panicked|error|Compiling|Running'
echo "rc ${PIPESTATUS[0]} end $(date '+%T') out $(wc -c < $OUT) bytes sha256 $(shasum -a 256 $OUT | cut -c1-16)"
