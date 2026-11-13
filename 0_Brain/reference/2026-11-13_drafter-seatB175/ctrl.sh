export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB175
C=$D/clone_work/clone
for p in "ae5b615f4cc0 2223 cb6f1a6a6410" "ae5b615f4cc0 2222 9bbb1b76751f" "1ebc3eae6cf4 2224 17a269f4da70"; do set -- $p; t=$(git -C $C merge-tree --write-tree $1 refs/remotes/pr/$2); echo "$2 on $1: ${t:0:12} want $3"; done
t=$(git -C $C merge-tree --write-tree a6af38a517161709e56bbce61b82e2a9ccbce6a5 refs/remotes/pr/2227); echo "2227 on a6af38a5: ${t:0:12} want 3aee88a0360a (gate 350)"
t=$(git -C $C merge-tree --write-tree ef22a2d10182f1ad524ebd845b285410540e3342 refs/remotes/pr/2227); echo "2227 on ef22a2d1: ${t:0:12} want 9229982efb57 (B174 READY)"
echo "develop tree: $(git -C $C rev-parse origin/develop^{tree}) parents: $(git -C $C rev-list --parents -n1 origin/develop)"
git -C $C diff --name-only ef22a2d10182 origin/develop | head
echo "r118 analog parent: $(git -C $C rev-list --parents -n1 refs/remotes/pr/r118an)"
git -C $C diff --numstat origin/develop refs/remotes/pr/r118an | head
