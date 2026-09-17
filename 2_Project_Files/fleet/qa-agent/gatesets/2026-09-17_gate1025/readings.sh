#!/bin/bash
# read-only readings of the Secuura checkout + origin (drafter 1025)
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
date '+%Y-%m-%d %H:%M:%S %Z'
echo "porcelain $(git -C "$R" status --porcelain 2>&1 | wc -l | tr -d ' ')"
echo "config sha256 $(shasum -a 256 "$R/.git/config" | cut -c1-16)"
echo "refs $(git -C "$R" for-each-ref 2>&1 | wc -l | tr -d ' ')"
echo "git/worktrees entries $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
git -C "$R" ls-remote origin refs/heads/develop refs/pull/1025/head refs/heads/chore/audit-redate-react-router-rows-v7-landing 2>&1
for s in 9954a7069a16987da140654337555c9a13268b1f efaaa6034; do echo "cat-file $s: $(git -C "$R" cat-file -t $s 2>&1)"; done
