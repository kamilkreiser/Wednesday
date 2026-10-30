# READY — KS-0-KS-0-O25-P4 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_no_pii_store_untracked_leg/out.md.checker/patch.diff`** (from `ls` at 14:14 2026-10-30; sha256[:16] 13b3f9dbbe90247c, 5934 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_no_pii_store_untracked_leg/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_no_pii_store_untracked_leg/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_no_pii_store_untracked_leg-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 5934 B vs golden 6223 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-no-pii-store.sh 4, check_no_pii_store_untracked_leg.test.sh 84); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 14:14 2026-10-30 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_no_pii_store_untracked_leg/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558, Blockchain/Dev/scripts/check-no-pii-store.sh and Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-no-pii-store.sh', 'Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-no-pii-store.sh , Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-no-pii-store.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 2 brief `+` line(s) present; script `+` lines 2 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 1/1 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-no-pii-store.sh` (+2/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh` (+84/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: untracked variant not reported: out=OK — no PII store file is tracked by git.', 'FAIL: untracked variant: rc=0 out=OK — no PII store file is tracked by git.']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-no-pii-store.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-no-pii-store.sh` (+2/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh` (+84/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_no_pii_store_untracked_leg/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_no_pii_store_untracked_leg/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-no-pii-store.sh
+++ b/Blockchain/Dev/scripts/check-no-pii-store.sh
@@ -53,7 +53,7 @@
 # Second leg: the store must not sit inside the working tree even UNTRACKED —
 # an untracked store is one `git add -f`, or one .gitignore edit, from exposure,
 # and `git clean -fdx` will silently destroy it.
-UNTRACKED=$(git ls-files --others --exclude-standard=false \
+UNTRACKED=$(git ls-files --others --exclude-standard \
               '*pii*.json' '*ks256-pii-data*' 2>/dev/null || true)
 # --exclude-standard=false still honours .gitignore for `--others`, so also scan
 # the filesystem directly: an ignored file is exactly the case we want to warn on.
@@ -62,6 +62,6 @@
 if [ -n "$UNTRACKED" ] || [ -n "$FOUND" ]; then
   echo "WARNING (KS-256): a PII store file exists inside the working tree:" >&2
-  { [ -n "$UNTRACKED" ] && echo "$UNTRACKED"; [ -n "$FOUND" ] && echo "$FOUND"; } | sed 's/^/  /' >&2
+  { [ -n "$UNTRACKED" ] && echo "$UNTRACKED"; [ -n "$FOUND" ] && echo "$FOUND"; true; } | sed 's/^/  /' >&2
   echo "" >&2
   echo "  It is ignored today, but an in-repo store is one .gitignore slip from" >&2
   # NOTE: single-quoted deliberately. This line previously used double quotes with
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh
@@ -0,0 +1,84 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-no-pii-store.sh - its second (untracked) leg must work
+# and must stay a WARNING.
+# =============================================================================
+# Two faults. (1) `git ls-files --others --exclude-standard=false` is not a valid option
+# (`--exclude-standard` takes no value): git exits 129, `|| true` hides it, UNTRACKED is always
+# empty, and an untracked pii-data.local.json is never reported although the header promises the
+# whole family. (2) Once (1) works, `{ [ -n UNTRACKED ] && echo ...; [ -n FOUND ] && echo ...; }` ends
+# on a failing test when only UNTRACKED is set, so `set -e` + `pipefail` exit the script with 1
+# in the middle of a "Warning, not a failure" block.
+# Real git and a private fixture repo in a temp dir; nothing outside it is read.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_pii_store_untracked_leg.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${CHECK_NO_PII_STORE_SH:-$HERE/../check-no-pii-store.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-pii-store.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/pii.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+REAL_GREP="$(command -v grep)"
+
+run_case() {   # $1 = name, $2 = file to plant (relative to Blockchain/Dev, "" for none), $3 = 1 to git-add it, $4 = 1 to gitignore it
+  local root="$WORK/$1"
+  mkdir -p "$root/Blockchain/Dev/scripts"
+  cp "$SUBJ" "$root/Blockchain/Dev/scripts/check-no-pii-store.sh"
+  git -C "$root" init -q
+  if [[ -n "$2" ]]; then
+    echo '{}' > "$root/Blockchain/Dev/$2"
+    [[ "$4" == "1" ]] && echo "$2" > "$root/Blockchain/Dev/.gitignore"
+    [[ "$3" == "1" ]] && git -C "$root" add "Blockchain/Dev/$2"
+  fi
+  ( cd "$root" && bash Blockchain/Dev/scripts/check-no-pii-store.sh ) >"$WORK/$1.out" 2>&1
+  echo $?
+}
+
+RC_UNTR="$(run_case untr pii-data.local.json 0 0)"
+RC_TRACKED="$(run_case tracked pii-data.json 1 0)"
+RC_CLEAN="$(run_case clean "" 0 0)"
+RC_IGN="$(run_case ign ks256-pii-data.json 0 1)"
+
+# CELL 1 (RED at the tip) - an untracked, not-ignored pii variant is reported by name.
+if "$REAL_GREP" -qF 'WARNING (KS-256)' "$WORK/untr.out" && "$REAL_GREP" -qF 'pii-data.local.json' "$WORK/untr.out"; then
+  echo "PASS: an untracked pii-data.local.json is reported"; PASS=$((PASS+1))
+else
+  echo "FAIL: untracked variant not reported: out=$(head -3 "$WORK/untr.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - that report is a warning: exit 0 and the closing line is printed.
+if [[ "$RC_UNTR" == "0" ]] && "$REAL_GREP" -qF 'Warning, not a failure' "$WORK/untr.out"; then
+  echo "PASS: the untracked-file report exits 0 and prints its full block"; PASS=$((PASS+1))
+else
+  echo "FAIL: untracked variant: rc=$RC_UNTR out=$(tail -2 "$WORK/untr.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - a tracked pii file exits 1 with the ERROR and the git rm hint.
+if [[ "$RC_TRACKED" == "1" ]] && "$REAL_GREP" -qF 'ERROR (KS-256)' "$WORK/tracked.out" \
+   && "$REAL_GREP" -qF 'git rm --cached Blockchain/Dev/pii-data.json' "$WORK/tracked.out"; then
+  echo "PASS: CONTROL a tracked pii file exits 1 with the git rm hint"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL tracked: rc=$RC_TRACKED out=$(head -3 "$WORK/tracked.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - a clean repo exits 0 with the OK line and no warning.
+if [[ "$RC_CLEAN" == "0" ]] && "$REAL_GREP" -qF 'no PII store file is tracked' "$WORK/clean.out" \
+   && ! "$REAL_GREP" -qF 'WARNING' "$WORK/clean.out"; then
+  echo "PASS: CONTROL a clean repo exits 0 with no warning"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL clean: rc=$RC_CLEAN out=$(head -3 "$WORK/clean.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 5 (GREEN CONTROL, tip AND after) - an IGNORED ks256 store is still found by the filesystem leg, exit 0.
+if [[ "$RC_IGN" == "0" ]] && "$REAL_GREP" -qF 'ks256-pii-data.json' "$WORK/ign.out"; then
+  echo "PASS: CONTROL an ignored ks256 store is still warned about, exit 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL ignored store: rc=$RC_IGN out=$(head -3 "$WORK/ign.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+echo "check_no_pii_store_untracked_leg: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 5 ]]
```
