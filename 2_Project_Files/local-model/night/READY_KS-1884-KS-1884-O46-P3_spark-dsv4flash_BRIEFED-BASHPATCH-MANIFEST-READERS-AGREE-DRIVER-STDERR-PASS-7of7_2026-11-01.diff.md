# READY — KS-1884-KS-1884-O46-P3 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p3_ks1884_readers_agree_driver_stderr/out.md.checker/patch.diff`** (from `ls` at 21:55 2026-11-01; sha256[:16] 5b215981de6d6de3, 6633 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p3_ks1884_readers_agree_driver_stderr/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p3_ks1884_readers_agree_driver_stderr/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p3_ks1884_readers_agree_driver_stderr-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 6633 B vs golden 6906 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (manifest_readers_agree.test.sh 15, manifest_readers_agree_stderr.test.sh 77); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 21:55 2026-11-01 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p3_ks1884_readers_agree_driver_stderr/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d7691f35312ea158f043e87a3227e477cccb183d`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at d7691f35312ea158f043e87a3227e477cccb183d, systemTest/__tests__/manifest_readers_agree.test.sh and systemTest/__tests__/manifest_path.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['systemTest/__tests__/manifest_readers_agree.test.sh', 'systemTest/__tests__/manifest_readers_agree_stderr.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { systemTest/__tests__/manifest_readers_agree.test.sh , systemTest/__tests__/manifest_readers_agree_stderr.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `systemTest/__tests__/manifest_readers_agree.test.sh` (script) and `systemTest/__tests__/manifest_readers_agree_stderr.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `systemTest/__tests__/manifest_path.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 10 brief `+` line(s) present; script `+` lines 11 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 4; must_change sites 0/0 each a `-` line; must_remove 4 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `systemTest/__tests__/manifest_readers_agree.test.sh` (+11/-4 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `systemTest/__tests__/manifest_readers_agree_stderr.test.sh` (+77/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: systemTest/__tests__/manifest_readers_agree_stderr.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 2 pass line(s); FAIL lines: ["FAIL: the npx stub's stderr is not in the output of a failing run (rc=1)", "FAIL: the python3 stub's stderr is not in the output of a failing run (rc=1)"]]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: systemTest/__tests__/manifest_readers_agree_stderr.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive manifest_readers_agree.test.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=systemTest/__tests__/manifest_readers_agree_stderr.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `systemTest/__tests__/manifest_readers_agree.test.sh` (+11/-4 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `systemTest/__tests__/manifest_readers_agree_stderr.test.sh` (+77/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d7691f35312ea158f043e87a3227e477cccb183d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p3_ks1884_readers_agree_driver_stderr/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p3_ks1884_readers_agree_driver_stderr/checker.out`.

