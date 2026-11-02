#!/bin/bash
# base suite (base product, new tests absent) and red-first (new tests at base product); restores head and checks sha + git status.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930
A=$G/repo/Blockchain/Dev/services/security/src; L=$G/logs
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW=$(cd $A/__tests__ && ls | grep -E '^ks1868-security-(admin-scopes-get|audit-and-event|db-probe|save-api-key|validate-route)')
echo "new tests: $NEW"
mkdir -p $L/newtests_hold
cp $L/index_base.ts $A/index.ts; cp $L/db_base.ts $A/db.ts
echo "base product: $(sha $A/index.ts) $(sha $A/db.ts)"
bash $G/scripts/vt.sh $L/red_base.log --reporter=json --outputFile=$L/red_base.json $(for f in $NEW; do echo src/__tests__/$f; done); echo "red-first rc=$?"
for f in $NEW; do mv $A/__tests__/$f $L/newtests_hold/; done
bash $G/scripts/vt.sh $L/suite_base.log --reporter=json --outputFile=$L/suite_base.json; echo "base suite rc=$?"
for f in $NEW; do mv $L/newtests_hold/$f $A/__tests__/; done
cp $L/index_head.ts $A/index.ts; cp $L/db_head.ts $A/db.ts
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930/repo status --short > $L/status_after_base_runs.log; echo "git status lines: $(wc -l < $L/status_after_base_runs.log)"
echo "restored: $(sha $A/index.ts) $(sha $A/db.ts)"
