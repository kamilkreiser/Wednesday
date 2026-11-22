STARTABLE: YES - kit B1912 (seat X27, test-only, two files under tests/Datasec.Suite.Sessions.Tests/) is prototyped end to end on main bf6b441e: the new F13 cell is RED by its own assertion against arrival-order answers (whole solution failed: 1; 70 of 70 single-cell runs) and GREEN against index-keyed answers (whole solution total: 1579, failed: 0; 420 single-cell runs, 0 failed); stamp_check 159 claims, 159 measured, rc 0. Stamp S4 must answer Q1 (index-keyed answers, the default) in words.

# B1912 drafter report | Datasec / OXPd_2 | the F13 test race on main bf6b441e | drafter Opus, 2026-11-22 19:30 to 19:58 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1912_SEAT-X27_oxpd2-f13-test-race.md` (61658 bytes, 197 lines, ASCII only, 8 unfilled slot lines). Sidecar: the same path plus `.measured` (159 claim lines, a header line with the write clock, a `KIT` line). Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1912/gate/` (9 files). Scratch, logs, the prototype clones and the evidence files: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1912/`.

## BLUF
1. **The precondition holds.** `main` = `bf6b441e30900127487145c3b65b29d8cc9eb5ea`, read at 19:32:14, 19:48:31, 19:54:21 and 19:58:17. There are 0 open pull requests and no `b1912` ref (the control, `b1840`, gives 1). Push run 45001737294 is red on linux alone. Its one failed line names F13, and it printed `total: 1578`, `failed: 1`, `succeeded: 1573`, `skipped: 4`. Windows, secret-scan and rules are all success.
2. **The fix is test-only and FROZEN as two patches.**
   - `1-red-first.patch` (166 lines) makes three changes:
     - It changes the fake refresher: record a call, then count it, inside the lock. It also adds `AnswerOfCall`, `BeforeAnswer` and `Answering`.
     - It moves F13's body into one shared scenario, `LateAnswerAfterTimeOut`.
     - It adds the new cell `F13_the_late_answer_is_never_kept_when_the_timed_out_call_answers_after_the_second_call`.
     - F13's answers are still by ARRIVAL order, so this is the red state.
   - `2-index-keyed.patch` (17 lines) switches the answers to the call's INDEX: the green state.
   - Both patches were applied with `git apply` to a fresh clone and compared with `cmp`, rc 0. A second apply is refused (rc 1, the control).
3. **Red first is deterministic and lives in the repository.**
   - The seam holds call 1 after it is recorded until call 2 has started its answer: the hosted interleaving, on every run.
   - Under arrival order the cell fails with `F13 first answers last after the late answer: the held grant is not the expected one`. That is the hosted message shape: `:22` reached from the scenario's `HoldsGrant`.
   - Under index order it passes.
   - No sleep, no environment variable, no timing.
4. **Q1 (STOP-class) default: index-keyed answers**, not the diagnosis's stricter wait.
   - The stricter wait (`made == 1`) fixes the order by forbidding the legal interleaving "time-out before call 1 reaches its answer".
   - That interleaving would never be tested again, and the held-call cell could not exist, because its wait would run into its 10 s guard.
   - Index-keyed answers make `late` always the timed-out call's answer, in every order. So the property in the test's name is tested more fully.
5. **The other seven cells with the same wait need no change.** Those are F15, F05 hang, F05 late, F08, F09, E07 and L01.
   - Each has ONE refresher call in flight, so no answer can go to the wrong call.
   - The fake's record-then-count change makes four `TokenOfCall` and `RenewalStateOfCall` reads safe without editing them: F05 `:114`, F05 `:130`, F13 `:134` and F13 `:138`.
6. **No file under `src/` changes:** `git diff --quiet bf6b441e -- src ...` gave rc 0, and the control over `tests` gave rc 1. No project file, no lock file (24 lock files hashed before and after the locked restore: equal), no solution line, no workflow change.

