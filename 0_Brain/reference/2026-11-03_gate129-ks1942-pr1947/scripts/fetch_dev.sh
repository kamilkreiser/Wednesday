#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947/repo
git -C $R fetch -q origin +refs/heads/develop:refs/gate/develop2; echo "fetch rc=$?"; git -C $R rev-parse refs/gate/develop2
