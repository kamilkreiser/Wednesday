#!/bin/bash
# QA-POLICY-NEXT: run ONE cargo test target in a named tree with its own target dir and test tmp. usage: run1.sh <tree> <log> <cargo test args...>
W=/private/tmp/claude-501/qpx
T=$1; LOG=$2; shift 2
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_$T/target COAGENT_TEST_TMP=$W/tt_$T/testtmp RED_CONTROLS_LOG=$W/tt_$T/red-normal.log
mkdir -p $COAGENT_TEST_TMP
echo "tree $T head $(git -C $W/$T rev-parse HEAD) start $(date '+%T') CARGO_TARGET_DIR=$CARGO_TARGET_DIR COAGENT_TEST_TMP=$COAGENT_TEST_TMP args: $*" > $LOG
python3 -B $W/h/inroot.py $W/$T cargo test -p coagent-policy --locked --offline "$@" >> $LOG 2>&1
echo "rc $? end $(date '+%T')" >> $LOG
