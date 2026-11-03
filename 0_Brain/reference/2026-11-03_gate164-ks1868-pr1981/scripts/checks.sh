#!/bin/bash
# G164: test-types ratchet base/head + planted; tsc service; eslint test file + product + planted; docs-fragments + planted.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate164-ks1868-pr1981
R=$W/repo; DEV=$R/Blockchain/Dev; S=$DEV/services/security
BASE=0a6575f7fd92d60849d1186efa0632961db21be5; HEAD=2e0f5ec046d640c1f83dcf248f15e4d570340959
T=$S/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts
for v in $BASE $HEAD; do
  git -C $R checkout -q --detach $v
  node $W/harness/inroot.js "$DEV" node scripts/typecheck-tests/check.cjs services/security > $W/logs/ratchet_${v:0:7}.log 2>&1
  echo "ratchet ${v:0:7} rc=$?"; tail -4 $W/logs/ratchet_${v:0:7}.log
done
echo "== ratchet planted (type error in the head test file)"
printf '\nconst g164Planted: number = "x";\nexport { g164Planted };\n' >> $T
node $W/harness/inroot.js "$DEV" node scripts/typecheck-tests/check.cjs services/security > $W/logs/ratchet_planted.log 2>&1; echo "planted rc=$?"; tail -3 $W/logs/ratchet_planted.log
git -C $R checkout -q -- Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts
echo "== tsc service tsconfig head"; $DEV/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/tsc_svc_head.log 2>&1; echo "rc=$? errors=$(grep -c 'error TS' $W/logs/tsc_svc_head.log)"
echo "== tsc planted"; printf '\nconst g164P: number = "x";\nexport { g164P };\n' >> $S/src/index.ts
$DEV/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/tsc_planted.log 2>&1; echo "rc=$? errors=$(grep -c 'error TS' $W/logs/tsc_planted.log)"
git -C $R checkout -q -- Blockchain/Dev/services/security/src/index.ts
echo "== eslint head (test file)"; node $W/harness/eslint_run.js $T | tail -4
echo "== eslint head (index.ts, product) and base index.ts for comparison"; node $W/harness/eslint_run.js $S/src/index.ts | tail -1
git -C $R show $BASE:Blockchain/Dev/services/security/src/index.ts > $S/src/index.ts; node $W/harness/eslint_run.js $S/src/index.ts | tail -1; git -C $R checkout -q -- Blockchain/Dev/services/security/src/index.ts
echo "== eslint planted"; printf '\nfunction g164p() { debugger; const unusedG164 = 1; }\nexport { g164p };\n' >> $T
node $W/harness/eslint_run.js $T | tail -3
git -C $R checkout -q -- Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts
echo "== docs-fragments check head"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_head.log 2>&1; echo rc=$?; tail -3 $W/logs/frag_head.log
F="$R/Projects Documents/fragments/flow/KS-1868-security-rotate.html"
echo "== planted flow unclosed div"; printf '<div>\n' >> "$F"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_planted_flow.log 2>&1; echo rc=$?; tail -2 $W/logs/frag_planted_flow.log
git -C $R checkout -q -- "Projects Documents/fragments/flow/KS-1868-security-rotate.html"
echo "== after restore"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_after.log 2>&1; echo rc=$?
echo "HEAD=$(git -C $R rev-parse --short HEAD) status=$(git -C $R status --porcelain | wc -l)"
