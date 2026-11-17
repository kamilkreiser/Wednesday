#!/bin/bash
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r6/env.sh
export RED_CONTROLS_LOG=$G/logs/red_normal_build.log
echo "HEAD $(git -C $C rev-parse HEAD)" > $G/logs/red_ci.log
bash $C/crates/coagent-policy/red-controls.sh >> $G/logs/red_ci.log 2>&1
echo "EXIT $?" >> $G/logs/red_ci.log
