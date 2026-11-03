#!/bin/bash
# usage: vt.sh <label> [vitest args...]   runs vitest in the clone's auth service under the gate172 outbound guard
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate172-ks1968-pr1988; A=$W/repo/Blockchain/Dev/services/auth
L=$1; shift
mkdir -p $W/logs
: > $W/runs/guard_$L.log; : > $W/runs/guardpids_$L.log
env -i PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp \
  GATE_GUARD_LOG=$W/runs/guard_$L.log GATE_GUARD_LOADED=$W/runs/guardpids_$L.log \
  NODE_OPTIONS="--import=$W/scripts/hibp_guard.mjs" ${GATE_EXTRA_ENV} \
  bash -c "cd $A && $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A $*" > $W/logs/$L.log 2>&1
rc=$?
echo "$L rc=$rc guard_blocked=$(wc -l < $W/runs/guard_$L.log | tr -d ' ') guard_loaded_pids=$(sort -u $W/runs/guardpids_$L.log | wc -l | tr -d ' ')"
sed 's/\x1b\[[0-9;]*m//g' $W/logs/$L.log | grep -E '^ +(Tests|Test Files) '
