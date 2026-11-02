#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta/repo; F=Blockchain/Dev/services/anchoring/src/index.ts
MB=$(git -C $R merge-base 473ef1e01bb2 2d3b3bb3d386); echo "merge-base of the 2nd merge's parents: $MB"
echo "files PR 1955 changed (mb..2d3b3bb3):"; git -C $R diff --name-only $MB 2d3b3bb3d386
echo "files both sides changed:"; comm -12 <(git -C $R diff --name-only $MB 473ef1e01bb2|sort) <(git -C $R diff --name-only $MB 2d3b3bb3d386|sort)
echo "THIS BRANCH hunks on index.ts (old-line start,count):"; git -C $R diff -U0 $MB 473ef1e01bb2 -- $F | grep '^@@' | sed -E 's/^@@ -([0-9,]+) .*/\1/' | tr '\n' ' '; echo
echo "PR 1955 hunks on index.ts:"; git -C $R diff -U0 $MB 2d3b3bb3d386 -- $F | grep '^@@' | sed -E 's/^@@ -([0-9,]+) .*/\1/' | tr '\n' ' '; echo
