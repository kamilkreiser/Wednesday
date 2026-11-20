#!/bin/bash
# run_mut.sh <name> <file> <old> <new> <test target> [test filter...]
W=/private/tmp/claude-501/qrr; N=$1; F=$2; O=$3; NW=$4; T=$5; shift 5
cd $W/clone || exit 9
export COAGENT_TOOLS=$W/t CARGO_TARGET_DIR=$W/t/target-dev; . scripts/env.sh
python3 $W/mut/mutate.py "$F" "$O" "$NW" || exit 8
git diff --stat
cargo build --locked --workspace --bins -q 2>&1 | grep -E "^error" -A5
cargo test --locked -p coagent-daemon --test "$T" -- --test-threads=4 "$@" > $W/mut/$N.log 2>&1; rc=$?
git checkout -- "$F"
git status --short | grep -v '^??' 
echo "MUTANT $N target $T exit $rc"; grep -E "^test .*(FAILED|ok)$|test result" $W/mut/$N.log | tail -15; grep -E "panicked" -A2 $W/mut/$N.log | head -12 | cut -c1-300
