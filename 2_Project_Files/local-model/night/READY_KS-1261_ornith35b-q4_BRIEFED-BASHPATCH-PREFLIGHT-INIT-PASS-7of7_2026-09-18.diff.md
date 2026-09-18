# READY — KS-1261 (Ornith, briefed, bash_patch) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1261-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.opts`.**

**Held 2026-09-18 15:53 by the 14:4x Wednesday seat after a source read.** Tip `8b9c3f022`. Product `Blockchain/Dev/scripts/preflight/preflight.sh` — **the pre-push gate every author runs: say so in the PR body.** Brief `night/briefs/KS-1261.md` (search round 2).

## Source read
- Adds `FAILED_LEGS=""` and `fail_total=0` under `fail=0` (:94). At the tip both are only READ (:154, :168, :693, :695, each with a `:-` default), so a caller's exported value reached the verdict.
- The 3 '+' lines are IDENTICAL to the brief (python compare: 0 missing, 0 extra). B1-B6 PASS incl. B6: the 5 sibling suites that drive preflight.sh show no NEW failure.
- **Do not brief KS-1260 (same file, verdict region) until this merges.**
**HELD. Not raised.** Refs KS-1261, linkKind contributes.

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -94,3 +94,6 @@ GATEWAY="${GATEWAY_URL:-http://localhost:6882}"
 fail=0
+# KS-1261: start the run state clean, so a FAILED_LEGS or fail_total exported by the caller cannot reach the verdict.
+FAILED_LEGS=""
+fail_total=0
 env_fail=0   # KS-991: leg 1 could not RUN (no workspace install) vs a real finding
 
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/preflight_state_is_initialised.test.sh
@@ -0,0 +1,77 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS that preflight's run state starts clean whatever the caller exported (KS-1261)
+# =============================================================================
+# preflight.sh read FAILED_LEGS and fail_total with their own defaults but never
+# initialised them, so a FAILED_LEGS exported by the caller turned a clean run
+# into a false red naming a leg that never failed, and fail_total=abc aborted
+# the verdict. These cases build the KS-1209 harness from preflight.sh's OWN
+# lines - its state, its step() and _leg_concluded() helpers, and its closing
+# verdict - drive all the legs through step(), and run it under a caller
+# environment. No leg body runs: no npm, no node, no network, no stack.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/preflight_state_is_initialised.test.sh
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
+tmp="$(mktemp -d "${TMPDIR:-/tmp}/ks1261-state.XXXXXX")"
+trap 'rm -rf "$tmp"' EXIT INT TERM
+
+# The product's own lines. helpers.sh: from `fail=0` up to the first leg (state
+# and helper functions). verdict.sh: from the `n_stack=` line to the end of the file.
+awk '/^fail=0$/{on=1} /^step "1\//{on=0} on' "$PREFLIGHT" > "$tmp/helpers.sh"
+awk 'index($0, "n_stack=") == 1 {on=1} on' "$PREFLIGHT" > "$tmp/verdict.sh"
+
+# run_legs <legs that fail for real, space-separated> [NAME=value ...]
+# Every leg goes through the script's own step(); the NAME=value pairs are the
+# caller's exported environment. Sets RC and writes $tmp/out.txt.
+run_legs() {
+  local real="$1"; shift
+  {
+    printf 'set -uo pipefail\nGATEWAY=http://127.0.0.1:9\n'
+    cat "$tmp/helpers.sh"
+    printf 'n=1\nwhile [ "$n" -le "$TOTAL_LEGS" ]; do\n  step "$n/$TOTAL_LEGS  leg $n"\n'
+    printf '  case " %s " in *" $n "*) fail=1 ;; esac\n' "$real"
+    printf '  n=$((n + 1))\ndone\n'
+    cat "$tmp/verdict.sh"
+  } > "$tmp/run.sh"
+  env "$@" bash "$tmp/run.sh" > "$tmp/out.txt" 2>&1
+  RC=$?
+}
+
+has() { if grep -q -F -- "$1" "$tmp/out.txt"; then echo yes; else echo no; fi; }
+
+expect "CONTROL the harness holds preflight's own state, step() and closing verdict" "yes yes yes" \
+  "$(grep -q '^fail=0$' "$tmp/helpers.sh" && echo yes || echo no) $(grep -q '^step() {' "$tmp/helpers.sh" && echo yes || echo no) $(grep -q 'PREFLIGHT FAILED' "$tmp/verdict.sh" && echo yes || echo no)"
+
+run_legs ""
+expect "CONTROL a clean run with nothing exported exits 0 and says PREFLIGHT PASSED" "0 yes" "$RC $(has 'PREFLIGHT PASSED')"
+
+run_legs "7" FAILED_LEGS=
+expect "CONTROL a real leg-7 failure is still named and still exits 1" "1 yes" "$RC $(has 'leg(s) 7')"
+
+run_legs "" FAILED_LEGS=7
+expect "🔴 a clean run with FAILED_LEGS=7 exported still passes and names no leg" "0 yes no" \
+  "$RC $(has 'PREFLIGHT PASSED') $(has 'leg(s)')"
+
+run_legs "" fail_total=abc
+expect "🔴 a clean run with fail_total=abc exported still passes" "0 yes" "$RC $(has 'PREFLIGHT PASSED')"
+
+echo ""
+echo "preflight_state_is_initialised: $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ]
```
