#!/bin/bash
# Gate 187 runner. usage: run_suite.sh <base|head|/abs/vc-issuer-dir> <outfile> [vitest args...]
# Starts vitest with its CWD inside the workdir (cwd/), anchored by --root, under env -i.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate187-ks1868-pr1968
T="$1"; OUT="$2"; shift 2
case "$T" in /*) D="$T";; *) D="$W/scratch/$T/Blockchain/Dev/services/vc-issuer";; esac
NODEDIR="$(dirname "$(command -v node)")"
mkdir -p "$W/cwd" "$W/home" "$W/tmp"
builtin cd "$W/cwd" || exit 99
env -i PATH="$NODEDIR:/usr/bin:/bin" HOME="$W/home" TMPDIR="$W/tmp" CI=1 NODE_ENV=test \
  "$W/scratch/head/Blockchain/Dev/node_modules/.bin/vitest" run --root "$D" --reporter=verbose "$@" > "$OUT" 2>&1
echo "rc=$?" >> "$OUT"
