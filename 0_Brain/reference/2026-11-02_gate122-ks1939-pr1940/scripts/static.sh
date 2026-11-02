#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940; R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs
mkdir -p $L/_quarantine $L/tsc_base_q; TSC=$D/node_modules/.bin/tsc; TC=$W/scripts/tsconfig.tests.json
F=src/routes/verification.ts; MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
cnt(){ $TSC -p $TC --listFilesOnly 2>/dev/null | /usr/bin/grep -c "/services/originate/src/__tests__/.*\.test\.ts$"; }
$TSC -p $A/tsconfig.json --noEmit > $L/tsc_plain_head.log 2>&1; echo "rc=$?" >> $L/tsc_plain_head.log
$TSC -p $TC > $L/tsc_tests_head.log 2>&1; echo "rc=$?" >> $L/tsc_tests_head.log; echo "test files in program: $(cnt)" >> $L/tsc_tests_head.log
# base: base product, new tests moved out
h0=$(sha $A/$F); git -C $R show $MB:Blockchain/Dev/services/originate/$F > $A/$F
mv $A/src/__tests__/ks1939-verification-*.test.ts $L/tsc_base_q/
$TSC -p $TC > $L/tsc_tests_base.log 2>&1; echo "rc=$?" >> $L/tsc_tests_base.log; echo "test files in program: $(cnt)" >> $L/tsc_tests_base.log
mv $L/tsc_base_q/ks1939-verification-*.test.ts $A/src/__tests__/
git -C $R show 96208f377d14:Blockchain/Dev/services/originate/$F > $A/$F; [ "$(sha $A/$F)" = "$h0" ] && echo TSC_RESTORE_OK
P=$A/src/__tests__/zz-gate122-planted.test.ts; printf "const zzPlanted: number = 'x';\nexport {};\n" > $P
$TSC -p $TC > $L/tsc_tests_planted.log 2>&1; echo "rc=$?" >> $L/tsc_tests_planted.log
mv $P $L/_quarantine/planted_tsc.test.ts
E="$A/src/routes/verification.ts $A/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts $A/src/__tests__/ks1939-verification-lookup-catch-unreadable-throw.test.ts"
$D/node_modules/.bin/eslint --resolve-plugins-relative-to $D $E > $L/eslint_pr_files.log 2>&1; echo "rc=$?" >> $L/eslint_pr_files.log
P2=$A/src/zz-gate122-lint.ts; printf "export function f() { const unused = 1; debugger; }\n" > $P2
$D/node_modules/.bin/eslint $P2 > $L/eslint_planted.log 2>&1; echo "rc=$?" >> $L/eslint_planted.log
mv $P2 $L/_quarantine/planted_lint.ts
for k in flow cheat; do
  FR="$R/Projects Documents/fragments/$k/KS-1939-originate-verify-by-id-answer-and-lookup-catch.html"
  node $D/scripts/docs-fragments.mjs check > $L/frag_head_$k.log 2>&1; echo "rc=$?" >> $L/frag_head_$k.log
  h1=$(sha "$FR"); cp "$FR" $L/_quarantine/frag_orig_$k.html; printf "<div>\n" >> "$FR"
  node $D/scripts/docs-fragments.mjs check > $L/frag_planted_$k.log 2>&1; echo "rc=$?" >> $L/frag_planted_$k.log
  cp $L/_quarantine/frag_orig_$k.html "$FR"; [ "$(sha "$FR")" = "$h1" ] && echo FRAG_RESTORED_$k
done
git -C $R status --short
