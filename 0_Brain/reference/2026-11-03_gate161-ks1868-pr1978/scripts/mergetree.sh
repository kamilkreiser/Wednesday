#!/bin/bash
# G161: merge-tree of the PR head onto develop 19fc6830, inside the gate's own clone (objects only, no checkout).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate161-ks1868-pr1978; R=$W/repo
B=66cbe4e52d5afadc9d13ca141200026cc68d5095; Hd=1062b621269dac98f618a89f10baa51ff49c8c34; D=19fc68309c254227e751b3186970360f921fdc74
echo "merge-base(head,develop)=$(git -C $R merge-base $Hd $D)"; echo "base..develop commits: $(git -C $R rev-list --count $B..$D)"
T=$(git -C $R merge-tree --write-tree $D $Hd); echo "merge-tree rc=$? tree=$T"
echo "## merged tree vs develop:"; git -C $R diff --name-only $D $T
echo "## PR paths:"; git -C $R diff --name-only $B $Hd
echo "## base..develop paths:"; git -C $R diff --name-only $B $D
echo "## overlap with PR paths:"; comm -12 <(git -C $R diff --name-only $B $D | sort) <(git -C $R diff --name-only $B $Hd | sort)
echo "## base..develop under services/auth:"; git -C $R diff --name-only $B $D -- Blockchain/Dev/services/auth | wc -l
echo "## head vs merged under services/auth (lines):"; git -C $R diff $Hd $T -- Blockchain/Dev/services/auth | wc -l
