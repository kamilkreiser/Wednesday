W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968; R=$W/repo
git -C $R ls-remote origin refs/heads/develop refs/pull/1968/head
git -C $R fetch -q origin develop:dev_new; git -C $R rev-parse dev_new; git -C $R merge-tree --write-tree dev_new pr1968 > $W/logs/merge_tree.log 2>&1; echo rc=$?; head -3 $W/logs/merge_tree.log
T=$(head -1 $W/logs/merge_tree.log); git -C $R diff --name-only dev_new $T > $W/logs/merged_vs_develop.log; git -C $R diff --name-only 2f9f7db313b3 pr1968 > $W/logs/pr_paths.log; diff $W/logs/merged_vs_develop.log $W/logs/pr_paths.log && echo PATHS_EQUAL; wc -l < $W/logs/pr_paths.log
git -C $R diff --name-only 2f9f7db313b3 dev_new | /usr/bin/grep -E "vc-issuer|fragments/(flow|cheat)/KS-1868-vc-issuer" | head
