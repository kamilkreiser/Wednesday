#!/bin/bash
# G189: for every PR head NOT an ancestor of develop, list migrations/NNN_*.sql it ADDS relative to its merge-base.
# Superset of open PRs (closed-unmerged and squash-merged heads also appear). Prints "pr<TAB>file".
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate189-ks1256-pr2001/repo
DEV=refs/gate/develop
git -C "$R" for-each-ref --format='%(refname)' refs/gate/pr | while read -r ref; do
  n=${ref##*/}
  git -C "$R" merge-base --is-ancestor "$ref" "$DEV" && continue
  mb=$(git -C "$R" merge-base "$ref" "$DEV") || continue
  git -C "$R" diff --name-only --diff-filter=A "$mb" "$ref" -- Blockchain/Dev/migrations/ | grep -E '/[0-9]{3}_[^/]*\.sql$' | sed "s|^|$n\t|"
done
