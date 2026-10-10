# READY — KS-1417-KS-1417-ENVLOCALEXAMPLEDEADGATEWAYPORT-2 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p2-env-local-example-dead-gateway-port/out.md.checker/patch.diff`** (from `ls` at 19:04 2026-10-10; sha256[:16] 2199d5bcff79c49c, 1986 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p2-env-local-example-dead-gateway-port/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p2-env-local-example-dead-gateway-port/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; golden path `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-10_spark-screen/carve_1850/KS-1417-p2-env-local-example-dead-gateway-port/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 19:04 2026-10-10 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p2-env-local-example-dead-gateway-port/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `785cb671557a5cfc383946ccff410b9608c4b537`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 785cb671557a5cfc383946ccff410b9608c4b537, Blockchain/Dev/env.local.example and Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/env.local.example', 'Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/env.local.example , Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/env.local.example` (script) and `Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 3 brief `+` line(s) present; script `+` lines 3 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 0/0 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/env.local.example` (+3/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh` (+15/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh fails at the untouched tip (rc=1, 1 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=1 pass_lines=5 load_error=0 timeout=0` [red_first.out re-count: 1 FAIL line(s), 5 pass line(s); FAIL lines: ['FAIL: env.local.example still sets API_GATEWAY_PORT (nothing reads it)']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 6 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=6 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 6 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names env.local.example — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/env.local.example` (+3/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh` (+15/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `785cb671557a5cfc383946ccff410b9608c4b537` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p2-env-local-example-dead-gateway-port/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p2-env-local-example-dead-gateway-port/checker.out`.

```diff
--- a/Blockchain/Dev/env.local.example
+++ b/Blockchain/Dev/env.local.example
@@ -53,7 +53,9 @@
 # =============================================================================
 # SERVICE PORTS
 # =============================================================================
-API_GATEWAY_PORT=6882
+# The gateway's host port is GATEWAY_PORT, which scripts/stack_env.sh derives per slot.
+# Nothing is set here on purpose: a port written in this file would be a slot-1 literal.
+# KS-1417: this block used to set API_GATEWAY_PORT (6882), which nothing reads; it was copied into every clone's .env.
 ORIGINATE_PORT=6000
 PRISM_PORT=6001
 WALLET_PORT=6002
--- a/Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh
@@ -75,5 +75,20 @@
   echo "FAIL: CONTROL bootstrap rc=$BOOT_RC, .env present=$([[ -f "$TREE/.env" ]] && echo yes || echo NO)"; FAIL=$((FAIL+1))
 fi
 
+# CELL 5 (RED at the tip) - the local template (env.local.example, PIECE 2) does not set the dead key either.
+LOCAL="${ENV_LOCAL_EXAMPLE_SH:-$DEV_DIR/env.local.example}"
+if [[ -f "$LOCAL" ]] && ! has_dead_key "$LOCAL"; then
+  echo "PASS: env.local.example does not set API_GATEWAY_PORT"; PASS=$((PASS+1))
+else
+  echo "FAIL: env.local.example still sets API_GATEWAY_PORT (nothing reads it)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 6 (GREEN CONTROL, tip AND after) - env.local.example was really read: it keeps its heading and a neighbouring port.
+if [[ -f "$LOCAL" ]] && grep -qF '# SERVICE PORTS' "$LOCAL" && grep -qE '^ORIGINATE_PORT=' "$LOCAL"; then
+  echo "PASS: CONTROL env.local.example is present and keeps the SERVICE PORTS heading and ORIGINATE_PORT"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL env.local.example is missing, or lost the SERVICE PORTS heading or ORIGINATE_PORT"; FAIL=$((FAIL+1))
+fi
+
 echo "ks1417_env_example_no_dead_gateway_port: $PASS passed, $FAIL failed"
 [[ $FAIL -eq 0 ]]
```
