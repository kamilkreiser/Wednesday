#!/bin/zsh
# close_read.sh — READ ONLY close reading of the Secuura checkout and the heads.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
echo "close_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/develop refs/pull/1008/head refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -c1-16) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
