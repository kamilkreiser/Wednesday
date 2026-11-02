#!/bin/bash
# tsc (plain + tests in program, planted control), eslint (changed files + planted), docs-fragments (head + planted). Run with HEAD product in place.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate106-ks1868-pr1925; R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs
mkdir -p $L/_quarantine
TSC=$D/node_modules/.bin/tsc
(cd $A && $TSC -p tsconfig.json --noEmit > $L/tsc_plain_head.log 2>&1; echo "rc=$?" >> $L/tsc_plain_head.log)
(cd $A && $TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_head.log 2>&1; echo "rc=$?" >> $L/tsc_tests_head.log)
(cd $A && $TSC -p $W/scripts/tsconfig.tests.json --listFilesOnly 2>/dev/null | /usr/bin/grep -c "/services/originate/src/__tests__/.*\.test\.ts$" > $L/tsc_tests_count.log; $TSC -p $W/scripts/tsconfig.tests.json --listFilesOnly 2>/dev/null | /usr/bin/grep -c "ks1868-verification" >> $L/tsc_tests_count.log)
P=$A/src/__tests__/zz-gate106-planted.test.ts; printf "const zzPlanted: number = 'x';\n" > $P
(cd $A && $TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_planted.log 2>&1; echo "rc=$?" >> $L/tsc_tests_planted.log)
mv $P $L/_quarantine/planted_tsc.test.ts
F="src/routes/verification.ts src/routes/verificationV2.ts src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts src/__tests__/ks1868-verification-verify-file-route-catch-p2-unreadable-throw.test.ts src/__tests__/ks1868-verification-verify-hash-status-route-catches-p1-unreadable-throw.test.ts"
(cd $A && $D/node_modules/.bin/eslint $F > $L/eslint_pr_files.log 2>&1; echo "rc=$?" >> $L/eslint_pr_files.log)
P2=$A/src/zz-gate106-lint.ts; printf "export function f() { const unused = 1; debugger; }\n" > $P2
(cd $A && $D/node_modules/.bin/eslint src/zz-gate106-lint.ts > $L/eslint_planted.log 2>&1; echo "rc=$?" >> $L/eslint_planted.log)
mv $P2 $L/_quarantine/planted_lint.ts
FR="$R/Projects Documents/fragments/cheat/KS-1868-originate-verification-route-catches-unreadable-thrown-value.html"
(cd $R && node Blockchain/Dev/scripts/docs-fragments.mjs check > $L/frag_head.log 2>&1; echo "rc=$?" >> $L/frag_head.log)
h0=$(shasum -a 256 "$FR" | cut -d" " -f1); cp "$FR" $L/_quarantine/frag_orig.html; printf "<div>\n" >> "$FR"
(cd $R && node Blockchain/Dev/scripts/docs-fragments.mjs check > $L/frag_planted.log 2>&1; echo "rc=$?" >> $L/frag_planted.log)
cp $L/_quarantine/frag_orig.html "$FR"; [ "$(shasum -a 256 "$FR" | cut -d" " -f1)" = "$h0" ] && echo FRAG_RESTORED
git -C $R status --short
