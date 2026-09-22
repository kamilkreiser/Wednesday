# READY — KS-1011-MARKERWARN-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1011-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 11:13 2026-09-22; sha256[:16] bc6f28e5047bad41, 3666 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1011-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1011-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1011-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/MARKERWARN/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 11:13 2026-09-22 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1011-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1011MARKERWARN-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Start_Up/start-secuura.sh and Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Start_Up/start-secuura.sh', 'Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Start_Up/start-secuura.sh , Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Start_Up/start-secuura.sh` (script) and `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 14 brief `+` line(s) present; script `+` lines 14 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 0; must_change sites 0/0 each a `-` line; must_remove 0 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Start_Up/start-secuura.sh` (+14/-0 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh` (+56/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh fails at the untouched tip (rc=1, 4 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=4 pass_lines=1 load_error=0 timeout=0` [red_first.out re-count: 4 FAIL line(s), 1 pass line(s); FAIL lines: ['FAIL: no reference to com.secuura.stack.owner in /private/tmp/claude-501/night/clone_ks1011/Start_Up/start-secuura.sh', "FAIL: no 'WARNING (KS-1011)' line in /private/tmp/claude-501/night/clone_ks1011/Start_Up/start-secuura.sh", "FAIL: the guard does not name 'docker compose ... --force-recreate'", 'FAIL: no KS-1011 guard in /private/tmp/claude-501/night/clone_ks1011/Start_Up/start-secuura.sh']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive start-secuura.sh: no NEW failure after (4 suite(s))` [4 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Start_Up/start-secuura.sh` (+14/-0 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh` (+56/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1011-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['MARKERWARN', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1011-R16B-MARKERWARN.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1011-ornith35b-night/checker.out`.

```diff
--- a/Start_Up/start-secuura.sh
+++ b/Start_Up/start-secuura.sh
@@ -719,4 +719,18 @@ echo -e "  ${BOLD}Stack lease (KS-666):${NC}"
 echo -e "    Branch:   $STACK_BRANCH @ $STACK_COMMIT"
 echo -e "    Started:  $STACK_STARTED_AT (UTC)"
 echo ""
+# KS-1011 (Kam 2026-09-16, option b): marker labels are baked at container CREATE
+# time, so a stack brought up any other way than this script - Docker Desktop
+# restoring `restart: unless-stopped` containers after a reboot, or a plain
+# `docker compose up -d` - carries "unknown" for the life of those containers, and
+# a later run of this script cannot repair them. Warn loudly and name the remedy;
+# never fail the start over it.
+if [[ -n "$_SLOT_IDS" ]]; then
+  _MARKER_UNKNOWN=$(docker inspect --format '{{index .Config.Labels "com.secuura.stack.owner"}}' $_SLOT_IDS 2>/dev/null | grep -c '^unknown$' || true)
+  if [[ "$_MARKER_UNKNOWN" -gt 0 ]]; then
+    echo -e "  ${BOLD}WARNING (KS-1011):${NC} $_MARKER_UNKNOWN of $TOTAL_CONTAINERS running containers report stack.owner=unknown."
+    echo "    They were created outside this script, so their KS-666 marker labels cannot be repaired in place."
+    echo "    Recreate them to restore the marker:  docker compose -f $COMPOSE_FILE up -d --force-recreate"
+  fi
+fi
 announce_lease "started"
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh
@@ -0,0 +1,56 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TEST: KS-1011 guard presence and shape in start-secuura.sh
+# =============================================================================
+# Verifies that the warning block added by KS-1011 is present in the script,
+# names itself correctly, prints the recreate command, does not exit non-zero,
+# and leaves the existing KS-666 lease line intact. Reads the file as text only.
+# No Docker daemon, no compose, no network.
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+START="${START_SH:-$REPO_ROOT/Start_Up/start-secuura.sh}"
+[ -f "$START" ] || { echo "FATAL: not found: $START"; exit 2; }
+PASS=0; FAIL=0
+
+SRC="$(cat "$START")"
+
+if printf '%s' "$SRC" | grep -q 'com.secuura.stack.owner'; then
+  echo "PASS: the marker guard reads the stack.owner label"; PASS=$((PASS+1))
+else
+  echo "FAIL: no reference to com.secuura.stack.owner in $START"; FAIL=$((FAIL+1))
+fi
+
+if printf '%s' "$SRC" | grep -q 'WARNING (KS-1011)'; then
+  echo "PASS: the guard WARNS by name"; PASS=$((PASS+1))
+else
+  echo "FAIL: no 'WARNING (KS-1011)' line in $START"; FAIL=$((FAIL+1))
+fi
+
+if printf '%s' "$SRC" | grep -q 'force-recreate'; then
+  echo "PASS: the guard prints the recreate remedy"; PASS=$((PASS+1))
+else
+  echo "FAIL: the guard does not name 'docker compose ... --force-recreate'"; FAIL=$((FAIL+1))
+fi
+
+if printf '%s' "$SRC" | grep -q 'KS-1011'; then
+  if printf '%s' "$SRC" | sed -n '/KS-1011/,$p' | grep -q 'exit 1'; then
+    echo "FAIL: the KS-1011 guard can fail the start (an 'exit 1' follows it)"; FAIL=$((FAIL+1))
+  else
+    echo "PASS: the guard warns without failing the start"; PASS=$((PASS+1))
+  fi
+else
+  echo "FAIL: no KS-1011 guard in $START"; FAIL=$((FAIL+1))
+fi
+
+if printf '%s' "$SRC" | grep -q 'Owner:    \$STACK_OWNER'; then
+  echo "PASS: CONTROL the KS-666 lease line is intact"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL the KS-666 lease line was disturbed"; FAIL=$((FAIL+1))
+fi
+
+echo ""; echo "PASS=$PASS FAIL=$FAIL"
+[ "$FAIL" -eq 0 ]
```
