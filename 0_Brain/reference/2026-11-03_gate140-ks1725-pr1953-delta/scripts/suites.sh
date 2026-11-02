#!/bin/bash
# Whole suites + tsc at the head for the units the delta touched (shared, nft-certificate, vc-issuer, auth) and the
# units develop's merges touched (anchoring, originate, governance, api-gateway, staking), plus anchoring on develop alone. npm --prefix anchored.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta; O=$G/logs/suites; mkdir -p $O
run() { local T=$1 u=$2 lbl=$3; local D=$T/Blockchain/Dev; local n=$(echo $u | tr / _)_$lbl
  "$D/node_modules/.bin/tsc" --noEmit -p "$D/$u/tsconfig.json" > $O/tsc_$n.log 2>&1; echo "$lbl $u tsc rc=$? errors=$(grep -c 'error TS' $O/tsc_$n.log)" >> $O/summary.txt
  local t=$(node -p "require('$D/$u/package.json').scripts.test||''")
  if [[ "$t" == *jest* ]]; then npm --prefix "$D/$u" run test > $O/test_$n.log 2>&1; rc=$?; tl=$(grep -E '^Tests:' $O/test_$n.log | tail -1)
  else if [[ "$t" == *"vitest run"* ]]; then npm --prefix "$D/$u" run test > $O/test_$n.log 2>&1; rc=$?; else npm --prefix "$D/$u" run test -- --run > $O/test_$n.log 2>&1; rc=$?; fi
    tl=$(grep -E '^\s+Tests ' $O/test_$n.log | tail -1); fi
  echo "$lbl $u test rc=$rc $tl" >> $O/summary.txt; }
run $G/repo_base services/anchoring develop
for u in services/anchoring packages/shared services/nft-certificate services/vc-issuer services/auth services/originate services/governance services/staking services/api-gateway; do run $G/repo $u head; done
echo ALLDONE >> $O/summary.txt
