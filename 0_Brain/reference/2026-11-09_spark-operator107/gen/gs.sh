#!/bin/bash
# gs.sh <path-under-Blockchain/Dev> [start end]  -- read-only show at origin/develop of the spark cache
f="$1"; s="${2:-1}"; e="${3:-100000}"
git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src show "origin/develop:Blockchain/Dev/$f" | awk -v s="$s" -v e="$e" 'NR>=s && NR<=e {printf "%d:%s\n", NR, $0}'
