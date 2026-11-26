#!/bin/bash
W=/private/tmp/claude-501/qan2
unset COAGENT_RED_AW
S=$(date +%s)
bash $W/r.sh $W/c $W/t cargo build --workspace --bins --locked > $W/build_t.log 2>&1
echo "exit $? secs $(( $(date +%s) - S ))" >> $W/build_t.log
S=$(date +%s)
bash $W/r.sh $W/c $W/t cargo test --locked -p coagent-daemon --test aw_disk -- --exact every_disk_failure_gets_a_row_and_nothing_is_recorded_twice --nocapture > $W/aw_disk_normal.log 2>&1
echo "exit $? secs $(( $(date +%s) - S ))" >> $W/aw_disk_normal.log
S=$(date +%s)
bash $W/r.sh $W/c $W/t cargo clippy -p coagent-daemon -p coagent-mcp --all-targets --locked -- -D warnings > $W/clippy.log 2>&1
echo "exit $? secs $(( $(date +%s) - S ))" >> $W/clippy.log
