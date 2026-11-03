#!/bin/bash
# Worktrees of MY clone (never the Secuura checkout) + read-only node_modules symlinks to the checkout's installs.
set -e
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
R=$W/repo
O="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
for pair in "head:dba3a90a95c9fb6028d1529195ed0af464259158" "base:4d1ab2cb6574e2b221353ac3a1de56d515711aaf" "dev:66cbe4e52d5afadc9d13ca141200026cc68d5095"; do
  n=${pair%%:*}; sha=${pair#*:}
  [ -d "$W/wt_$n" ] || git -C "$R" worktree add -q --detach "$W/wt_$n" "$sha"
  echo "wt_$n at $(git -C "$W/wt_$n" rev-parse HEAD)"
  for nm in node_modules Blockchain/Dev/node_modules Blockchain/Dev/services/node_modules Blockchain/Dev/services/anchoring/node_modules Blockchain/Dev/packages/shared/node_modules; do
    [ -e "$W/wt_$n/$nm" ] || ln -s "$O/$nm" "$W/wt_$n/$nm"
  done
  # shared dist is gitignored: link the checkout's built dist (same for base/head/dev; PR does not touch shared)
  [ -e "$W/wt_$n/Blockchain/Dev/packages/shared/dist" ] || ln -s "$O/Blockchain/Dev/packages/shared/dist" "$W/wt_$n/Blockchain/Dev/packages/shared/dist"
done
