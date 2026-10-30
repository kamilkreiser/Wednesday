#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-dockerfile-non-root.sh - a Dockerfile that
# runs as root, or has no USER at all, must be REPORTED, not swallowed.
# =============================================================================
# Two faults on the last_user line. (1) With no USER directive `grep` exits 1, `pipefail`
# makes the command substitution fail and `set -e` ends the script silently: exit 1, no
# message, so the gate fails but names no file. (2) The `sed -E` uses `\s`, which BSD sed
# (macOS) does not know, so `USER root` is read as `USERroot`, never equals `root`, and the
# gate prints OK for a root container.
# Real tools, a private fixture tree; nothing outside the temp dir is read.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_DOCKERFILE_NON_ROOT_SH:-$HERE/../check-dockerfile-non-root.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-dockerfile-non-root.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/dfroot.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

run_case() {   # $1 = name, $2 = Dockerfile text -> prints rc; output in $WORK/$1.out
  local root="$WORK/$1"
  mkdir -p "$root/scripts" "$root/services/s" "$root/frontend" "$root/docker" "$root/connectors" "$root/deployment"
  cp "$SUBJ" "$root/scripts/check-dockerfile-non-root.sh"
  printf '%s' "$2" > "$root/services/s/Dockerfile"
  ( cd "$root" && bash scripts/check-dockerfile-non-root.sh ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_NOUSER="$(run_case nouser $'FROM node:20\nRUN true\n')"
RC_ROOT="$(run_case root $'FROM node:20\nUSER root\n')"
RC_APP="$(run_case app $'FROM node:20\nUSER app\n')"
RC_MULTI="$(run_case multi $'FROM node:20 AS build\nUSER root\nFROM node:20\nUSER app\n')"

# CELL 1 (RED at the tip) - no USER directive: exit 1 AND the file is named.
if [[ "$RC_NOUSER" == "1" ]] && "$REAL_GREP" -qF 'has NO USER directive' "$WORK/nouser.out" \
   && "$REAL_GREP" -qF 'services/s/Dockerfile' "$WORK/nouser.out"; then
  echo "PASS: a Dockerfile with no USER directive exits 1 and is named"; PASS=$((PASS+1))
else
  echo "FAIL: no-USER case: rc=$RC_NOUSER out=$(head -2 "$WORK/nouser.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip on a BSD/macOS userland) - a final USER root exits 1 and is named.
if [[ "$RC_ROOT" == "1" ]] && "$REAL_GREP" -qF "final USER is 'root'" "$WORK/root.out"; then
  echo "PASS: a final USER root exits 1 and is named"; PASS=$((PASS+1))
else
  echo "FAIL: USER root case: rc=$RC_ROOT out=$(head -2 "$WORK/root.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - a non-root USER passes.
if [[ "$RC_APP" == "0" ]] && "$REAL_GREP" -qF 'OK - all 1 Dockerfile' <(sed 's/ — / - /' "$WORK/app.out"); then
  echo "PASS: CONTROL USER app exits 0 with the OK line"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL USER app: rc=$RC_APP out=$(head -2 "$WORK/app.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - USER root in a build stage, non-root at the end, passes.
if [[ "$RC_MULTI" == "0" ]]; then
  echo "PASS: CONTROL a root build stage with a non-root final USER exits 0"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL multi-stage: rc=$RC_MULTI out=$(head -2 "$WORK/multi.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

echo "check_dockerfile_non_root_reports_root: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
