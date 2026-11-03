#!/bin/bash
# Red-first: base product + the PR's two new test files (head versions), in a separate worktree wt_red of MY clone.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
O="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
if [ ! -d "$W/wt_red" ]; then
  git -C "$W/repo" worktree add -q --detach "$W/wt_red" 4d1ab2cb6574e2b221353ac3a1de56d515711aaf
  for nm in node_modules Blockchain/Dev/node_modules Blockchain/Dev/services/node_modules Blockchain/Dev/services/anchoring/node_modules Blockchain/Dev/packages/shared/node_modules Blockchain/Dev/packages/shared/dist; do
    ln -s "$O/$nm" "$W/wt_red/$nm"
  done
fi
T=Blockchain/Dev/services/anchoring/src/__tests__
for f in ks1868-reconciler-catches-unreadable-throw.test.ts ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts; do
  git -C "$W/repo" show "dba3a90a:$T/$f" > "$W/wt_red/$T/$f"
done
git -C "$W/wt_red" status --short
bash "$W/scripts/vt.sh" red redfirst src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts
