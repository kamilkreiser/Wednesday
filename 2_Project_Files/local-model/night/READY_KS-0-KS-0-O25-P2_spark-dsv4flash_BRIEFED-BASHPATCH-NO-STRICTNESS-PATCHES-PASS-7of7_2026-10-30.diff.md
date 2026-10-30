# READY — KS-0-KS-0-O25-P2 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_strictness_patches_skips_node_modules/out.md.checker/patch.diff`** (from `ls` at 14:14 2026-10-30; sha256[:16] bc7246bf606ff9eb, 4599 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_strictness_patches_skips_node_modules/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_strictness_patches_skips_node_modules/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_strictness_patches_skips_node_modules-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4599 B vs golden 4934 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-no-strictness-patches.sh 2, check_no_strictness_patches_skips_node_modules.test.sh 76); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 14:14 2026-10-30 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_strictness_patches_skips_node_modules/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558, Blockchain/Dev/scripts/check-no-strictness-patches.sh and Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-no-strictness-patches.sh', 'Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-no-strictness-patches.sh , Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-no-strictness-patches.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-no-strictness-patches.sh` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh` (+76/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL: node_modules-only hit: rc=1 out=::error::Found banned TS-strictness flip (pen-test H3 regression):   services/s/node_modules/dep/node_modules/deeper/ci.yml:1:x: noUnusedLocals = false', 'FAIL: mixed hits: rc=1 out=::error::Found banned TS-strictness flip (pen-test H3 regression):   services/s/Dockerfile:1:RUN sed -i x && noUnusedLocals = false   services/s/node_modules/dep/node_modules/deeper/ci.yml:1:x: noUnusedLocals = false']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-no-strictness-patches.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-no-strictness-patches.sh` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh` (+76/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_strictness_patches_skips_node_modules/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_strictness_patches_skips_node_modules/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-no-strictness-patches.sh
+++ b/Blockchain/Dev/scripts/check-no-strictness-patches.sh
@@ -45,5 +45,5 @@
 for pat in "${PATTERNS[@]}"; do
-  hits=$(grep -rEn --include='Dockerfile*' --include='*.sh' --include='*.yml' \
+  hits=$(grep -rEn --exclude-dir=node_modules --include='Dockerfile*' --include='*.sh' --include='*.yml' \
                    --exclude='check-no-strictness-patches.sh' \
                    "$pat" "${SEARCH_PATHS[@]}" 2>/dev/null \
          | grep -v '^[[:space:]]*#' || true)
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh
@@ -0,0 +1,76 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-no-strictness-patches.sh - the scan must not
+# read installed packages.
+# =============================================================================
+# The scan is `grep -rEn --include=Dockerfile* --include=*.sh --include=*.yml ... services frontend
+# scripts deployment` with no --exclude-dir, and nothing filters node_modules afterwards, so a
+# vendored package that mentions the flip makes the gate fail for code the repo does not own, and
+# every installed tree is read on each run. Its siblings pass --exclude-dir=node_modules.
+# Real tools, a private fixture tree; nothing outside the temp dir is read.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_strictness_patches_skips_node_modules.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${CHECK_NO_STRICTNESS_PATCHES_SH:-$HERE/../check-no-strictness-patches.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-strictness-patches.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/strict.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+REAL_GREP="$(command -v grep)"
+
+run_case() {   # $1 = name, $2 = 1 to plant a hit in a nested node_modules, $3 = 1 to plant a real hit -> prints rc
+  local root="$WORK/$1"
+  mkdir -p "$root/scripts" "$root/services/s" "$root/frontend" "$root/deployment"
+  cp "$SUBJ" "$root/scripts/check-no-strictness-patches.sh"
+  if [[ "$2" == "1" ]]; then
+    mkdir -p "$root/services/s/node_modules/dep/node_modules/deeper"
+    printf 'x: noUnusedLocals = false\n' > "$root/services/s/node_modules/dep/node_modules/deeper/ci.yml"
+  fi
+  if [[ "$3" == "1" ]]; then
+    printf 'RUN sed -i x && noUnusedLocals = false\n' > "$root/services/s/Dockerfile"
+  fi
+  ( cd "$root" && bash scripts/check-no-strictness-patches.sh ) >"$WORK/$1.out" 2>&1
+  echo $?
+}
+
+RC_DEP="$(run_case dep 1 0)"
+RC_REAL="$(run_case real 0 1)"
+RC_CLEAN="$(run_case clean 0 0)"
+RC_BOTH="$(run_case both 1 1)"
+
+# CELL 1 (RED at the tip) - a hit only inside node_modules is not the repo's code: exit 0.
+if [[ "$RC_DEP" == "0" ]] && "$REAL_GREP" -qF 'no TS-strictness flips found' <(sed 's/ — / - /' "$WORK/dep.out") ; then
+  echo "PASS: a flip that exists only under node_modules is ignored"; PASS=$((PASS+1))
+else
+  echo "FAIL: node_modules-only hit: rc=$RC_DEP out=$(head -3 "$WORK/dep.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - with a real hit and a node_modules hit, only the real one is printed.
+if [[ "$RC_BOTH" == "1" ]] && "$REAL_GREP" -qF 'services/s/Dockerfile:1:' "$WORK/both.out" \
+   && ! "$REAL_GREP" -qF 'node_modules' "$WORK/both.out"; then
+  echo "PASS: only the repo's own hit is printed"; PASS=$((PASS+1))
+else
+  echo "FAIL: mixed hits: rc=$RC_BOTH out=$(head -4 "$WORK/both.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - a real hit exits 1 and prints the error and the file.
+if [[ "$RC_REAL" == "1" ]] && "$REAL_GREP" -qF 'Found banned TS-strictness flip' "$WORK/real.out" \
+   && "$REAL_GREP" -qF 'services/s/Dockerfile:1:' "$WORK/real.out"; then
+  echo "PASS: CONTROL a real flip exits 1 and is printed"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL real hit: rc=$RC_REAL out=$(head -3 "$WORK/real.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - a clean tree exits 0.
+if [[ "$RC_CLEAN" == "0" ]]; then
+  echo "PASS: CONTROL a clean tree exits 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL clean: rc=$RC_CLEAN out=$(head -3 "$WORK/clean.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+echo "check_no_strictness_patches_skips_node_modules: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```
