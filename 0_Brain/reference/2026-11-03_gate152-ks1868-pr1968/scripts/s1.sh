W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968; R=$W/repo
git -C $R fetch origin develop:dev_local 2>&1|tail -1
git -C $R rev-parse dev_local pr1968
git -C $R merge-base pr1968 dev_local
git -C $R diff --stat dev_local...pr1968 | tail -10
git -C $R diff dev_local...pr1968 -- Blockchain/Dev/services/vc-issuer/src > $W/logs/hunks.diff
