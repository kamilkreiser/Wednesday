STARTABLE: YES

# B1932 DRAFTER REPORT | kit `2026-11-22_B1932_SEAT-X35_oxpd2-d-round2.md` (OXPd 2, lane D, round 2 of 2, seat X35)

Drafted 2026-11-22 22:54 to 23:10 AEDT by a read-only Opus drafter. Kit 66788 bytes, 205 lines (sidecar last line); sidecar 119 claims, `stamp_check.py <kit>` rc 0. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1932/` (below `<d>`).

## BLUF
- The Minor (FOUND 1) is closed by `var outer = saving; ... finally { saving = outer; }` in both overrides (`5-fix.diff`, `SuiteDbContext.cs` +6 -3, plus a doc sentence). Two red-first cells of the G03 and G04 shapes: RED at the pushed head `69eeb1dc` (Data `Total: 63, Errors: 0, Failed: 2`, each `Assert.IsType() Failure: Value is null`), GREEN after the fix (`63 / 0`).
- Info 3: a cell for the `Tracked` half (red under `mNoTracked` only) and one for the synchronous path (red under `mNoSyncFlag` only). Info 3, README: the command interceptor is named among the limits (not asserted; probe P1 measured the bypass). Info 2: a `SavedChanges` handler is named as a limit with its cell (red under `mNoStateChanged`).
- Eight mutants (`mutants2.py`: round 1's four, unchanged, and four new ones) each red on exactly its listed cells, every undo `equal True`, green again `63 / 0`.
- Totals MEASURED: Data 58 -> 63; whole solution on head + patches `total: 1592`, `succeeded: 1588`, `skipped: 4` (1587 + 5); on the merge with `main` `3a3f9f89` + patches `total: 1657`, `succeeded: 1653`. `surface.py` equal against `69eeb1dc` and `7b0f4f55`. `unittest` 111 OK, `RULES: clean (500 files)`, `WORDS: clean (2 files)`, gitleaks clean with a firing control.
- The form is the B1915 fix-round form: one fast-forward commit on the pushed branch, never rebase, the merge-base check (`is-ancestor` rc 1 by design), `hosted2.py` with the seat's own total (PREDICTED 1592).

## FACTS RE-MEASURED (instrument -> result)
- Origin by `gh api -X GET` (23:01:53): branch `b1921/...` one row `69eeb1dc`; `main` `3a3f9f89` (PR 23, lane A1, landed after the gate; one parent `83683af4`); `compare/7b0f4f55...3a3f9f89` 40 files, 0 under the Data folders or `Directory.Packages.props` (control over `7b0f4f55..69eeb1dc`: 6), 0 under `.github/` (control `src/` 21); PR 24 (lane S) open, 6 files, 0 under the Data folders; `b1932` refs 0.
- The drafter's three scratch clones (`clone.py draft`, push URL `invalid://no-push`): `<d>/clone` (work), `<d>/clone2` (fresh apply of both patches: rc 0 each, every file `cmp`-equal to `<d>/clone`; a second `--check` refused), `<d>/clone3` (`merge-tree --write-tree 3a3f9f89 69eeb1dc` tree `ffca56da...`, then both patches).
- Every dotnet job through round 1's `heavy.py` unchanged: 31 jobs, lock waits 0, load1 2.77 to 6.68. Logs `<d>/logs/`; mutant summary `<d>/logs/mutants.out`.
- Probes (scratch class `D1932Probes`, in no patch, file moved to `<d>/_quarantine/probe-file/`, tree rebuilt 63 / 0 after): P1 command interceptor `exception none; rows 4; rows user-9 3`; P2 interceptor `SavedChangesAsync` `SuiteDataException AuditEntryChanged; rows 4`; P3 sync outer / sync nested refused, `rows 3; rows user-9 0`; P4 the flag is off again after a nested refusal.
- Spot lines for Tuesday's stamp check (the sidecar): `0dd8f3f9` (2 red messages), `57a0daa1` (1592), `78e76b7f` (main moves 0), `89f66764` (no `var outer` at HEAD1), `0c3e9c87` (`[Fact]` 13 -> 18), `4459ee74` (merge tree).

