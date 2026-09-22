#!/bin/bash
# checkout_counts.sh <out> — READ verbs only against the Secuura checkout (gate19C shape)
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
{
echo "READ $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "porcelain non-untracked: $(git -C "$R" status --porcelain 2>/dev/null | grep -v '^??' | wc -l | tr -d ' ')"
echo "porcelain total: $(git -C "$R" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
echo "worktrees: $(ls "$R/.git/worktrees" 2>/dev/null | wc -l | tr -d ' ')"
echo "for-each-ref: $(git -C "$R" for-each-ref | wc -l | tr -d ' ')"
git -C "$R" count-objects -v
echo "config sha256: $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1)"
echo "HEAD: $(git -C "$R" rev-parse --abbrev-ref HEAD) $(git -C "$R" rev-parse --short=9 HEAD)"
git -C "$R" config --get remote.origin.url
} > "$1" 2>&1
