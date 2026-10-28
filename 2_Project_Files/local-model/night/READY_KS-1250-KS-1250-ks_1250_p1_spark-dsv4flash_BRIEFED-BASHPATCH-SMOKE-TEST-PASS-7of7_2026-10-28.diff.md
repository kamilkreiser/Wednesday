# READY — KS-1250-KS-1250-ks_1250_p1 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; sha256[:16] b78e533aee0506b5, 5818 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 5818 B vs golden 6093 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (smoke-test.sh 4, smoke_test_honours_smoke_base_url.test.sh 88); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8894c7486f82f6eb682fecb879791f53312537b1`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8894c7486f82f6eb682fecb879791f53312537b1, Blockchain/Dev/scripts/smoke-test.sh and Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/smoke-test.sh', 'Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/smoke-test.sh , Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/smoke-test.sh` (script) and `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 3 brief `+` line(s) present; script `+` lines 3 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 0/0 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/smoke-test.sh` (+3/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh` (+88/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh fails at the untouched tip (rc=1, 3 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=3 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 3 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL RED SMOKE_BASE_URL set: every URL is under the given base', "FAIL RED the run prints 'Smoke target: <base>' once", "FAIL CONTROL - the default run prints 'Smoke target: http://localhost:6882' once"]]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive smoke-test.sh: no NEW failure after (2 suite(s))` [2 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/smoke-test.sh` (+3/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh` (+88/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8894c7486f82f6eb682fecb879791f53312537b1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1250_p1/KS-1250.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/smoke-test.sh
+++ b/Blockchain/Dev/scripts/smoke-test.sh
@@ -15,4 +15,6 @@
-GATEWAY="http://localhost:6882"
+# KS-1250: RUNBOOK 2.2 tells an operator to point this script at an environment with SMOKE_BASE_URL, but the script never read it, so a run could look like a check of kintsugi or demo while it checked localhost. An unset or empty value keeps the old default.
+GATEWAY="${SMOKE_BASE_URL:-http://localhost:6882}"
+echo "Smoke target: $GATEWAY"
 RED='\033[0;31m'
 GREEN='\033[0;32m'
 YELLOW='\033[1;33m'
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh
@@ -0,0 +1,88 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/smoke-test.sh - KS-1250: the script must honour SMOKE_BASE_URL
+# =============================================================================
+# RUNBOOK 2.2 (deployment/azure/RUNBOOK.md) tells an operator to run the smoke test against an environment with
+# `SMOKE_BASE_URL=https://<gateway> scripts/smoke-test.sh`. The script set its gateway from a literal and never read the
+# variable, so the run checked localhost whatever the variable said. Fixed: GATEWAY comes from SMOKE_BASE_URL (unset or
+# empty keeps http://localhost:6882) and the script prints the target it is using.
+#
+# curl is NEVER really run here (no stack, no network): a STUB curl on a private PATH records every URL it is given and
+# answers like a healthy gateway, in the shape of smoke_test_counters_survive_errexit.test.sh. The script runs in --quick mode.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh
+# =============================================================================
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SMOKE="$REPO_ROOT/Blockchain/Dev/scripts/smoke-test.sh"
+[ -f "$SMOKE" ] || { echo "FATAL: smoke-test.sh not found at $SMOKE" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/smokebase.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+BASE="http://smoke-target.invalid:9999"
+
+# A stub curl that appends every URL argument to $root/urls.txt, serves a healthy /health/deep body and a 200 for -w.
+build_fixture() {
+  local root="$1"
+  mkdir -p "$root/bin"
+  : > "$root/urls.txt"
+  printf '%s' '{"ready":true,"status":"ok","checks":{}}' > "$root/deep.json"
+  sed "s#@ROOT@#$root#g" > "$root/bin/curl" <<'STUB'
+#!/bin/bash
+for a in "$@"; do
+  case "$a" in http://*|https://*) printf '%s\n' "$a" >> "@ROOT@/urls.txt" ;; esac
+done
+for a in "$@"; do
+  case "$a" in */health/deep) cat "@ROOT@/deep.json"; exit 0 ;; esac
+done
+for a in "$@"; do [ "$a" = "-w" ] && { printf '200'; exit 0; }; done
+exit 0
+STUB
+  chmod +x "$root/bin/curl"
+}
+
+# Run the smoke test in --quick mode with the stub curl first on PATH. $2 is the value of SMOKE_BASE_URL, or the word UNSET.
+run_smoke() {
+  local root="$1" value="$2"
+  if [ "$value" = "UNSET" ]; then
+    ( unset SMOKE_BASE_URL; export PATH="$root/bin:$PATH"; bash "$SMOKE" --quick ) > "$root/out.txt" 2>&1
+  else
+    ( export SMOKE_BASE_URL="$value"; export PATH="$root/bin:$PATH"; bash "$SMOKE" --quick ) > "$root/out.txt" 2>&1
+  fi
+}
+total_urls() { grep -c . "$1/urls.txt"; }
+urls_not_under() { grep -v -c -F "$2" "$1/urls.txt"; }
+
+# CONTROL - without the variable every URL goes to the default gateway, and there is at least one.
+build_fixture "$WORK/unset"; run_smoke "$WORK/unset" UNSET
+got="$([ "$(total_urls "$WORK/unset")" -gt 0 ] && echo some || echo none) $(urls_not_under "$WORK/unset" "http://localhost:6882")"
+if [ "$got" = "some 0" ]; then ok "CONTROL - SMOKE_BASE_URL unset: every URL is under http://localhost:6882"; else bad "CONTROL - SMOKE_BASE_URL unset: every URL is under http://localhost:6882" "want 'some 0', got '$got'"; fi
+
+# CONTROL - an empty variable behaves as unset.
+build_fixture "$WORK/empty"; run_smoke "$WORK/empty" ""
+got="$([ "$(total_urls "$WORK/empty")" -gt 0 ] && echo some || echo none) $(urls_not_under "$WORK/empty" "http://localhost:6882")"
+if [ "$got" = "some 0" ]; then ok "CONTROL - SMOKE_BASE_URL empty: every URL is under http://localhost:6882"; else bad "CONTROL - SMOKE_BASE_URL empty: every URL is under http://localhost:6882" "want 'some 0', got '$got'"; fi
+
+# RED - with the variable set, every URL goes under it and none goes to localhost.
+build_fixture "$WORK/set"; run_smoke "$WORK/set" "$BASE"
+got="$([ "$(total_urls "$WORK/set")" -gt 0 ] && echo some || echo none) $(urls_not_under "$WORK/set" "$BASE")"
+if [ "$got" = "some 0" ]; then ok "RED SMOKE_BASE_URL set: every URL is under the given base"; else bad "RED SMOKE_BASE_URL set: every URL is under the given base" "want 'some 0', got '$got' (urls: $(tr '\n' ' ' < "$WORK/set/urls.txt"))"; fi
+
+# RED - the script prints the target it is using.
+got="$(grep -c -F "Smoke target: $BASE" "$WORK/set/out.txt")"
+if [ "$got" = "1" ]; then ok "RED the run prints 'Smoke target: <base>' once"; else bad "RED the run prints 'Smoke target: <base>' once" "want 1, got $got"; fi
+
+# CONTROL - the default run prints the default target, so the line is not specific to the override.
+got="$(grep -c -F "Smoke target: http://localhost:6882" "$WORK/unset/out.txt")"
+if [ "$got" = "1" ]; then ok "CONTROL - the default run prints 'Smoke target: http://localhost:6882' once"; else bad "CONTROL - the default run prints 'Smoke target: http://localhost:6882' once" "want 1, got $got"; fi
+
+printf '\n  %d passed, %d failed\n' "$pass" "$fail"
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
