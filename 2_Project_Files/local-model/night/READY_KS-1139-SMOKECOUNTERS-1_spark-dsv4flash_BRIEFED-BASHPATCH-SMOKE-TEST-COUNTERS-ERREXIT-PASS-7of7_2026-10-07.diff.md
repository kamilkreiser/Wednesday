# READY — KS-1139 smoke-test counters (Spark DeepSeek V4 Flash, briefed, bash_patch, rung 1) — PASS 7/7 — HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1139-smoke-test-counters-errexit/out.md.checker/patch.diff`. BYTE-IDENTICAL to the brief's golden `night/briefs/KS-1139-smoke-test-counters-errexit/golden.diff` (git headers stripped, `cmp -s` rc 0; control against the KS-1410-notifications golden rc 1, measured by Wednesday).

**Held BY HAND 00:09 2026-10-08 by Wednesday (late-evening seat)** — `hold_ready.py` refuses `--model-tag` off the code_patch path (OWED). Every verdict line below is COPIED from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1139-smoke-test-counters-errexit/checker.out` by script, not typed. Refs KS-1139 (Peter's 10-07 10:05Z carve) and KS-1148; closes neither. NOT an auth surface (counters only; test runs `--quick` against a stub curl). UNMEASURED: bash >= 4.1 (host has 3.2 only); whether `smoke_test_degraded_warns` goes green on the Linux runner after this (Peter: a second failure may sit behind the first). Collides with nothing open; the held `READY_KS-1250` edits the same file at `:15` (disjoint hunk).

## Checker verdict lines (verbatim)
- PASS B0 subject: clone at 2c27ddfeef519599407682c89a28c275d7bc3559, Blockchain/Dev/scripts/smoke-test.sh and Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh present
- PASS B1 output is exactly one fenced ```diff block
- PASS B2 every section applies at the tip (strict)
- PASS B3 touched-file set == { Blockchain/Dev/scripts/smoke-test.sh , Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh (new) }
- PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'
- PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh fails at the untouched tip (rc=1, 3 FAIL line(s))
- PASS B5a the script parses after the hunk (bash -n)
- PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 6 pass line(s))
- PASS B6 sibling suite(s) that drive smoke-test.sh: no NEW failure after (1 suite(s))
- RESULT: PASS (7/7)
- PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)

