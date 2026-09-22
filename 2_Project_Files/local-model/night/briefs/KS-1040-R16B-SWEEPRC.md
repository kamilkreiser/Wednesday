# KS-1040-part1 R16B-SWEEPRC - re-brief at develop 8c2f7b3fd of READY_KS-1040-part1_ornith35b-q4_BASHPATCH-RETRY-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 10:27:58 AEST by Wednesday's feed9 drafter under the FEED 8 ruling; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip (KS-1081: one hunk corrected to the old brief's intent - see the drafter's note), every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
Preflight leg 4 (`preflight.sh:292-304`) runs `node scripts/preflight/path-resolvability.mjs` and, on ANY non-zero exit, prints `FAIL — a published path is unroutable (KS-473 class)` (`:299`). But the sweep has two failure exits: **1** = it ran and a published path answered "Route ... not found" (a real routing finding), and **2** = it could NOT run at all — the spec was unreadable or the login was refused (`path-resolvability.mjs:34-35` documents "2 on setup errors (spec unreadable, login failed)"; `:177-178` `console.error('Sweep aborted:', …); process.exit(2)`). On 2026-09-09 the IP-scoped login limiter returned 429, the sweep printed `Sweep aborted: login failed: HTTP 429 for demo@secuura.io` and exited 2, and leg 4 told the reader a path was unroutable — sending them to the OpenAPI spec for a login-budget problem. **This task: leg 4 names exit 2 as a sweep that could NOT RUN, keeps the exit-1 message byte-identical, and still sets `fail=1` on both** (the ticket: "The gate is right to refuse … Do not fix this by relaxing the gate"). NOT in this task: echoing `RateLimit-Reset` (that is a change to `path-resolvability.mjs`, a second file), leg 3, or the verdict block.
## Drafter's note (feed9, read before the hunk)
RULING (Wednesday, the FEED 9 commission): the tip's `echo "FAIL — a published path is unroutable (KS-473 class)"` is REMOVED (the `-` line) and RE-ADDED inside the new `case` as the `*)` arm - it must be a `+` line, so its em-dash is written as `--` in the NEW text (`FAIL -- a published path is unroutable (KS-473 class)`), and the new `2)` arm's message takes the same `--`. The suite's cells grep `a published path is unroutable` and `could NOT RUN` (no dash), so the wording change is invisible to them. The tip's own bytes are untouched elsewhere. This is PART ONE of KS-1040 only (the reset-time half needs path-resolvability.mjs and is NOT in this brief); KS-1040 stays OPEN after merge.

## The exact change - 1 hunk(s) in `Blockchain/Dev/scripts/preflight/preflight.sh` (1 '-' line(s), 6 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -303,7 +303,12 @@ if curl -sf -o /dev/null "$GATEWAY/health" 2>/dev/null; then
     elif node scripts/preflight/path-resolvability.mjs --base "$GATEWAY"; then
         echo "OK — every published path routes to a handler"
     else
-        echo "FAIL — a published path is unroutable (KS-473 class)"
+        paths_rc=$?
+        # KS-1040: path-resolvability.mjs exits 2 when the sweep could not RUN (login refused, spec unreadable) and 1 on a real finding.
+        case "$paths_rc" in
+            2) echo "FAIL -- the path sweep could NOT RUN (exit 2, see the 'Sweep aborted' line above): nothing was measured, so this is not a routing finding (KS-1040)" ;;
+            *) echo "FAIL -- a published path is unroutable (KS-473 class)" ;;
+        esac
         fail=1
     fi
 else
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:306` - **must change**: `        echo "FAIL — a published path is unroutable (KS-473 class)"`
* `:303` - (correct) `    elif node scripts/preflight/path-resolvability.mjs --base "$GATEWAY"; then` - stays
* `:304` - (correct) `        echo "OK — every published path routes to a handler"` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh`

