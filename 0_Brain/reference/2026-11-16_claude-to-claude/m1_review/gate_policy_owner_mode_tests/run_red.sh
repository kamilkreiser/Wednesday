#!/bin/bash
# QA-POLICY-OWNER-MODE: run the policy red controls once from the clone root, own target dir and test tmp.
W=/private/tmp/claude-501/qpom
. $W/env.sh
export CARGO_TARGET_DIR=$W/t_red COAGENT_TEST_TMP=$W/ttmp_red
mkdir -p $W/ttmp_red
echo "start $(date '+%F %T') heavy=$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh)"
python3 -B -c 'import os,sys; os.chdir(sys.argv[1]); os.execvp("bash", ["bash", "crates/coagent-policy/red-controls.sh"])' $W/clone
echo "red-controls exit $? end $(date '+%F %T')"
