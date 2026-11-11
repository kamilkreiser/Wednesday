# READY — KS-1163-O145-P2 (spark-dsv4flash, briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2/out.md.checker/patch.diff`** (from `ls` at 01:05 2026-11-12; sha256[:16] 5d45727f4aca25fd, 2544 B; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2/out.md.checker/section_3.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made. Run's own golden_cmp.out [verbatim]: `golden tree 8c12d017489b5371d3cb3ca0fec8f4f9c8e22df5 · patch tree 8c12d017489b5371d3cb3ca0fec8f4f9c8e22df5 -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2_`.

**Held 01:05 2026-11-12 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `cb46c28eef6f6aa761111f4737e53f3de1e43d74`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 2 test(s): 2 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at cb46c28eef6f6aa761111f4737e53f3de1e43d74, Start_Up/start-secuura.sh and Blockchain/Dev/scripts/__tests__/stack_env.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Start_Up/start-secuura.sh', 'Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh', 'Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Start_Up/start-secuura.sh } + { Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh , Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (3 files: 1 product(s) + 2 test(s)); reference test `Blockchain/Dev/scripts/__tests__/stack_env.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of start-secuura.sh are '-' lines, no stays-site removed; all 3 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 3 brief `+` line(s) among the product sections' `+` lines (multiset; 1 NON-ASCII chars); must_change sites 0/0 of `Start_Up/start-secuura.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Start_Up/start-secuura.sh 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh 1 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services/KS-1163.md`]: `File:` lines == product_files ['Start_Up/start-secuura.sh']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh', 'Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Start_Up/start-secuura.sh` (+3/-1 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh` (+1/-6 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 3 `section_3.diff` → `Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh` (+1/-1 counted from the applied section file; git-apply options per `section_3.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — start_secuura_expected_services.test.sh=RED(rc 1, 2 FAIL) start_secuura_slot_names.test.sh=RED(rc 1, 8 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): start_secuura_expected_services.test.sh(5 pass) start_secuura_slot_names.test.sh(23 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh` (modified) — B4 [verbatim]: `B4 start_secuura_expected_services.test.sh (RED) with the test edits alone: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red FAIL lines: ['FAIL no default-profile long-running service is missing from EXPECTED_SUFFIXES (compose has it, script does not wait)', 'FAIL EXPECTED_SUFFIXES count equals the derived set']] · B5 [verbatim]: `B5 start_secuura_expected_services.test.sh after every product section: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0`
- RED test `Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh` (modified) — B4 [verbatim]: `B4 start_secuura_slot_names.test.sh (RED) with the test edits alone: rc=1 fail_lines=8 pass_lines=15 load_error=0 timeout=0` [red FAIL lines: ['FAIL slot 2: health wait sees all 32 containers (no 120 s timeout)', 'FAIL slot 2: inspects 32 distinct secuura-s2-* names (positive control for the next case)', 'FAIL slot 1: health wait sees all 32 containers', 'FAIL slot 1: inspects 32 distinct secuura-* names', 'FAIL slot 1 --status: reports 32/32 running, 32 healthy', 'FAIL slot 1 --status: inspects 32 distinct secuura-* names', 'FAIL slot 3 --status: reports 32/32 running, 32 healthy', 'FAIL slot 3 --status: inspects 32 distinct secuura-s3-* names']] · B5 [verbatim]: `B5 start_secuura_slot_names.test.sh after every product section: rc=0 fail_lines=0 pass_lines=23 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (8 suite(s): bootstrap_env_slot_ports.test.sh 51p/0f->51p/0f; ks1355_slot_blind_launchers.test.sh 78p/0f->78p/0f; ks1413_start_banners_print_no_demo_password.test.sh 4p/0f->4p/0f; restore_local_secrets.test.sh 0p/0f->0p/0f; stack_env.test.sh 25p/0f->25p/0f; stack_guard.test.sh 27p/0f->27p/0f; start_secuura_banner.test.sh 4p/0f->4p/0f; start_secuura_marker_unknown_warning.test.sh 5p/0f->5p/0f;)` [8 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=4 ok=4 bad=0 skipped_newfile=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=1 tests=2 red=2 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Start_Up/start-secuura.sh` (+3/-1) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh` (MODIFIED, RED, +1/-6), `Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh` (MODIFIED, RED, +1/-1); 3 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `cb46c28eef6f6aa761111f4737e53f3de1e43d74` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2/input.json`. Brief (given by --brief): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services/KS-1163.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1163_o145_p1_start_secuura_waits_for_the_five_unwaited_services-r2/checker.out`.

```diff
--- a/Start_Up/start-secuura.sh
+++ b/Start_Up/start-secuura.sh
@@ -60,7 +60,7 @@
 BOLD='\033[1m'
 NC='\033[0m'
 
-# Expected services (27 total — secuura-midnight removed in the KS-312 cut)
+# Expected services (32 total — secuura-midnight removed in the KS-312 cut; the last five added by KS-1163)
 # KS-1096: these are SUFFIXES, prefixed with STACK_PREFIX below. They used to be
 # slot 1's bare names (`secuura-postgres`, ...), while docker-compose.local.yml
 # names every container `${STACK_PREFIX}-<svc>` — `secuura-sN-<svc>` on slot N.
@@ -79,6 +79,8 @@
   issuer-frontend verifier-frontend
   admin-frontend status-frontend
   website-frontend tokenomics-website
+  demo-service mcp-server pgbouncer
+  tenant-provisioning tokenisation
 )
 # Derived once, after stack_env.sh (sourced above) has exported STACK_PREFIX —
 # `secuura` on slot 1, so slot 1's names are byte-identical to before. Filled
--- a/Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh
@@ -47,12 +47,7 @@
 # reason. Anything here that is no longer declared in compose fails the test —
 # an exception for a service that does not exist is a stale exception.
 KNOWN_UNWAITED=(
-  stack-marker          # KS-666 ownership marker; a label carrier, not a service
-  demo-service          # KS-1163: never in the KS-312 list of 27; wait-or-not is Kamil's call — remove this line when KS-1163 decides
-  mcp-server            # KS-1163, as above
-  pgbouncer             # KS-1163, as above
-  tenant-provisioning   # KS-1163, as above
-  tokenisation          # KS-1163, as above
+  stack-marker          # KS-666 ownership marker; a label carrier, not a service (the five KS-1163 services are waited for, not excepted)
 )
 
 expect() {
--- a/Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh
@@ -43,7 +43,7 @@
 pg_port()    { echo $(( BASE_PG    + 100 * ($1 - 1) )); }
 redis_port() { echo $(( BASE_REDIS + 100 * ($1 - 1) )); }
 prefix_of()  { if (( $1 > 1 )); then echo "secuura-s$1"; else echo "secuura"; fi; }
-readonly EXPECTED_COUNT=27   # the script's EXPECTED_SERVICES size (KS-312 cut)
+readonly EXPECTED_COUNT=32   # the script's EXPECTED_SERVICES size (KS-312 cut, plus the five KS-1163 services)
 
 # KS-786 / KS-1016: strip every variable stack_env.sh honours with `${VAR:-…}`
 # before running a case, measured under `env -i` exactly as stack_env.test.sh
```

> NOTE (operator o145, 2026-11-12): bash_patch2, 3 files (start-secuura.sh + the KS-1096 suite + the start_secuura_slot_names sibling typed count 27 to 32). Kam RULED option (a) 2026-09-22 (ticket comment). Model wrote it TREE-IDENTICAL. First control FAILED B6 on the sibling suite (checker caught my brief gap; sibling declared). First real PASS refused by hold_ready (B3x unmeasured: a pure-deletion test hunk has no plus line; one comment clause added; re-run). UNMEASURED: the five healthchecks on a real stack start.
