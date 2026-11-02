#!/bin/bash
# Whole suites of the 25 touched units, base (c70f3390 worktree) then head, one unit at a time, 2 workers.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
mkdir -p $G/logs/suites
UNITS="packages/shared services/anchoring services/vc-issuer services/api-gateway services/mcp-server services/tenant-provisioning services/analytics services/auth services/billing services/demo-service services/governance services/guardian services/kyc services/m365-integration services/nft-certificate services/originate services/prism services/queue services/referral services/security services/staking services/timestamping services/tokenisation services/transfer services/wallet-connector"
for U in $UNITS; do
  N=$(echo $U | tr / _)
  for T in base repo; do
    bash $G/scripts/vt.sh $T $U $G/logs/suites/${N}_$T.log; echo "$U $T rc=$?" >> $G/logs/suites/_progress.log
  done
done
echo DONE >> $G/logs/suites/_progress.log
