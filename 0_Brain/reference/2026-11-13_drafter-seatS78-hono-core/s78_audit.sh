#!/bin/bash
export GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="Authorization: Basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64)"
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; C=$F/clone2; W=$F/s78_work2
git -C $C ls-tree -r --name-only refs/scratch/merged2226 -- Blockchain/Dev/scripts/audit Blockchain/Dev/audit-baseline.json > $F/s78_auditfiles.out; wc -l < $F/s78_auditfiles.out; head -20 $F/s78_auditfiles.out
git -C $C archive refs/scratch/merged2226 $(cat $F/s78_auditfiles.out | tr '\n' ' ') | tar -x -C $W/merged
git -C $C archive refs/scratch/merged2226 $(cat $F/s78_auditfiles.out | tr '\n' ' ') | tar -x -C $W/after
