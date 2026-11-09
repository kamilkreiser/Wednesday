# READY — KS-1794-KS-1794-O113-P1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials/out.md.checker/patch.diff`** (from `ls` at 10:25 2026-11-09; sha256[:16] 1c61132b9f30dfb5, 3156 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials-control/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 10:25 2026-11-09 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4e529633d0a19a3efe626adfe05684fbd964e595`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 4e529633d0a19a3efe626adfe05684fbd964e595, Blockchain/Dev/scripts/smoke-test.sh and Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/smoke-test.sh', 'Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/smoke-test.sh , Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/smoke-test.sh` (script) and `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 2 brief `+` line(s) present; script `+` lines 2 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/smoke-test.sh` (+2/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh` (+12/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=6 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 6 pass line(s); FAIL lines: ['FAIL RED KS-1794 a base URL with credentials: the secret is not printed anywhere in the output', 'FAIL RED KS-1794 a base URL with credentials: the target line shows scheme, host and port only']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 8 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=8 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 8 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive smoke-test.sh: no NEW failure after (3 suite(s))` [3 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/smoke-test.sh` (+2/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh` (+12/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4e529633d0a19a3efe626adfe05684fbd964e595` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1794_o113_p1_smoke_target_strips_credentials/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/smoke-test.sh
+++ b/Blockchain/Dev/scripts/smoke-test.sh
@@ -14,7 +14,8 @@
 
 # KS-1250: RUNBOOK 2.2 tells an operator to point this script at an environment with SMOKE_BASE_URL, but the script never read it, so a run could look like a check of kintsugi or demo while it checked localhost. An unset or empty value keeps the old default.
 GATEWAY="${SMOKE_BASE_URL:-http://localhost:6882}"
-echo "Smoke target: $GATEWAY"
+# KS-1794: the target is printed without any user:password@ part of the URL, so a token in SMOKE_BASE_URL is not written to a terminal or a CI log.
+echo "Smoke target: $(printf '%s' "$GATEWAY" | sed -E 's#^([A-Za-z][A-Za-z0-9+.-]*://)[^/@]*@#\1#')"
 # KS-1250 (ruled by Wednesday 2026-11-06 01:45Z): twelve checks below call the services on their own ports, http://localhost:60xx. Those ports exist
 # on the local stack only: the gateway routes none of timestamping, M365, VC issue, tokenisation, tenant provisioning or MCP, and a gateway URL such as
 # RUNBOOK 2.2's https://<prod-gateway-fqdn> carries no service ports. Before this, a run with SMOKE_BASE_URL set printed its target and then tested
--- a/Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh
@@ -83,6 +83,18 @@
 got="$(grep -c -F "Smoke target: http://localhost:6882" "$WORK/unset/out.txt")"
 if [ "$got" = "1" ]; then ok "CONTROL - the default run prints 'Smoke target: http://localhost:6882' once"; else bad "CONTROL - the default run prints 'Smoke target: http://localhost:6882' once" "want 1, got $got"; fi
 
+# RED (KS-1794) - credentials embedded in the base URL are not printed: the target line shows the URL without the user:password@ part.
+CRED_BASE="https://alice:s3cr3t-token@smoke-target.invalid:9999"
+build_fixture "$WORK/cred"; run_smoke "$WORK/cred" "$CRED_BASE"
+got="$(grep -c -F "s3cr3t-token" "$WORK/cred/out.txt")"
+if [ "$got" = "0" ]; then ok "RED KS-1794 a base URL with credentials: the secret is not printed anywhere in the output"; else bad "RED KS-1794 a base URL with credentials: the secret is not printed anywhere in the output" "want 0, got $got"; fi
+got="$(grep -c -F "Smoke target: https://smoke-target.invalid:9999" "$WORK/cred/out.txt")"
+if [ "$got" = "1" ]; then ok "RED KS-1794 a base URL with credentials: the target line shows scheme, host and port only"; else bad "RED KS-1794 a base URL with credentials: the target line shows scheme, host and port only" "want 1, got $got"; fi
+
+# CONTROL (KS-1794) - the request still goes to the credentialed base: only the printed line is scrubbed, not the URL the script calls.
+got="$([ "$(total_urls "$WORK/cred")" -gt 0 ] && echo some || echo none) $(urls_not_under "$WORK/cred" "$CRED_BASE")"
+if [ "$got" = "some 0" ]; then ok "CONTROL KS-1794 a base URL with credentials: every request still goes under the full base"; else bad "CONTROL KS-1794 a base URL with credentials: every request still goes under the full base" "want 'some 0', got '$got'"; fi
+
 printf '\n  %d passed, %d failed\n' "$pass" "$fail"
 [ "$fail" -eq 0 ] || exit 1
 exit 0
```
