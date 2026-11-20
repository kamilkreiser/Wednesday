#!/bin/bash
# red.sh <var> <name> <target> <test> -- one red control, my own run (dev target)
W=/private/tmp/claude-501/qrr; V=$1; N=$2; T=$3; TS=$4
cd $W/clone || exit 9
export COAGENT_TOOLS=$W/t CARGO_TARGET_DIR=$W/t/target-dev; . scripts/env.sh
L=$W/mut/red_${N}__${T}.log
{ env "$V=$N" cargo build --workspace --bins --locked 2>&1; env "$V=$N" cargo test --locked -p coagent-daemon --test "$T" -- --exact "$TS" --nocapture 2>&1; } > $L
if grep -qF "test $TS ... FAILED" $L || grep -q "test result: FAILED" $L; then r=RED; elif grep -q "test result: ok" $L; then r=GREEN; else r=ERROR; fi
echo "RED-CHECK $V=$N $T::$TS -> $r :: $(grep -m1 -A1 'panicked at' $L | tail -1 | cut -c1-260)"
