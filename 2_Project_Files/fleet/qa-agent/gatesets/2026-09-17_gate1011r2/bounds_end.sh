#!/bin/zsh
# bounds_end.sh — READ-ONLY close reading of the Secuura checkout counters + origin refs for the #1011 ROUND 2 drafter.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
echo "bounds_end $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/pull/1011/head refs/heads/develop
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "checkout .vite/.vitest/.cache entries newer than the drafter setup script: $(find "$R/Blockchain/Dev" -maxdepth 4 \( -name .vite -o -name .vitest -o -name .cache \) -prune -newer /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011r2/drafter_setup.py -print | wc -l | tr -d ' ') (control, any age: $(find "$R/Blockchain/Dev" -maxdepth 4 \( -name .vite -o -name .vitest -o -name .cache \) -prune -print | wc -l | tr -d ' '))"
