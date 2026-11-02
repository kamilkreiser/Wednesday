#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930/repo
git -C $R fetch origin develop:develop_end 2>&1; git -C $R rev-parse develop_end
git -C $R log --oneline c2c2e03afdb3..develop_end
