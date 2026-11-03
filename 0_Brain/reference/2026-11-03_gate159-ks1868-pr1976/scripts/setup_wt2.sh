#!/bin/bash
# Round 2 environment. The Secuura checkout's installed node_modules are stale (zod 3.25.76; the tree wants ^4.6.7; the
# shared dist lacks boundedJson/zod3-compat), which load-fails 20 anchoring files at base, head and develop alike.
# These worktrees of MY clone link READ-ONLY to the fresh install in the author's own worktree s-r76-anchoring-recon
# (zod 4.6.7; @secuura/shared -> its packages/shared, whose tree edf16d9a is identical at base, head and develop).
set -e
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
F="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-r76-anchoring-recon"
for pair in "head:dba3a90a95c9fb6028d1529195ed0af464259158" "base:4d1ab2cb6574e2b221353ac3a1de56d515711aaf" "dev:66cbe4e52d5afadc9d13ca141200026cc68d5095" "red:4d1ab2cb6574e2b221353ac3a1de56d515711aaf" "c1:bdc1d4d8449e74a5be0b231fe9efb759078333e0" "mut:dba3a90a95c9fb6028d1529195ed0af464259158"; do
  n=${pair%%:*}; sha=${pair#*:}
  [ -d "$W/wt2_$n" ] || git -C "$W/repo" worktree add -q --detach "$W/wt2_$n" "$sha"
  for nm in Blockchain/Dev/node_modules Blockchain/Dev/services/anchoring/node_modules Blockchain/Dev/packages/shared/node_modules Blockchain/Dev/packages/shared/dist; do
    [ -e "$W/wt2_$n/$nm" ] || [ -L "$W/wt2_$n/$nm" ] || ln -s "$F/$nm" "$W/wt2_$n/$nm"
  done
  echo "wt2_$n at $(git -C "$W/wt2_$n" rev-parse HEAD)"
done
T=Blockchain/Dev/services/anchoring/src/__tests__
for f in ks1868-reconciler-catches-unreadable-throw.test.ts ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts; do
  git -C "$W/repo" show "dba3a90a:$T/$f" > "$W/wt2_red/$T/$f"
done
