From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to.

# BRIEF B213 (SEAT D): HPSM-POC — ROW 1 + ROW 1b (first, they block deploys: two time-budget tests): make `RequestTimingLogTests` stop failing on runner timing while it still fails on a real regression (test only) · ROW 2: B211's notes on B206 (N-1 the `%PDF-` `.csv`, N-2 a Down test for the migration, N-5 the README line)
**From:** Friday, @NOW@ 2026-10-11 (DRAFT by Friday's drafter; pins read 08:33Z–08:36Z; Friday re-pins at launch). **Seat:** Datasec/HPSM-POC-D, pane Datasec/HPSM-POC-D. The project's launcher picks the newest `Briefs/` file containing `_SEAT-D_` (`Launch_Claude.command:106`, `:110`). The newest one now is `2026-10-11_B206_SEAT-D_…`, so this file is the newest once it is copied into `Briefs/`. **B213 is free:** `ls Briefs | grep -ci b213` → 0; `ls briefs_drafts | grep -ci b213` → 0; `ls .tools | grep -i b213` → nothing.
Report `Briefs/2026-10-11_B213_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · NEW WORDS · Records). Write it as a file in the project's records folder (`1_Project_Definition/Briefs/`, the project-root repo); do not commit records. Evidence goes in `Briefs/2026-10-11_B213_evidence/` (summaries only); kits and raw logs stay in `.tools/b213/`, and no scripts go in the records (B100). Last line exactly `READY FOR GATE: b213/timing-bounds-import-followups <sha>` (the sha read by `ls-remote` after your last push), or `STOPPED: NEEDS FRIDAY` and ONE question.
**Tier 2** (through-code gate). Row 1 changes one test file and no product behaviour. Row 2 changes how one crafted upload is handled, adds one test and fixes one README line. A QA gate follows, and Friday opens the PR. **Nothing is deployed in this brief.**

**Premise key:** `(ls-remote 08:33:01Z)` = read by the drafter with that verb at that time · `(git <verb>)` = a read verb on a scratch `clone --shared` of `2_Project_Files` with `main` fetched · `(gh …)` = `friday_as.sh datasec gh …`, read only · `(read: file:line)` = quoted from that file at `46da436` · **UNKNOWN** = not established by the drafter; the reason and the instrument that closes it are given. Re-check every premise at your start. A wrong one is a finding. A moved pin is a STOP unless a rule below covers it.

## AUTHORITY
- **Row 1:** Friday's order. CI went red on this test four or more times today (table below), each time on a tree that passed elsewhere. A red `ci` on main blocks the deploy lane. There is no Kam ruling on the test: it is test hygiene, and the bound must stay able to catch a real regression (Row 1 rules).
- **Row 2:** gate B211 `B206 0cb0922: GO WITH NOTES` (read: `2026-10-11_B211_STATUS.md:1`), "Open, for Friday" N-1, N-2, N-5 (read: `:322-325`). B206 merged as PR #138 → main `46da436` (below). Kam's B206 ruling still stands (verbatim, read: B206 brief AUTHORITY): **"Decision hpsmpoc-import-kept-files-identifiers-1011: b — Store a cleaned copy instead (recommended)"**: *"The stored CSV has the identifier cells blanked, so a file is still kept as evidence but holds no identifier."* **The N-1 choice below is Friday's reading of those words, flagged for Kam, not a Kam ruling.**

## WHERE THIS COMES FROM (read these whole, first)
- `Briefs/2026-10-11_B211_STATUS.md`: Findings N-1 (`:59-65`), N-2 (`:66-79`), N-3 (`:80-86`), N-4 (`:87-94`), N-5 (`:95-97`), with each fix-shape and regression test; Mutants (`:252-261`, Td1 / Td2).
- `Briefs/2026-10-11_B206_SEAT-D_store-cleaned-import-copy.md` and `Briefs/2026-10-11_B206_STATUS.md`: your B206 (the not-read rule, "every data cell blanked"; FOUND 8 the README).
- `Briefs/2026-10-10_B195_SEAT-A_ADDENDUM-2_ci-sqlserver-timing-finding.md`: Friday's first ask on this flake (the 1128 run): "do NOT widen the bound by guessing … propose the bound change with that evidence". **UNKNOWN: where B195 answered it.** There is no `B195*STATUS*` file in `Briefs/` (`ls Briefs | grep -i b195` → the brief and two addenda only). Close it with `grep -rl "ADDENDUM-2" Briefs/ 5_Project_History/` and cite what you find, or say "not found".
- `Briefs/B210_ADDENDUM-1_q-b210-1-ci-rerun-state.md:8` (Friday's count of four today), `Briefs/2026-10-11_B210_STATUS.md:141` (the 2521 run), `Briefs/2026-10-11_B205_STATUS.md:67-71` (N-3), `BACKLOG.md:24-29` (the B202 follow-up).

## PINS (read by the drafter; instrument inline)
| What | Value | Instrument |
|---|---|---|
| `main` | `46da436702857941477402a3a35877411762865d` (PR #138 squash, "B206: store a cleaned copy of imported CSVs"); parent `ef69c4cf8611d0739c3cc43ef237c052e77bdf9c`; tree `89e2430619a70ecbf065f7c457f96ef04bd9fc20` | `git -C 2_Project_Files --no-optional-locks ls-remote origin refs/heads/main` (08:33:01Z); `rev-parse FETCH_HEAD FETCH_HEAD^{tree} FETCH_HEAD^` in the drafter's scratch `clone --shared` after `fetch origin main` |
| main tree = B206 tip tree | `git diff --quiet 0cb0922 46da436` → rc 0. **So B211's `file:line` refs (read at `0cb0922`) hold at `46da436`.** | (git diff) |
| `46da436` in `2_Project_Files`' object store | **NOT present** | `git --no-optional-locks cat-file -t 46da436…` → "could not get object info" (08:33Z). **You need one fetch of `main`. Take the lock for it.** |
| Other branches | `b208/customer-frame-alias` = `b885cbf6aa82ad97631a9be402db2f9a4e4259de` (under gate B212); no `b213/*` | `ls-remote origin 'refs/heads/b2*'` (08:33:01Z) |
| Test file | `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs`, last changed by `a50b22d` (B195, #133); before that `5a93aa3`, `80afdff`, `228032a` | `git log --oneline 46da436 -- <file>` |
| Latest `ci` on main | run `38123997170` on `46da436` (push, 08:12:32Z): **failure, but NOT this test**. See "Not this brief" below. | (gh run list / view) |
| `.tools/.git-lock` | absent, so free (a `mkdir` lock; `.tools/b209/lock.sh` / `.tools/b206/lock.sh`) | `ls` (08:3xZ) |

**At your start, re-read main** (`ls-remote`). If it is `46da436`, proceed. If it moved, read the new commit's files (`git diff --name-only 46da436 <new>`). If none of them is under `api/tests/HpsmPoc.Api.Tests/Hosting/**`, `api/src/HpsmPoc.Api/Timing/**`, `api/src/HpsmPoc.Modules.Assessment/{Ingest,Http,Persistence}/**`, `api/tests/**/Imports/**`, `api/tests/HpsmPoc.Api.Tests/Assessment/PersistenceTests.cs`, the module `README.md` or the contract copies, base on `46da436` anyway and report a read-only `git merge-tree --write-tree <new main> <your tip>` in BLUF. Otherwise **STOP**.

## THE OBSERVED FAILURES (the drafter's reads; re-quote each from the log in your FOUND)
The test's bounds (read: `RequestTimingLogTests.cs`): `Slack = 350` (`:247`, "Wide enough for a busy runner's scheduling, narrower than the gap between two stages' delays", `:246`). `StagedFactory`: `AuthDelay = 300, CallerDelay = 700, HandlerDelay = 1100` (`:253`). `CallerPartsFactory`: `LookupDelay = 400, WriteDelay = 900` (`:305`). Asserts: `:149` auth, `:150` caller, `:151` handler, `:152` rest, `:153` sum; `:223` lookup, `:224` write, `:225` caller ⊇ parts, `:227` sum. Stages are whole ms, **truncated**: `(long)Stopwatch.GetElapsedTime(…).TotalMilliseconds` (read: `api/src/HpsmPoc.Api/Timing/RequestTimingLog.cs:59`).

| # | Where | Run / attempt (instrument) | Assertion line (quoted from the log) | Stage |
|---|---|---|---|---|
| 1 | PR #133 `b195/api-fixes` `7609f3d`, job `api on SQL Server (api-other-and-feedback)` | `38054931274` attempt 1 (`gh run view 38054931274 --attempt 1 --log-failed`) | `RequestTimingLogTests.cs:line 150` · `Range:  (700 - 1050)` · `Actual: 1128` | caller, **+78 over** |
| 2 | B205's local merged-tree run (load 13–16) | not CI (read: B205 STATUS `:68`) | `:149` · `Range: (300 - 650) Actual: 832` | **auth**, +182 over. B205 calls it "caller"; the range and `:149` say auth. Quote it correctly. |
| 3 | PR #136 `b203/import-minimise` `9fb82eb`, job `api (ASP.NET Core)` | `38109651238` attempt 1 (`--attempt 1 --log-failed`) | `…caller_stage(write: "refresh") [FAIL]` · `RequestTimingLogTests.cs:line 224` · `Range:  (900 - 1250)` · `Actual: 899` | write, **1 ms under** |
| 4 | main push `ef69c4c`, job `api on SQL Server (api-other-and-feedback)` | `38116913868` attempt 1 (`--attempt 1 --log-failed`) | `…(write: "refresh") [FAIL]` · `RequestTimingLogTests.cs:line 224` · `Range:  (900 - 1250)` · `Actual: 2521` | write, **+1271 over** |
| 5 *(not in Friday's four)* | main push `3fa5c1b` (B200, #135), job `api (ASP.NET Core)` | `38107811879` attempt 1, **never re-run; that run is still `failure`** (`gh run view 38107811879 --log-failed`) | `…(write: "create") [FAIL]` · `RequestTimingLogTests.cs:line 223` · `Range:  (400 - 750)` · `Actual: 399` | lookup, **1 ms under** |
| 6 *(local)* | B202 laptop full run at `62bc3c5` under load | not CI (read: `BACKLOG.md:25-27`) | `:150` · `Range: (700 - 1050) Actual: 699` | caller, **1 ms under**. BACKLOG labels `:150` "auth"; the range is caller's. Quote it correctly. |

**The shape the drafter sees (a reading, not a cause; you measure it):** two classes. **(L) Exactly 1 ms under the injected delay** (#3, #5, #6). This is consistent with truncation to whole ms plus a timer that fires a fraction of a ms early relative to `Stopwatch`. **(U) Over by 78 to 1271 ms** (#1, #2, #4). This is consistent with a stall on a 2-vCPU runner (`ci.yml:159`) or a loaded laptop. Each tree passed on re-run or alone (B205: 5/5 alone, re-run 1,038/1,038; B210 ADDENDUM-1: "Each time the same tree passed elsewhere").

## ROW 1 — `RequestTimingLogTests` (FIRST; test file only)
**Ticket search (the drafter's, 08:3xZ; re-run it and cite it):**
- `BACKLOG.md` (36 lines): grep `RequestTiming|timing ?log|flak|InRange|Slack` → **1 hit**, the B202 follow-up `:24-29` (#6 above; open `[ ]`).
- `JIRA.md`: 0 hits (it holds no tickets).
- Jira `HPSMPOC`, read-only JQL `search/jql`:
  - `text ~ "RequestTimingLogTests"` → **0**;
  - `text ~ "RequestTiming"` → 1, HPSMPOC-232 (the hosted first-request time, not this test);
  - `text ~ "flake"` → 5 and `text ~ "flaky"` → 3, all e2e / vitest / harness (HPSMPOC-238, -244, -151, -144, -133), none this test;
  - `summary ~ "timing"` → 17, none this test (HPSMPOC-246 is the B193 gate notes on the timing *code*; HPSMPOC-247 is the import R2_2 flake);
  - `text ~ "Slack"` → 0.
- **So there is no Jira ticket for this flake, and one BACKLOG line.** Cite the BACKLOG line in PRIOR WORK, and in STATUS mark it "closed by B213 if gated". **No Jira or BACKLOG write in this brief:** Friday files or closes them.

**What the test protects (state it in BLUF, in your words):** B192 / B195 wrote it so that hosted's slow first read "says where the time went" (read: `:128-130`, `:198-201`). Each held stage is logged **in its own named stage**, the parts sit **inside** the caller stage, and the stages **add up to the total**. The delays are distinct "so a stage counted in the wrong place fails its range" (`:130`), and `Slack` is "narrower than the gap between two stages' delays" (`:246`). The regressions it must keep catching:
- a stage timed into the wrong bucket;
- a stage or a part missing from the line;
- the parts counted twice;
- **the line not written at all**;
- **real extra time inside a stage** (the B195 ADDENDUM-2 question: "does the split add REAL work inside the caller stage").

**Rules for the fix (all of them):**
1. **No retry, no skip, no `[Trait]` / filter exclusion, no move out of CI, no `Skip=`, no re-run loop, and no blanket widening of `Slack`.** A bound changes only with the measured distribution as its evidence (item 2).
2. **Lower bound (class L):** a tolerance below the injected delay is allowed only as large as you can justify from the code. Truncation is at `RequestTimingLog.cs:59` and wherever `RequestStages` / `Caller.cs` turn ticks into ms. Add the timer-granularity evidence you measure. The drafter expects 1 ms. Say why it is that number.
3. **Upper bound (class U):** whatever you choose, the tolerance above a stage's injected time must stay **below the smallest gap between two injected delays in that factory**, so that a stage counted in the wrong bucket still fails. The gaps today are 400 (auth→caller, caller→handler) and 500 (lookup→write). Shapes to weigh, measured, not guessed:
   - (a) the interceptor / auth handler records the **actual** elapsed time of its own injected wait (`Stopwatch` around the `Task.Delay`), and the stage is bounded against that, not the nominal constant (a stall inside the injection is then not a failure; a stall outside it is still bounded);
   - (b) re-space the delays with wider gaps and a wider slack (state the added test time);
   - (c) another shape you can defend.
   Pick one, and say why the others lose.
4. **Production code is not yours.** `api/src/HpsmPoc.Api/Timing/**`, `Http/RequestStages.cs`, `Identity/Caller.cs` and `Program.cs` are not changed. **If your measurement shows the product itself adds time inside a stage (a real defect, not runner noise), STOP** and give the file:line evidence.

**The work, in order:**
1. **FOUND, before any change, at `46da436`:** re-quote the six rows above from their logs (CI rows: run id, attempt, job, the `[FAIL]` line, `Range`, `Actual`, the stack line). Name every place a stage's ms is truncated (file:line). Name any other `Assert.InRange` on a measured time in this file (`:225`, `:227`, `:153` included) and say which class can fail it.
2. **Measure the distribution (base `46da436` = head before your change):**
   - this class alone ×30 and under deliberate load ×10. Load means what the failures had: e.g. 3 concurrent copies of the Api suite, or the B205 / B202 parallel-suites shape; state it and the load average;
   - on SQLite AND on your SQL Server 2025 (`@@VERSION` in the log, password masked);
   - per stage and per part, report (measured − injected): min / median / p95 / max, and the count of runs that would fail today's bounds;
   - **if load reproduces a red at base, keep that log: it is the flake's red.**
3. **Change the test** per the rules. In HOW, quote every changed bound with its before and after, and the measured number that justifies it.
4. **Red-proof that it still fails on a real regression.** Mutants live in a mutant worktree, never on your branch. Each must be red under the NEW test, then be restored EQUAL by `git diff --quiet` plus a byte compare:
   - **M1 absent line:** `RequestTimingLog` writes no line on an `Answered` path → red (the `WaitForAsync` → `Assert.Single` path).
   - **M2 slow stage:** a real, un-injected wait added inside the caller stage in product code (e.g. in `Caller.ResolveAsync` before its lookup). Find the **smallest added wait the new test catches**, by bisection, on SQLite and on SQL Server. It must be red at that size and stay below the factory's smallest gap (rule 3). Report the threshold at base and at head, side by side.
   - **M3 wrong bucket:** the caller's time is added to the handler stage (or the endpoint stamp is moved before the caller filter) → red.
   - **M4 missing part:** the lookup or write part is not recorded → red.
   - **M5 double count:** a part is added to the total twice → red (the sum assert).
   - **M6 auth stage:** auth time goes to `rest` → red.
5. **Green after:** the class ×30 alone and ×10 under the SAME load as item 2, on both providers: **0 failures**. Then the full Api suite once on each provider. If any run is red, it is a finding: report it, never re-run it away.

## ROW 2 — B211's notes on B206 (after Row 1 is pushed)
**N-1: a `.csv` whose bytes start `%PDF-` is kept byte for byte, identifiers included** (read: B211 `:59-65`; `ImportReader.cs:134-135` `if (bytes.AsSpan().StartsWith("%PDF-"u8)) return Done(reading, ImportKinds.Document, ImportFileStatus.Attached, null);` runs BEFORE the extension tests `:136-139`; `Kept` `:225` `if (reading.File.Kind == ImportKinds.Document) kept = bytes;`).
- **Propose, with code reasons (in BLUF):**
  - (R) **refuse** it, mirroring `:136-137` ("The file is named .pdf but is not a PDF."). Nothing is kept, and a new refusal reason appears.
  - (U) **treat it as an unreadable CSV**: when the name ends `.csv`, skip the `%PDF-` shortcut, so it takes the CSV path and B206's not-read rule (every data cell blanked; header line, row count and line structure kept).
- **Weigh both against:**
  - what each KEEPS: under (U) the header line survives raw, and for a crafted file that header can itself hold values. Measure it with B211's P1 bytes, `%PDF-1.7,Host Name,IP Address\r\nx,gate211-pdfpre-host,192.0.2.198\r\n`;
  - what a real binary PDF misnamed `.csv` does under each (no-comma lines, NUL bytes, size);
  - why the `%PDF-` test sits first (B172 R2-6, read: `:131`; `git log -S'%PDF-' -- …/ImportReader.cs` and the B172 brief or STATUS). Do not undo a gated decision silently;
  - the contract text (`createImport`'s reasons, the 0.17.0 changelog `openapi.yaml:227` "A CSV is no longer kept as uploaded").
- **Build the safer one** (the one that keeps less identifying data). Flag it in BLUF, in these words or close: **"N-1: built (R|U) as Friday's reading of Kam's 14:19:31 (b) words; Kam's word may change it."**
- A real PDF named `.pdf` stays `attached` and unchanged. A non-PDF named `.pdf` stays refused. Files stored before B213 are not changed.
- If the safer option needs a contract change beyond prose (a new status, field or enum value), **STOP**. Prose only: both contract copies byte-identical (sha256), `openapi.merged.json`, `npm run gen:api` if the generated file changes, `PROVENANCE.md` / `web/contract/SOURCES.md` re-hashed, and the version per `PROVENANCE.md`'s own rule (say which rule and which number).
- **Tests (red-first):** upload `devices.csv` with the P1 bytes. It is red at `46da436` (the tokens `gate211-pdfpre-host` and `192.0.2.198` are in the store and the download, read: B211 `:61`) and green after (refused, or no cell value kept). Run it on the File store AND the Blob store (your Azurite). Mutant: put back the old order → red.

**N-2: no test proves `ImportFileStoredSha256`'s Down** (read: B211 `:66-79`). The only down-migrating test, `api/tests/HpsmPoc.Api.Tests/Assessment/PersistenceTests.cs:186` (`MigrateAsync("20260924015317_ReadinessResult")`), passes through `ImportStore.Down`, which drops `import_file` whole and so masks it.
- Build B211's fix-shape:
  1. migrate to latest and record `import_file`'s DDL;
  2. migrate to `20261011021143_AttributionKeys` and assert the DDL equals a database migrated straight to `AttributionKeys`;
  3. migrate up again and assert the DDL equals step 1.
- On SQLite (`sqlite_master.sql`) and on the SQL Server leg (`sys.columns` / `sys.check_constraints` for `import_file`; compare by name and ordinal, not `column_id`, which is B211 N-4). Put it where CI's SQL Server shard runs it, and say which shard (`ci.yml:247` / `:250` filters on `HpsmPoc.Api.Tests.Assessment.`).
- **Red** under Td1 (the SQLite Down replaced by a no-op) and Td2 (the SQL Server Down without its `DropCheckConstraint`), re-made from B211 `:68` in your mutant worktree. Green at head.
- **No migration file changes:** `git diff --name-only 46da436..<final> -- '**/Migrations/**'` → 0 lines.

**N-5: module `README.md:90` still says "a tool's exported files, kept unchanged" and "A CSV or a PDF is KEPT byte for byte"** (read at `46da436`). Make the one-sentence fix-shape from B211 `:97`: since B206, a CSV is kept as a copy with its identifier cells blanked (`stored_sha256`); a PDF, and a file kept before B206, as uploaded. Add N-1's outcome to it. Change only that row's wording, with B213 named.

**NOT in this round:**
- **N-3** (loose `LIKE` on both hash CHECKs, `AssessmentDbContext.cs:283`, `:286`, the SQLite migration `:18`): fixing it needs a new migration on both providers. It is not in the same lines as N-1, N-2 or N-5, so it is not trivial. List it as open.
- **N-4** (SQL Server `column_id` on re-up): inherent, no fix (B211). List it.
- Also open, not yours: B205 N-1 (log-capture assertion; B211's Tf); HPSMPOC-247 (`ImportRobustnessTests.R2_2`); the pre-B206 stored data (not ruled).

## ROW 1b — `NarrativePipelineTests.B170_the_default_budget…` (added by Friday at placement; test file only; after Row 1, before Row 2)
**Friday's read, @NOW@ (`friday_as.sh datasec gh run view 38123997170 --log-failed`):** main `46da436`'s `ci` run `38123997170` attempt 1 failed in `api (ASP.NET Core)` on `HpsmPoc.Modules.Reporting.Tests.Narrative.NarrativePipelineTests.B170_the_default_budget_is_25_s_a_165_s_answer_is_generated_and_a_26_s_one_fails_closed_as_a_timeout` [26 s], `NarrativePipelineTests.cs:252`, `Expected: Tuple ("failed", "timeout")` · `Actual: Tuple ("generated", null)`. Friday re-ran the failed job (attempt 2) at @NOW@; **read attempt 2's result yourself** and quote it. Jira `text ~ "NarrativePipelineTests"` → 3 Done feature tickets, BACKLOG 0 (the drafter's search).
- Same shape as Row 1: a time-budget test judged on a shared runner. Establish from the test and the pipeline code how the 26 s case is timed (real wall clock vs an injectable clock/timer) and why a 26 s answer could come back "generated" under a 25 s budget.
- Fix in the TEST (or a test seam the product already offers) so the verdict does not depend on runner speed, e.g. a fake clock / deterministic delay. **The test must still fail on a real regression:** red-proof with a mutant that raises the default budget above 26 s (must go red) and one that removes the timeout path (must go red). No retry, no skip, no widened assertion.
- **If the cause is in the PRODUCT** (the budget is not enforced as specified), STOP: NEEDS FRIDAY with the lines; do not fix product code in this row.
- Write set addition for this row only: the test file `NarrativePipelineTests.cs` (and a test-only helper beside it if needed). Nothing else under `HpsmPoc.Modules.Reporting/**`.

## BASE
- Branch **`b213/timing-bounds-import-followups`** from **`46da436702857941477402a3a35877411762865d`**.
- Worktree `.tools/wt-b213`; a base worktree `.tools/wt-b213-base` at `46da436`; a mutant worktree `.tools/wt-b213-mut`; scratch `.tools/b213/`.
- Every code-repo ref write (fetch, worktree add, branch create, commit, push) runs under the shared lock `.tools/.git-lock`. Copy `.tools/b209/lock.sh` to `.tools/b213/`, and never remove another seat's lock. In `2_Project_Files` itself, use read git verbs only, with `--no-optional-locks`.
- **Row 1 is its own commit(s), pushed first**, so Friday can take Row 1 alone if Row 2 runs long. Say the Row-1-only sha in BLUF.
- Push a NEW branch: `git push origin b213/timing-bounds-import-followups`. No `--force`, no `--force-with-lease`, no `+refspec`; every later push is a fast-forward. Run `ls-remote` before and after each push and record the lines. A refused push → STOP.
- Read-only, in your scratch: `git merge-tree --write-tree <your tip> b885cbf` (B208's head) → state the exit code and whether any path is shared.

## PORTS: 6870–6879 only
The drafter checked at 2026-10-11T08:36:01Z:
- `lsof -nP -iTCP -sTCP:LISTEN` in 6700–6999 → 6755, 6756, 6860–6864 and 6867 only;
- `lsof -nP -iTCP:6870-6879` → 0 lines;
- `docker inspect` of every container's `HostConfig.PortBindings` (running and stopped), HostPort 6800–6999 → only `b212-azurite` 6867;
- `grep -hoE '\b68[7-9][0-9]\b'` over every HPSM-POC `Briefs/*.md` and Friday's `briefs_drafts/*.md` → only `6899`, which is a range end in B211's and B212's port text ("6700–6899"), not an allocation; `\b69[0-9][0-9]\b` → only `6999` (a range end).

**Never yours:** 6750–6769 (live elsewhere), 6770–6779 (B208), 6780–6789 (B206's, your old ones, stopped containers `b206-*`: do not restart them), 6790–6799 (B211), 6800–6855 (another seat's range), **6860–6869 (B212, live now)**.

Plan:
- **6870** SQL Server 2025 `b213-mssql` (CI's image by digest, as B205 / B211);
- **6871** Azurite `b213-azurite` (CI digest);
- **6872** API head (if a live probe is needed), **6873** base, **6874** mutant;
- 6875–6879 spare.

**Re-check with `lsof` before every bind**, and state the checks in STATUS. Containers `b213-*` only (new). Secrets go in `4_Credentials/b213-*.env`, read by name only. Never start, stop, reuse or remove any `b20[0-9]-*`, `b211-*` or `b212-*` container.

## PARTITION (from both sides)
- **Yours:**
  - `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs` (Row 1, the only Row 1 file);
  - `api/src/HpsmPoc.Modules.Assessment/Ingest/ImportReader.cs` (N-1; `ImportEndpoints.cs` only if the refusal path needs it, and say why);
  - import tests and fixtures (`api/tests/HpsmPoc.Api.Tests/Imports/**`, `api/tests/HpsmPoc.Modules.Assessment.Tests/Ingest/**`);
  - the N-2 test (`api/tests/HpsmPoc.Api.Tests/Assessment/PersistenceTests.cs` or a new file beside it);
  - `api/src/HpsmPoc.Modules.Assessment/README.md` (row `:90` only);
  - the contract copies, `openapi.merged.json`, `PROVENANCE.md`, `web/contract/SOURCES.md` and the generated `web/src/api/schema.gen.ts`, **only** if N-1 changes contract prose.
- **NOT yours: live seat `%60`, Datasec/HPSM-POC-E, gate B212** (read-only QA on `b208/customer-frame-alias` @ `b885cbf`, the web customer shell):
  - `web/src/components/customer/**`, `web/src/components/shell/**`, `web/src/components/screens/**`, `web/src/lib/**`, `web/e2e/**`;
  - in particular B208's 4 files (read: `2026-10-11_B208_STATUS.md:126-139`; B212 brief `:43`): `web/src/components/shell/CustomerShell.tsx`, `web/src/components/shell/CustomerShell.alias.test.tsx`, `web/src/components/customer/useCustomerShownAs.ts`, `web/e2e/customer-frame-alias.spec.ts`;
  - ports 6860–6869; containers `b212-*`; `.tools/b212/` and `.tools/wt-B212*`.
  - **From B212's side:** it writes no code, makes no commit and no push (read: B212 brief `:7`), and its partition check expects 0 `api/` files in B208. **So the two seats share no file.** Prove yours with `git diff --name-only 46da436..<final>` and grep it for `web/src/components|web/e2e|web/src/lib` → 0.
- **Not yours either:**
  - `api/src/HpsmPoc.Api/Timing/**`, `Http/RequestStages.cs`, `Identity/Caller.cs`, `Program.cs` (Row 1 rule 4);
  - every `Migrations/**` file and `AssessmentDbContext.cs` (N-2 is a test; N-3 is not this round);
  - `HpsmPoc.Modules.Reporting.Tests/**`, EXCEPT `NarrativePipelineTests.cs` (+ a test-only helper beside it) for Row 1b, added by Friday;
  - `.github/workflows/**`;
  - settings (`appsettings*.json`);
  - `Reporting/BlobReportStore.cs` / `IReportStore`;
  - every other seat's worktree, kit, container or port, including your own old `.tools/wt-b203*`, `.tools/wt-b206*` and `b206-*` (leave them).

## SUITES AND REPORT
- The full API suite on SQLite with your Azurite (all 5 projects, 0 skipped).
- The Hosting, import, persistence and contract classes on your SQL Server 2025.
- vitest `contract-drift`, typecheck, lint and build only if a web or contract file changed.
- gitleaks over `46da436..<final>`.
- A raw scan of the added lines with Python (not BSD grep, B205 N-4).
- Known flakes (HPSMPOC-247 `ImportRobustnessTests.R2_2`; the narrative B170 test above) are re-run alone and reported, never skipped.

## HOLDS (verbatim from B206, then this round's)
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)).
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert. **Friday opens the PR, and merges once CodeQL and the checks are green.**
- No deploy, no Azure, no setting change; nothing to HP or any human.
- Never delete; quarantine. **Never delete a file.**
- Never print a secret.
- Scoring/priorities unchanged (industry ruling a). No real revenue, no HP data feed, no HP partner id. No AI narrative touches the preview.
- Stop any process of yours by port + cwd (check its working directory first); never by name; never another seat's.
- No force-push of any kind, no branch delete, no history rewrite.
- No real customer export is used or requested; fixtures are synthetic (RFC 5737 / 3849 / 7042 documentation addresses, `SYNTH` serials).
- *(Added)* **Never edit a running script** (copy it, then edit the copy). **Your own worktrees only; never `gc`, `prune`, `worktree remove` or `reset` anything of another seat's** (or `2_Project_Files` itself).
- *(Added)* No Jira or BACKLOG write (Friday files and closes them). No re-run of a CI job to make it green.
- *(Added)* Files and rows stored before B213 are not changed.

## REPORT
`Briefs/2026-10-11_B213_STATUS.md`:
- **BLUF:**
  - main at start and end;
  - the Row 1 property in your words, the bound change, and the number that justifies it;
  - the M2 detection threshold at base and head;
  - the class result alone and under load, on both providers;
  - the Row-1-only sha;
  - the N-1 choice with the flag sentence;
  - the N-2 result under Td1 / Td2;
  - N-5 done;
  - N-3 / N-4 NOT done, and why.
- **FOUND:** Row 1 item 1, including the six quoted failures; the distribution tables; the B195 ADDENDUM-2 answer, or "not found"; anything else.
- **TESTED:** a red-first log for every new or changed test; each mutant red, then restored EQUAL; suites as above, with counts.
- **HOW:** commits, each with its files; every bound before and after.
- **NOT TESTED:** honestly. Every UNKNOWN names why it is unknown and the instrument that would close it.
- **PRIOR WORK:** file:line at `46da436`; `BACKLOG.md:24-29`; the Jira search (queries and hit counts).
- **NEW WORDS:** every user-visible string as string · where · why: the N-1 refusal text if (R), any contract prose, and the README sentence (docs).
- **Records:** containers left, worktrees, ports free at the end by `lsof`, the lock free.
- Last line exactly `READY FOR GATE: b213/timing-bounds-import-followups <sha>` (sha from `ls-remote` after your last push), or `STOPPED: NEEDS FRIDAY` and ONE question.

## UNKNOWN at draft time (why, and what closes each)
- **Where B195 answered ADDENDUM-2** (its 20-run distribution, if one exists). No B195 STATUS is in `Briefs/`, and the drafter did not search history or evidence folders. Closed by `grep -rl` over `Briefs/` and `5_Project_History/` (WHERE THIS COMES FROM).
- **The cause of class L (1 ms under) and class U (stalls).** The drafter read only logs and code, and ran no test. Closed by Row 1 items 1–2.
- **Whether the timing product code adds real time.** Not measured. Closed by M2 at base vs head; a defect there is a STOP (rule 4).
- **Why `%PDF-` is tested before the extension (B172 R2-6).** The drafter did not read B172's records. Closed by `git log -S` and the B172 brief or STATUS (N-1).
- **Whether the N-1 choice needs contract prose, and which version rule applies.** Not read. Closed by your reading of `openapi.yaml` and `PROVENANCE.md`.
- **Ports 6870–6879 free at your start; main unmoved; `.tools/.git-lock` free.** These were read at 08:33–08:36Z only. Closed by your `lsof`, `ls-remote` and `ls` re-checks.
