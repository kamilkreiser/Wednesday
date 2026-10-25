# READY — KS-1513-KS-1513 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1513_p1/out.md.checker/patch.diff`** (from `ls` at 09:51 2026-10-26; sha256[:16] a681afb81a43f0ef, 4799 B; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1513_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1513_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1513_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made. Run's own golden_cmp.out [verbatim]: `golden tree f8a9745dbbee06ee12229ac5ed515793cc1db86c · patch tree f8a9745dbbee06ee12229ac5ed515793cc1db86c -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-26_ks_1513_p1_094518/*_cmp.index.out)`.

**Held 09:51 2026-10-26 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1513_p1/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480, Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh and Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh', 'Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh } + { Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of preflight_test_types_ratchet_leg.test.sh are '-' lines, no stays-site removed; all 11 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 11 brief `+` line(s) among the product sections' `+` lines (multiset; 1 NON-ASCII chars); must_change sites 0/0 of `Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh 12 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh 61 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1513_p1/KS-1513.md`]: `File:` lines == product_files ['Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh` (+12/-0 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh` (+61/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh=RED(rc 1, 3 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh(5 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh` (new) — B4 [verbatim]: `B4 ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh (RED) with the test edits alone: rc=1 fail_lines=3 pass_lines=2 load_error=0 timeout=0` [red FAIL lines: ['FAIL with no install the suite exits 0', 'FAIL with no install the suite prints one SKIP line naming the missing install', 'FAIL with no install no cell is reported FAIL']] · B5 [verbatim]: `B5 ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh after every product section: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (2 suite(s): preflight_deps.test.sh 61p/0f->61p/0f; preflight_test_types_ratchet_leg.test.sh 25p/9f->22p/0f;)` [2 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh` (+12/-0) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh` (NEW, RED, +61/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1513_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1513_p1/KS-1513.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1513_p1/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh
@@ -102,4 +102,15 @@ expect "the legs run 1..16 in order and leg 16 is last" "1 2 3 4 5 6 7 8 9 10 11
 expect "CONTROL the header parser reads headers at all (it found 16)" "16" "$(printf '%s\n' "$hdrs" | grep -c .)"
 
+# KS-1513: everything from here down to the stub block runs the REAL checker, which needs the workspace install (typescript).
+# Without one those cells go red for an ENVIRONMENT reason that leg 1 already refuses, so they are skipped, as the leg itself
+# SKIPs (advisory). The wiring cells above and the stub cells below need no install and always run.
+if bash "$DEV/scripts/preflight/deps-present.sh" >/dev/null 2>&1; then
+  have_install=yes
+else
+  have_install=no
+  printf 'SKIP — workspace install absent (leg 1 refuses this tree): the real-checker cells are not run\n'
+fi
+if [ "$have_install" = yes ]; then
+
 # -----------------------------------------------------------------------------
 # BEHAVIOUR: the real script, the real checker, throwaway fixture services.
@@ -171,4 +182,5 @@ case "$LEG_OUT" in
      expect "🔴 ...and the verdict counts all three services" "yes" "$(has "$LEG_OUT" 'OK — 3 service(s)')" ;;
 esac
+fi
 
 # -----------------------------------------------------------------------------
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh
@@ -0,0 +1,61 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for preflight_test_types_ratchet_leg.test.sh - KS-1513: in a tree with no
+# workspace install that suite must SKIP its real-checker cells, not go red.
+# =============================================================================
+# The suite runs the REAL checker (check.cjs) over fixture services in 9 cells,
+# which needs the workspace install (typescript). With no install those 9 cells
+# fail for an ENVIRONMENT reason that preflight leg 1 already refuses. The leg
+# script prints `SKIP (advisory)` and exits 0 in that tree; the suite must mirror
+# it for those cells only: the wiring cells and the stub cells (KS-1520) need no
+# install and must still run.
+#
+# This suite aims the other suite at "no install" with DEPS_PRESENT_ROOT, the
+# variable scripts/preflight/deps-present.sh honours, pointed at a directory that
+# does not exist, then reads its output. Nothing in the repository is changed.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUITE="${RATCHET_LEG_SUITE_SH:-$HERE/preflight_test_types_ratchet_leg.test.sh}"
+PASS=0; FAIL=0
+
+[[ -f "$SUITE" ]] || { echo "FATAL: suite not found at $SUITE" >&2; exit 2; }
+
+tmp="$(mktemp -d "${TMPDIR:-/tmp}/secuura-ks1513.XXXXXX")"
+trap 'rm -rf "$tmp"' EXIT INT TERM
+
+check() {
+    local desc="$1" want="$2" got="$3"
+    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\n' "$desc"
+    else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
+}
+
+# Run the suite with no workspace install reachable.
+out="$(DEPS_PRESENT_ROOT="$tmp/no-install-here" bash "$SUITE" 2>&1 < /dev/null)"; rc=$?
+
+# --- CELL 1 (RED at the tip): it exits 0 -----------------------------------------
+check "with no install the suite exits 0" "0" "$rc"
+
+# --- CELL 2 (RED at the tip): it says it skipped the real-checker cells ----------
+check "with no install the suite prints one SKIP line naming the missing install" "1" \
+    "$(printf '%s\n' "$out" | grep -c '^SKIP .*workspace install absent')"
+
+# --- CELL 3 (RED at the tip): no cell is reported failed -------------------------
+check "with no install no cell is reported FAIL" "0" \
+    "$(printf '%s\n' "$out" | grep -c '^FAIL ')"
+
+# --- CELL 4 (CONTROL, tip AND after): the stub cells still run -------------------
+check "CONTROL with no install the stub cells still run (the default-run stub cell reports ok)" "1" \
+    "$(printf '%s\n' "$out" | grep -c '^ok   CONTROL the default run (no arguments) passes with all three checkers green')"
+
+# --- CELL 5 (CONTROL, tip AND after): the wiring cells still run -----------------
+check "CONTROL with no install the leg-16 wiring cells still run" "1" \
+    "$(printf '%s\n' "$out" | grep -c 'a failing leg-16 script FAILS the run')"
+
+echo ""
+echo "ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
```
