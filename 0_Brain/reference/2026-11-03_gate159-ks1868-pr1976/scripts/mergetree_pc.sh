#!/bin/bash
# Positive control for the merge-tree instrument, by git merge-file on scratch copies under logs/_pc (replaces the
# failed mktree attempt in mergetree.sh, whose control section errored: `git mktree` takes a non-recursive listing).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
R=$W/repo; PC=$W/logs/_pc; mkdir -p "$PC"
g() { git -C "$R" "$@"; }
D=66cbe4e52d5afadc9d13ca141200026cc68d5095; H=dba3a90a95c9fb6028d1529195ed0af464259158; MB=4d1ab2cb6574e2b221353ac3a1de56d515711aaf
for F in Blockchain/Dev/services/anchoring/src/reconciler.ts Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts; do
  b=$(basename "$F")
  g show "$MB:$F" > "$PC/$b.base"; g show "$H:$F" > "$PC/$b.head"
  g show "$D:$F" > "$PC/$b.dev_real"
  cp "$PC/$b.dev_real" "$PC/$b.merged_real"
  git merge-file -p "$PC/$b.merged_real" "$PC/$b.base" "$PC/$b.head" > "$PC/$b.out_real"; echo "$b real: conflicts=$?  out==head: $(cmp -s "$PC/$b.out_real" "$PC/$b.head" && echo yes || echo no)"
  # control: develop edits the very line the PR rewrites
  sed -E "s/error: err\?\.message( \}\);|,$)/error: String(err)\1/" "$PC/$b.dev_real" > "$PC/$b.dev_ctl"
  cmp -s "$PC/$b.dev_ctl" "$PC/$b.dev_real" && echo "$b CONTROL EDIT DID NOT APPLY"
  git merge-file -p "$PC/$b.dev_ctl" "$PC/$b.base" "$PC/$b.head" > "$PC/$b.out_ctl"; echo "$b control: conflicts=$?"
done
