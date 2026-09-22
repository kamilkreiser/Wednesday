# READY — KS-1245-1245DEGRADEDWARN-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `2_Project_Files/local-model/runs/2026-09-22_ks1245-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 19:35 2026-09-22; sha256[:16] 591d38f2f3983c7b, 5658 B — a BYTE count; NOTE — `cat section_*.diff | cmp patch.diff` rc 1, differing by 1 line(s); the checker REWROTE section_2.diff; patch.diff is the model's AS-WRITTEN block, the SECTION FILES are the applied units and the canonical for the raise: `2_Project_Files/local-model/runs/2026-09-22_ks1245-ornith35b-night/out.md.checker/section_1.diff`, `2_Project_Files/local-model/runs/2026-09-22_ks1245-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_2.diff: hunk header SYNTHESISED (a headerless new file; 0 context/bare line(s) restored to '+'; 0 '-' line(s) dropped — no old side in a new file); section_2.diff: new-file header count RECOUNTED 0 -> 81 (the declared count would have applied 0 of 81 lines and dropped the rest silently);` — STRICT APPLY NOT CLAIMED for the whole patch: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); CONTEXT-ONLY difference from the drafter's golden `2_Project_Files/local-model/runs/2026-09-22_feed16-drafter-precheck/DEGRADEDWARN/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 5658 B vs golden 5675 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (smoke-test.sh 6, smoke_test_degraded_warns.test.sh 81); context/empty lines run vs golden: equal counts; hunk headers differ (smoke_test_degraded_warns.test.sh: hunk COUNT differs (run 0 vs golden 1)); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 19:35 2026-09-22 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `2_Project_Files/local-model/runs/2026-09-22_ks1245-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3bad652d17cf111c1e2e1bed1ae7686894637487` (input `bash_patch_1245DEGRADEDWARN-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 3bad652d17cf111c1e2e1bed1ae7686894637487, Blockchain/Dev/scripts/smoke-test.sh and Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/smoke-test.sh', 'Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh']`
- New-file normalisation [checker.out, verbatim]: `B2 new-file normalisation (an accommodation the verdict names): section_2.diff: hunk header SYNTHESISED (a headerless new file; 0 context/bare line(s) restored to '+'; 0 '-' line(s) dropped — no old side in a new file); section_2.diff: new-file header count RECOUNTED 0 -> 81 (the declared count would have applied 0 of 81 lines and dropped the rest silently);`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/smoke-test.sh , Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/smoke-test.sh` (script) and `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 6 brief `+` line(s) present; script `+` lines 6 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 0; must_change sites 0/0 each a `-` line; must_remove 0 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/smoke-test.sh` (+6/-0 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh` (+81/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean); checker-REWRITTEN: NEW-FILE NORMALISED (as-written kept at section_2.diff.as-written))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL RED a degraded service passes the smoke test with one warning naming the service and its status', 'FAIL RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names smoke-test.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/smoke-test.sh` (+6/-0 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh` (+81/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — the CHECKER-REWRITTEN file, not the fence — at the tip `3bad652d17cf111c1e2e1bed1ae7686894637487` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `2_Project_Files/local-model/runs/2026-09-22_ks1245-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['1245', 'DEGRADEDWARN', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1245-R16B-DEGRADEDWARN.md`. Verdict source: `2_Project_Files/local-model/runs/2026-09-22_ks1245-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/smoke-test.sh
+++ b/Blockchain/Dev/scripts/smoke-test.sh
@@ -106,4 +106,10 @@
     [ -z "$svc" ] && continue
     if [ "$status" = "up" ]; then
       pass "$svc (latency ${latency}ms)"
+    elif [ "$status" = "degraded" ]; then
+      # KS-1245 (Kam 2026-09-22, option a): since #1037 /health/deep reports a
+      # soft-down dependency as 'degraded'. That is a PASS WITH A WARNING that
+      # names the service; only 'down' / 'error' (anything else) still fail.
+      pass "$svc (latency ${latency}ms) - DEGRADED"
+      warn "$svc - status=degraded (KS-1245: passes with this warning; down/error still fail)"
     else
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/smoke-test.sh - a 'degraded' /health/deep
+# service passes WITH a warning that names it; 'down'/'error' still fail
+# (KS-1245, Kam's ruling 2026-09-22 option a)
+# =============================================================================
+# curl is NEVER run here (no stack, no network): it is a STUB on a private
+# PATH, in the shape of container_trivy_failed_scan_is_loud.test.sh. The stub
+# answers /health/deep with the fixture's JSON and every http_code probe with
+# 200, so under --quick only section 1 of the smoke test can fail.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SMOKE="$REPO_ROOT/Blockchain/Dev/scripts/smoke-test.sh"
+[ -f "$SMOKE" ] || { echo "FATAL: smoke-test.sh not found at $SMOKE" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1245.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
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
+# CONTROL - every service 'up': rc 0, no failure, no warning.
+build_fixture "$WORK/allup" "$(deep_body up up up up up)"
+got="$(run_smoke "$WORK/allup") $(count "$WORK/allup" 'Failed: 0') $(count "$WORK/allup" 'Warnings: 0')"
+if [ "$got" = "0 1 1" ]; then ok "CONTROL - five services up: rc 0, Failed: 0, Warnings: 0"; else bad "CONTROL - five services up: rc 0, Failed: 0, Warnings: 0" "want 0 1 1, got $got"; fi
+
+# RED - auth 'degraded', the rest up: the run passes (rc 0) with ONE warning that names auth and its status.
+build_fixture "$WORK/degraded" "$(deep_body up up degraded up up)"
+got="$(run_smoke "$WORK/degraded") $(count "$WORK/degraded" 'Warnings: 1') $(count "$WORK/degraded" 'auth - status=degraded')"
+if [ "$got" = "0 1 1" ]; then ok "RED a degraded service passes the smoke test with one warning naming the service and its status"; else bad "RED a degraded service passes the smoke test with one warning naming the service and its status" "want 0 1 1, got $got"; fi
+got="$(count "$WORK/degraded" 'Passed: 13') $(count "$WORK/degraded" 'Failed: 0')"
+if [ "$got" = "1 1" ]; then ok "RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure"; else bad "RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure" "want 1 1, got $got"; fi
+
+# CONTROL - postgres 'down': still a failure (rc 1) naming the service and status, on both trees.
+build_fixture "$WORK/down" "$(deep_body up down up up up)"
+got="$(run_smoke "$WORK/down") $(count "$WORK/down" 'Failed: 1') $(count "$WORK/down" 'status=down')"
+if [ "$got" = "1 1 2" ]; then ok "CONTROL - a down service still fails the smoke test (rc 1, Failed: 1, postgres named twice: the line and the FAILURES list)"; else bad "CONTROL - a down service still fails the smoke test (rc 1, Failed: 1, postgres named twice: the line and the FAILURES list)" "want 1 1 2, got $got"; fi
+
+# CONTROL - anchoring 'error': still a failure, on both trees.
+build_fixture "$WORK/error" "$(deep_body up up up up error)"
+got="$(run_smoke "$WORK/error") $(count "$WORK/error" 'Failed: 1') $(count "$WORK/error" 'status=error')"
+if [ "$got" = "1 1 2" ]; then ok "CONTROL - an error service still fails the smoke test (rc 1, Failed: 1)"; else bad "CONTROL - an error service still fails the smoke test (rc 1, Failed: 1)" "want 1 1 2, got $got"; fi
+
+printf '\n  %d passed, %d failed\n' "$pass" "$fail"
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```

**APPLIED `section_2.diff` (NEW-FILE NORMALISED (as-written kept at section_2.diff.as-written)) — byte for byte:**
```diff
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh
@@ -0,0 +1,81 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/smoke-test.sh - a 'degraded' /health/deep
+# service passes WITH a warning that names it; 'down'/'error' still fail
+# (KS-1245, Kam's ruling 2026-09-22 option a)
+# =============================================================================
+# curl is NEVER run here (no stack, no network): it is a STUB on a private
+# PATH, in the shape of container_trivy_failed_scan_is_loud.test.sh. The stub
+# answers /health/deep with the fixture's JSON and every http_code probe with
+# 200, so under --quick only section 1 of the smoke test can fail.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SMOKE="$REPO_ROOT/Blockchain/Dev/scripts/smoke-test.sh"
+[ -f "$SMOKE" ] || { echo "FATAL: smoke-test.sh not found at $SMOKE" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1245.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
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
+# CONTROL - every service 'up': rc 0, no failure, no warning.
+build_fixture "$WORK/allup" "$(deep_body up up up up up)"
+got="$(run_smoke "$WORK/allup") $(count "$WORK/allup" 'Failed: 0') $(count "$WORK/allup" 'Warnings: 0')"
+if [ "$got" = "0 1 1" ]; then ok "CONTROL - five services up: rc 0, Failed: 0, Warnings: 0"; else bad "CONTROL - five services up: rc 0, Failed: 0, Warnings: 0" "want 0 1 1, got $got"; fi
+
+# RED - auth 'degraded', the rest up: the run passes (rc 0) with ONE warning that names auth and its status.
+build_fixture "$WORK/degraded" "$(deep_body up up degraded up up)"
+got="$(run_smoke "$WORK/degraded") $(count "$WORK/degraded" 'Warnings: 1') $(count "$WORK/degraded" 'auth - status=degraded')"
+if [ "$got" = "0 1 1" ]; then ok "RED a degraded service passes the smoke test with one warning naming the service and its status"; else bad "RED a degraded service passes the smoke test with one warning naming the service and its status" "want 0 1 1, got $got"; fi
+got="$(count "$WORK/degraded" 'Passed: 13') $(count "$WORK/degraded" 'Failed: 0')"
+if [ "$got" = "1 1" ]; then ok "RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure"; else bad "RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure" "want 1 1, got $got"; fi
+
+# CONTROL - postgres 'down': still a failure (rc 1) naming the service and status, on both trees.
+build_fixture "$WORK/down" "$(deep_body up down up up up)"
+got="$(run_smoke "$WORK/down") $(count "$WORK/down" 'Failed: 1') $(count "$WORK/down" 'status=down')"
+if [ "$got" = "1 1 2" ]; then ok "CONTROL - a down service still fails the smoke test (rc 1, Failed: 1, postgres named twice: the line and the FAILURES list)"; else bad "CONTROL - a down service still fails the smoke test (rc 1, Failed: 1, postgres named twice: the line and the FAILURES list)" "want 1 1 2, got $got"; fi
+
+# CONTROL - anchoring 'error': still a failure, on both trees.
+build_fixture "$WORK/error" "$(deep_body up up up up error)"
+got="$(run_smoke "$WORK/error") $(count "$WORK/error" 'Failed: 1') $(count "$WORK/error" 'status=error')"
+if [ "$got" = "1 1 2" ]; then ok "CONTROL - an error service still fails the smoke test (rc 1, Failed: 1)"; else bad "CONTROL - an error service still fails the smoke test (rc 1, Failed: 1)" "want 1 1 2, got $got"; fi
+
+printf '\n  %d passed, %d failed\n' "$pass" "$fail"
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
