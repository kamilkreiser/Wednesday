#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-no-pii-store.sh - its second (untracked) leg must work
# and must stay a WARNING.
# =============================================================================
# Two faults. (1) `git ls-files --others --exclude-standard=false` is not a valid option
# (`--exclude-standard` takes no value): git exits 129, `|| true` hides it, UNTRACKED is always
# empty, and an untracked pii-data.local.json is never reported although the header promises the
# whole family. (2) Once (1) works, `{ [ -n UNTRACKED ] && echo ...; [ -n FOUND ] && echo ...; }` ends
# on a failing test when only UNTRACKED is set, so `set -e` + `pipefail` exit the script with 1
# in the middle of a "Warning, not a failure" block.
# Real git and a private fixture repo in a temp dir; nothing outside it is read.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_NO_PII_STORE_SH:-$HERE/../check-no-pii-store.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-pii-store.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/pii.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

run_case() {   # $1 = name, $2 = file to plant (relative to Blockchain/Dev, "" for none), $3 = 1 to git-add it, $4 = 1 to gitignore it
  local root="$WORK/$1"
  mkdir -p "$root/Blockchain/Dev/scripts"
  cp "$SUBJ" "$root/Blockchain/Dev/scripts/check-no-pii-store.sh"
  git -C "$root" init -q
  if [[ -n "$2" ]]; then
    echo '{}' > "$root/Blockchain/Dev/$2"
    [[ "$4" == "1" ]] && echo "$2" > "$root/Blockchain/Dev/.gitignore"
    [[ "$3" == "1" ]] && git -C "$root" add "Blockchain/Dev/$2"
  fi
  ( cd "$root" && bash Blockchain/Dev/scripts/check-no-pii-store.sh ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_UNTR="$(run_case untr pii-data.local.json 0 0)"
RC_TRACKED="$(run_case tracked pii-data.json 1 0)"
RC_CLEAN="$(run_case clean "" 0 0)"
RC_IGN="$(run_case ign ks256-pii-data.json 0 1)"

# CELL 1 (RED at the tip) - an untracked, not-ignored pii variant is reported by name.
if "$REAL_GREP" -qF 'WARNING (KS-256)' "$WORK/untr.out" && "$REAL_GREP" -qF 'pii-data.local.json' "$WORK/untr.out"; then
  echo "PASS: an untracked pii-data.local.json is reported"; PASS=$((PASS+1))
else
  echo "FAIL: untracked variant not reported: out=$(head -3 "$WORK/untr.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - that report is a warning: exit 0 and the closing line is printed.
if [[ "$RC_UNTR" == "0" ]] && "$REAL_GREP" -qF 'Warning, not a failure' "$WORK/untr.out"; then
  echo "PASS: the untracked-file report exits 0 and prints its full block"; PASS=$((PASS+1))
else
  echo "FAIL: untracked variant: rc=$RC_UNTR out=$(tail -2 "$WORK/untr.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - a tracked pii file exits 1 with the ERROR and the git rm hint.
if [[ "$RC_TRACKED" == "1" ]] && "$REAL_GREP" -qF 'ERROR (KS-256)' "$WORK/tracked.out" \
   && "$REAL_GREP" -qF 'git rm --cached Blockchain/Dev/pii-data.json' "$WORK/tracked.out"; then
  echo "PASS: CONTROL a tracked pii file exits 1 with the git rm hint"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL tracked: rc=$RC_TRACKED out=$(head -3 "$WORK/tracked.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - a clean repo exits 0 with the OK line and no warning.
if [[ "$RC_CLEAN" == "0" ]] && "$REAL_GREP" -qF 'no PII store file is tracked' "$WORK/clean.out" \
   && ! "$REAL_GREP" -qF 'WARNING' "$WORK/clean.out"; then
  echo "PASS: CONTROL a clean repo exits 0 with no warning"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL clean: rc=$RC_CLEAN out=$(head -3 "$WORK/clean.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 5 (GREEN CONTROL, tip AND after) - an IGNORED ks256 store is still found by the filesystem leg, exit 0.
if [[ "$RC_IGN" == "0" ]] && "$REAL_GREP" -qF 'ks256-pii-data.json' "$WORK/ign.out"; then
  echo "PASS: CONTROL an ignored ks256 store is still warned about, exit 0"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL ignored store: rc=$RC_IGN out=$(head -3 "$WORK/ign.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

echo "check_no_pii_store_untracked_leg: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq 5 ]]
