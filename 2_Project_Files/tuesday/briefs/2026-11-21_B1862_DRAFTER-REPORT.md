STARTABLE: YES (after Tuesday's stamp; Stamp S4 must answer Q34, the moved main and the solution file, IN WORDS: STOP-class)

# B1862 drafter report: lane G (WP1.7 in part, `Datasec.Suite.Jobs`) fix round, round 2 of 2

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1862_SEAT-X23_oxpd2-wp17-jobs-fix-round.md` (its sidecar `.measured` beside it). Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s306/d1862/gate/` (eleven files, hashed in the kit). Drafted 20:46:30 to 21:17:58 AEDT 2026-11-21 (clocks by `date`; the kit head lists its reads, the sidecar line 1 its write clock), Opus. `stamp_check.py <kit>` exits 0: 246 claims, 246 measured (each line names the run and what it printed, or why the literal is a name and not an output).

## BLUF
- **Every ruling of the commission has a cell seen RED and then GREEN, MEASURED in my own scratch clone** (not a harness: the lane's own test project, the round-1 `heavy.py`, the wave lock, load1 first, 0 lock waits every job). Against HEAD1's product code the Jobs project read `total: 120`, `failed: 10` (exactly the ten cases of rulings 1, 2, 4, 5 and the close site); with `1-code.diff` `failed: 0` in nine runs; whole solution `total: 1093`, `failed: 0`, `skipped: 4`.
- **The census found ONE more raw-exception site** beside B1859's `:328`: the answer stream's `DisposeAsync` in the `finally` (round 1 `PrintJobSender.cs:336`). MEASURED: a good answer whose stream throws on close made `SendAsync` throw `TaskCanceledException` after the printer accepted the job. Fixed under D20 (Q25, default: the close is caught, the answer or its refusal stands) with its own cell (two rows).
- **Ruling 2 needed THREE yield points, not two:** with only `RunAsync` yielding, an answer stream that blocks its thread ends at the SEND bound (30 min), not the answer bound (60 s); a private `ReadAnswerAsync` yields too (mutant mYieldRead proves the cell sees it). I used `ConfigureAwaitOptions.ForceYielding`, not `Task.Yield()` (which posts to a caller's SynchronizationContext): D21, Q26.
- **The solution file CONFLICTS with main `977cbeb2`** (MEASURED by `merge-tree`: `CONFLICT (content): Merge conflict in Datasec.Suite.slnx`, at HEAD1 and at my fix). Q34 STOP-class default: the one fix commit, then ONE merge commit of main whose only resolution is the solution file by `place.py`. I prototyped it: the merged diff against main is 32 `A` plus 1 `M` (2 added, 0 removed), the whole solution read `total: 1290`, `failed: 0`; `RULES: clean (400 files)`; guards 10 and 11; neutral scan `25 of 25`, `objects of this commit not among them 0`.
- **One round-1 cell had to change:** J08 send bound read `fake.Tokens[0]` right after the bound; with the exchange on the pool the transport may be called later; it failed ONCE under load (`ArgumentOutOfRangeException`). `2-cells.diff` adds one `Guard.Signal` before that read (a superseded line).

## Facts re-measured (instrument, result)
- `gh api -X GET` under the project `GH_CONFIG_DIR` (21:03:56): `.private` true, push true; branch `b1841/wp17-scan-and-print-jobs` = `5dd0f8595bc7f243c2ae97585e63fb32ad0d70bb`, parent `762e774e`; main = `977cbeb2994e6592ba9e4ce677c278c5131d11c4`; open PRs 0; no PR on a b1841 head; no `b1862` ref.
- `git diff --name-only 762e774e 977cbeb2`: 40 files, 0 under the lane's two folders (control: 17 under `src/Datasec.Suite.Graph/`); `.github`, `build`, `Directory.Packages.props` unchanged between them.
- The six round-1 lines printed at HEAD1: `:107` and `:281` `catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)`; `:252` `catch (JobServiceException ex) when (ex.Reason is TransportFailed or ResponseTimedOut)`; `:302` `catch (Exception ex) when (ex is not OperationCanceledException || !token.IsCancellationRequested)`; `:328` `catch (Exception ex) when (ex is not OperationCanceledException and not JobServiceException)`; `:330` the comment "never a raw exception to the caller".
- Census (`grep -n -E '\bcatch\b'` over the 14 library `.cs` files; control: a planted line counts 1): **28 catch sites at HEAD1, 16 with `when`**; 32 and 18 at the fix. Only `:328` and the `finally` close let a non-typed exception out of the sender; F4's `ObjectDisposedException` sites in the receiver besides.
- Hosted, by `hosted.py` (R5-aware, `--unit 60 --floor 60`): HEAD1 `--total 1081 --rules 360` PASS; main `977cbeb2` `--total 1170 --rules 368` PASS (control `--total 1171` FAIL 4).
- Toolchain 10.0.404, gitleaks 8.30.1; load 3.44 at 21:03; 999 GiB free; panes OXPd2-X25, X15, X20 live, none X23; no `.tools/b1862`; lock folder absent at 21:03:49.

## What I measured on my prototype (all in `<scratch>` = `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s306/d1862`, logs in `logs/`)
- RED (`p-red4`, cells as shipped on HEAD1's product): failed 10, each by assertion (type mismatch, the 10 s guard's message, or the cell's own message); C06 exact, C06 free race, A03 green (pinning cells).
- GREEN (`p-green1..4`, five reruns): 120/0; Jobs assembly 564 to 637 ms (round 1: "about 1.2 s" for 108): the added wall time is nil within noise; the RED run costs 30 s (three 10 s guards).
- Mutants (eleven, `3-mutants.txt`, on fixed product code): ten RED on their named cells; **mReasonDisposed SURVIVES** (a race-only line of D22; named in the kit, D27 (b)). mCheckOutsideLock RED in 8 of 8 runs; mSpoolCap RED on C06 exact and the free race; mUnknownEarly RED on A03. My own trap, written into the kit: a `--no-build` run after an undo runs the mutant's binaries (five runs read `failed: 1` until I rebuilt).
- The merge prototype: restore `--locked-mode` with `CI=true` rc 0, nothing changed; build 0/0; 1290/0/4; publishes rc 0; `GUARD: clean (10 files)` and `(11 files)`; `repo_rules.py` (no option, `../1_Project_Definition` absent) `RULES: clean (400 files)`; on a worktree of the fix commit `RULES: clean (361 files)`; `unittest` `Ran 60 tests` OK.
- Text: 562 added lines, 0 non-printable, 0 tabs (control U+200B counts 1); `words.py` `WORDS: clean (3 files)` with both messages (control 13 of 13); boundary words 0 in the 57 added product lines (18 of 18 planted fire); gitleaks rc 0 on the diffs, the messages and the whole prototype clone (two-half planted token rc 1).
- `git apply --cached --check` with a scratch index: `2-cells.diff` then `1-code.diff` rc 0 on HEAD1; the resulting tree equals my prototype's tree (`1402c107...`).

## D-decisions (the kit's D19 to D32; the main ones)
D19 the filter exactly in the reader's shape; D20 the close caught; D21 ForceYielding in `CopyAsync`, `RunAsync`, `ReadAnswerAsync`; D22 `Fail` catches `ObjectDisposedException`, the receive ends `JobNotFound`, the README lists every `ObjectDisposedException` member exactly; D23 sticky `SpoolCorrupt`/`StorageFailed`; D24/D25 the drafter's `2-cells.diff` and `1-code.diff` applied by the seat (cells first); D30 the merge commit.

## Q-questions for Tuesday (each with its default; STOP-class marked)
- **Q34 (STOP-CLASS; S4 in words): the moved main.** Default: ONE fix commit, then ONE merge commit of the then-current `origin/main` resolving ONLY `Datasec.Suite.slnx` (main's file plus `place.py`), D28's four checks, hosted run on the merge (1290 / 400 PREDICTED). This keeps the squash on main exactly the reviewed `main..head`. Alternative: the fix commit alone; GitHub cannot squash a conflicting PR, so a resolution would be made after the review by whoever writes the branch. Cost of the default: a second commit against ruling 8's "ONE new commit" (a merge, never code).
- Q25 the answer stream's close: default caught (alt: `TransportFailed`, which reports an accepted job as failed).
- Q26 the bounds: default ForceYielding in three places (alt: `Task.Yield()`, `Task.Run`, or two places).
- Q27 disposed spool: default `JobNotFound` from a receive (alt: keep `ObjectDisposedException`, list it).
- Q28 the cells: default the drafter's diff, a new file `HardeningTests.cs` (rules 361 at the fix commit) (alt: the seat writes them, or puts them in existing files).
- Q29 the code: default the drafter's diff. Q30 eleven mutants, mReasonDisposed a named survivor. Q31 named limits. Q32 the census. Q33 `StorageFailed` sticky without a cell (no plantable read failure). Q35 round 2 of 2 (a NO GO is a card). Q36 180/140 minutes, pane X23.

## UNMEASURED
- Your hosted run on the merge head (PREDICTED 1290 / 400 / 4 / 19 / Ran 60). The blocking cells on the hosted Windows and Linux legs. `StorageFailed` stickiness (DERIVED). The cost of the thread-pool hop (microseconds, DERIVED). CodeQL.

## Chain inputs (each produced earlier or present at BASE)
Step 1: `<src>`, `<repo>`'s local values, GitHub (all exist). Step 3: `2-cells.diff` (Step 1's copy). Step 4: the red tree (Step 3), `1-code.diff`, `3-mutants.txt` (Step 1). Step 5: the green tree (Step 4). Step 6: the staged tree (Step 5), both messages (Step 1). Step 7: `C1` (7(a)), `origin/main` (7(b)'s fetch), `place.py` (Step 1), HEAD1's hosted numbers (Step 1).

## STOP-severity checks run on my prototype (PASS, control FIRED) or NEVER RUN
- Owned-paths property: PASS on `HEAD1..ea223fa0` (7 rows) and on the merge (32 A + 1 M); the planted rows are the seat's control (NEVER RUN by me as a planted list).
- ASCII/tab: PASS, control fired. Scanner: PASS, control fired; neutral scan PASS (25 of 25). Words: PASS, control 13 of 13. Boundary: PASS, 18 of 18 planted fired. `repo_rules.py` without `--source-documents`: PASS (`../1_Project_Definition` absent, rc 0). Release guard: PASS 10/11. `place.py --dry` REFUSED after `--write`: fired (rc 2).
- `hosted.py` on a head of this round: NEVER RUN (marked so in the kit). The seat-mode clone: NEVER RUN by me (RELAYED from round 1).

## Reading load (READ-WHOLE of the kit, bytes, by program)
Items 2 to 8: **234,548 bytes** (CLAUDE.md 10,052; CLARIFICATIONS 33,300; the two verdicts 23,034 + 15,215; round-1 kit ranges 31,717 + 3,691; round-1 STATUS ranges 7,081 + 3,726; six tool headers 6,011; the three diffs/texts 40,309; the four product files at HEAD1 42,275; JobSpool range 1,017; FakeTransport and ManualClock 14,861; the two test ranges 2,259), **plus the kit itself (100,804 bytes): 335,352 bytes in all.**

## Outside the fences (disclosure)
- I made two LOCAL commits and one worktree in MY scratch clone (`<scratch>/clone`, push URL `invalid://no-push`, never pushed) under a throwaway local identity `B1862 drafter scratch <drafter@invalid.example>` set by `git config --local` there (not `-c` flags), so that `merge-tree` and the merge prototype could run. No git write in any project tree; no `git` command in `<repo>`.
- I read the two readers' `evidence/` folders (their mutant texts and probe shapes) to make the mutants exact; nothing of a probe file is in the kit's diffs (shapes rebuilt on the lane's helpers).
- Every dotnet job of mine went through `heavy.py` and the wave lock (OXPd_2 `.tools/wave1-heavy.lock.d`), as the commission allows; 0 waits; I released by move into `<scratch>/_quarantine/locks/`.
- `gh api -X GET` only, under the project's `GH_CONFIG_DIR`. No Jira, no message, no Artifact or Docs tool. Nothing deleted: the first-round tools I did not need and my probe file are in `<scratch>/_quarantine/`.
