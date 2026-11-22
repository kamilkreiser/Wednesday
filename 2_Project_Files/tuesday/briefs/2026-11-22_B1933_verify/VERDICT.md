GATE B1933: GO WITH FINDINGS @ 07ae18e on main 40bfe5d

Gate G1 (persistence and audit integrity), round 2 of 2, the one reader. OXPd 2, lane D: kit B1921 (seat X33, round 1,
Q1 = b) and kit B1932 (seat X35, round 2, Q1 = a, Q2 = a by stamp S4: the coordinator's calls, not the product
owner's): owed item 43 (1) and (2). Head `07ae18eb4e44f8537423af479d03db92b9114b24` on
`b1921/d-audit-limit-duplicate-race`, TWO commits (`69eeb1dc` over `7b0f4f55`, `07ae18eb` over `69eeb1dc`). Read and
measured 2026-11-22 23:27 to 23:40 AEDT on Opus 5.5, in my own clones under `fleet/state/s311/g1933/`: `clone`
(detached at the head; at `69eeb1dc` once for the probe control), `clone2` (main `40bfe5db` with the merge tree in
index and worktree), each by the kit's `clone.py ... draft` (push URL `invalid://no-push`, no identity). Origin by
`gh api -X GET` under the project GH_CONFIG_DIR at 23:28 and 23:36: branch = 07ae18eb (one `b1921` ref); main =
40bfe5db; open pull requests 0; `compare 69eeb1dc...07ae18eb` ahead 1, behind 0, README.md +11 -4, SuiteDbContext.cs
+6 -3, AuditTests.cs +128; `compare 40bfe5db...07ae18eb` diverged, ahead 2, behind 4, merge base 7b0f4f55. No write to
the project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted (probe files and the scanner control
moved to `g1933/_quarantine/`). One `git fetch` in `clone2` was refused by the origin (no key in a draft clone): it
fetched nothing and was not needed (the objects were in the clone).

**BLUF.** Round 2 closes what it set out to close. The flag is restored, not cleared (`SuiteDbContext.cs:96`, `:104`,
`:111`, `:119`), so round 1's FOUND 1 shapes are now refused: G03 `AuditEntryChanged; rows 4; rows user-9 0` (was
`none; rows 4; rows user-9 4`), G04 `AuditEntryChanged; rows 4` (was `none; rows 0`). Outside the frame the restore
holds too: three levels, a nested save that throws, and every sync/async mix are refused on the head and were accepted
at `69eeb1dc`. The eight mutants are each red on exactly their cells. `surface.py` is equal against both refs. The
merge with main 40bfe5db reads **1662 / 0 failed**, RULES 530. The head's push run reads PASS at 1592. Words and
gitleaks are clean. **One Minor finding, which round 2 did not introduce: a hook that catches the refusal and goes on
keeps its change** (FOUND 1, measured the same at `69eeb1dc`), so the README's audit sentence is still false in that
one shape. It is not a regression (main refuses nothing inside a save). Nothing blocks the landing. There is no round
3, so the landing texts name the shape as still open and FOR-RECORDS carries it to the backlog with a fix sketch.
Whether to land now with it owed, or to send it as a card first, is the coordinator's choice.

## FOUND

1. **Minor (from round 1's design, no main regression): a hook that catches the refusal keeps its change, and the
   outer save writes it.** `RefuseDuringSave` throws from inside the tracker's `StateChanged` / `Tracked` event
   (`SuiteDbContext.cs:203` to `:211`), and EF Core raises those after the entry's state has changed. The exception
   therefore lands in the hook's own code, with the entry already `Modified` or `Deleted`. If the hook catches it (a
   catch-all around the hook's own work is enough), the outer `base.SaveChanges` writes the change. The pre-save check
   ran before the hook, and nothing checks again before the commit. MEASURED (scratch probes, macOS arm64, the same
   at `07ae18eb` and at `69eeb1dc`): N5a, a `SavingChanges` handler that catches around each change: `caught 3;
   exception none; rows 4; rows user-9 4` (all three saved rows changed, plus the appended one, which is the named
   being-added limit). N5b, a save interceptor that catches around each removal: `caught 3; exception none; rows 1`
   (all three saved rows removed). The README's audit sentence (`README.md:26` to `:30`, "the change is never
   written: ... inside it when a handler ... or a save interceptor ... changes or removes it") is false in this shape,
   and so is the doc comment's "the change is never written" (`SuiteDbContext.cs:198`).
   By the same mechanism its `SavedChanges` line (`:56`, "the change is never written") is false for a `SavedChanges`
   handler that catches (DERIVED, not probed). Fix sketch: (a) name it among the Limits with a limit cell of N5a's
   shape; or (b) a latch set by the watch when it refuses, read by a library-owned command interceptor that refuses
   the save's own commands before they run (DERIVED; not built; its order against a host's interceptors is
   UNMEASURED). Named in pr-body "Still open", the squash body and FOR-RECORDS 1.
