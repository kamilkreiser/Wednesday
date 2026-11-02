#!/bin/bash
# lock_key.sh <git repo> <commit-ish>  — print the deps LOCK KEY (2026-11-03).
# LOCK KEY = sha256 over the sorted lines "<path> <blob sha>" of every package.json and package-lock.json under
# Blockchain/Dev at that commit (git ls-tree -r; no checkout, no node_modules involved). Read-only. bash 3.2, no cd.
set -uo pipefail
[ $# -eq 2 ] || { echo "usage: lock_key.sh <repo> <commit>" >&2; exit 64; }
OUT="$(git -C "$1" ls-tree -r "$2" -- Blockchain/Dev)" || { echo "lock_key: ls-tree failed for $2 in $1" >&2; exit 1; }
LINES="$(printf '%s\n' "$OUT" | awk -F'\t' '{n=split($2,a,"/"); b=a[n]; if (b=="package.json"||b=="package-lock.json") {split($1,m," "); print $2" "m[3]}}' | LC_ALL=C sort)"
[ -n "$LINES" ] || { echo "lock_key: no package files under Blockchain/Dev at $2" >&2; exit 1; }
printf '%s\n' "$LINES" | shasum -a 256 | awk '{print $1}'
