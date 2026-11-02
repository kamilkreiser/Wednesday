R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/repo
git -C $R checkout -q --detach pr1937 2>&1 | tail -3
git -C $R rev-parse HEAD
git -C $R ls-files | wc -l