2. **Info: a hook that saves first and then ADDS an entry.** N4a: `exception none; rows 5` (the added entry is
   written, back-dated 30 days through the test-only `AuditEntry.Create`). Host code cannot make an `AuditEntry`
   (private constructor `Audit.cs:103`, `internal` factory `:122`), so outside the library this is an append through
   `EfAuditLog` (timed by the clock) or reflection, not a change to a saved entry. N4b (save, then add, then change
   the added entry): `none; rows 5; rows user-9 1`, which is the named and asserted entry-being-added limit
   (`README.md:60` to `:62`).
3. **Info: the outside-the-frame shapes the commission named all hold on the head** (each MEASURED; each accepted at
   `69eeb1dc` unless stated otherwise):
   - Three levels, with the change at level 2 after level 3 (N1a) or at level 1 after 2 and 3 (N1b): both
     `AuditEntryChanged; rows 4; rows user-9 0`.
   - A nested save that throws from its handler, caught by the outer hook, then a change (N2a): nested
     `InvalidOperationException`, outer `AuditEntryChanged; rows 3; rows user-9 0`. At `69eeb1dc`: `outer none; rows 4;
     rows user-9 4`. So `finally` gives back the outer value.
   - A nested save refused by the database (a trigger), then a change (N2b): outer `AuditEntryChanged; rows 3`.
   - Sync and async mixed: a sync outer with an async nested save in a handler (N3a) `AuditEntryChanged; rows 4; rows
     user-9 0`; a sync outer with an interceptor whose sync step runs an async nested save, then removes (N3b)
     `AuditEntryChanged; rows 4`; an async outer with an interceptor whose async step runs a sync nested save, then
     removes (N3c) `AuditEntryChanged; rows 4`.
   - After a nested throw ends the whole save (N6): `InvalidOperationException; marking outside a save none; rows 3`.
     The flag is off again.
4. **Info: the README read sentence by sentence.** Everything else is true as written: the restore and "what a hook's
   own save already wrote stays written" (`:29` to `:30`: G03, G04 and N1 each keep 4 rows; N2a keeps 3); the
   `SavedChanges` line's commit order and its cell (G05 `rows 4 (3 before the append)`; cell `AuditTests.cs:261`); the
   being-added line (N4b); the doc comment's restore sentence at `SuiteDbContext.cs:198` to `:199` (its "the change is
   never written" at `:198` has FOUND 1's exception, like the README's audit line). The command-interceptor sentence
   (`:54` to `:55`) is RELAYED from the drafter's probe P1, which I did not re-run. Its claim that the interceptor "can
   change" a save's SQL is the same class as the raw-SQL limit.

## ROUND 1'S PROBES G01 TO G05 ON THE HEAD (the shapes of round 1's file, re-typed in `G1933Probes`)

- G01 sync handler change: `AuditEntryChanged; table equal True; rows user-9 0` (cell `:239`).
- G02 detached tracked as modified: `AuditEntryChanged; table equal True; rows 3; rows user-9 0` (cell `:217`).
- G03 handler saves first, then changes: `AuditEntryChanged; rows 4; rows user-9 0`. Round 1's FOUND 1 is closed
  (cell `:171`).
- G04 interceptor saves first, then removes: `AuditEntryChanged; rows 4`. Closed (cell `:202`).
- G05 `SavedChanges` marks modified: `AuditEntryChanged; rows 4 (3 before the append)`, named and asserted as the
  round-2 kit's D3 says (cell `:261`).
- Control: the same probe file at `69eeb1dc` printed G03 `none; rows 4; rows user-9 4` and G04 `none; rows 0`, so the
  probes can tell the two heads apart.

## TESTED (MEASURED, macOS arm64; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at a
time; load1 1.6 to 7.0; lock waits 0; lock folders moved to `g1933/_quarantine/locks/`)

- Tools: the eleven files of kit B1932's THE TOOLS copied from `d1932/gate`, sha256 11 of 11 equal. Commit 2's stored
  message equals `commit-message-2.txt` (`cmp` rc 0).
