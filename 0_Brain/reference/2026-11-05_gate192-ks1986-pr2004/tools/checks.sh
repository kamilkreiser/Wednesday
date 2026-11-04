#!/bin/bash
# Gate 192: red-at-base (unit), tsc over the test files with jest types, eslint on the three files, docs-fragments check + planted defect.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004
R=$W/repo; D=$R/Blockchain/Dev; S=$D/services/originate
REL=Blockchain/Dev/services/originate/src/routes/verification.ts
E="env -i PATH=$PATH HOME=$W/home TMPDIR=$W/tmp"
T1=$S/src/__tests__/ks1986-v1-original-across-tenants.test.ts
T2=$S/src/__tests__/ks1561-g188-f1-original-outside-the-fetched-row-set.test.ts
cd $W/cwd || exit 9

# 1. red at base: base verification.ts under the head tests
git -C $R show 035685291b9d:$REL > $R/$REL
$E $D/node_modules/.bin/jest -c $S/jest.config.js --rootDir $S --cacheDirectory $W/tmp/jestcache --runTestsByPath $T1 $T2 > $W/runs/red_base.out 2>&1
echo "red-at-base jest rc=$?"
git -C $R checkout -- $REL
echo "restored blob equal head: $([ "$(git -C $R hash-object $R/$REL)" = "$(git -C $R rev-parse 577f668f:$REL)" ] && echo yes || echo NO)"
grep -E "^Tests:" $W/runs/red_base.out
echo "error TS: $(grep -c 'error TS' $W/runs/red_base.out)  TypeError: $(grep -c 'TypeError' $W/runs/red_base.out)  Expected: $(grep -c 'Expected' $W/runs/red_base.out)"

# 2. tsc over the PR's test files + verification.ts with jest types (a temporary tsconfig in the gate's tmp)
cat > $W/tmp/tsconfig.tests.json <<JSON
{ "extends": "$S/tsconfig.json", "compilerOptions": { "noEmit": true, "types": ["jest", "node"], "rootDir": "$D", "typeRoots": ["$D/node_modules/@types", "$S/node_modules/@types"] },
  "include": [], "files": ["$T1", "$T2", "$S/src/routes/verification.ts"] }
JSON
$E $D/node_modules/.bin/tsc -p $W/tmp/tsconfig.tests.json > $W/runs/tsc_tests.out 2>&1
echo "tsc tests rc=$? errors=$(grep -c 'error TS' $W/runs/tsc_tests.out)"
# control: plant a type error in a COPY of the test file inside tmp and compile it the same way
cp $T1 $W/tmp/planted.test.ts; echo 'const g192Planted: number = "not a number";' >> $W/tmp/planted.test.ts
sed "s#\"$T1\"#\"$W/tmp/planted.test.ts\"#" $W/tmp/tsconfig.tests.json > $W/tmp/tsconfig.planted.json
$E $D/node_modules/.bin/tsc -p $W/tmp/tsconfig.planted.json > $W/runs/tsc_planted.out 2>&1
echo "tsc planted control rc=$? errors=$(grep -c 'error TS' $W/runs/tsc_planted.out)"

# 3. eslint on the three files
cd $D || exit 9
$E $D/node_modules/.bin/eslint $S/src/routes/verification.ts $T1 $T2 > $W/runs/eslint.out 2>&1
echo "eslint rc=$? problems-lines=$(grep -cE '^\s+[0-9]+:[0-9]+' $W/runs/eslint.out)"
cd $W/cwd || exit 9
