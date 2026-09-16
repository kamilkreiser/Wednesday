# READY — KS-1040 PART ONLY (preflight leg 4: a sweep that could NOT RUN, exit 2, is reported as such instead of as an unroutable path; the gate still refuses) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on RETRY-ONCE (first sample FAIL B3b). Held by Wednesday at 22:49 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1040-ornith35b-night (the diff below is retry/out.md).
# Source read by me (Wednesday): the script hunk is the brief's ONE '-' (:299) → six '+' byte-for-byte (paths_rc=$? first in the else; case 2 → 'could NOT RUN'; * → the old message); 'fail=1' untouched below; B5a bash -n ok; the new suite red at the tip (rc 1, 2 FAIL) and 5/5 after; B6 all 4 sibling suites that drive preflight.sh show no new failure.
# PR NOTES for the raising seat: PARTIAL — the ticket's reset-time half needs path-resolvability.mjs (a second file), so KS-1040 stays OPEN after merge. Premise (exit 2 on a refused login) measured against a local fake server by the searcher, not on a live gateway.

```diff
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -296,7 +296,12 @@ if curl -sf -o /dev/null "$GATEWAY/health" 2>/dev/null; then
     elif node scripts/preflight/path-resolvability.mjs --base "$GATEWAY"; then
         echo "OK — every published path routes to a handler"
     else
-        echo "FAIL — a published path is unroutable (KS-473 class)"
+        paths_rc=$?
+        # KS-1040: path-resolvability.mjs exits 2 when the sweep could not RUN (login refused, spec unreadable) and 1 on a real finding.
+        case "$paths_rc" in
+            2) echo "FAIL — the path sweep could NOT RUN (exit 2, see the 'Sweep aborted' line above): nothing was measured, so this is not a routing finding (KS-1040)" ;;
+            *) echo "FAIL — a published path is unroutable (KS-473 class)" ;;
+        esac
         fail=1
     fi
 else
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh
@@ -0,0 +1,97 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for preflight.sh leg 4 — a sweep that could not RUN is not a routing
+# finding (KS-1040)
+# =============================================================================
+# path-resolvability.mjs exits 1 when a published path answered "Route ... not
+# found" and exits 2 when the sweep could not run at all (spec unreadable, or the
+# login refused — HTTP 429 from the IP-scoped login limiter on 2026-09-09). Leg 4
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
+# 🔴 CELL 1 — exit 2 is reported as a sweep that could not run
+if echo "$OUT2" | grep -qF 'could NOT RUN'; then
+  ok "🔴 exit 2 is reported as a sweep that could NOT RUN"
+else
+  bad "🔴 exit 2 is reported as a sweep that could NOT RUN" "leg 4 printed no 'could NOT RUN' line for exit 2"
+fi
+
+# 🔴 CELL 2 — exit 2 does not claim an unroutable path
+if echo "$OUT2" | grep -qF 'a published path is unroutable'; then
+  bad "🔴 exit 2 does not claim a published path is unroutable" "leg 4 printed the routing verdict for a sweep that never ran"
+else
+  ok "🔴 exit 2 does not claim a published path is unroutable"
+fi
+
+# CONTROL CELL 3 — exit 2 still refuses the push
+if echo "$OUT2" | grep -qx 'LEG4_FAIL=1'; then
+  ok "CONTROL exit 2 still sets fail=1 (the gate refuses)"
+else
+  bad "CONTROL exit 2 still sets fail=1 (the gate refuses)" "fail was not 1 after exit 2"
+fi
+
+# CONTROL CELL 4 — exit 1 is still the routing finding, and refuses
+if echo "$OUT1" | grep -qF 'a published path is unroutable' && echo "$OUT1" | grep -qx 'LEG4_FAIL=1'; then
+  ok "CONTROL exit 1 reports a published path is unroutable and sets fail=1"
+else
+  bad "CONTROL exit 1 reports a published path is unroutable and sets fail=1" "exit 1 lost its routing verdict or its refusal"
+fi
+
+# CONTROL CELL 5 — exit 0 passes (and proves the leg's block was extracted)
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
+  echo "  INCOMPLETE — $((pass + fail)) of $TOTAL_CELLS cells ran"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
