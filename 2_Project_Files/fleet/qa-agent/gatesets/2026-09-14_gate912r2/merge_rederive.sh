#!/bin/bash
# merge_rederive.sh — re-derive PR #912's develop merge (323151415 = ae8751f38 + 8861e6216) in the gate set's OWN
# --shared --no-checkout clone (the ONE write verb of the build — `git merge-tree --write-tree` — runs HERE, never in the
# Secuura checkout). Prints: git's own auto-merge of develop into the r1 head (expected: a CONFLICT in
# anchorStateSync.ts), the builder's hand resolution diffed against git's conflicted blob (expected: ONLY that file
# differs), the marker census, the `const prior` counts, and two controls.
set -u
CLONE='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/model/clone912'
DEV='8861e62161466c40f08d2b10a30edeb203123993'
R1='ae8751f380ed361505694ba71ad9bf1308ee0e87'
MERGE='3231514154aaa8a469e6cdd5f553ee8ce6079b89'
HEAD='609c44c55323b5c90320847b6837ca37f6586705'
F='Blockchain/Dev/services/originate/src/services/anchorStateSync.ts'
echo "merge_rederive.sh — $(date '+%Y-%m-%d %H:%M:%S %Z') — clone $CLONE"
echo "== merge-tree --write-tree develop r1"
MT_OUT="$(git -C "$CLONE" merge-tree --write-tree "$DEV" "$R1" 2>&1)"; rc=$?
echo "rc=$rc"; echo "$MT_OUT"
MT="$(echo "$MT_OUT" | head -1)"
echo "== the merge commit's tree"; MTREE="$(git -C "$CLONE" rev-parse "${MERGE}^{tree}")"; echo "$MTREE"
echo "== diff-tree --name-status <git's conflicted auto-merge tree> <merge commit tree>  (expect exactly $F)"
git -C "$CLONE" diff-tree -r --name-status "$MT" "$MTREE"
echo "== diff --numstat between them"
git -C "$CLONE" diff --numstat "$MT" "$MTREE"
echo "== the patch: git's auto-merge (with markers) -> the builder's hand resolution"
git -C "$CLONE" diff "$MT" "$MTREE" -- "$F"
echo "== conflict-marker census in git's auto-merge blob (positive control: 'markDocumentAnchorFailed' count on the same blob)"
git -C "$CLONE" show "$MT:$F" | /usr/bin/grep -c -i -e '^<<<<<<<' -e '^=======' -e '^>>>>>>>'
git -C "$CLONE" show "$MT:$F" | /usr/bin/grep -c -i 'markDocumentAnchorFailed'
echo "== 'const prior' count: git's auto-merge blob / merge commit / head  (expect 2 / 1 / 1)"
for t in "$MT" "$MTREE" "${HEAD}^{tree}"; do printf '%s: ' "${t:0:12}"; git -C "$CLONE" show "$t:$F" | /usr/bin/grep -c -i 'const prior'; done
echo "== control 1: merge-tree develop develop == develop's tree"
git -C "$CLONE" merge-tree --write-tree "$DEV" "$DEV"; git -C "$CLONE" rev-parse "${DEV}^{tree}"
echo "== control 2: merge-tree develop <merge commit> == the merge commit's tree (develop is its ancestor; nothing to merge)"
git -C "$CLONE" merge-tree --write-tree "$DEV" "$MERGE"; echo "$MTREE"
echo "== control 3: merge-tree develop <head> == head's tree"
git -C "$CLONE" merge-tree --write-tree "$DEV" "$HEAD"; git -C "$CLONE" rev-parse "${HEAD}^{tree}"
echo "== merge-base head develop / --is-ancestor develop head rc / rev-list --left-right --count develop...head"
git -C "$CLONE" merge-base "$HEAD" "$DEV"; git -C "$CLONE" merge-base --is-ancestor "$DEV" "$HEAD"; echo "rc=$?"; git -C "$CLONE" rev-list --left-right --count "${DEV}...${HEAD}"
echo "== the merge's parents / the fix's parent"
git -C "$CLONE" log -1 --format='%P' "$MERGE"; git -C "$CLONE" log -1 --format='%P' "$HEAD"
echo "done $(date '+%H:%M:%S %Z')"
