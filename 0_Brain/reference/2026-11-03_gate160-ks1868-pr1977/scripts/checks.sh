#!/bin/bash
# G160: tsc test-types ratchet (auth) base/head + planted; eslint changed .ts + planted; docs-fragments check + planted.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977
R=$W/repo; DEV=$R/Blockchain/Dev; A=$DEV/services/auth
BASE=f7b4a7173010a407864ecb7ab92814824f9cb4b6; HEAD=ccbca31cfa49b7d1b222a62853924764ab998990
T1=$A/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts
T2=$A/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts
for v in $BASE $HEAD; do
  git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q --detach $v
  node $W/harness/inroot.js "$DEV" node scripts/typecheck-tests/check.cjs services/auth > $W/logs/ratchet_${v:0:7}.log 2>&1
  echo "ratchet ${v:0:7} rc=$?"; tail -4 $W/logs/ratchet_${v:0:7}.log
done
echo "== ratchet planted (type error in head session.ts)"
printf '\nconst g160Planted: number = "x";\nexport { g160Planted };\n' >> $A/src/services/session.ts
node $W/harness/inroot.js "$DEV" node scripts/typecheck-tests/check.cjs services/auth > $W/logs/ratchet_planted.log 2>&1; echo "planted rc=$?"; tail -3 $W/logs/ratchet_planted.log
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q -- Blockchain/Dev/services/auth/src/services/session.ts
echo "== tsc service tsconfig head"; $DEV/node_modules/.bin/tsc -p $A/tsconfig.json --noEmit > $W/logs/tsc_svc_head.log 2>&1; echo "rc=$? errors=$(grep -c 'error TS' $W/logs/tsc_svc_head.log)"
echo "== eslint head (4 changed .ts)"; node $W/harness/eslint_run.js $A/src/db.ts $A/src/services/session.ts $T1 $T2; echo rc=$?
echo "== eslint planted"; printf '\nfunction g160p() { debugger; const unusedG160 = 1; }\nexport { g160p };\n' >> $A/src/db.ts
node $W/harness/eslint_run.js $A/src/db.ts; echo rc=$?
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q -- Blockchain/Dev/services/auth/src/db.ts
echo "== eslint base product files"
git -C $R show $BASE:Blockchain/Dev/services/auth/src/db.ts > $A/src/db.ts; git -C $R show $BASE:Blockchain/Dev/services/auth/src/services/session.ts > $A/src/services/session.ts
node $W/harness/eslint_run.js $A/src/db.ts $A/src/services/session.ts; echo rc=$?
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q -- Blockchain/Dev/services/auth/src/db.ts Blockchain/Dev/services/auth/src/services/session.ts
echo "== docs-fragments check head"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_head.log 2>&1; echo rc=$?; tail -3 $W/logs/frag_head.log
F="$R/Projects Documents/fragments/flow/KS-1868-auth-session-db.html"; C="$R/Projects Documents/fragments/cheat/KS-1868-auth-session-db.html"
echo "== planted flow unclosed div"; printf '<div>\n' >> "$F"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_planted_flow.log 2>&1; echo rc=$?; tail -2 $W/logs/frag_planted_flow.log
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q -- "Projects Documents/fragments/flow/KS-1868-auth-session-db.html"
echo "== planted cheat unclosed div"; printf '<div>\n' >> "$C"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_planted_cheat.log 2>&1; echo rc=$?; tail -2 $W/logs/frag_planted_cheat.log
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q -- "Projects Documents/fragments/cheat/KS-1868-auth-session-db.html"
echo "== after restore"; node $DEV/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_after.log 2>&1; echo rc=$?
echo "HEAD=$(git -C $R rev-parse --short HEAD) status=$(git -C $R status --porcelain | wc -l) db=$(git -C $R hash-object $A/src/db.ts) session=$(git -C $R hash-object $A/src/services/session.ts)"
