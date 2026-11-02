#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955/repo
git -C $R fetch origin develop 2>&1 | tail -2; echo "origin/develop $(git -C $R rev-parse origin/develop)"
git -C $R log --format='%h %s' 8150eeb3802b..origin/develop
echo "paths 8150eeb3..new: $(git -C $R diff --name-only 8150eeb3802b origin/develop | wc -l)"
git -C $R diff --name-only 8150eeb3802b origin/develop | grep -i -E "services/anchoring/|originate/src/routes/anchors|fragments/.*anchors-message" || echo "none in anchoring/ or originate anchors.ts (positive control: count above)"
