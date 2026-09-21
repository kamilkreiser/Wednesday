# KS-1047 R16B-STACKLEGS - re-brief at develop 8c2f7b3fd of READY_KS-1047_ornith35b-q4_BASHPATCH-RECOUNTED-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 09:48:20 AEST by Wednesday's feed8 drafter; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip, every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
`.githooks/pre-push:268` is a load-bearing comment: it is the rationale for sourcing `slot-target.sh` before the preflight so the stack-dependent legs probe THIS slot. It names those legs as **(3, 4, 7)**; measured 2026-09-09 they are **3, 4, 8** (leg 7 is the standalone-lock advisories, not stack-dependent; leg 8, served-spec consistency, is) — a leg was inserted and the comment did not move. The ticket's better fix, in the spirit of KS-1046 (#925, which made the verdict PRINT the skipped legs): drop the enumeration and point at the verdict line, which cannot drift. **This task: line 268 becomes a pointer to the verdict, plus one new shell suite proving the stale enumeration is gone, the pointer is present, and the comment's anchor and the hook's syntax are untouched.** NOT in this task: :269–:274 (the rest of the comment), any code.

## The exact change - 1 hunk(s) in `.githooks/pre-push` (1 '-' line(s), 1 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
--- a/.githooks/pre-push
+++ b/.githooks/pre-push
@@ -266,6 +266,6 @@ echo "[pre-push] Blockchain/Dev changes detected → running preflight gate (bypass
 # Safe on macOS bash 3.2: the script uses no bash-4 constructs (no mapfile/readarray,
 # no associative arrays, no ${x^^}).
-# KS-691: source slot-target.sh first so the stack-dependent legs (3, 4, 7) probe
+# KS-691: source slot-target.sh first so the stack-dependent legs (the ones the preflight verdict lists as SKIPPED when the stack is down - KS-1046; not enumerated here, an enumeration drifts) probe
 # THIS slot's gateway. preflight.sh defaults GATEWAY to localhost:6882 (slot 1),
 # so from any other slot those legs either silently SKIP (slot 1 down) — the push
 # passes having probed nothing — or probe SLOT 1 and report success for a stack
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:268` - **must change**: `# KS-691: source slot-target.sh first so the stack-dependent legs (3, 4, 7) probe`
* `:266` - (correct) `# Safe on macOS bash 3.2: the script uses no bash-4 constructs (no mapfile/readarray,` - stays
* `:267` - (correct) `# no associative arrays, no ${x^^}).` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh`

File: `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (74 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh`, ONE hunk header `@@ -0,0 +1,74 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for .githooks/pre-push line :268 comment - stale leg enumeration gone, pointer present (KS-1047)
# =============================================================================
# The defect at tip `48e65c435`: line 268 enumerates legs "(3, 4, 7)" which is
# wrong (measured 2026-09-09 they are 3, 4, 8). The fix drops the enumeration
# and points at the verdict line instead. These four cells prove that.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh
# =============================================================================
set -uo pipefail
TOTAL_CELLS=4

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
SUBJ="${PRE_PUSH_HOOK-$REPO_ROOT/.githooks/pre-push}"
[ -f "$SUBJ" ] || { echo "FATAL: pre-push hook not found at $SUBJ" >&2; exit 2; }
[ -r "$SUBJ" ] || { echo "FATAL: PRE_PUSH_HOOK is not readable at $SUBJ" >&2; exit 2; }
printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"

pass=0; fail=0
ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }

# ---------------------------------------------------------------------------
# CELL 1 - KS-1047 RED. THE STALE ENUMERATION IS GONE.
# ---------------------------------------------------------------------------
stale_hits="$(grep -c '(3, 4, 7)' "$SUBJ" || true)"
if [ "$stale_hits" = 0 ]; then
  ok "the stale leg enumeration (3, 4, 7) is gone from pre-push"
else
  bad "the stale leg enumeration (3, 4, 7) is gone from pre-push" \
      "count=$stale_hits (expected 0)"
fi

# ---------------------------------------------------------------------------
# CELL 2 - KS-1047 RED. THE COMMENT POINTS AT THE VERDICT LINE (KS-1046), NOT LEGS.
# ---------------------------------------------------------------------------
ptr_hits="$(grep -c 'KS-1046' "$SUBJ" || true)"
if [ "$ptr_hits" = 1 ]; then
  ok "the comment points at the verdict line (KS-1046) instead of enumerating legs"
else
  bad "the comment points at the verdict line (KS-1046) instead of enumerating legs" \
      "count=$ptr_hits (expected 1)"
fi

# ---------------------------------------------------------------------------
# CELL 3 - CONTROL. THE KS-691 RATIONALE COMMENT IS STILL THERE.
# ---------------------------------------------------------------------------
anchor_hits="$(grep -c 'KS-691: source slot-target.sh first so the stack-dependent legs' "$SUBJ" || true)"
if [ "$anchor_hits" = 1 ]; then
  ok "the KS-691 rationale comment anchor is still present in pre-push"
else
  bad "the KS-691 rationale comment anchor is still present in pre-push" \
      "count=$anchor_hits (expected 1)"
fi

# ---------------------------------------------------------------------------
# CELL 4 - CONTROL. PRE-PUSH PARSes (bash -n).
# ---------------------------------------------------------------------------
if bash -n "$SUBJ" >/dev/null 2>&1; then
  ok "pre-push parses (bash -n)"
else
  bad "pre-push parses (bash -n)" "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"
fi

printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
# A cell that never ran is not a pass: the ratio must add up.
if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
  printf '  INCOMPLETE - %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
  exit 1
fi
[ "$fail" -eq 0 ] || exit 1
exit 0
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `# CELL 1 - KS-1047 RED. THE STALE ENUMERATION IS GONE.`
- `ok "the stale leg enumeration (3, 4, 7) is gone from pre-push"`
- `# CELL 2 - KS-1047 RED. THE COMMENT POINTS AT THE VERDICT LINE (KS-1046), NOT LEGS.`
- `ok "the comment points at the verdict line (KS-1046) instead of enumerating legs"`
- `# CELL 3 - CONTROL. THE KS-691 RATIONALE COMMENT IS STILL THERE.`
- `ok "the KS-691 rationale comment anchor is still present in pre-push"`
- `# CELL 4 - CONTROL. PRE-PUSH PARSes (bash -n).`
- `ok "pre-push parses (bash -n)"`

## Output
Exactly ONE ```diff block with TWO files: `--- a/.githooks/pre-push` / `+++ b/.githooks/pre-push` (1 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh` (one hunk, `@@ -0,0 +1,74 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed8 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 09:48:20 AEST)
- `.githooks/pre-push` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:.githooks/pre-push`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed8-drafter-precheck/STACKLEGS/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1047 on the Secuura board at 2026-09-22 09:48:20 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
