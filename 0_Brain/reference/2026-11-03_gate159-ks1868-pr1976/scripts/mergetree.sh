#!/bin/bash
# merge-tree of head onto develop 66cbe4e5, path overlap, merged-blob equality, and a positive control.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
R=$W/repo
g() { git -C "$R" "$@"; }
D=66cbe4e52d5afadc9d13ca141200026cc68d5095; H=dba3a90a95c9fb6028d1529195ed0af464259158; MB=$(g merge-base $D $H)
echo "merge-base $MB"
echo "develop moved: $(g rev-list --count $MB..$D) commits, $(g diff --name-only $MB $D | wc -l | tr -d ' ') paths"
g diff --name-only $MB $D | sort > "$W/logs/dev_paths.txt"
g diff --name-only $MB $H | sort > "$W/logs/pr_paths.txt"
echo "PR paths: $(wc -l < "$W/logs/pr_paths.txt" | tr -d ' ')"; cat "$W/logs/pr_paths.txt"
echo "overlap: $(comm -12 "$W/logs/dev_paths.txt" "$W/logs/pr_paths.txt" | wc -l | tr -d ' ')"
echo "develop touched under services/anchoring or packages/shared or fragments dirs:"; grep -E 'services/anchoring/|packages/shared/|fragments/(flow|cheat)/' "$W/logs/dev_paths.txt" | head -20
T=$(g merge-tree --write-tree $D $H); rc=$?
echo "merge-tree rc=$rc tree=$(echo "$T" | head -1)"; echo "$T" | sed -n '2,20p'
MT=$(echo "$T" | head -1)
echo "merged-vs-develop paths:"; g diff --name-only $D $MT | sort > "$W/logs/merged_vs_dev_paths.txt"; cat "$W/logs/merged_vs_dev_paths.txt"
diff "$W/logs/merged_vs_dev_paths.txt" "$W/logs/pr_paths.txt" && echo "MERGED PATHS == PR PATHS"
while read -r p; do
  a=$(g rev-parse "$MT:$p"); b=$(g rev-parse "$H:$p"); [ "$a" = "$b" ] && echo "blob equal: $p" || echo "BLOB DIFFERS: $p"
done < "$W/logs/pr_paths.txt"
# positive control: a synthetic develop commit editing reconciler.ts line the PR edits, merge-tree must conflict
PC=$W/logs/_pc; mkdir -p "$PC"
F=Blockchain/Dev/services/anchoring/src/reconciler.ts
g show "$D:$F" | sed "s/deps.log('warn', 'Reconciler pass failed', { error: err?.message });/deps.log('warn', 'Reconciler pass failed (control)', { error: String(err) });/" > "$PC/reconciler.ts"
cmp -s "$PC/reconciler.ts" <(g show "$D:$F") && echo "CONTROL EDIT DID NOT APPLY"
BLOB=$(g hash-object -w "$PC/reconciler.ts")
TREE=$(g ls-tree -r $D | awk -v f="$F" -v b="$BLOB" 'BEGIN{OFS="\t"} { split($0,a,"\t"); if (a[2]==f) { sub(/[0-9a-f]{40}/, b, a[1]) } print a[1], a[2] }' | g mktree --missing)
C=$(g commit-tree "$TREE" -p $D -m 'gate159 positive control')
T2=$(g merge-tree --write-tree $C $H); echo "control merge-tree rc=$? first line $(echo "$T2" | head -1)"; echo "$T2" | grep -i conflict | head -3
