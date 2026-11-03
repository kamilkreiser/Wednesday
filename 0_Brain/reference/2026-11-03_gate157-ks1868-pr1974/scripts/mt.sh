#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate157-ks1868-pr1974/repo
H=35f1842fa7dee22125ce5fa3ba0dafcc5e32d713
echo "develop: $(git -C $R rev-parse refs/remotes/gate/develop)"; git -C $R log --oneline -3 refs/remotes/gate/develop
echo "merge-base(head, develop): $(git -C $R merge-base $H refs/remotes/gate/develop)"
for D in 4deb2fc10b7d refs/remotes/gate/develop; do
  echo "== $D $(git -C $R rev-parse $D 2>&1)"
  T=$(git -C $R merge-tree --write-tree $D $H); echo "rc=$? tree=$(echo "$T"|head -1)"
  echo "changed vs develop:"; git -C $R diff --name-only $D $(echo "$T"|head -1)
done
echo "--- base..develop count: $(git -C $R diff --name-only 7ad0dcc14e5c refs/remotes/gate/develop | wc -l)"
echo "--- base..develop billing/shared/lock paths:"; git -C $R diff --name-only 7ad0dcc14e5c refs/remotes/gate/develop | grep -E 'services/billing|packages/shared|Dev/shared/|package(-lock)?\.json' || echo "(none)"
T=$(git -C $R merge-tree --write-tree refs/remotes/gate/develop $H | head -1)
echo "--- head vs merged tree under billing/shared/lock: $(git -C $R diff --name-only $H $T -- Blockchain/Dev/services/billing Blockchain/Dev/packages/shared Blockchain/Dev/shared Blockchain/Dev/package.json Blockchain/Dev/package-lock.json | wc -l) paths"
echo "--- lockfile head vs develop: $(git -C $R diff --name-only $H refs/remotes/gate/develop -- Blockchain/Dev/package-lock.json Blockchain/Dev/services/billing/package-lock.json | wc -l) differ"
