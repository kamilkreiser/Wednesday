STARTABLE: YES

# B1455 drafter report: SEAT-G378, tier-1 QA gate of `b1394/hpsmpoc-api` @ c0a5fa17

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1455_SEAT-G378_hpsmpoc-api-gate.md`. Drafted 04:51-05:00 AEDT 2026-11-10 (clock from `date`).

## BLUF
The branch builds ONE change: HPSMPOC-436, a 422 `narrative.no-findings` in `ReportingEndpoints.cs:186-187`, plus a 2-row test class and one note string in `ContractTests.cs`. Everything else in the builder's ticket list is CLOSED WITH EVIDENCE at main (7 lines, among them 428's retry and 315's audit note), HELD, or follow-up (b) NOT REPRODUCED. So the gate probes 428 and 315 on MAIN's code (unchanged by the branch). The branch's 3 paths overlap 0 paths of main's move and 0 of every other open lane branch. **Neither SQL Server shard can run here:** the project has no script for it, and this seat has no docker grant. The kit says NOT RUN, names the four items that lose their proof, and makes hosted CI on the PR the SQL Server proof. Tier 1 Opus by row G1. Port block 9520-9529.

## FACTS, re-measured with instruments (all at drafting, 04:51-04:56 AEDT)
- Refs, read with `gh api -X GET git/ref/heads/...`: b1394 = c0a5fa17c5580443d2e85e96a4defbe4e6bb3bdf; main = 884fd72b238ec8dc0d566b0e9c18b5362f920a2b; b1393 = d7df877a; b1392/hpsmpoc-web-ui = 121ee236; b1392/hpsmpoc-web-ui-d = aca2290c (it was cut from 884fd72); b1395/hpsmpoc-ci-tooling = 0cdfc74e. The brief's name `b1392-d` is a 404: the real ref is `b1392/hpsmpoc-web-ui-d`, which I found in the branch list.
- Open PRs: only 298 (b1393, at d7df877a). `pulls/99999` rc 1. Control: the closed list printed 297..293.
- Builder STATUS: `tail -n 1` = `READY B1394: c0a5fa17c5580443d2e85e96a4defbe4e6bb3bdf`, and that is the only READY line (`:118`). `## PRIOR WORK` is at `:32`. CLOSED-WITH-EVIDENCE lines: 7. sha256/16 of the file: f2cb6b4be3bca60c.
- Diff (`compare/fa401da9...c0a5fa17`): 1 commit, 3 files, +90 -1, unsigned. Message checks: non-ASCII lines 0 (planted U+200B control counts 1); `B<digits>` 0 (control 1); trailers 1; ticket-key lines 1 (the subject).
- Path overlap by program (`sort | uniq -d`; control: the branch against itself prints 3): main's move 0, b1393 0, b1392 0, b1392-d 0, b1395 0. `api/` paths in each list: main's move 0, b1393 0, b1392 0, b1392-d 0, b1395 1 (`Hpsmpoc178CustomerNameTests.cs`). That file is in the same test project and the same `api-assessment` shard as the new 436 class.
- Migrations: 0 diff paths under `Migrations/` (control: 88 in the tree at 884fd72).
- SQL Server:
  - The tree at 884fd72 (`git/trees?recursive=1`, 1502 blobs) has 6 non-test scripts. Each holds `HPSM_TEST_SQLSERVER` 0 times and `docker` 0 times (control `bash|python|set -` hits 2-7 in each).
  - CI starts SQL Server with `docker run` (`ci.yml:205`) and sets `HPSM_TEST_SQLSERVER` (`:223`).
  - Docker on this machine: `command -v docker` = /usr/local/bin/docker; `~/.docker/run/docker.sock` exists; `pgrep -fl` shows `com.docker.backend` running. I did not query the engine (my fences forbid docker).
- `ci.yml` at 884fd72 (682 lines, `grep -n`): `api` :32-33, restore :49, vulnerable packages :55-70, build :71, Azurite :76-85, test :87, Azurite-by-name :88-121, deploy package :125-133. `api-sqlserver-shard` :165-166, matrix :175, step :242-260, filters :252/:255/:256, floors :314-316. Roll-up :353-365.
- `build-migration-bundles.sh` header (`sed -n 1,40p` of a gh raw read, not run): "`--sql-only` ... connects to no database".
- Pointers re-printed at 884fd72 with `awk NR==n` over gh raw reads:
  - FeedbackDispatcher.cs :127, :192, :200-202, :255-261
  - StubServer.cs :68/:69/:71
  - Hpsmpoc214Tests.cs :301/:303/:329/:339
  - AssessmentModule.cs :103
  - SqlServerWakeRetry.cs :23-25, :27-31, :67-73, :110-122
  - FeedbackModule.cs :86
  - ShowcaseSummaryTests.cs Facts :31/:104/:134/:163
  - ReportingEndpoints.cs at head :173-190; at main `no-findings` 0 (control `finding-unknown` :181)
  - ShowcaseSeeder.cs :251 (ExecutiveSummary only)
