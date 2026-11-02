#!/bin/bash
# Real-process probe matrix. Product swaps in the clone are sha256-restored at the end.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962
R=$W/repo; REL=Blockchain/Dev/services/transfer/src; P=$R/$REL/services/approvalWorkflowService.ts; DB=$R/$REL/db.ts
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g146
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
HP=$(sha $P); HD=$(sha $DB)
KINDS="none ordinary string revokedProxy throwingGetter bigintMsg"
run(){ ver=$1; shift; for sc in "$@"; do for k in $KINDS; do
  case $sc in sweep_k2) node $W/scripts/driver.cjs $ver-k2 sweep_k $k 2 > /dev/null 2>&1;; sweep_k3) node $W/scripts/driver.cjs $ver-k3 sweep_k $k 3 > /dev/null 2>&1;; *) node $W/scripts/driver.cjs $ver $sc $k > /dev/null 2>&1;; esac
done; done; }
ALL="boot_probe boot_seed1 boot_seedall sweep_k2 sweep_k3 sweep_select sweep_wfread"
git -C $R show cc33e702:$REL/services/approvalWorkflowService.ts > $P; run base $ALL
git -C $R show pr1962:$REL/services/approvalWorkflowService.ts > $P; run head $ALL
git -C $R show origin/develop:$REL/db.ts > $DB; run merged boot_probe boot_seed1 sweep_k3
git -C $R show cc33e702:$REL/services/approvalWorkflowService.ts > $P; run devnow boot_probe boot_seed1 sweep_k3
git -C $R show pr1962:$REL/services/approvalWorkflowService.ts > $P; git -C $R show pr1962:$REL/db.ts > $DB
{ [ "$(sha $P)" = "$HP" ] && [ "$(sha $DB)" = "$HD" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/probes_restore.log
date > $W/logs/probes.done