```diff
--- a/systemTest/__tests__/manifest_readers_agree.test.sh
+++ b/systemTest/__tests__/manifest_readers_agree.test.sh
@@ -43,17 +43,21 @@
+# KS-1884: each driver's stderr goes to its own file here (not /dev/null), so a FAIL can say why a driver answered nothing.
+ERR_DIR="$(mktemp -d "${TMPDIR:-/tmp}/readers-agree.XXXXXX")"
+trap 'rm -rf "$ERR_DIR"' EXIT
+
 writer() {
   ( cd "$PW" && env "${CLEAR[@]}" "$@" npx tsx -e \
     "import {manifestPath} from '../fixtures/manifest.ts'; import {basename} from 'node:path';
-     try { console.log(basename(manifestPath())); } catch (e) { console.log('ERROR'); }" 2>/dev/null | tail -1 )
+     try { console.log(basename(manifestPath())); } catch (e) { console.log('ERROR'); }" 2>"$ERR_DIR/writer" | tail -1 )
 }
 playwright() {
   ( cd "$PW" && env "${CLEAR[@]}" "$@" npx tsx -e \
     "import {manifestPathForThisSlot} from './config/actorManifest.ts'; import {basename} from 'node:path';
-     try { console.log(basename(manifestPathForThisSlot())); } catch (e) { console.log('ERROR'); }" 2>/dev/null | tail -1 )
+     try { console.log(basename(manifestPathForThisSlot())); } catch (e) { console.log('ERROR'); }" 2>"$ERR_DIR/playwright" | tail -1 )
 }
 performance() {
   # This reader resolves at IMPORT time, so the import itself is the thing under test.
   ( cd "$PERF" && env "${CLEAR[@]}" "$@" npx tsx -e \
-    "import('./runner/actor_manifest.ts').then(m => console.log(require('node:path').basename(m.manifestPath))).catch(() => console.log('ERROR'));" 2>/dev/null | tail -1 )
+    "import('./runner/actor_manifest.ts').then(m => console.log(require('node:path').basename(m.manifestPath))).catch(() => console.log('ERROR'));" 2>"$ERR_DIR/performance" | tail -1 )
 }
 schemathesis() {
   local py="$ST/.venv/bin/python"; [ -x "$py" ] || py="$(command -v python3)"
@@ -63,5 +67,5 @@
     import actor_manifest as m
     print(m.MANIFEST_PATH.name)
 except Exception:
-    print('ERROR')" 2>/dev/null | tail -1 )
+    print('ERROR')" 2>"$ERR_DIR/schemathesis" | tail -1 )
 }
@@ -75,5 +79,8 @@
     PASS=$((PASS+1)); echo "ok   $label -> $want"
   else
     FAIL=$((FAIL+1)); echo "FAIL $label — expected all four = '$want'; writer='$w' playwright='$p' performance='$f' schemathesis='$s'"
+    for _k in writer playwright performance schemathesis; do
+      [[ -s "$ERR_DIR/$_k" ]] && echo "     $_k stderr: $(head -c 400 "$ERR_DIR/$_k" | tr '\n' ' ')"
+    done
   fi
 }
--- /dev/null
+++ b/systemTest/__tests__/manifest_readers_agree_stderr.test.sh
@@ -0,0 +1,77 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for systemTest/__tests__/manifest_readers_agree.test.sh - a driver that answers nothing must
+# say why (KS-1884).
+# =============================================================================
+# The four driver functions end `2>/dev/null | tail -1`, so a tool that fails to start leaves an empty
+# answer and the FAIL line shows only `writer=''`: the reason is thrown away. The fix keeps each
+# driver's stderr in a file and prints it under a FAIL line.
+# Real bash, env and tail; `npx` and `python3` are STUBS on a private PATH (they print their noise to
+# stderr and nothing to stdout), so no tsx, no Python and no stack is needed. Nothing outside the temp
+# dir is written.
+# Usage: bash systemTest/__tests__/manifest_readers_agree_stderr.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${MANIFEST_READERS_AGREE_SH:-$HERE/manifest_readers_agree.test.sh}"
+SUPPORT="$HERE/support/slot-expect.sh"
+STACK_ENV="$HERE/../../Blockchain/Dev/scripts/stack_env.sh"
+for _f in "$SUBJ" "$SUPPORT" "$STACK_ENV"; do
+  [[ -r "$_f" ]] || { echo "FATAL: not readable: $_f" >&2; exit 2; }
+done
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/readers-stderr.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+REAL_GREP="$(command -v grep)"
+
+run_case() {   # $1 = case name, $2 = what the stubs print on stdout (may be empty) -> prints the subject's exit code
+  local f="$WORK/$1"
+  mkdir -p "$f/systemTest/__tests__/support" "$f/systemTest/playwright" "$f/systemTest/performance" \
+           "$f/systemTest/schemathesis/tests" "$f/Blockchain/Dev/scripts" "$f/bin"
+  cp "$SUBJ" "$f/systemTest/__tests__/manifest_readers_agree.test.sh"
+  cp "$SUPPORT" "$f/systemTest/__tests__/support/slot-expect.sh"
+  cp "$STACK_ENV" "$f/Blockchain/Dev/scripts/stack_env.sh"
+  printf '#!/bin/sh\necho "STUB-NPX-NOISE tsx failed to start" >&2\n[ -n "%s" ] && echo "%s"\nexit 1\n' "$2" "$2" > "$f/bin/npx"
+  printf '#!/bin/sh\necho "STUB-PY-NOISE python failed to start" >&2\n[ -n "%s" ] && echo "%s"\nexit 1\n' "$2" "$2" > "$f/bin/python3"
+  chmod +x "$f/bin/npx" "$f/bin/python3"
+  ( cd "$f" && PATH="$f/bin:$PATH" bash systemTest/__tests__/manifest_readers_agree.test.sh ) >"$WORK/$1.out" 2>&1
+  echo $?
+}
+
+RC_SILENT="$(run_case silent '')"
+RC_ERROR="$(run_case error 'ERROR')"
+
+# CELL 1 (RED at the tip) - the npx stub's stderr appears in the output of a failing run.
+if "$REAL_GREP" -qF 'STUB-NPX-NOISE' "$WORK/silent.out"; then
+  echo "PASS: a driver's stderr is printed on a FAIL (npx)"; PASS=$((PASS+1))
+else
+  echo "FAIL: the npx stub's stderr is not in the output of a failing run (rc=$RC_SILENT)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - the python3 stub's stderr (the schemathesis driver) appears too.
+if "$REAL_GREP" -qF 'STUB-PY-NOISE' "$WORK/silent.out"; then
+  echo "PASS: a driver's stderr is printed on a FAIL (python3)"; PASS=$((PASS+1))
+else
+  echo "FAIL: the python3 stub's stderr is not in the output of a failing run (rc=$RC_SILENT)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - drivers that answer nothing still fail the suite and still say FAIL.
+if [[ "$RC_SILENT" != "0" ]] && "$REAL_GREP" -q '^FAIL ' "$WORK/silent.out"; then
+  echo "PASS: CONTROL silent drivers still fail the suite with FAIL lines"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL silent drivers: rc=$RC_SILENT"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - stderr is printed only for a FAIL: no passing case carries it.
+if "$REAL_GREP" -q '^ok ' "$WORK/error.out" && ! "$REAL_GREP" '^ok ' "$WORK/error.out" | "$REAL_GREP" -q 'STUB-'; then
+  echo "PASS: CONTROL an ok line never carries driver stderr"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL ok lines: rc=$RC_ERROR, ok lines=$("$REAL_GREP" -c '^ok ' "$WORK/error.out")"; FAIL=$((FAIL+1))
+fi
+
+echo ""
+echo "Results: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 ]]
```
