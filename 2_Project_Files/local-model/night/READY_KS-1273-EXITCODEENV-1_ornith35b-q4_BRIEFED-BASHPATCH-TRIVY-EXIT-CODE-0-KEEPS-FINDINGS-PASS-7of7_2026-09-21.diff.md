# READY — KS-1273-EXITCODEENV-1 (Ornith, briefed, bash_patch: ONE product hunk + ONE NEW bash suite) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night/out.md.checker/patch.diff`** (two sections, `section_1.diff` + `section_2.diff` beside it; from `ls` at 06:07 2026-09-21). Checker B2: every section applies at the tip (strict); the run's `patch.diff` is BYTE-IDENTICAL to the drafter's `golden.diff` (`cmp -s` rc 0, the 04:3x/morning Wednesday seat).

**Held 06:07 2026-09-21 by the 04:3x/morning Wednesday seat after a source read (clauses built from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night/checker.out` and the `cmp` above, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Files: `Blockchain/Testing/jobs/04-container-trivy.sh` (the `:93` line: `--exit-code 0` added before `"$img"`, one `-`/`+` pair + a KS-1273 comment) and NEW `Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh` (3 CONTROL + 2 red cells on the KS-1136 harness with a `findings` stub mode). Checker lines: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · `PASS B6 sibling suite(s) that drive 04-container-trivy.sh: no NEW failure after (2 suite(s))`. Drafter's measured precedence (real trivy 0.71.0, offline secret scan): env `TRIVY_EXIT_CODE=1` + findings → rc 1; with `--exit-code 0` → rc 0.

**PR NOTES for the raise seat:** bash lane (PR G's shape from the 12th: `/bin/bash <suite>` from the worktree root, rc on its own line, `ok`/`FAIL` counts from the file; the red-proof via a tampered COPY of `04-container-trivy.sh` passed as `TRIVY_JOB_SH=`). `Refs KS-1273` (Closes at the raiser's discretion — the hunk IS the ticket's fix). Collision: both orders with the held/raised KS-1137-F2 patch (the image-filter suite) → one sha `ba7a4a360dce8949` (drafter, `collision_orders.log`); shellcheck not installed (B7 informational). Tier 2 (a test-harness job; no product service). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night/input.json`. Brief: `night/briefs/KS-1273-EXITCODEENV-1.md`.

```diff
--- a/Blockchain/Testing/jobs/04-container-trivy.sh
+++ b/Blockchain/Testing/jobs/04-container-trivy.sh
@@ -92,4 +92,5 @@
     --skip-db-update \
-    "$img" 2>/dev/null)"; trc=$?
+    --exit-code 0 "$img" 2>/dev/null)"; trc=$?
+  # KS-1273: --exit-code 0 keeps trc meaning "the scan ran" - a TRIVY_EXIT_CODE (or a trivy.yaml exit-code) in the caller's environment would otherwise make findings read as a failed scan and drop them.
   # KS-1136: trc is trivy's own exit code - a failed scan is no longer turned into an empty, clean-looking report.
   # extract just the high-signal subset
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
@@ -0,0 +1,114 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Testing/jobs/04-container-trivy.sh - a TRIVY_EXIT_CODE in
+# the caller's environment must not turn an image WITH findings into a failed
+# scan (KS-1273)
+# =============================================================================
+# The defect: after KS-1136 the job keeps trivy's own exit code as "the scan
+# ran". But trivy also exits non-zero when it FOUND something, if the caller's
+# environment carries TRIVY_EXIT_CODE (or a trivy.yaml sets exit-code). With no
+# --exit-code on its command line the job then recorded such an image as
+# error: scan-failed, counts {} and vulns [] - the findings DROPPED - exited 1
+# and said "could not scan" about an image it did scan. Measured on trivy
+# 0.71.0: TRIVY_EXIT_CODE=1 plus findings exits 1; the same scan with
+# --exit-code 0 on the command line exits 0 (the flag wins over the env).
+#
+# docker and trivy are NEVER run here (no stack, no daemon): both are STUBS on
+# a private PATH, in the shape of container_trivy_failed_scan_is_loud.test.sh.
+# The trivy stub reads $root/fail.txt ("<image> findings|empty" per line): a
+# findings image prints a report with 1 CRITICAL + 1 HIGH and, like the real
+# trivy, exits TRIVY_EXIT_CODE when that is set UNLESS --exit-code 0 is on its
+# command line; an empty image exits 1 with no output; every other image gets
+# `{}` and exits 0.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+JOB="$REPO_ROOT/Blockchain/Testing/jobs/04-container-trivy.sh"
+[ -f "$JOB" ] || { echo "FATAL: 04-container-trivy.sh not found at $JOB" >&2; exit 2; }
+command -v jq >/dev/null 2>&1 || { echo "FATAL: jq is not on PATH - the subject cannot run, so nothing here can be graded" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1273.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# Build a fixture around the job under test.
+#   $1 = dir   $2 = corpus text (what `docker images` prints)   $3 = mode list ("<image> findings|empty" lines)
+build_fixture() {
+  local root="$1" corpus="$2" modes="${3:-}"
+  rm -rf "$root"; mkdir -p "$root/Testing/jobs" "$root/bin" "$root/run"
+  cp "$JOB" "$root/Testing/jobs/04-container-trivy.sh"
+  printf '%s\n' "$corpus" > "$root/images.txt"
+  printf '%s\n' "$modes" > "$root/fail.txt"
+  { printf '#!/bin/bash\n'
+    printf 'case "${1:-}" in\n'
+    printf '  info) exit 0 ;;\n'
+    printf '  images) cat "%s/images.txt" ;;\n' "$root"
+    printf 'esac\nexit 0\n'
+  } > "$root/bin/docker"
+  sed "s#@ROOT@#$root#g" > "$root/bin/trivy" <<'STUB'
+#!/bin/bash
+for last; do :; done
+echo "$*" >> "@ROOT@/trivy_calls.txt"
+mode="$(awk -v i="$last" '$1 == i { print $2 }' "@ROOT@/fail.txt")"
+if [ "$mode" = empty ]; then exit 1; fi
+if [ "$mode" = findings ]; then
+  echo '{"Results":[{"Vulnerabilities":[{"VulnerabilityID":"CVE-2026-1273","PkgName":"openssl","InstalledVersion":"3.0.0","Severity":"CRITICAL"},{"VulnerabilityID":"CVE-2026-1274","PkgName":"zlib","InstalledVersion":"1.2.0","Severity":"HIGH"}]}]}'
+  case " $* " in *" --exit-code 0 "*) exit 0 ;; esac
+  exit "${TRIVY_EXIT_CODE:-0}"
+fi
+echo '{}'
+STUB
+  chmod +x "$root/bin/docker" "$root/bin/trivy"
+}
+
+# Run the job the way the orchestrator / audit runner do; when $2 is given the
+# caller's environment carries it as TRIVY_EXIT_CODE. Prints rc.
+run_job() {
+  local root="$1" envcode="${2:-}"
+  ( export PATH="$root/bin:/usr/bin:/bin" SELF="$root/Testing" RUN_DIR="$root/run"
+    if [ -n "$envcode" ]; then export TRIVY_EXIT_CODE="$envcode"; fi
+    cd "$SELF" && bash jobs/04-container-trivy.sh ) >"$root/out.txt" 2>&1
+  echo $?
+}
+art() { jq -r "$2" "$1/run/04-container-trivy.json" 2>/dev/null || echo unparseable; }
+# The ONE image's row: "<error or none> <CRITICAL count> <HIGH count>"
+row() { echo "$(art "$1" '.images[0].error // "none"') $(art "$1" '.images[0].counts.CRITICAL // 0') $(art "$1" '.images[0].counts.HIGH // 0')"; }
+
+# CONTROL - no TRIVY_EXIT_CODE: an image WITH findings is counted, no error, rc 0 (both trees).
+build_fixture "$WORK/plain" 'dev-auth:latest' 'dev-auth:latest findings'
+rc="$(run_job "$WORK/plain")"
+got="$rc $(row "$WORK/plain")"
+if [ "$got" = "0 none 1 1" ]; then ok "CONTROL - without TRIVY_EXIT_CODE an image with findings is counted: rc 0, no error, CRITICAL=1 HIGH=1"; else bad "CONTROL - without TRIVY_EXIT_CODE an image with findings is counted: rc 0, no error, CRITICAL=1 HIGH=1" "want 0 none 1 1, got $got"; fi
+
+# CONTROL - TRIVY_EXIT_CODE=1 and an image with NO findings: clean, rc 0 (the gate's second row; both trees).
+build_fixture "$WORK/cleanenv" 'dev-auth:latest'
+rc="$(run_job "$WORK/cleanenv" 1)"
+got="$rc $(row "$WORK/cleanenv")"
+if [ "$got" = "0 none 0 0" ]; then ok "CONTROL - TRIVY_EXIT_CODE=1 with an image that has no findings stays clean: rc 0, no error"; else bad "CONTROL - TRIVY_EXIT_CODE=1 with an image that has no findings stays clean: rc 0, no error" "want 0 none 0 0, got $got"; fi
+
+# CONTROL - KS-1136 survives: a trivy that exits 1 with NO output is still scan-failed, rc 1 (both trees).
+build_fixture "$WORK/empty" 'dev-auth:latest' 'dev-auth:latest empty'
+rc="$(run_job "$WORK/empty" 1)"
+got="$rc $(row "$WORK/empty")"
+if [ "$got" = "1 scan-failed 0 0" ]; then ok "CONTROL - a trivy that exits 1 with no output is still recorded as scan-failed and the job still exits 1"; else bad "CONTROL - a trivy that exits 1 with no output is still recorded as scan-failed and the job still exits 1" "want 1 scan-failed 0 0, got $got"; fi
+
+# RED - KS-1273: TRIVY_EXIT_CODE=1 in the caller's environment and the ONLY image HAS findings.
+build_fixture "$WORK/envcode" 'dev-auth:latest' 'dev-auth:latest findings'
+rc="$(run_job "$WORK/envcode" 1)"
+got="$rc $(row "$WORK/envcode")"
+if [ "$got" = "0 none 1 1" ]; then ok "🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keeps them: rc 0, no error, CRITICAL=1 HIGH=1"; else bad "🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keeps them: rc 0, no error, CRITICAL=1 HIGH=1" "want 0 none 1 1, got $got (trivy argv: $(tr '\n' ';' < "$WORK/envcode/trivy_calls.txt" 2>/dev/null))"; fi
+
+# RED - KS-1273: the same run prints the clean-run summary with the counts and never says "could not scan".
+got="$(grep -c -F 'CRITICAL=1 HIGH=1 across 1 image(s)' "$WORK/envcode/out.txt") $(grep -c -F 'could not scan' "$WORK/envcode/out.txt")"
+if [ "$got" = "1 0" ]; then ok "🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 image(s) and never says could not scan"; else bad "🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 image(s) and never says could not scan" "want 1 0, got $got, output: $(tr '\n' ' ' < "$WORK/envcode/out.txt")"; fi
+
+printf '\n  %d passed, %d failed\n' "$pass" "$fail"
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
