#!/bin/bash
# G161: red-first, new tests at head, full auth vitest suite at head and base. Every runner anchored in the clone.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate161-ks1868-pr1978
R=$W/repo; A=$R/Blockchain/Dev/services/auth
BASE=66cbe4e52d5afadc9d13ca141200026cc68d5095; HEAD=1062b621269dac98f618a89f10baa51ff49c8c34
P=Blockchain/Dev/services/auth/src/services
T="src/__tests__/ks1868-email-send-catches-unreadable-throw.test.ts src/__tests__/ks1868-issuer-cert-sweep-body-catches-unreadable-throw.test.ts src/__tests__/ks1868-oauth-state-consume-catch-unreadable-throw.test.ts src/__tests__/ks1868-password-verify-hibp-catches-unreadable-throw.test.ts"
run() { local n=$1; shift
  nice -n 5 node $W/harness/vt.js "$W/logs/vt_$n.json" "$@"; local rc=$?
  node -e 'const r=require(process.argv[1]);console.log(process.argv[2],"rc="+process.argv[3],"files="+r.testResults.length,"tests="+r.numTotalTests,"pass="+r.numPassedTests,"fail="+r.numFailedTests,"pending="+r.numPendingTests+"/todo="+r.numTodoTests);const per={};for(const f of r.testResults){const k=f.name.split("/").pop();for(const t of f.assertionResults){per[k]=per[k]||{p:0,f:0,assert:0};if(t.status==="passed")per[k].p++;if(t.status==="failed"){per[k].f++;const m=(t.failureMessages[0]||"");if(/AssertionError/.test(m))per[k].assert++;console.log("  FAIL",k,"::",t.title.slice(0,90),"::",m.split("\n")[0].slice(0,140))}}}if(Object.keys(per).length<=6)console.log(JSON.stringify(per))' "$W/logs/vt_$n.json" "$n" "$rc"
}
git -C $R checkout -q --detach $HEAD
case "${1:-all}" in
  red)
    for f in email.ts issuerCertSweep.ts oauthState.ts password.ts; do git -C $R show $BASE:$P/$f > $A/src/services/$f; done
    echo "swapped in base: $(for f in email.ts issuerCertSweep.ts oauthState.ts password.ts; do echo -n "$f=$(git -C $R hash-object $A/src/services/$f | cut -c1-10) "; done)"
    run redfirst $T
    git -C $R checkout -q -- $P/email.ts $P/issuerCertSweep.ts $P/oauthState.ts $P/password.ts
    echo "restored status=$(git -C $R status --porcelain | wc -l)"
    run head_new $T ;;
  full)
    run head_full
    git -C $R checkout -q --detach $BASE
    run base_full
    git -C $R checkout -q --detach $HEAD
    echo "back at $(git -C $R rev-parse --short HEAD) status=$(git -C $R status --porcelain | wc -l)" ;;
esac
