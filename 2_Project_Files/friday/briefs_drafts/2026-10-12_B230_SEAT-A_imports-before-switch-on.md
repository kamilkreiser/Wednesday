From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to (your STATUS file is the wrap).

# BRIEF B230 (SEAT A): HPSM-POC — imports, before they are switched on: a firmware version must hold an ASCII letter or digit (HPSMPOC-229 R3-1), a database error at the phase-2 save marks the run failed (HPSMPOC-229 R3-2, first half), the cap-file test stops timing out under parallel load (HPSMPOC-247), and a test proves the API's log carries no device identifier (gate B205 N-1)

**From:** Friday, fired @NOW@. This is a DRAFT by Friday's drafter. Pins were read 08:23Z on 2026-10-12 UTC (19:23 AEDT). Friday re-pins at launch.

**Seat:** Datasec/HPSM-POC-A, pane Datasec/HPSM-POC-A.
- **How the launcher picks the brief.** It tells the seat its commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains `_SEAT-${SEAT}_` (NOT simply the newest file)" (`Launch_Claude.command:110`). The seat comes from the pane name `*HPSM-POC-?` (`:106`). This file is that one once it is copied into `Briefs/` (`2026-10-12_B230…` sorts after `2026-10-12_B228…`).
- **The last `_SEAT-A_` builder, B228, is finished.** Its STATUS ends `READY FOR GATE: b228/demo-name-check-round-3 371f9005e7528e06c8fc0d7a371706de540bbfad` (`Briefs/2026-10-12_B228_STATUS.md`, last line).
- **Its gate B229 (Seat E) is IN FLIGHT** on ports 6981–6990, with containers `b229-mssql` and `b229-azurite`. You run beside it; touch nothing of it.
- **B230 is free:** `ls -a .tools | grep -i b230` → nothing; no `b230*` ref (`ls-remote`, 08:23Z).

**Report:** `Briefs/2026-10-12_B230_STATUS.md`, written as a file in `1_Project_Definition/Briefs/`.
- **Sections:** BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · NEW WORDS · Records.
- **Do not commit records, and do not write `5_Project_History/history.md`.** This overrides the launcher's "record progress … history.md and the Jira ticket(s)": Friday does both.
- **Evidence:** summaries in `Briefs/2026-10-12_B230_evidence/`. Kits and raw logs stay in `.tools/b230/`. No scripts in the records (B100).
- **Last line, exactly:** `READY FOR GATE: b230/imports-before-switch-on <sha>`, with the sha read by `git ls-remote origin refs/heads/b230/imports-before-switch-on` after your last push. Or `STOPPED: NEEDS FRIDAY` plus ONE question.

**QA tier 1** (data integrity of imported customer evidence). A QA gate follows. Kam approves every user-facing word on a card (NEW WORDS) before any deploy.
- **Nothing is deployed in this brief.** Imports stay OFF on hosted: `appsettings.json:17` `"ImportsEnabled": false`; C-84 (analysis CLARIFICATIONS `:947`, "Imports 404 …").
- **Do not change that setting.**

**Premise key:**
- `(ls-remote 08:23Z)` = read by the drafter with that verb.
- `(read: file:line)` = quoted by the drafter at `caa5a97` with `git show`/`git grep` in `2_Project_Files`, with `--no-optional-locks`.
- **UNMEASURED** = not established by the drafter; the instrument that closes it is given.

Re-check every premise at your start. A wrong premise is a finding. A moved pin is a STOP unless a rule below covers it.

