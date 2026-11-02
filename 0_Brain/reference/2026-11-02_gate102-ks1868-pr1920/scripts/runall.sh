#!/bin/bash
# Base/head measurements. Product file swapped in place, sha256 restored and checked after every run.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920
R=$G/repo
S=$R/Blockchain/Dev/services/analytics
P=$S/src/services/scheduledJobs.ts
REL=Blockchain/Dev/services/analytics/src/services/scheduledJobs.ts
NEW=src/__tests__/ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts
NEWF=$S/$NEW
cp "$P" $G/logs/head_product.ts
HSHA=$(shasum -a 256 "$P" | cut -d' ' -f1)
git -C $R show origin/develop:$REL > $G/logs/base_product.ts
echo "head sha $HSHA; base sha $(shasum -a 256 $G/logs/base_product.ts | cut -d' ' -f1)"
restore() { cp $G/logs/head_product.ts "$P"; [ "$(shasum -a 256 "$P" | cut -d' ' -f1)" = "$HSHA" ] && echo "restore True" || echo "RESTORE FAILED"; }

# 1. red-first: base product, new test only
cp $G/logs/base_product.ts "$P"
bash $G/scripts/vt.sh $G/logs/red_base_new.log $NEW > /dev/null
grep -n "AssertionError\|✓\|×\|FAIL\|Tests " $G/logs/red_base_new.log | head -12
# 2. base whole suite without / with new file
mv "$NEWF" $G/logs/_newtest_held.ts
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log > /dev/null; grep -n "Test Files\|Tests " $G/logs/base_whole_excl_new.log
mv $G/logs/_newtest_held.ts "$NEWF"
bash $G/scripts/vt.sh $G/logs/base_whole_incl_new.log > /dev/null; grep -n "Test Files\|Tests " $G/logs/base_whole_incl_new.log
# 3. probes at base and head
for V in base head; do
  if [ $V = base ]; then cp $G/logs/base_product.ts "$P"; else cp $G/logs/head_product.ts "$P"; fi
  cp "$P" $S/src/services/zz_probe_jobs.ts
  echo "export { dbSaveAlert };" >> $S/src/services/zz_probe_jobs.ts
  sed 's#//.*##' $G/scripts/probe_template.test.ts > /dev/null
  cp $G/scripts/probe_template.test.ts $S/src/__tests__/zz_probe.test.ts
  bash $G/scripts/vt.sh $G/logs/probe_$V.log src/__tests__/zz_probe.test.ts > /dev/null
  grep -h "^PROBE" $G/logs/probe_$V.log | sort > $G/logs/probe_$V.jsonl
  rm -f $S/src/services/zz_probe_jobs.ts $S/src/__tests__/zz_probe.test.ts
done
restore
git -C $R status --short
