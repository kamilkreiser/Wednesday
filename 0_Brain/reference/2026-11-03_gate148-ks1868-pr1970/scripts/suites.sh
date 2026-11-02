#!/bin/bash
# api-gateway: new files at head; head whole; base product + new files (red first); base whole without new files. sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970
R=$W/repo; D=$R/Blockchain/Dev; V=$D/node_modules/.bin/vitest; A=$D/services/api-gateway
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g148; mkdir -p $SC
export TMPDIR=$SC
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 $V run --root $A --maxWorkers=3 "$@" > $log 2>&1; echo "rc=$?" >> $log; }
NEW="ks1868-audit-write-failed-catch-unreadable-throw.test.ts ks1868-brute-force-redis-catch-unreadable-throw.test.ts ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts"
NEWP=""; for t in $NEW; do NEWP="$NEWP src/__tests__/$t"; done
PROD="security rateLimitEnforce audit"
: > $W/logs/suites_sha.log; for f in $PROD; do echo "$f $(sha $A/src/middleware/$f.ts)" >> $W/logs/suites_sha.log; done
vt $W/logs/head_new.log $NEWP
vt $W/logs/head_whole.log
for f in $PROD; do git -C $R show 4d1ab2cb:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $A/src/middleware/$f.ts; done
for t in $NEW; do vt $W/logs/red_base_$t.log src/__tests__/$t; done
mkdir -p $SC/held; for t in $NEW; do mv $A/src/__tests__/$t $SC/held/$t; done
vt $W/logs/base_whole_excl_new.log
for t in $NEW; do mv $SC/held/$t $A/src/__tests__/$t; done
for f in $PROD; do git -C $R show pr1970:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $A/src/middleware/$f.ts; done
: > $W/logs/suites_restore.log; while read f h; do [ "$(sha $A/src/middleware/$f.ts)" = "$h" ] && echo "$f restore OK" >> $W/logs/suites_restore.log || echo "$f RESTORE FAIL" >> $W/logs/suites_restore.log; done < $W/logs/suites_sha.log
git -C $R status --short >> $W/logs/suites_restore.log
echo done > $W/logs/suites.done
