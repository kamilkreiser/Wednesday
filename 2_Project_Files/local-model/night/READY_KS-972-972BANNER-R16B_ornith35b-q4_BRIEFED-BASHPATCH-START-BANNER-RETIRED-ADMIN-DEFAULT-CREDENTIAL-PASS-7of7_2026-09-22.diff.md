# READY — KS-972-972BANNER-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks972-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 10:29 2026-09-22; sha256[:16] 5c16c2daf2198978, 4505 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks972-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks972-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_1.diff: --recount --ignore-whitespace needed;` — STRICT APPLY NOT CLAIMED for the whole patch: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/BANNER/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4505 B vs golden 4503 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (start-secuura.sh 2, start_secuura_banner.test.sh 78); context/empty lines run vs golden: start-secuura.sh 5/6 context; hunk headers differ (start-secuura.sh: run `@@ -709,7 +709,7 @@ echo -e ""` vs golden `@@ -709,7 +709,7 @@`); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 10:29 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks972-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_972BANNER-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Start_Up/start-secuura.sh and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Start_Up/start-secuura.sh', 'Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Start_Up/start-secuura.sh , Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Start_Up/start-secuura.sh` (script) and `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Start_Up/start-secuura.sh` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `--recount --ignore-whitespace`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): NON-EMPTY: `error: corrupt patch at line 11`)
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` (+78/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL the Credentials banner no longer prints the retired admin credential', 'FAIL the banner names the provisioning mechanism instead of a value']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive start-secuura.sh: no NEW failure after (4 suite(s))` [4 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh red_first=yes apply_mode=lenient`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Start_Up/start-secuura.sh` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` (+78/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks972-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['972', 'BANNER', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-972-R16B-BANNER.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks972-ornith35b-night/checker.out`.

```diff
--- a/Start_Up/start-secuura.sh
+++ b/Start_Up/start-secuura.sh
@@ -709,7 +709,7 @@ echo -e ""
 echo -e "  ${BOLD}Credentials:${NC}"
 echo -e "    Issuer:  demo@secuura.io / demo123"
-echo -e "    Admin:   admin@secuura.com / admin123"
+echo -e "    Admin:   provisioned per run - see systemTest/fixtures/provision-actors.ts (KS-966: no shared admin credential is published)"
 echo ""
 # KS-666: state, on screen, who now holds this stack — so the next person does
 # not have to run a destructive command to discover it is occupied.
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
@@ -0,0 +1,78 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Start_Up/start-secuura.sh Credentials banner (KS-972)
+# =============================================================================
+# The defect: line 712 still prints `Admin: admin@secuura.com / admin123` - a
+# login retired by PR #888. Every operator reads it as valid; every attempt to
+# use it returns 401. This task replaces the value with a pointer to where the
+# admin is actually provisioned per run and adds one shell suite proving the
+# change took effect without touching any other line.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=4
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SUBJ="${START_SECUURA_SH-$REPO_ROOT/Start_Up/start-secuura.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: start-secuura.sh not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: START_SECUURA_SH is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# ---------------------------------------------------------------------------
+# CELL 1 - RED. Untouched script has exactly one hit of the retired credential
+# in its own source. After the fix there must be zero hits.
+# ---------------------------------------------------------------------------
+banner_hits="$(grep -c 'Admin:.*admin123' "$SUBJ" || true)"
+if [ "$banner_hits" = 0 ]; then
+  ok "the Credentials banner no longer prints the retired admin credential ($banner_hits hits)"
+else
+  bad "the Credentials banner no longer prints the retired admin credential" \
+      "found $banner_hits hit(s) of 'Admin:.*admin123' in $SUBJ"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 2 - RED. The new mechanism-pointer text must appear exactly once.
+# ---------------------------------------------------------------------------
+mech_hits="$(grep -c 'Admin:.*provision-actors.ts' "$SUBJ" || true)"
+if [ "$mech_hits" = 1 ]; then
+  ok "the banner names the provisioning mechanism instead of a value ($mech_hits hit)"
+else
+  bad "the banner names the provisioning mechanism instead of a value" \
+      "expected 1 hit, got $mech_hits"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 3 - CONTROL (green on both trees). Issuer line untouched.
+# ---------------------------------------------------------------------------
+issuer_hits="$(grep -c 'Issuer:  demo@secuura.io / demo123' "$SUBJ" || true)"
+if [ "$issuer_hits" = 1 ]; then
+  ok "CONTROL - issuer line untouched (demo@secuura.io still authenticates)"
+else
+  bad "CONTROL - issuer line untouched" \
+      "expected 1 hit, got $issuer_hits"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 4 - CONTROL (green on both trees). Script parses under bash -n.
+# ---------------------------------------------------------------------------
+if bash -n "$SUBJ" >/dev/null 2>&1; then
+  ok "start-secuura.sh parses (bash -n)"
+else
+  bad "start-secuura.sh parses (bash -n)" \
+      "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"
+fi
+
+printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
+# A cell that never ran is not a pass: the ratio must add up.
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+  printf '  INCOMPLETE - %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