## The patch
```diff
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh
@@ -0,0 +1,102 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/smoke-test.sh - the pass/fail/warn counters
+# must not return a failure status when they count from zero
+# =============================================================================
+# The defect: pass(), fail() and warn() counted with `((PASS++))`. A post-
+# increment from 0 evaluates to 0, so the arithmetic command returns status 1.
+# smoke-test.sh runs under `set -euo pipefail`; bash 4.1 and later apply errexit
+# to `(( ))`, so on the Linux CI runner (bash 5.2) the script died at its FIRST
+# check and printed nothing after it. macOS /bin/bash 3.2 ignores that status,
+# which is why it passed locally.
+#
+# The RED cells read each helper's counter statement out of smoke-test.sh and
+# run it from a zero counter: it must return 0 AND leave the counter at 1.
+# That status is measurable on bash 3.2 too, so these cells are red on any host.
+# curl is NEVER run here (no stack, no network): the CONTROL runs use a STUB
+# curl on a private PATH, in the shape of smoke_test_degraded_warns.test.sh.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SMOKE="$REPO_ROOT/Blockchain/Dev/scripts/smoke-test.sh"
+[ -f "$SMOKE" ] || { echo "FATAL: smoke-test.sh not found at $SMOKE" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/smokectr.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# The first statement of a one-line helper `name() { <stmt>; ... }` in smoke-test.sh.
+first_stmt() { sed -n "s/^$1() { \([^;]*\);.*/\1/p" "$SMOKE"; }
+
+# Run a counter statement from a zero counter. Prints "<rc> <counter after>".
+step_from_zero() {
+  local var="$1" stmt="$2"
+  bash -c "$var=0; $stmt
+rc=\$?; printf '%s %s' \"\$rc\" \"\$$var\""
+}
+
+# CONTROL - each helper is defined exactly once, on one line, and its first statement names its own counter.
+got="$(grep -c '^pass() { ' "$SMOKE") $(grep -c '^fail() { ' "$SMOKE") $(grep -c '^warn() { ' "$SMOKE") $(first_stmt pass | grep -c 'PASS') $(first_stmt fail | grep -c 'FAIL') $(first_stmt warn | grep -c 'WARN')"
+if [ "$got" = "1 1 1 1 1 1" ]; then ok "CONTROL - pass/fail/warn are each defined once and each counts its own counter first"; else bad "CONTROL - pass/fail/warn are each defined once and each counts its own counter first" "want 1 1 1 1 1 1, got $got"; fi
+
+# RED - pass()'s counter statement from PASS=0: status 0, PASS=1.
+got="$(step_from_zero PASS "$(first_stmt pass)")"
+if [ "$got" = "0 1" ]; then ok "RED pass() counts from zero with status 0 (errexit-safe)"; else bad "RED pass() counts from zero with status 0 (errexit-safe)" "want 0 1, got $got (statement: $(first_stmt pass))"; fi
+
+# RED - fail()'s counter statement from FAIL=0: status 0, FAIL=1.
+got="$(step_from_zero FAIL "$(first_stmt fail)")"
+if [ "$got" = "0 1" ]; then ok "RED fail() counts from zero with status 0 (errexit-safe)"; else bad "RED fail() counts from zero with status 0 (errexit-safe)" "want 0 1, got $got (statement: $(first_stmt fail))"; fi
+
+# RED - warn()'s counter statement from WARN=0: status 0, WARN=1.
+got="$(step_from_zero WARN "$(first_stmt warn)")"
+if [ "$got" = "0 1" ]; then ok "RED warn() counts from zero with status 0 (errexit-safe)"; else bad "RED warn() counts from zero with status 0 (errexit-safe)" "want 0 1, got $got (statement: $(first_stmt warn))"; fi
+
+# A /health/deep body with the five services at the given statuses.
+deep_body() {
+  printf '{"ready":true,"status":"x","checks":{"redis":{"status":"%s","latencyMs":1},"postgres":{"status":"%s","latencyMs":2},"auth":{"status":"%s","latencyMs":3},"originate":{"status":"%s","latencyMs":4},"anchoring":{"status":"%s","latencyMs":5}}}' "$1" "$2" "$3" "$4" "$5"
+}
+
+# Build a fixture: $1 = dir, $2 = the /health/deep body the stub curl returns.
+build_fixture() {
+  local root="$1" deep="$2"
+  rm -rf "$root"; mkdir -p "$root/bin"
+  printf '%s' "$deep" > "$root/deep.json"
+  sed "s#@ROOT@#$root#g" > "$root/bin/curl" <<'STUB'
+#!/bin/bash
+for a in "$@"; do
+  case "$a" in */health/deep) cat "@ROOT@/deep.json"; exit 0 ;; esac
+done
+for a in "$@"; do [ "$a" = "-w" ] && { printf '200'; exit 0; }; done
+exit 0
+STUB
+  chmod +x "$root/bin/curl"
+}
+
+# Run the smoke test in --quick mode with the stub curl first on PATH. Prints rc.
+run_smoke() {
+  local root="$1"
+  ( export PATH="$root/bin:$PATH"; bash "$SMOKE" --quick ) > "$root/out.txt" 2>&1
+  echo $?
+}
+count() { grep -c -F "$2" "$1/out.txt"; }
+
+# CONTROL - auth 'degraded': the whole run still counts passes and the warning (rc 0, Passed: 13, Warnings: 1, Failed: 0).
+build_fixture "$WORK/degraded" "$(deep_body up up degraded up up)"
+got="$(run_smoke "$WORK/degraded") $(count "$WORK/degraded" 'Passed: 13') $(count "$WORK/degraded" 'Warnings: 1') $(count "$WORK/degraded" 'Failed: 0')"
+if [ "$got" = "0 1 1 1" ]; then ok "CONTROL - a degraded run still counts: rc 0, Passed: 13, Warnings: 1, Failed: 0"; else bad "CONTROL - a degraded run still counts: rc 0, Passed: 13, Warnings: 1, Failed: 0" "want 0 1 1 1, got $got"; fi
+
+# CONTROL - postgres 'down': the failure is still counted and still fails the run (rc 1, Failed: 1).
+build_fixture "$WORK/down" "$(deep_body up down up up up)"
+got="$(run_smoke "$WORK/down") $(count "$WORK/down" 'Failed: 1')"
+if [ "$got" = "1 1" ]; then ok "CONTROL - a down service is still counted as a failure: rc 1, Failed: 1"; else bad "CONTROL - a down service is still counted as a failure: rc 1, Failed: 1" "want 1 1, got $got"; fi
+
+printf '\n  %d passed, %d failed\n' "$pass" "$fail"
+[ "$fail" -eq 0 ] || exit 1
+exit 0
--- a/Blockchain/Dev/scripts/smoke-test.sh
+++ b/Blockchain/Dev/scripts/smoke-test.sh
@@ -25,6 +25,6 @@
 FAILURES=()
-
-pass() { ((PASS++)); printf "  ${GREEN}✓${NC} %s\n" "$1"; }
-fail() { ((FAIL++)); FAILURES+=("$1"); printf "  ${RED}✗${NC} %s\n" "$1"; }
-warn() { ((WARN++)); printf "  ${YELLOW}!${NC} %s\n" "$1"; }
+
+pass() { PASS=$((PASS + 1)); printf "  ${GREEN}✓${NC} %s\n" "$1"; }
+fail() { FAIL=$((FAIL + 1)); FAILURES+=("$1"); printf "  ${RED}✗${NC} %s\n" "$1"; }
+warn() { WARN=$((WARN + 1)); printf "  ${YELLOW}!${NC} %s\n" "$1"; }
 section() { printf "\n${CYAN}━━━ %s ━━━${NC}\n" "$1"; }
```
