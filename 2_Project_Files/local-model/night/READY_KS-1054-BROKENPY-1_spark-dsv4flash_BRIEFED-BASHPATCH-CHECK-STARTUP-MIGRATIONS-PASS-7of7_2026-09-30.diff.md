# READY — KS-1054-BROKENPY-1 (Spark deepseek-v4-flash-0731, thinking OFF, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA
> Model label corrected by hand: `hold_ready.py` refuses `--model-tag` off the code_patch path, so it wrote `Ornith` / `ornith35b-q4`; the diff was written by the Spark (run `runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/out.md.meta.json`: backend spark, model deepseek-v4-flash-0731, thinking false). File renamed with `mv`, same precedent as KS-1346-B-r2 / KS-1121 on 09-27. Nothing else in this file was edited.

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/out.md.checker/patch.diff`** (from `ls` at 02:39 2026-09-30; sha256[:16] 4870de91a9e496dd, 3699 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1054-N-1350-1/precheck/out.md.checker/patch.diff` rc 0, Spark brief-writer (Wednesday sub-agent)); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 02:39 2026-09-30 by Spark brief-writer (Wednesday sub-agent) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `37205947ddd2775a72a417beb5b7ac8e3240fbf3`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 37205947ddd2775a72a417beb5b7ac8e3240fbf3, Blockchain/Dev/deployment/azure/check-startup-migrations.sh and Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/deployment/azure/check-startup-migrations.sh', 'Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/deployment/azure/check-startup-migrations.sh , Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/deployment/azure/check-startup-migrations.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 4 brief `+` line(s) present; script `+` lines 4 ordered-equal (whitespace-stripped) to expected_plus (1 NON-ASCII chars); `-` lines 2; must_change sites 2/2 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/deployment/azure/check-startup-migrations.sh` (+4/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh` (+27/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=38 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 38 pass line(s); FAIL lines: ["FAIL P10 python3 present but BROKEN + a failed-2 body -> FAILS CLOSED (rc 1), not read as 'not JSON'", 'FAIL P10b python3 present but BROKEN + a CLEAN body ALSO fails closed: a parser that cannot run is not evidence']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 40 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=40 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 40 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-startup-migrations.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/deployment/azure/check-startup-migrations.sh` (+4/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh` (+27/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `37205947ddd2775a72a417beb5b7ac8e3240fbf3` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1/checker.out`.

```diff
--- a/Blockchain/Dev/deployment/azure/check-startup-migrations.sh
+++ b/Blockchain/Dev/deployment/azure/check-startup-migrations.sh
@@ -74,8 +74,10 @@
 # this makes the two scripts consistent instead of inventing a new failure mode. Kam's option (a) is
 # explicit that the deploy reads as FAILED.
 # Checked EXPLICITLY, before the pipeline, so the message can name the real cause.
-if ! command -v python3 > /dev/null 2>&1; then
-  echo "  ✗ startupMigrations: python3 is NOT on PATH, so /health's body cannot be parsed."
+# N-1350-1 (gate47): a python3 that is PRESENT but BROKEN (on PATH, exits non-zero) is the same host
+# defect. It is probed here, or the pipeline's `|| echo UNPARSEABLE` reads it as "not JSON" (rc 2).
+if ! command -v python3 > /dev/null 2>&1 || ! python3 -c 'import json' > /dev/null 2>&1 < /dev/null; then
+  echo "  ✗ startupMigrations: python3 is NOT on PATH or does not run, so /health's body cannot be parsed."
   echo "    A missing parser is not evidence of a clean run; the DEPLOY fails (Kam's option (a))."
   exit 1
 fi
--- a/Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh
@@ -114,6 +114,33 @@
       '{"status":"healthy","startupMigrations":{"ran":true,"failed":2}}' 1 "2 migration(s) FAILED"
 probe "P9d CONTROL the clean body with python3 present -> rc 0, so the stub PATH is what moved P9b" \
       '{"status":"healthy","startupMigrations":{"ran":true,"applied":41,"failed":0}}' 0 "0 failed"
+# ---- N-1350-1 (gate47): python3 PRESENT but BROKEN (on PATH, exits non-zero; a stub exiting 127
+# here, and a macOS /usr/bin/python3 shim with no tools installed is the same shape) must FAIL CLOSED
+# exactly like python3 ABSENT. The base read a failed-2 body as "not JSON" -> rc 2, so deploy.sh
+# passed "with 1 check(s) SKIPPED" over failed migrations. P5 stays the genuinely-non-JSON CONTROL.
+echo "=== P-BADPY: python3 present but broken must FAIL CLOSED, and name the parser ==="
+BADPY_BIN="$NOPY_BIN/badpy"
+mkdir -p "$BADPY_BIN"
+printf '#!/bin/sh\nexit 127\n' > "$BADPY_BIN/python3"
+chmod +x "$BADPY_BIN/python3"
+badpy_probe() { # $1 label  $2 body  $3 want-rc  $4 want-substring
+  local out rc
+  out="$(PATH="$BADPY_BIN" /bin/bash "$SUBJ" "$2" 2>&1 < /dev/null)"; rc=$?
+  if [[ "$rc" != "$3" ]]; then bad "$1" "rc=$rc want $3 :: $out"; return; fi
+  if [[ -n "$4" && "$out" != *"$4"* ]]; then bad "$1" "output did not name '$4' :: $out"; return; fi
+  ok "$1"
+}
+if PATH="$BADPY_BIN" /bin/bash -c 'command -v python3 >/dev/null 2>&1 && ! python3 -c "import json" >/dev/null 2>&1'; then
+  ok "P10-FIXTURE python3 is on the stub PATH and exits non-zero (so the cells below are not vacuous)"
+else
+  bad "P10-FIXTURE python3 is on the stub PATH and exits non-zero" "the stub is absent or it runs - the cells below would prove nothing"
+fi
+badpy_probe "P10 python3 present but BROKEN + a failed-2 body -> FAILS CLOSED (rc 1), not read as 'not JSON'" \
+      '{"status":"healthy","startupMigrations":{"ran":true,"failed":2}}' 1 "python3"
+badpy_probe "P10b python3 present but BROKEN + a CLEAN body ALSO fails closed: a parser that cannot run is not evidence" \
+      '{"status":"healthy","startupMigrations":{"ran":true,"failed":0}}' 1 "python3"
+badpy_probe "P10c CONTROL python3 broken + an EMPTY body -> still rc 2: that branch never needed a parser" \
+      '' 2 "not a pass"
 # An EMPTY body needs no parser at all, so it must still be PASS-WITH-SKIP even with python3 gone.
 nopy_probe "P9e python3 absent + an EMPTY body -> still rc 2: that branch never needed a parser" \
       '' 2 "not a pass"
```
