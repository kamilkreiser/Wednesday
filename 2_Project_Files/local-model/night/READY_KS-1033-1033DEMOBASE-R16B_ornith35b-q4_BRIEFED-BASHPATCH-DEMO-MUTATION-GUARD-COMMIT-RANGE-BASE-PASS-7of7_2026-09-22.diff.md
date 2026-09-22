# READY — KS-1033-1033DEMOBASE-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 10:29 2026-09-22; sha256[:16] 3b7af3c61b016703, 6394 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_1.diff: --recount (MISCOUNTED header, measured first — strict rc=0 is not trusted with a miscount: hunk @@ -55,6 +59,6 @@ elif [ -n "${1:-}" ];  declared old=6 new=6 actual old=7 new=7 (+1 trailing empty)); every line byte-exact;` — STRICT APPLY NOT CLAIMED for the whole patch: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/DEMOBASE/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 6394 B vs golden 6392 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-no-demo-mutation.sh 8, check_no_demo_mutation_base.test.sh 126); context/empty lines run vs golden: check-no-demo-mutation.sh 10/9 context; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 10:29 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1033DEMOBASE-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/scripts/check-no-demo-mutation.sh and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-no-demo-mutation.sh', 'Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-no-demo-mutation.sh , Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 6 brief `+` line(s) present; script `+` lines 6 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 2/2 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (+6/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `--recount`; `section_1.diff.header_measure.out`: NON-EMPTY: `hunk @@ -55,6 +59,6 @@ elif [ -n "${1:-}" ];  declared old=6 new=6 actual old=7 new=7 (+1 trailing empty)`; `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` (+126/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ["FAIL: a develop-based branch touching no demo path exited 1, not 0 - the base dragged in develop's own commits (1 demo path line(s) reported)", 'FAIL: clean-message present=NO, block banner present=YES']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-no-demo-mutation.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh red_first=yes apply_mode=lenient`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (+6/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` (+126/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['1033', 'DEMOBASE', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1033-R16B-DEMOBASE.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-no-demo-mutation.sh
+++ b/Blockchain/Dev/scripts/check-no-demo-mutation.sh
@@ -49,5 +49,9 @@ DEMO_PREFIXES=(
 # Determine the diff range. In CI this is the PR base..head; locally
-# default to comparing against origin/main.
+# default to comparing against origin/develop (KS-1033). The three-dot diff
+# below takes the merge-base, and under Git Flow develop is permanently ahead
+# of main, so an origin/main base shows the whole develop-vs-main delta as
+# this branch's own change - measured: 4 demo files on a branch that touched
+# nothing.
 if [ -n "${GITHUB_BASE_REF:-}" ]; then
   BASE="origin/${GITHUB_BASE_REF}"
   HEAD="HEAD"
@@ -55,6 +59,6 @@ elif [ -n "${1:-}" ]; then
   BASE="$1"
   HEAD="${2:-HEAD}"
 else
-  BASE="origin/main"
+  BASE="origin/develop"
   HEAD="HEAD"
 fi
 
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh
@@ -0,0 +1,126 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-no-demo-mutation.sh - the DEFAULT diff
+# base must be origin/develop, not origin/main (KS-1033 item 1)
+# =============================================================================
+# Under Git Flow develop is permanently ahead of main, so an origin/main base
+# shows the whole develop-vs-main delta as this branch's own change. Every
+# fixture is a throwaway repo under mktemp -d pushing to a LOCAL BARE REMOTE.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${DEMO_GUARD_SH:-$HERE/../check-no-demo-mutation.sh}"
+[ -r "$SUBJ" ] || { echo "FATAL: check-no-demo-mutation.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1033.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+EXPECTED_CELLS=4
+DEMO_FILE="Blockchain/Dev/deployment/azure/migrate/init.sql"
+PLAIN_FILE="Blockchain/Dev/README.md"
+
+build() {
+  rm -rf "$1"
+  mkdir -p "$1"
+  (
+    export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
+    git init -q --bare -b main "$1/origin.git"
+    git init -q -b main "$1/seed"
+    cd "$1/seed" || exit 9
+    git config user.email t@t.t
+    git config user.name t
+    mkdir -p Blockchain/Dev/deployment/azure/migrate
+    echo base > "$PLAIN_FILE"
+    echo base > "$DEMO_FILE"
+    git add -A
+    git commit -qm init
+    git checkout -q -b develop
+    echo "develop moved ahead" > "$DEMO_FILE"
+    git add -A
+    git commit -qm "develop touches a demo path"
+    git remote add origin "$1/origin.git"
+    git push -q origin main develop
+    cd "$1" || exit 9
+    git clone -q "$1/origin.git" work
+    cd "$1/work" || exit 9
+    git config user.email t@t.t
+    git config user.name t
+    git checkout -q -b feature origin/develop
+    if [ "$2" = demo ]; then
+      echo "feature touches a demo path too" > "$DEMO_FILE"
+    else
+      echo "an ordinary change" > "$PLAIN_FILE"
+    fi
+    git add -A
+    git commit -qm "feature work"
+  ) > "$1/build.log" 2>&1
+}
+
+run_guard() {
+  (
+    unset GITHUB_BASE_REF
+    if [ -n "$2" ]; then export GITHUB_BASE_REF="$2"; fi
+    cd "$1/work" || exit 9
+    bash "$SUBJ"
+  ) > "$1/out.txt" 2>&1
+  echo $?
+}
+
+build "$WORK/plain" plain
+RC_PLAIN="$(run_guard "$WORK/plain" "")"
+OUT_PLAIN="$WORK/plain/out.txt"
+build "$WORK/demo" demo
+RC_DEMO="$(run_guard "$WORK/demo" "")"
+OUT_DEMO="$WORK/demo/out.txt"
+build "$WORK/ciref" plain
+RC_CIREF="$(run_guard "$WORK/ciref" develop)"
+OUT_CIREF="$WORK/ciref/out.txt"
+
+# CELL 1 (RED at the tip) - a develop-based branch that touched no demo path
+# must be allowed. At the tip the origin/main base drags develop's own demo
+# commit into the diff and the guard exits 1.
+if [ "$RC_PLAIN" = "0" ]; then
+  echo "PASS: a develop-based branch touching no demo path exits 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: a develop-based branch touching no demo path exited $RC_PLAIN, not 0 - the base dragged in develop's own commits ($(grep -c 'migrate/init.sql' "$OUT_PLAIN") demo path line(s) reported)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - and it must say so, not print the block banner.
+if grep -qF 'no demo-shaping paths touched' "$OUT_PLAIN" && ! grep -qF 'DEMO MUTATION DETECTED' "$OUT_PLAIN"; then
+  echo "PASS: the guard reports no demo-shaping paths touched and prints no block banner"; PASS=$((PASS+1))
+else
+  echo "FAIL: clean-message present=$(grep -qF 'no demo-shaping paths touched' "$OUT_PLAIN" && echo yes || echo NO), block banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_PLAIN" && echo YES || echo no)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the guard still refuses a REAL demo
+# change on the branch itself. This is what stops a fix that just always passes.
+if [ "$RC_DEMO" = "1" ] && grep -qF 'DEMO MUTATION DETECTED' "$OUT_DEMO"; then
+  echo "PASS: CONTROL a branch that really touches a demo path is still blocked with exit 1"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL a real demo change exited $RC_DEMO (want 1), banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_DEMO" && echo yes || echo NO)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - GITHUB_BASE_REF still wins over the
+# default, so the branch named there is what the diff is taken against.
+if [ "$RC_CIREF" = "0" ] && grep -qF 'no demo-shaping paths touched' "$OUT_CIREF"; then
+  echo "PASS: CONTROL GITHUB_BASE_REF=develop is still honoured ahead of the default"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL GITHUB_BASE_REF=develop exited $RC_CIREF (want 0): $(head -1 "$OUT_CIREF")"; FAIL=$((FAIL+1))
+fi
+
+# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing
+# is a check that cannot fail, so a short count is itself a FAIL.
+if [ $((PASS + FAIL)) -eq "$EXPECTED_CELLS" ]; then
+  echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))
+else
+  echo "FAIL: only $((PASS + FAIL)) of $EXPECTED_CELLS cells ran - a suite that asserts nothing is not a pass"; FAIL=$((FAIL+1))
+fi
+
+echo ""
+echo "check_no_demo_mutation_base: $PASS passed, $FAIL failed"
+[ $FAIL -eq 0 ]
```
