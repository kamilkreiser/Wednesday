#!/bin/bash
# G160: red-first, new tests at head, full auth vitest suite at base and head. Every runner anchored in the clone.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977
R=$W/repo; A=$R/Blockchain/Dev/services/auth; VT=$R/Blockchain/Dev/node_modules/.bin/vitest
BASE=f7b4a7173010a407864ecb7ab92814824f9cb4b6; HEAD=ccbca31cfa49b7d1b222a62853924764ab998990
T1=src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts
T2=src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts
run() { # name, args...
  local n=$1; shift
  node $W/harness/vt.js "$W/logs/vt_$n.json" "$@"; local rc=$?
  node -e 'const r=require(process.argv[1]);console.log(process.argv[2],"rc="+process.argv[3],"files="+r.numTotalTestSuites+"/"+r.testResults.length,"tests="+r.numTotalTests,"pass="+r.numPassedTests,"fail="+r.numFailedTests,"pending="+r.numPendingTests+"/todo="+r.numTodoTests);for(const f of r.testResults)for(const t of f.assertionResults)if(t.status==="failed")console.log("  FAIL",f.name.split("/").pop(),"::",t.title.slice(0,90),"::",(t.failureMessages[0]||"").split("\n")[0].slice(0,140))' "$W/logs/vt_$n.json" "$n" "$rc"
}
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q --detach $HEAD
case "${1:-all}" in
  red)
    git -C $R show $BASE:Blockchain/Dev/services/auth/src/db.ts > $A/src/db.ts
    git -C $R show $BASE:Blockchain/Dev/services/auth/src/services/session.ts > $A/src/services/session.ts
    echo "swapped in base: db $(git -C $R hash-object $A/src/db.ts) session $(git -C $R hash-object $A/src/services/session.ts)"
    run redfirst_T1 $T1; run redfirst_T2 $T2
    git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q -- Blockchain/Dev/services/auth/src/db.ts Blockchain/Dev/services/auth/src/services/session.ts
    echo "restored: db $(git -C $R hash-object $A/src/db.ts) session $(git -C $R hash-object $A/src/services/session.ts) status=$(git -C $R status --porcelain | wc -l)"
    run head_new $T1 $T2 ;;
  full)
    run head_full
    git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q --detach $BASE
    run base_full
    git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo checkout -q --detach $HEAD
    echo "back at $(git -C $R rev-parse --short HEAD) status=$(git -C $R status --porcelain | wc -l)" ;;
esac
