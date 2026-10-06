# READY — KS-1136-06-TENANT-STDERR-OWN-FILE-1 (Spark DeepSeek V4 Flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file/out.md.checker/patch.diff`** (from `ls` at 00:21 2026-10-07; sha256[:16] ddc7035ace50bb56, 6421 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file-control/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 00:21 2026-10-07 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d75bfe2deb8075583cfb55af0921e4964e7c6f0e`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at d75bfe2deb8075583cfb55af0921e4964e7c6f0e, Blockchain/Testing/jobs/06-tenant-isolation.sh and Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh', 'Blockchain/Testing/jobs/06-tenant-isolation.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Testing/jobs/06-tenant-isolation.sh , Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Testing/jobs/06-tenant-isolation.sh` (script) and `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_2.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 3 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 3; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` (+97/-0 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Testing/jobs/06-tenant-isolation.sh` (+3/-3 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh fails at the untouched tip (rc=1, 4 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=4 pass_lines=1 load_error=0 timeout=0` [red_first.out re-count: 4 FAIL line(s), 1 pass line(s); FAIL lines: ["FAIL RED the fallback run's artefact is the runner's JSON alone: rc 0, parses, 3 tested, 0 findings", 'FAIL RED the fallback run prints tested=3 cross-tenant_findings=0', "FAIL RED the runner's stderr is kept in 06-tenant-isolation.json.stderr", 'FAIL RED a leak found on a fallback run stays readable: rc 0, 1 finding, observed tenant-a']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive 06-tenant-isolation.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Testing/jobs/06-tenant-isolation.sh` (+3/-3 counted from `section_2.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` (+97/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d75bfe2deb8075583cfb55af0921e4964e7c6f0e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh
@@ -0,0 +1,97 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Testing/jobs/06-tenant-isolation.sh - the runner's
+# STDERR must never land inside the JSON artefact
+# =============================================================================
+# The defect: the job ran its runner as `> "$OUT" 2>&1`, so runner.ts login()'s
+# `console.error` - printed on the DESIGNED fallback, when verifier@ cannot log
+# in and holder@ is used instead - was written INTO 06-tenant-isolation.json
+# ahead of the JSON. A legitimate run's artefact was then unparseable: the job's
+# own summary read `tested=? cross-tenant_findings=?`, and 09-aggregate-report.sh
+# could not read the findings, a real cross-tenant leak included.
+#
+# node, curl and tsx are NEVER run here (no stack, no network): all three are
+# STUBS on a private PATH, in the shape of container_trivy_failed_scan_is_loud.test.sh.
+# The tsx stub reads $root/mode.txt: `fallback` prints the login-failed line to
+# stderr and then a clean result to stdout; `leak` does the same with one
+# cross-tenant finding; `quiet` prints the clean result with no stderr at all.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+JOB="$REPO_ROOT/Blockchain/Testing/jobs/06-tenant-isolation.sh"
+[ -f "$JOB" ] || { echo "FATAL: 06-tenant-isolation.sh not found at $JOB" >&2; exit 2; }
+command -v jq >/dev/null 2>&1 || { echo "FATAL: jq is not on PATH - the subject cannot run, so nothing here can be graded" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/tenant06.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# Build a fixture around the job under test.   $1 = dir   $2 = mode (fallback|leak|quiet)
+build_fixture() {
+  local root="$1" mode="$2"
+  rm -rf "$root"; mkdir -p "$root/Testing/jobs" "$root/Testing/tests/tenant-isolation" "$root/bin" "$root/run"
+  cp "$JOB" "$root/Testing/jobs/06-tenant-isolation.sh"
+  echo '// fixture: the tsx stub stands in for the runner' > "$root/Testing/tests/tenant-isolation/runner.ts"
+  printf '%s\n' "$mode" > "$root/mode.txt"
+  printf '#!/bin/bash\nexit 0\n' > "$root/bin/node"
+  printf '#!/bin/bash\nexit 0\n' > "$root/bin/curl"
+  sed "s#@ROOT@#$root#g" > "$root/bin/tsx" <<'STUB'
+#!/bin/bash
+mode="$(cat "@ROOT@/mode.txt")"
+if [ "$mode" != quiet ]; then
+  echo 'login failed for verifier@secuura.com: 401 {"success":false}' >&2
+fi
+if [ "$mode" = leak ]; then
+  printf '{"tested":["GET /api/documents","GET /api/anchors","GET /api/webhooks"],"findings":[{"endpoint":"GET /api/documents","observed_tenant":"tenant-a","expected_tenant":"tenant-b"}]}\n'
+else
+  printf '{"tested":["GET /api/documents","GET /api/anchors","GET /api/webhooks"],"findings":[]}\n'
+fi
+STUB
+  chmod +x "$root/bin/node" "$root/bin/curl" "$root/bin/tsx"
+}
+
+# Run the job the way the orchestrator / audit runner do. Prints rc.
+run_job() {
+  local root="$1"
+  ( export PATH="$root/bin:/usr/bin:/bin" SELF="$root/Testing" RUN_DIR="$root/run"
+    cd "$SELF" && bash jobs/06-tenant-isolation.sh ) >"$root/out.txt" 2>&1
+  echo $?
+}
+art() { jq -r "$2" "$1/run/06-tenant-isolation.json" 2>/dev/null || echo unparseable; }
+
+# CONTROL - a run with NO stderr: rc 0, the artefact parses, 3 endpoints tested, 0 findings.
+build_fixture "$WORK/quiet" quiet
+rc="$(run_job "$WORK/quiet")"
+got="$rc $(art "$WORK/quiet" '.tested | length') $(art "$WORK/quiet" '.findings | length')"
+if [ "$got" = "0 3 0" ]; then ok "CONTROL - a runner with no stderr: rc 0, artefact parses, 3 tested, 0 findings"; else bad "CONTROL - a runner with no stderr: rc 0, artefact parses, 3 tested, 0 findings" "want 0 3 0, got $got"; fi
+
+# RED - the designed verifier@ -> holder@ fallback: the login-failed line goes to stderr.
+build_fixture "$WORK/fallback" fallback
+rc="$(run_job "$WORK/fallback")"
+got="$rc $(art "$WORK/fallback" '.tested | length') $(art "$WORK/fallback" '.findings | length')"
+if [ "$got" = "0 3 0" ]; then ok "RED the fallback run's artefact is the runner's JSON alone: rc 0, parses, 3 tested, 0 findings"; else bad "RED the fallback run's artefact is the runner's JSON alone: rc 0, parses, 3 tested, 0 findings" "want 0 3 0, got $got"; fi
+
+# RED - the same run's summary line counts what the runner tested.
+got="$(grep -c -F 'tested=3 cross-tenant_findings=0' "$WORK/fallback/out.txt")"
+if [ "$got" = "1" ]; then ok "RED the fallback run prints tested=3 cross-tenant_findings=0"; else bad "RED the fallback run prints tested=3 cross-tenant_findings=0" "want 1, got $got, output: $(tr '\n' ' ' < "$WORK/fallback/out.txt")"; fi
+
+# RED - the runner's stderr is KEPT, beside the artefact, not thrown away.
+got="$(cat "$WORK/fallback/run/06-tenant-isolation.json.stderr" 2>/dev/null | grep -c -F 'login failed for verifier@secuura.com')"
+if [ "$got" = "1" ]; then ok "RED the runner's stderr is kept in 06-tenant-isolation.json.stderr"; else bad "RED the runner's stderr is kept in 06-tenant-isolation.json.stderr" "want 1, got $got"; fi
+
+# RED - a REAL cross-tenant leak on a fallback run is still readable as a finding.
+build_fixture "$WORK/leak" leak
+rc="$(run_job "$WORK/leak")"
+got="$rc $(art "$WORK/leak" '.findings | length') $(art "$WORK/leak" '.findings[0].observed_tenant')"
+if [ "$got" = "0 1 tenant-a" ]; then ok "RED a leak found on a fallback run stays readable: rc 0, 1 finding, observed tenant-a"; else bad "RED a leak found on a fallback run stays readable: rc 0, 1 finding, observed tenant-a" "want 0 1 tenant-a, got $got"; fi
+
+printf '\n  %d passed, %d failed\n' "$pass" "$fail"
+[ "$fail" -eq 0 ] || exit 1
+exit 0
--- a/Blockchain/Testing/jobs/06-tenant-isolation.sh
+++ b/Blockchain/Testing/jobs/06-tenant-isolation.sh
@@ -69,5 +69,5 @@ if [ -z "$TSX_BIN" ]; then
 fi
-
-TARGET_BASE="$TARGET" "$TSX_BIN" "$RUNNER" > "$OUT" 2>&1 || true
-
+
+TARGET_BASE="$TARGET" "$TSX_BIN" "$RUNNER" > "$OUT" 2> "$OUT.stderr" || true
+
 # stdout summary
```
