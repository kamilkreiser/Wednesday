#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate157-ks1868-pr1974/repo
git -C $R checkout -q --detach ${1:-35f1842fa7dee22125ce5fa3ba0dafcc5e32d713}; echo "HEAD $(git -C $R rev-parse HEAD) status=$(git -C $R status --porcelain | wc -l)"
