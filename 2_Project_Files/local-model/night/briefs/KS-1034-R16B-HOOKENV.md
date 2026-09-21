# KS-1034 R16B-HOOKENV - re-brief at develop 8c2f7b3fd of READY_KS-1034_ornith35b-q4_BASHPATCH-RETRY-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 09:46:42 AEST by Wednesday's feed8 drafter; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip, every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
`check-stack-safety.sh:34` derives the repository root as `git -C "$ROOT" rev-parse --show-toplevel`. When git runs a hook from a **linked worktree** it exports `GIT_DIR` to the hook, and under `GIT_DIR` (with no `GIT_WORK_TREE`) that query answers the directory it was asked from — `Blockchain/Dev` — not the repository root. Every repo-root path the guard builds is then one level too deep, and it reports **60** `::error::` lines calling present files "missing" (`docker-compose.local.yml`, `Start_Up/start-secuura.sh`, …) and exits 1. `run-code-guards.sh:59` already shields every guard by unsetting the git environment, but the guard called directly from a hook is still exposed. **This task: clear `GIT_DIR` and `GIT_WORK_TREE` for that one git query (the ticket's second fix option, which keeps the comment above it — "Resolve it via git" — true), add one comment line saying why, plus one new shell suite that runs the real guard against the checkout with and without a hook-style `GIT_DIR`.** NOT in this task: the ticket's "sweep the other guards for the same pattern" (a separate change per file), `run-code-guards.sh`, `run_code_guards.test.sh`.

## The exact change - 1 hunk(s) in `Blockchain/Dev/scripts/check-stack-safety.sh` (1 '-' line(s), 2 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
--- a/Blockchain/Dev/scripts/check-stack-safety.sh
+++ b/Blockchain/Dev/scripts/check-stack-safety.sh
@@ -32,6 +32,7 @@ set -uo pipefail
 # succeeds, because && binds to the result of the whole `a || cd b` list — which
 # concatenated both paths into REPO and broke every path built from it.
-REPO="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || (cd "$ROOT/../.." && pwd))"
+# KS-1034: in a linked worktree git exports GIT_DIR to hooks, and under it --show-toplevel answers the directory asked from, so clear it for this one query.
+REPO="$(env -u GIT_DIR -u GIT_WORK_TREE git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || (cd "$ROOT/../.." && pwd))"
 
 EXIT=0
 CHECKS=0
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:34` - **must change**: `REPO="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || (cd "$ROOT/../.." && pwd))"`
* `:32` - (correct) `# succeeds, because && binds to the result of the whole `a || cd b` list — which` - stays
* `:33` - (correct) `# concatenated both paths into REPO and broke every path built from it.` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh`

File: `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (71 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh`, ONE hunk header `@@ -0,0 +1,71 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-stack-safety.sh - repo root inside a
# git hook (KS-1034)
# =============================================================================
# The defect: git exports GIT_DIR to hooks run in a linked worktree, and under
# GIT_DIR the query `git -C Blockchain/Dev rev-parse --show-toplevel` answers
# Blockchain/Dev instead of the repository root. The guard built every repo-root path one
# level too deep and reported present files as "missing". run-code-guards.sh
# shields the guard by unsetting the git env; a direct call from a hook was
# still exposed. The guard now clears GIT_DIR for that one query.
#
# The cells run the REAL guard against this checkout: once with GIT_DIR set the
# way a hook sets it, once without. It reads files only.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh
#        STACK_SAFETY_SH=/path/to/other/copy bash ...   (red-proof)
# =============================================================================
set -uo pipefail
TOTAL_CELLS=5

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
if [ "${STACK_SAFETY_SH+set}" = set ] && [ -z "$STACK_SAFETY_SH" ]; then
  echo "FATAL: STACK_SAFETY_SH is set but EMPTY - refusing to silently grade the shipped script." >&2
  exit 2
fi
SUBJ="${STACK_SAFETY_SH-$REPO_ROOT/Blockchain/Dev/scripts/check-stack-safety.sh}"
[ -f "$SUBJ" ] || { echo "FATAL: check-stack-safety.sh not found at $SUBJ" >&2; exit 2; }
GD="$(env -u GIT_DIR -u GIT_WORK_TREE git -C "$REPO_ROOT" rev-parse --absolute-git-dir 2>/dev/null)"
[ -n "$GD" ] || { echo "FATAL: $REPO_ROOT is not a git checkout - this suite needs one to set GIT_DIR" >&2; exit 2; }

pass=0; fail=0
ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1"; echo "     $2"; fail=$((fail + 1)); }

rc_hook=0; out_hook="$(env -u GIT_WORK_TREE GIT_DIR="$GD" bash "$SUBJ" 2>&1)" || rc_hook=$?
rc_plain=0; out_plain="$(env -u GIT_DIR -u GIT_WORK_TREE bash "$SUBJ" 2>&1)" || rc_plain=$?
errors_hook="$(printf '%s' "$out_hook" | grep -c -F '::error::' || true)"
top_hook="$(env -u GIT_WORK_TREE GIT_DIR="$GD" git -C "$REPO_ROOT/Blockchain/Dev" rev-parse --show-toplevel 2>/dev/null)"

# CELL 1 - red at the tip
if [ "$rc_hook" -eq 0 ]; then ok "the guard passes when a hook's GIT_DIR is set"
else bad "the guard fails when a hook's GIT_DIR is set" "rc=$rc_hook"; fi

# CELL 2 - red at the tip
if [ "$errors_hook" -eq 0 ]; then ok "no present file is reported missing under GIT_DIR"
else bad "files reported missing under GIT_DIR" "$errors_hook error line(s), first: $(printf '%s' "$out_hook" | grep -m1 -F '::error::')"; fi

# CONTROL CELL 3 - green on both trees
if [ "$rc_plain" -eq 0 ] && printf '%s' "$out_plain" | grep -qF 'shared-stack safety invariants hold'; then ok "CONTROL the guard passes on this tree without GIT_DIR"
else bad "CONTROL the guard fails on this tree even without GIT_DIR" "rc=$rc_plain"; fi

# CONTROL CELL 4 - green on both trees
case "$top_hook" in
  */Blockchain/Dev) ok "CONTROL under GIT_DIR git itself answers Blockchain/Dev as the top level" ;;
  *) bad "CONTROL git no longer answers Blockchain/Dev under GIT_DIR - this suite cannot see the hook defect" "top=$top_hook" ;;
esac

# CONTROL CELL 5 - green on both trees
if bash -n "$SUBJ"; then ok "CONTROL check-stack-safety.sh parses (bash -n)"
else bad "CONTROL check-stack-safety.sh does not parse" "bash -n failed"; fi

echo ""
echo "  $pass passed, $fail failed (of $TOTAL_CELLS cells)"
if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
  echo "  INCOMPLETE - $((pass + fail)) of $TOTAL_CELLS cells ran"
  exit 1
fi
[ "$fail" -eq 0 ] || exit 1
exit 0
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `# CELL 1 - red at the tip`
- `# CELL 2 - red at the tip`
- `# CONTROL CELL 3 - green on both trees`
- `# CONTROL CELL 4 - green on both trees`
- `# CONTROL CELL 5 - green on both trees`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/check-stack-safety.sh` / `+++ b/Blockchain/Dev/scripts/check-stack-safety.sh` (1 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh` (one hunk, `@@ -0,0 +1,71 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed8 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 09:46:42 AEST)
- `Blockchain/Dev/scripts/check-stack-safety.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Blockchain/Dev/scripts/check-stack-safety.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed8-drafter-precheck/HOOKENV/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1034 on the Secuura board at 2026-09-22 09:46:42 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
