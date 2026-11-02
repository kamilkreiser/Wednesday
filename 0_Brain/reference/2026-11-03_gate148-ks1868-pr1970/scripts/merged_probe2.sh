#!/bin/bash
# Attempt 2 of the merged-overlay probe cells (attempt 1 died: tsx IPC pipe path too long under the scratchpad TMPDIR, EINVAL). Default TMPDIR, like probe_matrix.sh.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/api-gateway; T=$D/node_modules/.bin/tsx
DEV=4deb2fc10b7d852194183c08e86e2ecacb7231db
RP=src/services/redis.ts
H0=$(shasum -a 256 $A/$RP | awk '{print $1}')
git -C $R show $DEV:Blockchain/Dev/services/api-gateway/$RP > $A/$RP
echo "overlay redis.ts == develop: $([ "$(git -C $R hash-object $A/$RP)" = "$(git -C $R rev-parse $DEV:Blockchain/Dev/services/api-gateway/$RP)" ] && echo yes || echo NO)"
OUT=$W/logs/probe_merged.jsonl; : > $OUT; : > $W/logs/probe_merged.rc; : > $W/logs/probe_merged.err
for cell in bf rl_hdr rl_redis audit; do for v in ordinary revokedProxy getterThrows; do
  $T $W/scripts/probe_child.ts head $cell $v >> $OUT 2>>$W/logs/probe_merged.err; echo "rc=$? merged $cell $v" >> $W/logs/probe_merged.rc
done; done
$T $W/scripts/probe_child.ts head bf_arm none >> $OUT 2>>$W/logs/probe_merged.err; echo "rc=$? merged bf_arm none" >> $W/logs/probe_merged.rc
git -C $R show pr1970:Blockchain/Dev/services/api-gateway/$RP > $A/$RP
echo "restore redis.ts: $([ "$(shasum -a 256 $A/$RP | awk '{print $1}')" = "$H0" ] && echo OK || echo FAIL)"
echo "status lines: $(git -C $R status --short | wc -l)"
