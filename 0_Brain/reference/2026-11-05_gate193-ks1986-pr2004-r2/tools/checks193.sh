#!/bin/bash
# Gate 193 Q9: red proof at 577f, whole originate suite, tsc (project + test files with jest types, planted control), eslint on the
# touched TS files (planted control), docs-fragments check clean / planted dangling ref / restored. All in the gate's OWN clone, CWD in
# the workdir, env -i. LINEAGE: gate 192's tools/checks.sh, suite.sh, docs_lint.sh, re-keyed to head 4432db22.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2
R=$W/repo; D=$R/Blockchain/Dev; S=$D/services/originate
HEADC=4432db224a5867fdb6afaabf56df08cdf640d067; R1=577f668f478679a3e4965a28fba6b96a9e2212d6
REL=Blockchain/Dev/services/originate/src/routes/verification.ts
E="env -i PATH=$PATH HOME=$W/home TMPDIR=$W/tmp"
T1=$S/src/__tests__/ks1986-v1-original-across-tenants.test.ts
T2=$S/src/__tests__/ks1561-g188-f1-original-outside-the-fetched-row-set.test.ts
T3=$S/src/__tests__/ks1561-verify-original-registrant-certifier.test.ts
blobok() { [ "$(git -C $R hash-object $R/$REL)" = "$(git -C $R rev-parse $HEADC:$REL)" ] && echo yes || echo NO; }
cd $W/cwd || exit 9

echo "== 1. red proof: 577f verification.ts under head's KS-1986 test file"
git -C $R show $R1:$REL > $R/$REL
$E $D/node_modules/.bin/jest -c $S/jest.config.js --rootDir $S --cacheDirectory $W/tmp/jestcache --runTestsByPath $T1 > $W/runs/red_r1.out 2>&1
echo "red-at-577f jest rc=$?"
git -C $R checkout -- $REL; echo "restored blob equal head: $(blobok)"
grep -E "^Tests:" $W/runs/red_r1.out
echo "TS diagnostics: $(grep -cE 'TS[0-9]{4}' $W/runs/red_r1.out)  TypeError: $(grep -c TypeError $W/runs/red_r1.out)  suite-failed-to-run: $(grep -c 'Test suite failed to run' $W/runs/red_r1.out)"
grep -E "^\s+✕" $W/runs/red_r1.out
echo "-- control: the same file at head"
$E $D/node_modules/.bin/jest -c $S/jest.config.js --rootDir $S --cacheDirectory $W/tmp/jestcache --runTestsByPath $T1 > $W/runs/green_t1.out 2>&1
echo "head jest rc=$?"; grep -E "^Tests:" $W/runs/green_t1.out
echo "-- control for the TS counter: a planted type error in a copy of the test file, same counter"
P=$S/src/__tests__/g193-planted-ts.test.ts
cp $T1 $P; echo 'const g193Planted: number = "not a number"; void g193Planted;' >> $P
$E $D/node_modules/.bin/jest -c $S/jest.config.js --rootDir $S --cacheDirectory $W/tmp/jestcache --runTestsByPath $P > $W/runs/ts_planted_jest.out 2>&1
echo "planted jest rc=$? TS diagnostics: $(grep -cE 'TS[0-9]{4}' $W/runs/ts_planted_jest.out)"
mv $P $W/tmp/g193-planted-ts.test.ts.quarantine

echo "== 2. the three unit files at head"
$E $D/node_modules/.bin/jest -c $S/jest.config.js --rootDir $S --cacheDirectory $W/tmp/jestcache --runTestsByPath $T1 $T2 $T3 > $W/runs/unit3_head.out 2>&1
echo "rc=$?"; grep -E "^Tests:|^Test Suites:" $W/runs/unit3_head.out

