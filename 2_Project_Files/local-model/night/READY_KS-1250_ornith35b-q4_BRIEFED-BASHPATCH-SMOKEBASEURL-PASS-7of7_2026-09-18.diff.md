# READY — KS-1250 (Ornith, briefed, BASH tier) — PASS 7/7 FIRST attempt, strict apply — HELD, and ⚠ DO NOT RAISE WITHOUT KAM


> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1250-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.opts`.** That is exactly what the checker graded PASS 7/7. **Never apply the embedded ```diff block below.** The embedded diff below is COMPLETE; the checker applied it in strict mode. (Corrected 2026-09-18 12:4x after seat A 10th measured that none of the embedded blocks applied as patches.)

**Held 2026-09-18 12:1x by the 10:0x Wednesday seat after a source read.** Run `runs/2026-09-18_ks1250-ornith35b-night`, tip `207716440`.
Product `Blockchain/Dev/scripts/smoke-test.sh` (+4 lines after :15). New test `smoke_test_honours_smoke_base_url.test.sh` (`curl` is a PATH stub, so there's no network).

## Source read
Minimal and correct: `GATEWAY="${SMOKE_BASE_URL:-$GATEWAY}"`, plus it **prints the target**, so a run can't look like it checked somewhere it didn't. With the variable unset, localhost behaviour is unchanged (the brief's control).

## ⚠ WHY THIS NEEDS KAM BEFORE IT IS RAISED, EVEN AT 7/7
Today RUNBOOK §2.2's command silently smoke-tests **localhost**. **After this change, a full (non-`--quick`) run against a named gateway will log in with the demo credentials, POST a `Smoke-Test` document and try to ANCHOR it there** (`smoke-test.sh :147-214`). Anchoring writes to the chain. That's presumably what the runbook always meant, but **nobody could have been doing it until now**, so this changes what a smoke run does to real servers. The ticket offered *honour the variable, or fix the runbook*. **Choosing between those is Kam's call.**
Also out of scope and noted: section 7 onward still probes hard-coded `localhost:60xx` ports.
**HELD. Not raised.**

---
## The diff, verbatim

```diff
--- a/Blockchain/Dev/scripts/smoke-test.sh
+++ b/Blockchain/Dev/scripts/smoke-test.sh
@@ -15,2 +15,6 @@
 GATEWAY="http://localhost:6882"
+# KS-1250: RUNBOOK section 2.2 points this script at an environment with SMOKE_BASE_URL. Honour it,
+# and say which target is being checked, so a run cannot look like it checked somewhere it did not.
+GATEWAY="${SMOKE_BASE_URL:-$GATEWAY}"
+echo "Smoke target: $GATEWAY"
 RED='\033[0;31m'
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh
@@ -0,0 +1,80 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for scripts/smoke-test.sh honouring SMOKE_BASE_URL (KS-1250)
+# =============================================================================
+# deployment/azure/RUNBOOK.md section 2.2 runs the smoke test against an
+# environment with `SMOKE_BASE_URL=https://<gateway> ../../scripts/smoke-test.sh`.
+# The script hardcoded http://localhost:6882 and never read the variable, so a
+# run that looked like it checked that environment checked localhost instead.
+#
+# `curl` is stubbed onto PATH (the stack_guard.test.sh pattern): the stub writes
+# every URL it is handed to a log and fails, so no request leaves this machine.
+# The script runs in --quick mode, whose every request goes to the gateway.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/smoke-test.sh"
+PASS=0
+FAIL=0
+
+expect() {
+  local desc="$1" want="$2" got="$3"
+  if [[ "$got" == "$want" ]]; then
+    PASS=$((PASS + 1)); printf 'ok   %s\n' "$desc"
+  else
+    FAIL=$((FAIL + 1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"
+  fi
+}
+
+tmp="$(mktemp -d "${TMPDIR:-/tmp}/ks1250-smoke.XXXXXX")"
+trap 'rm -rf "$tmp"' EXIT INT TERM
+mkdir -p "$tmp/bin"
+cat > "$tmp/bin/curl" <<'STUB'
+#!/usr/bin/env bash
+for a in "$@"; do
+  case "$a" in
+    http://*|https://*) printf '%s\n' "$a" >> "$CURL_LOG" ;;
+  esac
+done
+exit 7
+STUB
+chmod +x "$tmp/bin/curl"
+
+# run_smoke <SMOKE_BASE_URL or the word UNSET>: runs the script in --quick mode and
+# leaves the URLs it requested in $tmp/urls.txt and its output in $tmp/out.txt.
+run_smoke() {
+  : > "$tmp/urls.txt"
+  if [ "$1" = "UNSET" ]; then
+    env -u SMOKE_BASE_URL PATH="$tmp/bin:$PATH" CURL_LOG="$tmp/urls.txt" bash "$SCRIPT" --quick > "$tmp/out.txt" 2>&1
+  else
+    env SMOKE_BASE_URL="$1" PATH="$tmp/bin:$PATH" CURL_LOG="$tmp/urls.txt" bash "$SCRIPT" --quick > "$tmp/out.txt" 2>&1
+  fi
+}
+
+# How many requested URLs there were, and how many of them start with $1.
+url_counts() {
+  local total under
+  total=$(grep -c . "$tmp/urls.txt")
+  under=$(grep -c -F -- "$1" "$tmp/urls.txt")
+  printf '%s %s' "$total" "$under"
+}
+
+run_smoke UNSET
+expect "CONTROL without SMOKE_BASE_URL all 9 quick-mode requests go to http://localhost:6882" "9 9" "$(url_counts 'http://localhost:6882/')"
+
+run_smoke "http://smoke-target.ks1250.invalid:7"
+expect "🔴 with SMOKE_BASE_URL set all 9 quick-mode requests go to that target, none to localhost, and the run names its target" "9 9 0 yes" \
+  "$(url_counts 'http://smoke-target.ks1250.invalid:7/') $(grep -c -F 'localhost' "$tmp/urls.txt") $(grep -q -F 'Smoke target: http://smoke-target.ks1250.invalid:7' "$tmp/out.txt" && echo yes || echo no)"
+
+echo ""
+echo "smoke_test_honours_smoke_base_url: $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ]
```
