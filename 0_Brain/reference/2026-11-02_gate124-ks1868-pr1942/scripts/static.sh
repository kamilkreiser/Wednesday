#!/bin/bash
# gate 124 static checks at head: tsc (plain + with tests + planted), eslint (API, cwd=originate, + planted), docs-fragments (+ planted)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942; R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
mkdir -p $L/_quarantine
TSC=$D/node_modules/.bin/tsc
$TSC -p $A/tsconfig.json --noEmit > $L/tsc_plain_head.log 2>&1; echo "rc=$?" >> $L/tsc_plain_head.log
$TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_head.log 2>&1; echo "rc=$?" >> $L/tsc_tests_head.log
$TSC -p $W/scripts/tsconfig.tests.json --listFilesOnly 2>/dev/null | /usr/bin/grep -c "/services/originate/src/__tests__/.*\.test\.ts$" > $L/tsc_tests_count_head.log
P=$A/src/__tests__/zz-gate124-planted.test.ts; printf "const zzPlanted: number = 'x';\n" > $P
$TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_planted.log 2>&1; echo "rc=$?" >> $L/tsc_tests_planted.log
mv $P $L/_quarantine/planted_tsc.test.ts
NEWT=$(git -C $R diff --name-only $MB pr1942 -- Blockchain/Dev/services/originate/src/__tests__ | sed "s#^#$R/#")
node $W/scripts/lint.cjs $A $A/src/routes/certifications.ts $NEWT > $L/eslint_pr_files.log 2>&1; echo "rc=$?" >> $L/eslint_pr_files.log
P2=$A/src/zz-gate124-lint.ts; printf "export function f() { const unused = 1; debugger; }\n" > $P2
node $W/scripts/lint.cjs $A $P2 > $L/eslint_planted.log 2>&1; echo "rc=$?" >> $L/eslint_planted.log
mv $P2 $L/_quarantine/planted_lint.ts
FR="$R/Projects Documents/fragments/cheat/KS-1868-originate-certifications-issue-recertify-catches-read-safely.html"
node $D/scripts/docs-fragments.mjs check > $L/frag_head.log 2>&1; echo "rc=$?" >> $L/frag_head.log
h0=$(shasum -a 256 "$FR" | cut -d" " -f1); cp "$FR" $L/_quarantine/frag_orig.html; printf "<div>\n" >> "$FR"
node $D/scripts/docs-fragments.mjs check > $L/frag_planted.log 2>&1; echo "rc=$?" >> $L/frag_planted.log
cp $L/_quarantine/frag_orig.html "$FR"; [ "$(shasum -a 256 "$FR" | cut -d" " -f1)" = "$h0" ] && echo FRAG_RESTORED
node $D/scripts/docs-fragments.mjs check > $L/frag_after_restore.log 2>&1; echo "rc=$?" >> $L/frag_after_restore.log
git -C $R status --short
