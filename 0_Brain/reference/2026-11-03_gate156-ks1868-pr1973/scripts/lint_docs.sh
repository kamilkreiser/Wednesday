#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate156-ks1868-pr1973; R=$W/repo; G=$R/Blockchain/Dev/services/governance
T=$G/src/__tests__/ks1868-governance-db-pool-error-and-ready-hook-unreadable-throw.test.ts
echo "== eslint head"; node $W/harness/eslint_run.js $G/src/db.ts $T; echo rc=$?
echo "== eslint planted (debugger + unused const in db.ts)"
printf '\nfunction g156p() { debugger; const unusedG156 = 1; }\nexport { g156p };\n' >> $G/src/db.ts
node $W/harness/eslint_run.js $G/src/db.ts; echo rc=$?
git -C $R checkout -q -- Blockchain/Dev/services/governance/src/db.ts
echo "== eslint base db.ts"; git -C $R show 7ad0dcc14e5c:Blockchain/Dev/services/governance/src/db.ts > $G/src/db.ts; node $W/harness/eslint_run.js $G/src/db.ts; echo rc=$?
git -C $R checkout -q -- Blockchain/Dev/services/governance/src/db.ts
echo "== docs-fragments check"; node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_head.log 2>&1; echo rc=$?; tail -3 $W/logs/frag_head.log
F="$R/Projects Documents/fragments/flow/KS-1868-governance-db-pool.html"; C="$R/Projects Documents/fragments/cheat/KS-1868-governance-db-pool.html"
echo "== planted flow unclosed div"; printf '<div>\n' >> "$F"; node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_planted_flow.log 2>&1; echo rc=$?; tail -2 $W/logs/frag_planted_flow.log; git -C $R checkout -q -- "Projects Documents/fragments/flow/KS-1868-governance-db-pool.html"
echo "== planted cheat unclosed div"; printf '<div>\n' >> "$C"; node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_planted_cheat.log 2>&1; echo rc=$?; tail -2 $W/logs/frag_planted_cheat.log; git -C $R checkout -q -- "Projects Documents/fragments/cheat/KS-1868-governance-db-pool.html"
echo "== after restore"; node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $R > $W/logs/frag_after.log 2>&1; echo rc=$?
echo "status=$(git -C $R status --porcelain | wc -l) HEAD=$(git -C $R rev-parse --short HEAD)"
