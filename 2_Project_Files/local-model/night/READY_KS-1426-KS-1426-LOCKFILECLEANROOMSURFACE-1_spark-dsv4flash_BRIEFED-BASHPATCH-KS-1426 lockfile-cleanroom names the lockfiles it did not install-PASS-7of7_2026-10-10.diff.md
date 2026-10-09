# READY — KS-1426-KS-1426-LOCKFILECLEANROOMSURFACE-1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface/out.md.checker/patch.diff`** (from `ls` at 08:50 2026-10-10; sha256[:16] 503b0cda009442f6, 7392 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface-control/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 08:50 2026-10-10 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7834fd8059da31025aba15a47c4b4d61447016ed`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 7834fd8059da31025aba15a47c4b4d61447016ed, Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh and Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh', 'Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh , Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 34 brief `+` line(s) present; script `+` lines 35 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh` (+35/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh` (+107/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: the leg does not name the locks outside its four directories: All 3 standalone lock(s) pass clean-room npm ci.   covered: packages/p scripts/preflight services/a', "FAIL: no 'surface: 3 of 6 tracked' line in the output"]]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive lockfile-cleanroom.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh` (+35/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh` (+107/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7834fd8059da31025aba15a47c4b4d61447016ed` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1426-p1-lockfile-cleanroom-names-surface/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh
+++ b/Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh
@@ -88,6 +88,37 @@
     fi
 }
 
+# KS-1426: name the surface. "All N standalone lock(s) pass" reads like a total; it is
+# only the locks the discovery above reaches. List every tracked package-lock.json this
+# leg did NOT install, so the gap is on the screen. It reports only; the exit code is untouched.
+report_surface() {
+    local top prefix lock d covered covered_n=0 total=0 outside=0 lines=""
+    top="$(git rev-parse --show-toplevel 2>/dev/null)" || {
+        echo "  surface: not a git checkout - cannot list the tracked lockfiles this leg does not install"
+        return 0
+    }
+    prefix="$(git rev-parse --show-prefix)"
+    while IFS= read -r lock; do
+        total=$((total + 1))
+        covered=0
+        for d in ${CHECKED[@]+"${CHECKED[@]}"}; do
+            if [ "$lock" = "$prefix$d/package-lock.json" ]; then covered=1; fi
+        done
+        if [ "$covered" -eq 1 ]; then
+            covered_n=$((covered_n + 1))
+        else
+            outside=$((outside + 1))
+            lines="$lines    $lock"$'\n'
+        fi
+    done < <(git -C "$top" ls-files '*package-lock.json')
+    echo "  surface: $covered_n of $total tracked package-lock.json file(s) were installed by this leg"
+    if [ "$outside" -gt 0 ]; then
+        echo "  NOT installed by this leg ($outside):"
+        printf '%s' "$lines"
+    fi
+    return 0
+}
+
 FAILED=()
 CHECKED=()
 INFRA_SKIP=0
@@ -130,4 +161,7 @@
 # the success line — so a corpus of zero standalone locks prints "All 0 ... pass"
 # and then kills the gate. `${#CHECKED[@]}` on the line above is safe; only
 # the `[*]` expansion is not. Not reachable while every member carries a lock.
