STARTABLE: YES

# B2153 DRAFTER REPORT: OXPd 2, lane OX-C kit 2 PART 2 (owed 137 and 121; 138 named and left), seat X82

Drafted 2026-11-27 by an in-session read-only drafter (Opus) for Tuesday s333 (lane C2 of commission B2154, the "B2153 (lane C2)" section). First `date`: `Fri 27 Nov 2026 16:58:28 AEDT`; the sidecar's first line carries the write clock (17:18:59). Kit: `tuesday/briefs/2026-11-27_B2153_SEAT-X82_oxpd2-lane-c-kit2-part2.md` (232 lines), sidecar `.measured` (`stamp_check.py` exit 0: "155 claims, 155 measured, 0 not measured"). Scratch: `fleet/state/s333/d2153/` (the seat's tools are in its `seat-tools/`).

**STARTABLE means: the kit is complete and stamp-checked; its LAUNCH waits on things outside it** (in its REFUSE AT ONCE and Stamp S2/S3): the stamp, and the records seat of pull request 58 (kit B2146, seat R339: drafted, NOT yet stamped or launched at 17:11) ending READY. One OXPd seat at a time, so it is not launchable this minute.

## BLUF
- **137 (Q1 default a):** the Server tests' `HostRig` gets `BoundedAsync(step, bound, what)`. The step gets a token that is cancelled at the bound, and `Task.WaitAsync(bound)` ends the wait at the bound even if the step ignores that token. If the step is still running at the bound, or ends because of that token, the result is a `TimeoutException`: "the host's <what> did not end within <s> s". Any other way the step ends comes through unchanged. `StartAsync` runs its start step `"start"` through it, and `DisposeAsync` runs stop plus disposal as one step `"stop"`. Each gets 60 s. All 13 host-starting landed cells are bounded and none of their lines change. To make the bound testable without a hang there are two internal test seams, `beforeStart` (an optional parameter) and `BeforeStop` (a property), plus a settable `StepBound`. No product (`src/**/*.cs`) file changes.
- **Why this form:** it is the owed list's first named form and the commission's wording. Owed 137's relayed Symptom says "no inet socket open", so no request was in flight. The wait was therefore in a start or a stop/disposal (DERIVED; which one is UNMEASURED). The red names the step, which is the "then a managed stack read" half of 137. The alternative is xunit's `[Fact(Timeout=...)]` on the 13 cells, using the landed form `HangGuardMilliseconds = 30_000`.
- **Cells (seat-written):** H17 tests the helper in 6 shapes. H18 tests the start and stop uses through the seams, with a control that the default bound is 60 s and `/health` answers. Every wait is under an outer `WaitAsync(20 s, Ct)`, so a mutant that removes a bound fails as an assertion and cannot hang the run.
- **5 frozen mutants:** `mWaitDropped` (H17, H18), `mTokenNeverCancelled` (H17), `mOwnTimeoutWrapped` (H17), `mStartUnbounded` and `mStopUnbounded` (H18: the bound is made `TimeSpan.FromHours(1)`). The `OperationCanceledException` catch has no mutant row: the token and the wait share one bound and which fires first is UNMEASURED. That is a named limit (R3).
- **121 (README-line option, the sweep's):** one Limits bullet each in the Jobs transport, OXPd 1.x client and Lab READMEs. Each says the handler sets no `CertificateChainPolicy`, so nothing there turns certificate downloads off, and contrasts this with the device token client. A fetch during the handshake is UNMEASURED "on every platform". The Lab line names all three handlers the tool uses (`DeviceChannel`, the transport for `print`, `Oxpd1Client`). `checks_c3.py` check 8 proves what each line says, in the staged tree.
- **PREDICTED:** Server exe `Total: 18` (BASE 16, DERIVED); whole solution `total: 2433` (BASE 2431 MEASURED by `hosted3.py` PASS; 2432 control FAIL 4); `RULES: clean (679 files)`.

## FACTS RE-MEASURED (instrument, then what it printed)
- Origin (`gh api -X GET`, OXPd GH_CONFIG_DIR, 16:58:57): main `760e1a644ce9...` (tree `8e3985c1`, parent `0ca8c655`), PR 58 merged, open 0; `matching-refs/heads/b215` 0 rows, and `b2153` 0 rows (control `b2138` 1).
- BASE tree: tarball by `gh api -X GET`, 679 files, scratch `git write-tree` = `8e3985c1` (equal).
- BASE hosted: `hosted3.py 760e1a64 --total 2431 --rules 679 --skipped-linux 4 --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15` gave PASS. The control `--total 2432` gave `FAIL 4` rc 1.
- BACKLOG.md `74800003...` (1212 lines): lines STARTING WITH `137. - [ ] `, `138. - [ ] `, `121. - [ ] `: 1 each. Control `122. - [x] `: 1.
- Frozen edits: each OLD occurs once (7 of 7). `apply_c3.py` on a copy of BASE: support 1 of 1 files equal, text 3 of 3 files equal. A second `support` apply was refused (rc 1). `check` printed BASE ×4 before and FROZEN ×4 after.
- `checks_c3.py`: on BASE's index `CHECKS: 5 of 9 PASS` (control FIRED on all 9). On the simulated staged tree (frozen edits plus prototype cells) `CHECKS: 9 of 9 PASS`.
- `mutants_c3.py --list` printed `LIST: 5 mutants, 1 suites, 2 cells` rc 0. A bad row under the Lab gave rc 1. `apply`/`undo` of all five on the simulated green files: `equal True` ×5.
- `words.py --control` fired 13 of 13. Over the 132 simulated added lines and the commit message: `WORDS: clean (2 files)`. `B2[0-9]{3}` count 0 and 0.
- gitleaks 8.30.1: control rc 1 (quarantined). The 11 tools plus the added lines: rc 0, `no leaks found`.
- Documents (project-local, read by program): `System.Runtime.xml` 10.0.15 for `Task.WaitAsync(TimeSpan)` ("faulted with a TimeoutException") and `CancellationTokenSource(TimeSpan)`. `xunit.v3.core.xml` 4.0.3: Timeout is in ms and is "only reliable" with the Conservative parallel algorithm, which is the default.
- PRIOR-WORK control found 2 lines for `await app.StartAsync();` across `tests` (one is Oxpd1 `StubDevice.cs`), so the kit scopes it to `tests/Datasec.Suite.Server.Tests`.
- `"health"` appears on 4 lines of HostCellTests.cs. The 13 host-starting cells were counted with `grep -c` (13).
- Seat id X82: 0 of 200 non-`.pre-` SEAT kits of 2026-11-2x (control X81: 4). Load at 17:11 was `1.14 1.41 1.33`. The lock folder was absent. Panes: `tuesday` plus two unnamed. `.tools/b2153` absent.

## D-DECISIONS (all coordinator defaults)
- **D1:** the start/stop bound goes in HostRig, not xunit Timeout.
- **D2:** the edits and mutants are frozen; the cells are the seat's.
- **D3:** stop plus disposal is one bounded step.
- **D4:** the bound is 60 s.
- **D5:** 121 gets one README bullet per module, with the device token client contrast and "UNMEASURED on every platform".
- **D6:** the Lab line names all three handlers.
- **D7:** new cells only; no early return.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS): the form of 137's bound.** Default **a:** the HostRig `BoundedAsync` bound on start and stop. Alternative b: xunit `Timeout` on the 13 cells (13 landed lines change). Alternative c: both.
- **Q2: owed 138.** Default: NOT a precondition. This kit's cells and mutants cannot hang a run (outer 20 s waits), so its orphan risk is only 137's landed hang, which the interim pid rule already covers. 138 is a separate tooling commission in Tuesday's tree that can run NOW in parallel: it needs no OXPd lock and no dotnet job, only a process-group test with a sleeping child. If it lands first, Stamp S8 names its sha256. Alternative: hold this kit for it (one more serial step).
- **Q3 (STOP-CLASS): who writes what.** Default **a:** edits and mutants frozen, cells the seat's.
- **Q4:** the README wording. Default: with the contrast clause. Alternative: without it.
- **Q5:** the bound. Default: 60 s. Alternative: 30 s.
- **Q6:** the gate. Default: one G1 gate, Opus, pane `Datasec/OXPd2-X82`, READY Step 0 + 120, push by Step 0 + 100. Alternative: G2.
- **Q7:** a landed cell that reds with the bound's own message. Default: STOP with its log (137 caught). Alternative: go on.

