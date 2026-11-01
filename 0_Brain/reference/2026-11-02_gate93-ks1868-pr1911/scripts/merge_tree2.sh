#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/repo
git -C $R fetch -q origin refs/heads/develop:refs/gate/develop_end; echo "fetch rc=$?"
git -C $R rev-parse refs/gate/develop_end
echo "commits 03977e89..develop_end:"; git -C $R log --oneline refs/gate/develop..refs/gate/develop_end
echo "paths changed on develop since base:"; git -C $R diff --name-only refs/gate/develop refs/gate/develop_end
echo "shared with PR paths:"; comm -12 <(git -C $R diff --name-only refs/gate/develop refs/gate/develop_end | sort) <(git -C $R diff --name-only refs/gate/develop...refs/gate/pr1911 | sort); echo "(end shared)"
echo "positive control (PR vs itself): $(comm -12 <(git -C $R diff --name-only refs/gate/develop...refs/gate/pr1911 | sort) <(git -C $R diff --name-only refs/gate/develop...refs/gate/pr1911 | sort) | wc -l)"
T=$(git -C $R merge-tree --write-tree refs/gate/develop_end refs/gate/pr1911); echo "merge-tree rc=$? tree=$T"
diff <(git -C $R diff --name-only refs/gate/develop_end $T) <(git -C $R diff --name-only refs/gate/develop...refs/gate/pr1911) && echo "merged change vs develop_end == PR's 6 paths"
git -C $R diff --stat refs/gate/develop_end $T | tail -1
echo "services/auth changed on develop since base: $(git -C $R diff --name-only refs/gate/develop refs/gate/develop_end -- Blockchain/Dev/services/auth | wc -l)"
