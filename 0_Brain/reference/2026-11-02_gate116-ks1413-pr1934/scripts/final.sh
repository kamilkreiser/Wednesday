#!/bin/bash
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934; R=$D/repo
git -C $R fetch -q origin develop; DEV=$(git -C $R rev-parse origin/develop); echo develop=$DEV
git -C $R merge-tree --write-tree origin/develop pr1934 > $D/logs/mergetree.log 2>&1; echo mt_rc=$?
T=$(head -1 $D/logs/mergetree.log); git -C $R diff --name-only origin/develop $T > $D/logs/mt_changed.txt
git -C $R diff --name-only 8f313815f415 pr1934 > $D/logs/pr_paths.txt
diff <(sort $D/logs/mt_changed.txt) <(sort $D/logs/pr_paths.txt) && echo SAME_PATHS
git -C $R diff --name-only 8f313815f415 origin/develop | grep -Fxf $D/logs/pr_paths.txt; echo overlap_rc=$? "(1=none)"
for f in Start_Up/start-secuura.sh Blockchain/Dev/scripts/start-local.sh; do bash -n $D/wt_head/$f && echo "bash -n ok $f"; done
echo "--- non-banner diff lines (excluding the 2 hunks), numstat"; git -C $R diff --numstat 8f313815f415 pr1934 -- Start_Up Blockchain/Dev/scripts/start-local.sh
echo "--- diff -U0 of scripts"; git -C $R diff -U0 8f313815f415 pr1934 -- Start_Up/start-secuura.sh Blockchain/Dev/scripts/start-local.sh | grep -E '^[-+@]' | grep -vE '^(---|\+\+\+)'
echo "--- other demo123/admin123 echoing scripts"; git -C $R grep -nE '(echo|printf|log_[a-z]+|info|warn)[^|]*(demo123|admin123|secuura_grafana)' origin/develop -- '*.sh' ':!*__tests__*' | head
echo "--- head end"; git -C $R ls-remote origin refs/pull/1934/head refs/heads/develop
