# READY — KS-1413-KS-1413-O76_P1 (spark-dsv4flash, briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker/patch.diff`** (from `ls` at 14:01 2026-11-02; sha256[:16] ebe6b0f88640ed34, 5046 B; NOTE — `cat section_*.diff | cmp patch.diff` rc 1: the SECTION FILES are the applied units: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker/section_3.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker/section_4.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password-control-r3/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT(S): the two checkers' own `after_start-secuura.sh` IDENTICAL (`cmp` rc 0); `after_start-local.sh` IDENTICAL (`cmp` rc 0).

**Held 14:01 2026-11-02 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `c0f9af13f94b94d5d4acb7a7708c6dc3b6263231`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 2 product(s), 2 test(s): 1 red, 1 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at c0f9af13f94b94d5d4acb7a7708c6dc3b6263231, Start_Up/start-secuura.sh and Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Start_Up/start-secuura.sh', 'Blockchain/Dev/scripts/start-local.sh', 'Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh', 'Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Start_Up/start-secuura.sh , Blockchain/Dev/scripts/start-local.sh } + { Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh , Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (4 files: 2 product(s) + 2 test(s)); reference test `Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of start-secuura.sh are '-' lines, no stays-site removed; all 4 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 4 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 0/0 of `Start_Up/start-secuura.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Start_Up/start-secuura.sh 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/start-local.sh 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh 49 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1413_o76_p1_start_banners_no_demo_password/KS-1413.md`]: `File:` lines == product_files ['Start_Up/start-secuura.sh', 'Blockchain/Dev/scripts/start-local.sh']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh', 'Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Start_Up/start-secuura.sh` (+2/-1 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/start-local.sh` (+2/-1 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 3 `section_3.diff` → `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` (+5/-4 counted from the applied section file; git-apply options per `section_3.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 4 `section_4.diff` → `Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh` (+49/-0 counted from the applied section file; git-apply options per `section_4.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — start_secuura_banner.test.sh=green-support ks1413_start_banners_print_no_demo_password.test.sh=RED(rc 1, 2 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 2 product section(s): start_secuura_banner.test.sh(4 pass) ks1413_start_banners_print_no_demo_password.test.sh(4 pass)`
- SUPPORT test `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` (modified) — B4 [verbatim]: `B4 start_secuura_banner.test.sh (SUPPORT) with the test edits alone: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [red FAIL lines: []] · B5 [verbatim]: `B5 start_secuura_banner.test.sh after every product section: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0`
- RED test `Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh` (new) — B4 [verbatim]: `B4 ks1413_start_banners_print_no_demo_password.test.sh (RED) with the test edits alone: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red FAIL lines: ['FAIL start-secuura.sh echoes no demo password value', 'FAIL start-local.sh echoes no demo password value']] · B5 [verbatim]: `B5 ks1413_start_banners_print_no_demo_password.test.sh after every product section: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (8 suite(s): bootstrap_env_slot_ports.test.sh 51p/0f->51p/0f; check_slot_credentials.test.sh 32p/0f->32p/0f; ks1355_slot_blind_launchers.test.sh 36p/0f->36p/0f; stack_env.test.sh 25p/0f->25p/0f; stack_guard.test.sh 27p/0f->27p/0f; start_secuura_expected_services.test.sh 5p/0f->5p/0f; start_secuura_marker_unknown_warning.test.sh 5p/0f->5p/0f; start_secuura_slot_names.test.sh 23p/0f->23p/0f;)` [8 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=3 ok=3 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=4 products=2 tests=2 red=1 support=1 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Start_Up/start-secuura.sh` (+2/-1), `Blockchain/Dev/scripts/start-local.sh` (+2/-1) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` (MODIFIED, SUPPORT, +5/-4), `Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh` (NEW, RED, +49/-0); 4 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict); section 4 `section_4.diff`: `git apply -p1` (strict) — at the tip `c0f9af13f94b94d5d4acb7a7708c6dc3b6263231` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/input.json`. Brief (given by --brief): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1413_o76_p1_start_banners_no_demo_password/KS-1413.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/checker.out`.

```diff
diff --git a/Start_Up/start-secuura.sh b/Start_Up/start-secuura.sh
--- a/Start_Up/start-secuura.sh
+++ b/Start_Up/start-secuura.sh
@@ -709,5 +709,6 @@
 echo ""
 echo -e "  ${BOLD}Credentials:${NC}"
-echo -e "    Issuer:  demo@secuura.io / demo123"
+# KS-1413: print the mechanism, not the demo password value.
+echo -e "    Issuer:  demo@secuura.io (password: the published demo default - see CLAUDE.md)"
 echo -e "    Admin:   provisioned per run - see systemTest/fixtures/provision-actors.ts (KS-966: no shared admin credential is published)"
 echo ""
diff --git a/Blockchain/Dev/scripts/start-local.sh b/Blockchain/Dev/scripts/start-local.sh
--- a/Blockchain/Dev/scripts/start-local.sh
+++ b/Blockchain/Dev/scripts/start-local.sh
@@ -282,5 +282,6 @@
     echo ""
     echo -e "  ${BLUE}Demo Credentials:${NC}"
-    echo "    Issuer:  demo@secuura.io  / demo123"
+    # KS-1413: print the mechanism, not the demo password value.
+    echo "    Issuer:  demo@secuura.io  (password: the published demo default - see CLAUDE.md)"
     echo "    Admin:   admin@secuura.com / admin123"
     echo ""
diff --git a/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh b/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
--- a/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
@@ -49,11 +49,12 @@
 
 # ---------------------------------------------------------------------------
-# CELL 3 - CONTROL (green on both trees). Issuer line untouched.
+# CELL 3 - CONTROL (green on both trees). The Issuer line is still there and names the account (KS-1413
+# reworded its password text; ks1413_start_banners_print_no_demo_password.test.sh pins that the value is gone).
 # ---------------------------------------------------------------------------
-issuer_hits="$(grep -c 'Issuer:  demo@secuura.io / demo123' "$SUBJ" || true)"
+issuer_hits="$(grep -c 'Issuer:  demo@secuura.io' "$SUBJ" || true)"
 if [ "$issuer_hits" = 1 ]; then
-  ok "CONTROL - issuer line untouched (demo@secuura.io still authenticates)"
+  ok "CONTROL - issuer line still names the demo account"
 else
-  bad "CONTROL - issuer line untouched" \
+  bad "CONTROL - issuer line still names the demo account" \
       "expected 1 hit, got $issuer_hits"
 fi
diff --git a/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh b/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh
@@ -0,0 +1,49 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for the startup banners - KS-1413: start-secuura.sh and start-local.sh must not
+# echo the demo issuer password value in their closing credentials banner.
+# =============================================================================
+# Reads the two scripts with grep only; nothing is started, no network, no docker.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+START_SECUURA="$REPO_ROOT/Start_Up/start-secuura.sh"
+START_LOCAL="$REPO_ROOT/Blockchain/Dev/scripts/start-local.sh"
+PASS=0; FAIL=0
+
+check() {
+    local desc="$1" want="$2" got="$3"
+    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\n' "$desc"
+    else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
+}
+
+# echoed_secret <file>: prints the number of echo lines in the file that contain the demo password value
+echoed_secret() {
+    grep -cE '^[[:space:]]*echo[^|]*demo123' "$1" || true
+}
+
+# --- CELL 0 (CONTROL): the instrument matches an echo line that carries the value ---
+PLANT="$(printf '%s\n' '    echo "    Issuer:  demo@secuura.io  / demo123"' | grep -cE '^[[:space:]]*echo[^|]*demo123' || true)"
+check "CONTROL the echo matcher sees a planted banner line with the value" "1" "$PLANT"
+
+# --- CELL 1 (CONTROL, tip AND after): both banners still name the issuer account ---
+NAMED=0
+for f in "$START_SECUURA" "$START_LOCAL"; do
+    if grep -qE '^[[:space:]]*echo.*Issuer:.*demo@secuura\.io' "$f"; then NAMED=$((NAMED+1)); fi
+done
+check "CONTROL both banners still name the demo issuer account" "2" "$NAMED"
+
+# --- CELL 2 (RED at the tip): start-secuura.sh banner prints no password value ---
+check "start-secuura.sh echoes no demo password value" "0" "$(echoed_secret "$START_SECUURA")"
+
+# --- CELL 3 (RED at the tip): start-local.sh banner prints no password value ---
+check "start-local.sh echoes no demo password value" "0" "$(echoed_secret "$START_LOCAL")"
+
+echo ""
+echo "ks1413_start_banners_print_no_demo_password: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
```
