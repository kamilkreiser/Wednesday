W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate151-ks1868-pr1967
R=$W/repo
git -C $R fetch origin develop
DEV=$(git -C $R rev-parse origin/develop); echo develop=$DEV
T=$(git -C $R merge-tree --write-tree $DEV pr1967); echo rc=$? tree=$T
git -C $R diff --name-only $DEV $T | sort > $W/logs/merged_vs_develop.log
git -C $R diff --name-only origin/develop...pr1967 | sort > $W/logs/pr_paths.log
diff $W/logs/merged_vs_develop.log $W/logs/pr_paths.log && echo paths-equal
git -C $R diff --stat $DEV 118cf6d972e5723284c5270a66cc7337027ef6e0 -- Blockchain/Dev/services/demo-service/src/routes/state.ts | tail -1
git -C $R merge-base pr1967 $DEV
