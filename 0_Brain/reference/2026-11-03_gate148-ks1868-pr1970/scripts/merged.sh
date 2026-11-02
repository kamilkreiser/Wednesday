#!/bin/bash
# Resumed gate 148: overlay develop 4deb2fc1's two api-gateway paths onto the head checkout (= merged tree for api-gateway, since
# merge-tree showed merged blobs == head on all PR paths and develop touched only these two api-gateway paths), run the whole
# api-gateway suite + the probe cells that answer the fail-open question, then restore by sha.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/api-gateway; V=$D/node_modules/.bin/vitest; T=$D/node_modules/.bin/tsx
DEV=4deb2fc10b7d852194183c08e86e2ecacb7231db
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/eec7efc2-5c14-4e14-ad4f-4325692f2476/scratchpad/g148r; mkdir -p $TMPDIR
RP=src/services/redis.ts; NT=src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts
H0=$(shasum -a 256 $A/$RP | awk '{print $1}')
test -e $A/$NT && { echo "new test already present, abort"; exit 1; }
git -C $R show $DEV:Blockchain/Dev/services/api-gateway/$RP > $A/$RP
git -C $R show $DEV:Blockchain/Dev/services/api-gateway/$NT > $A/$NT
echo "overlay redis.ts == develop: $([ "$(git -C $R hash-object $A/$RP)" = "$(git -C $R rev-parse $DEV:Blockchain/Dev/services/api-gateway/$RP)" ] && echo yes || echo NO)"
nice -n 10 $V run --root $A --maxWorkers=3 > $W/logs/merged_whole.log 2>&1; echo "rc=$?" >> $W/logs/merged_whole.log
OUT=$W/logs/probe_merged.jsonl; : > $OUT
for cell in bf rl_hdr rl_redis audit; do for v in ordinary revokedProxy getterThrows; do
  $T $W/scripts/probe_child.ts head $cell $v >> $OUT 2>>$W/logs/probe_merged.err; echo "rc=$? merged $cell $v" >> $W/logs/probe_merged.rc
done; done
$T $W/scripts/probe_child.ts head bf_arm none >> $OUT 2>>$W/logs/probe_merged.err; echo "rc=$? merged bf_arm none" >> $W/logs/probe_merged.rc
mkdir -p $W/logs/_quarantine/merged; mv $A/$NT $W/logs/_quarantine/merged/
git -C $R show pr1970:Blockchain/Dev/services/api-gateway/$RP > $A/$RP
echo "restore redis.ts: $([ "$(shasum -a 256 $A/$RP | awk '{print $1}')" = "$H0" ] && echo OK || echo FAIL)"
git -C $R status --short; echo "status lines: $(git -C $R status --short | wc -l)"
echo done > $W/logs/merged.done