-echo "  covered: ${CHECKED[*]-}"
+echo "  covered: ${CHECKED[*]-}" # KS-1426: report_surface names what was NOT installed
+if [ "$#" -eq 0 ]; then
+    report_surface
+fi
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh
@@ -0,0 +1,107 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for scripts/preflight/lockfile-cleanroom.sh - KS-1426: the leg names the
+# tracked lockfiles it does NOT install
+# =============================================================================
+# The leg prints "All N standalone lock(s) pass" and reads like a total, but its
+# file list comes from four hardcoded directories (services packages frontend
+# scripts). Tracked locks elsewhere (connectors/, the workspace root, systemTest/)
+# are never installed by it. node and npm are stubs on a private PATH, so no
+# package is ever installed; the scratch tree is a throwaway git repo so the leg
+# can ask git which package-lock.json files are tracked.
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1426_lockfile_cleanroom_names_its_surface.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${LOCKFILE_CLEANROOM_SH:-$HERE/../preflight/lockfile-cleanroom.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: lockfile-cleanroom.sh not readable at $SUBJ" >&2; exit 2; }
+command -v git >/dev/null 2>&1 || { echo "FATAL: git required" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1426.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+
+# Stubs: node answers 24 (so the leg takes its host path, no docker); npm succeeds
+# unless the directory it runs in holds a file named FAIL_ME.
+mkdir -p "$WORK/bin"
+cat > "$WORK/bin/node" <<'STUB'
+#!/bin/sh
+echo 24
+STUB
+cat > "$WORK/bin/npm" <<'STUB'
+#!/bin/sh
+[ -e FAIL_ME ] && exit 1
+exit 0
+STUB
+chmod +x "$WORK/bin/node" "$WORK/bin/npm"
+
+# Scratch repo: three locks inside the leg's four directories, three outside.
+REPO="$WORK/repo"
+DEV="$REPO/Blockchain/Dev"
+mkdir -p "$DEV/scripts/preflight" "$DEV/services/a" "$DEV/packages/p" "$DEV/frontend" \
+         "$DEV/connectors/wa" "$REPO/systemTest/akto"
+cp "$SUBJ" "$DEV/scripts/preflight/lockfile-cleanroom.sh"
+touch "$DEV/frontend/.keep"
+for l in "$DEV/services/a" "$DEV/packages/p" "$DEV/scripts/preflight" "$DEV/connectors/wa" "$DEV" "$REPO/systemTest/akto"; do
+  echo '{}' > "$l/package-lock.json"
+done
+git -C "$REPO" init -q
+git -C "$REPO" add -A
+
+run_leg() {   # $@ = leg arguments -> output in $WORK/out.txt, prints rc
+  ( export PATH="$WORK/bin:/usr/bin:/bin"; bash "$DEV/scripts/preflight/lockfile-cleanroom.sh" "$@" ) >"$WORK/out.txt" 2>&1
+  echo $?
+}
+
+RC_ALL="$(run_leg)"
+cp "$WORK/out.txt" "$WORK/out_all.txt"
+RC_ONE="$(run_leg services/a)"
+cp "$WORK/out.txt" "$WORK/out_one.txt"
+touch "$DEV/services/a/FAIL_ME"
+RC_FAIL="$(run_leg)"
+cp "$WORK/out.txt" "$WORK/out_fail.txt"
+
+# CELL 1 (RED at the tip) - every tracked lock outside the four directories is named.
+if grep -qF 'Blockchain/Dev/connectors/wa/package-lock.json' "$WORK/out_all.txt" \
+   && grep -qF 'Blockchain/Dev/package-lock.json' "$WORK/out_all.txt" \
+   && grep -qF 'systemTest/akto/package-lock.json' "$WORK/out_all.txt"; then
+  echo "PASS: the leg names the three tracked locks it does not install"; PASS=$((PASS+1))
+else
+  echo "FAIL: the leg does not name the locks outside its four directories: $(tail -2 "$WORK/out_all.txt" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - the surface is stated as a count of the tracked locks.
+if grep -qF 'surface: 3 of 6 tracked package-lock.json file(s) were installed by this leg' "$WORK/out_all.txt"; then
+  echo "PASS: the leg states its surface as 3 of 6 tracked locks"; PASS=$((PASS+1))
+else
+  echo "FAIL: no 'surface: 3 of 6 tracked' line in the output"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the existing OK line and exit code are kept.
+if [[ "$RC_ALL" == "0" ]] && grep -qF 'All 3 standalone lock(s) pass clean-room npm ci.' "$WORK/out_all.txt" \
+   && grep -qF 'OK    services/a' "$WORK/out_all.txt"; then
+  echo "PASS: CONTROL a clean run still exits 0 and prints 'All 3 standalone lock(s) pass'"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL clean run: rc=$RC_ALL, $(grep -F 'All ' "$WORK/out_all.txt" | head -1)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - naming one directory on the command line prints no surface lines.
+if [[ "$RC_ONE" == "0" ]] && grep -qF 'All 1 standalone lock(s) pass' "$WORK/out_one.txt" \
+   && ! grep -qF 'surface:' "$WORK/out_one.txt" && ! grep -qF 'NOT installed' "$WORK/out_one.txt"; then
+  echo "PASS: CONTROL a run that names one directory prints no surface lines"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL one-directory run: rc=$RC_ONE, $(tail -3 "$WORK/out_one.txt" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 5 (GREEN CONTROL, tip AND after) - a failing lock still fails the leg, exit 1, no OK line.
+if [[ "$RC_FAIL" == "1" ]] && grep -qF 'FAIL  services/a' "$WORK/out_fail.txt" \
+   && ! grep -qF 'standalone lock(s) pass' "$WORK/out_fail.txt"; then
+  echo "PASS: CONTROL a failing lock still exits 1 and prints no pass line"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL failing lock: rc=$RC_FAIL, $(tail -3 "$WORK/out_fail.txt" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+echo "ks1426_lockfile_cleanroom_names_its_surface: $PASS passed, $FAIL failed"
+[[ $FAIL -eq 0 ]]
```
