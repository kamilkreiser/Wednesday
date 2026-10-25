# READY — KS-1560-KS-1560 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1560_p1/out.md.checker/patch.diff`** (from `ls` at 09:51 2026-10-26; sha256[:16] 8cbb0b071bba3158, 4194 B; NOTE — `cat section_*.diff | cmp patch.diff` rc 1: the SECTION FILES are the applied units: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1560_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1560_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_1.diff: --recount --ignore-whitespace needed;` — STRICT APPLY NOT CLAIMED: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1560_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made. Run's own golden_cmp.out [verbatim]: `golden tree a6af682eb22bc12114177655e72bd41359d6a9c8 · patch tree a6af682eb22bc12114177655e72bd41359d6a9c8 -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-26_ks_1560_p1_093900/*_cmp.index.out)`.

**Held 09:51 2026-10-26 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1560_p1/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480, Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh and Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh', 'Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh } + { Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 1 must_change site(s) of tenant_isolation_stderr_own_file.test.sh are '-' lines, no stays-site removed; all 6 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 6 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 1/1 of `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh 64 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1560_p1/KS-1560.md`]: `File:` lines == product_files ['Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` (+6/-1 counted from the applied section file; git-apply options per `section_1.diff.opts`: `--recount --ignore-whitespace`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): NON-EMPTY: `error: corrupt patch at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1560_p1/out.md.checker/section_1.diff:19`)
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh` (+64/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks1560_private_path_suites_link_jq.test.sh=RED(rc 1, 1 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks1560_private_path_suites_link_jq.test.sh(3 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh` (new) — B4 [verbatim]: `B4 ks1560_private_path_suites_link_jq.test.sh (RED) with the test edits alone: rc=1 fail_lines=1 pass_lines=2 load_error=0 timeout=0` [red FAIL lines: ['FAIL every private-PATH suite that checks jq links jq into its stub dir']] · B5 [verbatim]: `B5 ks1560_private_path_suites_link_jq.test.sh after every product section: rc=0 fail_lines=0 pass_lines=3 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (1 suite(s): tenant_isolation_stderr_own_file.test.sh 5p/0f->5p/0f;)` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=accommodated (see the B2 line)`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` (+6/-1) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh` (NEW, RED, +64/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1560_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1560_p1/KS-1560.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1560_p1/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh
@@ -26,5 +26,9 @@ REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
 JOB="$REPO_ROOT/Blockchain/Testing/jobs/06-tenant-isolation.sh"
 [ -f "$JOB" ] || { echo "FATAL: 06-tenant-isolation.sh not found at $JOB" >&2; exit 2; }
-command -v jq >/dev/null 2>&1 || { echo "FATAL: jq is not on PATH - the subject cannot run, so nothing here can be graded" >&2; exit 2; }
+# KS-1137 F-4 / KS-1560: the subject runs under a PRIVATE PATH ("$root/bin:/usr/bin:/bin"), so a jq check on the
+# OUTER PATH passes on a host whose jq is homebrew-only and the subject then reds with "jq: command not found".
+# Resolve jq once here and link it into each fixture's stub dir.
+JQ_BIN="$(command -v jq 2>/dev/null || true)"
+[ -n "$JQ_BIN" ] && [ -x "$JQ_BIN" ] || { echo "FATAL: jq could not be resolved on PATH - the subject cannot run, so nothing here can be graded" >&2; exit 2; }
 
 WORK="$(mktemp -d "${TMPDIR:-/tmp}/tenant06.XXXXXX")"
@@ -57,4 +61,5 @@ fi
 STUB
   chmod +x "$root/bin/node" "$root/bin/curl" "$root/bin/tsx"
+  ln -sf "$JQ_BIN" "$root/bin/jq"
 }
 
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh
@@ -0,0 +1,64 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for the shell suites in this directory - KS-1560 M1: a suite that checks
+# jq on the OUTER PATH but runs its subject under a PRIVATE PATH must link jq into
+# the fixture's stub dir.
+# =============================================================================
+# KS-1137 F-4 fixed three trivy suites, found by a filename census. The defect is
+# not trivy-shaped: any suite that preflights jq on one PATH and runs the subject
+# on "$root/bin:/usr/bin:/bin" false-reds on a host whose jq lives elsewhere
+# (homebrew). This census reads every sibling *.test.sh, selects the suites that
+# have BOTH a `command -v jq` check and a `$root/bin:` private PATH, and requires
+# each to carry the `bin/jq` link. It reads files only; nothing is run.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SELF="$(basename "${BASH_SOURCE[0]}")"
+PASS=0; FAIL=0
+
+check() {
+    local desc="$1" want="$2" got="$3"
+    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\n' "$desc"
+    else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
+}
+
+# in_census <suite file name>: prints 1 when the census holds it, else 0
+in_census() {
+    case " $census" in
+        *" $1 "*) echo 1 ;;
+        *) echo 0 ;;
+    esac
+}
+
+census=""      # suites with both a jq check and a private PATH
+offenders=""   # of those, the ones with no bin/jq link
+for f in "$HERE"/*.test.sh; do
+    name="$(basename "$f")"
+    [[ "$name" == "$SELF" ]] && continue
+    if grep -qF 'command -v jq' "$f" && grep -qF '$root/bin:' "$f"; then
+        census="${census}${name} "
+        grep -qF 'bin/jq' "$f" || offenders="${offenders}${name} "
+    fi
+done
+
+# --- CELL 0 (CONTROL): the census instrument sees the three trivy suites ---------
+trivy=0
+for n in container_trivy_exit_code_env_keeps_findings container_trivy_failed_scan_is_loud container_trivy_image_filter; do
+    trivy=$((trivy + $(in_census "$n.test.sh")))
+done
+check "CONTROL the census finds the three trivy suites" "3" "$trivy"
+
+# --- CELL 1 (CONTROL, tip AND after): the tenant-isolation suite is in the census ---------
+check "CONTROL the census includes tenant_isolation_stderr_own_file.test.sh" "1" \
+    "$(in_census tenant_isolation_stderr_own_file.test.sh)"
+
+# --- CELL 2 (RED at the tip): no census suite lacks the jq link ------------------
+check "every private-PATH suite that checks jq links jq into its stub dir" "" "${offenders% }"
+
+echo ""
+echo "ks1560_private_path_suites_link_jq: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
```
