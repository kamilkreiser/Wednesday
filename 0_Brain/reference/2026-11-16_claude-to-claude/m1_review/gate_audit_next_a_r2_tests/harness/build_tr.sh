#!/bin/bash
W=/private/tmp/claude-501/qan2
S=$(date +%s)
COAGENT_RED_AW=seal_error_ends_the_engine bash $W/r.sh $W/c $W/tr cargo build --workspace --bins --locked > $W/build_tr.log 2>&1
echo "exit $? secs $(( $(date +%s) - S ))" >> $W/build_tr.log