## FACTS RE-MEASURED (instrument in brackets)
- **Origin** [`gh api -X GET`, project `GH_CONFIG_DIR`]: private and push both true. `main` is `bf6b441e`, which is pull request 17, lane F, merged 2026-11-22T08:12:41Z. There are 18 branches and 0 open pull requests.
- **Main's push run** [job logs by GET with `--allow-escape-sequences`; `hosted2.py` unchanged]:
  - linux: `total: 1578`, `failed: 1`, `succeeded: 1573`, `skipped: 4`, and no GUARD line (the job stopped at the test step).
  - windows: `total: 1578` twice, `failed: 0`, `succeeded: 1559`, `skipped: 19`, `GUARD: clean (11 files)`.
  - rules: `Ran 111 tests in`, `UNIT-TEST FLOOR: ran 111, floor 111`, `RULES: clean (500 files)`.
  - `hosted2.py ... --total 1578 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111 --hardened-scan` printed `FAIL 6`. All six rows are linux rows; that exact line is in kit FACT 3. Every windows, secret-scan and rules row read OK, and the CodeQL analyses were success.
  - The escape-stripped linux log has 1 line `failed Datasec.` (F13). The control `passed` counts 22.
- **Tree** [`git` at `bf6b441e`, tree `de9817fc`]:
  - `ls-files` gives 500, and the test folder has 13 files.
  - `RefreshBoundCellTests.cs` has 4 indented `[Fact]` (0 at column 1), 1 `[Theory]` and 2 `[InlineData`. After the patches it has 5, 0, 1 and 2.
  - `F13` is named nowhere outside the Sessions test folder (0 lines; the control, `F05` in `RefreshCellTests.cs`, gives 12).
- **ci.yml** [read at `bf6b441e`]: 218 lines, sha256 `c25bdbb2...` (unchanged since AMENDMENT 1 of B1840). The dotnet lines are 40/42/45/46/48 and 70/72/75/76/78. `FLOOR=111` is at line 211 and `repo_rules.py .` at line 218. The push triggers include `b[0-9]*/**`, so the branch `b1912/f13-test-race` runs CI. `concurrency` with `cancel-in-progress` is at lines 14-16.
- **Toolchain** [by PATH]: `.tools/dotnet/dotnet` 10.0.404; gitleaks 8.30.1.
- **Model** [`model-routing.md`]: row L6 (line 85, "Test-only pin") and row C2 (line 92) name a local worker or Sonnet first. G2 (line 109) is "Tier 2: tests-only", and its Opus column reads "1st if the follow-up's mechanism sits on a G1 surface". `<project>/CLAUDE.md:7` puts every agent on this project on the newest Opus. The model id is `claude-opus-5-5` (`models_latest.json:17`). `brief_seat.sh:31` defaults to opus, and `:33` accepts opus, sonnet or fable.
- **Landing rule** [`<project>/CLAUDE.md:55-56`, `:82`]: seats push a branch only; Tuesday lands by SQUASH, `--match-head-commit`, one parent.
- **Machine**: load 4.17 to 5.58 between my jobs; 991 GiB free; 3 tmux panes, none OXPd2; no lock folder before or after my jobs; `.tools/b1912` absent.

