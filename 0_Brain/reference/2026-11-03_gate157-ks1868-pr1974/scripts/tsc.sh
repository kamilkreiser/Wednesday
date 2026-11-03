#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate157-ks1868-pr1974; R=$W/repo; B=$R/Blockchain/Dev/services/billing; TSC=$R/Blockchain/Dev/node_modules/.bin/tsc
for v in 7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6 35f1842fa7dee22125ce5fa3ba0dafcc5e32d713; do
  git -C $R checkout -q --detach $v
  "$TSC" -p "$B/tsconfig.json" --noEmit > $W/logs/tsc_svc_${v:0:7}.log 2>&1; a=$?
  "$TSC" -p "$W/harness/tsconfig.tests.json" > $W/logs/tsc_tests_${v:0:7}.log 2>&1; b=$?
  "$TSC" -p "$W/harness/tsconfig.tests.json" --listFilesOnly 2>/dev/null | grep -c __tests__ > $W/logs/tsc_tests_count_${v:0:7}.txt
  grep 'error TS' $W/logs/tsc_tests_${v:0:7}.log | sed -E 's/\([0-9]+,[0-9]+\)//' | sed "s#$R/##" | sort > $W/logs/tsc_tests_set_${v:0:7}.txt
  echo "${v:0:7} tsc service rc=$a errors=$(grep -c 'error TS' $W/logs/tsc_svc_${v:0:7}.log) | tests-included rc=$b errors=$(grep -c 'error TS' $W/logs/tsc_tests_${v:0:7}.log) test files=$(cat $W/logs/tsc_tests_count_${v:0:7}.txt) in db.ts/new test: $(grep -cE 'src/db.ts|ks1868-billing-db' $W/logs/tsc_tests_${v:0:7}.log)"
done
echo "error set base vs head (location-stripped) diff lines: $(diff $W/logs/tsc_tests_set_7ad0dcc.txt $W/logs/tsc_tests_set_35f1842.txt | wc -l)"
cut -d: -f1 $W/logs/tsc_tests_set_35f1842.txt | sort | uniq -c
printf '\nconst g157Planted: number = "x";\nexport { g157Planted };\n' >> $B/src/db.ts
"$TSC" -p "$B/tsconfig.json" --noEmit > $W/logs/tsc_planted_svc.log 2>&1; echo "planted service rc=$? $(grep -c 'error TS' $W/logs/tsc_planted_svc.log) err"
"$TSC" -p "$W/harness/tsconfig.tests.json" > $W/logs/tsc_planted_tests.log 2>&1; echo "planted tests-included rc=$? $(grep -c 'error TS' $W/logs/tsc_planted_tests.log) err"
git -C $R checkout -q -- Blockchain/Dev/services/billing/src/db.ts
echo "restored HEAD $(git -C $R rev-parse --short HEAD) db.ts blob $(git -C $R hash-object $B/src/db.ts) status=$(git -C $R status --porcelain | wc -l)"
