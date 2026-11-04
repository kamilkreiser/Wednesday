#!/bin/bash
# Gate 188 runner. usage: runjest.sh <outname> <jest args...>
# Process cwd is <workdir>/cwd (commission gate_common s2), env -i, HOME/TMPDIR in the workdir.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000
O=$W/repo/Blockchain/Dev/services/originate
out=$1; shift
mkdir -p "$W/cwd" "$W/runs" "$W/tmp"
cd "$W/cwd" || exit 9
env -i GATE_OUT="$GATE_OUT" PATH="$PATH" HOME=$W/home TMPDIR=$W/tmp NODE_ENV=test \
  "$O/node_modules/.bin/jest" --rootDir "$O" --config "$W/jest.gate.config.js" --cacheDirectory "$W/tmp/jc" "$@" > "$W/runs/$out.txt" 2>&1
rc=$?
echo "rc=$rc"; grep -E "^(Tests|Test Suites):" "$W/runs/$out.txt"
