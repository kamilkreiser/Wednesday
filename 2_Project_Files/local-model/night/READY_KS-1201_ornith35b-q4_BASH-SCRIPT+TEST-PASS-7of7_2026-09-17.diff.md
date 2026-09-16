# READY — KS-1201 (systemTest bootstrap_login_diagnosis.test.sh ends every login stub it starts: start_stub writes its pid to stub.pid, stop_stub reads it back when the subshell's STUB_PID never arrived; + NEW suite bootstrap_login_diagnosis_stub_survivors.test.sh, 2 red cells + control) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (08:42). Held by Wednesday at 09:15 AEST (the model finished 08:42; held late — ledger w=5 idle row). Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1201-ornith35b-night
# Source read by me (Wednesday): the model's script lines (2 '-', 11 '+') and the new suite's 108 lines IDENTICAL to the brief's fences (python compare, scratchpad cmp1201.py; a mutated copy unequal). Apply LENIENT for section 1 (--recount --ignore-whitespace: hunk header count only; content identical). B4 red-first 2 FAIL by assertion at 7e89318bc; B5 green 3 pass; B6 sibling suite no new failure. shellcheck not installed.
# PR NOTES: brief says "Closes KS-1201" — test tooling (systemTest), not service runtime; confirm §5f does not apply at GO. Not the ticket's prose shape (5 edits) — the 2-edit pid-file route; the ticket calls the shape the owner's choice (brief raise notes). Pinned at develop 7e89318bc; ps -ww measured on macOS only. Expected tier: 1 per brief (test harness that kills processes) — Wednesday's reading: tier 2 candidate (test-only tooling, no product surface); gate decides.

