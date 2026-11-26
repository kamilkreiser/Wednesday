#!/bin/bash
W=/private/tmp/claude-501/qan2
S=$(date +%s)
COAGENT_RED_AW=seal_error_ends_the_engine bash $W/r.sh $W/o $W/to cargo build --workspace --bins --locked > $W/build_to.log 2>&1
echo "exit $? secs $(( $(date +%s) - S ))" >> $W/build_to.log
bash $W/loop20.sh $W/o $W/to $W/L/old 20 1
