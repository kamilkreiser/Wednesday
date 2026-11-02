#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942
R=$W/repo; A=$R/Blockchain/Dev/services/originate; L=$W/logs; J=$W/scripts/jest.sh
F=src/routes/certifications.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
NEW="ks1868-certifications-issue-anchoring-catch-o79p2 ks1868-certifications-issue-compensating-delete-catch-o79p5 ks1868-certifications-issue-holder-check-and-legacy-update-catches-o79p4 ks1868-certifications-issue-reserve-save-charge-catches-o79p3 ks1868-certifications-recertify-anchoring-catch-o79p1"
IGN='(ks1868-certifications-issue-anchoring-catch-o79p2|ks1868-certifications-issue-compensating-delete-catch-o79p5|ks1868-certifications-issue-holder-check-and-legacy-update-catches-o79p4|ks1868-certifications-issue-reserve-save-charge-catches-o79p3|ks1868-certifications-recertify-anchoring-catch-o79p1)'
mkdir -p $L/head_copy/src/routes; cp $A/$F $L/head_copy/$F; sha $A/$F > $L/runs_sha_before.txt
git -C $R show $MB:Blockchain/Dev/services/originate/$F > $A/$F; sha $A/$F > $L/runs_sha_base.txt
uptime > $L/load_runs.log
bash $J $L/red_base.json $L/red_base_new.log $NEW
bash $J $L/whole_base.json $L/whole_base.log --testPathIgnorePatterns '/node_modules/' '\.integration\.test\.ts$' "$IGN"
uptime >> $L/load_runs.log
cp $L/head_copy/$F $A/$F; sha $A/$F > $L/runs_sha_after.txt; cmp $L/runs_sha_before.txt $L/runs_sha_after.txt && echo RESTORE_OK > $L/runs_restore.log
bash $J $L/head_new.json $L/head_new.log $NEW
bash $J $L/whole_head.json $L/whole_head.log
uptime >> $L/load_runs.log
git -C $R status --short > $L/runs_status_end.log
date > $L/runs.done
