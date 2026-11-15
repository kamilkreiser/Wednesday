STARTABLE: YES (after Tuesday's stamp; five questions, each with a default; Q-1 and Q-2 shape the ending the seat may reach)

# B1605 drafter report: HPSM-POC lane H-2, SQL Server start-up timing (HPSMPOC-482, HPSMPOC-470 point 4), seat H172

Drafted 2026-11-16 from 08:05 to 08:20 AEDT (`date` printed 08:05:35, 08:06:03, 08:09:18, 08:12:07, 08:17:12, 08:19:36).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1605_SEAT-H172_hpsmpoc-lane-h2-sqlserver-startup-flake.md` (232 lines).
- Sidecar: `...startup-flake.md.measured`, 95 lines (77 stamp_check claims plus S01-S18). `stamp_check.py <kit>` exits 0.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s281/d1605/` (Jira dumps, hosted job logs, the sha-pinned source tree, the census files, `fill.py`).
- The drafter had no docker and no SQL Server and ran no test. Every number about a run of the test code is the seat's to take.

## BLUF
- **Pickup check first.** No HELD, DROPPED or needs-ruling line covers 482 or 470 point 4 (grep over the pickup and both daily notes; lines read: pickup 283, 361, 565; daily 11-15 line 37, 46; daily 11-16 line 40). HPSMPOC-480/481 stay out per Q1; 470 points 1 (built, #319), 3 (lane H-3), 2 and 5 (layout calls) are not in the kit.
- **The two tickets are three failure shapes, not two.**
  1. **Sighting 1 (482): `Only_a_first_login_that_timed_out_is_retried`, line 788.** The stack holds no product frame (0 product-class hits in log lines 330-337; MEASURED from hosted job 132569731977). The first `waiting.OpenAsync()` of a `MaxPoolSize = 1` pool, with the only connection held, did not throw. The output shows it was the FIRST loop pass (`en-US`), because the `pool wait (` line is absent (0) while three control lines are present (1 each). No other test calls `SqlConnection.ClearAllPools` (1 hit, inside this very test, after the failing line; 3 SQLite hits are the control). So: not a product defect, and not cross-test pool pollution. Mechanism UNMEASURED.
  2. **Sighting 2 (482 comment, B1585 gate): which test is UNMEASURED.** The quoted sentence is warning 3213's text, which three tests of the class print when they fail. The gate's logs were not found.
  3. **Point 4 (470): two tests failed in the same second (`00:01:57.09` and `.11`) on different GUID databases**, in `AcquireDatabaseLock` through `Migrator.Migrate`, through a test factory's `HostStartRetry.Run`. The error is a client command timeout (258), and the retry helper accepts only SQL Server 1223 (`HostStartRetry.cs:39`), so this shape is not retried by design. A server- or runner-wide stall is the reading that fits; UNMEASURED.
- **Base rate (MEASURED census).** Workflow `ci`, runs created from 2026-11-09, every attempt, `api on SQL Server (api-assessment)`: 87 attempts = 78 success + 8 failure + 1 cancelled. Of the 8: 1 sighting 1, 1 the point-4 pair, 3 ForwardedProof, 3 other tests on 11-10. Each H-2 shape is therefore **1 in 87**. A seat's 0-of-30 base run is the expected result, so the kit makes "not reproducible, nothing built" an allowed ending (`NO-BUILD B1605: ...`) and makes the build conditional on a named mechanism plus a red-first forcing test.
- **Build is conditional.** Property first (a mechanism in this repository's test code, a deterministic forcing test red on base, no bound shortened, no retry, skip, wait or delay), then refused shapes. `HostStartRetry.cs` is NOT owned (byte-for-byte pair with the Feedback tests' copy; widening it is a retry): STOP `NEEDS-SHARED`.
- **Model and gate.** Sonnet builder (`model-routing.md:85` row L6, "Test-only pin", Sonnet = 1st fallback; the commission names Sonnet), G2 on Opus (`:109`). `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes. Ports 10180-10189, seat id H172, containers `b1605-mssql` and `b1605-azurite`.

## Facts re-measured with instruments
- **Main** `678a1153d28be006a088a3b1fba8f5aab52e8d0e` (`gh api -X GET branches/main` at 08:06, again in the sidecar at 08:19:16; `git/ref/heads/main` equal). Open PRs 0. `matching-refs/heads/b1605` length 0. The project checkout cannot see this sha (`cat-file -t` prints `fatal: Not a valid object name`), so the seat clones by URL (as B1599 did).
- **Tickets.** HPSMPOC-482 (Backlog, Low; 1 comment) and HPSMPOC-470 (Backlog, Medium; 1 comment) read with a GET-only helper (`jget.py` in scratch; the token is read in-process and never printed). HPSMPOC-99999 returned 404 (control).
- **Source pointers** at `678a1153` printed by `awk NR==n` over the raw files (S02, S05, S08, S11, S14): the class at :522, the test at :711, the helper at :771, the pool half :775-:797, `held` at :780, the failing assertion at :788, `ClearAllPools` at :833, the three 3213-printing assertions at :634, :667, :698, `HostStartRetry.cs:39`, `AssessmentModule.cs:182` and `:185`, `ci.yml` :184, :205, :252, :303, :314.
- **Hosted logs** (`gh api -X GET --allow-escape-sequences .../actions/jobs/<id>/logs`): jobs 132569731977 (sighting 1), 130383313163 (point 4), plus 132858498635, 132787210932, 132861839652, 129673026941, 129641315238, 129588586947 for the census. The 11-11 failed run also printed `host starts retried after a lost migrations lock: 2` (the 1223 retry fired in that very run on other databases).
- **Product reading (DERIVED, S11):** `Migrate()` runs only `if (options.MigrateOnStartup)` (`AssessmentModule.cs:182`); the three hosts the slow-login class starts write that setting `false` (:629, :662, :693). Whether any live host sets it true is UNMEASURED and fenced.
- **Ports 10180-10189:** `lsof` 0 rows (unfiltered 12); the 50 non-`.pre-` SEAT kits of 15 and 16 Nov gave 0 for `1018[0-9]` (control `1017[0-9]` over B1599: 4); no HPSM-POC pane.
- **Toolchain:** `DOTNET_ROOT=<project>/.tools/dotnet-10.0.404` first on PATH printed `10.0.404` at 08:12 (S16). Disk 1157 GiB available. load1 8.00 at 08:12.
- **Template.** Shape copied from the B1599 kit; its STATUS "FOR TUESDAY" imprecisions were applied: clone by URL (checkout key path), the landing line with literal `<PR-NUMBER>`, and C# CodeQL "cannot run on this arm64 machine" carried as a kit warning (RELAYED, not re-measured).

## Step input table (MEASURED LITERALS rule 4)

| Step | Inputs | Produced by |
|---|---|---|
| 0 | stamped kit, deploy key, project git config, toolchain `.tools/dotnet-10.0.404`, docker | exists at BASE / Tuesday's stamp |
| 1 | origin reads, the clones | Step 0 |
| 2 | `mut` clone, restore, both containers | Step 0 |
| 3 | `mut` copy `mut-diag`, Step 2's runs, the CI logs named in the kit | Step 0, Step 2; logs on hosted CI |
| 4 | Steps 2 and 3 results | Steps 2-3 |
| 5 | `head` clone, the Step-4 verdicts | Step 0, Step 4 |
| 6 | the Step-5 diff, name lists (`CLAUDE.md`, `JIRA.md`, the gate-verifier ban list) | Step 5; project files at BASE |
| 7 | runs.tsv, diagnosis, evidence | Steps 2-6 |

## D-decisions (the drafter's)
- **D1 Diagnosis before build, with an explicit no-build ending.** The commission says "diagnose test defect vs product first, as B1599 did". B1599's cause was found by the drafter. Here the cause is not findable by reading: 1 in 87 attempts, and no local SQL Server. So the kit's Step 3-4 is a measured diagnosis ladder with a control per rung (D-1's `MaxPoolSize = 2` control must always succeed), and Step 4 forces an explicit verdict per item.
- **D2 Three items, not two.** The ticket's two sightings are different tests of one class (or the same one); the kit treats sighting 2 as its own item, "which test" first.
- **D3 No synthetic load.** The machine is shared; the kit forbids a CPU burner and allows only limits on the seat's own processes (processor count, container CPU). The exact knobs are written UNMEASURED.
- **D4 `HostStartRetry.cs` not owned.** Widening it is a retry (commission: no retry) and it has a byte-for-byte pair in the Feedback tests.
- **D5 New file named by property, not by name.** At most one new file under `Assessment/`, after Step 4 names a TEST DEFECT; `HostedDemoStartTimingTests.cs` is absent from the 1845-path tree (S18), as an example only.
- **D6 Jira comments drafted by the seat, posted by Tuesday's records pass.** `jira-comments.txt` in the evidence folder; the seat reads and writes no Jira.

## Q-questions for Tuesday (each with a default)
- **Q-1 Is `NO-BUILD` an acceptable READY?** The expected ending is "not reproducible, nothing built, two comments for the records pass". **Default: yes** (the ticket itself says "not reproduced; the cause is not established"; SWEEP-0640 says "not reproducible is an allowed ending and is a comment, not a build").
- **Q-2 May the seat add a diagnostic-only change** (more text on the failing assertion, so the next hosted red names its cause) if no mechanism is found? That changes no bound and adds no wait, but it is a build the commission did not name. **Default: no** (the kit builds only a proved TEST DEFECT). Alternative: allow it as a G3-style one-line change after Tuesday's word.
- **Q-3 Builder model.** **Default: Sonnet** (row L6's Sonnet cell, as commissioned). Raise to Opus only if Tuesday reads a SqlClient-pool diagnosis as decision-shaped.
- **Q-4 Gate.** **Default: G2 on Opus** (commission). It applies only if a branch is pushed; a `NO-BUILD` needs no gate, only Tuesday's read of `diagnosis.md`.
- **Q-5 Window.** **Default: one window, READY target 300 minutes after Step 0.** The whole-part runs (5 plus the constrained runs) dominate; their local wall time is UNMEASURED (hosted: 15 m 48 s to 20 m 58 s for that shard, from the census logs).

## UNMEASURED
- The mechanism of sighting 1 (why a second open of a held `MaxPoolSize = 1` pool succeeds). Candidates are not named in the kit, to avoid anchoring the seat.
- Which test failed in the B1585 gate's whole run.
- The cause of the same-second pair in point 4, and whether any live host sets `MigrateOnStartup` true.
- The local wall time of the `api-assessment` part and of the class alone; the local base failure rate.
- The knob names for limiting the test process and the container to one processor (confirm in the tools' help).
- Whether `bash infra/scripts/validate.sh` runs here (B1585's gate printed rc 127 at main and at the merge; RELAYED).
- The three other 11-10 failures (`ActionPlan*`, `B215DemoAliasPdfTests`, `B223DemoNameCheckTests`): named from the logs, causes not read.

## Outside-the-fences disclosure
- **Source tree extracted.** The drafter downloaded the sha-pinned tarball of origin main with `gh api -X GET repos/datasecau/HPSM-POC/tarball/<sha>` (read-only, under the project's own `GH_CONFIG_DIR`) into `d1605/dl/` and extracted it into `d1605/src/` (scratch; an untrusted tree, never executed, no script run from inside it). It also fetched three raw files by `gh api` (`contents/...?ref=<sha>`) to `d1605/`.
- **Hosted logs and run lists.** `gh api -X GET` of 8 job logs (about 0.1 MB each) and of the run and job lists for the census (75 runs, 173 job rows). No hosted site, UAT or demo host was touched.
- **Jira.** GET only, through a script in scratch that reads the project `.env` in-process: HPSMPOC-482, HPSMPOC-470 and HPSMPOC-99999 (404 control). No token printed, no write.
- **Reads.** The pickup, the daily notes of 11-15 and 11-16 (grep for the keys), the B1599 kit, report, sidecar and the B1599 STATUS headings, `2026-11-16_B1585_verify/VERDICT.md` and `pr-body.txt`, `model-routing.md` lines, `models_latest.json:23`, `brief_seat.sh:31`. The B1585 lane's `.tools/b1585` and the s280 state folder were searched for the failure text with a recursive grep (it matched source files only; the search was slow and moved to the background once).
- **Not done.** No docker, az, ssh, mail, board, Artifact, `decision_queue.sh`, or ledger read; no `cd`; no clone, fetch, checkout or ref write in the project repo; the project checkout was read with `cat-file -t` only.
- **A hook refused one command** (an `rm -f` of a non-existent temp name); nothing was deleted. The sidecar skeleton from the first `--init` was moved to `d1605/measured.init.bak` and regenerated after two kit edits.

DRAFTED B1605: kit 232 lines, sidecar rc 0, questions 5
