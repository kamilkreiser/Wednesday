# KS-1093 R16B-LATESTSLOT - re-brief at develop 8c2f7b3fd of READY_KS-1093_ornith35b-q4_BASHPATCH-B3CREPAIRED-RECOUNTED-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 09:50:10 AEST by Wednesday's feed8 drafter; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip, every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
§6f's KS-682 loop (`:323–:335`) probes six per-slot Playwright artefact shapes with `git check-ignore -q`. The fourth shape is `results/latest-slot${slot}/index.html`. Since KS-682 a real run makes `results/latest-slot<N>` a **symlink** to the timestamped report directory, and `git check-ignore` refuses any path *beyond* a symlink (`fatal: pathspec '…' is beyond a symbolic link`, rc 128). The loop reads the non-zero rc as "not ignored" and the gate goes red exactly when it has just been used — a false red naming a real-looking defect. Measured at this tip: `git check-ignore -q systemTest/playwright/results/latest-slot4` (the symlink ITSELF) is rc 0 both when the symlink exists and on a clean tree (the blanket `results/` rule at `systemTest/playwright/.gitignore:17` covers it), so probing the symlink itself removes the failure without weakening what is proven. **This task: E1 adds a two-line comment naming the rule; E2 changes the ONE probe line to the symlink itself; plus one NEW shell suite with two text reds, one behavioural red (the gate run with a `latest-slot4` symlink present), and three controls.** NOT in this task: the other five shapes, §6f2, any other block.

## The exact change - 2 hunk(s) in `Blockchain/Dev/scripts/check-stack-safety.sh` (1 '-' line(s), 3 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
--- a/Blockchain/Dev/scripts/check-stack-safety.sh
+++ b/Blockchain/Dev/scripts/check-stack-safety.sh
@@ -318,7 +318,9 @@ PW_STAMP="2026-01-01T00-00-00-000Z"
 # Honest limit, measured on #803 review: `systemTest/playwright/.gitignore` carries a blanket
 # `results/`, so every `results/...` probe passes by that line alone — they prove the blanket
 # holds, not the suffix. The `.auth-*/` probe is the one that tests a suffix pattern, and it is the
 # one holding a bearer token, which is why it is here for every slot and not just slot 3.
+# KS-1093: `latest-slot<N>` is a SYMLINK once a run exists, and `git check-ignore` refuses any path
+# beyond a symlink (fatal, rc 128 - read as "not ignored"). Probe the symlink ITSELF, never through it.
 PW_STAMP="2026-01-01T00-00-00-000Z"
 for slot in 1 2 3 4; do
   for artifact in \
@@ -325,7 +327,7 @@ PW_STAMP="2026-01-01T00-00-00-000Z"
     "$REPO/systemTest/playwright/results/playwright-report-ks-682-${PW_STAMP}-slot${slot}/index.html" \
     "$REPO/systemTest/playwright/results/test-results-ks-682-${PW_STAMP}-slot${slot}/.last-run.json" \
     "$REPO/systemTest/playwright/results/har-ks-682-${PW_STAMP}-slot${slot}/1.har" \
