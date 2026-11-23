STARTABLE: YES (only with Q1 and Q2 answered "a" in words at the stamp: Q1 the refusals and exit codes of `undo-owed`; Q2 fail closed at exit 10 on any element of the read's result outside HP's record shape)

# B2021 DRAFTER REPORT: lane W2 round 2 (the fix build for gate B2016 FOUND 1 to 4), seat Datasec/OXPd2-X61

Drafter B2021 (Opus, in-session, read-only toward the project and GitHub), 2026-11-24 08:17 to about 09:10 AEDT. Lane B2021 ONLY; nothing of lane B2022 touched. Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2021_SEAT-X61_oxpd2-w2r2.md`, sidecar `.measured` beside it (`stamp_check.py`: 210 claims, 210 measured, rc 0). Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s320/b2021/` (below `<d>`); seat tools `<d>/seat-tools/`. Gate tier G1, round 2 of 2 of lane W2.

## BLUF
- **BASE** is main `b0b26b60a37cf771a2121000ca60f420658e0088` (PR 44 squash, one parent `c5b103ee`, tree `b2a09571`), re-measured by `gh api -X GET` and two draft clones. Its hosted run, read by `hosted3.py`: `HOSTED b0b26b60...: PASS` at `--total 2093 --rules 657` (run 45187062667; linux 2089, windows 2072, guards 14 and 15).
- **What is built** (frozen in `1-red.diff` + `2-fix.diff`; five paths, all M, no file added):
  - **FOUND 1 (Major):** `undo-owed` now
    - refuses a folder that holds `undo-list.tsv` itself, with exit 2 and "nothing was read";
    - prints `no undo list was read` and exits 11 when no run folder directly inside holds a list;
    - names an empty or header-only list as unreadable (exit 11);
    - says `nothing is owed` (exit 0) only when at least one list was read, every list holds an entry line, every line was read and nothing is owed.
  - **FOUND 2:** the read before a register visits every child element of the result. Any element that is not `AuthenticationAgentRecord` in the result's namespace, or a record without exactly one `id`, ends the run with exit 10 and nothing written.
  - **FOUND 3:** `--agent-name` is refused (exit 2) before any folder or connection when a character fails `XmlConvert.IsXmlChar` and is not half of a well-formed surrogate pair.
  - **FOUND 4:** the printed undo now carries `--password-name`, the pins, `--soap-port`, `--addressing` and `--timeout-seconds`, always.
- **Infos of gate B2016, each in or out:**
  - **5 IN:** cell V13 (a device holding another agent only is written to) plus mutant `mAnyRecordRefuses`.
  - **6 IN, README text only:** ties are ordered by folder name, and the order follows the recorded clock.
  - **7 IN, README text only:** an exception or cancellation after the send prints no undo; the `Pending` row stays owed.
  - **8 IN as an UNMEASURED README Limits line; code OUT:** .NET's re-send on a pooled connection is the landed client's behaviour, and the adapter does not change.
  - **9 IN as README text; code OUT:** the host is compared as typed, which is the safe side.
- **Cells:** 6 new cells (19 cases), appended to the landed `Oxpd1WriteTests`: V12 to V16 and U05. The stub gains one plan property, `ExtraInResult`. No landed cell, assertion or helper changes (numstat: 0 deleted lines in both test files).
- **Measured in a fresh `<d>/clone3` with the frozen patches:**
  - RED on BASE itself (tests only): the Lab executable `Total: 187, Errors: 0, Failed: 16`, each red by `Assert.Equal() Failure` (16 of 16).
    - V14's rows read `Expected: 2`, `Actual: -1`: on BASE the run threw. The cell catches it with `Record.ExceptionAsync`, so the red is an assertion, not an exception.
    - Green on BASE (pins, made red by mutants): V13, V15 and U05's control row.
  - GREEN: `total: 2112`, `failed: 0`, `succeeded: 2108`, `skipped: 4` (2093 + 19).
  - Mutants: `MUTANTS: 11 of 11 MATCH, 11 of 11 undone equal`. After them: rebuild 0/0, the dll later than both mutated sources, and green again at 2112/0.
  - Chain: locks equal 34 of 34; build 0/0; test 2112/0/2108/4; `GUARD: clean (14 files)` and `(15 files)` with no Lab file published; `Ran 111 tests` OK; `RULES: clean (657 files)`; ls-files 657.
  - Checks and scans: `checks_w2r2.py` `CHECKS: 8 of 8 PASS`; `WORDS: clean (2 files)`; `B2[0-9]{3}` 0 and 0 (control: the kit has 35 lines); gitleaks control rc 1, the clone and 10 neutral files rc 0.
- **PREDICTED hosted:** `--total 2112 --rules 657` (linux succeeded 2108, windows 2091).
- **Partition from B2022:** this lane writes five repository paths under `src/Datasec.Suite.Lab/Commands/Oxpd1/` and `tests/Datasec.Suite.Lab.Tests/Oxpd1/`, plus `<project>/.tools/b2021/**` and `<project>/1_Project_Definition/Briefs/2026-11-24_B2021_*`.
  - B2022 writes `CLARIFICATIONS.md` (if owed), `BACKLOG.md` and `5_Project_History/history.md` in the project folder.
  - MEASURED: `git -C <project> rev-parse --show-toplevel` rc 128, so the project folder is not a repository. The repository is `2_Project_Files`.
  - No common path. `checks_w2r2.py` check 1 proves the repository side (exactly five M rows).

