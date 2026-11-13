export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172
C=$D/clone
for p in "ae5b615f4cc0 2223 cb6f1a6a6410" "ae5b615f4cc0 2222 9bbb1b76751f" "1ebc3eae6cf4 2224 17a269f4da70"; do set -- $p; t=$(git -C $C merge-tree --write-tree $1 refs/remotes/pr/$2); echo "$2 on $1: ${t:0:12} want $3"; done
git -C $C log --oneline -3 origin/develop
echo count dc57..develop: $(git -C $C rev-list --count dc57df60a959..origin/develop)
git -C $C diff --name-only dc57df60a959 origin/develop