-    "$REPO/systemTest/playwright/results/latest-slot${slot}/index.html" \
+    "$REPO/systemTest/playwright/results/latest-slot${slot}" \
     "$REPO/systemTest/playwright/.auth-ks-682-slot${slot}/token.json" \
     "$REPO/systemTest/playwright/.auth-ks-682-slot${slot}/state.json"; do
     if git -C "$REPO" check-ignore -q "$artifact" 2>/dev/null; then ok; else
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:328` - **must change**: `    "$REPO/systemTest/playwright/results/latest-slot${slot}/index.html" \`
* `:318` - (correct) `# Honest limit, measured on #803 review: `systemTest/playwright/.gitignore` carries a blanket` - stays
* `:319` - (correct) `# `results/`, so every `results/...` probe passes by that line alone — they prove the blanket` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh`

File: `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (67 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh`, ONE hunk header `@@ -0,0 +1,67 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-stack-safety.sh - latest-slot symlinks (KS-1093)
# =============================================================================
# The defect: with `systemTest/playwright/results/latest-slot4` a symlink,
# the gate prints `::error::latest-slot4/index.html is NOT gitignored on slot 4 (KS-682).`
# and exits 1 because `git check-ignore` refuses paths beyond a symbolic link.
# This suite proves E1+E2 fix that without weakening what is proven.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh
# =============================================================================
set -uo pipefail
TOTAL_CELLS=6

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
SUBJ="${CHECK_STACK_SAFETY_SH-$REPO_ROOT/Blockchain/Dev/scripts/check-stack-safety.sh}"
[ -f "$SUBJ" ] || { echo "FATAL: check-stack-safety.sh not found at $SUBJ" >&2; exit 2; }
[ -r "$SUBJ" ] || { echo "FATAL: CHECK_STACK_SAFETY_SH is not readable at $SUBJ" >&2; exit 2; }
printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1093.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

pass=0; fail=0
ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
RES="$REPO_ROOT/systemTest/playwright/results"

# CELL 1 - RED at the tip: the through-symlink probe is gone.
through_hits="$(grep -c 'results/latest-slot${slot}/index.html' "$SUBJ" || true)"
if [ "$through_hits" -eq 0 ]; then ok "the probe no longer reads THROUGH the latest-slot symlink (index.html)"; else bad "the probe no longer reads THROUGH the latest-slot symlink (index.html)" "count=$through_hits (expected 0)"; fi
# CELL 2 - RED at the tip: the probe of the symlink itself is present.
self_hits="$(grep -c 'results/latest-slot${slot}"' "$SUBJ" || true)"
if [ "$self_hits" -eq 1 ]; then ok "the probe names the latest-slot symlink ITSELF"; else bad "the probe names the latest-slot symlink ITSELF" "count=$self_hits (expected 1)"; fi
# CELL 3 - CONTROL on a clean checkout: the gate exits 0 on this tree as found (nothing created yet).
bash "$SUBJ" > "$WORK/clean.out" 2>&1; rc_clean=$?
if [ "$rc_clean" -eq 0 ]; then ok "the gate exits 0 on this tree as found"; else bad "the gate exits 0 on this tree as found" "rc=$rc_clean: $(grep '::error::' "$WORK/clean.out" | head -2 | tr '\n' ' ')"; fi
# CELL 4 - RED at the tip: with a latest-slot4 SYMLINK present the gate still exits 0 and names no latest-slot error.
made_results=0; made_link=0
[ -d "$RES" ] || { mkdir -p "$RES"; made_results=1; }
if [ ! -e "$RES/latest-slot4" ] && [ ! -L "$RES/latest-slot4" ]; then
  mkdir -p "$RES/playwright-report-ks-1093-slot4"; : > "$RES/playwright-report-ks-1093-slot4/index.html"
  ln -s playwright-report-ks-1093-slot4 "$RES/latest-slot4"; made_link=1
fi
bash "$SUBJ" > "$WORK/symlink.out" 2>&1; rc_link=$?
link_errors="$(grep -c '::error::latest-slot' "$WORK/symlink.out" || true)"
if [ "$made_link" -eq 1 ]; then rm "$RES/latest-slot4"; rm "$RES/playwright-report-ks-1093-slot4/index.html"; rmdir "$RES/playwright-report-ks-1093-slot4"; fi
if [ "$made_results" -eq 1 ]; then rmdir "$RES" 2>/dev/null || true; fi
if [ "$rc_link" -eq 0 ] && [ "$link_errors" -eq 0 ]; then ok "with a latest-slot4 symlink present the gate exits 0 and names no latest-slot error"; else bad "with a latest-slot4 symlink present the gate exits 0 and names no latest-slot error" "rc=$rc_link latest-slot errors=$link_errors"; fi
# CELL 5 - CONTROL: the git mechanism the fix rests on, in a throwaway repo (through the symlink: rc 128; the symlink itself: rc 0).
git -C "$WORK" init -q; printf 'results/\n' > "$WORK/.gitignore"
mkdir -p "$WORK/results/playwright-report-x-slot4"; ln -s playwright-report-x-slot4 "$WORK/results/latest-slot4"
git -C "$WORK" check-ignore -q results/latest-slot4/index.html 2>/dev/null; rc_through=$?
git -C "$WORK" check-ignore -q results/latest-slot4 2>/dev/null; rc_self=$?
if [ "$rc_through" -eq 128 ] && [ "$rc_self" -eq 0 ]; then ok "git check-ignore refuses a path beyond a symlink (rc 128) and accepts the symlink itself (rc 0)"; else bad "git check-ignore refuses a path beyond a symlink (rc 128) and accepts the symlink itself (rc 0)" "through=$rc_through self=$rc_self"; fi
# CELL 6 - CONTROL: the subject parses.
if bash -n "$SUBJ" >/dev/null 2>&1; then ok "check-stack-safety.sh parses (bash -n)"; else bad "check-stack-safety.sh parses (bash -n)" "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"; fi

printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
# A cell that never ran is not a pass (KS-1093 round 2): the ratio must add up.
if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
  printf '  INCOMPLETE - %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
  exit 1
fi
[ "$fail" -eq 0 ] || exit 1
exit 0
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `# CELL 1 - RED at the tip: the through-symlink probe is gone.`
- `# CELL 2 - RED at the tip: the probe of the symlink itself is present.`
- `# CELL 3 - CONTROL on a clean checkout: the gate exits 0 on this tree as found (nothing created yet).`
- `# CELL 4 - RED at the tip: with a latest-slot4 SYMLINK present the gate still exits 0 and names no latest-slot error.`
- `# CELL 5 - CONTROL: the git mechanism the fix rests on, in a throwaway repo (through the symlink: rc 128; the symlink itself: rc 0).`
- `# CELL 6 - CONTROL: the subject parses.`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/check-stack-safety.sh` / `+++ b/Blockchain/Dev/scripts/check-stack-safety.sh` (2 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh` (one hunk, `@@ -0,0 +1,67 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed8 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 09:50:10 AEST)
- `Blockchain/Dev/scripts/check-stack-safety.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Blockchain/Dev/scripts/check-stack-safety.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed8-drafter-precheck/LATESTSLOT/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1093 on the Secuura board at 2026-09-22 09:50:10 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
