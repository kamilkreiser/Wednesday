GATE B1930: GO WITH FINDINGS @ 69eeb1d on main 83683af

Gate G1 (persistence and audit integrity), round 1, the one reader. OXPd 2, kit B1921 (seat X33, lane D), Q1 = b by
stamp S4 (the coordinator's call, not the product owner's): owed item 43 (1) and (2). Head
`69eeb1dc1e6a24747bcf0708a3cf85f33cfc51f5` on `b1921/d-audit-limit-duplicate-race`, ONE commit, parent `7b0f4f55`.
Read and measured 2026-11-22 22:35 to 22:52 AEDT on Opus 5.5, in my own clones under `fleet/state/s311/g1930/`:
`clone` (detached at the head), `clone2` (7b0f4f55 plus the kit's patches), `clone3` (the merge tree), each by the
kit's `clone.py ... draft` (push URL `invalid://no-push`, no identity). Origin by `gh api -X GET` under the project
GH_CONFIG_DIR: branch = 69eeb1dc (one `b1921` ref); main was 0fc3344a at 22:36 and **83683af4 at 22:47** (pull request
22, lane U, per the coordinator's note, re-read by GET: one parent 0fc3344a). `compare main...69eeb1dc`: diverged,
merge base 7b0f4f55, exactly the six owned paths at the kit's numstat. No write to the project, GitHub or Jira; no push,
no pull request; no `cd`; nothing deleted (probe files and the scanner control moved to `g1930/_quarantine/`).

**BLUF.** The race fix is right and the in-save refusal does what its cells say, on both the async and sync paths and
for both the `StateChanged` and `Tracked` halves; every edit only adds a refusal or a mapping, so nothing main refused
is now accepted. Measured on macOS arm64: red first of each patch on 7b0f4f55 exactly as the seat's STATUS (55/3, 55/0,
58/2, 58/0; the patched tree equals the head's tree `d81e2579`); the four mutants each red on exactly their cells; the
head 58 / 0; the merge with main 83683af4 **1595 / 0 failed**; hosted push run 45017600055 PASS at 1587; main's
45018313743 PASS at 1589. **One Minor finding: the in-save flag is not re-entrant** (a hook that runs a nested save
first can still change or remove every saved entry: measured), so the new README sentence is false in that shape. It
is not a regression (main refused nothing inside a save) and code holding the context still has `ExecuteDelete`, a named
limit; the landing texts name it as still open. The rest are Info. Nothing blocks the landing; a two-line follow-up
closes the Minor (FOUND 1). Whether to land now and owe it, or to fix it first in one more round, is the coordinator's
choice.

## FOUND

1. **Minor (new code, no main regression): the `saving` flag is cleared, not restored, at the end of a nested save.**
   `SaveChanges` and `SaveChangesAsync` set `saving = true` and `saving = false` in `finally`. A `SavingChanges`
   handler or a save interceptor that calls `SaveChanges` itself and then changes entries leaves the outer save running
   with the flag off, so the change detected by the outer save is not refused. MEASURED (probes, run twice):
   G03, a handler that calls `context.SaveChanges()` then sets every tracked entry's actor id during a library append:
   `exception none; rows 4; rows user-9 4`. G04, an interceptor that awaits `SaveChangesAsync` then marks every entry
   deleted: `exception none; rows 0` (the three saved entries AND the one just appended removed). The README's new
   audit sentence ("refuses ... also when a handler of the context's `SavingChanges` event or a save interceptor in its
   options changes or removes it inside the save") is false in these shapes. Fix sketch: `var outer = saving; saving =
   true; try { ... } finally { saving = outer; }` in both overrides (or a depth counter), plus one cell of the G03 or
   G04 shape (red against today's head). Named in pr-body "Still open", the squash body and FOR-RECORDS 1.
2. **Info: a `SavedChanges` handler runs inside `base.SaveChanges`, after the commit.** G05: a handler that marks a
   saved entry `Modified` is refused `AuditEntryChanged`, but the append's row is already written (`rows 4 (3 before
   the append)`): the caller sees a failure for a written row; the change itself is not written. The squash body and
   pr-body say "before the commit nothing is written" and name this shape.
3. **Info: coverage the head does not commit, measured here.** The `Tracked` half: G02 (a detached entry attached as
   `Modified` inside the save) is refused at the head, `table equal True`; with the `Tracked` line removed (my own
   scratch mutant `mNoTracked`, undone, `cmp 0`) it is accepted, `rows user-9 1`. So the half works and has no
   committed cell or kit mutant. The sync path: G01 (`context.SaveChanges()` with a changing handler) refused
   `AuditEntryChanged`, table equal. The command interceptor is not named among the README's limits, though the kit's
   D2 and stamp S4 said it would be (the seat's H7; the pr-body names it).
4. **Info: what `Clear()` drops (H10).** G07: an audit entry pending, unsaved, on the shared context when an add loses
   its race is rolled back with the insert and then cleared: `tracked before 1, after 0; audit rows 0`. The README says
   the tracker is cleared "as after a stale update", not that a caller's other unsaved changes are dropped; the squash
   body and pr-body say it. The library's own calls never leave a pending entry (`AppendAsync` saves at once).
5. **Info: a failure of the re-read (H9).** G06 (the save fails on the key, then the token is cancelled in
   `SaveChangesFailedAsync`): `OperationCanceledException`, no inner exception (the original `DbUpdateException` is
   lost), tracked after 0, and the next append on the same context is written (`audit 1`). The pr-body names it. On
   PostgreSQL a re-read inside a caller's failed transaction could fail the same way instead of mapping: DERIVED from
   that provider's aborted-transaction rule, UNMEASURED (no real server; the library opens no transaction itself).
6. **Each rule's other inputs, read whole and probed, all hold.** `throw;` keeps the original (the not-a-duplicate
   cell asserts the exact type). The pattern `state is EntityState.Modified or EntityState.Deleted` binds as one
   pattern (C#: `or` is a pattern combinator). An exception in the save: G09 (a trigger refusing the audit insert):
   `DbUpdateException`, then marking an entry modified outside a save is not refused, so the flag is reset. Two
   contexts on one connection: G08, a handler on one context changing the other context's entries: the append writes,
   the other context's own save is refused, `rows user-9 0`. Every legitimate library call stays green (52 existing
   Data cells and the whole solution at the merge).
7. **Seat's claims re-measured, all held:** the 14 tool hashes; the commit message equals `commit-message-b.txt`
   (`cmp` rc 0); numstat 17/1, 10/2, 42/3, 72/0, 55/0, 27/0; 500 files; PUBLIC 85 lines and SCHEMA 8 files equal
   (`surface.py` control `CONTROL FIRED: 2 of 2`); the mutant sha256 lines byte for byte the seat's; the hosted numbers.

## NOTHING NEWLY ACCEPTED (does any path accept what main refused? No; DERIVED from the diff, each with a probe)

- The add: a key that main refused before the save is still refused there; a lost race was an untyped failure on main
  and is now `DuplicateDevice` (cells); any other failure is still EF Core's exception (cell). The re-read only reads.
- The context: the pre-save check is unchanged and still first; the watch adds only throws, only while a save runs
  (G09: off after a save, also a failed one). Every shape it misses (FOUND 1, 2, the residual limits) main also missed.

## TESTED (MEASURED, macOS arm64; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at a
time; lock folders moved to `g1930/_quarantine/locks/`; waits only on load or on other holders, never broken)

- Red first, `clone2` at 7b0f4f55: restore rc 0; build 0/0; Data `Total: 52, Errors: 0, Failed: 0`; `1-race-red.diff`
  `Total: 55, Errors: 0, Failed: 3` (the three race cells: `Assert.IsType() Failure: Value is not the exact type`,
  actual `DbUpdateException`; two `Assert.Null() Failure`); `2-race-fix.diff` `55 / 0`; `3b-guard-red.diff` `Total: 58,
  Errors: 0, Failed: 2` (both refusal cells, `Assert.IsType() Failure: Value is null`); `3b-guard-fix.diff` `58 / 0`;
  `git write-tree` of the patched tree `d81e2579d30eedbe286c8ce0b8ae13a274207377` = the head's tree.
- Mutants on the head (`clone`), `mutants.py` unchanged: `mNoMap` `Failed: 1` (the lost-race cell); `mNoClear`
  `Failed: 2` (the audit-after-race and not-a-duplicate cells); `mAlwaysDuplicate` `Failed: 1` (the not-a-duplicate
  cell); `mNoStateChanged` `Failed: 2` (both refusal cells); every `undone ... equal True`; porcelain 0; green again
  `58 / 0`. Mine: `mNoTracked` turns probe G02 from refused to accepted (FOUND 3).
- Probes: a scratch class `G1930Probes` (9 facts, each reports by `Assert.Fail("PROBE ...")`; source
  `g1930/scratch/G1930Probes.cs`, in no patch), built 0/0 and run by `-class` (Total 9, every one reporting); the
  first run's G06 and G07 had faults of my own probe (an interceptor firing twice; a first add that fired the race
  early), corrected and run again (`logs/p3-data.log`); the other seven read the same in all three runs. The file was
  then moved to `_quarantine/probe-file3/`; `git diff --quiet 69eeb1dc` rc 0, porcelain 0, rebuilt, `58 / 0`.
- Merge: `git merge-tree --write-tree 83683af4 69eeb1dc` rc 0, tree `8e637e8f5ec76ea4b94b05108e5a03cfe6090d71`, 500
  files; differs from 83683af4 in exactly the six owned paths and from 69eeb1dc in exactly the nine files main gained.
  That tree checked out in `clone3` (`git diff --quiet 8e637e8f` rc 0 before and after the restore): locked restore rc
  0; build `0 Warning(s)` `0 Error(s)`; whole solution `total: 1595`, `failed: 0`, `succeeded: 1591`, `skipped: 4`,
  `failed Datasec.` 0. Expected hosted on the merge ref: 1589 + 6 = 1595 both legs, succeeded 1591 / 1576, skipped
  4 / 19.
- HOSTED head: `hosted2.py 69eeb1dc... --total 1587 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111
  --floor 111 --hardened-scan` rc 0: run 45017600055, attempt 1, four jobs success, `check runs beside the four: 0`;
  linux 1587 x2 / 1583 / 4, windows 1587 x2 / 1568 / 19; `failed Datasec.` 0 and 0 (control `total: 1587` 2 and 2);
  `HOSTED 69eeb1dc1e6a24747bcf0708a3cf85f33cfc51f5: PASS`.
- HOSTED main: `hosted2.py 83683af4... --wait --total 1589 ...` rc 0: run 45018313743, four jobs success, Analyze
  actions, csharp, python success beside them; linux 1589 / 1585, windows 1589 / 1570;
  `HOSTED 83683af4be3fb39612153c103f922fc2febf7acc: PASS`.
- WORDS: `--control` `CONTROL FIRED: 13 of 13`; over the 223 added lines (7b0f4f55..69eeb1dc) and the stored commit
  message: `WORDS: clean (2 files)`.
- GITLEAKS 8.30.1: control FIRST (a token shape built by program from two halves and 36 random characters, never
  printed): rc 1, `leaks found: 1`, moved to `_quarantine/gl-control`; then the added lines and the message as neutral
  `1.txt`, `2.txt`: rc 0, `no leaks found`.

## CODEQL (read on the pull request; landing step 3)

No CodeQL locally. A reader of the Analyze (csharp) rows checks a `/language:csharp` row AT 69eeb1dc with results_count
0 and open alerts 0, and, if any alert appears, reads it against the shapes this diff adds on purpose: a bare `throw;`
in `catch (DbUpdateException)` after an awaited query; handlers subscribed in the constructors that throw; a mutable
`bool` read in them; the `async` override in `try`/`finally`; in tests, interpolated SQL in `RaceWinner` (literal
synthetic values only) and `eventData.Context!`. An alert is fixed by a new commit and a new gate, never dismissed.

## NOT TESTED

- Nothing on Linux or Windows locally (the hosted legs are those runs). The probes on Linux and Windows: UNMEASURED.
- No publish or release guard locally (the hosted legs ran both: GUARD clean 10 and 11 files). No `run_step.py`
  neutral scan locally (the hosted secret-scan ran it on this head). No `repo_rules.py` or `unittest` locally (hosted
  rules job: `RULES: clean (500 files)`, `Ran 111 tests`, floor 111).
- The red-first runs and the mutants on the merge tree (the six Data files are byte-equal between the head and the
  merge, which differs only outside the Data folders).
- G03 and G04 on main (DERIVED: main has no in-save watch, so both shapes, and the plain ones, are accepted there).
- No real PostgreSQL or SQL Server (by rule).

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 151 bytes (not the commit subject, 288 bytes). `squash-subject.txt` 160 bytes, the title plus
  ` (#PRNUM)`. `squash-body.txt`: what and why in three paragraphs, naming the dropped unsaved changes and the shapes
  still open (an entry being added, ExecuteUpdate, ExecuteDelete, raw SQL, a command interceptor, a nested save, a
  SavedChanges handler), ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. `pr-body.md`: why (item
  43 (1) and (2)), what changed, what proves it, still open (FOUND 1 to 5 and the residual limits), who decides: the
  coordinator, as coordinator; no line says the product owner decided anything; ends with the Claude Code line.
  `landing.txt` in B1924's form with this pull request's numbers: main 83683af4, merge tree 8e637e8f, merge-ref totals
  1595 both legs, succeeded 1591 / 1576, skipped 4 / 19, RULES 500, Ran 111, floor 111; step 6 main's push run PASS
  at 1595; MAIN MOVES for lanes S (+5) and A1 (+57) (E and U already landed), with any change under the two Data
  folders or to the EF Core package a STOP. `FOR-RECORDS.md` for the records pass.

## SCANS (of the landing texts, after the last edit)

- `words.py` per file: `pr-title.txt`, `squash-subject.txt`, `squash-body.txt` every class 0. `pr-body.md`:
  `coordinator` 2 (the required "who decides" line) and 4 non-ASCII bytes (the required robot line), every other
  class 0.
- gitleaks 8.30.1: a fresh firing control, then the texts of this folder as neutral `<n>.txt`: see the last line below.
- `build/squash_scan.py` (main 83683af4's, from `clone3`) with `#PRNUM` replaced by `#23` and `squash-body.txt`:
  control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks (1595 on both legs) and CodeQL read as its
step 3 requires. The Minor finding (FOUND 1) goes to the backlog with its fix sketch unless the coordinator chooses a
fix round first; it is not a condition of this landing.
- gitleaks result: fresh control rc 1 (moved to `_quarantine/gl-control2`); the seven texts of this folder (this file before this line) as neutral `1.txt` to `7.txt`: rc 0, `no leaks found`.
