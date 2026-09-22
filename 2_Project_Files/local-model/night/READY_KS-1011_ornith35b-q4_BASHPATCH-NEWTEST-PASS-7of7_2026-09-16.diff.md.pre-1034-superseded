# READY — KS-1011 (KS-666 stack marker reads "unknown" whenever the stack is not started via start-secuura.sh — KAM RULED option b at 09:53: the script only WARNS, loudly and by name, and prints the recreate command; it must not fail the start) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r4, BASH_PATCH, NEW test file, tip develop M55 48e65c435 (G6 override verified against origin; Start_Up/ is untouched by Peter's #997, whose 36 files are all under systemTest/), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1011-ornith35b-night4
# Source read by me (Wednesday): the applied `after.sh` block is BYTE-FOR-BYTE the brief's 14 lines — six comment lines, the outer `if [[ -n "$_SLOT_IDS" ]]`, the one-line `docker inspect --format '{{index .Config.Labels "com.secuura.stack.owner"}}'` count, the inner `if`, three echo lines, two `fi`. It reuses `_SLOT_IDS` (:687) and `TOTAL_CONTAINERS` (:688) rather than re-querying Compose, and the KS-666 lease block above it is untouched (the suite's CONTROL cell asserts that line and is green at the tip AND after). B4 red-first is genuine: 4 FAIL lines at the untouched tip. B6: four sibling suites drive start-secuura.sh and none gained a failure.
# THREE EARLIER ROUNDS, ALL WEDNESDAY'S BRIEF DEFECTS, none the model's: r1 showed the file's CONTEXT lines inside the fenced block and the model copied one as a '+' (B3b); r2's retry dropped the backslash-continued `--format` line, so the `docker inspect` became ONE line deliberately; r3 described the test cells in prose and the model invented an `expect` helper whose third argument was a mutation, so every cell reported FAIL while the product hunk was already correct. r4 = literal cells in the brief, first sample, 7/7. The RETRY-ONCE trigger also gained B3b/B3c this round — it had listed only the vitest tier's stop points, so the bash tier had no retry at all.
# PR NOTES for the Sunday raising seat: (1) TWO files: `Start_Up/start-secuura.sh` (a 14-line insertion after :720) + the NEW suite `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh`; KS-1011 → Done, citing Kam's 09:53 ruling. (2) `Start_Up/start-secuura.sh` is ALSO the product file of KS-1163, whose edit is at :63-82 — far away, so the two apply together, but whichever is raised second rebases on the first. (3) The suite reads the script as TEXT: no Docker, no compose, consistent with its two siblings in that directory. (4) Accommodations the checker named: section_1 needed `--recount --ignore-whitespace`; the new-file header was RECOUNTED. Apply the sections as held here.

```diff
--- a/Start_Up/start-secuura.sh
+++ b/Start_Up/start-secuura.sh
@@ -717,6 +717,20 @@ echo -e "  ${BOLD}Stack lease (KS-666):${NC}"
 echo -e "    Branch:   $STACK_BRANCH @ $STACK_COMMIT"
 echo -e "    Started:  $STACK_STARTED_AT (UTC)"
 echo ""
+# KS-1011 (Kam 2026-09-16, option b): marker labels are baked at container CREATE
+# time, so a stack brought up any other way than this script — Docker Desktop
+# restoring `restart: unless-stopped` containers after a reboot, or a plain
+# `docker compose up -d` — carries "unknown" for the life of those containers, and
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
@@ -0,0 +1,62 @@
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
