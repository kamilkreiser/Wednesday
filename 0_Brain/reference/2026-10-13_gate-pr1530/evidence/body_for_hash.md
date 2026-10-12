# Gate report: Secuura Platform K PR #1530 (KS-998 item 3), narrow gate

Head under test: `c9ac49f5508d4f06b96bc23c9c868ae16acd4a3f` (fetched from `refs/pull/1530/head`, asserted equal). Base develop `5d5aea41fecaba0dcadcbd240fa0c4196b32dc49` (unmoved). Gate date 2026-10-13. Method: `git clone --shared` of the project into my scratchpad, GitHub fetch over the project's deploy key (read), all suites and mutants run only in my clone. The project folder was not written; no pushes, no GitHub or Linear writes. Raw outputs in `evidence/`.

## Severity counts
Majors: 0. Minors: 3. Informational: 2.

## 1. Suites, head vs develop (3 repeated runs each, instrument: the suites' own tally line + rc)
| Suite | head c9ac49f55 | develop 5d5aea41f |
|---|---|---|
| pre_push_hook_base | 33/0 rc0 x3 | 28/0 rc0 x3 |
| pre_push_hook_base_fixture_guard | 6/0 rc0 x3 | 6/0 rc0 x3 |
| pre_push_hook_base_leg_comment | 4/0 rc0 x3 | 4/0 rc0 x3 |
| pre_push_stack_legs_comment | 4/0 rc0 x3 | 4/0 rc0 x3 |
| pre_push_hook_current_develop | 4/0 rc0 x3 | 4/0 rc0 x3 |

Stable. The delta is exactly +5 cells (CASE 12 x3, CASE 13 x2), as the commit message says. Control: the develop tree is a separate worktree of the same clone, so the 28 baseline is independent of the head tree. Files: `evidence/repo_*`, `evidence/wt_dev_*`.

## 2. Mutants (hook mutated via the suite's own `HOOK_SH`; each diff in `evidence/mut_*.diff`)
Hook branch under test: `.githooks/pre-push:239-244`. All mutant hooks are non-empty, valid, one-edit diffs of the real hook.
| Mutant | Edit | Result (subject suite) | Verdict |
|---|---|---|---|
| v1 | `exit 1` -> `exit 0` at :243 | 32/1, only "CASE 12 - a MISSING formatting gate REFUSES the push" red | reproduces claim, names the right cell only |
| v2 | condition inverted (`[ -f ]`) | 20/13: CASE 12 right-reason and both CASE 13 cells red, but also 10 earlier cells | claim true, but v2 is not isolated: inverting the condition breaks every push that reaches the gate. CASE 13 reds, not alone |
| v3 | message reworded, still exit 1 | 32/1, only "CASE 12 - RIGHT reason" red | reproduces claim; first CASE 12 cell correctly stays green (it was refused) |
| m4 (mine) | branch disabled (`if false`) so the later `bash <missing gate>` fails with the gate-FAILED text and exit 1 | 32/1, only CASE 12 "RIGHT reason" red | different-reason refusal (different message) is caught |
| m5 (mine) | missing-gate message printed unconditionally, gate present | 30/3: CASE 13 "branch does NOT fire" red (plus two docs-only cells) | CASE 13 message control can fail |
| m6 (mine) | unrelated `exit 1` + unrelated message at hook line 2 (refusal for an unrelated reason) | CASE 12 "RIGHT reason" red; CASE 13 control red; CASE 12 first cell stays green | confirms the first cell alone cannot tell reasons apart and the second cell is load-bearing |
| m7 (mine) | branch keeps `exit 1`, message lines removed | 32/1, only CASE 12 "RIGHT reason" red | message-assertion is what pins the branch |
| pinned tally | one cell (CASE 13 second cell) removed from a copy of the subject suite | subject 32/0; guard 5/1, CONTROL cell red with `tally='32/0'` | reproduces claim; guard reds on the exact number |

Note on instruments: the first m6 and m7 attempts were malformed (a failed `sed` produced an empty hook, which reds nearly everything). I discarded those runs and rebuilt both mutants with python; the numbers above are from the rebuilt, verified mutants (`mut_m6.diff`, `mut_m7.diff`).

