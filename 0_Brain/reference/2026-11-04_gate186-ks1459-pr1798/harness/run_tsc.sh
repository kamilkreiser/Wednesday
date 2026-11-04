#!/bin/bash
# Gate 186: tsc --noEmit over the auth service (and its test config), cwd inside the workdir.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate186-ks1459-pr1798
A=$G/repo/Blockchain/Dev/services/auth
L=$1
cd "$G/cwd" || exit 9
env -i PATH="$PATH" HOME="$G/home" TMPDIR="$G/tmp" "$G/repo/Blockchain/Dev/node_modules/.bin/tsc" -p "$A/tsconfig.json" --noEmit > "$G/runs/tsc_$L.out" 2>&1
echo "$L tsc rc=$? errors=$(/usr/bin/grep -c 'error TS' "$G/runs/tsc_$L.out")"
