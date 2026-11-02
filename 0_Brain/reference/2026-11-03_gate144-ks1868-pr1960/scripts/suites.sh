#!/bin/bash
# api-gateway: new file at head; head whole; base product + new file (red first); base + new whole; base without new (whole). sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
R=$W/repo; D=$R/Blockchain/Dev; V=$D/node_modules/.bin/vitest; A=$D/services/api-gateway
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g144; mkdir -p $SC
export TMPDIR=$SC
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 $V run --root $A --maxWorkers=4 "$@" > $log 2>&1; echo "rc=$?" >> $log; }
P=$A/src/services/redis.ts; REL=Blockchain/Dev/services/api-gateway/src/services/redis.ts
TB=ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts; T=$A/src/__tests__/$TB
H=$(sha $P)
vt $W/logs/head_new.log src/__tests__/$TB
vt $W/logs/head_whole.log
git -C $R show 2d3b3bb3:$REL > $SC/base_redis.ts
cp $SC/base_redis.ts $P
vt $W/logs/red_base_new.log src/__tests__/$TB
vt $W/logs/base_plus_new_whole.log
mv $T $SC/$TB
vt $W/logs/base_whole_excl_new.log
mv $SC/$TB $T
git -C $R show pr1960:$REL > $P
[ "$(sha $P)" = "$H" ] && echo "restore OK" > $W/logs/suites_restore.log || echo "RESTORE FAIL" > $W/logs/suites_restore.log
git -C $R status --short >> $W/logs/suites_restore.log
echo done > $W/logs/suites.done
