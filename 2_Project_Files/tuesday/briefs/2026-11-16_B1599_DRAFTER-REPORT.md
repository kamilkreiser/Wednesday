STARTABLE: YES (after Tuesday's stamp; six questions, each with a default that lets it start; Q-1 decides what the TICKET slot says)

# B1599 drafter report: HPSM-POC builder, the ForwardedProofTests intermittent red, seat H171

Drafted 2026-11-16 from 02:05 to 02:29 AEDT (`date` printed 02:05:56, 02:21:34, 02:23:03, 02:26:25, 02:28:42, 02:28:53).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1599_SEAT-H171_hpsmpoc-forwardedproof-race.md` (311 lines).
- Sidecar: `...forwardedproof-race.md.measured`, with 84 claims plus S01-S17. `stamp_check.py <kit>` exits 0.
- Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s280/d1599/`.

## BLUF
- **Root cause.** The test's own watch filter writes its reading AFTER the app's pipeline returns. TestServer's `SendAsync` hands the response back as soon as the 404 body starts. So the test reads a plain field that still holds either nothing, `(False, null)`, or the PREVIOUS request's reading, `(False, "198.51.100.7")`.
- **TEST defect, not a product defect.** No client-address mis-attribution is possible in production from this. The product gate decides per request on that request's own headers, with immutable start-up state. Every wrong value the test saw is either "not yet written" or "the previous request's correct answer".
- **Fix shape** (one test file, no product file):
  - The watch hands each reading over through a `Channel` and the test awaits it. The assertions are unchanged.
  - One deterministic forcing test holds the filter's after-pipeline code until the response is back. It is red-first: 10 of 10 red with base's field read, 10 of 10 green with the handoff.
- **No retry, skip, wait or weakened assertion.** The only time value is a 30 s hang guard on the await (Q-5).
- Main moved during drafting: lane Q's #323 landed as `243400dd`. The blobs of every file this kit touches or points at are identical to `a9e0052f`, so all pointers and run counts hold.
- **Model and gate.** Sonnet builder (`model-routing.md:92`, C2). Gate G2 tests-only (`:109`), on Opus by that row's O55 cell, because the test pins a security control (Q-2, Q-3). Launch with `BRIEF_SEAT_LEVEL=sonnet`.

## Facts re-measured with instruments
- **Main.** At 02:0x, `gh api -X GET branches/main` gave `a9e0052f...` with #323 open. At 02:26 it gave `243400ddbaa6f1bce4dbb37ccf01e51a272b478f`, with #323 closed and merged (merge sha equal). `git ls-remote` from the drafter's own clone, using the project deploy key, gave the same.
  - `rev-list --count a9e0052f..243400dd` gave 1. The diff has 44 files, and 0 under `api/tests/HpsmPoc.Api.Tests/Hosting/` or `api/src/HpsmPoc.Api/Auth/`.
  - Control: the loose pattern `Hosting/|/Auth/|FollowUpKit|Program\.cs` matched 1 path, `api/tests/HpsmPoc.Api.Tests/Auth/UatLabelTests.cs`, which is not this kit's.
  - Blob ids of `ForwardedProofTests.cs`, `ForwardedProofGate.cs`, `Program.cs`, `ci.yml` and `global.json` printed SAME.
- **Open PRs at 02:26: 0** (control: `state=all&per_page=3` gave 323, 322 and 321, all closed). `pulls/99999` gave HTTP 404, and `pulls?state=open` gave HTTP 200. `matching-refs/heads/b1599` gave length 0.
- **Lane N.** `b1585/hpsmpoc-narrative-reedit` = `afb70bc3`, 1 ahead and 0 behind `a9e0052f`, with 18 files and 0 matching `Hosting/|ForwardedProof|ForwardedClient|FollowUpKit`. Lane Q's #323 had 30 files, 0 under `Hosting/`. Both lane kits fence `api/**/Hosting/` (B1597 kit lines 18, 56 and 60 by `grep -n`). Lane N's kit reads `Hosting/DeleteGrantCensusTests.cs` as UNAFFECTED.
- **Hosted CI** (`gh api -X GET --allow-escape-sequences .../actions/jobs/<id>/logs`, run 43724185758 = PR #323):
  - Attempt 1 (job 132842408533) and attempt 2 (job 132848556963) each failed the `api (ASP.NET Core)` job, the default host, not a SQL Server part.
  - Each failure: `Failed: 1, Passed: 2343, Total: 2344` in `HpsmPoc.Api.Tests.dll`, at `ForwardedProofTests.cs:line 165`, `Actual: Tuple (False, "198.51.100.7")`.
  - Attempt 3 was in progress at 02:1x; #323 then landed.
- **Local lane log** `.tools/b1585/logs/s6-mssql-forwarded.log` (read-only) holds 4 reds of the `(False, "198.51.100.7")` shape, and 1 red `Expected: Tuple (False, "198.51.100.7") / Actual: Tuple (False, null)`: the never-written shape, at the first assertion.
- **Drafter's runs** (own clone; dotnet 10.0.404 by path; `-nodeReuse:false`; NuGet from the project cache as a read-only fallback folder, with 0 B added to the drafter's own package folder):

  | Tree | Test | Runs | Result | Load1 |
  |---|---|---|---|---|
  | base | target test alone | 10 | **4 red**: runs 2 and 10 `(False, "198.51.100.7")`, runs 4 and 8 `(False, null)` | 15.95-17.66 |
  | base + 250 ms plant after `await nextMiddleware(context)` (test code only) | target test | 10 | **10 of 10 red**, all `(False, null)` | 16.63-19.53 |
  | channel fix + the same plant | target test | 10 | 10 of 10 green | |
  | channel fix, no plant | target test | 10 | 10 of 10 green | |
  | fix | `Hosting.` group | 2 | 220/220 each | 13.93, 11.01 |
  | base | `Hosting.` group | 2 | 220/220 each: the group rarely shows it, matching Tuesday's 220/220 | |
  | red form: hook + forcing test reading base's field | forcing test | 10 | **10 of 10 red**, `(False, null)`, about 2 s each, no hang | up to 22.71 |
  | green form (the kit's DESIGN) | forcing test | 10 | **10 of 10 green**. `Assert.False(reading.IsCompleted)` held each time: direct proof that `SendAsync` returned before the pipeline finished | |
  | green form | target test | 10 | 10 of 10 green | |
  | green form | whole `ForwardedProofTests` class | 2 | 23/23 each | 18.93 at the last |

  Logs are in `d1599/logs/`, one file per run.
- **Product reading (DERIVED, pointers S09-S12 in the sidecar):**
  - `ForwardedProofGate.cs:12` holds only `ForwardedClientAddress`, a sealed record (`ForwardedClientAddress.cs:32`) with an `init`-only digest (`:53`).
  - `:20-22` decide on the request's own headers.
  - `Program.cs:134/:136` build the gate and the options once.
  - Nothing per-request is shared, so there is no product race. The only shared mutable state is the TEST's `Watch.Seen` field, registered as a singleton `IStartupFilter` (`ForwardedProofTests.cs:260`).
- **Sibling scan.** `/usr/bin/grep -rn -i -E 'await (next|nextMiddleware|following|nxt)\('` over `api/tests` printed 4 lines in 4 files. The other three (`DevelopmentAuthTests.cs:38`, `ImportUtf7Tests.cs:64`, `Hpsmpoc290Tests.cs:458`) write nothing after the await, so no other test has this race shape.
- **Ports 10170-10179.** `lsof` gave 0 rows (unfiltered 18). The scan of 45 non-`.pre-` SEAT kits of 15-16 Nov for `1017[0-9]` gave 0 each (control `992[0-9]` over the B1577 kit gave 2). Panes at 02:23: `%0 tuesday`, `%111 Datasec/NexusAI-N135`, `%1 fleet-monitor` and unnamed panes. No HPSM-POC pane.
- **Seat id.** The highest existing `SEAT-H` in briefs/ is H170, so H171 is free.
- **Identity** (for Tuesday's IDENTITY slot): the project `2_Project_Files` config prints user.name `kamilDatasec` and user.email `88359143+kamilDatasec@users.noreply.github.com`.
- **Checkout key.** The project checkout's `core.sshCommand` points at `/Volumes/Laptop-DEV/.../github_deploy_rw`, so `ls-remote` from it fails. The kit tells the seat to clone by URL with the Datasec_DEV key.

## D-decisions (the drafter's)
- **D1 Channel handoff over `OnStarting`.**
  - Reading in `Response.OnStarting` would also be deterministic: TestServer runs OnStarting before completing `SendAsync`. But it changes the moment of the reading from "after the pipeline" to "when the response starts".
  - The Channel keeps the test's stated meaning ("once the pipeline has read it") and adds a one-reading-per-request check (`Unread == 0`).
- **D2 The forcing test stays in the suite**, so the race cannot come back unseen. Its red-first is measured on the hook with base's field read. The kit also keeps the scratch 250 ms plant as a second, base-only red (Step 2c).
- **D3 Run counts.**
  - As commissioned: the test alone 20x, and the `Hosting.` group plus the `api-assessment` SQL Server part 5x each, at base and head.
  - Added by the drafter: the whole `api` predicate once at head (hosted CI failed THAT job); the forcing test 10x; the class 5x; and `infra` (the hidden-character scan reads every tracked file, DRAFTER_RULES fence 8).
  - A base 0-of-20 is allowed (timing-dependent); the planted base red is required.
- **D4 G2, not G1.** It is a test-only change and the product is untouched. G2's own O55 cell routes it to Opus because the test guards the client-address attribution control.

## Q-questions for Tuesday (each with a default)
- **Q-1 TICKET slot.** Have a records seat file a ticket first, or stamp `none yet`? **Default:** stamp `none yet: an infrastructure defect blocking landings (hosted api job red on #320 and #323 twice), built under the standing words "keep going with the tickets"; a records seat may file it after READY and cite the PR`. The key never enters the commit either way.
- **Q-2 Gate model.** **Default: Opus G2** (`model-routing.md:109`, O55 cell). Alternative: Sonnet G2 (the S55 cell, "1st").
- **Q-3 Builder model.** **Default: Sonnet** (`:92`, C2; the fix is spelled out and prototyped). Raise to Opus only if Tuesday reads the forcing-test hook as design work.
- **Q-4 Keep the forcing test in the suite?** **Default: yes.** Alternative: the proof only in scratch (the plant), with the committed change limited to D1.
- **Q-5 The 30 s hang guard** on `WatchedAsync`. **Default: keep it.** It makes a missing reading fail instead of hanging the run, and never decides a pass. Alternative: no guard (xunit 2.9.3 has no per-test cancellation token here, so a lost write would hang the job until its CI timeout).
- **Q-6 Window.** **Default: one window, READY target 300 min after Step 0.** The 10 SQL Server part runs dominate; their per-run time is UNMEASURED locally.

## Step input table (MEASURED LITERALS rule 4)

| Step | Inputs | Produced by |
|---|---|---|
| 0 | stamped kit, deploy key, project git config, toolchain at `.tools/dotnet-10.0.404` | exists at BASE / Tuesday's stamp |
| 1 | origin reads, clones | Step 0 |
| 2 | `mut` clone, restore; containers | Step 0; started inside 2(d) |
| 3 | `head` clone | Step 0 |
| 4 | Step-3 tree (hook + forcing test), containers | Step 3; Step 2(d) (or restarted by name) |
| 5 | the Step-4 diff, the name lists | Step 4; project files at BASE |
| 6 | Steps 2-5 green | Steps 2-5 |
| 7 | runs.tsv, red.diff, green diff, pushed sha | Steps 2-6 |

## UNMEASURED
- The api-assessment SQL Server part's local wall time.
- The whole-api local wall time (hosted: 14m52s to 16m35s for `HpsmPoc.Api.Tests.dll`).
- The base red rate over 20 runs.
- The TestServer source itself. The early-return behaviour is measured by the forcing test's `IsCompleted == false`, not read from the framework source.
- Whether lane N lands before launch.

## Outside-the-fences disclosure
- **Scratch clone.** The drafter cloned HPSM-POC into `d1599/repo`, using the project deploy key read-only via `GIT_SSH_COMMAND`. It added three local worktrees (`fix`, `proto`, `red`, all local branches `d1599-*`), ran one `git fetch origin main` inside that scratch clone, and made test-only edits there. Nothing was pushed, and no project repo was written.
- **Builds and test runs.** Four `dotnet build`s and 76 test-run invocations (one log file each in `d1599/logs/`) in that scratch clone, with load1 up to 22.71. The drafter did not run `dotnet build-server shutdown` and stopped no process.
- **Reads outside the scratch folder.** Read-only `gh api -X GET` of two Actions job logs, and read-only reads of the b1585 lane logs.
- **Stray file.** One stray write outside the scratch folder: `/tmp/x` (stderr of a `gh api` 404 probe; no secret). It was left in place, not deleted.
- **Kit edits by another hand.** The kit was reformatted on disk between the drafter's writes, by a process other than the drafter. The drafter accepted it, re-derived the sidecar claims from the current file, and `stamp_check` exits 0 on it.
- **Not done.** No Jira, mail, board, az, docker, Artifact or decision_queue use, and no read of `_ledger.md`.

DRAFTED B1599: kit 311 lines, sidecar rc 0, questions 6
