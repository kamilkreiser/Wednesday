#!/bin/bash
# swap.sh base|head : write the 4 product route files from git objects into the worktree, print sha
set -e
REPO=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate113-ks1868-pr1931/repo
case "$1" in base) REF=968f17070208efc1e888308bdea49de5112a42e8;; head) REF=bafab56a1edc99eac9b80bd74c402917f3a14cf5;; *) echo usage; exit 2;; esac
for f in auth internal issuerCerts oauth; do
  P=Blockchain/Dev/services/auth/src/routes/$f.ts
  git -C "$REPO" show "$REF:$P" > "$REPO/$P"
  echo "$1 $f $(shasum -a 256 "$REPO/$P" | cut -c1-12) blob=$(git -C "$REPO" rev-parse "$REF:$P" | cut -c1-8) wt=$(git -C "$REPO" hash-object "$REPO/$P" | cut -c1-8)"
done
