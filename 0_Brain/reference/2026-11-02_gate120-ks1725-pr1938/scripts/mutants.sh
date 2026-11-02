#!/bin/bash
# product-only mutants at head; tests untouched; sha256 restore asserted after each
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
D=$W/repo/Blockchain/Dev; L=$W/logs/mutants; mkdir -p $L; OUT=$L/summary.txt; : > $OUT
bash $W/scripts/co.sh pr1938 > /dev/null
run() { # name file sedexpr unit testpattern
  local name=$1 f=$D/$2 expr=$3 unit=$4 pat=$5
  local before=$(shasum -a 256 "$f" | cut -d' ' -f1)
  sed -i '' "$expr" "$f"
  local after=$(shasum -a 256 "$f" | cut -d' ' -f1)
  [ "$before" = "$after" ] && echo "$name: SED DID NOT CHANGE FILE" >> $OUT
  cd $D/$unit && $D/node_modules/.bin/vitest run --root $D/$unit $pat > $L/$name.log 2>&1; local rc=$?
  git -C $W/repo checkout -q -- "Blockchain/Dev/$2"
  local restored=$(shasum -a 256 "$f" | cut -d' ' -f1)
  local ok=RESTORE_OK; [ "$before" = "$restored" ] || ok=RESTORE_FAILED
  local line=$(grep -E '^ +Tests ' $L/$name.log | head -1)
  echo "$name: vitest rc=$rc | $line | $ok" >> $OUT
}
# M1: revert ONE tenant-provisioning site back to .errors (the source-count cell C3 should name it)
run M1_tp_one_site services/tenant-provisioning/src/index.ts '1,/details: err\.issues/ s/details: err\.issues/details: err.errors/' services/tenant-provisioning ks1410
# M2: revert all three
run M2_tp_all_sites services/tenant-provisioning/src/index.ts 's/details: err\.issues/details: err.errors/' services/tenant-provisioning ks1410
# M3: typo in shared errorHandler (.issuez) -> a 422 for a ZodError must break
run M3_shared_typo packages/shared/src/errors/index.ts 's/err\.issues/err.issuez/' packages/shared error-handler
# M4: revert shared errorHandler to .errors (equivalent on zod 3: expect SURVIVE = no test pins the spelling)
run M4_shared_revert packages/shared/src/errors/index.ts 's/err\.issues/err.errors/' packages/shared error-handler
# M5: auth errorHandler typo
run M5_auth_typo services/auth/src/middleware/errorHandler.ts 's/err\.issues\[0\]/err.issuez[0]/' services/auth ks703 ks1013 ks622 ks1467-the-weak
# M6: auth errorHandler revert (equivalent)
run M6_auth_revert services/auth/src/middleware/errorHandler.ts 's/err\.issues/err.errors/g' services/auth ks703 ks1013 ks622 ks1467-the-weak
# M7: requestRefusal typo
run M7_refusal_typo services/security/src/requestRefusal.ts 's/error\.issues\[0\]/error.issuez[0]/' services/security ks976a
# M8: referral errorHandler revert (equivalent)
run M8_referral_revert services/referral/src/middleware/errorHandler.ts 's/err\.issues/err.errors/' services/referral errorHandler
# M9: z.record key narrowed to z.number() in analytics filters (behaviour change on zod 3: string keys rejected)
run M9_record_key_number services/analytics/src/types/analytics.types.ts 's/z\.record(z\.string(), z\.unknown())/z.record(z.number(), z.unknown())/' services/analytics exportReportRequest
# M10: nft routes record key to enum
run M10_nft_key services/nft-certificate/src/routes/nft.routes.ts 's/z\.record(z\.string(), z\.unknown())/z.record(z.literal("only"), z.unknown())/' services/nft-certificate nft
echo DONE >> $OUT
