R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/repo
bash -n $R/Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh; echo "bash -n rc=$?"
git -C $R rev-list --count origin/develop..pr1937 ; git -C $R rev-list --count 8f313815f415..pr1937
git -C $R merge-tree --write-tree origin/develop pr1937 > /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/merge_tree.out 2>&1; echo "merge-tree rc=$?"
T=$(head -1 /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/merge_tree.out); git -C $R diff --name-only origin/develop $T
git -C $R diff --name-only origin/develop...pr1937 | sort > /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/pr_paths.txt
git -C $R diff --name-only origin/develop $T | sort | diff - /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/pr_paths.txt && echo SAME_PATHS
git -C $R diff --name-only 8f313815f415 origin/develop -- Blockchain/Dev/env.example Blockchain/Dev/docker-compose.yml Blockchain/Dev/scripts/bootstrap-env.sh Blockchain/Dev/services/auth/src/repositories/userRepo.ts Blockchain/Dev/services/timestamping | wc -l
git -C $R ls-remote origin refs/pull/1937/head refs/heads/develop
