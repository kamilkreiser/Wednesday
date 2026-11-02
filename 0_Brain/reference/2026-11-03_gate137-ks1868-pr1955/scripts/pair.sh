#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955; R=$W/repo
F=Blockchain/Dev/services/anchoring/src/index.ts
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad
echo "1953 $(git -C $R rev-parse pr/1953)  1955 $(git -C $R rev-parse pr/1955)  merge-base $(git -C $R merge-base pr/1953 pr/1955)"
echo "shared paths: $(comm -12 <(git -C $R diff --name-only 9a9bf86967e3 pr/1953 | sort) <(git -C $R diff --name-only 9a9bf86967e3 pr/1955 | sort) | tr '\n' ' ')"
T=$(git -C $R merge-tree --write-tree pr/1953 pr/1955); RC=$?; echo "merge-tree 1953+1955 rc=$RC tree=$T"
echo "$T" > $W/logs/mt_tree_pair.txt
# merged index.ts must contain both PRs' changes: every '+' line of each PR's index.ts hunks present
for P in 1953 1955; do
  git -C $R diff -U0 9a9bf86967e3 pr/$P -- $F | grep '^+' | grep -v '^+++' | sed 's/^+//' > $S/plus_$P.txt
  git -C $R show $T:$F > $S/merged_index.ts
  miss=0; while IFS= read -r l; do grep -qxF -- "$l" $S/merged_index.ts || miss=$((miss+1)); done < $S/plus_$P.txt
  echo "PR $P index.ts '+' lines: $(wc -l < $S/plus_$P.txt), missing from merged: $miss"
done
echo "merged tree vs 1953 head: paths = $(git -C $R diff --name-only pr/1953 $T | tr '\n' ' ')"
echo "merged tree vs 1955 head: path count = $(git -C $R diff --name-only pr/1955 $T | wc -l)"
# planted control: a commit on top of 1953 that edits 1955's POST-verify site line
git -C $R show pr/1953:$F > $S/planted_index.ts
L=$(grep -n "reason = err?.message;" $S/planted_index.ts | sed -n 2p | cut -d: -f1); echo "planted at 1953-coords line $L: $(sed -n ${L}p $S/planted_index.ts)"
sed -i '' "${L}s/reason = err?.message;/reason = String(err?.message); \/\/ g137 planted/" $S/planted_index.ts
B=$(git -C $R hash-object -w $S/planted_index.ts)
export GIT_INDEX_FILE=$S/pair.index; git -C $R read-tree pr/1953; git -C $R update-index --cacheinfo 100644,$B,$F; PT=$(git -C $R write-tree); unset GIT_INDEX_FILE
PC=$(git -C $R commit-tree $PT -p pr/1953 -m "g137 planted control"); echo "planted commit $PC"
git -C $R merge-tree --write-tree --name-only $PC pr/1955 > $S/planted_mt.out 2>&1; echo "planted merge-tree rc=$?"; head -6 $S/planted_mt.out
