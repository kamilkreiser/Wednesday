# READY — KS-1047-1047STACKLEGS-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1047-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 10:29 2026-09-22; sha256[:16] 129ffdfd8aa17643, 4522 B — a BYTE count; NOTE — `cat section_*.diff | cmp patch.diff` rc 1, differing by 4 line(s); the checker REWROTE section_1.diff; patch.diff is the model's AS-WRITTEN block, the SECTION FILES are the applied units and the canonical for the raise: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1047-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1047-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_1.diff: REANCHORED (hunk 1: reanchored at 268 (1 '-' / 1 '+' lines; model header -266,6 +266,6);reanchored 1/1 hunk(s););` — STRICT APPLY NOT CLAIMED for the whole patch: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/STACKLEGS/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4522 B vs golden 4520 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (pre-push 2, pre_push_stack_legs_comment.test.sh 74); context/empty lines run vs golden: pre-push 6/5 context; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 10:29 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1047-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1047STACKLEGS-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, .githooks/pre-push and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['.githooks/pre-push', 'Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { .githooks/pre-push , Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `.githooks/pre-push` (script) and `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `.githooks/pre-push` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: NON-EMPTY: `hunk @@ -266,6 +266,6 @@ echo "[pre-push] Blo declared old=6 new=6 actual old=7 new=7 (+1 trailing empty)`; `section_1.diff.check.out` (strict --check): EMPTY (clean); checker-REWRITTEN: REANCHORED (applied file = the reanchored hunks; as-written kept at section_1.diff.as-written))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh` (+74/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL the stale leg enumeration (3, 4, 7) is gone from pre-push', 'FAIL the comment points at the verdict line (KS-1046) instead of enumerating legs']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive pre-push: no NEW failure after (7 suite(s))` [7 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `.githooks/pre-push` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh` (+74/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — the CHECKER-REWRITTEN file, not the fence; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1047-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['1047', 'STACKLEGS', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1047-R16B-STACKLEGS.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1047-ornith35b-night/checker.out`.

```diff
--- a/.githooks/pre-push
+++ b/.githooks/pre-push
@@ -266,6 +266,6 @@ echo "[pre-push] Blockchain/Dev changes detected → running preflight gate (bypass
 # Safe on macOS bash 3.2: the script uses no bash-4 constructs (no mapfile/readarray,
 # no associative arrays, no ${x^^}).
-# KS-691: source slot-target.sh first so the stack-dependent legs (3, 4, 7) probe
+# KS-691: source slot-target.sh first so the stack-dependent legs (the ones the preflight verdict lists as SKIPPED when the stack is down - KS-1046; not enumerated here, an enumeration drifts) probe
 # THIS slot's gateway. preflight.sh defaults GATEWAY to localhost:6882 (slot 1),
 # so from any other slot those legs either silently SKIP (slot 1 down) — the push
 # passes having probed nothing — or probe SLOT 1 and report success for a stack
 
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh
@@ -0,0 +1,74 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for .githooks/pre-push line :268 comment - stale leg enumeration gone, pointer present (KS-1047)
+# =============================================================================
+# The defect at tip `48e65c435`: line 268 enumerates legs "(3, 4, 7)" which is
+# wrong (measured 2026-09-09 they are 3, 4, 8). The fix drops the enumeration
+# and points at the verdict line instead. These four cells prove that.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=4
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SUBJ="${PRE_PUSH_HOOK-$REPO_ROOT/.githooks/pre-push}"
+[ -f "$SUBJ" ] || { echo "FATAL: pre-push hook not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: PRE_PUSH_HOOK is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# ---------------------------------------------------------------------------
+# CELL 1 - KS-1047 RED. THE STALE ENUMERATION IS GONE.
+# ---------------------------------------------------------------------------
+stale_hits="$(grep -c '(3, 4, 7)' "$SUBJ" || true)"
+if [ "$stale_hits" = 0 ]; then
+  ok "the stale leg enumeration (3, 4, 7) is gone from pre-push"
+else
+  bad "the stale leg enumeration (3, 4, 7) is gone from pre-push" \
+      "count=$stale_hits (expected 0)"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 2 - KS-1047 RED. THE COMMENT POINTS AT THE VERDICT LINE (KS-1046), NOT LEGS.
+# ---------------------------------------------------------------------------
+ptr_hits="$(grep -c 'KS-1046' "$SUBJ" || true)"
+if [ "$ptr_hits" = 1 ]; then
+  ok "the comment points at the verdict line (KS-1046) instead of enumerating legs"
+else
+  bad "the comment points at the verdict line (KS-1046) instead of enumerating legs" \
+      "count=$ptr_hits (expected 1)"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 3 - CONTROL. THE KS-691 RATIONALE COMMENT IS STILL THERE.
+# ---------------------------------------------------------------------------
+anchor_hits="$(grep -c 'KS-691: source slot-target.sh first so the stack-dependent legs' "$SUBJ" || true)"
+if [ "$anchor_hits" = 1 ]; then
+  ok "the KS-691 rationale comment anchor is still present in pre-push"
+else
+  bad "the KS-691 rationale comment anchor is still present in pre-push" \
+      "count=$anchor_hits (expected 1)"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 4 - CONTROL. PRE-PUSH PARSes (bash -n).
+# ---------------------------------------------------------------------------
+if bash -n "$SUBJ" >/dev/null 2>&1; then
+  ok "pre-push parses (bash -n)"
+else
+  bad "pre-push parses (bash -n)" "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"
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

**APPLIED `section_1.diff` (REANCHORED (applied file = the reanchored hunks; as-written kept at section_1.diff.as-written)) — byte for byte:**
```diff
--- a/.githooks/pre-push
+++ b/.githooks/pre-push
@@ -265,7 +265,7 @@
 # KS-487 session note above. `bash <file>` needs no exec bit.
 # Safe on macOS bash 3.2: the script uses no bash-4 constructs (no mapfile/readarray,
 # no associative arrays, no ${x^^}).
-# KS-691: source slot-target.sh first so the stack-dependent legs (3, 4, 7) probe
+# KS-691: source slot-target.sh first so the stack-dependent legs (the ones the preflight verdict lists as SKIPPED when the stack is down - KS-1046; not enumerated here, an enumeration drifts) probe
 # THIS slot's gateway. preflight.sh defaults GATEWAY to localhost:6882 (slot 1),
 # so from any other slot those legs either silently SKIP (slot 1 down) — the push
 # passes having probed nothing — or probe SLOT 1 and report success for a stack
```
