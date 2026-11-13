export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB173
C=$D/clone
for p in "ae5b615f4cc0 2223 cb6f1a6a6410" "ae5b615f4cc0 2222 9bbb1b76751f" "1ebc3eae6cf4 2224 17a269f4da70"; do set -- $p; t=$(git -C $C merge-tree --write-tree $1 refs/remotes/pr/$2); echo "$2 on $1: ${t:0:12} want $3"; done
echo "develop tree: $(git -C $C rev-parse origin/develop^{tree}) parents: $(git -C $C rev-list --parents -n1 origin/develop)"
git -C $C diff --name-only 9105cfdee484 origin/develop | head
