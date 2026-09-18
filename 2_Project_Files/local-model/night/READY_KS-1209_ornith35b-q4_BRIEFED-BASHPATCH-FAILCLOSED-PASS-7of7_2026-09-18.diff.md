# READY — KS-1209 (Ornith, briefed, BASH tier) — PASS 7/7 on the FIRST attempt, HELD for QA

**Held 2026-09-18 11:2x by the 10:0x Wednesday seat, after a source read** (below).

| field | value |
|---|---|
| ticket | KS-1209: preflight's closing verdict blames the environment even when other legs genuinely failed |
| run | `runs/2026-09-18_ks1209-ornith35b-night` (first attempt; no retry needed) |
| tier | **bash_patch**: one script hunk set + one new `*.test.sh` |
| product | `Blockchain/Dev/scripts/preflight/preflight.sh` (tip blob `28d3636c1…`, 753 lines) |
| new test | `Blockchain/Dev/scripts/__tests__/preflight_verdict_names_real_failures.test.sh` |
| tip | develop `207716440e2a6282b90ed2a118614d9cf98bee1e` |
| verdict | **PASS (7/7)**, `red_first=yes`, `apply_mode=lenient` (hunk counts recounted, which is harmless) |

## Checker evidence
- **B4 RED-FIRST:** the new test fails at the untouched tip (rc 1, 1 FAIL line).
- **B5 GREEN-AFTER:** it passes with the hunk (rc 0, 4 pass lines). **B5a:** the script still parses (`bash -n`).
- **B6: the four sibling suites that drive `preflight.sh` show no new failure.** The brief-writer had explicitly said
  it could NOT run these (they need the whole tree); **the checker ran them.** That closes the brief's one declared gap.

## My own source read
**The fix is fail-closed by construction, which is the property that matters in a pre-push gate.**
- Hunk 1: `_leg_concluded` records a leg that set `fail=1` into `FAILED_LEGS`.
- Hunk 2: `step()` calls `_leg_concluded` **first**, *then* accumulates `fail_total |= fail` and resets `fail=0`.
  The order is correct: the leg is recorded before its flag is cleared.
- Hunk 3: before the verdict, `fail` is **folded back** to the whole-run value (`fail_total | fail`), then any failing
  leg other than an env-only leg 1 produces `PREFLIGHT FAILED on leg(s) …` and `exit 1`.
  **Because `fail` is folded back before the original verdict logic, the new block can only ADD an earlier, better
  named `exit 1`. It can't turn a failing run into a passing one.** A gate change that could loosen the gate
  would be the dangerous kind; this one can't.

**The load-bearing assumption, MEASURED rather than trusted:** resetting `fail` per leg is safe only if nothing reads it
mid-run. The brief claimed it's read in one place. **Counted at the tip: exactly ONE read of `$fail`, at `:688`**
(with a positive control; the other hits are all assignments `fail=1`). So no leg body can observe the per-leg
reset. (Checked specifically because "read in only one place" is an absence claim, and I had two of those
wrong today.) `set -u` safety: every new variable is read with a default (`${FAILED_LEGS:-}`, `${fail_total:-0}`, `${env_fail:-0}`).

## Scope note
**Refs KS-1209, not Closes.** The ticket's Polish item (`lock-discovery.mjs` saying "missing expires" for a malformed value)
is a different file and isn't addressed here.

## Status
**HELD.** Not raised, not gated, not merged. It touches the **pre-push gate every developer runs**, so its QA gate
should confirm the verdict wording change breaks no human or tool that greps it (the brief found none; confirm it).

---
## The diff, verbatim

