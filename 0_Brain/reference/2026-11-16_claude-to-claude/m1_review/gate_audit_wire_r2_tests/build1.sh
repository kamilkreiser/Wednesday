#!/bin/bash
Q=/private/tmp/claude-501/qaw2
date; bash $Q/r.sh $Q/c $Q/t cargo fetch --locked > $Q/fetch_head.log 2>&1; echo fetch head rc=$?
bash $Q/r.sh $Q/o $Q/to cargo fetch --locked > $Q/fetch_old.log 2>&1; echo fetch old rc=$?
date; bash $Q/r.sh $Q/c $Q/t cargo build --workspace --bins --locked > $Q/build_head.log 2>&1; echo build head rc=$?
date; bash $Q/r.sh $Q/c $Q/t cargo test -p coagent-daemon --locked --no-run > $Q/build_head_tests.log 2>&1; echo build head tests rc=$?
date; bash $Q/r.sh $Q/o $Q/to cargo build --workspace --bins --locked > $Q/build_old.log 2>&1; echo build old rc=$?
date; bash $Q/r.sh $Q/o $Q/to cargo test -p coagent-daemon --locked --no-run > $Q/build_old_tests.log 2>&1; echo build old tests rc=$?
date
