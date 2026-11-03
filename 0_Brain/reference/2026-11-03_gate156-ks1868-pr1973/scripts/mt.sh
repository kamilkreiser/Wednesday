#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate156-ks1868-pr1973/repo
git -C $R log --oneline -6 refs/remotes/gate/develop; echo ---
git -C $R diff --stat 7ad0dcc14e5c e16104beec; echo
for D in 4deb2fc10b7d852194183c08e86e2ecacb7231db refs/remotes/gate/develop; do
  echo "== $D $(git -C $R rev-parse $D)"
  T=$(git -C $R merge-tree --write-tree $D e16104beec); echo "rc=$? tree=$T"
  echo "changed vs develop:"; git -C $R diff --name-only $D $(echo "$T"|head -1)
done
echo "--- base..develop governance paths:"; git -C $R diff --name-only 7ad0dcc14e5c refs/remotes/gate/develop | grep -i governance
echo "--- base..develop count: $(git -C $R diff --name-only 7ad0dcc14e5c refs/remotes/gate/develop | wc -l)"
