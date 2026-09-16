#!/bin/zsh
# bounds_end.sh — #1007 drafter: heads at origin + Secuura checkout readings, read verbs only.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
echo "bounds $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-864-ornith-dead-estate-pointers refs/pull/1007/head refs/heads/develop
echo "checkout porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ')"
