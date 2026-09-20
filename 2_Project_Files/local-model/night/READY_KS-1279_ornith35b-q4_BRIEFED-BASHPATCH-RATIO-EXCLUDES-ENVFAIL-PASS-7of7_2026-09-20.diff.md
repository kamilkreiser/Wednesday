# READY — KS-1279 (Ornith, briefed, bash_patch) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = TWO SECTION FILES, NOT `patch.diff`:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1279-ornith35b-night/out.md.checker/section_1.diff` (product, `2 1 …/scripts/preflight/preflight.sh`, strict apply rc 0, header `@@ -701,7 +701,8 @@`) + `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1279-ornith35b-night/out.md.checker/section_2.diff` (test, `83 0 …/scripts/__tests__/preflight_ratio_excludes_leg1_no_install.test.sh`). Both EXIST (`ls` at 23:10 2026-09-20). **The concatenated `patch.diff` in the same dir is CORRUPT as a whole** (its first hunk header `@@ -702,6 +702,7 @@` undercounts, so `git apply` — strict OR `--recount` — swallows the second file's `--- /dev/null` header and reports `86 2` on ONE file). The checker graded the sections; the raise applies the sections. Same class as KS-1203's header miscount, in the multi-file costume.

**Held 23:10 2026-09-20 by the 21:2x Wednesday seat after a source read.** Tip `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`. ONE product line changed + ONE comment line in `preflight.sh` at `:704` (the four-space-indented `n_ran=` inside the real-failure branch; the stripped twin at `:711` is UNTOUCHED — it differs by indent and the checker's B5 caught a variant that edited it) + ONE new bash test (83 lines) on the KS-1260 harness. **`Refs KS-1279`, never a closing word** — the ticket's option 1 (`_note_skip SKIPPED_ADVISORY 1` at `:236-237`) is outside the harness and not briefed.

**What it fixes.** Preflight's "(N/15 legs ran)" counts leg 1 as run on a no-install tree because its no-install branch declares no skip; the ratio now subtracts `env_fail` from `n_ran`.

**Source read (Wednesday, same action):** the `-` line is byte-identical to `:704` at the tip; two `+` lines (a KS-1279 comment + the arithmetic) match the brief; sections' numstats 2/1 and 83/0.

**Checker (23:08–23:09):** `RESULT: PASS (7/7)`, B4 red-first `fail_lines=2 pass_lines=4`, B5 `pass_lines=6`, B6 8 sibling suites no new red. **Drafter's pre-queue measurements (scratch clone, `/bin/bash` 3.2.57):** test at tip 4/6 (both 🔴 red), with the fix 6/6, 8 sibling suites identical both trees, `bash -n` ok; golden PASS ×3; `test_only` → B3, `wrong_site_711` → B5, `always_minus_one` / `dropped_comment` → B3b.

**For the raise seat:** apply `section_1.diff` then `section_2.diff` (strict, each); numstat MUST read `2 1` on preflight.sh and `83 0` on the new test; run the bash test + the 8 sibling preflight suites; shellcheck informational; `Refs KS-1279`. Partition: disjoint from Seat B 10th's three PRs and Seat A's anchoring/**; bank for the next raise seat with KS-1234.

**NOT TESTED:** the real `preflight.sh` process on a no-install tree (the harness drives `step()`/verdict, the KS-1260 idiom); shellcheck (not installed).

---
## section_1.diff
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -701,7 +701,8 @@
 done
 if [ -n "$real_failed" ]; then
     # KS-1260: this early exit keeps KS-1046's ratio, so a real failure still names the legs that ran.
-    n_ran=$(printf '%s' "$RAN_LEGS" | wc -w | tr -d ' ')
+    # KS-1279: a leg 1 that could not RUN (no workspace install, env_fail) is not a leg that ran - the next line says so.
+    n_ran=$(( $(printf '%s' "$RAN_LEGS" | wc -w | tr -d ' ') - ${env_fail:-0} ))
     echo "PREFLIGHT FAILED on leg(s)$real_failed - fix the above before pushing. ($n_ran/$TOTAL_LEGS legs ran)"
     if [ "${env_fail:-0}" -ne 0 ]; then
         echo "  Leg 1 also could not RUN (no workspace install): run npm ci in Blockchain/Dev as well."

## section_2.diff
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/preflight_ratio_excludes_leg1_no_install.test.sh
@@ -0,0 +1,83 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS that preflight's legs-ran ratio excludes a leg 1 that could not RUN (KS-1279)
+# =============================================================================
+# On a run with no workspace install and a real failure elsewhere, preflight
+# prints "(12/15 legs ran)" and, on the next line, "Leg 1 also could not RUN".
+# The ratio counts leg 1 as run; by the script's own next line it did not.
+# These cases build the KS-1209 harness from preflight.sh's OWN lines - its
+# state, its step() and _leg_concluded() helpers, and its closing verdict -
+# drive all the legs through step(), and read the verdict. No leg body runs:
+# no npm, no node, no network.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/preflight_ratio_excludes_leg1_no_install.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+PREFLIGHT="$HERE/../preflight/preflight.sh"
+PASS=0
+FAIL=0
+
+expect() {
+  local desc="$1" want="$2" got="$3"
+  if [[ "$got" == "$want" ]]; then
+    PASS=$((PASS + 1)); printf 'ok   %s\n' "$desc"
+  else
+    FAIL=$((FAIL + 1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"
+  fi
+}
+
+tmp="$(mktemp -d "${TMPDIR:-/tmp}/ks1279-leg1.XXXXXX")"
+trap 'rm -rf "$tmp"' EXIT INT TERM
+
+# The product's own lines. helpers.sh: from `fail=0` up to the first leg (state
+# and helper functions). verdict.sh: from the `n_stack=` line to the end of the file.
+awk '/^fail=0$/{on=1} /^step "1\//{on=0} on' "$PREFLIGHT" > "$tmp/helpers.sh"
+awk 'index($0, "n_stack=") == 1 {on=1} on' "$PREFLIGHT" > "$tmp/verdict.sh"
+TOTAL="$(awk -F= '$1 == "TOTAL_LEGS" {print $2}' "$tmp/helpers.sh")"
+
+# run_legs <legs that fail for real> <legs that skip (stack not up)> <legs that fail with no install>, each space-separated.
+# Every leg goes through the script's own step(); a skipped leg calls the
+# script's own skip_stack; a no-install leg sets fail=1 and env_fail=1, as leg 1 does.
+# Sets RC and writes $tmp/out.txt.
+run_legs() {
+  local real="$1" skipped="$2" envfail="$3"
+  {
+    printf 'set -uo pipefail\nGATEWAY=http://127.0.0.1:9\n'
+    cat "$tmp/helpers.sh"
+    printf 'n=1\nwhile [ "$n" -le "$TOTAL_LEGS" ]; do\n  step "$n/$TOTAL_LEGS  leg $n"\n'
+    printf '  case " %s " in *" $n "*) skip_stack ;; esac\n' "$skipped"
+    printf '  case " %s " in *" $n "*) fail=1 ;; esac\n' "$real"
+    printf '  case " %s " in *" $n "*) fail=1; env_fail=1 ;; esac\n' "$envfail"
+    printf '  n=$((n + 1))\ndone\n'
+    cat "$tmp/verdict.sh"
+  } > "$tmp/run.sh"
+  bash "$tmp/run.sh" > "$tmp/out.txt" 2>&1
+  RC=$?
+}
+
+has() { if grep -q -F -- "$1" "$tmp/out.txt"; then echo yes; else echo no; fi; }
+
+expect "CONTROL the harness holds preflight's own state, step(), failure verdict and leg total" "yes yes yes yes" \
+  "$(grep -q '^fail=0$' "$tmp/helpers.sh" && echo yes || echo no) $(grep -q '^step() {' "$tmp/helpers.sh" && echo yes || echo no) $(grep -q 'PREFLIGHT FAILED on leg(s)' "$tmp/verdict.sh" && echo yes || echo no) $([ "${TOTAL:-0}" -gt 1 ] && echo yes || echo no)"
+
+run_legs "" "" "1"
+expect "CONTROL a leg-1 failure with no install and nothing else failing keeps the environment verdict and exits 1" "1 yes" "$RC $(has 'but leg 1 could not RUN')"
+
+run_legs "11" "3 4 5" ""
+expect "CONTROL a real leg-11 failure with legs 3 4 5 skipped on an installed tree counts twelve legs ran" "1 yes" "$RC $(has "($((TOTAL - 3))/$TOTAL legs ran)")"
+
+run_legs "11" "3 4 5" "1"
+expect "CONTROL a real leg-11 failure with legs 3 4 5 skipped and no install still says Leg 1 could not RUN and exits 1" "1 yes" "$RC $(has 'Leg 1 also could not RUN')"
+
+run_legs "11" "3 4 5" "1"
+expect "🔴 KS-1279 a real leg-11 failure with legs 3 4 5 skipped and no install counts leg 1 as NOT run - eleven legs ran" "1 yes" "$RC $(has "($((TOTAL - 4))/$TOTAL legs ran)")"
+
+run_legs "11" "3 4 5" "1"
+expect "🔴 KS-1279 the same run no longer prints the ratio that counted leg 1 as run" "1 no" "$RC $(has "($((TOTAL - 3))/$TOTAL legs ran)")"
+
+echo ""
+echo "preflight_ratio_excludes_leg1_no_install: $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ]
