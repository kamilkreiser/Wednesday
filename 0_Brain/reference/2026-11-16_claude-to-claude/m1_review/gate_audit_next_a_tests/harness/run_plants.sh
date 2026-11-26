#!/bin/bash
# Build each plant tree into its own empty target dir and run the builder's named test(s).
Q=/private/tmp/claude-501/qana; L=$Q/logs/plants; mkdir -p $L
run() { # plant test [filter]
  local p=$1 t=$2 f=$3 n=${1#p}
  date "+%T $p $t $f"
  [ -e $Q/tp$n/debug/coagent ] || { bash $Q/r.sh $Q/$p $Q/tp$n cargo build --workspace --bins --locked > $L/${p}_bins.log 2>&1; echo "bins rc=$? compiling-daemon=$(grep -c 'Compiling coagent-daemon' $L/${p}_bins.log)"; }
  bash $Q/r.sh $Q/$p $Q/tp$n cargo test -p coagent-daemon --locked --test $t -- $f --nocapture > $L/${p}_${t}.log 2>&1
  echo "rc=$? compiling-daemon=$(grep -c 'Compiling coagent-daemon' $L/${p}_${t}.log)"
  grep -m1 -E "panicked at|error\[|^error" $L/${p}_${t}.log; grep -m1 -A2 "panicked at" $L/${p}_${t}.log | sed -n '2p' | cut -c1-400
  grep -E '^test result' $L/${p}_${t}.log
}
for spec in "$@"; do run $spec; done
date +%T
