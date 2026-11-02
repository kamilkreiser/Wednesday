#!/bin/bash
# usage: run.sh <anchoring|originate> <logprefix> [extra args...]
set -u
SVC="$1"; P="$2"; shift 2
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955
D=$G/repo/Blockchain/Dev
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad
echo "node $(node -v) load $(sysctl -n vm.loadavg) $(date -u +%T)" > "$P.log"
if [ "$SVC" = anchoring ]; then
  nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/anchoring --maxWorkers=3 --reporter=default --reporter=json --outputFile.json="$P.json" "$@" >> "$P.log" 2>&1; RC=$?
else
  ( cd_dir=$D/services/originate; nice -n 10 $D/node_modules/.bin/jest --rootDir $cd_dir --config $cd_dir/jest.config.js --maxWorkers=3 --forceExit --json --outputFile="$P.json" "$@" >> "$P.log" 2>&1 ); RC=$?
fi
echo "rc=$RC $(date -u +%T)" >> "$P.log"; exit $RC
