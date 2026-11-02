#!/bin/bash
# tsc with zod mapped to a scratch zod 4.6.7 (units' own tsconfig, noEmit); counts errors at base and head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
D=$W/repo/Blockchain/Dev; Z=$W/zod4/node_modules/zod; L=$W/logs/z4; mkdir -p $L
for pair in "8f313815f415 base" "pr1938 head"; do
  set -- $pair; bash $W/scripts/co.sh $1 > /dev/null
  $D/node_modules/.bin/tsc -p $D/packages/shared/tsconfig.json > /dev/null 2>&1
  for u in packages/shared services/anchoring services/auth services/governance services/security services/analytics services/billing services/kyc services/m365-integration services/nft-certificate services/originate services/prism services/referral services/shared services/staking services/tenant-provisioning services/timestamping services/transfer services/vc-issuer; do
    n=$(echo $u | tr / _)
    cat > $D/$u/tsconfig.z4.json <<EOT
{"extends":"./tsconfig.json","compilerOptions":{"noEmit":true,"baseUrl":".","paths":{"zod":["$Z"],"zod/*":["$Z/*"]}}}
EOT
    cd $D/$u && $D/node_modules/.bin/tsc -p $D/$u/tsconfig.z4.json > $L/${2}_$n.log 2>&1
    echo "$2 $u $(grep -c 'error TS' $L/${2}_$n.log)" >> $L/summary.txt
    rm -f $D/$u/tsconfig.z4.json
  done
done
echo DONE >> $L/summary.txt
