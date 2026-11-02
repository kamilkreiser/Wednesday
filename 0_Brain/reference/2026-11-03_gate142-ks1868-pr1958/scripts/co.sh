#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958/repo
git -C $R checkout -q "$1" && git -C $R rev-parse HEAD
