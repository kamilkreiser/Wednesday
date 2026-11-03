#!/bin/bash
# G161: test-types ratchet base/head + planted; tsc service; eslint changed .ts + planted; docs-fragments check + planted.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate161-ks1868-pr1978
R=$W/repo; DEV=$R/Blockchain/Dev; A=$DEV/services/auth; S=$A/src/services; TD=$A/src/__tests__
BASE=66cbe4e52d5afadc9d13ca141200026cc68d5095; HEAD=1062b621269dac98f618a89f10baa51ff49c8c34
for v in $BASE $HEAD; do
  git -C $R checkout -q --detach $v
  node $W/harness/inroot.js "$DEV" node scripts/typecheck-tests/check.cjs services/auth > $W/logs/ratchet_${v:0:7}.log 2>&1
  echo "ratchet ${v:0:7} rc=$?"; tail -4 $W/logs/ratchet_${v:0:7}.log
done
echo "== ratchet planted (type error in head password.ts)"
printf '\nconst g161Planted: number = "x";\nexport { g161Planted };\n' >> $S/password.ts
node $W/harness/inroot.js "$DEV" node scripts/typecheck-tests/check.cjs services/auth > $W/logs/ratchet_planted.log 2>&1; echo "planted rc=$?"; tail -3 $W/logs/ratchet_planted.log
git -C $R checkout -q -- Blockchain/Dev/services/auth/src/services/password.ts
echo "== tsc service tsconfig head"; $DEV/node_modules/.bin/tsc -p $A/tsconfig.json --noEmit > $W/logs/tsc_svc_head.log 2>&1; echo "rc=$? errors=$(grep -c 'error TS' $W/logs/tsc_svc_head.log)"
echo "== eslint head (4 product + 4 test .ts)"; node $W/harness/eslint_run.js $S/email.ts $S/issuerCertSweep.ts $S/oauthState.ts $S/password.ts $TD/ks1868-email-send-catches-unreadable-throw.test.ts $TD/ks1868-issuer-cert-sweep-body-catches-unreadable-throw.test.ts $TD/ks1868-oauth-state-consume-catch-unreadable-throw.test.ts $TD/ks1868-password-verify-hibp-catches-unreadable-throw.test.ts | tail -6; echo rc=$?
echo "== eslint planted"; printf '\nfunction g161p() { debugger; const unusedG161 = 1; }\nexport { g161p };\n' >> $S/oauthState.ts
node $W/harness/eslint_run.js $S/oauthState.ts | tail -3
git -C $R checkout -q -- Blockchain/Dev/services/auth/src/services/oauthState.ts
echo "== docs-fragments check head"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_head.log 2>&1; echo rc=$?; tail -3 $W/logs/frag_head.log
F="$R/Projects Documents/fragments/flow/KS-1868-auth-credentials.html"
echo "== planted flow unclosed div"; printf '<div>\n' >> "$F"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_planted_flow.log 2>&1; echo rc=$?; tail -2 $W/logs/frag_planted_flow.log
git -C $R checkout -q -- "Projects Documents/fragments/flow/KS-1868-auth-credentials.html"
echo "== after restore"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_after.log 2>&1; echo rc=$?
echo "HEAD=$(git -C $R rev-parse --short HEAD) status=$(git -C $R status --porcelain | wc -l)"
