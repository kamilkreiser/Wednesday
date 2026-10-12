#!/bin/bash
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g1521r1
for T in head dev; do
  D=$W/$T/Blockchain/Dev
  echo "== $T $(git -C $W/$T rev-parse --short HEAD) index.ts sha16 $(shasum -a 256 $D/services/security/src/index.ts | cut -c1-16) stray-gate-files: $(ls $D/services/security/src/__tests__ | grep -c zz_gate)"
  (cd $D/services/security && unset DATABASE_URL GATE_DB; npx vitest run) > $W/out/suite-sec-$T.log 2>&1; echo "security rc=$? $(grep -E '^\s+(Test Files|Tests) ' $W/out/suite-sec-$T.log | tr -s ' ' | tr '\n' ' ')"
  (cd $D/packages/shared && npx vitest run) > $W/out/suite-shared-$T.log 2>&1; echo "shared rc=$? $(grep -E '^\s+(Test Files|Tests) ' $W/out/suite-shared-$T.log | tr -s ' ' | tr '\n' ' ')"
  (cd $D/services/security && npx tsc --noEmit -p tsconfig.json) > $W/out/tsc-$T.log 2>&1; echo "tsc(security) rc=$? lines=$(wc -l < $W/out/tsc-$T.log)"
  (cd $D && npx eslint services/security/src/index.ts services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts) > $W/out/eslint-$T.log 2>&1; echo "eslint rc=$? lines=$(wc -l < $W/out/eslint-$T.log)"
done
