#!/bin/bash
Q=/private/tmp/claude-501/qana
date "+%F %T fetch"; bash $Q/r.sh $Q/c $Q/t cargo fetch --locked > $Q/fetch_head.log 2>&1; echo fetch head rc=$?
bash $Q/r.sh $Q/b $Q/tb cargo fetch --locked > $Q/fetch_base.log 2>&1; echo fetch base rc=$?
date "+%F %T build head"; bash $Q/r.sh $Q/c $Q/t cargo build --workspace --bins --locked > $Q/build_head.log 2>&1; echo build head rc=$?
date "+%F %T build head tests"; bash $Q/r.sh $Q/c $Q/t cargo test -p coagent-daemon -p coagent-mcp -p coagent-audit-host --locked --no-run > $Q/build_head_tests.log 2>&1; echo build head tests rc=$?
date "+%F %T build base"; bash $Q/r.sh $Q/b $Q/tb cargo build --workspace --bins --locked > $Q/build_base.log 2>&1; echo build base rc=$?
date "+%F %T build base tests"; bash $Q/r.sh $Q/b $Q/tb cargo test -p coagent-daemon -p coagent-mcp -p coagent-audit-host --locked --no-run > $Q/build_base_tests.log 2>&1; echo build base tests rc=$?
date "+%F %T done"
