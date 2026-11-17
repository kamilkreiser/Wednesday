#!/bin/bash
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r6/env.sh
export CARGO_TARGET_DIR=$G/target2
python3 -I $O/mutate_r6.py $G/t $G/m $G/mutation "$@"
diff -r $G/t $G/m > $G/mutation/restore_check.txt 2>&1; echo "restore_diff_rc=$?" >> $G/mutation/restore_check.txt