echo "== 3. whole originate suite at head"
echo "verification.ts blob equal head: $(blobok)"
$E $D/node_modules/.bin/jest -c $S/jest.config.js --rootDir $S --cacheDirectory $W/tmp/jestcache --json --outputFile=$W/runs/suite.json > $W/runs/suite.log 2>&1
echo "jest rc=$?"
python3 -I -c "import json; j=json.load(open('$W/runs/suite.json')); print('tests', j['numPassedTests'], 'of', j['numTotalTests'], 'failed', j['numFailedTests'], 'pending', j['numPendingTests'], '| suites', j['numPassedTestSuites'], 'of', j['numTotalTestSuites'], 'failed', j['numFailedTestSuites'])"

echo "== 4. tsc"
$E $D/node_modules/.bin/tsc --noEmit -p $S/tsconfig.json > $W/runs/tsc.out 2>&1; echo "tsc -p originate rc=$? errors=$(grep -c 'error TS' $W/runs/tsc.out)"
cat > $W/tmp/tsconfig.tests.json <<JSON
{ "extends": "$S/tsconfig.json", "compilerOptions": { "noEmit": true, "types": ["jest", "node"], "rootDir": "$D", "typeRoots": ["$D/node_modules/@types", "$S/node_modules/@types"] },
  "include": [], "files": ["$T1", "$T2", "$T3", "$S/src/routes/verification.ts"] }
JSON
$E $D/node_modules/.bin/tsc -p $W/tmp/tsconfig.tests.json > $W/runs/tsc_tests.out 2>&1; echo "tsc tests rc=$? errors=$(grep -c 'error TS' $W/runs/tsc_tests.out)"
cp $T1 $W/tmp/planted.test.ts; echo 'const g193Planted: number = "not a number";' >> $W/tmp/planted.test.ts
sed "s#\"$T1\"#\"$W/tmp/planted.test.ts\"#" $W/tmp/tsconfig.tests.json > $W/tmp/tsconfig.planted.json
$E $D/node_modules/.bin/tsc -p $W/tmp/tsconfig.planted.json > $W/runs/tsc_planted.out 2>&1; echo "tsc planted control rc=$? errors=$(grep -c 'error TS' $W/runs/tsc_planted.out)"

echo "== 5. eslint on the touched TS files (round 2: verification.ts + the KS-1986 test) and the full range's third TS file"
cd $D || exit 9
$E $D/node_modules/.bin/eslint $S/src/routes/verification.ts $T1 $T2 > $W/runs/eslint.out 2>&1; echo "eslint rc=$? problem-lines=$(grep -cE '^\s+[0-9]+:[0-9]+' $W/runs/eslint.out)"
P=$S/src/__tests__/g193-planted-lint.test.ts
cp $T1 $P; printf '%s\n' 'var g193Planted: any = 1; // eslint control' >> $P
$E $D/node_modules/.bin/eslint $P > $W/runs/eslint_planted.out 2>&1; echo "eslint planted control rc=$? problem-lines=$(grep -cE '^\s+[0-9]+:[0-9]+' $W/runs/eslint_planted.out)"
mv $P $W/tmp/g193-planted-lint.test.ts.quarantine

echo "== 6. docs-fragments"
FL="$R/Projects Documents/fragments/flow/KS-1986-v1-original-across-tenants.html"
cd $R || exit 9
$E node $D/scripts/docs-fragments.mjs check > $W/runs/docs_clean.out 2>&1; echo "docs clean rc=$?"
cp "$FL" $W/tmp/flow.orig
printf '%s\n' '<p>see <!--ref:KS-9999-g193-planted-dangling-ref--></p>' >> "$FL"
$E node $D/scripts/docs-fragments.mjs check > $W/runs/docs_planted.out 2>&1; echo "docs planted (dangling ref) rc=$?"
cp $W/tmp/flow.orig "$FL"
git -C $R diff --quiet -- "Projects Documents" && echo "restored: git diff clean"
$E node $D/scripts/docs-fragments.mjs check > $W/runs/docs_restored.out 2>&1; echo "docs restored rc=$?"
echo "== git status of the clone (expect clean)"; git -C $R status --porcelain | head
