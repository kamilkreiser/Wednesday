#!/bin/bash
S=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_daemon
. $S/env.sh
N=$(sysctl -n hw.ncpu)
pids=()
for i in $(seq 1 $N); do /usr/bin/yes > /dev/null & pids+=($!); done
echo "load pids: ${pids[*]}"
for i in 1 2 3 4 5; do
  log=$S/loadrun$i.log
  start=$(date +%s)
  cargo test --manifest-path $S/repo/Cargo.toml --locked -p coagent-daemon -p coagent-mcp > $log 2>&1; rc=$?
  echo "load run $i: exit $rc, $(/usr/bin/grep -Eci "^test .* ok$" $log) tests ok, $(/usr/bin/grep -ci 'FAILED' $log) FAILED lines, $(( $(date +%s)-start )) s"
  /usr/bin/grep -E "^test .* FAILED|panicked" $log
done
kill "${pids[@]}"