```diff
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -151,3 +151,5 @@ _leg_concluded() {
     [ "$CURRENT_LEG" = "?" ] && return 0
+    # KS-1209: a leg that set fail=1 is recorded by number, so the verdict can name it.
+    [ "$fail" -ne 0 ] && FAILED_LEGS="${FAILED_LEGS:-} $CURRENT_LEG"
     case " $SKIPPED_STACK $SKIPPED_ADVISORY " in
         *" $CURRENT_LEG "*) return 0 ;;   # it declared a skip — not a run
     esac
@@ -163,4 +165,6 @@ step() {
     _leg_concluded
+    # KS-1209: fail is per-leg from here on; fail_total keeps the run's result.
+    fail_total=$(( ${fail_total:-0} | fail )); fail=0
     CURRENT_LEG="${1%%/*}"
     _hdr_total="${1#*/}"; _hdr_total="${_hdr_total%% *}"
     if [ "$_hdr_total" != "$TOTAL_LEGS" ]; then
@@ -685,2 +689,18 @@ n_ran=$(printf '%s' "$RAN_LEGS" | wc -w | tr -d ' ')
 _leg_concluded
+# KS-1209: fold the per-leg flag back in, then name the legs that failed for REAL.
+# Leg 1 is left out only when it failed because the tree has no workspace install
+# (env_fail); a run whose ONLY failure is that keeps the environment verdict below.
+fail=$(( ${fail_total:-0} | fail ))
+real_failed=""
+for _leg in ${FAILED_LEGS:-}; do
+    if [ "$_leg" = "1" ] && [ "${env_fail:-0}" -ne 0 ]; then continue; fi
+    real_failed="$real_failed $_leg"
+done
+if [ -n "$real_failed" ]; then
+    echo "PREFLIGHT FAILED on leg(s)$real_failed - fix the above before pushing."
+    if [ "${env_fail:-0}" -ne 0 ]; then
+        echo "  Leg 1 also could not RUN (no workspace install): run npm ci in Blockchain/Dev as well."
+    fi
+    exit 1
+fi
 n_ran=$(printf '%s' "$RAN_LEGS" | wc -w | tr -d ' ')

--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/preflight_verdict_names_real_failures.test.sh
@@ -0,0 +1,75 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for preflight's closing verdict when leg 1 cannot run (KS-1209)
+# =============================================================================
+# When leg 1 found no workspace install, the closing verdict called the whole
+# run "an environment condition, not a finding about your change" even when
+# another leg had failed for real. These cases build a harness from
+# preflight.sh's OWN lines - its state, its step() and _leg_concluded()
+# helpers, and its closing verdict - drive all the legs through step() exactly
+# as the script does, and read the verdict. No leg body runs: no npm, no node,
+# no network, no stack.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/preflight_verdict_names_real_failures.test.sh
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
+tmp="$(mktemp -d "${TMPDIR:-/tmp}/ks1209-verdict.XXXXXX")"
+trap 'rm -rf "$tmp"' EXIT INT TERM
+
+# The product's own lines. helpers.sh: from `fail=0` up to the first leg (state
+# and helper functions). verdict.sh: from `n_stack=$(` to the end of the file.
+awk '/^fail=0$/{on=1} /^step "1\//{on=0} on' "$PREFLIGHT" > "$tmp/helpers.sh"
+awk '/^n_stack=\$\(/{on=1} on' "$PREFLIGHT" > "$tmp/verdict.sh"
+
+# run_legs <legs that fail for real, space-separated> <1 when leg 1 has no install, else 0>
+# Every leg goes through the script's own step(); sets RC and writes $tmp/out.txt.
+run_legs() {
+  local real="$1" nodeps="$2"
+  {
+    printf 'set -uo pipefail\nGATEWAY=http://127.0.0.1:9\n'
+    cat "$tmp/helpers.sh"
+    printf 'n=1\nwhile [ "$n" -le "$TOTAL_LEGS" ]; do\n  step "$n/$TOTAL_LEGS  leg $n"\n'
+    printf '  if [ "$n" = 1 ] && [ %s = 1 ]; then fail=1; env_fail=1; fi;\n' "$nodeps"
+    printf '  case " %s " in *" $n "*) fail=1 ;; esac\n' "$real"
+    printf '  n=$((n + 1))\ndone\n'
+    cat "$tmp/verdict.sh"
+  } > "$tmp/run.sh"
+  bash "$tmp/run.sh" > "$tmp/out.txt" 2>&1
+  RC=$?
+}
+
+has() { if grep -q -F -- "$1" "$tmp/out.txt"; then echo yes; else echo no; fi; }
+
+expect "CONTROL the harness holds preflight's own step() and its closing verdict" "yes yes" \
+  "$(grep -q '^step() {' "$tmp/helpers.sh" && echo yes || echo no) $(grep -q 'PREFLIGHT FAILED' "$tmp/verdict.sh" && echo yes || echo no)"
+
+run_legs "" 0
+expect "CONTROL a run where nothing fails exits 0 and says PREFLIGHT PASSED" "0 yes" "$RC $(has 'PREFLIGHT PASSED')"
+
+run_legs "" 1
+expect "CONTROL leg 1 without an install and NOTHING else failed keeps the environment verdict and exits 1" "1 yes" "$RC $(has 'environment condition')"
+
+run_legs "7" 1
+expect "🔴 leg 1 without an install plus a real leg-7 failure names leg 7 and does not blame the environment" "1 yes no" \
+  "$RC $(has 'leg(s) 7') $(has 'environment condition')"
+
+echo ""
+echo "preflight_verdict_names_real_failures: $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ]
```
