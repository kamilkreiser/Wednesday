# READY — KS-0-KS-0-O25-P1 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root/out.md.checker/patch.diff`** (from `ls` at 14:14 2026-10-30; sha256[:16] 7dc8ddd272d93e2f, 4503 B — a BYTE count; NOTE — `cat section_*.diff | cmp patch.diff` rc 1, differing by 4 line(s); the checker REWROTE section_1.diff; patch.diff is the model's AS-WRITTEN block, the SECTION FILES are the applied units and the canonical for the raise: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_1.diff: REANCHORED (hunk 1: reanchored at 27 (1 '-' / 1 '+' lines; model header -24,5 +24,5);reanchored 1/1 hunk(s););` — STRICT APPLY NOT CLAIMED for the whole patch: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4503 B vs golden 4818 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-dockerfile-non-root.sh 2, check_dockerfile_non_root_reports_root.test.sh 70); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 14:14 2026-10-30 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558, Blockchain/Dev/scripts/check-dockerfile-non-root.sh and Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-dockerfile-non-root.sh', 'Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-dockerfile-non-root.sh , Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): NON-EMPTY: `error: corrupt patch at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root/out.md.c`; checker-REWRITTEN: REANCHORED (applied file = the reanchored hunks; as-written kept at section_1.diff.as-written))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` (+70/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL: no-USER case: rc=1 out=', 'FAIL: USER root case: rc=0 out=OK — all 1 Dockerfile(s) drop root for runtime.']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-dockerfile-non-root.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` (+70/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — the CHECKER-REWRITTEN file, not the fence; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_dockerfile_non_root_reports_root/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-dockerfile-non-root.sh
+++ b/Blockchain/Dev/scripts/check-dockerfile-non-root.sh
@@ -24,5 +24,5 @@
 for f in $DOCKERFILES; do
   # Find the LAST USER directive in the file (the one that takes effect at runtime).
   # Allow `USER root` only inside the build stages — the FINAL USER must not be root.
-  last_user=$(grep -E '^\s*USER\s+' "$f" | tail -1 | sed -E 's/^\s*USER\s+//; s/[#].*$//' | tr -d '[:space:]')
+  last_user=$(grep -E '^[[:space:]]*USER[[:space:]]+' "$f" | tail -1 | sed -E 's/^[[:space:]]*USER[[:space:]]+//; s/[#].*$//' | tr -d '[:space:]' || true)
 
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh
@@ -0,0 +1,70 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-dockerfile-non-root.sh - a Dockerfile that
+# runs as root, or has no USER at all, must be REPORTED, not swallowed.
+# =============================================================================
+# Two faults on the last_user line. (1) With no USER directive `grep` exits 1, `pipefail`
+# makes the command substitution fail and `set -e` ends the script silently: exit 1, no
+# message, so the gate fails but names no file. (2) The `sed -E` uses `\s`, which BSD sed
+# (macOS) does not know, so `USER root` is read as `USERroot`, never equals `root`, and the
+# gate prints OK for a root container.
+# Real tools, a private fixture tree; nothing outside the temp dir is read.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${CHECK_DOCKERFILE_NON_ROOT_SH:-$HERE/../check-dockerfile-non-root.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: check-dockerfile-non-root.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/dfroot.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+REAL_GREP="$(command -v grep)"
+
+run_case() {   # $1 = name, $2 = Dockerfile text -> prints rc; output in $WORK/$1.out
+  local root="$WORK/$1"
+  mkdir -p "$root/scripts" "$root/services/s" "$root/frontend" "$root/docker" "$root/connectors" "$root/deployment"
+  cp "$SUBJ" "$root/scripts/check-dockerfile-non-root.sh"
+  printf '%s' "$2" > "$root/services/s/Dockerfile"
+  ( cd "$root" && bash scripts/check-dockerfile-non-root.sh ) >"$WORK/$1.out" 2>&1
+  echo $?
+}
+
+RC_NOUSER="$(run_case nouser $'FROM node:20\nRUN true\n')"
+RC_ROOT="$(run_case root $'FROM node:20\nUSER root\n')"
+RC_APP="$(run_case app $'FROM node:20\nUSER app\n')"
+RC_MULTI="$(run_case multi $'FROM node:20 AS build\nUSER root\nFROM node:20\nUSER app\n')"
+
+# CELL 1 (RED at the tip) - no USER directive: exit 1 AND the file is named.
+if [[ "$RC_NOUSER" == "1" ]] && "$REAL_GREP" -qF 'has NO USER directive' "$WORK/nouser.out" \
+   && "$REAL_GREP" -qF 'services/s/Dockerfile' "$WORK/nouser.out"; then
+  echo "PASS: a Dockerfile with no USER directive exits 1 and is named"; PASS=$((PASS+1))
+else
+  echo "FAIL: no-USER case: rc=$RC_NOUSER out=$(head -2 "$WORK/nouser.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip on a BSD/macOS userland) - a final USER root exits 1 and is named.
+if [[ "$RC_ROOT" == "1" ]] && "$REAL_GREP" -qF "final USER is 'root'" "$WORK/root.out"; then
+  echo "PASS: a final USER root exits 1 and is named"; PASS=$((PASS+1))
+else
+  echo "FAIL: USER root case: rc=$RC_ROOT out=$(head -2 "$WORK/root.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - a non-root USER passes.
+if [[ "$RC_APP" == "0" ]] && "$REAL_GREP" -qF 'OK - all 1 Dockerfile' <(sed 's/ — / - /' "$WORK/app.out"); then
+  echo "PASS: CONTROL USER app exits 0 with the OK line"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL USER app: rc=$RC_APP out=$(head -2 "$WORK/app.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - USER root in a build stage, non-root at the end, passes.
+if [[ "$RC_MULTI" == "0" ]]; then
+  echo "PASS: CONTROL a root build stage with a non-root final USER exits 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL multi-stage: rc=$RC_MULTI out=$(head -2 "$WORK/multi.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+echo "check_dockerfile_non_root_reports_root: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```

**APPLIED `section_1.diff` (REANCHORED (applied file = the reanchored hunks; as-written kept at section_1.diff.as-written)) — byte for byte:**
```diff
--- a/Blockchain/Dev/scripts/check-dockerfile-non-root.sh
+++ b/Blockchain/Dev/scripts/check-dockerfile-non-root.sh
@@ -24,7 +24,7 @@
 for f in $DOCKERFILES; do
   # Find the LAST USER directive in the file (the one that takes effect at runtime).
   # Allow `USER root` only inside the build stages — the FINAL USER must not be root.
-  last_user=$(grep -E '^\s*USER\s+' "$f" | tail -1 | sed -E 's/^\s*USER\s+//; s/[#].*$//' | tr -d '[:space:]')
+  last_user=$(grep -E '^[[:space:]]*USER[[:space:]]+' "$f" | tail -1 | sed -E 's/^[[:space:]]*USER[[:space:]]+//; s/[#].*$//' | tr -d '[:space:]' || true)
 
   if [ -z "$last_user" ]; then
     echo "::error::$f has NO USER directive — runs as root (pen-test F-15)"
```
