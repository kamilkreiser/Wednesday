#!/bin/bash
# QA-POLICY-B: the red script ONCE, whole, from the clean clone tree at the head. Own target/log/fixtures.
W=/private/tmp/claude-501/qpb
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_red/target RED_CONTROLS_LOG=$W/tt_red/red-normal.log COAGENT_TEST_TMP=$W/tt_red/testtmp
echo "red tree head $(git -C $W/red rev-parse HEAD) status_lines $(git -C $W/red status --porcelain | wc -l) heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) start $(date '+%F %T') CARGO_TARGET_DIR=$CARGO_TARGET_DIR RED_CONTROLS_LOG=$RED_CONTROLS_LOG COAGENT_TEST_TMP=$COAGENT_TEST_TMP"
python3 -B $W/h/inroot.py $W/red bash crates/coagent-policy/red-controls.sh
echo "rc $? end $(date '+%F %T')"
