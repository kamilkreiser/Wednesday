#!/bin/bash
# Whole suites + tsc at head, one unit at a time (anchored with npm --prefix to this clone).
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953; D=$G/repo/Blockchain/Dev; O=$G/logs/suites_head; mkdir -p $O
for u in packages/shared services/governance services/anchoring services/security services/analytics services/transfer services/referral services/nft-certificate services/staking services/kyc services/tenant-provisioning services/billing services/timestamping services/vc-issuer services/m365-integration services/prism services/demo-service services/originate; do
  n=$(echo $u | tr / _)
  "$D/node_modules/.bin/tsc" --noEmit -p "$D/$u/tsconfig.json" > $O/tsc_$n.log 2>&1; echo "$u tsc rc=$? errors=$(grep -c 'error TS' $O/tsc_$n.log)" >> $O/summary.txt
  t=$(node -p "require('$D/$u/package.json').scripts.test||''")
  if [[ "$t" == *jest* ]]; then npm --prefix "$D/$u" run test > $O/test_$n.log 2>&1; rc=$?; tl=$(grep -E '^Tests:' $O/test_$n.log | tail -1)
  else
    if [[ "$t" == *"vitest run"* ]]; then npm --prefix "$D/$u" run test > $O/test_$n.log 2>&1; rc=$?; else npm --prefix "$D/$u" run test -- --run > $O/test_$n.log 2>&1; rc=$?; fi
    tl=$(grep -E '^\s+Tests ' $O/test_$n.log | tail -1)
  fi
  echo "$u test rc=$rc $tl" >> $O/summary.txt
done
echo ALLDONE >> $O/summary.txt
