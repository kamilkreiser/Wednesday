# READY — KS-1413-KS-1413-O120-P1 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords/out.md.checker/patch.diff`** (from `ls` at 21:42 2026-11-09; sha256[:16] 6ce6cde2616553c0, 2321 B; NOTE — `cat section_*.diff | cmp patch.diff` rc 1: the SECTION FILES are the applied units: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_1.diff: --recount --ignore-whitespace needed;` — STRICT APPLY NOT CLAIMED: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1): change lines (`+`/`-`, ordered) IDENTICAL in every section; APPLIED PRODUCT(S): the two checkers' own `after_start-local.sh` IDENTICAL (`cmp` rc 0). Run's own golden_cmp.out [verbatim]: `golden tree c08992fbf93c6cf3dfe04fb2483c04449a495759 · patch tree c08992fbf93c6cf3dfe04fb2483c04449a495759 -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords_`.

**Held 21:42 2026-11-09 by Spark operator o120 (priority-triage seat for the 18:46 Wednesday) after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at d0b4825cc24493213f82b609670a4a0fa521a4b9, Blockchain/Dev/scripts/start-local.sh and Blockchain/Dev/scripts/__tests__/stack_guard.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/start-local.sh', 'Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/scripts/start-local.sh } + { Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/stack_guard.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of start-local.sh are '-' lines, no stays-site removed; all 2 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 2 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 0/0 of `Blockchain/Dev/scripts/start-local.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/scripts/start-local.sh 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh 11 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3a689f50-fb0e-41b4-be7d-665810ecc4e4/scratchpad/KS-1413.holdcopy.md`]: `File:` lines == product_files ['Blockchain/Dev/scripts/start-local.sh']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/start-local.sh` (+2/-2 counted from the applied section file; git-apply options per `section_1.diff.opts`: `--recount --ignore-whitespace`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): NON-EMPTY: `error: corrupt patch at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana`)
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh` (+11/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks1413_start_banners_print_no_demo_password.test.sh=RED(rc 1, 2 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks1413_start_banners_print_no_demo_password.test.sh(7 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh` (modified) — B4 [verbatim]: `B4 ks1413_start_banners_print_no_demo_password.test.sh (RED) with the test edits alone: rc=1 fail_lines=2 pass_lines=5 load_error=0 timeout=0` [red FAIL lines: ['FAIL start-local.sh echoes no Grafana password value', 'FAIL start-local.sh echoes no admin password value']] · B5 [verbatim]: `B5 ks1413_start_banners_print_no_demo_password.test.sh after every product section: rc=0 fail_lines=0 pass_lines=7 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (2 suite(s): check_slot_credentials.test.sh 32p/0f->32p/0f; ks1355_slot_blind_launchers.test.sh 78p/0f->78p/0f;)` [2 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=accommodated (see the B2 line)`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/start-local.sh` (+2/-2) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh` (MODIFIED, RED, +11/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords/input.json`. Brief (given by --title-from-brief): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3a689f50-fb0e-41b4-be7d-665810ecc4e4/scratchpad/KS-1413.holdcopy.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1413_o120_p1_start_local_banner_prints_grafana_and_admin_passwords/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/start-local.sh
+++ b/Blockchain/Dev/scripts/start-local.sh
@@ -277,13 +277,13 @@
     echo "    Cardano Devnet:    http://localhost:6092"
     echo ""
     echo -e "  ${BLUE}Monitoring:${NC}"
-    echo "    Grafana:           http://localhost:6300 (admin/secuura_grafana)"
+    echo "    Grafana:           http://localhost:6300 (login: the local default, not printed here)"
     echo "    Prometheus:        http://localhost:6301"
     echo ""
     echo -e "  ${BLUE}Demo Credentials:${NC}"
     # KS-1413: print the mechanism, not the demo password value.
     echo "    Issuer:  demo@secuura.io  (password: the published demo default - see CLAUDE.md)"
-    echo "    Admin:   admin@secuura.com / admin123"
+    echo "    Admin:   admin@secuura.com  (password: the local seed default, not printed here)"
     echo ""
 }
 
--- a/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh
@@ -44,6 +44,17 @@
 # --- CELL 3 (RED at the tip): start-local.sh banner prints no password value ---
 check "start-local.sh echoes no demo password value" "0" "$(echoed_secret "$START_LOCAL")"
 
+# --- CELL 4 (CONTROL): the Grafana and admin matchers see a planted banner line each ---
+PLANT_G="$(printf '%s\n' '    echo "    Grafana:  http://localhost:6300 (admin/secuura_grafana)"' | grep -cE '^[[:space:]]*echo.*secuura_grafana' || true)"
+PLANT_A="$(printf '%s\n' '    echo "    Admin:   admin@secuura.com / admin123"' | grep -cE '^[[:space:]]*echo.*admin@secuura\.com[[:space:]]*/' || true)"
+check "CONTROL the Grafana and admin matchers see a planted banner line each" "11" "${PLANT_G}${PLANT_A}"
+
+# --- CELL 5 (RED at the tip): start-local.sh banner prints no Grafana password value ---
+check "start-local.sh echoes no Grafana password value" "0" "$(grep -cE '^[[:space:]]*echo.*secuura_grafana' "$START_LOCAL" || true)"
+
+# --- CELL 6 (RED at the tip): start-local.sh banner prints no admin password value ---
+check "start-local.sh echoes no admin password value" "0" "$(grep -cE '^[[:space:]]*echo.*admin@secuura\.com[[:space:]]*/' "$START_LOCAL" || true)"
+
 echo ""
 echo "ks1413_start_banners_print_no_demo_password: ${PASS} passed, ${FAIL} failed"
 (( FAIL == 0 ))
```
