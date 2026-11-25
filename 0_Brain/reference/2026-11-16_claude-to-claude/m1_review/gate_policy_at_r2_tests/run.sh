#!/bin/bash
# QA-POLICY-AT-R2: run a cargo command in <tree> with this check's own dirs.
# usage: run.sh <tree dir> <tag> <cargo args...>
#   CARGO_TARGET_DIR=$W/tt_<tag>/target, RED_CONTROLS_LOG=$W/tt_<tag>/red.log,
#   COAGENT_TEST_TMP=${TT:-$W/tt_<tag>/testtmp}; TT=UNSET leaves COAGENT_TEST_TMP unset (task 2 (c) only).
W=/private/tmp/claude-501/qpa2; TREE=$1; TAG=$2; shift 2
. $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_$TAG/target RED_CONTROLS_LOG=$W/tt_$TAG/red.log
if [ "${TT:-}" = "UNSET" ]; then unset COAGENT_TEST_TMP; else export COAGENT_TEST_TMP=${TT:-$W/tt_$TAG/testtmp}; mkdir -p "$COAGENT_TEST_TMP"; fi
mkdir -p $W/tt_$TAG
echo "RUN tree=$TREE head=$(git -C $TREE rev-parse HEAD) status_lines=$(git -C $TREE status --porcelain | wc -l | tr -d ' ') heavy=$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) start=$(date '+%F %T')"
echo "ENV CARGO_TARGET_DIR=$CARGO_TARGET_DIR RED_CONTROLS_LOG=$RED_CONTROLS_LOG COAGENT_TEST_TMP=${COAGENT_TEST_TMP-<unset>}"
echo "CMD cargo $*"
python3 -B $W/h/inroot.py "$TREE" cargo "$@" 2>&1
RC=$?
echo "RC $RC end=$(date '+%F %T')"
exit $RC