- Head (`clone` at 07ae18eb, 500 files): locked restore rc 0, porcelain 0; build `0 Warning(s)` `0 Error(s)`; Data
  `Total: 63, Errors: 0, Failed: 0`.
- Mutants (`mutants2.py` unchanged; every `undone ... equal True`, then `git diff --quiet 07ae18eb` rc 0), Data 63
  each:
  - `mNoMap` `Failed: 1`: the lost-race cell.
  - `mNoClear` `Failed: 2`: the audit-after-race and not-a-duplicate cells.
  - `mAlwaysDuplicate` `Failed: 1`: the not-a-duplicate cell.
  - `mNoStateChanged` `Failed: 6`: `:171`, `:202`, `:239`, `:261` and round 1's two refusal cells.
  - `mNoTracked` `Failed: 1`: `:217`.
  - `mNoSyncFlag` `Failed: 1`: `:239`.
  - `mNoRestoreSync` `Failed: 1`: `:171`.
  - `mNoRestoreAsync` `Failed: 1`: `:202`.
  - Each is exactly the set the round-2 kit's THE CONTROLS lists. Green again afterwards: 63 / 0.
- Probes: a scratch class `G1933Probes` (17 facts; each reports by `Assert.Fail("PROBE ...")`; source
  `g1933/scratch/G1933Probes.cs`, in no patch). Built 0/0 and run with `-class` on the head and on `69eeb1dc`. Both
  times the file was moved out afterwards (`_quarantine/probe-file/` and `probe-file-head1/`). Then `git diff --quiet
  07ae18eb` rc 0, porcelain 0, rebuilt, `63 / 0`.
- Surface: `surface.py clone 69eeb1dc...` and `... 7b0f4f55...` each rc 0, `PUBLIC: equal (85 lines)`, `SCHEMA: equal
  (8 files)`. Control `CONTROL FIRED: 2 of 2`.
- Paths: `diff --name-status 69eeb1dc 07ae18eb` gives three `M` rows (the three owned paths).
  `diff --numstat 7b0f4f55 07ae18eb` gives the six round-1 paths at 17/1, 19/4, 45/3, 200/0, 55/0, 27/0. The six
  files are printable ASCII, with no tab, 0 CR and a final LF (control: a planted U+200B counts 1).
- Merge: `git merge-tree --write-tree 40bfe5db 07ae18eb` rc 0, tree `ecfaad0aefab7d7a1fe3aa549e5c4415b0d179eb`,
  530 files.
  - It differs from 40bfe5db in exactly the six owned paths, each blob equal to the head's. It differs from 07ae18eb
    in the 46 paths main gained since 7b0f4f55, of which 0 are under the two Data folders or `Directory.Packages.props`
    (control: 6 over `7b0f4f55..07ae18eb`).
  - That tree in `clone2` (`git diff --quiet` rc 0 before and after the restore): locked restore rc 0; build 0/0;
    whole solution `total: 1662`, `failed: 0`, `succeeded: 1658`, `skipped: 4`; `failed Datasec.` 0 (control `Test
    run summary` 1); Data 63 / 0; `unittest` `Ran 111 tests`, `OK`; `repo_rules.py` (no `--source-documents`)
    `RULES: clean (530 files)`.
  - Expected hosted on the merge ref: 1651 + 11 = 1662 on both legs, succeeded 1658 / 1641, skipped 4 / 21,
    RULES 530, unit 111.
- HOSTED head: `hosted2.py 07ae18eb... --total 1592 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111
  --floor 111 --hardened-scan` rc 0.
  - Run 45021959952, four jobs success, attempt 1, check runs beside the four 0.
  - linux 1592 x2 / 1588 / 4, GUARD 10 files; windows 1592 x2 / 1573 / 19, GUARD 11 files; rules 500 files and floor
    111; every hardened secret-scan row OK.
  - `HOSTED 07ae18eb4e44f8537423af479d03db92b9114b24: PASS`.
- HOSTED main: `hosted2.py 40bfe5db... --total 1651 --rules 530 --skipped-linux 4 --skipped-windows 21 ...` rc 0.
  - Run 45020207120, four jobs success; Analyze actions, csharp and python success beside them.
  - linux 1651 / 1647 / 4, windows 1651 / 1630 / 21.
  - `HOSTED 40bfe5db658f8dd767eaf34e53dc9e89f0ef2cf4: PASS`.
- WORDS: `--control` gives `CONTROL FIRED: 13 of 13`. Over the added lines of commit 1 (223) and commit 2 (145), and
  both stored messages (346 and 393 bytes): `WORDS: clean (4 files)`.
