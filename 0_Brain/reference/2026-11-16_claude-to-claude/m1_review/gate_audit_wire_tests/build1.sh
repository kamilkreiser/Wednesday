#!/bin/bash
Q=/private/tmp/claude-501/qaw
date; bash $Q/r.sh $Q/c $Q/t cargo fetch --locked > $Q/fetch_head.log 2>&1; echo fetch head rc=$?
bash $Q/r.sh $Q/b $Q/tb cargo fetch --locked > $Q/fetch_base.log 2>&1; echo fetch base rc=$?
date; bash $Q/r.sh $Q/c $Q/t cargo build --workspace --bins --locked > $Q/build_head.log 2>&1; echo build head rc=$?
date; bash $Q/r.sh $Q/b $Q/tb cargo build --workspace --bins --locked > $Q/build_base.log 2>&1; echo build base rc=$?
date
