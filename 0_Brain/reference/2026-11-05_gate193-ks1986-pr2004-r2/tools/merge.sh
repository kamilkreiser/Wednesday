#!/bin/bash
# Gate 193 Q8 + Q1 full-range checks, in the gate's OWN clone only. usage: merge.sh <develop-sha>
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2
R=$W/repo
D=${1:-e899463d2a0b1b30f2cff46b23d001622620029a}; HD=4432db224a5867fdb6afaabf56df08cdf640d067; B=035685291b9d58ae6ea8ba5f05adf9379f9c2944
T=$(git -C $R merge-tree --write-tree $D $HD); echo "merge-tree develop=$D rc=$? tree=$T"
echo "base ancestor of develop: $(git -C $R merge-base --is-ancestor $B $D && echo yes || echo no)"
git -C $R diff --name-only $B $D | sort > $W/runs/dev_range.txt
git -C $R diff --name-only $B $HD | sort > $W/runs/pr_range.txt
echo "develop range files: $(wc -l < $W/runs/dev_range.txt); pr range: $(wc -l < $W/runs/pr_range.txt)"
echo "shared(dev range, pr range): $(comm -12 $W/runs/dev_range.txt $W/runs/pr_range.txt | wc -l)"
echo "control pr vs pr: $(comm -12 $W/runs/pr_range.txt $W/runs/pr_range.txt | wc -l)"
(cat $W/runs/dev_range.txt; echo Blockchain/Dev/services/originate/src/routes/verification.ts) | sort > $W/tmp/planted_dev.txt
echo "planted control (dev list + verification.ts) vs pr: $(comm -12 $W/tmp/planted_dev.txt $W/runs/pr_range.txt | wc -l)"
echo "-- develop range:"; cat $W/runs/dev_range.txt
echo "-- per-path blob, merge tree vs head"
while read -r p; do a=$(git -C $R rev-parse "$T:$p"); b=$(git -C $R rev-parse "$HD:$p"); echo "$([ "$a" = "$b" ] && echo EQUAL || echo DIFF) ${a:0:12} $p"; done < $W/runs/pr_range.txt
echo "-- diff develop..mergetree numstat"; git -C $R diff --numstat $D $T
echo "-- full range: api-gateway/migration/verificationV2 paths: $(git -C $R diff --name-only $B $HD | grep -ciE 'api-gateway|migration|verificationV2')"
echo "-- ks1561-g188-f1 existing-test changed lines (base..head):"
git -C $R diff -U0 $B $HD -- Blockchain/Dev/services/originate/src/__tests__/ks1561-g188-f1-original-outside-the-fetched-row-set.test.ts | grep -E '^[-+][^-+]'
P=Blockchain/Dev/services/originate/src/__tests__/ks1561-g188-f1-original-outside-the-fetched-row-set.test.ts
echo "ks1561-g188-f1 blob 577f / head: $(git -C $R rev-parse 577f668f:$P | cut -c1-12) $(git -C $R rev-parse $HD:$P | cut -c1-12)"
C="Projects Documents/fragments/cheat/KS-1986-v1-original-across-tenants.html"
echo "cheat blob 577f / head: $(git -C $R rev-parse "577f668f:$C" | cut -c1-12) $(git -C $R rev-parse "$HD:$C" | cut -c1-12)"
V=Blockchain/Dev/services/originate/src/routes/verificationV2.ts
echo "verificationV2 blob base / head: $(git -C $R rev-parse $B:$V | cut -c1-12) $(git -C $R rev-parse $HD:$V | cut -c1-12)"
V1=Blockchain/Dev/services/originate/src/routes/verification.ts
echo "verification.ts blob base / develop: $(git -C $R rev-parse $B:$V1 | cut -c1-12) $(git -C $R rev-parse $D:$V1 | cut -c1-12)"
