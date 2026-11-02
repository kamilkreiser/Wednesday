#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941; R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350; FILES="src/routes/verification.ts src/routes/verificationV2.ts"
mkdir -p $L/_quarantine $L/tsc_base_q
TSC=$D/node_modules/.bin/tsc
$TSC -p $A/tsconfig.json --noEmit > $L/tsc_plain_head.log 2>&1; echo "rc=$?" >> $L/tsc_plain_head.log
$TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_head.log 2>&1; echo "rc=$?" >> $L/tsc_tests_head.log
$TSC -p $W/scripts/tsconfig.tests.json --listFilesOnly 2>/dev/null | /usr/bin/grep -c "/services/originate/src/__tests__/.*\.test\.ts$" > $L/tsc_tests_count_head.log
P=$A/src/__tests__/zz-gate123-planted.test.ts; printf "const zzPlanted: number = 'x';\n" > $P
$TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_planted.log 2>&1; echo "rc=$?" >> $L/tsc_tests_planted.log
mv $P $L/_quarantine/planted_tsc.test.ts
# base tsc with tests (new tests removed, base product)
for f in $FILES; do shasum -a 256 $A/$f; done > $L/tscb_before.txt
for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done
NEWT=$(git -C $R diff --name-only $MB pr1941 -- Blockchain/Dev/services/originate/src/__tests__)
for t in $NEWT; do mv $R/$t $L/tsc_base_q/; done
$TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_base.log 2>&1; echo "rc=$?" >> $L/tsc_tests_base.log
$TSC -p $W/scripts/tsconfig.tests.json --listFilesOnly 2>/dev/null | /usr/bin/grep -c "/src/__tests__/.*\.test\.ts$" > $L/tsc_tests_count_base.log
for t in $NEWT; do mv $L/tsc_base_q/$(basename $t) $R/$t; done
git -C $R checkout -- Blockchain/Dev/services/originate/src/routes
for f in $FILES; do shasum -a 256 $A/$f; done > $L/tscb_after.txt; cmp $L/tscb_before.txt $L/tscb_after.txt && echo TSCB_RESTORE_OK
# eslint (config resolution from the file path; cwd irrelevant for flat config? record)
F="$A/src/routes/verification.ts $A/src/routes/verificationV2.ts $(for t in $NEWT; do echo $R/$t; done)"
$D/node_modules/.bin/eslint --config $D/eslint.config.mjs $F > $L/eslint_pr_files.log 2>&1; echo "rc=$?" >> $L/eslint_pr_files.log
P2=$A/src/zz-gate123-lint.ts; printf "export function f() { const unused = 1; debugger; }\n" > $P2
$D/node_modules/.bin/eslint --config $D/eslint.config.mjs $P2 > $L/eslint_planted.log 2>&1; echo "rc=$?" >> $L/eslint_planted.log
mv $P2 $L/_quarantine/planted_lint.ts
# docs-fragments (script resolves the repo from its own path? record)
FR="$R/Projects Documents/fragments/cheat/KS-1868-originate-verification-coerce-message-and-chain-fact.html"
node $D/scripts/docs-fragments.mjs check > $L/frag_head.log 2>&1; echo "rc=$?" >> $L/frag_head.log
h0=$(shasum -a 256 "$FR" | cut -d" " -f1); cp "$FR" $L/_quarantine/frag_orig.html; printf "<div>\n" >> "$FR"
node $D/scripts/docs-fragments.mjs check > $L/frag_planted.log 2>&1; echo "rc=$?" >> $L/frag_planted.log
cp $L/_quarantine/frag_orig.html "$FR"; [ "$(shasum -a 256 "$FR" | cut -d" " -f1)" = "$h0" ] && echo FRAG_RESTORED
git -C $R status --short
