#!/bin/bash
# tsc (plain + with tests, head vs base), eslint, docs-fragments (+ planted defect), merge-tree
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920
R=$G/repo; D=$R/Blockchain/Dev; A=$D/services/analytics; L=$G/logs
REL=Blockchain/Dev/services/analytics/src/services/scheduledJobs.ts
TREL=Blockchain/Dev/services/analytics/src/__tests__/ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts
TSC=$D/node_modules/.bin/tsc
cd "$A"
cat > $G/scripts/tsconfig.gate102.json <<J
{ "extends": "$A/tsconfig.json", "compilerOptions": { "noEmit": true, "rootDir": "$A/src" }, "include": ["$A/src/**/*"], "exclude": ["$A/node_modules","$A/dist"] }
J
echo "--- plain tsc head"
$TSC -p tsconfig.json --noEmit > $L/tsc_plain_head.log 2>&1; echo rc=$?
echo "--- tsc with tests head"
$TSC -p $G/scripts/tsconfig.gate102.json > $L/tsc_tests_head.log 2>&1; echo rc=$?; grep -c 'error TS' $L/tsc_tests_head.log; grep 'error TS' $L/tsc_tests_head.log | cut -c1-200
echo "--- tsc with tests base (product at base, new test moved aside)"
cp $A/src/services/scheduledJobs.ts $L/head_product.ts
git -C $R show origin/develop:$REL > $A/src/services/scheduledJobs.ts
mv $A/src/__tests__/ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts $G/_quarantine/newtest_for_base_tsc.ts
$TSC -p $G/scripts/tsconfig.gate102.json > $L/tsc_tests_base.log 2>&1; echo rc=$?; grep -c 'error TS' $L/tsc_tests_base.log
mv $G/_quarantine/newtest_for_base_tsc.ts $A/src/__tests__/ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts
cp $L/head_product.ts $A/src/services/scheduledJobs.ts
diff <(grep 'error TS' $L/tsc_tests_head.log | sort) <(grep 'error TS' $L/tsc_tests_base.log | sort) > $L/tsc_diff.log; echo "sorted error lists diff rc=$?"
echo "--- tsc planted control"
printf 'const gate102Planted: number = "x";\nexport {};\n' > $A/src/__tests__/zz_planted.test.ts
$TSC -p $G/scripts/tsconfig.gate102.json > $L/tsc_planted.log 2>&1; echo rc=$?; grep 'zz_planted' $L/tsc_planted.log | cut -c1-160
mv $A/src/__tests__/zz_planted.test.ts $G/_quarantine/zz_planted.test.ts
echo "--- eslint changed files"
ESL=$D/node_modules/.bin/eslint
$ESL src/services/scheduledJobs.ts src/__tests__/ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts > $L/eslint_pr.log 2>&1; echo rc=$?; tail -5 $L/eslint_pr.log
printf 'debugger;\nconst unusedGate102 = 1;\n' > $A/src/zz_planted.ts
$ESL src/zz_planted.ts > $L/eslint_planted.log 2>&1; echo planted rc=$?; tail -6 $L/eslint_planted.log
mv $A/src/zz_planted.ts $G/_quarantine/zz_planted_eslint.ts
cd "$R"
echo "--- docs-fragments check"
node Blockchain/Dev/scripts/docs-fragments.mjs check > $L/frag_head.log 2>&1; echo rc=$?; tail -5 $L/frag_head.log | cut -c1-220
F="Projects Documents/fragments/flow/KS-1868-analytics-scheduled-jobs-catch-unreadable-thrown-value.html"
cp "$F" $G/_quarantine/frag_flow_orig.html
SHA=$(shasum -a 256 "$F" | cut -d' ' -f1)
echo '<div>unclosed planted' >> "$F"
node Blockchain/Dev/scripts/docs-fragments.mjs check > $L/frag_planted.log 2>&1; echo planted rc=$?; tail -3 $L/frag_planted.log | cut -c1-220
cp $G/_quarantine/frag_flow_orig.html "$F"
[ "$(shasum -a 256 "$F" | cut -d' ' -f1)" = "$SHA" ] && echo "frag restore True"
git -C $R status --short
echo "--- merge-tree"
git -C $R ls-remote origin refs/heads/develop
git -C $R merge-tree --write-tree origin/develop pr1920 > $L/merge_tree.log 2>&1; echo rc=$?; cat $L/merge_tree.log | head -3
