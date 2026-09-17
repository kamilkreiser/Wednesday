#!/bin/zsh
# bounds.sh — READ-ONLY checkout bounds reading (label as $1) for the #1019 drafter: porcelain, config sha, refs, worktrees, origin develop / pull/1019 head /
# branch / pull/1017 head, checkout branch, .vite readings (count newer than this set's git_read.sh, with a positive control of any age). stderr kept.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
echo "bounds $1 $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/develop refs/pull/1019/head refs/heads/feature/ks-1187-security-an-absolute-form-request-target-bypasses-the-ks-843 refs/pull/1017/head 2>&1
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD 2>&1) branch $(git -C "$R" rev-parse --abbrev-ref HEAD 2>&1) porcelain $(git -C "$R" --no-optional-locks status --porcelain 2>&1 | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref 2>&1 | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" 2>&1 | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list 2>&1 | wc -l | tr -d ' ')"
V="$R/Blockchain/Dev/services/api-gateway/node_modules/.vite"; S="$R/Blockchain/Dev/packages/shared/node_modules/.vite"; D="$R/Blockchain/Dev/node_modules/.vite"
echo "vite api-gateway results.json $(stat -f '%z %Sm' "$V/vitest/"*/results.json 2>&1) | shared .vite entries $(ls -laR "$S" 2>&1 | wc -l | tr -d ' ') | Dev .vite entries $(ls -laR "$D" 2>&1 | wc -l | tr -d ' ') | .vite entries newer than git_read.sh: $(find "$D" "$V" "$S" -newer "$GS/git_read.sh" 2>&1 | wc -l | tr -d ' ') | control (any age): $(find "$D" "$V" "$S" 2>&1 | wc -l | tr -d ' ')"
