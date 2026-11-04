#!/bin/bash
# usage: run_tsc.sh <base|head> <tsconfig name> <outfile>
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate187-ks1868-pr1968
case "$1" in /*) D="$1";; *) D="$W/scratch/$1/Blockchain/Dev/services/vc-issuer";; esac
NODEDIR="$(dirname "$(command -v node)")"
builtin cd "$W/cwd" || exit 99
env -i PATH="$NODEDIR:/usr/bin:/bin" HOME="$W/home" TMPDIR="$W/tmp" \
  "$W/scratch/head/Blockchain/Dev/node_modules/.bin/tsc" -p "$D/$2" --noEmit --incremental false > "$3" 2>&1
echo "rc=$?" >> "$3"
