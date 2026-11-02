#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920
S=$G/repo/Blockchain/Dev/services/analytics
P=$S/src/services/scheduledJobs.ts
HSHA=$(shasum -a 256 $G/logs/head_product.ts | cut -d' ' -f1)
mkdir -p $G/_quarantine
for V in base head; do
  [ -e $G/logs/probe_$V.jsonl ] && mv $G/logs/probe_$V.jsonl $G/_quarantine/probe_$V.$(date +%s).jsonl
  cp $G/logs/${V}_product.ts "$P"
  cp "$P" $S/src/services/zz_probe_jobs.ts
  echo "export { dbSaveAlert };" >> $S/src/services/zz_probe_jobs.ts
  cp $G/scripts/probe_template.test.ts $S/src/__tests__/zz_probe.test.ts
  PROBE_OUT=$G/logs/probe_$V.jsonl bash $G/scripts/vt.sh $G/logs/probe_$V.log src/__tests__/zz_probe.test.ts | tail -4
  mv $S/src/services/zz_probe_jobs.ts $G/_quarantine/zz_probe_jobs.$V.ts
  mv $S/src/__tests__/zz_probe.test.ts $G/_quarantine/zz_probe.$V.test.ts
  sort -o $G/logs/probe_$V.jsonl $G/logs/probe_$V.jsonl
done
cp $G/logs/head_product.ts "$P"
[ "$(shasum -a 256 "$P" | cut -d' ' -f1)" = "$HSHA" ] && echo "restore True" || echo "RESTORE FAILED"
git -C $G/repo status --short