## UNMEASURED (each named in the kit where it is used)
- No dotnet job ran, so every pin, green, total and mutant expectation is PREDICTED, each with the assertion it must break. The OXPd wave lock was never taken.
- That the frozen HostRig code builds warning-free under TreatWarningsAsErrors plus xunit.analyzers is DERIVED: the landed HostRig already calls token-free async methods outside test methods. A build failure of a frozen line is `STOPPED: NEEDS TUESDAY`.
- What WebApplication does with a token cancelled mid-start or mid-stop. The helper does not depend on it.
- Which wait 137's hang was in, and whether the main thread's `Monitor.Wait` was the test's or the runner's. A blocked call that never returns a task is not bounded (R7).
- The prototype cells (`d2153/gen/proto_cells.cs.txt`) were never compiled. They are NOT given to the seat and NOT frozen.

## CHAIN INPUTS
| Step | Inputs |
|---|---|
| 0 | stamp (S2 BASE, S3 R339's READY, S4, S8) |
| 1 | `<src>` (exists), `<repo>` values, origin, BASE run, R339 STATUS, BACKLOG |
| 2 | BASE files + `edits_c3.json` (from Step 1) |
| 3 | group support + cells on the Step-1 clone |
| 4 | pinned tree (from 3) + group text + frozen mutants (from 1) |
| 5 | green tree (from 4) |
| 6 | staged tree (from 5) + checks/words/message/edits (from 1) |
| 7 | commit (7a), origin/main fetch, run_step/hosted3 (from 1) |

## PARTITION
**This kit owns** `tests/Datasec.Suite.Server.Tests/HostRig.cs`, `tests/Datasec.Suite.Server.Tests/HostCellTests.cs`, `src/Datasec.Suite.Jobs.Transport/README.md`, `src/Datasec.Suite.Adapters.Oxpd1/README.md` and `src/Datasec.Suite.Lab/README.md`.

**B2155 (lane OX-D):** the sweep gives it `build/**`, `.github/workflows/ci.yml` and the root `README.md`. None of the five is among those, and none of those is among the five. B2155's kit did not exist when I wrote this, so its own side is for it to state.

**B2146's records files** (outside the repository) share none of the five.

Two of the five READMEs sit in lane A/B modules. The sweep keeps 121's README-line option in OX-C, and no A/B lane is open.

## OUTSIDE THE FENCES (disclosure)
- **Writes:** only the kit, its `.measured`, this report, and scratch under `fleet/state/s333/d2153/`. The scratch includes three scratch git repositories made there: `k3repo` (BASE index), `sim` (the simulated staged tree, with `core.worktree` = `sim_tree`) and none with a remote or a commit. A first sidecar, its TODO skeleton and a first mutant keep folder were moved to `d2153/_quarantine/`. Nothing was written to the OXPd project folder, Jira, GitHub or any card store. No push, no PR, no dotnet job, no lock taken.
- **Project reads,** by path only (no recursive read): `CLAUDE.md`, `BACKLOG.md` (items 121, 137, 138 and in-process counts), `CLARIFICATIONS.md` (sha256 and C-ids), the tail of the B2138/B2134/B2140 STATUS files, `ls` of `Briefs/` and `.tools/` (depth 1), `.tools/dotnet` (`--version`, two reference XML docs), `.tools/nuget-packages/xunit*` (names, two XML docs). I never touched `Source_Documents/` or `4_Credentials/` beyond `GH_CONFIG_DIR` for `gh`.
- **Hook refusals,** each before anything ran: `git -C $D init` (re-issued as `git init <path>`); an unquoted `=====` separator; a stray `rm -rf /dev/null` fragment in one command (nothing deleted; re-issued without it).
- **GitHub:** `gh api -X GET` only (commits, pulls, matching-refs, one tarball, commits?path, and check runs/job logs via `hosted3.py`). No Jira call. No HTTP to any other host. No person, HP or device contacted.
- **Tuesday-tree reads:** DRAFTER_RULES, commission B2154, kits/commissions/reports B2134 and B2138, ANSWER-1, the sweep's OX-C lines, B2146's kit (grep for 121/137/138 and its last line). I did NOT read the ledger, the scoreboard, `fleet/briefs_staged/`, any card store, or any WEDNESDAY/FRIDAY tree.
