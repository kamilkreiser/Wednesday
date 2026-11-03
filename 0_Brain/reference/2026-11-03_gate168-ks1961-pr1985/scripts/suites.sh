#!/bin/bash
# Gate 168 suites: head whole x2; red-first (base product + head's changed tests); base whole x2 (develop tree). sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate168-ks1961-pr1985
R=$W/repo; D=$R/Blockchain/Dev; V=$D/node_modules/.bin/vitest; A=$D/services/api-gateway; L=$W/logs
export HOME=$W/home TMPDIR=$W/tmp
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 $V run --root $A --maxWorkers=3 --reporter=json --outputFile=$log.json "$@" > $log 2>&1; echo "rc=$?" >> $log; }
P=Blockchain/Dev/services/api-gateway/src
CHANGED_TESTS="auth.test.ts ks1868-brute-force-redis-catch-unreadable-throw.test.ts ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts ks1961-brute-force-guard-fails-closed.test.ts ks1961-rate-limit-header-step-fails-closed.test.ts ks480-connector-auth.test.ts security.test.ts"
git -C $R rev-parse HEAD > $L/suites_head_rev.log
: > $L/suites_sha.log; for f in security rateLimitEnforce; do echo "$f $(sha $A/src/middleware/$f.ts)" >> $L/suites_sha.log; done
vt $L/head_whole1.log
vt $L/head_whole2.log
# red first: base product, head tests
for f in security rateLimitEnforce; do git -C $R show gh/develop:$P/middleware/$f.ts > $A/src/middleware/$f.ts; done
for t in $CHANGED_TESTS; do vt $L/red_base_$t.log src/__tests__/$t; done
for f in security rateLimitEnforce; do git -C $R show pr/1985:$P/middleware/$f.ts > $A/src/middleware/$f.ts; done
: > $L/suites_restore.log; while read f h; do [ "$(sha $A/src/middleware/$f.ts)" = "$h" ] && echo "$f restore OK" >> $L/suites_restore.log || echo "$f RESTORE FAIL" >> $L/suites_restore.log; done < $L/suites_sha.log
# base whole: the develop tree
git -C $R checkout -q --detach gh/develop && git -C $R rev-parse HEAD > $L/suites_base_rev.log
vt $L/base_whole1.log
vt $L/base_whole2.log
git -C $R checkout -q gate168 && git -C $R rev-parse HEAD >> $L/suites_restore.log
git -C $R status --short >> $L/suites_restore.log
echo done > $L/suites.done