- GITLEAKS 8.30.1:
  - Control FIRST: a token shape built by a program from two halves and 36 random characters, never printed. rc 1,
    `leaks found: 1`, then moved to `_quarantine/gl-control`.
  - The four texts above as neutral `1.txt` to `4.txt`: rc 0, `no leaks found`.

## CODEQL (read on the pull request; landing step 3)

No CodeQL locally. Main 40bfe5db's Analyze rows are success. A reader of this pull request's Analyze (csharp) rows
checks for a `/language:csharp` row AT 07ae18eb with results_count 0 and 0 open alerts. If an alert appears, read it
against the shapes this diff adds on purpose, which are listed in landing.txt step 3; round 2 adds two of them: the
flag saved in a local and written back in `finally`, and an un-`ConfigureAwait`ed await in the test-only
`NestedSaveThenRemove`. An alert is fixed by a new commit and a new gate, never dismissed.

## NOT TESTED

- Nothing on Linux or Windows locally (the hosted legs are those runs). The probes on Linux and Windows: UNMEASURED.
- No publish, release guard or `run_step.py` neutral scan locally. The head's hosted run covered all three (GUARD 10
  and 11 files; secret-scan rows OK), and so did the seat's local chain (RELAYED).
- The red first of `4-cells-red.diff` at `69eeb1dc` was not re-applied by me. Instead, the gate's own probes G03 and G04
  at `69eeb1dc` show the two shapes accepted there, and `mNoRestoreSync` / `mNoRestoreAsync` turn exactly those two
  cells red on the head.
- The mutants on the merge tree: the six Data files are byte-equal between the head and the merge, which differs only
  outside the Data folders.
- The drafter's probes P1 to P4 (RELAYED; N2a, N3a and N6 cover P3's and P4's shapes on my side).
- No real PostgreSQL or SQL Server (by rule).

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 178 bytes (not either commit subject).
- `squash-subject.txt` 187 bytes: the title plus ` (#PRNUM)`.
- `squash-body.txt`: what and why in three paragraphs, covering both commits. It names the dropped unsaved changes,
  the restore and what a hook's own save keeps, and the `SavedChanges` order. It names the shapes still open: an
  entry being added, ExecuteUpdate, ExecuteDelete, raw SQL and a command interceptor (each named in the README), and
  a hook that catches the refusal (not yet named). It ends `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- `pr-body.md`: why (item 43 (1) and (2)), what changed in both commits, what proves it, and what is still open
  (FOUND 1 first, then the residual limits). Who decides: the coordinator, as coordinator, including the second
  commit and every choice inside both. No line says the product owner decided anything. It ends with the Claude Code
  line.
- `landing.txt` in round 1's form with this head and these numbers:
  - main 40bfe5db; merge tree ecfaad0a (530 files).
  - Merge-ref totals: 1662 on both legs, succeeded 1658 / 1641, skipped 4 / 21, RULES 530, Ran 111, floor 111.
  - Step 6: main's push run must read PASS at 1662.
  - MAIN MOVES: E, U, A1 and S have already landed; no pull request was open at the read. If main moves anyway, the
    totals become that main's plus 11, and any change under the two Data folders or to the EF Core package is a STOP.
- `FOR-RECORDS.md` for the records pass.

## SCANS (of the landing texts, after the last edit)

- `words.py` per file:
  - `pr-title.txt`, `squash-subject.txt`, `squash-body.txt`: every class 0.
  - `pr-body.md`: `coordinator` 2 (the required "who decides" line) and 4 non-ASCII bytes (the required robot line);
    every other class 0.
- `build/squash_scan.py` (main 40bfe5db's: `git diff --quiet 40bfe5db -- build/squash_scan.py
  .github/workflows/ci.yml` rc 0 in `clone2`), run with `#PRNUM` replaced by `#25` and `squash-body.txt`: control
  `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks 8.30.1: a fresh firing control, then the texts of this folder as neutral `<n>.txt`: see the last line below.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks (1662 on both legs) and CodeQL read as
its step 3 requires. FOUND 1 is not a condition of this landing. There is no round 3, so it goes to the backlog with
its fix sketch (FOR-RECORDS 1), or to the product owner as a card if the coordinator chooses not to land with it owed.
- gitleaks result: fresh control rc 1, `leaks found: 1` (moved to `g1933/_quarantine/gl-control2`); the seven texts of this folder (this file before this line) as neutral `1.txt` to `7.txt`: rc 0, `no leaks found`.
