#!/bin/bash
# transfer (vitest): head new file; head whole; base product + new file (red first); base whole without new file. sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962
R=$W/repo; REL=Blockchain/Dev/services/transfer; T=$R/$REL; SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g146
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 node $W/scripts/vt.cjs "$@" > $log 2>&1; echo "rc=$?" >> $log; }
P=src/services/approvalWorkflowService.ts; TN=src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts; H=$(sha $T/$P)
vt $W/logs/head_new.log $TN
vt $W/logs/head_whole.log
git -C $R show cc33e702:$REL/$P > $T/$P
vt $W/logs/red_base_new.log $TN
mv $T/$TN $SC/new.test.ts
vt $W/logs/base_whole_excl_new.log
mv $SC/new.test.ts $T/$TN
git -C $R show pr1962:$REL/$P > $T/$P
{ [ "$(sha $T/$P)" = "$H" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/suites_restore.log
echo done > $W/logs/suites.done
