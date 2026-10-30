#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-connector-xss.sh - its scan must not descend
# into node_modules.
# =============================================================================
# The scan is `grep -rEn ... connectors/ --include=...` and only AFTERWARDS drops every hit
# whose path names node_modules, so it reads every installed package under connectors/ first.
# Its siblings (check-no-default-passwords.sh, check-no-math-random.sh) pass
# --exclude-dir=node_modules to grep itself.
# grep is a stub on a private PATH: it logs every call's arguments, answers the scan call with
# the lines in SHIM_HITS, and hands the script's own `grep -vE` filter call to the real grep.
# No tree is ever walked.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_CONNECTOR_XSS_SH:-$HERE/../check-connector-xss.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-connector-xss.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/xss.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

mkdir -p "$WORK/bin" "$WORK/root/scripts" "$WORK/root/connectors"
cp "$SUBJ" "$WORK/root/scripts/check-connector-xss.sh"
cat > "$WORK/bin/grep" <<'STUB'
#!/bin/sh
echo "$*" >> "$SHIM_LOG"
for a in "$@"; do
  case "$a" in -v*) exec "$REAL_GREP" "$@" ;; esac
done
[ -n "${SHIM_HITS:-}" ] && printf '%s\n' "$SHIM_HITS"
exit 0
STUB
chmod +x "$WORK/bin/grep"

run_case() {   # $1 = name, $2 = the lines the scan call answers with -> prints rc; output in $WORK/$1.out, grep calls in $WORK/$1.log
  : > "$WORK/$1.log"
  (
    export PATH="$WORK/bin:/usr/bin:/bin" REAL_GREP SHIM_LOG="$WORK/$1.log" SHIM_HITS="$2"
    cd "$WORK/root" && bash scripts/check-connector-xss.sh
  ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_CLEAN="$(run_case clean "")"
RC_HIT="$(run_case hit $'connectors/a/src/a.js:1:const h = \'<a onclick="x()">\';')"
RC_DEP="$(run_case dep $'connectors/a/node_modules/y/index.js:9:h = \'<a onclick="x()">\';')"
SCAN_CALL="$("$REAL_GREP" -m1 -e '-rEn' "$WORK/clean.log")"

# CELL 1 (RED at the tip) - the scan call itself excludes node_modules.
if [[ -n "$SCAN_CALL" && "$SCAN_CALL" == *"--exclude-dir=node_modules"* ]]; then
  echo "PASS: the scan call carries --exclude-dir=node_modules"; PASS=$((PASS+1))
else
  echo "FAIL: the scan call does not exclude node_modules: $SCAN_CALL"; FAIL=$((FAIL+1))
fi

# CELL 2 (GREEN CONTROL, tip AND after) - the scan still reads the four file types under connectors/.
if [[ "$SCAN_CALL" == *"--include=*.js"* && "$SCAN_CALL" == *"--include=*.ts"* && "$SCAN_CALL" == *"--include=*.jsx"* \
   && "$SCAN_CALL" == *"--include=*.tsx"* && "$SCAN_CALL" == *"connectors/"* ]]; then
  echo "PASS: CONTROL the scan still reads .js, .ts, .jsx and .tsx under connectors/"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL scan call: $SCAN_CALL"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - a hit exits 1 and prints the line and the headline; clean exits 0.
if [[ "$RC_CLEAN" == "0" && "$RC_HIT" == "1" ]] && "$REAL_GREP" -qF 'use addEventListener' "$WORK/hit.out" \
   && "$REAL_GREP" -qF '  connectors/a/src/a.js:1:' "$WORK/hit.out"; then
  echo "PASS: CONTROL a hit exits 1 and is printed; a clean scan exits 0"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL exit codes: clean=$RC_CLEAN hit=$RC_HIT out=$(head -2 "$WORK/hit.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - a hit under node_modules is still dropped by the script's own filter.
if [[ "$RC_DEP" == "0" ]]; then
  echo "PASS: CONTROL a hit under node_modules is still filtered out"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL node_modules hit: rc=$RC_DEP $(head -2 "$WORK/dep.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

echo "check_connector_xss_skips_node_modules: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
