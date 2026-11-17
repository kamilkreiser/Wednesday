#!/bin/bash
# usage: run_mine.sh <tree> <log> [cargo test args after --test r6_gate]
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r6/env.sh
export CARGO_TARGET_DIR=$G/target2
TREE=$1; LOG=$2; shift 2
cargo test --manifest-path $TREE/Cargo.toml -p coagent-policy --offline --test r6_gate "$@" -- --nocapture --test-threads 2 > $LOG 2>&1
echo "EXIT $?" >> $LOG
