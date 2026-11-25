#!/bin/bash
# QA-POLICY-AT: build (no run) the differential harness release in a tree with its own target dir. usage: build.sh <tree>
W=/private/tmp/claude-501/qpa; T=$1
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_$T${TT:-}/target COAGENT_TEST_TMP=$W/tt_$T/testtmp RED_CONTROLS_LOG=$W/tt_$T/red-normal.log
mkdir -p $COAGENT_TEST_TMP
echo "tree $T head $(git -C $W/$T rev-parse HEAD) heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) start $(date '+%T') target $CARGO_TARGET_DIR"
python3 -B $W/h/inroot.py $W/$T cargo test -p coagent-policy --locked --offline --release --test zz_qpa_diff --no-run 2>&1
echo "rc ${PIPESTATUS[0]} end $(date '+%T')"
