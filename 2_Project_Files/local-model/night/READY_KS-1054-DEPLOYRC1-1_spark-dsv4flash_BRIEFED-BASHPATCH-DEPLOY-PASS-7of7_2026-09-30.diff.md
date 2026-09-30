# READY — KS-1054-DEPLOYRC1-1 (Spark deepseek-v4-flash-0731, thinking OFF, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA
> Heading and filename corrected by hand (Spark brief-writer, Wednesday sub-agent, 2026-09-30): `hold_ready.py` refuses `--model-tag` off the code_patch path, so it wrote `Ornith` / `ornith35b-q4`, and it prefixed the ROWID with the ticket a second time. The diff was written by the Spark (run `runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/out.md.meta.json`: backend spark, model deepseek-v4-flash-0731, thinking 0). Renamed with `mv`; nothing else in this file was edited. Finding: gate47 N-1350-7 (deploy.sh rc-1 wording). Refs KS-1054, does NOT close it. A2a run by hand: `out.md.checker/a2a_anchor.out` rc 0.

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/out.md.checker/patch.diff`** (from `ls` at 13:17 2026-09-30; sha256[:16] 898dd867aa246f64, 4793 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1054-N-1350-7/precheck/out.md.checker/patch.diff` rc 0, Spark brief-writer (Wednesday sub-agent)); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 13:17 2026-09-30 by Spark brief-writer (Wednesday sub-agent) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3e3a68260d0ef541b2410d323849d2639ddd6941`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 3e3a68260d0ef541b2410d323849d2639ddd6941, Blockchain/Dev/deployment/azure/deploy.sh and Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/deployment/azure/deploy.sh', 'Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/deployment/azure/deploy.sh , Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/deployment/azure/deploy.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 3 brief `+` line(s) present; script `+` lines 3 ordered-equal (whitespace-stripped) to expected_plus (1 NON-ASCII chars); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/deployment/azure/deploy.sh` (+3/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh` (+79/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh fails at the untouched tip (rc=1, 1 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=1 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 1 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL M1 rc 1 names both causes']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive deploy.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/deployment/azure/deploy.sh` (+3/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh` (+79/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3e3a68260d0ef541b2410d323849d2639ddd6941` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-7/checker.out`.

```diff
--- a/Blockchain/Dev/deployment/azure/deploy.sh
+++ b/Blockchain/Dev/deployment/azure/deploy.sh
@@ -854,7 +854,9 @@
                 SKIPS=$((SKIPS + 1))
                 ;;
             *)
-                log_error "  API Gateway: startup migrations FAILED — see above"
+                # rc 1 is a failed count OR a count that could not be read (python3 missing, a non-integer
+                # `failed`), so this line must not claim the migrations were read (gate47 N-1350-7).
+                log_error "  API Gateway: startup migrations FAILED or could not be verified — see above"
                 ERRORS=$((ERRORS + 1))
                 ;;
         esac
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh
@@ -0,0 +1,79 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for gate47 N-1350-7 — deploy.sh's rc-1 line must not claim the migrations were read
+# =============================================================================
+# check-startup-migrations.sh exits 1 for a FAILED count and ALSO for a count it could not read
+# (python3 missing, or `failed` not an integer). deploy.sh's `*)` arm printed "startup migrations
+# FAILED — see above" for every one of them, which is false when the parser was missing.
+# deploy.sh's own call-site bytes are extracted by marker and EXECUTED against a STUB predicate
+# that exits with a chosen rc (the shape of the ks1054 suite's R1-R3 cells).
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh
+# =============================================================================
+set -uo pipefail
+#
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+ONE="$HERE/../../deployment/azure/deploy.sh"
+#
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n       %s\n' "$1" "$2"; fail=$((fail + 1)); }
+#
+[[ -f "$ONE" ]] || { echo "FATAL: subject not found at $ONE" >&2; exit 2; }
+#
+CALL_MARKER='# KS-1054 / N-1332-5 — startup migrations. A grep for "healthy"'
+CALL_HITS=$(grep -cF "$CALL_MARKER" "$ONE" || true)
+if [[ "$CALL_HITS" == "1" ]]; then
+  ok "M0 deploy.sh's migration call site is locatable by marker (1 occurrence)"
+else
+  bad "M0 deploy.sh's migration call site is locatable by marker" "expected 1 occurrence, found $CALL_HITS"
+fi
+CALL_BLOCK=$(awk -v m="$CALL_MARKER" 'index($0,m){f=1} f{print} f&&/^        esac$/{exit}' "$ONE")
+#
+drive_callsite() { # $1 = the rc the stub predicate exits with -> the block's log lines, then "ERRORS=<n> SKIPS=<n>"
+  local stubrc="$1" dir
+  dir="$(mktemp -d "${TMPDIR:-/tmp}/n1350_7_callsite.XXXXXX")"
+  printf '#!/usr/bin/env bash\nexit %s\n' "$stubrc" > "$dir/check-startup-migrations.sh"
+  chmod +x "$dir/check-startup-migrations.sh"
+  {
+    printf 'log_error() { printf "ERROR %%s\\n" "$*"; }\n'
+    printf 'log_warn() { printf "WARN %%s\\n" "$*"; }\n'
+    printf 'log_info() { printf "INFO %%s\\n" "$*"; }\n'
+    printf 'log_success() { printf "SUCCESS %%s\\n" "$*"; }\n'
+    printf 'ERRORS=0\nSKIPS=0\nAPI_HEALTH=\x27{"status":"healthy"}\x27\n'
+    printf '__n1350_7_callsite() {\n'
+    printf '%s\n' "$CALL_BLOCK"
+    printf '}\n__n1350_7_callsite\n'
+    printf 'printf "ERRORS=%%s SKIPS=%%s\\n" "$ERRORS" "${SKIPS-unset}"\n'
+  } > "$dir/drive.sh"
+  ( cd "$dir" && bash ./drive.sh 2>/dev/null < /dev/null )
+  rm -rf "$dir"
+}
+#
+if [[ -z "$CALL_BLOCK" ]]; then
+  bad "M1 rc 1 names both causes" "the call-site block extracted EMPTY"
+  bad "M2 CONTROL rc 1 still counts an ERROR" "the call-site block extracted EMPTY"
+  bad "M3 CONTROL rc 2 is still a SKIP, not an ERROR" "the call-site block extracted EMPTY"
+else
+  OUT_FAIL=$(drive_callsite 1)
+  if [[ "$OUT_FAIL" == *"ERROR   API Gateway: startup migrations FAILED or could not be verified"* ]]; then
+    ok "M1 rc 1 prints FAILED OR could not be verified, so a missing parser is not reported as read migrations"
+  else
+    bad "M1 rc 1 names both causes" "printed: $OUT_FAIL"
+  fi
+  if [[ "$(printf '%s\n' "$OUT_FAIL" | tail -1)" == "ERRORS=1 SKIPS=0" ]]; then
+    ok "M2 CONTROL rc 1 still counts an ERROR, so the wording change did not weaken the check"
+  else
+    bad "M2 CONTROL rc 1 still counts an ERROR" "printed: $OUT_FAIL"
+  fi
+  OUT_SKIP=$(drive_callsite 2)
+  if [[ "$(printf '%s\n' "$OUT_SKIP" | tail -1)" == "ERRORS=0 SKIPS=1" && "$OUT_SKIP" == *"SKIPPED"* && "$OUT_SKIP" != *"ERROR "* ]]; then
+    ok "M3 CONTROL rc 2 is still a named SKIP and prints no ERROR line"
+  else
+    bad "M3 CONTROL rc 2 is still a SKIP, not an ERROR" "printed: $OUT_SKIP"
+  fi
+fi
+#
+echo
+echo "n1350-7 deploy.sh rc-1 message: $pass passed, $fail failed"
+[[ "$fail" -eq 0 ]] || exit 1
```
