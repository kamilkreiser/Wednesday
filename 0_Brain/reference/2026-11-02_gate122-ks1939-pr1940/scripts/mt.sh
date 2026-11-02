#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940; R=$W/repo; L=$W/logs
git -C $R fetch -q origin refs/pull/1941/head:refs/remotes/pr/1941 refs/pull/1939/head:refs/remotes/pr/1939 refs/pull/1938/head:refs/remotes/pr/1938
for p in 1938 1939 1941; do echo "PR $p: $(git -C $R log -1 --format='%h %an %s' refs/remotes/pr/$p)"; git -C $R diff --name-only $(git -C $R merge-base refs/remotes/pr/$p origin/develop) refs/remotes/pr/$p | /usr/bin/grep -i "verification" ; done
echo "--- PR1940 onto develop 0e3a9b65"
git -C $R diff --name-only e2a2426d221d 96208f377d14 | sort > $L/pr_paths.log
T=$(git -C $R merge-tree --write-tree origin/develop refs/remotes/pr/1940); echo "rc=$? tree=$T"
git -C $R diff-tree -r --name-only origin/develop $T | sort > $L/merge_result_paths.log; wc -l < $L/merge_result_paths.log; diff $L/merge_result_paths.log $L/pr_paths.log && echo SAME_PATHS
echo "develop paths since base: $(git -C $R diff --name-only e2a2426d221d origin/develop | wc -l)"; git -C $R log --oneline e2a2426d221d..origin/develop
git -C $R diff --name-only e2a2426d221d origin/develop | sort > $L/develop_paths.log; echo "shared with PR:"; comm -12 $L/develop_paths.log $L/pr_paths.log; echo "control (develop vs itself) $(comm -12 $L/develop_paths.log $L/develop_paths.log | wc -l)"
echo "verification.ts on develop vs base: $(git -C $R diff --quiet e2a2426d221d origin/develop -- Blockchain/Dev/services/originate/src/routes/verification.ts && echo UNCHANGED || echo CHANGED)"
echo "$T" > $L/merge_tree_id.txt