## D-DECISIONS (each Tuesday's default as coordinator; kit D1 to D6)
- D1 restore, not a depth counter (the commission's item 1). D2 what a hook's own save wrote stays written, said in the README in words. D3 `SavedChanges`: a limit with its cell; the README line also names a save interceptor's `SavedChanges` step (probe P2, no cell). D4 command interceptor named, not asserted. D5 five cells, one test-only interceptor, nothing existing changed (+128 -0). D6 one fast-forward commit on `69eeb1dc`.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS, S4 answers in words):** what a hook's own nested save wrote stays written, and the README says so. Default **a** (restore, as built). Alternative **b**: refuse any save started inside a save (not built; behaviour change, new cells, new gate read).
- **Q2 (STOP-CLASS, S4 answers in words):** the `SavedChanges` handler. Default **a** named as a limit WITH its cell (built; 63 cells, 1592). Alternative **b** named without a cell (62, 1591); **c** also a sixth cell for the interceptor's `SavedChangesAsync` (not built; 1593).
- Q3 command interceptor: default named only (alternative: a limit cell of P1's shape, +1). Q4 restore vs depth counter: default restore. Q5 Opus by `<project>/CLAUDE.md:7`. Q6 READY Step 0 + 120, push by Step 0 + 90, pane `Datasec/OXPd2-X35`, gate G1 round 2 of 2.

## CHAIN INPUTS (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp S4 (Q1, Q2) | Tuesday's stamp |
| 1 | `<src>` 11 files; `<repo>` local values; origin branch at HEAD1 | exists (`<d>/gate`); exists; GitHub (MEASURED) |
| 2 | six files at HEAD1 | Step 1 clone |
| 3 | `4-cells-red.diff`, `5-fix.diff`; baseline build | Step 1 |
| 4 | green tree; `mutants2.py` | Step 3; Step 1 |
| 5 | green tree, mutants undone; lock-file hashes | Step 4; Step 1 |
| 6 | staged tree; `commit-message-2.txt` | Step 5; Step 1 |
| 7 | staged tree; `run_step.py` | Step 6; Step 1 |
| 8 | the commit; `origin/main` | Step 7; Step 8's fetch |
| 9 to 10 | the commit; origin | Step 7; GitHub |

## UNMEASURED / NOT RUN by the drafter
- Anything on Linux or Windows; the hosted run of the new head (PREDICTED 1592 / 1588 linux / 1573 windows); `dotnet publish` and `release_guard.py` (the guard counts 10 and 11 RELAYED from round 1's STATUS); `restore --force` with the lock-file comparison; `run_step.py` (its wordings RELAYED from round 1's STATUS); any commit or push (the drafter made none); `merge-base --is-ancestor` in a clone (DERIVED rc 1 from the GET compare).
- The live pane list (`tmux list-panes` printed nothing to the drafter): S3 is Tuesday's read.
- The merge total with lane S's PR 24 landed (+5 PREDICTED from that lane, UNMEASURED here).
- Concurrent saves on one context (EF Core's own rule; no cell, named as H11 DERIVED).

## OUTSIDE-THE-FENCES DISCLOSURE
- Writes: only the kit, its `.measured` sidecar, this report, and `<d>/**` (scratch: three clones, `gate/` with the tools and patches, `tools/` with my driver scripts `h.sh`, `mut.sh`, `fresh.sh`, `merge.sh`, `fill.py`, `logs/`, `scratch/`, `_quarantine/`). Git write verbs (`checkout --detach`, `apply`, `read-tree -u --reset`, `merge-tree --write-tree`) ran ONLY in my own scratch clones under `<d>` (push URL `invalid://no-push`), never in a project repo; the project's `.tools/wave1-heavy.lock.d` was taken and released (moved into `<d>/_quarantine/locks/`) by `heavy.py` for each of my 31 jobs, as the rule's round runner does.
- Reads in the project: `CLAUDE.md`, `CLARIFICATIONS.md` (hash and line 682 only), `BACKLOG.md` and `SETUP_RUNBOOK.md` (hashes only), round 1's STATUS (whole), `.tools/` listing and `.tools/b1921/` listing, the deploy-key folder listing (a count of names, no file opened), `Briefs/` listing. Nothing under `Source_Documents/`. No Jira, no az, no HTTP but `gh api -X GET` under the project `GH_CONFIG_DIR` and `git clone` from the origin.
- Two hook refusals during drafting (a `git -C $D/...` write verb whose variable the no-cd hook could not resolve, and an unquoted `$H` word-split): no command ran; each was redone with literal paths in a script under `<d>/tools/`.
- No message to any human; no Artifact, Docs or mail tool used.
