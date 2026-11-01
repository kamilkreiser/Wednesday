#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911; R=$G/repo; D=$G/merged_docs
[ -e $D ] && { echo "exists"; exit 1; }; mkdir -p $D
git -C $R archive -o $G/logs/merged_docs.tar 98141d38621612ad779b101ab8bd999fb05c1756 "Projects Documents" Blockchain/Dev/scripts/docs-fragments.mjs systemTest/__tests__/support; echo "archive rc=$?"
tar -x -C $D -f $G/logs/merged_docs.tar; echo "tar rc=$?"
nice -n 10 node $D/Blockchain/Dev/scripts/docs-fragments.mjs check --root $D; echo "rc=$?"