```diff
--- a/systemTest/__tests__/bootstrap_login_diagnosis.test.sh
+++ b/systemTest/__tests__/bootstrap_login_diagnosis.test.sh
@@ -40,7 +40,17 @@ STEP="$FIXTURES/pre-suite.ts"
 # shellcheck source=support/generated_guard.sh
 . "$HERE/support/generated_guard.sh"
 
 STUB_PID=""
-stop_stub() { if [ -n "$STUB_PID" ]; then kill "$STUB_PID" 2>/dev/null; wait "$STUB_PID" 2>/dev/null; STUB_PID=""; fi; }
+# KS-1201: every call site runs start_stub inside a command substitution, which is a subshell,
+# so the STUB_PID it set never reached this shell and neither this function nor the EXIT trap
+# killed anything (84 orphaned login stubs in 10 h on one machine). start_stub therefore also
+# writes the pid to stub.pid in the guard's scratch dir, and a STUB_PID this shell does not hold
+# is read back from there. The file is emptied once the stub is stopped, so no pid is killed twice.
+stop_stub() {
+  [ -n "$STUB_PID" ] || STUB_PID="$(cat "$GENERATED_GUARD_TMP/stub.pid" 2>/dev/null)"
+  if [ -n "$STUB_PID" ]; then kill "$STUB_PID" 2>/dev/null; wait "$STUB_PID" 2>/dev/null; STUB_PID=""; fi
+  : > "$GENERATED_GUARD_TMP/stub.pid"
+}
 # Chain onto the guard's EXIT trap rather than replacing it.
 trap 'stop_stub; generated_guard_restore' EXIT
 
@@ -48,7 +58,7 @@ trap 'stop_stub; generated_guard_restore' EXIT
 # Starts the stub answering login with $1 and prints its port.
 start_stub() { # $1=status
   local line
   STUB_LOGIN_STATUS="$1" node "$STUB" > "$GENERATED_GUARD_TMP/stub.out" 2>&1 &
-  STUB_PID=$!
+  STUB_PID=$!; printf '%s' "$STUB_PID" > "$GENERATED_GUARD_TMP/stub.pid"
   for _ in $(seq 1 50); do
     line="$(grep -m1 '^PORT=' "$GENERATED_GUARD_TMP/stub.out" 2>/dev/null || true)"
     [ -n "$line" ] && { printf '%s' "${line#PORT=}"; return 0; }

--- /dev/null
+++ b/systemTest/__tests__/bootstrap_login_diagnosis_stub_survivors.test.sh
@@ -0,0 +1,108 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS: bootstrap_login_diagnosis.test.sh ends every login stub it starts (KS-1201)
+# =============================================================================
+# The defect: each call site runs start_stub inside a command substitution, which
+# is a subshell, so the STUB_PID it sets never reaches the suite's own shell and
+# neither stop_stub nor the EXIT trap kills anything. Every run left its node
+# support/login_stub.mjs listeners behind (84 orphans in 10 h on one machine).
+#
+# These cells run COPIES of the suite and its support/ files inside a mktemp tree
+# whose unique name is the marker, with a stand-in npx first on PATH, so the
+# shipped pre-suite step is never run and nothing leaves loopback. A stub counts
+# only when its argv carries that marker, and the process table is written to a
+# file BEFORE it is searched, so the search never matches itself. Any survivor is
+# ended by its own pid (SIGTERM) when this file exits.
+#
+# Usage: bash systemTest/__tests__/bootstrap_login_diagnosis_stub_survivors.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUITE="$HERE/bootstrap_login_diagnosis.test.sh"
+STUB="$HERE/support/login_stub.mjs"
+GUARD="$HERE/support/generated_guard.sh"
+[ -f "$SUITE" ] || { echo "FATAL: suite not found at $SUITE" >&2; exit 2; }
+[ -f "$STUB" ] || { echo "FATAL: login stub not found at $STUB" >&2; exit 2; }
+[ -f "$GUARD" ] || { echo "FATAL: generated guard not found at $GUARD" >&2; exit 2; }
+command -v node >/dev/null 2>&1 || { echo "FATAL: node is required (the suite starts its stubs with it)" >&2; exit 2; }
+PASS=0; FAIL=0
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1201.XXXXXX")"
+MARK="$(basename "$WORK")"
+survivors() { # $1 = the copy's name; prints the pid of every stub still running from that copy
+  ps -A -ww -o pid= -o args= > "$WORK/ps.out"
+  awk -v m="$MARK/$1/systemTest/__tests__/support/login_stub.mjs" 'index($0, m) > 0 { print $1 }' "$WORK/ps.out"
+}
+end_survivors() {
+  for p in $(survivors full) $(survivors abandoned); do kill "$p" 2>/dev/null; done
+  rm -rf "$WORK"
+}
+trap end_survivors EXIT
+
+for copy in full abandoned; do
+  mkdir -p "$WORK/$copy/systemTest/__tests__/support" "$WORK/$copy/systemTest/fixtures"
+  cp "$SUITE" "$WORK/$copy/systemTest/__tests__/bootstrap_login_diagnosis.test.sh"
+  cp "$STUB" "$WORK/$copy/systemTest/__tests__/support/login_stub.mjs"
+  cp "$GUARD" "$WORK/$copy/systemTest/__tests__/support/generated_guard.sh"
+done
+mkdir -p "$WORK/bin" "$WORK/noseq"
+echo '#!/bin/sh' > "$WORK/bin/npx"
+echo 'echo "$API_BASE_URL" >> "$KS1201_TARGETS"' >> "$WORK/bin/npx"
+echo 'exit 0' >> "$WORK/bin/npx"
+echo '#!/bin/sh' > "$WORK/noseq/seq"
+echo 'exit 0' >> "$WORK/noseq/seq"
+chmod +x "$WORK/bin/npx" "$WORK/noseq/seq"
+
+: > "$WORK/full.targets"
+FIXTURES_DIR="$WORK/full/systemTest/fixtures" KS1201_TARGETS="$WORK/full.targets" PATH="$WORK/bin:$PATH" bash "$WORK/full/systemTest/__tests__/bootstrap_login_diagnosis.test.sh" > "$WORK/full.log" 2>&1
+FULL_RC=$?
+full_left=""
+for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
+  full_left="$(survivors full | wc -l | tr -d ' ')"
+  [ "$full_left" -eq 0 ] && break
+  sleep 0.1
+done
+
+: > "$WORK/abandoned.targets"
+FIXTURES_DIR="$WORK/abandoned/systemTest/fixtures" KS1201_TARGETS="$WORK/abandoned.targets" PATH="$WORK/noseq:$WORK/bin:$PATH" bash "$WORK/abandoned/systemTest/__tests__/bootstrap_login_diagnosis.test.sh" > "$WORK/abandoned.log" 2>&1
+ABANDONED_RC=$?
+abandoned_left=""
+for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
+  abandoned_left="$(survivors abandoned | wc -l | tr -d ' ')"
+  [ "$abandoned_left" -eq 0 ] && break
+  sleep 0.1
+done
+
+FULL_TARGETS="$(grep -c '^http://127.0.0.1:' "$WORK/full.targets")"
+FULL_SUMMARY="$(grep -c '^bootstrap_login_diagnosis.test.sh: ' "$WORK/full.log")"
+ABANDONED_NOPORT="$(grep -c 'stub did not report a port' "$WORK/abandoned.log")"
+ps -A -ww -o pid= -o args= > "$WORK/ps_self.out"
+PS_SEES_SELF="$(awk -v me="$$" '$1 == me' "$WORK/ps_self.out" | wc -l | tr -d ' ')"
+
+if [ "$full_left" -eq 0 ]; then
+  echo "PASS: every login stub a full run of the suite started is gone once it exits"; PASS=$((PASS+1))
+else
+  echo "FAIL: $full_left login stub(s) a full run of the suite started are still running after it exited (KS-1201)"; FAIL=$((FAIL+1))
+fi
+
+if [ "$abandoned_left" -eq 0 ]; then
+  echo "PASS: a stub whose start was abandoned (exit 2) is ended by the EXIT trap"; PASS=$((PASS+1))
+else
+  echo "FAIL: $abandoned_left stub(s) from an abandoned start are still running after the suite exited $ABANDONED_RC - the EXIT trap killed nothing (KS-1201)"; FAIL=$((FAIL+1))
+fi
+
+if [ "$PS_SEES_SELF" -eq 1 ] && [ "$FULL_TARGETS" -eq 5 ] && [ "$FULL_SUMMARY" -eq 1 ] && [ "$ABANDONED_RC" -eq 2 ] && [ "$ABANDONED_NOPORT" -eq 1 ]; then
+  echo "PASS: CONTROL ps lists this shell, the full run reached all 5 steps and its summary, the abandoned start exited 2"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL a count of 0 would mean nothing: ps-sees-self=$PS_SEES_SELF, full rc=$FULL_RC targets=$FULL_TARGETS summary=$FULL_SUMMARY, abandoned rc=$ABANDONED_RC no-port=$ABANDONED_NOPORT"; FAIL=$((FAIL+1))
+fi
+
+if [ $((PASS+FAIL)) -ne 3 ]; then
+  echo "FAIL: INCOMPLETE - $((PASS+FAIL)) of 3 cells ran"; FAIL=$((FAIL+1))
+fi
+
+echo ""
+echo "bootstrap_login_diagnosis_stub_survivors: $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ]
```
