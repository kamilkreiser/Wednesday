STARTABLE: NO until Tuesday fills the 11 four-underscore lines (S1, S2, S5, S6, S10 values, S11, S14, S15, S16, S17 and the READ-WHOLE line), re-reads `branches/main` = `009421a2`, and confirms that no other `Datasec/HPSM-POC-D*` pane is open. S14 and S16 are REQUIRED choices (see Q-1, Q-2). After that the kit is YES.

# B1466 DRAFTER REPORT: SEAT-D59, HPSM-POC UAT deploy of main `009421a2` WITH the ledger migration

**Files (written by this drafter; this replaces the dead B1466 drafter's work, which left no files):**
- Words: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1466_WORDS-FOR-KAM.md` (written first)
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1466_SEAT-D59_hpsmpoc-uat-deploy-main-migration.md`
- This report.

Line counts and sha256 are in the final message to Tuesday (taken after the last edit).

## BLUF
- **TARGET did not move.** `branches/main` = `009421a28616c8b31dde86b59d4c4ca674c288fa` at 19:58:59 AEDT. CI is green and the artifacts are live:
  - run `42773429652`: 17 success, 1 skipped (dependency review), all 3 SQL Server legs success;
  - CodeQL `42773429155`: success;
  - open alerts 0 (control: `fixed` 1);
  - deploy artifacts expire 2026-11-17.
- **Your five landings are right at source, with one correction to the ORDER.** #305 (`78d4b3ce`) landed FIRST, directly on `6b0c5f2c`; #304 (`22116082`) is second. The rest are as you wrote: #306 `7da797e8`, #307 `eb2e49c7`, #308 `009421a2`. 5 commits, 46 files.
- **The migration is ONE appended transaction in TARGET's CI-made `assessment.sql`** (`03f1afb3...`). It is PREV's script plus 94 lines, guarded by the history id `20261110003228_LedgerAuditAndFollowUpRetention`, with `THROW 50117` on any row mismatch. `feedback.sql` is PREV's byte for byte. The migration's own tests passed on SQL Server in CI (LedgerAuditTests 4, FollowUpRetentionPurgeTests 11).
- **How UAT's database is migrated (at source, twice on record):**
  - the product owner's `az` login is in the SQL Entra admin group `sg-hpsmpoc-sql-admins` and runs as `dbo`;
  - go-sqlcmd `-b` with `ActiveDirectoryDefault` applies the CI package's own `.sql`;
  - this needs ONE temporary /32 firewall rule, because the server admits Azure services only (B410; B1234);
  - **go-sqlcmd is not installed on this machine, and the earlier schema kits (`.tools/b1234`, `b410`, `b221`) are not on this volume.** The kit has the seat download the exact v1.10.0 asset (digest matches B410) and write its schema instruments fresh, rehearsed first on a local SQL Server container.
- **Two points the source does not settle, so I made them stamp slots instead of guessing:**
  - **S16, deploy to a stopped API?** No record shows `az webapp deploy` working on a stopped site. Every UAT deploy on record ran on started sites, and B410 attempt 2 started the sites first. The script also waits for "Site started" and reads Kudu afterwards.
    - My recommendation is `A`: stop the API, back up, migrate, run the identity script, START the API (PREV code, on the new schema, for about 2 minutes), then deploy.
    - The seat must first prove at PREV source that no multi-row audit save is reachable on UAT. Reset and erase are 403 there; the feedback dispatcher is off.
  - **S14, the backup:** a database copy taken right after the stop (provable by snapshot equality; new spend until someone deletes it) plus the point-in-time facts; or point-in-time only (no spend, no tested restore).
- **I would not start this before S14 and S16 are decided.**

## Facts re-measured (all read-only; clocks from `date`, 19:58:27-20:06 AEDT 2026-11-10)
- **Main and range:**
  - `gh api -X GET branches/main` = `009421a2...` (19:58:59).
  - The scratch clone with the project deploy key (push URL disabled) shows HEAD = the same.
  - `git log 6b0c5f2c..009421a2`: 5 commits, one parent each. `git diff --stat`: 46 files, +7788/-105.
- **PR map** (`commits/<sha>/pulls`, 19:59:18):

  | Squash | PR | Head | Merged (Z) |
  |---|---|---|---|
  | 78d4b3ce | #305 | 792c78f2 | 04:23:18 |
  | 22116082 | #304 | d49be881 | 05:00:48 |
  | 7da797e8 | #306 | 4aff7ec4 | 05:35:30 |
  | eb2e49c7 | #307 | c16f422e | 06:15:29 |
  | 009421a2 | #308 | aa9bac75 | 07:10:20 |

  Open PRs: 0.
- **Gates** (first lines of `tuesday/briefs/2026-11-10_B14xx_verify*/VERDICT.md`):
  - B1441 GO WITH FINDINGS @ 792c78f;
  - B1440-2 GO WITH FINDINGS @ fc90f07 (round 1: NO GO @ 1cbd4cd);
  - B1464 GO WITH FINDINGS @ 4aff7ec;
  - B1442 GO WITH FINDINGS @ c16f422;
  - B1463 GO WITH FINDINGS @ aa9bac7.

  **#304 landed one commit past its gate.** `compare fc90f07...d49be881`: ahead 1, 1 file, `PartnerDashboard.alias.test.tsx` (a test). The only Major is B1442 M1, the deploy order, which the kit is built on.
- **CI** (19:59:41-19:59:57):
  - run `42773429652` completed/success, 18 jobs as above;
  - CodeQL `42773429155` with 4 Analyze jobs, all success;
  - artifacts `deploy-web-009421a2...` 16,559,601 B and `deploy-api-...` 49,716,398 B, `expired=false`;
  - open code-scanning alerts 0 / control `fixed` 1;
  - the SQL Server `.trx` (downloaded by GET; counted with python): LedgerAuditTests Passed 4; FollowUpRetentionPurgeTests 11; FeedbackLedgerInsertTests 1; no failed test.
- **TARGET api package** (artifact downloaded by GET):
  - MANIFEST `commit` = TARGET; `api.zip` `1fd65b62...` (122 files);
  - `assessment.sql` `03f1afb36b5cb4261a5932f64da8a38b360a75e719fdff5bdccc25591b9e1bb5`, whose `diff` against PREV's is one hunk `1576a1577,1670`;
  - `feedback.sql` `2a587ac2...` = PREV's.
- **Source facts used by the kit:**
  - the UAT SQL admin group and its object id: `infra/env/uat.bicepparam:9-11`;
  - the database: serverless GP_S_Gen5 2, Local backup redundancy (`infra/modules/sql.bicep:66-71`); autoPauseDelay -1 (`uat.bicepparam:24`);
  - the runbook's rule, apply and identity steps: `infra/README.md:73-105`;
  - "re-run api-identity.sql after the migration": `infra/README.md:234-235` and `api-identity.sql:23`;
  - the new DENY line: `api-identity.sql:49`;
  - the AppIdentity on UAT is `id-api-hpsmpoc-uat` (`main.bicep:68` with prefix `:55`; B410 `:149`);
  - `MigrateOnStartup` true only in `appsettings.Development.json:13`;
  - the purge is registered nowhere; the dispatcher only when the route is not Off (`FeedbackModule.cs:96`);
  - the M1 probe route is `listFollowUps` (`AssessmentModule.cs:274`).
- **The way back (code):**
  - `.tools/b1460/target/` holds PREV's packages: web `e012f1a8...` 16,544,207 B and api `621662df...` 49,630,930 B (2115 / 122 files; MANIFEST commit = PREV); RUN `42717134381`;
  - PREV's artifacts read `expired=false` and expire 2026-11-16T23:13-23:15Z (20:00);
  - **`rollback1460uat.sh` rolls back to `884fd72b` and must NOT be used.**
- **Tools:**
  - `sqlcmd` absent; `dotnet` at `.tools/dotnet`; `docker` present (daemon unmeasured);
  - go-sqlcmd v1.10.0 `sqlcmd-darwin-arm64.tar.bz2` digest `e08fc8f6a884...0ca204` (GitHub API) = B410's;
  - the binary's sha256 `d4ce6c00...` is relayed from B1234's kit `:62`.
- **Ports and panes:**
  - 9970-9979 LISTEN 0 (control 13);
  - panes `%0 wednesday`, `%2 Datasec/Security-Composer-R205`, `%1 fleet-monitor`: no HPSM-POC pane (note: `%0` is named `wednesday` now);
  - load1 4.84.
- **Authority** (`0_Brain/dashboard/data/decisions.json`, read with python):
  - `hpsmpoc-uat-deploy-five-landings-1110` ruled `a` at 19:40:52 AEDT ("Deploy all five to UAT now, with the database update"; "backup first");
  - `hpsmpoc-retention-migration-1110` ruled `a` at 09:04:11;
  - the terminal line "go ahead and deploy to UAT" is RELAYED from you, not read.
- **Visible change list** (for WORDS-FOR-KAM): sidebar label `GlobalNav.tsx:44`; Demo alias (`PartnerDashboard.tsx:66-69`, `EngagementOverview.tsx:143`); logo link `AppShell.tsx:172`; Roadmap sentence `RoadmapScreen.tsx:86` (read by eye: my quote-extractor does not see JSX text, and the kit makes the seat's extractor read it).

## How the kit differs from B1460
1. **The migration window, PART M:**
   - platform backup facts;
   - stop the API;
   - open the rule; take snapshot S0 and T0;
   - the copy, proven equal by snapshot (S14);
   - apply TARGET's `assessment.sql` once, plus one re-run that must apply nothing;
   - S1 must show exactly the migration (history +1, ledger type 3, audit rows n = n = n, the column with 0 values);
   - `api-identity.sql` with the read-back (DENYs on both audit tables);
   - close the rule; then start and deploy per S16.
2. **New write classes, all named:** the API stop and start, the copy, one temporary rule (plus one for the read-back), the SQL apply and the identity script. The B1460 holds ("no SQL statement", "no restart") are replaced by exact allowances.
3. **A three-case way back** (`rollback1466uat.sh`):
   - **RB-0**, before the apply: start the API, nothing else.
   - **RB-2**, the apply refused: the transaction rolled back; prove it by snapshot and start the API.
   - **RB-1**, after the apply: your order, re-sequenced so no deploy meets a stopped site: deploy PREV's packages, stop the API, swap the database back by two renames (or a point-in-time restore and two renames), set autoPauseDelay -1, start, run PREV's `api-identity.sql`, live-check.

   `Down` is never used. Each case is stub-run.
4. **A local SQL Server rehearsal** (CI's image) of the exact apply with the same go-sqlcmd and flags, with controls: the ledger refuses an UPDATE with Msg 37359, and a planted change fails the comparator. Without it, STOP before the window.
5. **The live checks change their focus:**
   - the sidebar label, line count and height on every level;
   - the Demo alias count (real names shown to Demo, compared in memory, never written);
   - the logo link height;
   - **the M1 probe:** `GET .../follow-ups` must be 200 on the new code;
   - a SELECT-only schema read-back after the deploy (S2).

   B1460's readiness, caveat and Recent-activity readers stay as regression checks.
6. **PART F is reduced** to counts plus the items newer than B1460's 11:04:40 read.
7. **Carried B1460 fixes:** template-literal words, the empty-state test without the panel, the favicon pair allowed BY NAME, the backtick panes regex, no `pgrep -f`, no `rm`.
8. **Clock:** 150 min hard stop and 180 DONE (B1460: 120/150), plus an API DOWN LIMIT before the apply (S17).
9. **Main moved past TARGET at Step 0 = STOP** (B1460 allowed a later descendant), because a later commit could add another migration.

## Stamp slots (recommended values)
- **S1:** your stamp line (`date`; the kit read whole with its `wc -l`; CI and `branches/main` re-read).
- **S2:** the terminal line verbatim with its clock; the card `hpsmpoc-uat-deploy-five-landings-1110` ruled `a` 19:40:52; the card `hpsmpoc-retention-migration-1110` ruled `a` 09:04:11; whether the product owner saw WORDS-FOR-KAM.
- **S5:** `42773429652` (CodeQL `42773429155`).
- **S6:**
  - #305 `792c78f2` B1441 F1-F3 Minor, F4-F5 Info;
  - #304 `d49be881` (gated `fc90f07` + 1 test commit) B1440-2 G1 Finding, G2-G3 Minor;
  - #306 `4aff7ec4` B1464 F1-F3 Minor, F4-F5 Info;
  - #307 `c16f422e` B1442 M1 Major (carried as this kit's order), m1-m3 Minor, i1-i2 Info;
  - #308 `aa9bac75` B1463 1-4 Minor, 5 Info.
- **S10:** (a)-(h) CONFIRMED. (d) needs your word on an HP review session and the down time. (g) is the temporary SQL rule. (h) is the local container.
- **S11:** `UAT WORDS: THE CLOSED LIST OF D-8, READ BY THE PRODUCT OWNER`, once he has seen WORDS-FOR-KAM (or `HOLD`).
- **S14:** `COPY AND POINT-IN-TIME` (Q-1).
- **S15:**

  > On every signed-in page and level, the sidebar entry for /assessments reads "Playbook Partner Readiness" on two lines (link about 56 px, rows below about +12 px vs BEFORE) at 1440 x 900 and in the 390 x 844 drawer; the readiness hub as Partner keeps h1 "Playbook Partner Readiness", eyebrow "My readiness", first panel "Playbook Partner Readiness: current statements" with 16 statements in 4 areas, Start x1, runs list equal to BEFORE; at Demo level, real customer names shown on Home Upcoming = 0 and the overview "Customer name" row shows the alias; the header logo link is 44 px tall at 390 and 1440.

  The 56/+12 figures are B1463's local measurement at 1280 x 800 / 1024 x 768, not at 1440: the seat reports SEEN values.
- **S16:** `A: START PREV THEN DEPLOY` (Q-2).
- **S17:** `30`.
- **READ-WHOLE:** your line.

## Questions for Tuesday (each with a default)
- **Q-1 (S14, spend):** a database copy as the backup (new serverless database `hpsmpoc-b1466-pre`, auto-pause 60, billed until someone deletes it; the way back is two renames), or point-in-time only (no spend; restore time NOT MEASURED, never tested). The card said "backup first"; a copy is the only backup that can be shown to exist before the migration. **Default: COPY AND POINT-IN-TIME.**
- **Q-2 (S16, order):** `A` (start PREV on the migrated schema, then deploy at once) versus `L` (deploy to a stopped API, unproven on this platform). **Default: A**, gated by the seat's source proof (D-13).
- **Q-3:** the copy is made AFTER the stop (so it holds every row) and the platform facts BEFORE. That is a small re-reading of "backup first, then stop". **Default: as written.**
- **Q-4:** `api-identity.sql` runs right after the migration, before the start (m1 only needs "after the migration"). This shortens the rule's open time and the DENY gap on the new table. **Default: as written** (the order given was "after start").
- **Q-5:** the copy database and any renamed database are never deleted by the seat. Who decides that, and when?

## STOP conditions (do not start, or the seat stops)
- `branches/main` is not `009421a2` at the stamp or at Step 0. Do not retarget: a later commit may hold another migration.
- S14 or S16 missing or not exact; or the product owner has not seen the words (S11 HOLD).
- An HPSM-POC deploy pane is open, or UAT is not on `6b0c5f2c` (BUILD_ID `q9tnDMDG__k92hFNCyYJ1`, deployments `9f0f95f4`/`2091f096`).
- Any write in the activity log since 2026-11-09T23:50:28Z; the database not Online / -1; the firewall not exactly `AllowAllWindowsAzureIps`; a database other than `hpsmpoc`/`master` on the server.
- The SQL login is not `dbo`/`db_owner`; any authorization refusal on stop, copy, rule or SQL.
- go-sqlcmd digest mismatch; docker or the CI image unavailable (no rehearsal).
- PREV's packages unproven, or its artifacts expired (2026-11-16 23:13Z).
- For S16 = A: a PREV save path reachable on UAT that writes two or more audit rows in one save.
- Fewer than 90 minutes to the cut-off at Step 0.

## NOT MEASURED (by the drafter)
- Everything hosted:
  - whether UAT still runs `6b0c5f2c`; the settings; the activity since B1460; the database state;
  - the number of audit rows; the current migration history (B1234 last read Assessment 17 / Feedback 3 on 3 Nov);
  - the backup retention today.

  No `az`, no SQL and no HTTP to any hosted host were used.
- Whether `az webapp deploy` works on a stopped App Service site (the S16 question). One web search found only a forum report of "403 – This web app is stopped" for a push to a stopped app: not Microsoft documentation, not relied on.
- How long `az sql db copy`, a point-in-time restore, or `az sql db rename` take for this database. Whether a rename works with the API stopped and the web up. The exact `az sql db copy` flags for serverless (the kit has the seat read `-h` and stub them).
- Whether `PREV`'s API starts cleanly on the migrated SQL Server schema (`FirstVisitWarmup` writes and rolls back at start). The rehearsal tries it if the seat can boot the API against local SQL Server.
- The sidebar wrap at 1440 x 900 (B1463 measured 1280 x 800, 1024 x 768, 820 drawer, 390 drawer).
- Which UAT page shows the Roadmap register sentence.
- Whether the docker daemon is running; whether go-sqlcmd v1.10.0's archive still extracts to the binary with sha256 `d4ce6c00...` (relayed from B1234).
- `launch_when_cool.sh` and `brief_seat.sh` paths: relayed from B1460's kit, not re-listed. The model-routing lines: relayed from B1460.
- The terminal ruling "go ahead and deploy to UAT" (~18:1x): relayed by you. The card I read is ruled at 19:40:52.

## Outside-the-fences disclosure
- **Used:**
  - `gh api -X GET` under the HPSM-POC `GH_CONFIG_DIR`: branches, commits/pulls, compare, runs, jobs, artifacts, code-scanning alerts, pulls, and the public go-sqlcmd release;
  - **GET downloads of three artifacts** (deploy-api of TARGET; the two SQL Server test-result artifacts) into my scratchpad;
  - one `git clone` of the project repo with the project deploy key into my scratchpad (push URL disabled);
  - one web search (the stopped-site question).
- **Not used:** `az`, `sqlcmd`, docker, HTTP to any hosted host, any write verb on git or GitHub, `cd`, `rm`.
- **Reads only inside `!CODING`:** Briefs STATUS/kit files; `.tools/` listings, `shasum` and MANIFEST reads of `.tools/b1460/`.
- **Two Bash calls were refused by hooks before running:** an unquoted `=====` separator (zsh), and a redirect through `$D/..`. Both were re-run in a correct form; neither ran as refused.
- **Scratch:** `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/90f78cba-aa68-4adc-98aa-7d2087ff2f7f/scratchpad/b1466/` (`repo/`, `art-api/`, `trx-a/`, `trx-o/`, `gh/`).
- `0_Brain/learnings/_ledger.md` was not read. No mail, no PR, no Jira.
