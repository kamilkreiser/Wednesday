#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-no-strictness-patches.sh - the scan must not
# read installed packages.
# =============================================================================
# The scan is `grep -rEn --include=Dockerfile* --include=*.sh --include=*.yml ... services frontend
# scripts deployment` with no --exclude-dir, and nothing filters node_modules afterwards, so a
# vendored package that mentions the flip makes the gate fail for code the repo does not own, and
# every installed tree is read on each run. Its siblings pass --exclude-dir=node_modules.
# Real tools, a private fixture tree; nothing outside the temp dir is read.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_NO_STRICTNESS_PATCHES_SH:-$HERE/../check-no-strictness-patches.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-strictness-patches.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/strict.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

run_case() {   # $1 = name, $2 = 1 to plant a hit in a nested node_modules, $3 = 1 to plant a real hit -> prints rc
  local root="$WORK/$1"
  mkdir -p "$root/scripts" "$root/services/s" "$root/frontend" "$root/deployment"
  cp "$SUBJ" "$root/scripts/check-no-strictness-patches.sh"
  if [[ "$2" == "1" ]]; then
    mkdir -p "$root/services/s/node_modules/dep/node_modules/deeper"
    printf 'x: noUnusedLocals = false\n' > "$root/services/s/node_modules/dep/node_modules/deeper/ci.yml"
  fi
  if [[ "$3" == "1" ]]; then
    printf 'RUN sed -i x && noUnusedLocals = false\n' > "$root/services/s/Dockerfile"
  fi
  ( cd "$root" && bash scripts/check-no-strictness-patches.sh ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_DEP="$(run_case dep 1 0)"
RC_REAL="$(run_case real 0 1)"
RC_CLEAN="$(run_case clean 0 0)"
RC_BOTH="$(run_case both 1 1)"

# CELL 1 (RED at the tip) - a hit only inside node_modules is not the repo's code: exit 0.
if [[ "$RC_DEP" == "0" ]] && "$REAL_GREP" -qF 'no TS-strictness flips found' <(sed 's/ — / - /' "$WORK/dep.out") ; then
  echo "PASS: a flip that exists only under node_modules is ignored"; PASS=$((PASS+1))
else
  echo "FAIL: node_modules-only hit: rc=$RC_DEP out=$(head -3 "$WORK/dep.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - with a real hit and a node_modules hit, only the real one is printed.
if [[ "$RC_BOTH" == "1" ]] && "$REAL_GREP" -qF 'services/s/Dockerfile:1:' "$WORK/both.out" \
   && ! "$REAL_GREP" -qF 'node_modules' "$WORK/both.out"; then
  echo "PASS: only the repo's own hit is printed"; PASS=$((PASS+1))
else
  echo "FAIL: mixed hits: rc=$RC_BOTH out=$(head -4 "$WORK/both.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - a real hit exits 1 and prints the error and the file.
if [[ "$RC_REAL" == "1" ]] && "$REAL_GREP" -qF 'Found banned TS-strictness flip' "$WORK/real.out" \
   && "$REAL_GREP" -qF 'services/s/Dockerfile:1:' "$WORK/real.out"; then
  echo "PASS: CONTROL a real flip exits 1 and is printed"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL real hit: rc=$RC_REAL out=$(head -3 "$WORK/real.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - a clean tree exits 0.
if [[ "$RC_CLEAN" == "0" ]]; then
  echo "PASS: CONTROL a clean tree exits 0"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL clean: rc=$RC_CLEAN out=$(head -3 "$WORK/clean.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

echo "check_no_strictness_patches_skips_node_modules: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
