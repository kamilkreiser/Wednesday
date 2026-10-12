# Gate brief: Secuura Platform K PR #1530 (ticket KS-998 item 3), NARROW SONNET gate — test-only, light tier

Commissioned 2026-10-13 ~08:0x AEDT by the Wednesday seat. Author: K 8th.

## What you are gating
- Head `c9ac49f5508d4f06b96bc23c9c868ae16acd4a3f` (Wednesday's ls-remote of refs/pull/1530/head, equals the author's), branch `feature/ks-998-item3-fail-closed-cell`, base develop `5d5aea41feca` (unmoved at my read). TEST-ONLY: 2 files, +89/-4, two commits (5e767df9f the cells; c9ac49f55 moves a pinned tally 28/0 -> 33/0). No product file.
- What it adds (author's description, NOT evidence): CASE 12 drives the real `.githooks/pre-push` on the suite's existing bare-remote fixture with the gate script MOVED ASIDE (never deleted) and asserts the push is refused, by the branch's own named message (`.githooks/pre-push` ~lines 236-244, "gate script missing -> REFUSED, exit 1"), and that the commit landed first. CASE 13 is its control: the same push with the gate PRESENT is not refused and the message does not appear. Suite `pre_push_hook_base.test.sh` 28/0 -> 33/0. The sibling guard `pre_push_hook_base_fixture_guard.test.sh` CELL 3 pins the subject suite's tally exactly; the second commit moves that pin and adds a note.
- Author's mutants (claims): v1 branch exits 0 instead of 1 -> CASE 12 reds; v2 condition INVERTED -> CASE 13's control reds; v3 message reworded, branch still refusing -> CASE 12 "right reason" reds; and removing one cell from the subject suite makes the guard's CELL 3 red naming "the suite is 33/0".

## How to get the code (READ-ONLY on the project)
- `git clone --shared` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into YOUR scratchpad; fetch `refs/pull/1530/head` with the project's `core.sshCommand`; assert the head sha. Never write in the project folder, no pushes, no GitHub or Linear writes. Run the hook suites inside your clone only.

## What to attack
1. Re-run the five hook suites at the head and at develop: pre_push_hook_base (expect 33/0 at head), ..._fixture_guard (6/0), ..._leg_comment, pre_push_stack_legs_comment, ..._current_develop; stable over repeated runs; report counts for both trees.
2. Re-derive v1, v2, v3 yourself, each must fail the NAMED cell and nothing else of the suite for the wrong reason; re-derive the pinned-tally mutant (remove one cell -> the guard's CELL 3 reds). Add one mutant of your own (for example: the cell passes when the push is refused for a DIFFERENT reason, such as a missing remote).
3. DANGER CHECK: the fixture moves the gate script aside. If a cell fails midway or the shell is interrupted, is the gate restored (trap / cleanup)? Prove it by forcing a failure between the move and the restore and showing the file is back. Confirm the move is inside the fixture's copy, never the real repo file. A leftover moved file would silently break every later push check.
4. The hard-coded tally: `git grep` for other pinned tallies or suite counts in the tests directory; confirm the author's claim that CELL 3 is the only one; check the note added with the pin says what the author says.
5. Scope: the diff is exactly the 2 files, no product file, no hook change; `git merge-tree` against develop 5d5aea41 clean.
6. Find any existing cell that already covers the :236-244 branch (so CASE 12 duplicates it) and any guard no cell pins in this area.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1530/verdict.md` (this folder only, plus your scratchpad; raw outputs under `evidence/`, never a directory named `out`). Head under test; numbers with instruments and controls; FOUND / TESTED / HOW; NOT tested; severities with file:line.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors separately; verdict line and sha256/16 of the report at the top.
