#!/bin/bash
# QA-POLICY-WORDS: run cargo in <tree> with this check's own folders.
# usage: cg.sh <tree> <tag> <cargo args...>
#   CARGO_TARGET_DIR=$W/tt_<tag>/target  RED_CONTROLS_LOG=$W/tt_<tag>/red.log
#   COAGENT_TEST_TMP=${TT:-$W/tt_<tag>/testtmp}; TT=UNSET leaves it unset.
W=/private/tmp/claude-501/qpw; TREE=$1; TAG=$2; shift 2
. $W/h/envq.sh
export CARGO_TARGET_DIR=$W/tt_$TAG/target RED_CONTROLS_LOG=$W/tt_$TAG/red.log
if [ "${TT:-}" = "UNSET" ]; then unset COAGENT_TEST_TMP; else export COAGENT_TEST_TMP=${TT:-$W/tt_$TAG/testtmp}; mkdir -p "$COAGENT_TEST_TMP"; fi
mkdir -p $W/tt_$TAG
HEADSHA=$(git -C "$TREE" rev-parse HEAD 2>/dev/null || cat "$TREE/.qpw_sha" 2>/dev/null)
echo "RUN tree=$TREE sha=$HEADSHA heavy=$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) start=$(date '+%F %T')"
echo "ENV CARGO_TARGET_DIR=$CARGO_TARGET_DIR RED_CONTROLS_LOG=$RED_CONTROLS_LOG COAGENT_TEST_TMP=${COAGENT_TEST_TMP-<unset>}"
echo "CMD cargo $*"
python3 -B $W/h/indir.py "$TREE" cargo "$@" 2>&1
RC=$?
echo "RC $RC end=$(date '+%F %T')"
exit $RC
