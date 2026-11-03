#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate156-ks1868-pr1973; R=$W/repo; G=$R/Blockchain/Dev/services/governance; TSC=$R/Blockchain/Dev/node_modules/.bin/tsc
for v in 7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6 e16104beec024d4aa2fdf78ab2d1f92631272e2f; do
  git -C $R checkout -q --detach $v
  "$TSC" -p "$G/tsconfig.json" --noEmit > $W/logs/tsc_svc_${v:0:7}.log 2>&1; a=$?
  "$TSC" -p "$W/harness/tsconfig.tests.json" > $W/logs/tsc_tests_${v:0:7}.log 2>&1; b=$?
  "$TSC" -p "$W/harness/tsconfig.tests.json" --listFilesOnly 2>/dev/null | grep -c __tests__ > $W/logs/tsc_tests_count_${v:0:7}.txt
  echo "${v:0:7} tsc service rc=$a errors=$(grep -c 'error TS' $W/logs/tsc_svc_${v:0:7}.log) | tests-included rc=$b errors=$(grep -c 'error TS' $W/logs/tsc_tests_${v:0:7}.log) test files compiled=$(cat $W/logs/tsc_tests_count_${v:0:7}.txt)"
done
# positive control: planted type error in head db.ts must be caught by both
printf '\nconst g156Planted: number = "x";\nexport { g156Planted };\n' >> $G/src/db.ts
"$TSC" -p "$G/tsconfig.json" --noEmit > $W/logs/tsc_planted_svc.log 2>&1; echo "planted service rc=$? $(grep -c 'error TS' $W/logs/tsc_planted_svc.log) err"
"$TSC" -p "$W/harness/tsconfig.tests.json" > $W/logs/tsc_planted_tests.log 2>&1; echo "planted tests-included rc=$? $(grep -c 'error TS' $W/logs/tsc_planted_tests.log) err"
git -C $R checkout -q -- Blockchain/Dev/services/governance/src/db.ts
echo "restored HEAD $(git -C $R rev-parse --short HEAD) db.ts blob $(git -C $R hash-object $G/src/db.ts) status=$(git -C $R status --porcelain | wc -l)"
