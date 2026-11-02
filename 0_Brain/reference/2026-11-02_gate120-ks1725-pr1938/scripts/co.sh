#!/bin/bash
# usage: co.sh <ref>
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938/repo
git -C $R checkout -q --detach "$1" && git -C $R rev-parse HEAD
