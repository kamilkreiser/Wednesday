#!/bin/bash
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r6/env.sh
echo "HEAD $(git -C $C rev-parse HEAD) TMP=$COAGENT_TEST_TMP" > $G/logs/check_ci.log
bash $C/scripts/check.sh >> $G/logs/check_ci.log 2>&1
echo "EXIT $?" >> $G/logs/check_ci.log
