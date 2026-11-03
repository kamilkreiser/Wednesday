#!/bin/bash
# G164: red-first, new tests at head, full security vitest suite at head and base. Every runner anchored in the clone.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate164-ks1868-pr1981
R=$W/repo; S=$R/Blockchain/Dev/services/security
BASE=0a6575f7fd92d60849d1186efa0632961db21be5; HEAD=2e0f5ec046d640c1f83dcf248f15e4d570340959
P=Blockchain/Dev/services/security/src/index.ts
T=src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts
run() { local n=$1; shift
  nice -n 5 node $W/harness/vt.js "$W/logs/vt_$n.json" "$@"; local rc=$?
  node -e 'const r=require(process.argv[1]);console.log(process.argv[2],"rc="+process.argv[3],"files="+r.testResults.length,"tests="+r.numTotalTests,"pass="+r.numPassedTests,"fail="+r.numFailedTests,"pending="+r.numPendingTests+"/todo="+r.numTodoTests);for(const f of r.testResults){const k=f.name.split("/").pop();for(const t of f.assertionResults){if(t.status==="failed"){const m=(t.failureMessages[0]||"");console.log("  FAIL",k,"::",t.title.slice(0,100),"::",/AssertionError/.test(m)?"AssertionError":"OTHER",m.split("\n")[0].slice(0,120))}}}' "$W/logs/vt_$n.json" "$n" "$rc"
}
git -C $R checkout -q --detach $HEAD
case "${1:-all}" in
  red)
    git -C $R show $BASE:$P > $S/src/index.ts; echo "swapped base index.ts blob=$(git -C $R hash-object $S/src/index.ts)"
    run redfirst $T
    git -C $R checkout -q -- $P; echo "restored blob=$(git -C $R hash-object $S/src/index.ts) status=$(git -C $R status --porcelain | wc -l)"
    run head_new $T ;;
  full)
    run head_full
    git -C $R checkout -q --detach $BASE
    run base_full
    git -C $R checkout -q --detach $HEAD
    echo "back at $(git -C $R rev-parse --short HEAD) status=$(git -C $R status --porcelain | wc -l)" ;;
esac
