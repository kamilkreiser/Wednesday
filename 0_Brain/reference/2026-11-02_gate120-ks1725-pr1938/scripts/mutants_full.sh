#!/bin/bash
# survivors of the targeted run: re-run against the WHOLE suite of the unit
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
D=$W/repo/Blockchain/Dev; L=$W/logs/mutants; OUT=$L/summary_full.txt; : > $OUT
bash $W/scripts/co.sh pr1938 > /dev/null
run() {
  local name=$1 rel=$2 expr=$3 unit=$4
  local f=$D/$rel; local before=$(shasum -a 256 "$f" | cut -d' ' -f1)
  sed -i '' "$expr" "$f"
  cd $D/$unit && $D/node_modules/.bin/vitest run --root $D/$unit --reporter=json --outputFile=$L/full_$name.json > $L/full_$name.log 2>&1; local rc=$?
  git -C $W/repo checkout -q -- "Blockchain/Dev/$rel"
  local ok=RESTORE_OK; [ "$before" = "$(shasum -a 256 "$f" | cut -d' ' -f1)" ] || ok=RESTORE_FAILED
  echo "$name: rc=$rc $ok" >> $OUT
}
run F3_shared_typo packages/shared/src/errors/index.ts 's/err\.issues/err.issuez/' packages/shared
run F5_auth_typo services/auth/src/middleware/errorHandler.ts 's/err\.issues/err.issuez/g' services/auth
run F9_analytics_key services/analytics/src/types/analytics.types.ts 's/z\.record(z\.string(), z\.unknown())/z.record(z.number(), z.unknown())/' services/analytics
run F10_nft_key services/nft-certificate/src/routes/nft.routes.ts 's/z\.record(z\.string(), z\.unknown())/z.record(z.literal("only"), z.unknown())/' services/nft-certificate
echo DONE >> $OUT
