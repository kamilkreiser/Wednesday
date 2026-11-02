#!/bin/bash
# usage: run.sh <anchoring|originate> <logprefix> [extra args...]   JSON report to <logprefix>.json, console to <logprefix>.log
set -u
SVC="$1"; P="$2"; shift 2
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932
D=$G/repo/Blockchain/Dev
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a974be12-1abe-4d9a-9532-9c46296d28fc/scratchpad
echo "node $(node -v) load $(sysctl -n vm.loadavg) $(date -u +%T)" > "$P.log"
if [ "$SVC" = anchoring ]; then
  nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/anchoring --maxWorkers=3 --reporter=default --reporter=json --outputFile.json="$P.json" "$@" >> "$P.log" 2>&1; RC=$?
else
  ( cd_dir=$D/services/originate; nice -n 10 $D/node_modules/.bin/jest --rootDir $cd_dir --config $cd_dir/jest.config.js --maxWorkers=3 --forceExit --json --outputFile="$P.json" "$@" >> "$P.log" 2>&1 ); RC=$?
fi
echo "rc=$RC $(date -u +%T)" >> "$P.log"; exit $RC
