#!/bin/bash
# (C) F2-limit census at the head, product code (services/*/src, packages/shared/src, frontend excluded, tests excluded). Case-insensitive, with positive controls.
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta/repo; H=928ee20c84dc
P=( 'Blockchain/Dev/services/*/src/**' 'Blockchain/Dev/packages/*/src/**' )
filt() { grep -v -E '__tests__|\.test\.ts|\.spec\.ts|/frontend/'; }
c() { echo "[$1] $(git -C $R grep -i -n -E "$2" $H -- "${P[@]}" | filt | wc -l | tr -d ' ')"; git -C $R grep -i -n -E "$2" $H -- "${P[@]}" | filt | sed 's/^/    /' | cut -c1-220 | head -${3:-12}; }
c 'z.intersection(' 'z\.intersection\s*\('
c '.and(' '\.and\s*\('
c 'addIssue anywhere' 'addIssue\s*\(' 40
c 'too_small / too_big as an issue code literal' "code:\s*['\"](too_small|too_big)['\"]|ZodIssueCode\.(too_small|too_big)"
c 'invalid_type as an issue code literal (custom)' "code:\s*['\"]invalid_type['\"]|ZodIssueCode\.invalid_type"
c '.merge( on a z chain' 'z\.object\(.*\.merge\s*\(|Schema\.merge\s*\('
c 'z.preprocess(' 'z\.preprocess\s*\('
c '.pipe(' '\.pipe\s*\(' 20
echo "CONTROLS (must be > 0):"
c 'control z.union(' 'z\.union\s*\(' 2
c 'control .superRefine(' '\.superRefine\s*\(' 2
c 'control: the same census on the TESTS finds intersections? (info)' 'z\.intersection\s*\(' 2
echo "intersection/and in tests (unfiltered):"; git -C $R grep -i -n -E 'z\.intersection\s*\(|\.and\s*\(\s*z\.' $H -- 'Blockchain/Dev' | grep -E '__tests__|\.test\.' | head -5
