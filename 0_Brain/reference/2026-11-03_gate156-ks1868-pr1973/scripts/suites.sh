#!/bin/bash
# G156: governance jest at head, red-first (base db.ts + new test), base (no new test). Restores head by sha after.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate156-ks1868-pr1973
R=$W/repo
G=$R/Blockchain/Dev/services/governance
J=$R/Blockchain/Dev/node_modules/.bin/jest
T=src/__tests__/ks1868-governance-db-pool-error-and-ready-hook-unreadable-throw.test.ts
run() { # name, extra args
  local name=$1; shift
  "$J" --config "$G/jest.config.js" --rootDir "$G" --ci --json --outputFile "$W/logs/jest_$name.json" "$@" > "$W/logs/jest_$name.log" 2>&1
  local rc=$?
  node -e 'const j=require(process.argv[1]);console.log(process.argv[2],"rc="+process.argv[3],"suites",j.numPassedTestSuites+"/"+j.numTotalTestSuites,"tests pass",j.numPassedTests,"fail",j.numFailedTests,"total",j.numTotalTests);for(const s of j.testResults)for(const a of s.assertionResults)if(a.status!=="passed")console.log("  FAIL",a.title.slice(0,70),"|",(a.failureMessages[0]||"").split("\n").slice(0,2).join(" ").slice(0,160))' "$W/logs/jest_$name.json" "$name" "$rc"
}
git -C $R checkout -q --detach e16104beec024d4aa2fdf78ab2d1f92631272e2f
run head_full
run head_new "$G/$T"
# red first: base db.ts, head test
git -C $R show 7ad0dcc14e5c:Blockchain/Dev/services/governance/src/db.ts > $G/src/db.ts
echo "db.ts blob now: $(git -C $R hash-object $G/src/db.ts) (base 75d140b0b expected)"
run redfirst_new "$G/$T"
git -C $R checkout -q -- Blockchain/Dev/services/governance/src/db.ts
# base full (no new test)
git -C $R checkout -q --detach 7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6
run base_full
git -C $R checkout -q --detach e16104beec024d4aa2fdf78ab2d1f92631272e2f
echo "restored HEAD $(git -C $R rev-parse HEAD); status: $(git -C $R status --porcelain | wc -l) changed"
