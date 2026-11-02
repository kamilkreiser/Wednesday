#!/bin/bash
# tsc --noEmit for the 25 touched units, head (mut tree, clean) and base. Also tsconfig.test.json where present.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
UNITS="packages/shared services/anchoring services/vc-issuer services/api-gateway services/mcp-server services/tenant-provisioning services/analytics services/auth services/billing services/demo-service services/governance services/guardian services/kyc services/m365-integration services/nft-certificate services/originate services/prism services/queue services/referral services/security services/staking services/timestamping services/tokenisation services/transfer services/wallet-connector"
for T in mut base; do
  D=$G/$T/Blockchain/Dev
  for U in $UNITS; do
    for C in tsconfig.json tsconfig.test.json; do
      [ -e $D/$U/$C ] || continue
      O=$(nice -n 10 $D/node_modules/.bin/tsc --noEmit -p $D/$U/$C 2>&1); RC=$?
      echo "$T $U $C rc=$RC errors=$(printf '%s\n' "$O" | grep -c 'error TS')"
      printf '%s\n' "$O" | grep 'error TS' | sed "s#^#   #" | head -5
    done
  done
done
