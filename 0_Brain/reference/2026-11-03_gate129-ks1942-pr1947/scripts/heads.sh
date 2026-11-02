#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947/repo
date -u +%FT%TZ
git -C $R ls-remote origin refs/pull/1947/head refs/heads/develop
echo "local pr1947 $(git -C $R rev-parse refs/gate/pr1947)  develop $(git -C $R rev-parse refs/gate/develop) HEAD $(git -C $R rev-parse HEAD)"
git -C $R status --short | head -20