## Facts re-measured (instrument)
- Origin `main` = `b0b26b60...` (`gh api -X GET` at 08:17 and 08:38, `<d>/logs/misc.out`). Open pull requests 0. `matching-refs/heads/b2021` 0. Private `true`. `.tools/b2021` absent.
- Toolchain: `dotnet --version` printed `10.0.404`; `gitleaks version` printed `8.30.1`.
- `CLARIFICATIONS.md` (830 lines, sha `cdfb76f2`; the newest entry is C-78). Case-insensitive line counts:
  - undo, undo-owed, nothing is owed, surrogate, namespace, addressing, fail closed, U+FFFE, timeout, session folder and execute: each 0.
  - password-name: 1 (line 750, about what a log record carries; not this subject).
  - Controls: C-63 1, C-78 2, OXPd 150.
- `kam_rulings_today.sh` (4 lines, `Showing 0 of 0`): every subject word 0.
- No product-owner ruling touches this lane. The 08:12 terminal words are RELAYED from the commission (the board helper shows 0 messages today).
- Last real WRITE commands on the Lab paths: kit B2011's seat, `2026-11-23_B2011_STATUS.md`:
  - line 158: `git -C '<clone>' commit -F '<lane>/gate/commit-message.txt'`;
  - line 161: `git -C '<clone>' push origin HEAD:refs/heads/b2011/w2-oxpd1-lab-write`, at 00:06:00.
  - The kit's commands match these token for token, except the branch name `b2021/w2-lab-write-fixes`.
- That seat ran its mutants and its `hosted3.py --wait` as background calls (its DEVIATIONS). The kit now allows that form explicitly.

## D-decisions (all yours as coordinator)
- D1: `undo-owed` refuses a run folder given as the session (exit 2).
- D2: no list read gives exit 11; an empty or header-only list is unreadable.
- D3: fail closed at exit 10 on any element outside the record shape, or a record without exactly one id.
- D4: XML's character rule for the name; surrogate pairs are allowed.
- D5: the undo carries every connection option, defaults included.
- D6: Infos 6 to 9 are README text only.
- D7: the cells are appended to the landed class.
- D8: no new exit code.
- D9: one commit, one push, no pull request.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS): what `undo-owed` does when it read no entry.**
  - a (built): a run folder given → exit 2; no list read → exit 11; an empty or header-only list → unreadable.
  - b: read the given folder's own list as a session of one.
  - c: a new exit code 12.
- **Q2 (STOP-CLASS): a non-schema answer to the read before a register.**
  - a (built): exit 10.
  - b: exit 8.
  - c: search the whole answer for the id (this one is not fail-closed).
- Q3 to Q10 have their defaults as in the kit:
  - Q3: XML's rule for the name.
  - Q4: every option in the undo.
  - Q5: README only for the Infos.
  - Q6: cells appended to the landed class.
  - Q7: no new exit code.
  - Q8: one commit, one push.
  - Q9: Opus, READY by Step 0 + 120, pane X61, gate G1 round 2 of 2, hard stop before the meeting.
  - Q10: either landing order.
- For your stamp:
  - **S7:** the hard stop is before this evening's kick-off; the clock is yours.
  - **The gate:** `<project>/CLAUDE.md:7` says "Fable only where a need for it is flagged first" (C-56). Your reading of the 08:12 word ("Use fable to review") is what lets the G1 gate run on Fable; the kit names the gate "on Fable or Opus by Tuesday's reading".

## UNMEASURED / NEVER RUN
- Both hosted legs for this head.
- H12: a character XML cannot carry in `--agent-service` or `--prompt-page`. The kit names it a limit for the gate's probe.
- H9: content outside the result element (siblings, text, attributes). DERIVED as not read.
- Every device answer. How the M577 answers the records read is still UNMEASURED.
- The seat's own steps: the seat-mode clone, the commit, `run_step.py`'s neutral scan on a commit, the push, the read-back, `hosted3.py` on a head of this lane, and the rebase.

## Disclosure (no fence crossed; the edges)
- **First frozen run discarded.** My first frozen run (`<d>/clone2`) passed red, green and 11 of 11 mutants, but `checks_w2r2.py` check 4 FAILED: the Edit tool had turned three `\u` escapes in the new test file into literal U+FFFE, U+FFFF and an emoji.
  - I replaced them with ASCII escapes in the prototype, which changes the test file only (`Oxpd1WriteTests.cs` sha `8ae5d666...`).
  - I re-cut `1-red.diff`; `2-fix.diff` is unchanged (`cmp` equal).
  - I reran the whole frozen sequence in a fresh `<d>/clone3`. Every number in the kit is from `<d>/clone3`.
  - Old patches and gate copy: `<d>/_quarantine/seat-tools-v1/` and `<d>/_quarantine/gate-v1/`.
- **Partial sidecar quarantined.** A partial sidecar was moved to `<d>/_quarantine/measured-partial` before the full regeneration.
- **Hook refusals:**
  - `pretooluse_no_cd.sh`: once for a `cd`, and once for a `git -C "$D/clone2" apply` whose path the hook did not expand. I re-issued the latter with the literal path inside my own TUESDAY scratch.
  - `pretooluse_zsh_wordsplit.sh`: once for a `=====` separator.
  - `pretooluse_recursive_scope.sh`: once for an unscoped `find` under `fleet/state`. I listed the folder instead.
- **Git use:** draft clones only (push URL `invalid://no-push`), with stagings, applies and mutants in my own scratch. No commit, no ref, no push. GitHub only by `gh api -X GET` under the project's `GH_CONFIG_DIR`.
- **Heavy jobs:** every heavy job went through `heavy.py` and the wave lock: 71 jobs, lock waits 0. Load reached 23.05 from other agents, and the runner waited for it. No other holder's lock was touched.
- **Long programs in the background:** the mutant run, the chain and the clone3 sequence each ran as ONE background program call (the foreground cap).
- **Not touched:** Source_Documents, key folders, the NAS library, credentials files, `Design/`, `Meeting/`. No Jira, printer, Azure or message.
