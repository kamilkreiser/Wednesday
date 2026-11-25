#!/bin/bash
# QA-POLICY-AT: the base's whole suite, own target, test tmp under the work dir (/private/tmp), clean tree, no harness.
W=/private/tmp/claude-501/qpa; . $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_base/target COAGENT_TEST_TMP=$W/tt_base/suite_testtmp; mkdir -p $COAGENT_TEST_TMP
echo "start $(date '+%F %T') head $(git -C $W/base rev-parse HEAD) status_lines $(git -C $W/base status --porcelain | wc -l) heavy $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) CARGO_TARGET_DIR=$CARGO_TARGET_DIR COAGENT_TEST_TMP=$COAGENT_TEST_TMP" > $W/base_suite.log
python3 -B $W/h/inroot.py $W/base cargo test -p coagent-policy --locked --offline >> $W/base_suite.log 2>&1
echo "exit $? end $(date '+%F %T') status_lines $(git -C $W/base status --porcelain | wc -l)" >> $W/base_suite.log
