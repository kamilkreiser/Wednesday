#!/bin/bash
# check.sh on both volume kinds, then the seat's red-control runner (boot volume fixtures).
. "$(dirname "$0")/env_r5.sh"
R=$S/repo
mkdir -p $O/logs
echo "HEAD $(git -C $R rev-parse HEAD)" > $O/logs/check_ci.log
COAGENT_TEST_TMP=$S/fixtures_ci bash $R/scripts/check.sh >> $O/logs/check_ci.log 2>&1
echo "EXIT $?" >> $O/logs/check_ci.log
echo "HEAD $(git -C $R rev-parse HEAD)" > $O/logs/check_cs.log
COAGENT_TEST_TMP=$O/fixtures_cs bash $R/scripts/check.sh >> $O/logs/check_cs.log 2>&1
echo "EXIT $?" >> $O/logs/check_cs.log
echo "HEAD $(git -C $R rev-parse HEAD)" > $O/logs/red_ci.log
COAGENT_TEST_TMP=$S/fixtures_ci bash $R/crates/coagent-policy/red-controls.sh >> $O/logs/red_ci.log 2>&1
echo "EXIT $?" >> $O/logs/red_ci.log
