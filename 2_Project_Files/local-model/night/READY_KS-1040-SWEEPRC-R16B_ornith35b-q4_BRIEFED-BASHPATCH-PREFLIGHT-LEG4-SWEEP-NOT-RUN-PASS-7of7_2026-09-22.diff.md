# READY — KS-1040-SWEEPRC-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1040-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 11:14 2026-09-22; sha256[:16] c27fe350366a0e62, 5348 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1040-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1040-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1040-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/SWEEPRC/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 11:14 2026-09-22 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1040-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1040SWEEPRC-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/scripts/preflight/preflight.sh and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/preflight/preflight.sh', 'Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/preflight/preflight.sh , Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/preflight/preflight.sh` (script) and `Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 6 brief `+` line(s) present; script `+` lines 6 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/preflight/preflight.sh` (+6/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh` (+97/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL RED exit 2 is reported as a sweep that could NOT RUN', 'FAIL RED exit 2 does not claim a published path is unroutable']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive preflight.sh: no NEW failure after (9 suite(s))` [9 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/preflight/preflight.sh` (+6/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh` (+97/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1040-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['SWEEPRC', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1040-R16B-SWEEPRC.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1040-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -303,7 +303,12 @@ if curl -sf -o /dev/null "$GATEWAY/health" 2>/dev/null; then
     elif node scripts/preflight/path-resolvability.mjs --base "$GATEWAY"; then
         echo "OK — every published path routes to a handler"
     else
-        echo "FAIL — a published path is unroutable (KS-473 class)"
+        paths_rc=$?
+        # KS-1040: path-resolvability.mjs exits 2 when the sweep could not RUN (login refused, spec unreadable) and 1 on a real finding.
+        case "$paths_rc" in
+            2) echo "FAIL -- the path sweep could NOT RUN (exit 2, see the 'Sweep aborted' line above): nothing was measured, so this is not a routing finding (KS-1040)" ;;
+            *) echo "FAIL -- a published path is unroutable (KS-473 class)" ;;
+        esac
         fail=1
     fi
 else
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh
@@ -0,0 +1,97 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for preflight.sh leg 4 - a sweep that could not RUN is not a routing
+# finding (KS-1040)
+# =============================================================================
+# path-resolvability.mjs exits 1 when a published path answered "Route ... not
+# found" and exits 2 when the sweep could not run at all (spec unreadable, or the
+# login refused - HTTP 429 from the IP-scoped login limiter on 2026-09-09). Leg 4
+# printed "a published path is unroutable" for BOTH exits, which sends the reader
+# to the OpenAPI spec for a login-budget problem. The leg must still REFUSE on
+# exit 2: a sweep that measured nothing has not passed.
+#
+# The leg's own block is cut out of preflight.sh by text (from its step line to
+# the next section marker) and run in a throwaway directory with curl, node and
+# the step helpers stubbed, so no gateway, no network and no node run is needed.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh
+#        PREFLIGHT_SH=/path/to/other/preflight.sh bash ...   (red-proof)
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=5
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${PREFLIGHT_SH:-$HERE/../preflight/preflight.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: preflight.sh not found at $SUBJ" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1040.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
+bad() { echo "  FAIL $1"; echo "       $2"; fail=$((fail + 1)); }
+
+mkdir -p "$WORK/scripts/preflight/node_modules/yaml"
+awk -v start='step "4/15' -v stop='# --- scripts/audit deps' 'index($0, stop) == 1 { on = 0 } index($0, start) == 1 { on = 1 } on' "$SUBJ" > "$WORK/leg4.sh"
+cat > "$WORK/stubs.sh" <<'STUBS'
+step() { echo "=== $1 ==="; }
+skip_stack() { echo "SKIP stack"; }
+skip_advisory() { echo "SKIP advisory $1"; }
+curl() { return 0; }
+node() { echo "stub sweep exiting $SWEEP_RC"; return "$SWEEP_RC"; }
+GATEWAY="http://127.0.0.1:9"
+fail=0
+STUBS
+
+run_leg4() {
+  ( cd "$WORK" && SWEEP_RC="$1" bash -c '. ./stubs.sh; . ./leg4.sh; echo "LEG4_FAIL=$fail"' 2>&1 )
+}
+
+OUT2="$(run_leg4 2)"
+OUT1="$(run_leg4 1)"
+OUT0="$(run_leg4 0)"
+
+# RED CELL 1 - exit 2 is reported as a sweep that could not run
+if echo "$OUT2" | grep -qF 'could NOT RUN'; then
+  ok "RED exit 2 is reported as a sweep that could NOT RUN"
+else
+  bad "RED exit 2 is reported as a sweep that could NOT RUN" "leg 4 printed no 'could NOT RUN' line for exit 2"
+fi
+
+# RED CELL 2 - exit 2 does not claim an unroutable path
+if echo "$OUT2" | grep -qF 'a published path is unroutable'; then
+  bad "RED exit 2 does not claim a published path is unroutable" "leg 4 printed the routing verdict for a sweep that never ran"
+else
+  ok "RED exit 2 does not claim a published path is unroutable"
+fi
+
+# CONTROL CELL 3 - exit 2 still refuses the push
+if echo "$OUT2" | grep -qx 'LEG4_FAIL=1'; then
+  ok "CONTROL exit 2 still sets fail=1 (the gate refuses)"
+else
+  bad "CONTROL exit 2 still sets fail=1 (the gate refuses)" "fail was not 1 after exit 2"
+fi
+
+# CONTROL CELL 4 - exit 1 is still the routing finding, and refuses
+if echo "$OUT1" | grep -qF 'a published path is unroutable' && echo "$OUT1" | grep -qx 'LEG4_FAIL=1'; then
+  ok "CONTROL exit 1 reports a published path is unroutable and sets fail=1"
+else
+  bad "CONTROL exit 1 reports a published path is unroutable and sets fail=1" "exit 1 lost its routing verdict or its refusal"
+fi
+
+# CONTROL CELL 5 - exit 0 passes (and proves the leg's block was extracted)
+if echo "$OUT0" | grep -qF 'every published path routes to a handler' && echo "$OUT0" | grep -qx 'LEG4_FAIL=0'; then
+  ok "CONTROL exit 0 reports every path routes and leaves fail=0"
+else
+  bad "CONTROL exit 0 reports every path routes and leaves fail=0" "the leg 4 block did not run from $SUBJ"
+fi
+
+echo ""
+echo "  $pass passed, $fail failed (of $TOTAL_CELLS cells)"
+# A cell that never ran is not a pass: the ratio must add up.
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+  echo "  INCOMPLETE - $((pass + fail)) of $TOTAL_CELLS cells ran"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
