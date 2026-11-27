#!/bin/bash
# QA-POLICY-B: build (no run) one test target in a tree with its own target dir. usage: build.sh <tree> <release|debug> <test target|lib>
W=/private/tmp/claude-501/qpb; T=$1; PROF=$2; TG=$3
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_$T/$PROF COAGENT_TEST_TMP=$W/tt_$T/testtmp RED_CONTROLS_LOG=$W/tt_$T/red-normal.log
mkdir -p $COAGENT_TEST_TMP
R=""; [ "$PROF" = release ] && R="--release"
SEL="--test $TG"; [ "$TG" = lib ] && SEL="--lib"
echo "build tree $T head $(git -C $W/$T rev-parse HEAD) heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) start $(date '+%T') CARGO_TARGET_DIR=$CARGO_TARGET_DIR"
python3 -B $W/h/inroot.py $W/$T cargo test -p coagent-policy --locked --offline $R $SEL --no-run 2>&1 | grep -E "Compiling coagent-policy|Executable|error|warning: unused" | head -20
echo "rc ${PIPESTATUS[0]} end $(date '+%T')"
