#!/bin/bash
# predict_merge_scratch.sh — predict #1105's merged tree over the MOVED develop 778e6cfe2 by a REAL 3-way merge in a --shared --no-checkout clone
# in the drafter's scratchpad (git write verbs THERE only; the Secuura checkout is read-only). Controls: merge-base = dc061f2bb; the head alone
# over the OLD develop = the head tree (fast-forward, 8f066a817); a read-tree back to develop returns develop's tree; the merged tree differs from
# both parents; the merged tree's 12 #1105 paths carry the head blobs and the 4 squash paths carry develop's blobs.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
OLD=dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa; NEW=778e6cfe2b6061d60ffcf3a57a951c84dc152b67; HEAD=e02d3ecb51a457b0eb490db1854f28c6b1af69ad
S=$(mktemp -d "$1/predict1105-XXXXXX"); echo "scratch $S"; date -u '+%Y-%m-%dT%H:%M:%SZ'
git clone --quiet --shared --no-checkout "$REPO" "$S/c" ; echo "clone rc=$?"
C="$S/c"
for o in $OLD $NEW $HEAD; do git -C "$C" cat-file -e $o^{commit} && echo "object $o present"; done
echo "merge-base new-develop..head: $(git -C "$C" merge-base $NEW $HEAD) (want $OLD)"
echo "behind/ahead (rev-list --left-right --count $NEW...$HEAD): $(git -C "$C" rev-list --left-right --count $NEW...$HEAD)"
M=$(git -C "$C" merge-tree --write-tree $NEW $HEAD); rc=$?; echo "merge-tree --write-tree develop(778e6cfe2) x head rc=$rc (0 = clean, 1 = conflicts)"; echo "MERGED TREE $M"
M2=$(git -C "$C" merge-tree --write-tree $HEAD $NEW); echo "reverse order tree $M2 | same: $([ "$M" = "$M2" ] && echo True || echo False)"
FF=$(git -C "$C" merge-tree --write-tree $OLD $HEAD); echo "CONTROL head over OLD develop: $FF == head tree $(git -C "$C" rev-parse $HEAD^{tree}): $([ "$FF" = "$(git -C "$C" rev-parse $HEAD^{tree})" ] && echo True || echo False)"
echo "CONTROL merged differs from develop tree $(git -C "$C" rev-parse $NEW^{tree}): $([ "$M" != "$(git -C "$C" rev-parse $NEW^{tree})" ] && echo True || echo False); from head tree: $([ "$M" != "$(git -C "$C" rev-parse $HEAD^{tree})" ] && echo True || echo False)"
echo "--- merged tree vs new develop: name-status (want exactly #1105's 12 paths)"; git -C "$C" diff --name-status $NEW^{tree} $M
echo "count $(git -C "$C" diff --name-only $NEW^{tree} $M | wc -l | tr -d ' ')"
echo "--- merged tree vs head: name-status (want exactly the 4 squash paths)"; git -C "$C" diff --name-status $HEAD^{tree} $M
echo "--- blob checks in the merged tree"
ok=1
for p in $(git -C "$C" diff --name-only $OLD $HEAD); do a=$(git -C "$C" rev-parse "$M:$p"); b=$(git -C "$C" rev-parse "$HEAD:$p"); [ "$a" = "$b" ] || { echo "MISMATCH $p"; ok=0; }; done; echo "12 #1105 paths carry the head blobs: $([ $ok = 1 ] && echo True || echo False)"
ok=1
for p in $(git -C "$C" diff --name-only $OLD $NEW); do a=$(git -C "$C" rev-parse "$M:$p"); b=$(git -C "$C" rev-parse "$NEW:$p"); [ "$a" = "$b" ] || { echo "MISMATCH $p"; ok=0; }; done; echo "4 squash paths carry develop's blobs: $([ $ok = 1 ] && echo True || echo False)"
export GIT_INDEX_FILE="$S/idx"; git -C "$C" read-tree $NEW; echo "CONTROL read-tree back to develop -> $(git -C "$C" write-tree) == $(git -C "$C" rev-parse $NEW^{tree})"
echo "checkout porcelain (read): $(git -C "$REPO" status --porcelain | wc -l | tr -d ' ') | .git/worktrees: $(ls "$REPO/.git/worktrees" | wc -l | tr -d ' ')"
date -u '+%Y-%m-%dT%H:%M:%SZ'
