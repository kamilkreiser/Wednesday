R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/repo
git -C $R fetch origin refs/heads/develop:dev_now 2>&1 | tail -1
git -C $R rev-parse dev_now
git -C $R diff --name-only c70f339063ee dev_now | wc -l
git -C $R diff --name-only c70f339063ee dev_now | /usr/bin/grep -c -E 'env.example|docker-compose|bootstrap-env|userRepo|timestamping|KS-1081'
git -C $R merge-tree --write-tree dev_now pr1937 > /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/merge_tree2.out 2>&1; echo "merge-tree rc=$?"
T=$(head -1 /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/merge_tree2.out); git -C $R diff --name-only dev_now $T | sort | diff - /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/pr_paths.txt && echo SAME_PATHS
git -C $R ls-remote origin refs/pull/1937/head refs/heads/develop
