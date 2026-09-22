# READY — KS-1033-MISSINGBASE-1 (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 06:06 2026-09-23; sha256[:16] d1c7d5bc267b2b98, 6852 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night2/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed17-drafter-precheck/MISSINGBASE/out.md.checker/patch.diff` rc 0, Wednesday 06:0x seat 2026-09-23); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 06:06 2026-09-23 by Wednesday 06:0x seat 2026-09-23 after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2bc5ccf63b8c40911afb568b03cace066238ffcf` (input `bash_patch_1033MISSINGBASE-R17.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 2bc5ccf63b8c40911afb568b03cace066238ffcf, Blockchain/Dev/scripts/check-no-demo-mutation.sh and Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-no-demo-mutation.sh', 'Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-no-demo-mutation.sh , Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 3 brief `+` line(s) present; script `+` lines 3 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 3; must_change sites 3/3 each a `-` line; must_remove 3 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (+3/-3 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh` (+133/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: an unresolvable default base exited 0, not 2 - a demo mutation on this tree read as clean: [demo-guard] base origin/develop not found; nothing to compare', 'FAIL: cannot-be-resolved present=NO, nothing-to-compare present=YES']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive check-no-demo-mutation.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-no-demo-mutation.sh` (+3/-3 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh` (+133/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2bc5ccf63b8c40911afb568b03cace066238ffcf` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night2/input.json`. Brief (located by ticket + ROWID tokens ['MISSINGBASE', '1'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1033-R17-MISSINGBASE.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1033-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-no-demo-mutation.sh
+++ b/Blockchain/Dev/scripts/check-no-demo-mutation.sh
@@ -66,5 +66,5 @@
-# Skip if we can't resolve the base (first commit on a fresh clone).
+# KS-1033: a base that cannot be resolved is REFUSED (exit 2), never read as clean.
 if ! git rev-parse --verify "$BASE" >/dev/null 2>&1; then
-  echo "[demo-guard] base $BASE not found; nothing to compare"
-  exit 0
+  echo "[demo-guard] base $BASE cannot be resolved; refusing to read the tree as clean" >&2
+  exit 2
 fi
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh
@@ -0,0 +1,133 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-no-demo-mutation.sh - a diff BASE that
+# cannot be resolved is REFUSED (exit 2), never read as "nothing to compare"
+# (KS-1033; gate 19C finding DEMOBASE-MISSINGBASE-FAILOPEN on #1185)
+# =============================================================================
+# The default base is origin/develop (KS-1033 item 1). In a clone whose origin
+# has NO develop (a --single-branch main clone, a fresh fork) the guard printed
+# "base origin/develop not found; nothing to compare" and exited 0, so a demo
+# mutation on that tree read as clean. Every fixture is a throwaway repo under
+# mktemp -d pushing to a LOCAL BARE REMOTE, in the shape of
+# check_no_demo_mutation_base.test.sh.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_missing_base.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${DEMO_GUARD_SH:-$HERE/../check-no-demo-mutation.sh}"
+[ -r "$SUBJ" ] || { echo "FATAL: check-no-demo-mutation.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1033b.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+EXPECTED_CELLS=4
+DEMO_FILE="Blockchain/Dev/deployment/azure/migrate/init.sql"
+PLAIN_FILE="Blockchain/Dev/README.md"
+
+# build DIR LAST: a bare origin holding main only (LAST=main) or main AND develop
+# (LAST=develop), then a clone whose feature branch is cut from origin/LAST and
+# touches a demo path - a real demo mutation on every fixture.
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
+    git remote add origin "$1/origin.git"
+    if [ "$2" = develop ]; then
+      git checkout -q -b develop
+      echo "develop moved ahead" > "$PLAIN_FILE"
+      git add -A
+      git commit -qm "develop moves ahead on a plain path"
+      git push -q origin main develop
+    else
+      git push -q origin main
+    fi
+    cd "$1" || exit 9
+    git clone -q "$1/origin.git" work
+    cd "$1/work" || exit 9
+    git config user.email t@t.t
+    git config user.name t
+    git checkout -q -b feature "origin/$2"
+    echo "feature touches a demo path" > "$DEMO_FILE"
+    git add -A
+    git commit -qm "feature work"
+  ) > "$1/build.log" 2>&1
+}
+
+# run_guard DIR BASE-ARG TAG: the real guard with GITHUB_BASE_REF unset, with an
+# explicit base argument when BASE-ARG is non-empty. Prints its exit code; the
+# combined output lands in DIR/out-TAG.txt.
+run_guard() {
+  (
+    unset GITHUB_BASE_REF
+    cd "$1/work" || exit 9
+    if [ -n "$2" ]; then bash "$SUBJ" "$2"; else bash "$SUBJ"; fi
+  ) > "$1/out-$3.txt" 2>&1
+  echo $?
+}
+
+build "$WORK/nodev" main
+RC_NODEV="$(run_guard "$WORK/nodev" "" default)"
+OUT_NODEV="$WORK/nodev/out-default.txt"
+RC_ARGBASE="$(run_guard "$WORK/nodev" origin/main explicit)"
+OUT_ARGBASE="$WORK/nodev/out-explicit.txt"
+build "$WORK/withdev" develop
+RC_WITHDEV="$(run_guard "$WORK/withdev" "" default)"
+OUT_WITHDEV="$WORK/withdev/out-default.txt"
+
+# CELL 1 (RED at the tip) - a demo mutation on a clone whose origin has NO
+# develop must NOT read as clean: the guard exits 2 (1 means mutation detected).
+if [ "$RC_NODEV" = "2" ]; then
+  echo "PASS: an unresolvable default base exits 2 - refused, not read as clean"; PASS=$((PASS+1))
+else
+  echo "FAIL: an unresolvable default base exited $RC_NODEV, not 2 - a demo mutation on this tree read as clean: $(head -1 "$OUT_NODEV")"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - and it says why, never "nothing to compare".
+if grep -qF 'cannot be resolved' "$OUT_NODEV" && ! grep -qF 'nothing to compare' "$OUT_NODEV"; then
+  echo "PASS: the guard names the unresolvable base and prints no nothing-to-compare line"; PASS=$((PASS+1))
+else
+  echo "FAIL: cannot-be-resolved present=$(grep -qF 'cannot be resolved' "$OUT_NODEV" && echo yes || echo NO), nothing-to-compare present=$(grep -qF 'nothing to compare' "$OUT_NODEV" && echo YES || echo no)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the SAME tree with an explicit base
+# that resolves (origin/main as the argument) is a real demo mutation: blocked.
+if [ "$RC_ARGBASE" = "1" ] && grep -qF 'DEMO MUTATION DETECTED' "$OUT_ARGBASE"; then
+  echo "PASS: CONTROL the same tree with an explicit resolvable base is blocked with exit 1"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL explicit base origin/main exited $RC_ARGBASE (want 1), banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_ARGBASE" && echo yes || echo NO)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - when origin/develop exists the default
+# path is untouched: a demo mutation off develop is still blocked with exit 1.
+if [ "$RC_WITHDEV" = "1" ] && grep -qF 'DEMO MUTATION DETECTED' "$OUT_WITHDEV"; then
+  echo "PASS: CONTROL with origin/develop present a demo mutation is still blocked with exit 1"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL with origin/develop present exited $RC_WITHDEV (want 1), banner present=$(grep -qF 'DEMO MUTATION DETECTED' "$OUT_WITHDEV" && echo yes || echo NO)"; FAIL=$((FAIL+1))
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
+echo "check_no_demo_mutation_missing_base: $PASS passed, $FAIL failed"
+[ $FAIL -eq 0 ]
```
