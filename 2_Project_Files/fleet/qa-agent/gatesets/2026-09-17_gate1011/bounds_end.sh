#!/bin/zsh
# bounds_end.sh — READ-ONLY close reading of the Secuura checkout counters + origin refs for the #1011 drafter.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
echo "bounds_end $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/pull/1011/head refs/heads/develop
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(git -C "$R" worktree list | wc -l | tr -d ' ')"
