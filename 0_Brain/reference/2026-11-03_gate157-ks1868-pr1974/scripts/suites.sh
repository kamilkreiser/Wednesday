#!/bin/bash
# G157: billing vitest at head (full + new), red-first (base db.ts + new test), base full. Restores head by sha after.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate157-ks1868-pr1974
R=$W/repo
B=$R/Blockchain/Dev/services/billing
V=$R/Blockchain/Dev/node_modules/.bin/vitest
T=src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts
run() { # name, extra args
  local name=$1; shift
  "$V" run --root "$B" --reporter=json --outputFile="$W/logs/vitest_$name.json" "$@" > "$W/logs/vitest_$name.log" 2>&1
  local rc=$?
  node -e 'const j=require(process.argv[1]);console.log(process.argv[2],"rc="+process.argv[3],"files",j.numPassedTestSuites+"/"+j.numTotalTestSuites,"tests pass",j.numPassedTests,"fail",j.numFailedTests,"total",j.numTotalTests);for(const s of j.testResults)for(const a of s.assertionResults)if(a.status!=="passed")console.log("  FAIL",a.title.slice(0,60),"|",(a.failureMessages[0]||"").split("\n").slice(0,1).join(" ").slice(0,170))' "$W/logs/vitest_$name.json" "$name" "$rc"
}
git -C $R checkout -q --detach 35f1842fa7dee22125ce5fa3ba0dafcc5e32d713
run head_full
run head_new "$T"
git -C $R show 7ad0dcc14e5c:Blockchain/Dev/services/billing/src/db.ts > $B/src/db.ts
echo "db.ts blob now: $(git -C $R hash-object $B/src/db.ts) (base 0f15dc241 expected)"
run redfirst_new "$T"
git -C $R checkout -q -- Blockchain/Dev/services/billing/src/db.ts
git -C $R checkout -q --detach 7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6
run base_full
git -C $R checkout -q --detach 35f1842fa7dee22125ce5fa3ba0dafcc5e32d713
echo "restored HEAD $(git -C $R rev-parse HEAD) db.ts $(git -C $R hash-object $B/src/db.ts); status: $(git -C $R status --porcelain | wc -l) changed"
