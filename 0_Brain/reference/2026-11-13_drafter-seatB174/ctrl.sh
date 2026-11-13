export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB174
C=$D/clone
for p in "ae5b615f4cc0 2223 cb6f1a6a6410" "ae5b615f4cc0 2222 9bbb1b76751f" "1ebc3eae6cf4 2224 17a269f4da70"; do set -- $p; t=$(git -C $C merge-tree --write-tree $1 refs/remotes/pr/$2); echo "$2 on $1: ${t:0:12} want $3"; done
t=$(git -C $C merge-tree --write-tree a6af38a517161709e56bbce61b82e2a9ccbce6a5 refs/remotes/pr/2227); echo "2227 on a6af38a5: ${t:0:12} want 3aee88a0360a (gate 350)"
echo "develop tree: $(git -C $C rev-parse origin/develop^{tree}) parents: $(git -C $C rev-list --parents -n1 origin/develop)"
git -C $C diff --name-only a288aa45d6b2 origin/develop | head
echo "root lock line 15437-15438 on develop:"; git -C $C show origin/develop:Blockchain/Dev/package-lock.json | sed -n '15437,15438p'
echo "mcp lock line 2539-2540 on develop:"; git -C $C show origin/develop:Blockchain/Dev/services/mcp-server/package-lock.json | sed -n '2539,2540p'
echo "2227 head root lines:"; git -C $C show refs/remotes/pr/2227:Blockchain/Dev/package-lock.json | sed -n '15437,15438p'
echo "2227 parent: $(git -C $C rev-list --parents -n1 refs/remotes/pr/2227)"
git -C $C diff --numstat a288aa45d6b2 refs/remotes/pr/2227 | head
