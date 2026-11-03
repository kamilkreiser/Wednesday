#!/bin/bash
# merge-tree in THIS gate's clone only (repo/ inside the workdir).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate164-ks1868-pr1981
R=$W/repo
echo "develop and PR head by ls-remote now (read-only checkout):"
git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1981/head; date -u
echo "merge-base: $(git -C $R merge-base 32921f7921c2 2e0f5ec04)"
T=$(git -C $R merge-tree --write-tree 32921f7921c2 2e0f5ec04); echo "merge-tree rc=$? tree=$T"
echo "merged vs develop:"; git -C $R diff --name-only 32921f7921c2 $T
echo "PR paths:"; git -C $R diff --name-only 0a6575f7f 2e0f5ec04
echo "base..develop files: $(git -C $R diff --name-only 0a6575f7f 32921f7921c2 | wc -l)"
echo "base..develop under services/security: $(git -C $R diff --name-only 0a6575f7f 32921f7921c2 -- Blockchain/Dev/services/security | wc -l)"
echo "base..develop under services/ (control): $(git -C $R diff --name-only 0a6575f7f 32921f7921c2 -- Blockchain/Dev/services | wc -l)"
echo "base..develop docs fragments: $(git -C $R diff --name-only 0a6575f7f 32921f7921c2 | grep -c fragments)"
echo "head vs merged under services/security: $(git -C $R diff --name-only 2e0f5ec04 $T -- Blockchain/Dev/services/security | wc -l)"
echo "shared paths (PR paths also touched by base..develop):"
comm -12 <(git -C $R diff --name-only 0a6575f7f 2e0f5ec04 | sort) <(git -C $R diff --name-only 0a6575f7f 32921f7921c2 | sort)
echo "(end shared)"
