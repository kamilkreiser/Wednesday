STARTABLE: YES (once Stamp S4 answers Q21 in words: the moved-`main` rule decides whether a pushed commit may be rewritten)

# B1845 drafter report: lane D (token broker) fix round, kit `2026-11-21_B1845_SEAT-X18_oxpd2-wp15-fix-round.md`

Drafted 2026-11-21 17:47 to 18:05 AEDT (clocks by `date`) by a read-only Opus drafter for Tuesday s304. Kit: 240 lines, 86847 bytes, 0 non-ASCII bytes, 8 unfilled stamp slots (S1 to S7 and READ-WHOLE). Sidecar: 173 claims, 173 measured; `stamp_check.py <kit>` exit 0. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1845/`.

## BLUF
- **One new commit on top of `70c1fad5`, on the existing branch `b1831/wp15-token-broker`, pushed fast-forward from a NEW clone (`<project>/.tools/b1845/clone`).** Nine decisions D20 to D28, one per ruling of the commission:
  - D20: the refresher is started off the caller's thread (`Task.Run`, locals captured first), so the `RefreshTimeout` bound starts at once. S05 and S06 become builder cells F11 and F12. Every existing cell that reads `Calls` or `LiveTimers`, or moves the clock, straight after starting a refresh now waits first with `Expect.Eventually`; no assertion is loosened.
  - D23: idle is checked again on both clocks after a refresh, before any hand-out. A session whose idle deadline passed during the refresh ends `Expired` (cell E07).
  - D25: a clearing array-backed writer replaces `ArrayBufferWriter` (cell P04, on B1838's five rows).
  - D27 (b): `SignOutReason.RestartWindow` is removed (cell V02).
  - README limit lines are added.
  - Guarded-rule cells, each with its mutant: F15/mStaleWaiter, U03/mSubjAnswer, R08/mWritten, R09/mLoadKeep, R10/mWindowEdge, B07/mPsid, E08/mRestoreAnchor, F13/mLateKeep.
- **Two of the commission's points are named limits, not fixes, each with a cell that proves the bound that does hold:**
  - D21: two refresher calls can overlap after a time-out.
  - D24: a wall clock set back while the server runs, followed by a restart. My reading is that no sound fix exists without a timer or state that persists across a restart.
- **One contradiction needs Tuesday's answer (Q21, STOP-CLASS).** The commission says "rebase before push only if main moved". But `70c1fad5` is already pushed, so rebasing it would need a force-push, which both kits forbid. The default never rebases:
  - `main` still at `5e36d8dc`: push.
  - `main` moved but touches no lane path and not the solution file: push fast-forward and name the moved `main`.
  - `main` moved and touches a lane path: STOP.

## FACTS RE-MEASURED (instrument in brackets; controls named)
- Origin [`gh api -X GET`, project `GH_CONFIG_DIR`, 17:47:22]:
  - `main` `5e36d8dca42966395ea3dd014c7f788409eb585f`; branch `b1831/wp15-token-broker` `70c1fad55128667e62fa5379719dfc6e0ba3ac1b`.
  - `b1836/r5-hp-inputs-exemption` at `28d2852d` (not landed).
  - PRs 1 to 6 closed, 0 open; no `b1845` ref.
  - `.private` true, `.permissions.push` true.
- Head tree [tarball by GET into scratch]:
  - 325 files; lane 22 + 12 files, 3582 `.cs` lines.
  - Cells by the indented pattern: 44 methods, 6 theories, 15 `[InlineData` rows, so 53 cases (column-1 counts 0).
  - `Task.Run` in the library: 0 (control `AcceptLocked` 2).
  - `SignOutReason.RestartWindow` used outside its enum: 0 (control `SignOutReason.SubjectMismatch` in `TokenBroker.cs`: 2).
- Every `file:line` in the kit was printed by `ptr.py` (`d1845/pointers.txt`, 39 rows, each count 1, invented-fragment control 0), for example `TokenBroker.cs:334/337/346/389/390/433/446/497/581/609/618/749/789`, `SessionRecord.cs:68/69/104`, `SessionEventArgs.cs:36`, `RefreshCellTests.cs:108/126/196/240`.
  - One fragment did not stand on one line: the README's "wall clock set back keeps nothing alive" wraps across lines 37 and 38. The kit cites `:38` (`awk NR==38` printed it).
- Hosted [`hosted.py`, 17:51]:
  - `HOSTED 70c1fad5...: PASS` (`--total 947 --rules 325 --skipped-linux 4 --skipped-windows 19`).
  - Control `--skipped-linux 5`: `FAIL 2`.
  - `HOSTED 5e36d8dc...: PASS` (`894/291/4/19`).
- `repo_rules.py` [over a scratch git tree I made from the tarball, never in a project tree]:
  - With an EMPTY `--source-documents` folder: `RULES-NOTE: R5 hashed 0 files of the supplied source`, `RULES: clean (325 files)`, rc 0.
  - Control, a planted tracked `.gitleaksignore`: `RULES: R1 .gitleaksignore:0`, rc 1.
  - **Found on the way:** with NO option the program hashes `<root>/../1_Project_Definition/Source_Documents` when that folder exists (its header line 20). The kit therefore allows ONLY the empty-folder form.
- Tools [shasum]: five files copied unchanged from `d1831/gate` (`clone.py`, `heavy.py`, `hosted.py`, `run_step.py`, `words.py`, hashes equal to kit B1831's), plus the new `commit-message.txt` (`4112f48f...`).
  - `words.py --control`: `CONTROL FIRED: 13 of 13`.
  - Commit message: `WORDS: clean (1 files)`; gitleaks rc 0 (control rc 1); subject 142 bytes.
  - The 13 proposed test names: `WORDS: clean (1 files)` (control `F15_x_by_round_2_y`: 1 hit).
- Toolchain [17:50:59]: `.tools/dotnet/dotnet` `10.0.404`; gitleaks `8.30.1`.
- Machine [17:50:59]: load 4.75 5.63 4.95; 1003 GiB free; `.tools/` has no `b1845` and no lock folder.
- Panes: 12 in all; 3 OXPd2 panes (X14, X19, X24); none named X18.
- CI [`grep -n` over `ci.yml` at the head]: triggers are `push` (`main`, `b[0-9]*/**`), `pull_request` and `workflow_dispatch`, so the pull request's run builds the merge at landing (the basis of Q21's default). sha256 `c3894bbc...`, equal to round 1.

## D-DECISIONS (all Tuesday's as coordinator; none the product owner's)
- **D20** off-thread refresher call (ruling 1).
- **D21** overlap after a time-out stays a limit, with cell F13 (ruling 1, second half).
- **D22** F15 and U03 extended (ruling 2).
- **D23** idle re-check after a refresh (ruling 3).
- **D24** set-back-then-restart: a limit line plus E08's bound (ruling 4, framed as a DECISION).
- **D25** clearing writer and P04 (ruling 5).
- **D26** R08 and R09 (ruling 6, F4).
- **D27** "less than" made the text, pinned by R10; `RestartWindow` removed, with V02 (ruling 6, F5).
- **D28** B07; the blocking handler as a README line and a records line, no code (ruling 7).
- Window 180/140, pane X18, opus, the wave's lock (ruling 8). The kit's FOR TUESDAY section says what each delta reader re-runs (ruling 9).

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q21 (STOP-CLASS)** a moved `main`. Default: never rebase the pushed commit; push fast-forward; STOP only if the moved `main` touches the lane or the solution file. Alternatives: rebase with force-with-lease, which needs the hold lifted in words; or merge `main` into the branch.
- **Q22** `Task.Run`. Alternative: `Task.Yield`, which carries a context risk.
- **Q23** D21 as a limit. Alternative: close it, so no new call starts while a timed-out call still runs.
- **Q24** F15 through a `NewToken` handler that signs out (deterministic, since `Raise` runs before `TrySetResult`). Alternative: a two-thread race.
- **Q25** re-check in `ObtainAsync`. Alternative: also refuse to accept an answer once idle has passed.
- **Q26** D24 as a limit plus E08. Alternative: re-anchor at every write and on drift at `Sweep`. That only narrows the gap; it does not close it.
- **Q27** clearing writer. Alternatives: pre-size at 6 bytes per character, or bound the user and subject strings.
- **Q28** R09 keeps the built behaviour (a failing read at restart erases the record). Alternative: throw `StoreFailed` from the constructor.
- **Q29** remove `RestartWindow`. Alternative: keep it as reserved.
- **Q30** the blocking-handler line goes in README Limits and records. Alternative: records only, reading "stays a records line (no code)" narrowly.
- **Q31** how "red first" reads. Default: code-change cells are red against round-1 code; guarded-rule cells are red against round-1 code with their mutant applied. Alternative: mutants on the fixed code only.
- **Q32** names.
- **Q33** mutant runs: this round's 12 plus round 1's mTimeout, mRace and mLate, each over the lane's test PROJECT (a path, not a filter; its total printed). Alternative: the whole suite each time.
- **Q34** windows 180/140, pane X18.
- **Q35** G1 delta review, both readers.

## UNMEASURED
- What `Task.Run` makes of a null inner task. Cell F14 settles it; both shapes gave `RefreshFailed` at round 1 (RELAYED from B1838).
- Whether F12's 1500 ms bound holds on the hosted Windows runner.
- Whether a `ClearingBufferWriter` at today's estimate still grows on the escaped rows. DERIVED from B1838's allocation run with `ArrayBufferWriter`; P04 asserts it grew.
- How WP1.4's refresher (Microsoft's library) behaves before its first await, and whether it rotates renewal state.
- None of the new cells has been built or run; the drafter ran no build and no test.

## CHAIN INPUTS (MEASURED LITERALS rule 4: every input is made by an earlier step or exists at the base)
| Step | Inputs | Where each comes from |
|---|---|---|
| 0 | the kit, the stamp, the verdicts | Tuesday's stamp; files that exist now |
| 1 | `d1845/gate/` (6 files), the origin branch at `70c1fad5`, the project deploy key and identity | exist now (MEASURED) |
| 2 | the clone's test files | Step 1's clone |
| 3 | the Step-2 listing, the round-1 code, the readers' mutant edits | Step 2; Step 1's clone; `B1839_verify/tests/mutants.py`, B1838 VERDICT section 6 |
| 4 | the Step-3 cells | Step 3 |
| 5 | `<lane>/scratch/empty-folder` | made at Step 5 (a new empty folder) |
| 6 | the staged tree, `commit-message.txt` | Steps 3 and 4; Step 1's gate copy |
| 7 | the commit, `origin/main` | Step 7(a); fetched at 7(b) |

## STOP-SEVERITY CHECKS NOT RUN ON A REAL OUTPUT (marked NEVER RUN in the kit)
- The owned-paths property check.
- The hosted comparison of the new head.
- The heavy runner for this kit.
- The Step-2 listing program: the seat writes it, and its control is `RefreshCellTests.cs:108`, which must be listed.

## OUTSIDE-THE-FENCES DISCLOSURE
- Writes: only the kit, its `.measured` sidecar, this report, and scratch under `fleet/state/s304/d1845/` (`gate/`, `head/` tarball, `scratch/`, `logs/`, `pointers.txt`, `claims.txt`, hosted logs). In scratch, a git `init`/`add` in `scratch/rr/tree`, my own copy of the tarball, to run `repo_rules.py`.
  - The first attempt used a `$S` path and the workspace hook refused it as "outside TUESDAY". Nothing ran; I re-ran with the literal path inside `d1845`.
- No git write and no build or test in any project tree. No Jira, no message, no Artifact.
- `gh` was used only with `-X GET` under the project `GH_CONFIG_DIR`. No key folder was listed, hashed or opened. `repo_rules.py` was never run with the real `--source-documents`.
- Read-only, as the commission names: the B1831 STATUS in `<project>/1_Project_Definition/Briefs/`, the project `CLAUDE.md` (grep and sed of named lines), the `CLARIFICATIONS.md` headings, `tmux list-panes`, `ls <project>/.tools/`, and `ls` of the deploy-key folder (name count only).
