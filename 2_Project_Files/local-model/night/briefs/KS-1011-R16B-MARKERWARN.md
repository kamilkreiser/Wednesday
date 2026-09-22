# KS-1011 R16B-MARKERWARN - re-brief at develop 8c2f7b3fd of READY_KS-1011_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 10:25:10 AEST by Wednesday's feed9 drafter under the FEED 8 ruling; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip (KS-1081: one hunk corrected to the old brief's intent - see the drafter's note), every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
The KS-666 stack marker answers *"what is this stack running?"* through four container labels
(`com.secuura.stack.owner` / `.branch` / `.commit` / `.started_at`). `docker-compose.local.yml:50-55`
resolves each from an env var with an `unknown` default, and `start-secuura.sh` sets all four — so via
this script the labels are right. **Labels are baked at container CREATE time**, so a stack that came
up any other way carries `unknown` for the life of those containers: Docker Desktop restoring
`restart: unless-stopped` containers after a reboot (the routine case — it is how the stack comes up
after every restart), or a plain `docker compose up -d`. A later run of this script cannot repair
them. On 2026-09-08 all four read `unknown` on the live stack and four platform suites were run
against it with no staleness bound. **This task: option b — the script WARNS, loudly and by name, when
it sees running containers whose marker reads `unknown`, and prints the recreate command. It must NOT
fail the start.** NOT in this task: the compose files, the marker container, the `:-unknown` defaults
(they are deliberate — `:?required` would break plain `docker compose config` for anyone who has not
exported the vars).

## The exact change - 1 hunk(s) in `Start_Up/start-secuura.sh` (0 '-' line(s), 14 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
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
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)

* `:719` - (correct) `echo -e "    Branch:   $STACK_BRANCH @ $STACK_COMMIT"` - stays
* `:720` - (correct) `echo -e "    Started:  $STACK_STARTED_AT (UTC)"` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh`

File: `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (56 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh`, ONE hunk header `@@ -0,0 +1,56 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TEST: KS-1011 guard presence and shape in start-secuura.sh
# =============================================================================
# Verifies that the warning block added by KS-1011 is present in the script,
# names itself correctly, prints the recreate command, does not exit non-zero,
# and leaves the existing KS-666 lease line intact. Reads the file as text only.
# No Docker daemon, no compose, no network.
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
START="${START_SH:-$REPO_ROOT/Start_Up/start-secuura.sh}"
[ -f "$START" ] || { echo "FATAL: not found: $START"; exit 2; }
PASS=0; FAIL=0

SRC="$(cat "$START")"

if printf '%s' "$SRC" | grep -q 'com.secuura.stack.owner'; then
  echo "PASS: the marker guard reads the stack.owner label"; PASS=$((PASS+1))
else
  echo "FAIL: no reference to com.secuura.stack.owner in $START"; FAIL=$((FAIL+1))
fi

if printf '%s' "$SRC" | grep -q 'WARNING (KS-1011)'; then
  echo "PASS: the guard WARNS by name"; PASS=$((PASS+1))
else
  echo "FAIL: no 'WARNING (KS-1011)' line in $START"; FAIL=$((FAIL+1))
fi

if printf '%s' "$SRC" | grep -q 'force-recreate'; then
  echo "PASS: the guard prints the recreate remedy"; PASS=$((PASS+1))
else
  echo "FAIL: the guard does not name 'docker compose ... --force-recreate'"; FAIL=$((FAIL+1))
fi

if printf '%s' "$SRC" | grep -q 'KS-1011'; then
  if printf '%s' "$SRC" | sed -n '/KS-1011/,$p' | grep -q 'exit 1'; then
    echo "FAIL: the KS-1011 guard can fail the start (an 'exit 1' follows it)"; FAIL=$((FAIL+1))
  else
    echo "PASS: the guard warns without failing the start"; PASS=$((PASS+1))
  fi
else
  echo "FAIL: no KS-1011 guard in $START"; FAIL=$((FAIL+1))
fi

if printf '%s' "$SRC" | grep -q 'Owner:    \$STACK_OWNER'; then
  echo "PASS: CONTROL the KS-666 lease line is intact"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL the KS-666 lease line was disturbed"; FAIL=$((FAIL+1))
fi

echo ""; echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `echo "PASS: the marker guard reads the stack.owner label"; PASS=$((PASS+1))`
- `echo "PASS: the guard WARNS by name"; PASS=$((PASS+1))`
- `echo "PASS: the guard prints the recreate remedy"; PASS=$((PASS+1))`
- `echo "PASS: the guard warns without failing the start"; PASS=$((PASS+1))`
- `echo "PASS: CONTROL the KS-666 lease line is intact"; PASS=$((PASS+1))`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Start_Up/start-secuura.sh` / `+++ b/Start_Up/start-secuura.sh` (1 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh` (one hunk, `@@ -0,0 +1,56 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed9 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 10:25:10 AEST)
- `Start_Up/start-secuura.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Start_Up/start-secuura.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/start_secuura_expected_services.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x; FEED 9 inherits it) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed9-drafter-precheck/MARKERWARN/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1011 on the Secuura board at 2026-09-22 10:25:10 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