## 3. DANGER CHECK (gate moved aside)
FOUND: there is no restore and no trap specific to the gate. The safety is containment, not restoration.
- The `mv` runs in `$WORK/c12/fresh`, a throwaway clone made by `build_fixture` under `mktemp -d` (suite line ~65), never in the real repo. Instrumented probe printed `pwd=<TMPDIR>/ks854.Qr9HTW/c12/fresh`, and the real `systemTest/scripts/check-package-format.sh` sha256 was `f97f0bd7...` before and after, and `git status` of my clone was clean.
- Forced failure A (injected `exit 9` between the `mv` and anything else, run with `TMPDIR` set to an empty dir): CASE 12 reds, 32/1, and the EXIT trap `rm -rf "$WORK"` left 0 entries behind.
- Forced failure B (SIGKILL of the suite shell right after the `mv`, so the trap cannot run): one orphan fixture dir remains in `TMPDIR` with `.gate-moved-aside` inside it; the real file is untouched, and a later run of the real suite with that `TMPDIR` is 33/0. A leftover cannot affect any later push check because every fixture uses a fresh `mktemp` dir.
- So the author's phrasing "a move is reversible if a cell aborts" (test line 700) is not what happens: nothing restores it; the fixture is discarded. Safe, but the comment misdescribes the mechanism. (Minor 1.)
Evidence: `evidence/danger.txt`, `danger_A.txt`, `danger_B.txt`. Hazard noted during my own testing: my first variant used an unquoted heredoc and `kill -9 $PPID`, which killed my own outer shell; rerun with `kill -9 $$` and a quoted heredoc.

## 4. Pinned tallies
- Cross-suite pin: only `pre_push_hook_base_fixture_guard.test.sh:137` (`"33/0"`). Confirmed no other suite asserts another suite's count.
- But the note at guard line 128, "It is the only pinned tally in this directory", is overbroad: several suites in the same directory pin their OWN counts (`ks1136...:163` `-eq 6`, `ks1317...:132` `-eq 8`, `ks1405...:88` `-eq 4`, `ks1456...:92` `-eq 4`, `ks808...:104` `-eq 5`). Different mechanism (self-pin), so the claim holds only in the cross-suite sense. (Minor 2.)
- The note's arithmetic is right: 28 -> 33 = CASE 12's three cells + CASE 13's two; I counted them in the diff and the suite prints 33.
- `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html:3355` states "28 passed / 0 failed" for this suite; it is a dated record "at the same head" of another PR, not a live pin. Informational only.
Evidence: `evidence/greps.txt`.

## 5. Scope
`git diff origin/develop...pr1530 --stat`: exactly 2 files (`pre_push_hook_base.test.sh` +78, `pre_push_hook_base_fixture_guard.test.sh` +11/-4), 89/-4 total as claimed; no `.githooks/` file, no product file. `git merge-base` = develop `5d5aea41f`; `git merge-tree --write-tree` rc 0 (clean, tree `6b171f251e9a`). Two commits as described.

## 6. Existing coverage and gaps
- No existing cell covers hook lines 239-244: the only other `check-package-format.sh` suites (`systemTest/__tests__/package_format_gate.test.sh`, `ks998_*`) test the gate script's own branches; `ks884_*` and `pre_push_hook_current_develop` only install a stub gate. CASE 12 is not a duplicate.
- Unpinned in this area (not blocking): (a) only the first of the three REFUSED lines is asserted, so the path line (`$_fmt_gate`) and the "must not be read as a gate that passed" line can change unnoticed; (b) CASE 12 never asserts the branch did not land at the bare origin (the hook exit makes this implied, but the cell does not check it); (c) the gate present-but-not-a-regular-file / non-executable case (`-f` only) is untested. (Minor 3 for a and b together; c informational.)

## NOT tested
Real `git push` to GitHub; macOS-only (bash 3.2 fixture shell, Darwin); Linux/dash behaviour of the hook; the real (non-stub) gate script; the HTML doc staleness beyond noting it; interruption by SIGINT from a terminal (SIGKILL and an in-cell exit covered).

## Findings
- Minor 1: `pre_push_hook_base.test.sh:699-700` comment claims a move "is reversible if a cell aborts"; nothing restores it, safety is the mktemp fixture plus EXIT trap (SIGKILL leaves a harmless orphan dir). Reword.
- Minor 2: `pre_push_hook_base_fixture_guard.test.sh:128` "the only pinned tally in this directory" is true only for cross-suite pins; five sibling suites self-pin.
- Minor 3: `pre_push_hook_base.test.sh:723` asserts only the first REFUSED line; the path line is unasserted, and no cell checks the refused branch is absent at origin.
- Info 1: v2 inverts the condition for every push, so "CASE 13 reds" is true but not isolating.
- Info 2: stale "28/0" in `Projects Documents/...Flow_Diagrams.html:3355` (historical record).

No blocking issue: every author mutant reproduced against the named cell, the control can fail independently, the fixture cannot touch the real repo, and the scope is clean.
