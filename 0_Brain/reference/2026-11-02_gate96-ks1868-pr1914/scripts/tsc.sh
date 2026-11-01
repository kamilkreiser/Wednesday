#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate96-ks1868-pr1914
RR=$W/repo; A=$RR/Blockchain/Dev/services/analytics; L=$W/logs
TD=Blockchain/Dev/services/analytics/src/__tests__
pushd $A >/dev/null
cat > tsconfig.gate96.json <<'J'
{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": true, "rootDir": "./src" }, "include": ["src/**/*"], "exclude": ["node_modules","dist"] }
J
echo '--- A: head as pushed (with .js edit)'
npx tsc -p tsconfig.gate96.json > $L/tsc_head.log 2>&1; echo rc=$?; grep -c 'error TS' $L/tsc_head.log; grep 'error TS' $L/tsc_head.log | sed 's/(.*//' | sort | uniq -c
echo '--- B: head with the four tests at canonical bytes (operators generated)'
fn() { case $1 in o60_p1) echo ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts;; *) echo ks1868-analytics-routes-zod-catches-${1#o61_}-unreadable-throw.test.ts;; esac; }
mkdir -p $W/logs/pr_tests
for p in o60_p1 o61_p1 o61_p2 o61_p3; do cp src/__tests__/$(fn $p) $W/logs/pr_tests/$(fn $p); cp $W/logs/q2/$p/section_2.diff.gen src/__tests__/$(fn $p); done
npx tsc -p tsconfig.gate96.json > $L/tsc_canonical.log 2>&1; echo rc=$?; grep -c 'error TS' $L/tsc_canonical.log; grep 'error TS' $L/tsc_canonical.log | sed 's/(.*//;s/.*error/error/' | sort | uniq -c
for p in o60_p1 o61_p1 o61_p2 o61_p3; do cp $W/logs/pr_tests/$(fn $p) src/__tests__/$(fn $p); done
echo '--- C: base (tests absent): product at base, the four test files moved out'
git -C $RR show 03977e89a343:Blockchain/Dev/services/analytics/src/routes/analytics.ts > src/routes/analytics.ts
mkdir -p $W/_quarantine_2026-11-02/tests_for_base
for p in o60_p1 o61_p1 o61_p2 o61_p3; do mv src/__tests__/$(fn $p) $W/_quarantine_2026-11-02/tests_for_base/; done
npx tsc -p tsconfig.gate96.json > $L/tsc_base.log 2>&1; echo rc=$?; grep -c 'error TS' $L/tsc_base.log; grep 'error TS' $L/tsc_base.log
for p in o60_p1 o61_p1 o61_p2 o61_p3; do mv $W/_quarantine_2026-11-02/tests_for_base/$(fn $p) src/__tests__/; done
git -C $RR show refs/qa/pr1914:Blockchain/Dev/services/analytics/src/routes/analytics.ts > src/routes/analytics.ts
echo '--- plain tsc (product only)'
npx tsc --noEmit > $L/tsc_plain_head.log 2>&1; echo rc=$?
git -C $RR status --short | head
