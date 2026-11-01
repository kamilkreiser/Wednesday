#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate96-ks1868-pr1914
RR=$W/repo; A=$RR/Blockchain/Dev/services/analytics; L=$W/logs
P=Blockchain/Dev/services/analytics/src/routes/analytics.ts
pushd $A >/dev/null
HS=$(shasum -a 256 src/routes/analytics.ts | cut -c1-64); echo head product sha $HS
npx vitest run > $L/head_whole.log 2>&1; echo head_whole RC=$?; grep -E 'Test Files|Tests ' $L/head_whole.log
npx vitest run src/__tests__/ks1868-analytics-routes > $L/head_new.log 2>&1; echo head_new RC=$?; grep -E 'Test Files|Tests ' $L/head_new.log
# head x3 for stability
for i in 1 2; do npx vitest run src/__tests__/ks1868-analytics-routes 2>&1 | grep -E 'Tests ' ; done
# base product
git -C $RR show 03977e89a343:$P > src/routes/analytics.ts
echo base product sha $(shasum -a 256 src/routes/analytics.ts | cut -c1-16)
npx vitest run src/__tests__/ks1868-analytics-routes > $L/red_base_new.log 2>&1; echo red_base RC=$?; grep -E 'Test Files|Tests ' $L/red_base_new.log
npx vitest run --exclude 'src/__tests__/ks1868-analytics-routes-*' > $L/base_whole_excl_new.log 2>&1; echo base_excl RC=$?; grep -E 'Test Files|Tests ' $L/base_whole_excl_new.log
npx vitest run > $L/base_whole_incl_new.log 2>&1; echo base_incl RC=$?; grep -E 'Test Files|Tests ' $L/base_whole_incl_new.log
git -C $RR show refs/qa/pr1914:$P > src/routes/analytics.ts
[ "$(shasum -a 256 src/routes/analytics.ts | cut -c1-64)" = "$HS" ] && echo RESTORE_OK || echo RESTORE_FAIL
