#!/bin/bash
# Gate 170 suites: head whole x2; the 7 changed test files at head; red-first = head's tests on r1 product and on dev product. sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985
R=$W/repo; D=$R/Blockchain/Dev; V=$D/node_modules/.bin/vitest; A=$D/services/api-gateway; L=$W/logs
export HOME=$W/home TMPDIR=$W/tmp
[ "$(git -C $R rev-parse HEAD)" = a0a91f65d0006d1adc69325002e6ddf69abffc2b ] || { echo "tree not at head"; exit 1; }
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 $V run --root $A --maxWorkers=3 --reporter=json --outputFile=$log.json "$@" > $log 2>&1; echo "rc=$?" >> $log; }
P=Blockchain/Dev/services/api-gateway/src
CT="auth.test.ts ks1868-brute-force-redis-catch-unreadable-throw.test.ts ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts ks1961-brute-force-guard-fails-closed.test.ts ks1961-rate-limit-header-step-fails-closed.test.ts ks480-connector-auth.test.ts security.test.ts"
: > $L/suites_sha.log; for f in security rateLimitEnforce; do echo "$f $(sha $A/src/middleware/$f.ts)" >> $L/suites_sha.log; done
vt $L/head_whole1.log
vt $L/head_whole2.log
vt $L/head_changed.log $(for t in $CT; do echo src/__tests__/$t; done)
for base in r1:1e8c43fcaf6c9c6d42946b43c89e419f9d1f3f18 dev:ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8; do
  n=${base%%:*}; c=${base#*:}
  for f in security rateLimitEnforce; do git -C $R show $c:$P/middleware/$f.ts > $A/src/middleware/$f.ts; done
  for t in $CT; do vt $L/red_${n}_$t.log src/__tests__/$t; done
done
for f in security rateLimitEnforce; do git -C $R show a0a91f65d0006d1adc69325002e6ddf69abffc2b:$P/middleware/$f.ts > $A/src/middleware/$f.ts; done
: > $L/suites_restore.log; while read f h; do [ "$(sha $A/src/middleware/$f.ts)" = "$h" ] && echo "$f restore OK" >> $L/suites_restore.log || echo "$f RESTORE FAIL" >> $L/suites_restore.log; done < $L/suites_sha.log
git -C $R status --short >> $L/suites_restore.log
echo done > $L/suites.done