## AUTHORITY
- **Kam, verbatim (relayed by Friday, 2026-10-12 ~18:4x AEDT):** "keep going and keep rolling out agents to work through all tickets and items for MPS Calculator, Security Controls creation tool and HPSM POC". This lane is HPSM-POC tickets, nothing else.
- **HPSMPOC-229** (Jira, read-only; filed by B168 on Friday's B168 ADDENDUM-4): "Two notes from gate B172's re-check of the import … Neither matters while imports are switched off on the hosted site … both must be fixed before they are switched on there". Recommendation: "(1) the reader's firmware rule at least as strict as the database CHECK, and a rule that every SQL Server CHECK on an import table has a reader twin tested on SQL Server; (2) phase-2 database errors handled like store errors, plus a reconcile of runs left pending."
- **HPSMPOC-247** (Jira): "Options: (a) give that test's client a longer timeout … (b) run the cap-file test in a non-parallel collection; (c) both. Recommend (b): it also keeps the cap test from slowing every other class." Its 10-12 comment (B222) adds 3 sightings, every re-run alone green.
- **BACKLOG gate B205 N-1** (analysis `origin/main` `bb1e888`, `BACKLOG.md:116-123`): "no test pins that the API's own log output carries no identifier. … Fix-shape (prose): in `ImportMinimisationTests`, capture the host's log output for one SM upload and one FTA upload, and assert `NoIdentifier` over the captured text. The capture is a test `ILoggerProvider` added through the `ApiFactory`'s `ConfigureLogging`, plus `Console.Out` redirected for the call. Regression test: green at head, red under T3."
- **Standing rulings that bound you:**
  - **C-73** (CLAR `:768`): build Phase A of the SM/FTA input design; the printer's firmware number comes with the device.
  - **C-88** (CLAR `:1002`): device identifiers are dropped at import; keep firmware version, model and counts.
  - **C-96** (CLAR `:1077`): a cleaned copy of each uploaded file is stored.
  - **Never weaken any of them.**

## PINS (read by the drafter; instrument inline)
| What | Value | Instrument |
|---|---|---|
| `main` | `caa5a9713d4e5257d68d2a91ee1d331e3a1fc5d9` (#144 B224 on #143 B226) | `git ls-remote origin refs/heads/main 'refs/heads/b2*'` (08:23Z) |
| `caa5a97` locally | present (`cat-file -t` → commit, 08:2xZ) | `git cat-file -t caa5a97` |
| `b228/demo-name-check-round-3` | `371f9005e752…` (in gate B229; **not yours**) | same `ls-remote` |
| `b230/*` | does not exist | same `ls-remote` |
| In-flight diff (never yours) | `git diff --name-only caa5a97...371f900` gives 3 paths: `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs`, `api/tests/HpsmPoc.Api.Tests/Assessment/B226NameMatchingTests.cs`, `…/Assessment/B228NameMatchingTests.cs` | `git merge-base caa5a97 371f900` = `caa5a97` |
| `.tools/.git-lock` | absent (free) at 08:2xZ | `ls -la .tools/.git-lock` |
| Ports 6960–6969 | 0 lines | `lsof -nP -iTCP:6960-6969` (08:23Z) |

## BASE AND BRANCH
- **Branch: new `b230/imports-before-switch-on` from main `caa5a97…`.** Re-read main with `ls-remote` at your start.
- **If main moved:** run `git diff --name-only caa5a97 <new>`. If no changed path is under `api/src/HpsmPoc.Modules.Assessment/Ingest/**`, `api/tests/HpsmPoc.Api.Tests/Imports/**`, `api/tests/HpsmPoc.Api.Tests/Support/**` or `.github/workflows/**`, branch from the new main and report both shas in BLUF. Otherwise **STOP**.
- **Red-first base = `caa5a97`.** Each new or changed test is red there (where it pins a behaviour) and green at your tip.
- **Worktrees:** `.tools/wt-b230` (tip), `.tools/wt-b230-base` (at `caa5a97`), `.tools/wt-b230-mut` (mutants). Scratch goes in `.tools/b230/`.
- **The shared lock.** Every code-repo ref write (fetch, worktree add, branch create, commit, push) goes under `.tools/.git-lock`. Copy `.tools/b228/lock.sh` to `.tools/b230/`. Never remove another seat's lock.
- **In `2_Project_Files` itself:** read git verbs only, with `--no-optional-locks`.
- **Push a NEW branch:** `git push origin b230/imports-before-switch-on`.
  - No `--force`, no `--force-with-lease`, no `+refspec`. Later pushes fast-forward only.
  - Run `ls-remote` before and after each push and record the lines.
  - A refused push → STOP.

## PORTS: 6960–6969 only
- **Never yours:**
  - 6981–6990 (gate B229, live now: `b229-mssql` on 6985, `b229-azurite` on 6988, APIs on 6983/6984, web on 6981);
  - 6940–6949 (B231, Seat B, running beside you);
  - every other seat's.
- **Plan:**
  - 6965 `b230-mssql` (make it with a copy of `.tools/b224/sqlstart.zsh` re-keyed to `b230`: CI image digest; the random sa password lives only in `4_Credentials/b230-sql.env`, read by name, never printed);
  - 6968 `b230-azurite` (as `.tools/b226/azurite.sh`, re-keyed);
  - 6962 API tip and 6963 API base, only if you need a live probe;
  - 6969 spare.
- **Re-check with `lsof` before every bind** and log it.
- **At the end:** stop your containers (`docker stop`, never `rm`, never `-v`). Never touch `b229-*` or any other seat's container.
- **Secrets:** never open, print or copy `4_Credentials/.env`. Your own `b230-*.env` files are read by name only.

## PRIOR WORK (required BEFORE any code; cite `file:line` at `caa5a97`)
- **The project's CLARIFICATIONS.** The local working copy is stale: it ends at C-30, because the local analysis `main` is behind 111. Read analysis `origin/main` `bb1e8887687c07695dbca4b8dd35ff29d9df2344`:
  - `git -C <project root> --no-optional-locks show bb1e888:1_Project_Definition/CLARIFICATIONS.md` if the object is local;
  - otherwise a shallow clone of the analysis repo into `.tools/b230/ana`, using the project's analysis deploy key by the repo's own `core.sshCommand`.
  - **Cite** C-73 (`:768`), C-84 (`:935`, `:947`), C-88 (`:1002`), C-96 (`:1077`).
  - **Search** for any later ruling on imports, firmware or HPSMPOC-229/247: `grep -n -i 'import\|firmware\|HPSMPOC-229\|HPSMPOC-247'`, with a positive control (C-88 must hit).
  - **A ruling that contradicts this brief → STOP.**
- **BACKLOG.md** at the same rev (`:116-123`, B205 N-1, quoted above). The project's local `BACKLOG.md` is stale (53 lines); do not use it.
- **The code you change** (read: at `caa5a97`):
  - `Ingest/ImportReader.cs`: `Visible` `:328-329` (white space, control, Format and separator categories only, no ASCII rule); the SM Devices row `:383-399`, where the firmware check `:395` reads `"The device has no firmware version."`; the header check `:173-175`.
  - `Ingest/ImportEndpoints.cs`:
    - phase 1 `:90-117` (the run row saved `:115-116`);
    - **phase 2 `:119-135`:** the store write is inside a try `:122-132` (→ `FailAsync` + 500 `import.store-failed` `:129-131`), but **`reading.File.StoredAt = …; await db.SaveChangesAsync(CancellationToken.None)` at `:133-134` is OUTSIDE it**;
    - phase 3 `:137-185` (its catch `:179-184`: `DbUpdateException or InvalidOperationException or DbException` → `FailAsync(…, run.RunId)` + 500 `import.rows-failed`);
    - `FailAsync` `:194-…` ("A failure here leaves the run `pending` … never an orphan", `:196-197`);
    - `ImportLog` `:302-…` (EventIds 3300–3302).
  - The CHECK this rule must match: `AssessmentDbContext.cs:341` `ck_import_sm_device_firmware` `"TRIM(firmware_version) <> ''"`. **Read only; no migration in this lane.**
- **The tests you extend** (read):
  - `Imports/ImportRobustnessTests.cs`: R2_2 at `:235`; `R2_2_the_reader_allocates…` `:219`; `import.store-failed` asserted at `:128`. 0 hits for `Collection` or `Timeout`.
  - `Imports/ImportMinimisationTests.cs`: `NoIdentifier` `:68`, used `:125-135`, `:231-235`, `:252`. 0 hits for `ILoggerProvider` or `ConfigureLogging`.
  - `Imports/ImportTests.cs`.
- **Earlier STATUS files, read before code:**
  - B172 STATUS "ROUND 2 RE-CHECK" (R3-1, R3-2 instruments `B172R3.R2_4_firmware`, `B172R3.R2_1_atomicity_at_every_point`);
  - B203 and B205 STATUS (`2026-10-11_B205_STATUS.md:54-61`, mutant T3);
  - B206 STATUS (the kept copy);
  - B213 STATUS `:101-103`, `:137`, `:146` (R2_2 sightings).
  - Kits in `.tools/b172/`, `.tools/b205/` and `.tools/b213/` are **reference only**: read them, do not run or edit another seat's kit.
- **SQL Server test switch:** `HPSM_TEST_SQLSERVER` (read: `Support/SharedDatabase.cs:9`, `Support/PrivateDatabase.cs:27`, `Support/ApiFactory.cs:26`). CI runs `HpsmPoc.Api.Tests.Imports.*` in shard `api-other-and-feedback` (read: `.github/workflows/ci.yml:62-65`).

## THE WORK (in order; red-first for every new or changed test)

**1. FOUND, measured first (before any code), at `caa5a97`, on SQLite AND on `b230-mssql`:**
- **R3-1.** Upload an SM Devices CSV whose firmware cell holds only one of these:
  - U+034F, U+FE0F, U+2800;
  - U+3164, U+FFA0, U+115F;
  - an ASCII control: "firmware = <only that>".

  For each, record: the HTTP status and code, the run status, the rows per file, and the `import_sm_device` rows. Expected per the ticket: SQLite stores the row, and SQL Server refuses the WHOLE upload (500 `import.rows-failed`, 0 rows for every file). Hangul fillers count as a version on both.
- **R3-2.** Force a database error at the phase-2 `SaveChangesAsync` (`:134`). Use a test-only interceptor or a connection fault, as B172's `R2_1_atomicity_at_every_point` did; read its instrument first. Record:
  - the status and body;
  - the run status (expected `pending`);
  - whether a stored file shows "not landed" (download 404) while its bytes exist.
- **R2_2.** Its wall time alone (×5) and inside the full `HpsmPoc.Api.Tests` project under the 3-concurrent-copies load B213 used (`B213_STATUS.md:137`), with load1 per run. Report reds per copy.
- **B205 N-1.** Re-make mutant T3 at `caa5a97` (a `Console.WriteLine` of the raw row at the top of `ImportReader.Add`, or its equivalent at this tree) and show the suite is green under it (0 red).

**2. R3-1 fix (`ImportReader.cs` only).**
- **Rule:** a firmware version must contain at least one ASCII letter or digit (`[A-Za-z0-9]`), on the same field, before the row is emitted. HPSMPOC-229: "the tools' shapes are ASCII, e.g. 2509999_000073".
- **Keep `"The device has no firmware version."` as the rejection words** if they fit. If you change or add a reason, it is a NEW WORD.
- **Do not change `Visible`:** other columns use it.
- Prove "at least as strict as the CHECK": every value the reader accepts is accepted by `TRIM(firmware_version) <> ''` on SQL Server. Use a theory test on SQL Server over the FOUND set plus normal versions (`2509999_000073`, `5.7.0.2`, `FutureSmart 5.7`) and a leading or trailing blank.
- **The "reader twin" rule.** Add ONE test that enumerates every CHECK on an `import_*` table from the EF model (`IEntityType.GetCheckConstraints()`) and fails if a constraint has no named reader-twin test row. A list in the test, kept beside the CHECK names, is fine. Report the CHECKs it finds, with names.

**3. R3-2 fix, first half only (`ImportEndpoints.cs`).**
- **The fix:** a database error at the phase-2 `StoredAt` save is handled like a store error. It is caught (the same exception set as phase 3), logged (`ImportLog`), and the run is marked failed through `FailAsync`. The answer is 500 with an existing code. **Use `import.store-failed`** (the files could not be recorded as kept); its words are unchanged.
- **No new error code and no contract change.** The contract names exactly `import.store-failed` and `import.rows-failed` (read: `api/tests/HpsmPoc.Api.Tests/Contract/openapi.yaml:901`, `:950`). If you need a new code or new words, **STOP: NEEDS FRIDAY**. A contract edit would pull in `web/contract/**` and `web/src/api/contract-drift.test.ts` (gate B218 N-4).
- **Regression test:** the run is `failed` (not `pending`) after a forced phase-2 database error, on SQLite and SQL Server. No stored path is left unnamed (B172's orphan check). Red at `caa5a97`.
- **NOT IN SCOPE (say so in NOT TESTED; it stays on HPSMPOC-229 for Friday):** "a sweep or reconcile of pending runs". That is new start-up or background behaviour (`Program.cs`, hosted), which this lane does not own.

**4. HPSMPOC-247 (tests only).** Take option **(b)**: put `R2_2_an_upload_of_the_cap_file…` in a non-parallel xUnit collection, defined in a new file under `Imports/`. Option (a)/(c) (also raise that test client's `HttpClient.Timeout`) only if (b) alone still reds under the FOUND load, and say which.
- **Proof:**
  - same load as FOUND, ≥ 3 copies × 3 rounds, at tip and base, interleaved, with load1;
  - tip 0 red, and base's reds recorded;
  - plus R2_2 alone ×5.
- **Report** the full-project wall-time change this costs: a non-parallel collection runs after the parallel ones.

**5. B205 N-1 (tests only).**
- **The capture:** in `ImportMinimisationTests` (or a new file in `Imports/`), capture the host's log output for one SM upload and one FTA upload, and assert `NoIdentifier` over the captured text. Use a test `ILoggerProvider` via `WithWebHostBuilder(...ConfigureLogging...)` on the test's own factory, plus `Console.Out` redirected for the call.
- **Do not edit `Support/**`** (shared by every seat's tests). If a helper is needed, it lives in `Imports/`.
- **Red under T3 (the brief's regression); green at tip.**

**6. Mutants** (in `.tools/wt-b230-mut` only). Each must go red, then be restored EQUAL by `git diff --quiet` AND a byte compare.
- The ASCII rule dropped (R3-1 rows red, SQLite and SQL Server).
- The ASCII rule widened to any letter (`Rune.IsLetterOrDigit`): the Hangul-filler rows red.
- The phase-2 catch removed (R3-2 red).
- `FailAsync` not called in the new catch: red.
- T3 (B205 N-1 red).
- The R2_2 collection attribute removed: report its load series. This is a timing proof, not a red/green one; say so.

**7. Suites, at your tip:**
- `HpsmPoc.slnx` all projects on SQLite + `b230-azurite`, 0 skipped. Counts go beside B227's 2,788 (`B227_STATUS.md:53`) plus your added tests.
- `HpsmPoc.Api.Tests` with `HPSM_TEST_SQLSERVER` on `b230-mssql`, both CI filters (`~HpsmPoc.Api.Tests.Assessment.` and `!~…`). Counts per filter.
- contract-drift unchanged (no contract file in your diff).
- gitleaks over `caa5a97..<final>`. A raw scan of added lines: invisible and Hangul-filler characters appear ONLY as escapes (`ㅤ`), never raw (HPSMPOC-152's class).
- **Known flakes** (HPSMPOC-247 is yours now; `RequestTimingLogTests` BACKLOG `:56`): re-run alone and report. Never skip.

**8. THE CI TIMEOUT (measure; a workflow change is Kam's, not the seat's).**
- **The facts:** the `api` CI job ran **14m12s against `timeout-minutes: 15`** (read: `.github/workflows/ci.yml:35`; run 38191901218, attempt 2; Friday's read, UNMEASURED by the drafter). The job runs `dotnet test HpsmPoc.slnx -c Release --no-build` (`:87`). B228 (in gate) also adds tests.
- **Measure:** the `HpsmPoc.slnx` wall time at `caa5a97` and at your tip, Release, `--no-build`, same machine, interleaved, 3 runs each, with load1 per run. Report the test-count delta and the time delta per added or changed class, R2_2's collection change on its own line.
- **Project:** 852 s × (tip median ÷ base median).
  - **≥ 900 s → STOP: NEEDS FRIDAY.** Do not touch `ci.yml`, and do not split, skip or trim tests to fit.
  - **≥ 870 s → say so in BLUF** as a margin under 30 s.

**9. Partition.**
- **Yours:**
  - `api/src/HpsmPoc.Modules.Assessment/Ingest/ImportReader.cs`;
  - `api/src/HpsmPoc.Modules.Assessment/Ingest/ImportEndpoints.cs`;
  - `api/tests/HpsmPoc.Api.Tests/Imports/**` (existing files, plus ≤ 3 new files).
- **NOT yours:**
  - every path in `caa5a97...371f900` (above);
  - `api/src/HpsmPoc.Modules.Assessment/Endpoints/**` and `api/tests/HpsmPoc.Api.Tests/Assessment/**` (the Demo name-check path, in gate B229);
  - `Ingest/Csv.cs` and `Ingest/ImportEvidence.cs` (read only);
  - `Persistence/**` and every migration;
  - `Support/**`, `Program.cs`, `appsettings*.json`, `*.csproj`;
  - `web/**` (Seat B's lane, B231, runs beside you);
  - `web/contract/**`, `api/tests/HpsmPoc.Api.Tests/Contract/**`, `.github/workflows/**`, `infra/**`;
  - records beyond your own STATUS and evidence;
  - every other seat's worktree, kit, container, port or branch.
- **Prove it** with `git diff --name-only caa5a97..<final>` in HOW, and with the empty intersection against `git diff --name-only caa5a97...371f900`.

## STANDING LINES
- **Push your branch only.** Friday opens the PR and lands it once CodeQL and the checks are green. Never push an unscanned commit to main. Never dismiss an alert. **No PR** from this seat.
- **Never delete files:** quarantine them. Never edit a running script. Use your own worktree and kit only. Never `gc`, `prune`, `worktree remove` or `reset` anything of another seat's, or `2_Project_Files` itself.
- **Nothing deployed:** no Azure, no `az`, no setting change, nothing hosted.
- **No Jira or BACKLOG write.** Read-only searches are allowed; cite the queries and counts. Friday files tickets.
- **No `history.md` entry and no commit to the analysis repo.**
- **No contact with HP or any human.**
- **Every factual claim in STATUS carries its source** (`file:line` or the command), or the word UNMEASURED with why and the closing instrument.

## HOLDS
- **HP Restricted material.** No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)). That covers Claude seats, subagents, the product's model, Ornith and the Spark. Do not open `HP Reporting and Docs/` or the SOW file in the project root.
- **Datasec only.** No other client's names, tickets or paths.
- **Fixtures are synthetic.** Device names, serials, IPs and MACs are synthetic, as `Imports/Fixtures/*.synthetic.csv` are. No real customer export.
- **Stopping processes:** stop any process of yours by port + cwd, never by name, and never another seat's.
- **Imports stay OFF on hosted. No product trade-off is picked silently:** if the ASCII rule would refuse a firmware shape a real SM or FTA export is documented to emit, **STOP: NEEDS FRIDAY**. Check the B161/B166 guides (`1_Project_Definition/Content/hpsm-sm-3.16/`, `…/fta/`) and the fixtures.

## REPORT (`Briefs/2026-10-12_B230_STATUS.md`)
- **BLUF:**
  - main and `b228/*` at start and end;
  - per item (R3-1 · R3-2 first half · 247 · B205 N-1): done or not, the red-first evidence and the killing mutant;
  - the import-CHECK census;
  - R2_2's load series, base and tip;
  - the CI projection;
  - the flag line **"B230: imports stay OFF on hosted; the pending-run sweep (HPSMPOC-229 R3-2, second half) is not built; no contract change."**
- **FOUND** (item 1). **TESTED** (red-first logs, mutants, suites per class and per provider). **HOW** (commits, the rule and why ASCII, the CHECK census, the phase-2 catch, the collection, the log capture, the partition proof).
- **NOT TESTED:** each UNMEASURED item with its instrument; the sweep; hosted, by HOLD.
- **PRIOR WORK.**
- **NEW WORDS:** expected none (`import.store-failed`'s words unchanged; the firmware rejection words unchanged). List any you add.
- **Records:** ports free by `lsof`, containers stopped, lock free, nothing sent to any human.

## UNMEASURED at draft time (and what closes each)
- Whether SQL Server still refuses the whole upload at `caa5a97` for the R3-1 set: closed by FOUND item 1.
- Whether any documented SM/FTA firmware shape lacks an ASCII letter or digit: closed by the guides and fixtures read (HOLDS).
- The CI 14m12s figure (Friday's read): closed by Friday's PR run; yours is the local projection.
- Whether (b) alone ends R2_2's reds under load: closed by item 4's series.