- Routing: `model-routing.md:108` (G1), `:109` (G2), `:111` (cap). Model `claude-opus-5-5` at `models_latest.json:17`. `brief_seat.sh:24` sets the Opus default.
- Round count: my loop over 175 `GATE VERDICT` first lines found 0 hits for `b1394|no-findings|hpsmpoc-api`. Control: `a new sign-in entry point` hit 2 (B1385, B1390).
- Landing rule: `CLARIFICATIONS.md:3617` (5799 lines, analysis repo, gh raw read).
- Ports 9520-9529:
  - `lsof` showed 0 listeners (control: 16 listeners in all).
  - A scan of 57 non-`.pre-` SEAT kits dated 9 and 10 Nov (including B1453 G377 and B1454 D57, which were new while I drafted) hit 0, and so did every other 9/10 Nov file in briefs/. Control `957x` hit 1 (B1453).
  - Blocks taken: 9570-9580, 9590-9999 except the gaps listed in the kit (B1394 holds 9720-9729).
  - Live panes: %0, %1, %11-%22 (G374/G375/G376 are live).
- Tools: `.tools/dotnet` 10.0.402 (global.json 10.0.401 with latestFeature). `.tools/venv` exists. `.tools/b1455` is absent. 1365 GiB free. load 9.48 / 13.95 / 19.34 on 18 cores.

## D-decisions (taken in the kit)
- D1 **Tier 1 Opus, row G1.** The built change is small and client-report-facing. The tier comes from the CLOSED lines, which rest on data access (428 retry) and audit text (315, 99 N-7). G2's own line (`:109`) sends a follow-up whose mechanism sits on a G1 surface to Opus.
- D2 **SQL Server shards NOT RUN.** There is no project script, and the seat holds "no docker". I did not have the seat query the engine either. The four items that lose their SQL Server proof are 428, 315's 60-run done-when, follow-up (b), and 436's own rows (they run in the api-assessment shard). Hosted CI on the PR is the proof and a landing condition.
- D3 **Main may move (PR 298).** The kit compares main to S3. If the overlap with the 3 paths is greater than 0, the seat STOPs. If it is 0, the seat continues on the new main and names it. This deviates from the template's "any move stops", on the brief's instruction.
- D4 **428 probed without a server.** The seat runs a real-SqlClient black hole on 127.0.0.1:9521 with Connect Timeout=2 and a planted password. It measures attempts, seconds and log secrets. It also fakes `-2` throws on a command, an open and a close for the non-idempotent-write property. The Feedback context's `EnableRetryOnFailure` hazard is source-argued only and is a Note (it predates the branch and is not in a CLOSED claim).
- D5 **315 loop on SQLite:** 60 runs of the N1 rows at merge, or an honest "n of 60 (stopped for time)" once HARD STOP minus 40 minutes arrives. A 20-run StubServer-order mutant tests the cause claim, including the ticket's text `attempt 2 finished (sen`. A planted-value probe checks the audit note.
- D6 **Migrations frozen, two ways:** 0 added `Migrations/` files plus equal ModelSnapshots, and a byte-equal `build-migration-bundles.sh --sql-only` output at main and merge. The project's own script needs no database.
- D7 **M-ALL:** a merge-tree of all five open lane heads (clean y/n). A run of the two classes that share the api-assessment shard happens only if time allows.
- D8 **Name scans are underscore-aware:** `(?<![A-Za-z])<name>(?![a-z])` with a `Then_by_<name>_it_passes` control that must count 1 and a `\b` counter-control that must count 0. The names come from the project's CLAUDE.md and JIRA.md, and only their COUNT is written down.
- D9 **Port block 9520-9529.** The seat uses 9521 for the black hole and 9522 as the no-listener control.

## Q-questions for Tuesday (each with a default)
- Q1 Should this seat get a one-off docker grant to run a local SQL Server and the two shard commands from `ci.yml:251-257`? **Default: NO.** There is no project script, the HPSM-POC hold says no docker, and hosted CI on the PR is the SQL Server proof.
- Q2 If PR 298 lands before launch (no overlap), do you re-stamp S3 to the new main, or let the seat judge whatever main it reads? **Default: re-stamp S3 at the stamp to the main you read.** The kit already handles a 0-overlap move at Step 0.
- Q3 Should an M-ALL conflict on paths that are not this branch's (for example between b1392 and b1395 on `web/src/server/mock/`) stay a Note? **Default: yes, a Note for the landing order.**
- Q4 Should the seat's verdict cover the HELD items (99 N-4/N-9, 322 B477-7/-8, 428's hosted visit)? **Default: no.** They are graded only as "stated as held" and are not findings.

## UNMEASURED
- Whether the docker engine answers (not queried).
- Hosted CI on any PR for this branch (no PR exists).
- Every count in the builder's STATUS (left for the seat).
- The pointers in `Hpsmpoc99Tests.cs`, `FeedbackEndpoints.cs`, `Hpsmpoc226N9ExportTests.cs`, `NarrativeOutputValidator.cs` and `Providers.cs:144,157` (not re-printed by me).
- Whether any web path can send `finding-explanation` (left to Step 5(a)).
- Whether `-2` SqlExceptions can be constructed the way the existing rows do it (left to the seat's `grep -n`).

## Outside-the-fences disclosure
- No git write verbs and no `merge-tree --write-tree`. All repo reads went through `gh api -X GET` under the project's GH_CONFIG_DIR. No token was printed.
- No docker command was run. Only `command -v`, `ls -l` of socket paths and `pgrep -fl` (read-only process listing).
- `tmux list-panes -a` (read-only).
- I read the project's stale `2_Project_Files/global.json` once (read-only). The authoritative copy was then read from main via gh.
- Scratch files were written only to the session scratchpad.
- I did not read `_ledger.md` and ran no recursive grep in `0_Brain/learnings/`. I did not run `decision_queue.sh`. Nothing under `.tools/b1394/` was read. Only the builder STATUS and kit were read, as the brief asked.
- Writes: the two files in `tuesday/briefs/` only.
