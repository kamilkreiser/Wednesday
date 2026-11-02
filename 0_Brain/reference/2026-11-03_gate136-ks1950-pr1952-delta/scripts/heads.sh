#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta/repo
date -u +%FT%TZ
git -C $R ls-remote origin refs/pull/1952/head refs/heads/develop refs/pull/1953/head
echo "local pr1952 $(git -C $R rev-parse refs/gate/pr1952)  develop $(git -C $R rev-parse refs/gate/develop) HEAD $(git -C $R rev-parse HEAD)"
git -C $R status --short | head -20
