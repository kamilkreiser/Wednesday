#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate115-ks1725-pr1933/repo
L=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate115-ks1725-pr1933/logs
D=$R/Blockchain/Dev
BASE=8f313815f415c65849210f5d3e30cae44d15a516; HEAD=750da5097e6ba79c0c8c624da4de0f5e2acd4a9d
FILES=$(git -C $R diff --name-only $BASE $HEAD)
for f in $FILES; do git -C $R show "$BASE:$f" > "$R/$f"; done
git -C $R diff --stat $BASE -- $FILES > $L/base_run_swapcheck.log  # expect empty
npm --prefix $D ci --ignore-scripts > $L/base_ci_root.log 2>&1; echo "base root ci rc=$?"
npm --prefix $D/packages/shared run build > $L/base_build_shared.log 2>&1; echo "base build rc=$?"
node /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate115-ks1725-pr1933/scripts/resolve.cjs $D $D/packages/shared/src/vault/key-vault.ts $D/services/m365-integration/src/auth/token-manager.ts > $L/resolve_base_rootci.log 2>&1
npm --prefix $D/services/m365-integration test > $L/base_test_m365.log 2>&1; echo "base m365 rc=$?"
npm --prefix $D/packages/shared test > $L/base_test_shared.log 2>&1; echo "base shared rc=$?"
$D/node_modules/.bin/tsc -p $D/packages/shared/tsconfig.gate115.json > $L/base_tsc_shared.log 2>&1; echo "base tsc shared rc=$?"
$D/node_modules/.bin/tsc -p $D/services/m365-integration/tsconfig.test.json --noEmit > $L/base_tsc_m365.log 2>&1; echo "base tsc m365 rc=$?"
for f in $FILES; do git -C $R show "$HEAD:$f" > "$R/$f"; done
git -C $R status --short > $L/base_run_restore_status.log; echo "restore status lines: $(grep -v -c 'tsconfig.gate115\|^?? Blockchain/Dev/packages/shared/tsconfig' $L/base_run_restore_status.log)"
npm --prefix $D ci --ignore-scripts > $L/head_ci_root_r2.log 2>&1; echo "head root ci again rc=$?"
npm --prefix $D/packages/shared run build > $L/head_build_shared_r2.log 2>&1; echo "head build again rc=$?"