## THE PROTOTYPE (every job through the round's `heavy.py` unchanged; lane folder `d1912`; wave lock by `mkdir`; 25 jobs, every lock wait 0; the runner waited for load1 under 7 when it read up to 13.18)
| Label | rc | What it showed |
|---|---|---|
| `restore` / `build-red` | 0 / 0 | the locked restore needed nothing outside the project cache; `0 Warning(s)`, `0 Error(s)` |
| `sessions-red` | 1 | the Sessions assembly `Total: 75, Errors: 0, Failed: 1`, the new cell, the message above |
| `loop-red-new` / `loop-red-old` | 0 | 50 of 50 FAIL (new cell); 50 of 50 pass (old F13 name, same red build) |
| `build-green` / `sessions-green` | 0 / 0 | `Total: 75, Errors: 0, Failed: 0` |
| `loop-green-new` / `loop-green-old` | 0 | 200 of 200 pass each, 41 s each |
| `test-green` | 0 | the whole solution: `total: 1579`, `failed: 0`, `succeeded: 1575`, `skipped: 4` |
| `restore-locked`, `build-chain`, `test-chain`, `publish-linux`, `publish-windows` | 0 | `CI=true`, `--force`: 24 lock files unchanged; `total: 1579`, `failed: 0`; `GUARD: clean (10 files)` and `GUARD: clean (11 files)` (each with the existing `GUARD-WARN` line); unittest `Ran 111 tests`, `OK`; `repo_rules.py` without `--source-documents`: the R5 NOT RUN note and `RULES: clean (500 files)` |
| `build-mCountFirst` / `sessions-mCountFirst` | 0 / 0 | the fake counting before recording: `Total: 75, Errors: 0, Failed: 0`: the NAMED SURVIVOR (D6) |
| `build-after-undo` / `sessions-after-undo` | 0 / 0 | undo by copy, `cmp` 0; green again |
| `gloop-green-new` / `gloop-control` | 0 | the gate copy of `loop.sh`: 20 of 20 pass; a made-up name `runs 3 pass 0 fail 0 other 3` (the selector's control) |
| `build-red2` / `test-red2` / `gloop-red-new` | 0 / 2 / 0 | the whole solution red: `total: 1579`, `failed: 1`, the one `failed` line the new cell, the message counted 1; the gate loop `runs 20 pass 0 fail 20 other 0 seconds 4` |
| `build-green3` | 0 | back to green for the scans |
Scans:
- `gitleaks dir` over the two patched files and both patches under neutral names: `no leaks found`, rc 0. The control, a token built from two halves, gave rc 1 and was quarantined.
- `words.py`: `WORDS: clean` over the 75 added lines plus the commit message, and over the message plus both patches. `--control` printed `CONTROL FIRED: 13 of 13`.
- ASCII check: 0 on both files. The control, a planted U+200B, gave 1.

## D-DECISIONS (Tuesday's defaults; each has a Question)
- **D1 (Q1, STOP-class):** index-keyed answers through `AnswerOfCall`. The reasons are in BLUF 4. The commission asked me to choose "the one that leaves the property the test name states fully tested", and this is that one.
- **D2:** record, then count, inside the one lock of the fake.
- **D3:** the red-first seam (`BeforeAnswer` plus `Answering`) is test code in the repository, with a held-call cell. The proof is the cell, not a scratch diff, as the commission asked.
- **D4:** F13 keeps its name and its message texts (with `cell = "F13"`); its body becomes the shared scenario.
- **D5 (Q2):** ONE commit. The red state is run locally and recorded, never committed, because a pushed red commit would run red hosted jobs and the squash erases it anyway.
- **D6 (Q3):** no cell for the second race. No test can hold a call between the count and the record. `mCountFirst` is a named survivor, MEASURED green.

## Q-QUESTIONS FOR TUESDAY (defaults are already assumed in the kit)
- **Q1 (STOP-class, S4 in words):** index-keyed answers and the held-call cell. The alternative is the stricter wait, which is one line, but it cannot carry the in-repository red proof and it stops testing one legal interleaving.
- **Q2:** one commit, red recorded locally. The alternative is red and green commits on the branch.
- **Q3:** no cell for the record-then-count race (named survivor). The alternative is a non-deterministic stress cell.
- **Q4:** keep F13's name and messages. The alternative is to rename it.
- **Q5:** the level is Opus, by the project's own rule. The routing rows L6 and C2 would put this work on a local worker or Sonnet.
- **Q6:** READY at Step 0 + 120, the push by Step 0 + 90, pane `Datasec/OXPd2-X27`, gate G2 on Opus.
- **The seat name X27 was used before**, by kit B1863 on 2026-11-21 (tolerant reading, landed as pull request 14). No pane holds that name now. The commission names X27; the REFUSE line only counts live panes.

## UNMEASURED
- Every hosted leg of a head of this lane: linux, windows, the neutral scan of a real commit.
- Windows: the scenario is the same code and its waits are on the tests' own clock, but it has not been run there.
- The hosted frequency of the old race. One red push run is known; the diagnosis got 0 of 2500 locally (RELAYED).
- The `--cached` forms of Step 6 (a) and the commit steps: I staged nothing and made no commit. Their unstaged forms are MEASURED.
- The seat's baseline at BASE: PREDICTED `total: 1578`, derived as 1579 minus the one new case.

## CHAIN INPUTS (each produced earlier or present at BASE)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit, the Stamp slots | Tuesday's stamp |
| 1 | `<src>` (9 files, exists); `<repo>`'s local values; the origin; BASE's push run | the drafter's scratch; `<repo>`; GitHub |
| 2 | BASE's two files | Step 1's clone |
| 3 | `1-red-first.patch`, `loop.sh`; the baseline build | Step 1 (tools copy, baseline) |
| 4 | the red tree; `2-index-keyed.patch` | Step 3; Step 1 |
| 5 | the green tree, mutant undone | Step 4 |
| 6 | the staged tree; `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit; `origin/main` | Step 7 (a); the fetch of 7 (b) |

## THE CHECKS I RAN, AND THE CHECKS THAT ARE NEVER RUN
- RAN on my own prototype output, each with a control that fired:
  - the name-status and numstat of the diff (2 M rows; 32 added and 2 removed, 43 added and 16 removed);
  - `diff --quiet` over src and the shared files (rc 0; the control over tests gave rc 1);
  - ASCII (0; control 1);
  - gitleaks (rc 0; control rc 1);
  - words (clean; control 13 of 13);
  - the loop selector (a made-up name gave `other 3`);
  - patch application (`cmp` 0; the re-apply control rc 1);
  - the lock files (24 hashes equal);
  - `repo_rules`, the guard, unittest.
- The scans are the PROJECT'S own: `words.py` from the round's gate, gitleaks with the workflow's options, and `repo_rules.py` from the clone. None is a list of my own.
- NEVER RUN, and marked so in the kit:
  - the `--cached` forms;
  - `run_step.py`'s neutral scan of a real commit;
  - `hosted2.py` on a head of this lane;
  - `clone.py` in seat mode (I copied no identity).

## READING LOAD
The kit is 61658 bytes. Items 2 to 5 add 130732, the six headers 5507, the two patches 9564, and the two files plus `ci.yml` 27064. That is the kit plus about 173 kB, about 58K tokens in all.

## WHAT I DID NOT READ
`Source_Documents/`, the NAS library, any key folder, any sibling project, any decision card (no `decision_queue.sh` call), `fleet/briefs_staged/`, `projects_index/scoreboard.md`, `0_Brain/learnings/_ledger.md`, the files of B1906, B1909 and B1911.

## CORRECTIONS TO THE COMMISSION
- The commission cites `TokenBroker.cs:425-437` for the accept-only-without-error rule. At `bf6b441e`, `:430` is the error branch and `:437` is the `AcceptLocked` call; `:424` clears `state.Refresh`. The kit prints these lines by program.
- "Expected totals ... windows and the PR merge-ref read 1578": MEASURED here for windows and for the linux job as well (`total: 1578`); the merge-ref figure stays RELAYED.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Writes:**
  - this report, the kit and its sidecar, each through a temp file and `os.replace`;
  - everything under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1912/`: `gate/`, `clone/`, `clone2/`, `logs/`, `scratch/`, `evidence/`, `out/`, `_quarantine/`, `dotnet-home/`.
- **Two scratch clones:** both are local clones of the B1908 clone, with the push URL `invalid://no-push`. Their working trees were edited by my programs, and `git apply` was used in `clone2`. No `git add`, no commit, no ref written, nothing fetched from GitHub.
- **The one write in the OXPd_2 project folder:** the shared heavy lock, which `heavy.py` took by `mkdir` 25 times and moved into `d1912/_quarantine/locks/` each time. The project's package cache was read by the restores.
- **GitHub:** `gh api -X GET` only (job logs, runs, refs, pulls).
- **Not done:** no Jira call, no message, no `cd`, no delete. Moved to `_quarantine/`: the first `loop.sh`, the planted controls, the first sidecar skeleton, and one stray stamp_check output I first wrote to `/tmp/claude-501/sc.txt`, outside the scratch folder.
- **Hook refusals:** one Bash call was refused (a `git -C $D/clone2 apply` whose variable path the no-cd hook could not resolve). It was re-issued with the literal path inside TUESDAY.
- **Test runs beside a lock:** no other seat held the OXPd lock during my jobs (every lock wait 0). Load was up to 13.18 while the runner waited.
