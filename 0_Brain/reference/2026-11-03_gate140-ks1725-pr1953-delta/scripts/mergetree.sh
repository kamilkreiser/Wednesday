#!/bin/bash
# (G) merge-tree of the head onto CURRENT develop (read by ls-remote at start: 2d3b3bb3); paths vs gate 135's 146.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta; R=$G/repo; L=$G/logs; H=928ee20c84dce74930422176e17c962b1ed85bde; DV=2d3b3bb3d3865689e3cad843f9ebb90a2f606960
echo "merge-base(head, develop) = $(git -C $R merge-base $H $DV)"; git -C $R merge-base --is-ancestor $DV $H; echo "develop ancestor of head rc=$?"
T=$(git -C $R merge-tree --write-tree $DV $H 2>$L/merge_tree.err); rc=$?; echo "merge-tree rc=$rc tree=$T head-tree=$(git -C $R rev-parse $H^{tree})"
git -C $R diff --name-only $DV $T | sort > $L/mt_paths.txt; git -C $R diff --name-only $DV...$H | sort > $L/paths.txt
echo "merge result changes $(wc -l < $L/mt_paths.txt | tr -d ' ') paths; PR three-dot $(wc -l < $L/paths.txt | tr -d ' '); identical sets: $(cmp -s $L/mt_paths.txt $L/paths.txt && echo yes || echo NO)"
git -C $R diff --shortstat $DV...$H
sort /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953/logs/paths.txt > $L/g135_paths_sorted.txt
echo "paths NEW since gate 135:"; comm -13 $L/g135_paths_sorted.txt $L/paths.txt; echo "paths DROPPED since gate 135:"; comm -23 $L/g135_paths_sorted.txt $L/paths.txt
echo "paths whose PR diff changed since gate 135 (vs gate 135's head three-dot against its develop):"
comm -12 $L/g135_paths_sorted.txt $L/paths.txt | while IFS= read -r p; do a=$(git -C $R diff 8150eeb3802b...ea6d924eb5de -- "$p" | grep -E '^[-+]' | grep -v -E '^(\+\+\+|---)' | shasum | cut -c1-12); b=$(git -C $R diff $DV...$H -- "$p" | grep -E '^[-+]' | grep -v -E '^(\+\+\+|---)' | shasum | cut -c1-12); [ "$a" = "$b" ] || echo "  $p"; done
