# READY — KS-1558-TICKETEDEXCEPTIONS-1 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1558_p1/out.md.checker/patch.diff`** (from `ls` at 10:23 2026-10-20; sha256[:16] 79088739140e24a8, 4441 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1558_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1558_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; DIFFERS from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1558_p1-control/out.md.checker/patch.diff` (`cmp` rc 1): file headers differ (run ['+++ b/Blockchain/Dev/scripts/check-stack-safety.sh', '+++ b/Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh'] vs golden ['+++ b/Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh', '+++ b/Blockchain/Dev/scripts/check-stack-safety.sh']); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0 — read the diff before raising.

**Held 10:23 2026-10-20 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1558_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cd63883c62a9bb0e66969df8cd3f02db2b9b2217`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at cd63883c62a9bb0e66969df8cd3f02db2b9b2217, Blockchain/Dev/scripts/check-stack-safety.sh and Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-stack-safety.sh', 'Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-stack-safety.sh , Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-stack-safety.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 15 brief `+` line(s) present; script `+` lines 15 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 2/2 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-stack-safety.sh` (+15/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh` (+28/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh fails at the untouched tip (rc=1, 3 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=3 pass_lines=18 load_error=0 timeout=0` [red_first.out re-count: 3 FAIL line(s), 18 pass line(s); FAIL lines: ['FAIL RED KS-1558 R1: every LAUNCHER_EXCEPTIONS entry names a KS-nnn or PS-nnn ticket', "FAIL RED KS-1558 R2: the gate names a ticketless exception when Akto's two tickets are removed", 'FAIL RED KS-1558 R3: a bare KS- with no number is not a ticket']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 21 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=21 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 21 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive check-stack-safety.sh: no NEW failure after (3 suite(s))` [3 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-stack-safety.sh` (+15/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh` (+28/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cd63883c62a9bb0e66969df8cd3f02db2b9b2217` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1558_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1558_p1/KS-1558.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1558_p1/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-stack-safety.sh
+++ b/Blockchain/Dev/scripts/check-stack-safety.sh
@@ -166,4 +166,4 @@
   "observability/scripts/observability.sh|KS-200: a standalone stack with its own compose file, started only from observability/. It is not the platform stack."
-  "systemTest/akto/scripts/start.sh|Akto's own side-stack. systemTest/slot-target.sh namespaces its project, ports and volumes per slot instead."
-  "systemTest/akto/scripts/assert-compose-project.sh|Akto's own side-stack: a read-only assertion over its compose project name."
+  "systemTest/akto/scripts/start.sh|KS-666: Akto's own side-stack. systemTest/slot-target.sh namespaces its project, ports and volumes per slot instead."
+  "systemTest/akto/scripts/assert-compose-project.sh|KS-687: Akto's own side-stack: a read-only assertion over its compose project name."
 )
@@ -190,2 +190,15 @@
 _cands="$(_launcher_candidates)"
+# KS-1558 m4: every exception names a TICKET, not only a reason. The ruling was "a reason AND a ticket per entry";
+# the reason check below only asks for non-empty text, so two entries went in without one. A KS-nnn or PS-nnn token
+# anywhere in the reason satisfies this. It sits outside the census branch on purpose: the census can match nothing.
+_ticketless=""
+for _e in "${LAUNCHER_EXCEPTIONS[@]}"; do
+  case "${_e#*|}" in *KS-[0-9]*|*PS-[0-9]*) ;; *) _ticketless="$_ticketless ${_e%%|*}" ;; esac
+done
+if [[ -n "$_ticketless" ]]; then
+  fail "LAUNCHER_EXCEPTIONS entr(ies) cite no ticket (KS-1558):$_ticketless" \
+    "Write path|KS-nnn: reason. An exception with no ticket has no owner to retire it."
+else
+  ok
+fi
 if [[ -z "$_cands" ]]; then
--- a/Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh
@@ -117,2 +117,30 @@
 
+# --- KS-1558 m4: every LAUNCHER_EXCEPTIONS entry cites a ticket (KS-nnn or PS-nnn) ----------
+# The rule was "a reason AND a ticket per entry"; the reason check only asked for non-empty text.
+# Entries are read from the array in the real file; the gate itself is run on COPIES whose two
+# systemTest/akto entries have their ticket tokens removed or replaced, so no tracked file is touched.
+_entries="$(sed -n '/^LAUNCHER_EXCEPTIONS=(/,/^)/p' "$SAFETY" | grep '|')"
+expect "CONTROL KS-1558 the exception array was read (5 entries)" "5" "$(printf '%s\n' "$_entries" | grep -c '|')"
+expect "RED KS-1558 R1: every LAUNCHER_EXCEPTIONS entry names a KS-nnn or PS-nnn ticket" "0" \
+  "$(printf '%s\n' "$_entries" | grep -vcE 'KS-[0-9]|PS-[0-9]')"
+mkdir -p "$FIX/gate/Dev/scripts"
+cp "$SAFETY" "$FIX/gate/Dev/scripts/check-stack-safety.sh"
+bash "$FIX/gate/Dev/scripts/check-stack-safety.sh" >"$FIX/gate_pristine.out" 2>&1
+sed -e 's/KS-666: Akto/Akto/' -e 's/KS-687: Akto/Akto/' "$SAFETY" > "$FIX/gate/Dev/scripts/check-stack-safety.sh"
+bash "$FIX/gate/Dev/scripts/check-stack-safety.sh" >"$FIX/gate_stripped.out" 2>&1
+expect "CONTROL KS-1558 the gate copy with every ticket intact says nothing about a missing ticket" "no" \
+  "$(saw 'cite no ticket' "$(cat "$FIX/gate_pristine.out")")"
+expect "RED KS-1558 R2: the gate names a ticketless exception when Akto's two tickets are removed" "yes yes" \
+  "$(saw 'cite no ticket' "$(cat "$FIX/gate_stripped.out")") $(saw 'systemTest/akto/scripts/start.sh' "$(grep 'cite no ticket' "$FIX/gate_stripped.out")")"
+sed -e 's/KS-666: Akto/PS-12: Akto/' -e 's/KS-687: Akto/PS-9: Akto/' "$SAFETY" > "$FIX/gate/Dev/scripts/check-stack-safety.sh"
+bash "$FIX/gate/Dev/scripts/check-stack-safety.sh" >"$FIX/gate_ps.out" 2>&1
+expect "CONTROL KS-1558 a PS-nnn ticket counts as a ticket as well as a KS-nnn one" "no" \
+  "$(saw 'cite no ticket' "$(cat "$FIX/gate_ps.out")")"
+sed -e 's/KS-666: Akto/KS-: Akto/' -e 's/KS-687: Akto/PS-9: Akto/' "$SAFETY" > "$FIX/gate/Dev/scripts/check-stack-safety.sh"
+bash "$FIX/gate/Dev/scripts/check-stack-safety.sh" >"$FIX/gate_bare.out" 2>&1
+expect "RED KS-1558 R3: a bare KS- with no number is not a ticket" "yes" \
+  "$(saw 'systemTest/akto/scripts/start.sh' "$(grep 'cite no ticket' "$FIX/gate_bare.out")")"
+expect "CONTROL KS-1558 the gate still names only the stripped entries (KS-1550 and KS-200 entries keep theirs)" "no no" \
+  "$(saw 'start-environment.sh' "$(grep 'cite no ticket' "$FIX/gate_stripped.out")") $(saw 'observability.sh' "$(grep 'cite no ticket' "$FIX/gate_stripped.out")")"
+
 echo ""
```
