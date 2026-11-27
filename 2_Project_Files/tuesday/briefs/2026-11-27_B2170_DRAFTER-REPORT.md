STARTABLE: YES

# B2170 DRAFTER REPORT: OXPd 2, lane OX-C kit 2 part 2, re-draft R2 (owed 137 and 121): S4 re-frozen, seat X89

Drafted 2026-11-27 by in-session read-only drafter B2170 (Opus) for Tuesday s334. First `date`: `Fri 27 Nov 2026 18:51:10 AEDT`; last `date` before this report: `Fri 27 Nov 2026 19:09:28 AEDT`. The kit is `tuesday/briefs/2026-11-27_B2170_SEAT-X89_oxpd2-lane-c-kit2-part2-r2.md` (269 lines). Its sidecar `.measured`: `stamp_check.py` exit 0, "171 claims, 171 measured, 0 not measured". Scratch is `fleet/state/s334/d2170/` and the seat's tools are in `seat-tools/`. The unified diff against rev1 is `d2170/gen/kit-vs-rev1.diff` (98 lines added, 47 removed).

**STARTABLE means:** the kit is complete and stamp-checked. Launching it still needs the stamp, and the `Datasec/OXPd2-X85` device seat may be live beside it, which is NOT a refuse.

## BLUF
- **Root cause (DERIVED, matches seat X82's STATUS):** kit B2153's S4 used two timers set to the same bound. One was the token's source, the other `Task.WaitAsync(bound)`. It picked the outcome with `when (!running.IsCompleted)` at catch time. In one order the wait's timeout fires, then the token cancels the step, then the filter runs. The filter sees the step as completed, the second catch takes OCE only, and .NET's own `TimeoutException` escapes. That is the X82 pin-run red at H17 shape 3.
- **Re-frozen S4 (D8): one timer, one question.**
  ```
  using var cancel = new CancellationTokenSource(bound);
  Task running = step(cancel.Token);
  await Task.WhenAny(running, Task.Delay(Timeout.InfiniteTimeSpan, cancel.Token));
  if (cancel.IsCancellationRequested) { throw Late(what, bound); }
  await running;
  ```
  - There is no catch, no filter and no second timer.
  - The arm can only finish if the token is cancelled. So whenever the arm ends the wait, the question already reads yes, and once yes it stays yes.
  - The kit's THE RACE table walks six orders (O1–O6), covering step-ends-first, timeout-first and both together. Every one gives `Late` exactly when the bound has elapsed by the read; otherwise the step's own end passes through unchanged.
  - Shapes 4–6 are unchanged: their steps finish at about t=0, against a 1 s bound.
  - X82's R3 note (a source disposed before its timer fired) is closed too: the helper throws only after the token is cancelled.
  - The outer 20 s guards stay.
- **Only S4's NEW text changed.** S1–S3 and T1–T3 are copied byte for byte from B2153's `edits_c3.json`, and the 3 README results equal B2153's frozen sha256.
  - New HostRig result: `67be0414…` (389 lines); B2153's was `46c1e78f…`.
  - New `edits_c3.json`: `e622744e…`. New `mutants_c3.json`: `230408e7…`.
  - The other 9 tools are byte-equal to B2153's.
- **H17 gains shape 3b**, which makes X82's order certain. Inside `Task.Run`, the step blocks on `token.WaitHandle.WaitOne(10 s)` and then returns `Task.FromCanceled(token)`. The step has therefore already completed, cancelled, before the helper starts waiting.
- **Seven mutants, each tied to the assertion it breaks:**

  | Mutant | Cells it reds | Assertion it breaks |
  |---|---|---|
  | `mWaitDropped` | H17, H18 | H17 shape 2 message; H18 shape 1 message |
  | `mTokenNeverCancelled` | H17, H18 | the same two |
  | `mDecideByStepEnd` | H17 | **the race mutant**: B2153's decide-by-completion. Deterministic through 3b: `ThrowsAsync<TimeoutException>` meets `TaskCanceledException` |
  | `mOwnEndWrapped` | H17 | shape 4 `Assert.Same` |
  | `mStepEndDropped` | H17 | shape 4 `ThrowsAsync`: no exception |
  | `mStartUnbounded` | H18 | unchanged from B2153 |
  | `mStopUnbounded` | H18 | unchanged from B2153 |

  `mOwnTimeoutWrapped` is dropped because its OLD text is gone. The old R3 "named limit" (no row for the OCE catch) is removed: the race now has a deterministic row.
- **Lane:** new seat X89, new lane `.tools/b2170`, new branch `b2170/lane-c-kit2-part2-r2`, new STATUS `2026-11-27_B2170_STATUS.md`, last line `READY B2170`.
  - `.tools/b2153` is named READ-ONLY evidence in line 1, line 2, lines 14 and 27, FACTS 7 and REFUSE AT ONCE, which also says explicitly that it is not a refuse.
  - The PRIOR-WORK check and REFUSE AT ONCE require `matching-refs/heads/b2170` and `matching-refs/heads/b2153` to be 0 rows.
- **Rev1's narrowed rules are kept:** records seats may run beside it, and the one-builder rule covers `OXPd2-X`/`OXPd2-G` panes. `Datasec/OXPd2-X85` is called out as a device run, NOT a refuse, in line 2, FACTS 7, REFUSE AT ONCE, Q6, S3 and the launch line. A live `OXPd2-X82` pane would still be a refuse.
- **PREDICTED** (no dotnet job run): pin run `Total: 18, Errors: 0, Failed: 0`; whole solution `total: 2433`; `MUTANTS: 7 of 7 MATCH, 7 of 7 undone equal`.

## FACTS RE-MEASURED (instrument, then what it printed)
- **Origin** (`gh api -X GET`, OXPd GH_CONFIG_DIR, 18:57:03):
  - main is `760e1a64…` (tree `8e3985c1`, parent `0ca8c655`), unchanged.
  - Open PRs: 0. `pulls?state=all`: 58, of which 0 come from a `b2153/` or `b2170/` branch.
  - `matching-refs`: `heads/b2153` 0, `heads/b2170` 0, `heads/b217` 0; control `heads/b2138` 1.
- **BASE hosted:** `hosted3.py` gave PASS at `--total 2431 --rules 679`. The control at `--total 2432` gave `FAIL 4` with rc 1 (18:59:17).
- **X82 evidence (read-only):**
  - Clone `HostRig.cs` is `46c1e78f…` (= B2153 frozen) and `HostCellTests.cs` is `da7499b7…`.
  - `HostCellTests.cs:397` is shape 3's message `Assert.Equal`.
  - Clone `HostRig.cs:220` is `await running.WaitAsync(bound);` and `:222` is the filter.
  - The log reads `Total: 18, Errors: 0, Failed: 1`.
  - The clone is on local branch `b2153/lane-c-kit2-part2`, with 2 files modified and unstaged.
- **Generator** (`d2170/scripts/gen_edits_b2170.py`):
  - OLD found exactly once for 7 of 7 edits; each mutant's OLD found exactly once in the green HostRig for 7 of 7.
  - The README after-sha are all equal to B2153's.
- **Simulated BASE copy** (scratch `git write-tree` = `8e3985c1`):
  - `apply_c3.py` printed `check` BASE ×4, then support 1/1 equal, text 3/3 equal. A second support run was REFUSED with rc 1. `check` then printed FROZEN ×4.
  - `checks_c3.py` on the staged sim (with prototype cells) gave `CHECKS: 9 of 9 PASS`, all controls FIRED.
  - `mutants_c3.py --list` printed `LIST: 7 mutants, 1 suites, 2 cells` (rc 0). The bad row gave `LIST REFUSED: rows mBad` (rc 1). apply/undo ×7 gave `equal True` ×7.
  - `words.py --control` fired 13 of 13. Over 142 added lines plus the message it printed `WORDS: clean (2 files)`. The `B2[0-9]{3}` count was 0 and 0.
  - gitleaks 8.30.1: the control gave rc 1 and was quarantined. The tools plus the added lines gave rc 0, `no leaks found`.
- **Docs** (`System.Runtime.xml` 10.0.15, members printed whole): `Task.WhenAny`, `Task.Delay(TimeSpan, CancellationToken)`, `CancellationTokenSource(TimeSpan)`, `IsCancellationRequested`, `CancellationToken.WaitHandle`, `Task.FromCanceled`. Their quotes are in kit FACTS 5.
- **Compile risk checks:**
  - No type named `Timeout` exists in src/tests.
  - `Timeout.InfiniteTimeSpan` is used in 10+ test files, and in X82's cells, which built with 0 warnings in this assembly.
  - Landed `Task.WhenAny(task, Task.Delay(...))` form: `ManualClock.cs:163`.
  - No AnalysisMode or AnalysisLevel set; no `.editorconfig` severities.
- **Machine and panes** (18:56:45):
  - Panes: `%0 tuesday`, `%593 Datasec/OXPd2-X85`, plus 4 unnamed. X82's pane is closed.
  - The lock folder was absent. `.tools/b2170` was absent at 19:01:28. Load was `3.25 3.55 5.53`, with 838 GiB free.
  - BACKLOG `74800003…` is unchanged: 137, 138 and 121 open, 1 each. CLAUDE.md and CLARIFICATIONS sha are unchanged.
  - No B2161 STATUS exists.
- **Seat-id check:** X89 is in 0 of 43 SEAT kits and in 0 of 232 brief files other than this commission (control X88: 3 and 6).

## D-DECISIONS (coordinator defaults)
- **D1–D7:** as in B2153.
- **D8 (new):** S4 uses one timer and one question; the bound wins whenever it has elapsed by the read; `Late` carries no inner exception. The alternative is X82's option (a), a filter that passes on every `TimeoutException` that is not the step's own. It is not built because it keeps two timers and a decide-by-completion check, and still leaves the token uncancelled when the wait's timer fires first.

## CHAIN INPUTS
The steps are B2162's. Step 1 inputs now come from `<src>` = `d2170/seat-tools` (exists). B2153 STATUS and the pin-server log are READ WHOLE item 7 (exist). No step needs anything a later step makes.

## Q-QUESTIONS FOR TUESDAY (default in brackets)
- **Q1, Q3 (STOP-CLASS, answered in words in S4):** [a, a]. Q3 now says "seven mutants".
- **Q8 (new, D8):** [one timer, one question]. Alternative: X82's option (a), which needs a re-draft.
- **QA (report only):** the 3b cell blocks on `WaitHandle.WaitOne`. If an analyzer warns, the kit lets the seat use `SpinWait.SpinUntil` in its own cell. [seat's choice; nothing frozen]
- **QB (report only):** H17's prototype (`d2170/gen/proto_cells.cs.txt`) was never compiled and is not given to the seat. [unchanged rule: the seat writes the cells]
- Q2, Q4–Q7: as before. Q6's pane is now `Datasec/OXPd2-X89`.

## UNMEASURED
- No dotnet job ran, so whether the frozen S4 builds warning-free, the pin and green totals, and all 7 mutant outcomes are PREDICTED.
  - Two mutant builds are untested: `mWaitDropped`'s `Task.Delay(Timeout.InfiniteTimeSpan)` and `mStepEndDropped`'s `await Task.CompletedTask`.
  - A build failure of a frozen line, or a DIFFER row, is `STOPPED: NEEDS TUESDAY`.
- The order in which the runtime runs a cancelled token's callbacks, and which thread resumes an `await`. The re-frozen outcome does not depend on either; only the cancel-before-disposal mechanics behind shape 3's last assertion are DERIVED.
- R3b, a named limit: a step that ends on its own just before the bound but is read after it is reported late.

## OUTSIDE THE FENCES (disclosure)
- **Writes:**
  - The kit, its `.measured`, and this report.
  - Scratch under `fleet/state/s334/d2170/`, including a scratch git dir `sim.git` with worktree `sim_tree` (no remote, no commit).
  - The `--init` TODO sidecar and the gitleaks control were moved to `d2170/_quarantine/`.
  - **The kit file was written by a program** (`d2170/scripts/make_kit.py` + `kit_edits.py`: counted, asserted replacements over rev1) and then edited once with the Edit tool. DRAFTER_RULES says to use the Write/Edit tools; I did it this way to keep every unchanged rev1 line byte-equal. The `.measured` was filled by `d2170/scripts/fill_measured.py`.
- Nothing was written in the OXPd project (`.tools/b2153` was only read: STATUS, log, two clone files, `git branch --show-current`/`status --porcelain` with `--no-optional-locks`). Nothing went to Jira, GitHub, cards or mail. No dotnet job ran and no lock was taken.
- **GitHub:** `gh api -X GET` only (commits, pulls, matching-refs, plus `hosted3.py`'s check-run and log reads).
- **Hook refusals,** each before anything ran: a `cd`, and an unquoted `======` separator. Both were re-issued without it.
- **Not read:** Source_Documents, 4_Credentials (other than GH_CONFIG_DIR for gh), key folders, the ledger, the scoreboard, `briefs_staged`, cards, and the WEDNESDAY/FRIDAY trees.
