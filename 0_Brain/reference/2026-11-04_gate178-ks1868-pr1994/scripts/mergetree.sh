#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate178-ks1868-pr1994
R=$W/repo
git -C $R merge-tree --write-tree refs/gate/develop refs/gate/h1994 > $W/runs/mt_dev.txt; rc=$?
T1=$(head -1 $W/runs/mt_dev.txt); echo "1994 onto develop ea5134d6: rc=$rc tree=${T1:0:12} lines=$(wc -l < $W/runs/mt_dev.txt)"
git -C $R merge-tree --write-tree refs/gate/develop refs/gate/h1993 > $W/runs/mt_d93.txt; rc=$?
T93=$(head -1 $W/runs/mt_d93.txt); echo "1993 onto develop: rc=$rc tree=${T93:0:12}"
C93=$(git -C $R commit-tree $T93 -p refs/gate/develop -p refs/gate/h1993 -m sim-develop-plus-1993)
git -C $R merge-tree --write-tree $C93 refs/gate/h1994 > $W/runs/mt_d93_94.txt; rc=$?
T2=$(head -1 $W/runs/mt_d93_94.txt); echo "1994 onto develop+1993: rc=$rc tree=${T2:0:12} lines=$(wc -l < $W/runs/mt_d93_94.txt)"
echo "paths changed develop -> develop+1994: $(git -C $R diff --name-only refs/gate/develop $T1 | wc -l)"
echo "paths changed develop+1993 -> +1994: $(git -C $R diff --name-only $C93 $T2 | wc -l)"
echo "content equal to head for the 11 paths in T1: $(for f in $(git -C $R diff --name-only 79145a312f01 refs/gate/h1994 | tr ' ' '\001'); do f=$(echo "$f"|tr '\001' ' '); [ "$(git -C $R rev-parse "$T1:$f")" = "$(git -C $R rev-parse "refs/gate/h1994:$f")" ] && echo y; done | wc -l) of 11; in T2: $(for f in $(git -C $R diff --name-only 79145a312f01 refs/gate/h1994 | tr ' ' '\001'); do f=$(echo "$f"|tr '\001' ' '); [ "$(git -C $R rev-parse "$T2:$f")" = "$(git -C $R rev-parse "refs/gate/h1994:$f")" ] && echo y; done | wc -l) of 11"
git -C $R diff --name-only refs/gate/h1993^ refs/gate/h1993 | sort > $W/scratch/f93
git -C $R diff --name-only 79145a312f01 refs/gate/h1994 | sort > $W/scratch/f94
echo "1993 files: $(wc -l < $W/scratch/f93); 1994 files: $(wc -l < $W/scratch/f94); shared: $(comm -12 $W/scratch/f93 $W/scratch/f94 | wc -l)"
echo "control (1994 list + one planted 1993 path): $( (cat $W/scratch/f94; head -1 $W/scratch/f93) | sort | comm -12 $W/scratch/f93 - | wc -l)"
echo "1992 delta (79145a..develop) on nft.routes.ts: $(git -C $R diff --numstat 79145a312f01 refs/gate/develop -- Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts | wc -l); repo-wide control: $(git -C $R diff --numstat 79145a312f01 refs/gate/develop | wc -l)"
echo "1993 delta on nft-certificate service: $(git -C $R diff --numstat refs/gate/h1993^ refs/gate/h1993 -- Blockchain/Dev/services/nft-certificate | wc -l)"
cat $W/scratch/f93