File: `Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (97 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh`, ONE hunk header `@@ -0,0 +1,97 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for preflight.sh leg 4 - a sweep that could not RUN is not a routing
# finding (KS-1040)
# =============================================================================
# path-resolvability.mjs exits 1 when a published path answered "Route ... not
# found" and exits 2 when the sweep could not run at all (spec unreadable, or the
# login refused - HTTP 429 from the IP-scoped login limiter on 2026-09-09). Leg 4
# printed "a published path is unroutable" for BOTH exits, which sends the reader
# to the OpenAPI spec for a login-budget problem. The leg must still REFUSE on
# exit 2: a sweep that measured nothing has not passed.
#
# The leg's own block is cut out of preflight.sh by text (from its step line to
# the next section marker) and run in a throwaway directory with curl, node and
# the step helpers stubbed, so no gateway, no network and no node run is needed.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh
#        PREFLIGHT_SH=/path/to/other/preflight.sh bash ...   (red-proof)
# =============================================================================
set -uo pipefail
TOTAL_CELLS=5

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${PREFLIGHT_SH:-$HERE/../preflight/preflight.sh}"
[ -f "$SUBJ" ] || { echo "FATAL: preflight.sh not found at $SUBJ" >&2; exit 2; }

WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1040.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

pass=0; fail=0
ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1"; echo "       $2"; fail=$((fail + 1)); }

mkdir -p "$WORK/scripts/preflight/node_modules/yaml"
awk -v start='step "4/15' -v stop='# --- scripts/audit deps' 'index($0, stop) == 1 { on = 0 } index($0, start) == 1 { on = 1 } on' "$SUBJ" > "$WORK/leg4.sh"
cat > "$WORK/stubs.sh" <<'STUBS'
step() { echo "=== $1 ==="; }
skip_stack() { echo "SKIP stack"; }
skip_advisory() { echo "SKIP advisory $1"; }
curl() { return 0; }
node() { echo "stub sweep exiting $SWEEP_RC"; return "$SWEEP_RC"; }
GATEWAY="http://127.0.0.1:9"
fail=0
STUBS

run_leg4() {
  ( cd "$WORK" && SWEEP_RC="$1" bash -c '. ./stubs.sh; . ./leg4.sh; echo "LEG4_FAIL=$fail"' 2>&1 )
}

OUT2="$(run_leg4 2)"
OUT1="$(run_leg4 1)"
OUT0="$(run_leg4 0)"

# RED CELL 1 - exit 2 is reported as a sweep that could not run
if echo "$OUT2" | grep -qF 'could NOT RUN'; then
  ok "RED exit 2 is reported as a sweep that could NOT RUN"
else
  bad "RED exit 2 is reported as a sweep that could NOT RUN" "leg 4 printed no 'could NOT RUN' line for exit 2"
fi

# RED CELL 2 - exit 2 does not claim an unroutable path
if echo "$OUT2" | grep -qF 'a published path is unroutable'; then
  bad "RED exit 2 does not claim a published path is unroutable" "leg 4 printed the routing verdict for a sweep that never ran"
else
  ok "RED exit 2 does not claim a published path is unroutable"
fi

# CONTROL CELL 3 - exit 2 still refuses the push
if echo "$OUT2" | grep -qx 'LEG4_FAIL=1'; then
  ok "CONTROL exit 2 still sets fail=1 (the gate refuses)"
else
  bad "CONTROL exit 2 still sets fail=1 (the gate refuses)" "fail was not 1 after exit 2"
fi

# CONTROL CELL 4 - exit 1 is still the routing finding, and refuses
if echo "$OUT1" | grep -qF 'a published path is unroutable' && echo "$OUT1" | grep -qx 'LEG4_FAIL=1'; then
  ok "CONTROL exit 1 reports a published path is unroutable and sets fail=1"
else
  bad "CONTROL exit 1 reports a published path is unroutable and sets fail=1" "exit 1 lost its routing verdict or its refusal"
fi

# CONTROL CELL 5 - exit 0 passes (and proves the leg's block was extracted)
if echo "$OUT0" | grep -qF 'every published path routes to a handler' && echo "$OUT0" | grep -qx 'LEG4_FAIL=0'; then
  ok "CONTROL exit 0 reports every path routes and leaves fail=0"
else
  bad "CONTROL exit 0 reports every path routes and leaves fail=0" "the leg 4 block did not run from $SUBJ"
fi

echo ""
echo "  $pass passed, $fail failed (of $TOTAL_CELLS cells)"
# A cell that never ran is not a pass: the ratio must add up.
if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
  echo "  INCOMPLETE - $((pass + fail)) of $TOTAL_CELLS cells ran"
  exit 1
fi
[ "$fail" -eq 0 ] || exit 1
exit 0
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `ok "RED exit 2 is reported as a sweep that could NOT RUN"`
- `ok "RED exit 2 does not claim a published path is unroutable"`
- `# CONTROL CELL 3 - exit 2 still refuses the push`
- `ok "CONTROL exit 2 still sets fail=1 (the gate refuses)"`
- `# CONTROL CELL 4 - exit 1 is still the routing finding, and refuses`
- `ok "CONTROL exit 1 reports a published path is unroutable and sets fail=1"`
- `# CONTROL CELL 5 - exit 0 passes (and proves the leg's block was extracted)`
- `ok "CONTROL exit 0 reports every path routes and leaves fail=0"`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/preflight/preflight.sh` / `+++ b/Blockchain/Dev/scripts/preflight/preflight.sh` (1 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh` (one hunk, `@@ -0,0 +1,97 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed9 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 10:27:58 AEST)
- `Blockchain/Dev/scripts/preflight/preflight.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Blockchain/Dev/scripts/preflight/preflight.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/preflight_leg4_sweep_not_run.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x; FEED 9 inherits it) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed9-drafter-precheck/SWEEPRC/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1040 on the Secuura board at 2026-09-22 10:27:58 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
