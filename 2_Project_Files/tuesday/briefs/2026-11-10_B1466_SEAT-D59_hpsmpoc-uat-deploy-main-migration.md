From Tuesday (the product owner's Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail channel from this project). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`.
# BRIEF B1466 - SEAT-D59: HPSM-POC: deploy main at `TARGET` (#304-#308) to the hosted UAT review copy ONLY, WITH the one database migration in the same window: BACKUP the UAT database, STOP the API, apply `LedgerAuditAndFollowUpRetention` to the UAT database only, deploy the web AND API packages by the project script, START the API, re-run `infra/sql/api-identity.sql`, then live checks as seen (read-only), a schema read-back, and a read-only feedback count

**STARTABLE: NO until Tuesday has (1) filled every four-underscore slot (S1, S2, S5, S6, S10, S11, S14, S15, S16, S17 and the READ-WHOLE line: 11 lines), (2) re-read `branches/main` = `TARGET`, and (3) confirmed that no `Datasec/HPSM-POC-D*` pane is open. After that the kit is YES.**

In this brief **`TARGET`** = `009421a28616c8b31dde86b59d4c4ca674c288fa` (**`T8`** = `009421a2`), the squash of #308 on main. **`PREV`** = what UAT web AND API run now = `6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb` (**`PREV8`** = `6b0c5f2c`). This is **RELAYED, NOT MEASURED NOW** from the last line of `Briefs/2026-11-10_B1460_STATUS.md:319` (`DEPLOYED B1460: 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb <the UAT web address>`) and its FOR TUESDAY 1 (`:271`). **What B1460 recorded:**
- Deployed 10:48:22-10:50:27 AEDT 2026-11-10 (2026-11-09T23:48:22Z-23:50:27Z) by `scripts/deploy-from-ci.sh`.
- Active deployments: web `9f0f95f4-b621-4b9a-b5ff-96487f3aabb3`, API `2091f096-3755-4c39-b0cc-8636ddd16240`. Web `.next/BUILD_ID` `q9tnDMDG__k92hFNCyYJ1`. CI run `42717134381` (CodeQL `42717132328`).
- Packages: web `e012f1a8b15fc0e3da73f12a2de9541e9d6dedc8c6811b338c6251be764283e2` (16,544,207 B, 2115 files), API `621662df3bc93fc40bf708549f1f5bf12fcd678e227bc31cdfe685e2e6d18d43` (49,630,930 B, 122 files). Live-check AFTER: web 2115/2115, API 122/122, site-only 0. Wwwroot sha256 AFTER: web `3cd2e208c0578c94bfab2b6bc41266a6bd1aa15dfa8ec6617b4cfbe3d6a4a534`, API `ff854767a12c8aa2491acbf217e471fc3a1ac459f5e812e8df1a2258ffe3762b`.
- New containers: web `23:49:10.4920898Z Site started.`, API `23:50:06.7104657Z Site started.`, on images `node:24-lts_20261027.8` and `dotnetcore:10.0_20261027.8`.
- PART P PASSED; watchdog `WINDOWS PASSED t+922`; no rollback; **no schema step** (`assessment.sql` `8a4084b6...e220c`, `feedback.sql` `2a587ac2...d3c3`).

**Whether UAT still runs `PREV` is UNMEASURED by the drafter** (no `az`, no HTTP to any hosted host). The instruments are REFUSE 2 and PRE-DEPLOY SIGNAL 3. **If UAT is not on `PREV` (a different BUILD_ID or active deployment id): STOP, because someone else deployed.** The deploy-STATUS listing (`/usr/bin/grep -l -E '^(DEPLOYED|ROLLED BACK|PARTIAL)' 'Briefs/'*STATUS.md | tail -4`) read at 20:00 AEDT, newest last: B1307, B1391, B1454, B1460.

**Drafter's own measurements (MEASURED, read-only).** All by `gh api -X GET` under the project `GH_CONFIG_DIR`, and a scratch clone made with the project deploy key (push URL disabled). Clocks are from `date`, 19:58:59-20:06 AEDT 2026-11-10.
- `branches/main` = `009421a28616c8b31dde86b59d4c4ca674c288fa` (19:58:59). Open PRs: 0 (19:59:57).
- `git log PREV..TARGET`: **5 commits, each with one parent; 46 files, +7788/-105** (`git diff --stat`):

| Commit | Parent | PR | PR head (merged) | Gate first line | Subject |
|---|---|---|---|---|---|
| `78d4b3ce` | `6b0c5f2c` | #305 | `792c78f2` (04:23:18Z) | `GATE B1441: GO WITH FINDINGS @ 792c78f on main 6b0c5f2` | "API: refuse invisible-only customer names; file names fold width and space only" |
| `22116082` | `78d4b3ce` | #304 | `d49be881` (05:00:48Z) | `GATE B1440-2: GO WITH FINDINGS @ fc90f07 on main 6b0c5f2` (round 2; round 1 `GATE B1440: NO GO @ 1cbd4cd`) | "Web: header logo link 44 px, Demo alias on Home and customer details, register rule line, mock blank-name rule" |
| `7da797e8` | `22116082` | #306 | `4aff7ec4` (05:35:30Z) | `GATE B1464: GO WITH FINDINGS @ 4aff7ec on main 6b0c5f2` | "Walkthrough test: presenter-note row catches approve it, score this, saving and submit; exemption is step 6 exact phrase" |
| `eb2e49c7` | `7da797e8` | #307 | `c16f422e` (06:15:29Z) | `GATE B1442: GO WITH FINDINGS @ c16f422 on main 6b0c5f2` | "Audit ledger table on SQL Server and follow-up contact retention purge (HPSMPOC-117, HPSMPOC-100)" |
| `009421a2` | `eb2e49c7` | #308 | `aa9bac75` (07:10:20Z) | `GATE B1463: GO WITH FINDINGS @ aa9bac7 on main 2211608` | "Web: the sidebar link reads Playbook Partner Readiness" |

  - Gate verdicts are the first lines of `tuesday/briefs/2026-11-10_B14{41,40,64,42,63}_verify*/VERDICT.md`. #304's is `2026-11-10_B1440_verify_r2/VERDICT.md`. **The project `Briefs/` STATUS files of these lanes are BUILDER files, not gates.**
  - **#304 landed one commit past its gate:** `compare fc90f07...d49be881` reads ahead 1, behind 0, and 1 file, `web/src/components/partner/PartnerDashboard.alias.test.tsx` (a test path; MEASURED 19:59:37). The seat proves it again.
  - **Every other PR landed at its gated head** (#305 `792c78f`, #306 `4aff7ec`, #307 `c16f422`, #308 `aa9bac7`).
  - **Majors:** B1442 **M1 Major**. It is about the deploy ORDER, not the code; this kit is built on it. Every other gate: Minor, Note or Info only (by the `| <id> | <sev> |` rows of each VERDICT).
- **CI at `TARGET`** (19:59:41-19:59:57):
  - push run `ci` **`42773429652`** completed/success (2026-11-10T07:10:23Z-07:28:32Z). 18 jobs: 17 success and 1 skipped (`dependency review (pull requests; blocks on high/critical)`). The success jobs include `api (ASP.NET Core)`, **`api on SQL Server (api-assessment)`, `api on SQL Server (api-other-and-feedback)` and `api on SQL Server`** (3 of 3), `infra (Bicep validate)`, `secrets (gitleaks, full history)`, `web build (...)`, `web unit tests (vitest)` and `web (Next.js)`, plus 8 `web e2e` shards (prototype-tablet-1/-2, prototype-desktop-2, playbook-desktop-1/-2, playbook-mobile-1/-2, journey-and-prototype).
  - `Push on main` (CodeQL) **`42773429155`** completed/success, with 4 Analyze jobs (actions, python, csharp, javascript-typescript) all success.
  - Open code-scanning alerts on main: **0** (control: state `fixed` reads 1).
  - Artifacts read `expired=false`: `deploy-web-009421a2...` id 13743995311, 16,559,601 B, expires 2026-11-17T07:24:32Z; `deploy-api-009421a2...` id 13743691759, 49,716,398 B, expires 2026-11-17T07:26:23Z.
  - **The migration's tests ran on SQL Server in CI** (artifacts `api-sqlserver-test-results-api-assessment` and `...-api-other-and-feedback` downloaded by GET; counted with python over the `.trx`): `LedgerAuditTests` Passed **4**; `FollowUpRetentionPurgeTests` Passed **11**; `FeedbackLedgerInsertTests` Passed **1**; names containing `Hpsmpoc99Tests.N7` Passed 6. Totals: Passed 1,431 / 1,348, no other outcome. No failed test in either file. A no-such token was counted alongside and read 0.
- **TARGET's api package, downloaded by GET** (`actions/artifacts/13743691759/zip`, into the drafter's scratchpad):
  - `MANIFEST.json`: `commit` = `TARGET`; run `42773429652` attempt 1; `api.zip` `1fd65b623d3665568e50a2615d25d3f4e5936880355a4f93a1f2e65dc574f9ec` (49,644,626 B, 122 files, entry time 2026-11-10T07:26:14Z).
  - **`assessment.sql` `03f1afb36b5cb4261a5932f64da8a38b360a75e719fdff5bdccc25591b9e1bb5`** (64,330 B). It differs from PREV's `8a4084b6...` ONLY by one appended block: `diff` reads `1576a1577,1670`, 94 added lines and 0 changed. **That block is ONE batch and ONE transaction** (`BEGIN TRANSACTION;` `:1577` ... `COMMIT;` `:1668`, `GO`). Every statement is guarded by `IF NOT EXISTS (... [MigrationId] = N'20261110003228_LedgerAuditAndFollowUpRetention')`. In order:
    1. `ALTER TABLE [poc].[follow_up] ADD [contact_purged_at] datetime2(3) NULL` (`:1583`);
    2. `sp_rename` of `audit_event` to `audit_event_pre_ledger`, plus its PK, CHECK and two indexes;
    3. `CREATE TABLE [poc].[audit_event] ... WITH (LEDGER = ON (APPEND_ONLY = ON))` (`:1616`);
    4. two indexes, one filtered;
    5. the row copy with `IDENTITY_INSERT` and a reseed;
    6. `THROW 50117` unless both tables hold the same rows (`:1656`);
    7. the history row `(N'20261110003228_LedgerAuditAndFollowUpRetention', N'10.0.12')` (`:1665`).
  - **`feedback.sql` `2a587ac2824755f12d3e03f0dde768d3414e89e91c9ad85ac2b4f612b135d3c3` = PREV's**, so there is no Feedback migration.
- **Scope:**
  - The schema regex `Migrations|Persistence|\.sql$` over the 46 paths reads **12**: the two migrations, their designers, both model snapshots, `AssessmentDbContext.cs`, `Entities.cs`, `FollowUpEntities.cs`, `LedgerSafeSqlServerUpdateSqlGenerator.cs`, `FeedbackDbContext.cs`, and `infra/sql/api-identity.sql`.
  - Paths matching `^(\.github|scripts)/|package.*\.json|\.csproj|appsettings`: **0** (grep rc 1). So `scripts/deploy-from-ci.sh` and `scripts/deploy-package.py` are PREV's.
  - `infra/` paths: `infra/README.md` and `infra/sql/api-identity.sql`, neither deployed by the script.
- **Nothing in the range runs a migration on its own:**
  - `Assessment:MigrateOnStartup` is `true` only in `api/src/HpsmPoc.Api/appsettings.Development.json:13` (grep over `appsettings*.json`). B1460 read the UAT setting as absent.
  - The purge is registered nowhere: no `AddHostedService` and no caller outside its own file (grep over `api/src`).
  - `FeedbackDispatchService` is registered only when the route is not `Off` (`FeedbackModule.cs:96`).
- **The local tools:**
  - `sqlcmd` is NOT installed on this machine (`which`: not found). No earlier schema kit is on this volume: `.tools/b1234`, `b1273`, `b410` and `b221` are absent (`ls`).
  - go-sqlcmd v1.10.0 release asset `sqlcmd-darwin-arm64.tar.bz2` is 22,179,473 B, digest `sha256:e08fc8f6a884140fbeda29ac82fecad8e71548892381e6e572a82eda7b0ca204` (`gh api -X GET repos/microsoft/go-sqlcmd/releases/tags/v1.10.0`, 20:04:09). It equals B410's `e08fc8f6…` (`Briefs/2026-10-21_B410_STATUS.md:58`). The binary inside measured `d4ce6c0040ef3eee0ece719afabdc6d8060f0354609db1aefd4390f314dfe2aa` in B1234 (`Briefs/2026-11-03_B1234_SEAT-D45_...md:62`).
  - `dotnet` is at `.tools/dotnet` (via `.tools/env.sh`). `docker` is at `/usr/local/bin/docker`; whether its daemon runs is UNMEASURED. Machine `arm64`.
- **The way back (code), MEASURED 20:00:03:** `.tools/b1460/target/` holds `PREV`'s two packages: web.zip `e012f1a8...` 16,544,207 B and api.zip `621662df...` 49,630,930 B; `assessment.sql` `8a4084b6...`; `feedback.sql` `2a587ac2...`; both `MANIFEST.json` `commit` = `PREV` (2115 / 122 files); `RUN` = `42717134381`. `.tools/b1460/repo` HEAD = `PREV`. PREV's CI artifacts read `expired=false` and expire **2026-11-16T23:13:43Z / 23:15:22Z** (api / web; 19:59:57). **`rollback1460uat.sh` is NOT this run's way back:** it rolls back to `884fd72b`.
- Ports 9970-9979: `lsof` LISTEN **0** at 20:05:04 (control: all listeners 13). The `997[0-9]` word-boundary scan over today's SEAT kits hits B1391 (D56), B1450, B1454 (D57) and B1460 (D58), all ended. Panes at 20:05:04: `%0 wednesday`, `%2 Datasec/Security-Composer-R205`, `%1 fleet-monitor`; **0 HPSM-POC panes**. load1 4.84.
- `.tools/b1466` absent (`ls` fails). In `tuesday/briefs/`, no `SEAT-D59` file and no `B1466` file existed before this drafter's three files.

**Fact marks.** MEASURED = this drafter, read-only, as above. RELAYED = quoted from a named file. UNMEASURED = nobody ran it. **Source beats this brief: re-measure at source, and say in STATUS (Corrections) where they disagree.**

## WHAT THIS KIT IS (read first)
1. **The new part is the database.** #307 adds one Assessment migration on SQL Server: the audit table becomes an append-only LEDGER table (the old one is kept with its rows as `poc.audit_event_pre_ledger`), and `follow_up` gains `contact_purged_at`. **Gate B1442 finding M1 (Major; `tuesday/briefs/2026-11-10_B1442_verify/VERDICT.md:82`) makes the order FIXED:**
   - TARGET's API on the OLD schema breaks every follow-up read ("Invalid column name 'contact_purged_at'", probe P1).
   - PREV's API writing two or more audit rows in one save to the NEW ledger table fails with Msg 37359.
   - So: stop the API, migrate, deploy, start, then re-run `api-identity.sql`.
   - **The builder's `## FOR THE DEPLOY` in `Briefs/2026-11-10_B1442_STATUS.md` (step 1, "Deploy that API build. It runs on the old schema.") is WRONG. Never follow it.** Its SELECT read-backs (steps 2 and 4) are reused here.
2. **The fixed order, as this kit runs it (Tuesday's order; slot S16 settles the one point the source does not):**
   - **M1** BACKUP the UAT database and PROVE the backup exists (slot S14);
   - **M2** STOP the UAT API;
   - **M3** run the migration on the UAT database ONLY;
   - **M4** re-run `infra/sql/api-identity.sql` (AFTER the migration, m1);
   - **M5** START the API and deploy both packages by the project script (S16 says in which order);
   - then live checks AS SEEN, the schema read-back, and PART F.

   **How M1 and M2 interleave (drafter's reading; Tuesday may restamp):**
   - M1's platform backup facts (point-in-time window, retention) are read and checked BEFORE M2.
   - M1's copy, its proof and the restore point T0 are taken right AFTER M2's stop, so the backup holds every row the API wrote; nothing writes during the copy.
   - The migration (M3) never starts before BACKUP PROVEN.

   **The migration's `Down` NEVER runs on a hosted database** (m2). The way back is the M1 backup.
3. **Who runs the migration, and how (MEASURED at source, `infra/README.md:73-105`, and as UAT has done it twice).** The UAT SQL server is Entra-only. Its admin is the group `sg-hpsmpoc-sql-admins` (`infra/env/uat.bicepparam:9-11`), and the project's interactive `az` login (the product owner's account) is in it. It applies the scripts as `dbo`:
   - B410 (UAT stand-up, `Briefs/2026-10-21_B410_STATUS.md:137-153`): `assessment.sql` and `feedback.sql` with go-sqlcmd `-b`, ActiveDirectoryDefault, whoami `dbo`, then `api-identity.sql` with `AppIdentity=id-api-hpsmpoc-uat`;
   - B1234 (UAT, 3 Nov, `Briefs/2026-11-03_B1234_STATUS.md:114-149`): one Feedback migration by the CI package's own `feedback.sql`, a restore point, two equal snapshots, one temporary /32 rule open 17 s and closed by `trap`, and a refusal poll.

   **This kit applies `TARGET`'s CI-made `assessment.sql`** from the verified api package (digest `03f1afb3...`), with go-sqlcmd and `ActiveDirectoryDefault`. It never runs a laptop-built bundle and never runs `feedback.sql` (it is PREV's byte for byte, so there is nothing to apply).
4. **THE SQL FIREWALL admits Azure services only** (`AllowAllWindowsAzureIps`). The seat's machine reaches the database only through ONE temporary /32 rule. This is the README's own step (`infra/README.md:90-91`, `:102`) and B1234's D-4. It is a `[PROD-CLASS]` access write that S7 names.
5. **The backup (slot S14; MEASURED at source):**
   - The UAT database is serverless `GP_S_Gen5` capacity 2, `requestedBackupStorageRedundancy: 'Local'` (`infra/modules/sql.bicep:66-71`), autoPauseDelay -1 (`infra/env/uat.bicepparam:24`).
   - **Point-in-time restore** is the platform's own backup. B1234 read 7-day retention, a 12 h differential and no long-term retention (`B1234_STATUS.md:115`). A restore makes a NEW database; it cannot restore in place.
   - **Drafter default S14 = `COPY AND POINT-IN-TIME`.** After the API is stopped (so nothing writes), the seat makes ONE database copy `hpsmpoc-b1466-pre` on the same server (`az sql db copy`; serverless, autoPauseDelay 60, Local backup redundancy). It proves the copy exists by snapshot equality with the source. It also records the restore point T0 and the platform's `earliestRestoreDate` as a second way.
   - The copy is a new billed database until someone deletes it. This seat never deletes it.
   - **`POINT-IN-TIME ONLY`** makes no copy and takes no new spend. The "proof" is then the platform facts only, never a tested restore, and a way back waits for a restore of unknown length (NOT MEASURED).
6. **Five landings, of which these are visible on UAT** (words: `tuesday/briefs/2026-11-10_B1466_WORDS-FOR-KAM.md`, read WHOLE):
   - **(S) the sidebar label** "My readiness" -> "Playbook Partner Readiness" on every signed-in page, every level (`GlobalNav.tsx:44`). It wraps to two lines (link 44 -> 56 px; rows below +12 px; collapsed rail unchanged), per B1463's local wrap table (`tuesday/briefs/2026-11-10_B1463_verify/wrap-table.txt`, RELAYED).
   - **(D) Demo alias:** at the Demo level, Home "Upcoming activity" and the customer overview's "Customer name" row show the alias (#304, HPSMPOC-410; B1440-2 crawl: 6 real names before, 0 after).
   - **(L) Header logo link** min-height 44 px (`AppShell.tsx:172`; layout only).
   - **(G) Roadmap register sentence** (`RoadmapScreen.tsx:86`). Where UAT shows it is UNMEASURED.
   - **Not visible:**
     - (N) invisible-only customer names refused, 422 `customer.name-blank` (#305; never exercised on UAT: a write);
     - (F) feedback file-name fold (#305; an upload: never on UAT);
     - (X) the ledger and the idle purge (#307);
     - (T) #306, a test only.
7. **Authority (RELAYED by Tuesday; the drafter read the card, not the terminal).**
   - **Terminal:** in the Tuesday terminal ~18:1x on 2026-11-10, the product owner, verbatim: **"go ahead and deploy to UAT"**.
   - **Card `hpsmpoc-uat-deploy-five-landings-1110`, ruled `a` at 2026-11-10T19:40:52+11:00** (`0_Brain/dashboard/data/decisions.json`, read by the drafter with python): "Deploy all five to UAT now, with the database update". Option detail: "One deploy seat, backup first, the update in the same window, then a live check of what you will see; told to you after." Its BLUF says "the deploy stops the API, applies the update to the UAT database, deploys, and starts it again (a few minutes down)".
   - **Card `hpsmpoc-retention-migration-1110`, ruled `a` at 2026-11-10T09:04:11+11:00:** "Allow the one migration (gated, not deployed)".
   - **UAT ONLY. Never production, never the demo** (`hpsm-poc-rg`, `hpsm-poc-demo-rg`, `hpsm-poc-sm-rg`: never even read).
   - **This lifts the UAT hold for THIS deploy ONLY** (slot S13).
   - A correction arrives as `B1466_ADDENDUM-*.md` in `tuesday/briefs/`. Read each one whole before the first `az` call and again before M2. One that changes the site, the sha or the order is a STOP until Tuesday restamps.
8. **Template and what carries over.** The last executed, PASSED UAT deploy is B1460:
   - its kit `tuesday/briefs/2026-11-10_B1460_SEAT-D58_hpsmpoc-uat-deploy-main.md` (636 lines; read WHOLE);
   - its record `Briefs/2026-11-10_B1460_STATUS.md` (319 lines; read WHOLE, especially Corrections 1-7, FOR TUESDAY 5 (c)-(f) and NOT TESTED).

   **Inherited from B1460 unchanged unless this kit says otherwise:**
   - the identity pass before EVERY `az` call;
   - plain ARM GETs, never `az webapp show`;
   - the PRE-DEPLOY SIGNALS and the settings-hash compare;
   - D-5 (the database stays awake), D-6 (platform image), D-11 (the non-GET list), D-12 (readiness runner/results pages equal), D-14 (the review door), D-15 (no PDF), D-16 (customer counts 4/5/5/4 and the id-set hash);
   - the walk router that ABORTS and counts every non-GET other than D-11's named calls, and aborts GET prefetches of `/admin/feedback(/review)` outside PART F;
   - the STATUS-first-line discipline; no names in STATUS; no message to any human.

   **B1460's own fixes ARE carried:**
   - the words extractor reads `${...}` template literals (FOR TUESDAY 5 (c));
   - the walker's empty-state test excludes the walkthrough panel's text (5 (d));
   - **the favicon route-cache pair (`.next/server/route-cache/APP_ROUTE/<hash>/$/favicon.ico.{body,meta}`) is ALLOWED BY NAME as web site-only in the BEFORE live-check** (5 (e); any other site-only file = STOP);
   - the local seed's readiness run is on the current package, so the lead-with-current panel is NOT APPLICABLE locally (5 (f));
   - the panes regex reads "No \`az\`" with a backtick (Corrections 1).
9. **WHERE THE INSTRUMENTS ARE (MEASURED by `ls` and `shasum` at 20:00):**
   - `.tools/b1460/` holds D58's working set. The sha256 prefixes: `identity_pass1460.sh` `0d79a986`, `presig1460.py` `d97fc5c6`, `live1460.py` `37520de8`, `walk1460.cjs` `08fe7e77`, `cmpwalk1460.py` `7a0ee151`, `words1460.py` `8f61de80`, `partf1460.cjs` `929cce72`, `deploy1460.sh` `574120fd`, `rollback1460uat.sh` `55981253` (to `884fd72b`: NOT ours), plus `pkgcmp1460.py`, `lits1460.cjs`, `pairseed1460.py`, `webpair1460.py`, `cfgkeys1460.py`, `closedlist1460.py`, `statusnow.py`, `stub/`, `repo` (HEAD = `PREV`) and `target/` (`PREV`'s packages, above).
   - **The seat COPIES what it needs by name into `.tools/b1466/`** (read-only source; `cmp` each copy). It renames each to a `1466` name, hand-edits every hex, sha, BUILD_ID, window start and count map (never by `sed`), and runs each copy's plant control before relying on it. It never writes into `.tools/b1460/`.
   - **NEW in this kit (written by the seat; none exists on this volume):** `sqlget1466.sh`, `rule1466.sh`, `snap1466.sql` with `snapcmp1466.py`, `schema1466.sh`, `rollback1466uat.sh`, `sqlrehearse1466.sh`, and the go-sqlcmd copy `.tools/b1466/bin/sqlcmd`.

**What the product owner approved, and what is NOT covered.**
- **Covered:**
  - the database backup of S14;
  - `az webapp stop`/`start` of the UAT **API** only (M2, M5);
  - ONE temporary /32 SQL firewall rule, opened late and closed by `trap` (plus at most one more for the AFTER read-back, P3 (n), and one in a way back);
  - `TARGET`'s `assessment.sql` applied ONCE to `hpsmpoc` on `sql-hpsmpoc-uat-25onzn`, plus ONE idempotent re-run that must apply nothing;
  - `TARGET`'s `infra/sql/api-identity.sql` with `AppIdentity=id-api-hpsmpoc-uat` (idempotent);
  - SELECT-only reads of that database;
  - the CI packages of `TARGET` to the two UAT apps by the project script;
  - read-only live checks;
  - the way back (D-7);
  - PART F's read-only feedback count.
- **NOT covered:**
  - `[PROD-CLASS]` any other SQL statement: no `feedback.sql`, no `Down`, no `UPDATE`/`DELETE`/`INSERT` by hand, no `sp_verify_database_ledger`, no digest upload;
  - `[PROD-CLASS]` any other database, server, group or subscription (the copy `hpsmpoc-b1466-pre` excepted);
  - `[PROD-CLASS]` a template deploy or what-if; any app-setting, vault, plan, access or other firewall write; any web-app stop or restart other than the deploy's own;
  - any hosted-data reset, re-seed or demo-data change; any feedback item created, approved, deleted or moved; any narrative or readiness self-assessment on UAT;
  - deleting anything (the copy stays, and a way back's renamed database stays: Tuesday's later decision);
  - anything after `TARGET`;
  - anything to HP or to any human.

**Closed-list proof of what reaches UAT** (re-measured by the seat at Step 0; property first, then "at least these", then "any other shape: prove it or STOP").
- *Property:*
  - every commit in `PREV...TARGET` is on main, has one parent, and was merged by a PR the seat prints with its number, head and gate verdict line;
  - every product path's blob at `TARGET` equals the blob at the head of the PR that changed it (a path shared by two PRs equals the LATER PR's head);
  - 0 blob paths differ between `PREV` and `TARGET` outside the union of the PRs' files;
  - **schema paths are exactly the 12 above**, and the ONLY migrations are `20261110003228_LedgerAuditAndFollowUpRetention` (SqlServer) and `20261110003229_LedgerAuditAndFollowUpRetention` (Sqlite, local only) (`git diff --name-only -- '*/Migrations/*'`; control: `compare a3a06b9a...69338b64` lists the ReviewHeldState migration);
  - `TARGET`'s `assessment.sql` = PREV's plus exactly the one appended transaction block (`diff`: one `a` hunk after PREV's last line, 0 `c`/`d` hunks; control: a planted one-character edit to a scratch copy of PREV's lines reads a `c` hunk); `feedback.sql` digests are equal;
  - no `.github/`, `scripts/`, `package*.json`, `*.csproj` or `appsettings*` path;
  - every `infra/` path is `infra/README.md` or `infra/sql/api-identity.sql`, and `api-identity.sql` differs from PREV's by exactly the `audit_event_pre_ledger` DENY line plus comment lines (print the diff);
  - NEW configuration keys read by added product lines: listed. Expected: `FollowUp:ContactRetentionMonths` only, read by the unregistered purge, so NOT required. A new REQUIRED key = STOP.
- *At least these:* the 5 commits above and their 46 paths.
- *Controls:*
  - a planted extra path reads 1 differing;
  - a planted `Migrations/` path not in the list fails the migration rule.
- **Any other shape** (a 6th commit, a second migration, a Feedback migration, a changed `deploy-from-ci.sh`): STOP and list it.

**CI at `TARGET`.** The pass predicate is the script's (`scripts/deploy-from-ci.sh:49`; print it with `grep -n -i`).
- The push run `ci` of `TARGET` (slot S5) is `completed/success`, with ALL THREE `api on SQL Server` legs success (a skipped leg = STOP: this range has a SQL Server migration), `infra (Bicep validate)` success, and every `web e2e` shard success.
- `Push on main` (CodeQL) success. Open code-scanning alerts on main 0 (control: `fixed` >= 1).
- The migration's tests passed on SQL Server: `LedgerAuditTests` Passed >= 4, Failed 0; `FollowUpRetentionPurgeTests` Passed >= 11 (from the two `api-sqlserver-test-results-*` artifacts by GET; control: a no-such token 0).
- Artifacts `deploy-web-<TARGET>` / `deploy-api-<TARGET>` read `expired=false`.
- Never re-run CI; never dismiss an alert.

**Identity and tenant (workspace rule 4; records, not assumed).** RELAYED from `B1460_STATUS.md:115`:
- `IDENTITY PASS ... sub=a6b8fe11-d1b5-4293-8727-b34aba08a705 tenant=ec01829b-fdcb-4503-9834-eb2ffbd99169 name='Azure subscription 1' user=...@datasec-rd.com`;
- `AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.azure'`; `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config'`;
- which of the five Datasec environments this tenant is: NOT ASSERTED.

Rules:
- **`identity_pass1466.sh` (a `cmp`-checked copy of `identity_pass1460.sh`) runs before EVERY `az` call AND before EVERY `sqlcmd` call** (go-sqlcmd's ActiveDirectoryDefault reads the same `az` login; export `AZURE_CONFIG_DIR` explicitly in each SQL command). Control: `AZURE_CONFIG_DIR=/nonexistent` fails rc 2.
- `4_Credentials/.azure-sp` is never opened. An expired interactive login = STOP and ask.
- **Any authorization error is the boundary working: STOP and report it.** That includes `az sql db copy`, rename, `firewall-rule create` and a SQL login refusal other than the expected firewall refusal. Never `az account set`, never work around it, never ask for a broader right.
- **Never `az webapp show`.** The project script's own live-check line (`deploy-from-ci.sh:89`) is the only exception.
- **SQL identity proof before the first statement:** `SELECT USER_NAME(), IS_MEMBER('db_owner')` must read `dbo` and `1` on `hpsmpoc` (B410/B1234). Anything else = STOP, rule closed.

**CLOCK.** Hard stop = Step 0 + 150 minutes (slot S3), written by you as an absolute AEDT clock at Step 0. No write START after it (M1's copy, M2's stop, the rule, the apply and the deploy each count). DONE no later than Step 0 + 180 minutes. Step 0 within 45 minutes of slot S1.
- **API DOWN LIMIT (slot S17, default 30 minutes)** runs from M2's stop.
  - If the limit is reached BEFORE M3's apply has started: abort by RB-0 (D-7). The schema is untouched, so close the rule, start the API on `PREV`, then `STOPPED`.
  - After M3 has started, there is no abort: finish forward or take RB-1.
- CHECKPOINT lines with `date`, in this order: Step 0 | CI green | package checks | rollback point taken | local pair | SCHEMA REHEARSED | DATABASE STILL AWAKE (before) | UAT BEFORE walk | API STOPPED | BACKUP PROVEN | SCHEMA APPLIED | IDENTITY SCRIPT RUN | TEMP RULE CLOSED | API STARTED | UAT deploy START | PART P PASSED | SCHEMA READ-BACK | DATABASE STILL AWAKE (after) | PART F DONE | DONE. At every CHECKPOINT print the minutes left to the write cut-off and, between API STOPPED and API STARTED, the minutes of API down.
- A write that has started is not killed. A way back that must start, starts within 60 s.
- **If anything is in doubt BEFORE M2, leave UAT as it is and end `STOPPED: NEEDS TUESDAY <reason>`.** Between M2 and M5, "in doubt" means RB-0 if M3 has not started, and RB-1 if it has.

**Model route.** Opus, `BRIEF_SEAT_LEVEL=opus`, model id `claude-opus-5-5`. RELAYED from B1460's kit `:169`: `fleet/specs/model-routing.md` row C6 "Deploy". STATUS quotes the `brief_seat: model=` line or says none was shown. **Never run /model in this pane.**

**This phase builds no integration with HP tools.** UAT feedback delivery is OFF (`Feedback__Route` `off`; re-read at Step 0). This seat sends and approves nothing.

## DRAFTER DECISIONS (D-n; Tuesday accepts or changes them at the stamp; the defaults apply if Tuesday is silent, except where a slot is REQUIRED)
- **D-1: PIN `TARGET`.** At Step 0, `gh api -X GET branches/main` must equal S4. If main later moves past `TARGET`, deploy `TARGET` anyway and record it. **S4 not 40-hex, or `TARGET` not a descendant of `6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb`: STOP at once.** If main at Step 0 is NOT `TARGET` (a later commit), STOP: a later commit could carry another migration (the drafter did not measure one).
- **D-2: The write classes, all named, in this order only:**
  - (w1) S14's copy;
  - (w2) `az webapp stop` (API);
  - (w3) the temporary rule create/delete;
  - (w4) the `assessment.sql` apply and its one re-run;
  - (w5) `api-identity.sql`;
  - (w6) `az webapp start` (API);
  - (w7) the project script's two `az webapp deploy` lines (`deploy-from-ci.sh:68-69`);
  - (w8) the D-7 way back if it fires.

  Nothing else: `[PROD-CLASS]` no what-if, no `az deployment`, no `az sql db update` except inside D-7, no app-setting, vault, plan or access write.
- **D-3: Both packages, through the project script** (web, then API). The API restarts with NEW code (#305 VisibleText, #307 ledger-safe inserts and the new mapping). Whether an HP reviewer is in session is UNMEASURED; Tuesday states it in S10 (d).
- **D-4: The temporary SQL rule.**
  - ONE rule `b1466-schema-20261110` for this machine's /32. The address is taken from Azure SQL's own refusal text (no third-party host; B410/B1234 method) and never printed (`<ip>`).
  - Create it AFTER M2 is confirmed; delete it by `trap` on ANY exit of `schema1466.sh`.
  - The rules list after must equal the before list exactly (`AllowAllWindowsAzureIps` only; control: the during-list differs).
  - A refusal poll (read-only `SELECT 1` every ~30 s) records the first refusal after the delete. B1234 measured 5 min 29 s; it runs in the background and never blocks M5.
  - **P3 (n) may open ONE more rule, `b1466-read-20261110`,** for the AFTER read-back, under the same `trap` and poll.
  - Firewall writes total: at most 2 creates + 2 deletes (+1 pair in a way back).
- **D-5: THE DATABASE STAYS AWAKE.**
  - RELAYED baseline, B1460 W5 (`B1460_STATUS.md:230`): `status` Online, `autoPauseDelay` -1, `useFreeLimit` False, `pausedDate` None, `GP_S_Gen5` capacity 2, `minCapacity` 0.5, `maxSizeBytes` 34359738368; `databases/pause` since 2026-11-01T00:52:35Z **0** (control window 2026-11-01T00:24:13-00:52:00Z: 2).
  - Read before the window and after PART P. Any difference = STOP before the next write.
- **D-6: Platform-image rule, both UAT apps, as B1460 D-6.** The baseline is the Step 0 reading. RELAYED: web `NODE|24-lts` / `node server.js`; API `DOTNETCORE|10.0` / empty command line; images as above; active deployments `9f0f95f4-...` (web) and `2091f096-...` (API).
- **D-7: THE WAY BACK (three cases; `rollback1466uat.sh`, written at BUILD 5, stub-run, never run unless a case fires).**
  - **RB-0 (before M3's apply has started: a copy too slow or unproven, the API DOWN LIMIT reached, an identity or SQL login problem, an addendum):**
    1. delete the rule (the `trap`);
    2. `az webapp start` the API (it is `PREV`'s code on the untouched schema);
    3. wait for `/health` 200 and `/health/ready` 200;
    4. end `STOPPED: NEEDS TUESDAY`.

    No code deploy has happened. The copy (if made) stays.
  - **RB-1 (after M3 has committed, any slot-S9 class or a deploy failure; Tuesday's order, re-sequenced so that no `az webapp deploy` meets a stopped site, see D-13):**
    1. `az webapp deploy` `PREV`'s two packages from `.tools/b1466/rollback/<PREV>/` (web, then API), `--type zip --async false --clean true`. The API is running, so PREV's code lands on a started site;
    2. `az webapp stop` the API;
    3. **the database back from M1's backup:**
       - COPY form: `az sql db rename -n hpsmpoc --new-name hpsmpoc-b1466-migrated-<UTC stamp>`, then `az sql db rename -n hpsmpoc-b1466-pre --new-name hpsmpoc`, then `az sql db update -n hpsmpoc --auto-pause-delay -1` (D-5's value; the copy was made at 60);
       - PITR form: first `az sql db restore -n hpsmpoc --dest-name hpsmpoc-b1466-rb --time <T0> --edition GeneralPurpose --compute-model Serverless --family Gen5 --capacity 2 --min-capacity 0.5 --auto-pause-delay -1 --backup-storage-redundancy Local`, then the same two renames with `hpsmpoc-b1466-rb` in place of `hpsmpoc-b1466-pre`;
    4. `az webapp start` the API;
    5. the rule `b1466-rb-20261110` (`rule1466.sh`, `trap`), then **`PREV`'s `infra/sql/api-identity.sql`** (from `repo-rb`; it has no `audit_event_pre_ledger` line, so it runs on the restored pre-migration database), then delete the rule;
    6. snapshot = M1's backup snapshot (history Assessment 17 with no `LedgerAuditAndFollowUpRetention` row; `audit_event` NON_LEDGER; `contact_purged_at` absent);
    7. live-check against `PREV`'s packages (web 2115, API 122), BUILD_ID `q9tnDMDG__k92hFNCyYJ1` x1;
    8. D-5 (autoPauseDelay -1 on the renamed-in database);
    9. `ROLLED BACK`.

    **Rows written between T0 and the rollback are lost.** The API was stopped from T0 to M5, so the loss is only what UAT wrote after M5 (sign-in rows, audit rows of the walks). Say so in STATUS.
  - **RB-2 (M3 failed or THROW 50117): the transaction rolled back by itself.**
    1. prove it by snapshot = M1 (history unchanged; `audit_event` NON_LEDGER, rows equal; `audit_event_pre_ledger` absent; `contact_purged_at` absent);
    2. delete the rule;
    3. `az webapp start` the API on `PREV`;
    4. `STOPPED`. No code deploy, no restore.

  **`rollback1466uat.sh` guards before ANY `az` call:**
  - `repo-rb` HEAD = `PREV` (rc 96);
  - `PREV`'s zip sha256 `e012f1a8...` / `621662df...` (rc 97);
  - the group is exactly `hpsm-poc-uat-rg`, the server starts `sql-hpsmpoc-uat-`, and the database names are exactly `hpsmpoc` and the S14 backup name (rc 95);
  - FORM is `COPY` or `PITR` and T0 is a UTC minute (rc 94);
  - the identity pass before each `az` call (rc 2).

  **The migration's `Down` is never part of any way back** (m2). `rollback1460uat.sh` (to `884fd72b`) is NEVER run.
- **D-8: THE WORDS GATE (a closed list by STRING).**
  - *Property:* every customer-facing string that is new or changed on UAT is one of the strings in `tuesday/briefs/2026-11-10_B1466_WORDS-FOR-KAM.md` (as Tuesday amends it), each at the `file:line` written there, re-printed at `TARGET`.
  - *At least these (MEASURED by the drafter, 20:03-20:06):*
    - `GlobalNav.tsx:44` label "Playbook Partner Readiness" (CHANGED from "My readiness", `PREV:44`);
    - `RoadmapScreen.tsx:86` "Verified complete and Evidence submitted need an evidence reference. The reference is not checked independently." (CHANGED from "Verified complete needs an evidence reference. ...", `PREV:86`);
    - `CustomerEndpoints.cs:81`/`:202` "name is blank." (existing words, new trigger);
    - `customer-detail.ts:28` "name is blank." (mock only);
    - `FollowUpRetentionPurge.cs:48`, `:50`, `:107` (server-only, purge not registered);
    - `LedgerAuditAndFollowUpRetention.cs:74`/`:89` (the THROW texts; SQL only);
    - `EngagementOverview.tsx:143` "Customer name" (existing label, now conditional).
  - **The drafter's extractor misses plain JSX text** (it read `RoadmapScreen.tsx:86` by eye). Use `words1466.py` = a copy of `words1460.py` (template literals read). Run it over the ADDED and REMOVED lines of every product path, plus a JSX-text pass (text between `>` and `<` on added lines). Plant first: a phrase planted as JSX text into an in-memory copy of `RoadmapScreen.tsx`'s diff must be listed OTHER, rc 1.
  - **Any new customer-facing string not in WORDS-FOR-KAM = STOP before any hosted write**, listed with its `file:line`.
  - STATUS lists EVERY new or changed string (file, `file:line` at `TARGET`, string, OLD text). Underscore-aware person-name scan as B1460 D-8 (tokens from `.tools/b1390/scripts/drive.mjs:90`, read in-process, never printed; control `_by_<name>_` fires).
- **D-9: One attempt; a way back ends the run.**
- **D-10: Jira and records: this seat writes none.** STATUS lists the Jira keys the squash subjects and PR titles name (MEASURED: #307 names HPSMPOC-117 and HPSMPOC-100; the others name none in the subject).
- **D-11: No data written on UAT by the seat's own actions,** as B1460 D-11. The only non-GET calls to UAT web/API are the sign-in POSTs, the sign-out POSTs and the two refused probes (403 `uat.action-off`), all COUNTED.
  - Never click "Start a self-assessment".
  - Never create, rename or delete a customer: (N) is proven locally and in CI only.
  - Never open a feedback page's controls.
  - **SQL: SELECT only, except M3's apply and re-run, M4's `api-identity.sql` and D-7's.** `sqlget1466.sh` refuses any text with `INSERT|UPDATE|DELETE|MERGE|ALTER|CREATE|DROP|EXEC|GRANT|DENY|TRUNCATE` (rc 2; plant controls `UPDATE` and `SELECT 1; DELETE ...` each rc 2).
- **D-12: Readiness and every signed-in page: the differences are confined.**
  - Read BEFORE and AFTER, as B1460 D-12/D-13 (R), at 1440 x 900 and 390 x 844.
  - **Allowed AFTER differences:**
    - (1) the sidebar entry for `/assessments`: its label, link height, line count and the vertical offset of the rows below it, on EVERY signed-in page and level;
    - (2) at the **Demo** level only: Home "Upcoming activity" names and the customer overview's "Customer name" row;
    - (3) the header logo link's box height (layout only; no text);
    - (4) the Roadmap register sentence wherever a page shows it.
  - Everything else equals BEFORE (status, h1, visible text after removing the sidebar label, customer counts and id-set hash), including the readiness hub's H1 "Playbook Partner Readiness", eyebrow "My readiness", first panel, runs list and the D-12 runner and results pages.
  - Any other difference = STOP with the text diff (slot-S9 classes roll back).
- **D-13: S16, the window order (REQUIRED; Tuesday writes one value).** The drafter could not settle this point at source.
  - The fixed order says deploy (4), then start the API (5).
  - **No record shows `az webapp deploy` (Kudu OneDeploy) succeeding on a STOPPED site. Every UAT deploy on record ran on started sites.** B410 attempt 2 started both sites first (`B410_STATUS.md:488`, "Started both sites").
  - The deploy script waits for "Site started successfully" (`--async false`, `deploy-from-ci.sh:68-69`) and then reads each site's Kudu `wwwroot` (`:76-97`).
  - A public forum note reports "Error 403 – This web app is stopped" for a file push to a stopped app (UNVERIFIED, not Microsoft documentation).
  - **Value `A: START PREV THEN DEPLOY` (drafter's recommendation):**
    - M2 stop; M1 backup; M3 migrate; M4 `api-identity.sql`; rule closed; **M5a `az webapp start` the API (still `PREV`'s code, now on the migrated schema)**; M5b `deploy-from-ci.sh deploy TARGET ...` at once (web, then API).
    - `PREV`'s code runs on the migrated schema from M5a to the API leg of M5b (B1460 took about 2 minutes for both legs).
    - What B1442 M1 says breaks there: a save adding two or more audit rows. The builder named three such saves: showcase/demo reset, GDPR erasure with stored reports, and a Feedback delivery that lost its lease (`B1442_STATUS.md` FOR THE DEPLOY).
    - On UAT, reset and erase answer 403 `uat.action-off` (B1460 measured the reset probe) and the dispatcher is not registered with the route off (`FeedbackModule.cs:96`).
    - **The seat proves at `PREV` source, before M2, that every PREV save path reachable on UAT with the switch on and the route off adds at most one audit row per save.** Do it by reading each `Audit.Add`/`AddRange` site (B1442's census: 16 files) and each one's guard. Any reachable multi-row save that is not refused on UAT = STOP before M2 (then only `L` is possible).
    - The start-up writes: `FirstVisitWarmup` "warmCallerWrite rolled back" (`AssessmentModule.cs:123`; the B1234 start line) and the seeder's "already in this database; nothing was written". The SCHEMA REHEARSAL (BUILD 7 (iv)) boots `PREV`'s API on the migrated local SQL Server database if the seat can, and records whether its start-up line appears with no Msg 37359. If it cannot boot the API against SQL Server locally, say so: NOT TESTED.
  - **Value `L: DEPLOY TO THE STOPPED API`:**
    - The literal order: M2, M1, M3, M4, then `deploy-from-ci.sh deploy` with the API stopped, then `az webapp start`.
    - If the API leg fails (non-zero exit after the web leg), the script stops under `set -e`: the web runs `TARGET` and the API is stopped on the migrated schema. Then: `az webapp start` the API (it runs `PREV`'s code on the migrated schema), and run the D-7 RB-1 way back. **No second deploy attempt.**
  - Any other S16 value: STOP before the first `az` call.
- **D-14: The review door is NOT re-tested and NOT broken** (B1460 D-14, status only).
- **D-15: No live PDF.**
- **D-16: Hosted data is not reset,** as B1460 D-16 (customers 4/5/5/4; id-set hash BEFORE = AFTER).
  - **The audit rows are measured, not just counted:** M1's snapshot `audit_event` COUNT_BIG and MAX(audit_id) must equal, after M3, BOTH `audit_event` and `audit_event_pre_ledger` (B1442 FOR THE DEPLOY step 4).
  - Every other `poc` table: count and `CHECKSUM_AGG(BINARY_CHECKSUM(*))` equal before/after M3 (the API is stopped, so there is no live traffic).
  - Exceptions: `follow_up`, whose checksum changes with the new column (compare count and a checksum over its PREV columns, named from `PREV`'s model snapshot); `dbo.__EFMigrationsHistory` +1 row; `poc.audit_event_pre_ledger` new; `poc.audit_event` new object with equal rows.
- **D-17: PART F, the UAT feedback store, READ-ONLY, after PART P PASSED.**
  - The B1460 D-17 procedure, router, controls and naming rules, exactly as `B1460 kit:262-284`.
  - Print only: the total, the counts by category and by state, the held count, and **the items newer than B1460's PART F read (2026-11-10 11:04:40 AEDT)** with the D-17 table for those items only.
  - No screenshot of either feedback page. `.tools/b1466/fb/*.json` mode 600, never in `Briefs/`.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, no other step; each count with a control that can fail)
- **FIRST STEP: the way back is reachable.**
  - Copy `PREV`'s packages from `.tools/b1460/target/{web,api,RUN}` by name, read-only, into `.tools/b1466/rollback/6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb/`.
  - `shasum -a 256` + `stat -f %z` must give web `e012f1a8b15fc0e3da73f12a2de9541e9d6dedc8c6811b338c6251be764283e2` (16,544,207 B) and API `621662df3bc93fc40bf708549f1f5bf12fcd678e227bc31cdfe685e2e6d18d43` (49,630,930 B), file counts 2115 / 122, both `MANIFEST.json` `commit` = `PREV`, `RUN` = `42717134381`, and `assessment.sql` `8a4084b6...` (MEASURED by the drafter on the source copy at 20:00).
  - If absent or unequal, rebuild by `scripts/deploy-from-ci.sh fetch PREV` from a clean clone at `PREV` (its artifacts expire 2026-11-16T23:13:43Z).
  - Digests unequal or artifacts expired: `STOPPED: NEEDS TUESDAY no proven way back`.
- **The last UAT deploy.**
  - `tail -n 1 'Briefs/2026-11-10_B1460_STATUS.md'` begins `DEPLOYED B1460: 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb` (control: a scratch file ending `DEPLOY B1466: PENDING` counts 0 for `^DEPLOYED `).
  - The deploy-STATUS listing names no UAT deploy newer than B1460.
  - **Which build is live (UNMEASURED by the drafter):** public `GET /` names `q9tnDMDG__k92hFNCyYJ1` x1, and the live trees equal `PREV`'s packages (web 2115/2115 with only the favicon pair allowed site-only; API 122/122, site-only 0). Any other build = STOP.
- **Panes.** As B1460 REFUSE 3 (with its Corrections 1 regex). It fires ONLY on another `Datasec/HPSM-POC-D*` pane, or any pane whose kit lets it call a hosted HPSM-POC host or `az`. At drafting (20:05:04) there were 0 HPSM-POC panes. Re-list immediately before M2 and before the deploy START.
- **The target.**
  - S4 is 40-hex and equals `branches/main` at Step 0 (D-1). S5 is numeric. S12 is exactly `305 304 306 307 308`.
  - For every PR in S12: `merged` true; `merge_commit_sha` on main's first-parent line in `PREV..TARGET`; `head.sha` printed; check-runs on the head all success (control: a no-such PR 404).
  - Gate verdict lines printed (`head -n 1` of the five VERDICT files above). Each must read `GO` or `GO WITH FINDINGS` at the head that landed, except #304 (gated `fc90f07`, landed `d49be881`). For #304, prove by `compare fc90f07...d49be881` that the extra commit touches only `web/src/components/partner/PartnerDashboard.alias.test.tsx`.
  - S6 carries each gate's open findings by id. B1442 M1 is carried as "the order of this kit". A Major in any gate's FINDINGS that S6 does not carry = STOP.
- **CI at `TARGET`.** As above; equal to S5 or another green run of `TARGET` (say which).
- **Stamp slots.**
  - `/usr/bin/grep -o -E '_{4}' <your copy> | wc -l` reads 0 (control: a five-underscore scratch file >= 1). The last line begins `READ-WHOLE-BY-TUESDAY: DONE`.
  - S7 is exactly `BACKUP FIRST; API STOPPED; ONE ASSESSMENT MIGRATION; API IDENTITY SCRIPT; BOTH PACKAGES; ONE TEMPORARY SQL RULE; NO WHAT-IF; NO TEMPLATE DEPLOY; NO APP SETTING WRITE; NO DATA RESET`.
  - S8 is exactly `UAT ONLY`.
  - S10 holds `CONFIRMED` for (a)-(h), with no `NOT CONFIRMED` and no `UNSET` in the VALUE part (count over the value part only; B1460 Correction (d)).
  - S11 is exactly `UAT WORDS: THE CLOSED LIST OF D-8, READ BY THE PRODUCT OWNER` or exactly `UAT WORDS: THE CLOSED LIST OF D-8, SENT TO THE PRODUCT OWNER BESIDE THE DEPLOY` (the second added by Tuesday at the stamp: his 2026-11-10 ~09:09 terminal ruling, verbatim "don't wait, deploy as soon as it's ready", read then as new strings going to him beside the deploy, not before it) (or `HOLD`: STOP at once).
  - S13 is exactly `UAT HOLD LIFTED FOR THIS DEPLOY ONLY: ACCEPTED`.
  - S14 is exactly `COPY AND POINT-IN-TIME` or `POINT-IN-TIME ONLY`.
  - S15 is filled with text.
  - S16 is exactly `A: START PREV THEN DEPLOY` or `L: DEPLOY TO THE STOPPED API`.
  - S17 is an integer from 15 to 45.
  - Anything else: STOP.
- **Clock.** Later than 45 min after S1, or fewer than 90 minutes to the write cut-off at Step 0: STOPPED ("not enough time").
- **Identity.** As above. PRIOR WORK is read WHOLE before the first `az` call.
- **Names, settings, route** (UNMEASURED today; RELAYED from B1460 PHASE 0 `:116`). All read in-process; print only yes/no or the name list.
  - Sites exactly {`app-hpsmpoc-api-uat-25onzn`, `app-hpsmpoc-web-uat-25onzn`}.
  - SQL server exactly `sql-hpsmpoc-uat-25onzn`. **Databases on it exactly {`hpsmpoc`, `master`}** (a leftover `hpsmpoc-b1466-*` = STOP).
  - SQL firewall exactly `AllowAllWindowsAzureIps`. **The server's Entra admin is the group `sg-hpsmpoc-sql-admins`, object id `c8f8b814-b85f-4b97-a390-cec81be1c64c`** (ARM GET `servers/<sql>/administrators`; = `uat.bicepparam:9-10`), and `azureADOnlyAuthentication` true.
  - Setting names API 35 / web 17. **`Feedback__Route` exactly `off`.** `Assessment__MigrateOnStartup` absent. `Assessment__Environment` and web `HPSM_ENVIRONMENT` exactly `uat`. `Auth__UatOpen__Enabled` `true`. `HPSM_DEMO_NOTICE` `off`. `HostedDemo__Seed__Enabled` true and `__OwnerObjectId` present.
- **Platform backup facts (read-only, before M2):** `earliestRestoreDate` at least 24 h older than now; short-term retention days (B1234: 7); LTR none; backup storage redundancy Local/Local (`az sql db show`, `az sql db str-policy show`, `az sql db ltr-policy show`; B1234 M1 method). Missing or younger than 24 h = STOP.
- **go-sqlcmd.**
  - Download `sqlcmd-darwin-arm64.tar.bz2` of `microsoft/go-sqlcmd` v1.10.0 (`gh release download` or a GET of the asset), into its own new empty directory `.tools/b1466/bin/dl/`.
  - The archive sha256 must be `e08fc8f6a884140fbeda29ac82fecad8e71548892381e6e572a82eda7b0ca204`; extract and copy the binary to `.tools/b1466/bin/sqlcmd`; its sha256 must be `d4ce6c0040ef3eee0ece719afabdc6d8060f0354609db1aefd4390f314dfe2aa` (B1234's).
  - Unequal = STOP. Never `brew install`; never write to `/opt/homebrew`.
- **Ports.** Block **9970-9979** (D58's, ended). Re-run `lsof` (expect 0) and the `997[0-9]` kit scan just before the first listener, and take the next free 10-block if a live claim appears. Not to use: 9940-9969, 9980-9999, 9520-9529, 9570-9599, 9680-9739, 9640-9649, 9670-9679, 9840-9849 (B1442 gate containers). Bind `127.0.0.1` only.
- **Live seats and trees.** `.tools/b1466` was absent at drafting (MEASURED); anything there you did not make: STOP. `.tools/b1460/` is read by name only.

## PRE-DEPLOY SIGNALS (UAT; read ALL before M2, and again before the deploy START and before any way back; `presig1466.py` = a copy of `presig1460.py`)
1. Both sites Running, HTTPS only, `alwaysOn` true; stacks as D-6 (plain ARM GET).
2. App-setting names, value hashes (in-process) and slot flags: API 35 / web 17. Summaries RELAYED from B1460 W4 = `fa62b3968883ca61` / `fe5590fba73ea35f` (comparable only with `h16` byte-unchanged: say so). KV references `Resolved`, except the two feedback webhook references `SecretNotFound` (pre-existing since B874).
3. Active deployments web `9f0f95f4-b621-4b9a-b5ff-96487f3aabb3`, API `2091f096-3755-4c39-b0cc-8636ddd16240` (RELAYED); none in progress.
4. Platform lines newer than B1460's containers (web 2026-11-09T23:49:10Z, API 23:50:06Z): none, except as D-6 allows.
5. The ARM activity log of the group since **2026-11-09T23:50:28Z** (after B1460's `DEPLOY END 23:50:27Z`), with BOTH `--start-time` and `--end-time`:
   - restart / stop / start / config-write / sites-write / deployment counts 0;
   - `publishxml/action` reads listed (B1460's own after-reads made 4);
   - SQL `databases/pause` since 2026-11-01T00:52:35Z 0;
   - SQL `firewallRules/write` / `/delete` 0;
   - SQL `databases/write` 0.

   Any write = STOP; list it.
6. Plan `asp-hpsmpoc-uat` P0v3 x1 with `LastError` empty; access rules; SQL firewall (1); vault secret names (2); resources (14); tags: equal to B1460 W5.
7. The database as D-5; the public page build (`q9tnDMDG__k92hFNCyYJ1` x1); no `B1466_ADDENDUM-*.md`.

**Rule:** any difference not covered by D-6 STOPS before the next write, listing EVERY differing signal.

## BUILD (one attempt; fix root causes, never skip; nothing hosted is written in BUILD)
1. **Step 0 and PHASE 0 (read-only).**
   - Run `date` and the clock arithmetic (hard stop and write cut-off as absolute AEDT), then the REFUSE checks in order.
   - Copy this brief unchanged into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/`; record `cmp`, both sha256s and the slot count.
   - **Write STATUS `1_Project_Definition/Briefs/2026-11-10_B1466_STATUS.md` right after Step 0:** first line `DEPLOY B1466: PENDING`, then a STATUS-NOW line kept current (step, next command, minutes to cut-off, API down minutes). Write no `DEPLOYED`, `ROLLED BACK`, `PARTIAL` or `STOPPED` line until you mean it.
   - Re-measure `compare PREV...TARGET` and print every commit with its PR and every path with its +/-.
2. **Clones (detached):**
   - `.tools/b1466/repo` at `TARGET` and `.tools/b1466/repo-rb` at `PREV`;
   - each from origin with the project deploy key by a per-command `-c core.sshCommand=...` (key never printed);
   - push URL `DISABLED-no-push`;
   - never a fetch, worktree or ref write in `2_Project_Files`; never a push.
3. **Fetch and prove `TARGET`'s packages.**
   - From `repo`: `scripts/deploy-from-ci.sh fetch TARGET` (rc 0). Quote both `OK ... package` lines, both `MANIFEST.json` `commit` = `TARGET`, and `RUN` (= S5).
   - The api package's `assessment.sql` = `03f1afb36b5cb4261a5932f64da8a38b360a75e719fdff5bdccc25591b9e1bb5` and `feedback.sql` = `2a587ac2...` (MEASURED by the drafter on the artifact); api.zip `1fd65b62...` (MEASURED: MANIFEST). Unequal = STOP.
   - **The appended-block proof** (Closed-list) and its control.
   - Record the new web `.next/BUILD_ID` (it must differ from `q9tnDMDG__k92hFNCyYJ1`).
   - Control: `verify --expect-run 42717134381` on `TARGET`'s packages fails.
   - The migration's CI test counts (CI above).
   - `CHECKPOINT CI green`.
4. **Package checks, `TARGET` vs `PREV`, property first** (`pkgcmp1466.py`, `lits1466.cjs`; copies of the `1460` ones with their maps hand-edited; plant controls first).
   - **Web:**
     - page routes added 0, removed 0;
     - `node_modules/` 0 differences;
     - static/public equal;
     - the differing files are chunk, app and build-id files only;
     - `lits1466` UNEXPLAINED 0 both ways (the `encryptionKey` manifest classed by hand, redacted);
     - "Playbook Partner Readiness" control present in BOTH;
     - the RoadmapScreen sentence: `TARGET`'s >= 1 / 0 and `PREV`'s 0 / >= 1;
     - a test-only string from `PartnerDashboard.alias.test.tsx` reads 0 in the web package.
   - **API, the property "every HpsmPoc DLL may carry code; every non-DLL/PDB file is EQUAL":**
     - 122 = 122 files expected (STOP on any other count);
     - `appsettings.json`, `*.runtimeconfig.json`, `*.deps.json` and `SeedContent/` EQUAL (no new package or setting);
     - `HpsmPoc.Modules.Assessment.dll` `#US` holds `followup.contact-purged` x1 / x0 and `HPSMPOC-117: ` x1 / x0 (UTF-16LE; control: "name is blank." x1 / x1);
     - `HpsmPoc.Modules.Reporting.dll` and `HpsmPoc.Modules.Rules.dll`: 0 unnamed runs (stamp-only; the range touches neither: an unnamed run there = STOP);
     - every `TARGET` DLL embeds `T8` x1 and `PREV8` x0.
   - `CHECKPOINT package checks`.
5. **The way back, proven and not run.**
   - `PREV`'s packages per REFUSE line 1. `verify --expect-commit PREV --expect-run 42717134381` rc 0 (control: `--expect-run 42773429652` fails).
   - Download the BEFORE wwwroots read-only (as `live1460.py` did). The live-check against `PREV`'s packages must be equal (only the favicon pair allowed site-only on the web).
   - **Write `rollback1466uat.sh`** (D-7: RB-0, RB-1 and RB-2 as sub-commands `rb0`, `rb1`, `rb2`; FORM and backup name read from S14; T0 written by `schema1466.sh` into `.tools/b1466/db/restore-point.txt`, read by the script, never typed).
     - Guards as D-7. Each `az` write is preceded by the identity pass.
     - The SQL step uses `rule1466.sh` + `sqlget1466.sh`'s write-enabled sibling for the one named file only.
   - **Stub run** (a scratch `PATH` `az` and `sqlcmd` that answer `account show` with the records' identity and log every other argv), for `rb0`, `rb1 COPY`, `rb1 PITR` and `rb2`:
     - the argv names `hpsm-poc-uat-rg`, `sql-hpsmpoc-uat-25onzn`, `hpsmpoc`, the S14 backup name, the two UAT sites, and `PREV`'s zips;
     - **`rb1`'s first `az webapp deploy` comes BEFORE its `webapp stop`;**
     - `TARGET`'s sha or zips appear 0 times; `Down`, `feedback.sql` and any `delete` verb appear 0 times.
   - Stub controls: the HEAD check with `repo` (= `TARGET`) gives rc 96 with 0 calls; zips pointed at `TARGET`'s gives rc 97 with 0 calls; a group `hpsm-poc-rg` gives rc 95 with 0 calls.
   - `CHECKPOINT rollback point taken`.
6. **Instruments.**
   - Copy by name + `cmp` from `.tools/b1460/` (read-only), rename to `1466`, hand-edit: `identity_pass`, `presig`, `live`, `pkgcmp`, `words`, `lits`, `walk`, `cmpwalk`, `pairseed`, `webpair`, `deploy`, `statusnow`, `cfgkeys`, `closedlist`, `partf`, `pfplant`. List which.
   - **New behaviour in `walk1466.cjs` / `cmpwalk1466.py`:**
     - (a) **the sidebar reader:** at every signed-in page, level and width, the `/assessments` link's text, its box height, its line count (`getClientRects().length` of the label's text node range), and the next row's top; on the collapsed rail at 1440 too, if the seat can reach it by GET-only navigation (a click on the collapse control is NOT allowed, so say so if it cannot);
     - (b) **the Demo alias reader:** at the Demo level, Home "Upcoming activity" row names and the sample customer's overview "Customer name" row. Compared IN PROCESS against the set of real customer names that the Partner's `GET /api/v1/customers` returns, kept in memory, never written: count of real names shown to Demo BEFORE and AFTER (expected AFTER 0) and whether the row is present;
     - (c) **the header logo link height** at 390 and 1440 (expected AFTER 44);
     - (d) the B1460 readiness, (C) caveat and (A) Recent-activity readers kept as regression checks (all EQUAL BEFORE/AFTER now);
     - (e) `cmpwalk` allows ONLY D-12's four differences.
   - **New programs (written here):**
     - `sqlget1466.sh`: go-sqlcmd SELECT runner with the D-11 refusal list. Server host from an in-process ARM GET, never in evidence; `AZURE_CONFIG_DIR` exported; `-b -I`; `--authentication-method ActiveDirectoryDefault`; `-d` exactly `hpsmpoc` or the S14 backup name.
     - `rule1466.sh`: create/delete of one /32 rule, address from Azure SQL's refusal text, `trap`-deleted.
     - `snap1466.sql` + `snapcmp1466.py`: SELECT-only, metadata and aggregate checksums, no row content. Reads: whoami; history rows of `dbo.__EFMigrationsHistory` and `poc.__EFMigrationsHistory_Feedback`; per `poc` table count + `CHECKSUM_AGG(BINARY_CHECKSUM(*))`; `audit_event` and `audit_event_pre_ledger` COUNT_BIG + MAX(audit_id) where present; `sys.tables` `ledger_type_desc` for both; `COL_LENGTH('poc.follow_up','contact_purged_at')` and its non-null count; the `poc_app` permission and member read-back.
     - `schema1466.sh`: M1-M4 in order, with every guard below.
     - `sqlrehearse1466.sh`: BUILD 7 (iv).
   - **Forbidden-operation grep** `sql db (update|delete|restore|copy|rename)|deployment group (create|what-if)|appsettings (set|delete)|firewall-rule (create|delete)|webapp (stop|start|restart)|/submit|method: *.DELETE|Down\(` over `.tools/b1466/` programs (clones and packages excluded). It must list exactly:
     - `schema1466.sh` (copy, stop, rule);
     - `rule1466.sh`;
     - `rollback1466uat.sh`;
     - `deploy1466.sh` (start, if S16 = A);
     - the PART F plant line;
     - the router's abort list.

     Name each line. Control: a planted line lists 1 more.
   - Never copied: `rollback1460uat.sh` (wrong way back), shots, evidence trees, other seats' clones.
7. **Local proof (NO load gate; print `uptime` load1 beside each run; a timing-only failure is re-run once and both results written; run under `.tools/b1466/heavy.lock`).**
   - **(i) API seeder, SQLite, UAT-shaped** (as B1460 BUILD 7 (i)): `TARGET`'s API boots twice on a `PREV`-seeded db.
     - The SQLite twin migration `20261110003229_...` applies on the first boot (history +1; `follow_up` gains the column).
     - Then "...already in this database; nothing was written."
     - Every table's row count is equal and every table's row hash is equal, except `follow_up` (hash over its PREV columns equal) and the history table (+1 row).
     - Boot 2 = boot 1 exactly.
     - Plant: one added row reads 1 differing.
   - **(ii) Web pair** (as B1460 BUILD 7 (ii)):
     - 4 levels sign in;
     - route tables `TARGET` vs `PREV`: status differences 0; text differences only per D-12;
     - **the sidebar label reads "Playbook Partner Readiness" with 2 lines at 1440 and 390-drawer on `TARGET` and "My readiness" with 1 line on `PREV`** (plant);
     - **Demo alias: real names shown to Demo on Home `TARGET` 0, `PREV` >= 1** (or "not applicable locally" with the reason, if the local seed gives the Demo no Upcoming rows);
     - logo link 44 / `PREV` smaller below 1024.
   - **(iii) #305, local `TARGET` API only, then `PREV` as control:** as the local Admin or Partner, `POST /api/v1/customers` with a name of only U+200B and `synthetic: true` (read the create route from `TARGET` source; print its `file:line`). `TARGET` answers 422 `customer.name-blank` with 0 customer rows added. `PREV` (control) does not answer `customer.name-blank`. **Never on UAT.**
   - **(iv) SCHEMA REHEARSAL on a local SQL Server container** (`sqlrehearse1466.sh`; CI's image by digest from `.github/workflows/ci.yml` at `TARGET` (print the `MSSQL_IMAGE` line), `--platform linux/amd64`, `127.0.0.1` on the port block, container name `b1466-mssql`; SA password generated in-process, never printed; stopped, never removed, at the end):
     1. a database `hpsmpoc` with `PREV`'s `assessment.sql` then `feedback.sql` applied (rc 0), and at least 3 synthetic audit rows inserted (one with non-ASCII text) plus one `follow_up` row if its FKs allow (else say so);
     2. `snap1466.sql` read twice: byte-equal;
     3. **`TARGET`'s `assessment.sql` with the SAME go-sqlcmd binary and flags as the hosted step (`-b -I`; SQL auth here instead of Entra):** rc 0; re-run rc 0 with the history count unchanged;
     4. `snapcmp1466.py after` PASS: history +1 with the exact id and `10.0.12`; `audit_event` `APPEND_ONLY_LEDGER_TABLE`; `audit_event_pre_ledger` `NON_LEDGER_TABLE`; both counts and MAX(audit_id) = before; `contact_purged_at` present, 0 non-null; every other table equal;
     5. **controls:** the BEFORE snapshot against itself FAILS (no migration); a planted change on `poc.customer` FAILS; **an `UPDATE poc.audit_event ...` as SA after the apply is refused with Msg 37359** (the ledger is real);
     6. if the seat can boot `PREV`'s API against this database with a local SQL login (`ConnectionStrings` override in-process; never on UAT), record its start-up line and any Msg 37359; else NOT TESTED (S16 A evidence; D-13);
     7. `TARGET`'s `api-identity.sql` cannot run locally (`CREATE USER ... FROM EXTERNAL PROVIDER` needs Entra); say so. The gate measured its Msg 15151 behaviour (VERDICT m1).

     **Docker unavailable, or the image not pullable = STOP before M2** (`STOPPED: NEEDS TUESDAY schema rehearsal not possible`). The hosted apply never runs an unrehearsed instrument.
   - `CHECKPOINT local pair`, then `CHECKPOINT SCHEMA REHEARSED`.

## PART M + PART P: the window on UAT (`hpsm-poc-uat-rg`; SQL `sql-hpsmpoc-uat-25onzn` / `hpsmpoc`; web `app-hpsmpoc-web-uat-25onzn`, API `app-hpsmpoc-api-uat-25onzn`) `[PROD-CLASS]`
P1. **BEFORE (read-only; API up).**
- PRE-DEPLOY SIGNALS (all seven), D-5 (`CHECKPOINT DATABASE STILL AWAKE (before)`), and the platform backup facts.
- The live-check of the downloaded wwwroots against `PREV`; `/health/ready` once, timed.
- The B1460 P1 walk at both widths: start page; 8 plain sign-ins; route tables per level; customers 4/5/5/4 and id-set hash; the readiness hub (Partner); the 14 walkthrough steps (two walks); Recent activity; the refusal matrix; D-14; the D-12 runner/results pages.
- PLUS the D-12 readers: sidebar (every page), Demo alias, logo link, Roadmap sentence where reached.
- **The M1 probe BEFORE:** as Partner, `GET /api/v1/assessments/<the sample customer's assessment>/follow-ups` (`listFollowUps`, `AssessmentModule.cs:274` at `TARGET`). Record the status and item count only (expected 200 on `PREV`).
- Screenshots `before-uat-<page>-<w>x<h>.png` into `Briefs/2026-11-10_B1466_evidence/` (start page; Partner home 1440 and 390 with the sidebar; the readiness hub 1440; Demo home 1440). Never a feedback page. Open the key frames with the Read tool and describe them.
- `CHECKPOINT UAT BEFORE walk`.

P2. **THE WINDOW (`schema1466.sh`, then `deploy1466.sh`).**
- Re-list panes. Re-read the addenda (0) and the PRE-DEPLOY SIGNALS (W2 = W1 except the activity window). Re-read origin main against S4. Fresh identity pass.
- **M2 STOP the API:** `az webapp stop -g hpsm-poc-uat-rg -n app-hpsmpoc-api-uat-25onzn`.
  - State `Stopped` by ARM GET.
  - API `/health` not 200 within 60 s (record the status); web `/api/health` still 200.
  - Start the API DOWN clock. `CHECKPOINT API STOPPED`.
- **M1 BACKUP (S14):**
  - `rule1466.sh` opens `b1466-schema-20261110` (D-4).
  - whoami `dbo` / `db_owner` 1. `snap1466.sql` twice, byte-equal: **S0**. It records history Assessment (B1234: 17) and Feedback (B1234: 3), `audit_event` count and max id, `ledger_type_desc` NON_LEDGER, `audit_event_pre_ledger` absent, `contact_purged_at` absent.
  - **T0** = the UTC minute logged now, written to `db/restore-point.txt`.
  - COPY form:
    - `az sql db copy -g hpsm-poc-uat-rg -s sql-hpsmpoc-uat-25onzn -n hpsmpoc --dest-name hpsmpoc-b1466-pre` with serverless GP Gen5 2, min 0.5, auto-pause 60, backup redundancy Local. Read the flags from `az sql db copy -h` and stub them in BUILD 5.
    - Wait (by `kill -0`) for `Online`.
    - `snap1466.sql -d hpsmpoc-b1466-pre`: it must equal S0 on every row. That is **BACKUP PROVEN**.
  - PITR form: BACKUP PROVEN = `earliestRestoreDate` before T0 by >= 24 h, retention days >= 7, and T0 recorded. Say plainly that no restore was tested.
  - `CHECKPOINT BACKUP PROVEN`. **The API DOWN LIMIT is checked here: past it, run RB-0.**
- **M3 MIGRATE:**
  - `date` before the hard stop; addenda re-read.
  - `sqlcmd -b -I -i <TARGET's api package>/assessment.sql -d hpsmpoc` once. Rc 0 and error lines 0 expected.
  - Then the SAME file once more: rc 0, "nothing applied" (history count unchanged).
  - **rc non-zero or THROW 50117:** RB-2 (snapshot = S0 proves the rollback of the transaction).
  - `CHECKPOINT SCHEMA APPLIED`.
- **M3 AFTER:** `snap1466.sql` = **S1**. `snapcmp1466.py S0 S1` must read exactly:
  - Assessment history +1 = `20261110003228_LedgerAuditAndFollowUpRetention|10.0.12`; Feedback history equal;
  - `audit_event` `APPEND_ONLY_LEDGER_TABLE` with count and max id = S0's;
  - `audit_event_pre_ledger` `NON_LEDGER_TABLE` with count and max id = S0's;
  - `contact_purged_at` present, 0 non-null;
  - every other table equal per D-16.

  Any other difference: RB-1.
- **M4 `api-identity.sql`** (`TARGET`'s `infra/sql/api-identity.sql`, `-v AppIdentity=id-api-hpsmpoc-uat`): rc 0. Its read-back must show:
  - `DENY UPDATE` and `DENY DELETE` on `poc.audit_event` AND on `poc.audit_event_pre_ledger`;
  - `DENY UPDATE`/`DELETE` on `finding_disposition`;
  - `DENY INSERT`/`UPDATE`/`DELETE` on `__EFMigrationsHistory_Feedback`;
  - GRANT SELECT/INSERT/UPDATE on schema `poc`;
  - the 10 GRANT DELETE rows (B410's set);
  - `poc_app` <- `id-api-hpsmpoc-uat`.

  The read-back lines go in STATUS (they name a role and an identity, no person). `CHECKPOINT IDENTITY SCRIPT RUN`.
- **Rule deleted** by the `trap`. List = before. `CHECKPOINT TEMP RULE CLOSED`. The refusal poll starts in the background.
- **M5 per S16:**
  - **A:**
    1. `az webapp start` the API; record the time and whether `/health` answers 200 before the deploy starts. `CHECKPOINT API STARTED`;
    2. at once, `deploy1466.sh` (B1460's `deploy1460.sh` with its guards hand-edited: before the cut-off; `B1466_ADDENDUM` 0; `repo` HEAD = `TARGET`; `RUN` = S5; live public build `q9tnDMDG__k92hFNCyYJ1` x1 and `TARGET`'s x0; origin main = `TARGET`);
    3. then, in the same second as `DEPLOY START`, exactly `scripts/deploy-from-ci.sh deploy 009421a28616c8b31dde86b59d4c4ca674c288fa hpsm-poc-uat-rg app-hpsmpoc-web-uat-25onzn app-hpsmpoc-api-uat-25onzn` from `.tools/b1466/repo`.
  - **L:**
    1. the same `deploy1466.sh` and script with the API stopped;
    2. on exit 0, `az webapp start` the API (`CHECKPOINT API STARTED`);
    3. on a non-zero exit after the web leg: `az webapp start`, then RB-1.
  - Exit 0 = done. Exit 3 = DEPLOYED BUT NOT PROVEN: STOP with the list. Exit 1: read the reason; no hand steps; D-13 / RB-1.
  - Windows from deploy start: **web 420 s, API 900 s**; past a window, any non-200 starts `rollback1466uat.sh rb1` within 60 s. The poller writes every 10 s; the heartbeat every 30 s to `.tools/b1466/logs/heartbeat.txt`.
  - `CHECKPOINT UAT deploy START`. Record the API down minutes (M2 stop to the first 200 of the API's `/health` on `TARGET`).

P3. **AFTER (read-only HTTP; only D-11's named non-GET calls).**
- (a) `/api/health` and `/health` 200 x3 ten seconds apart; `/health/ready` 200 (timed; it touches SQL); `/` 200; `/customers` 307; session `{"signedIn":false}`; `login.microsoftonline.com` 0.
- (b) **THE M1 PROBE LIVE:** as Partner, `GET /api/v1/assessments/<same>/follow-ups`: **200** and the item count = BEFORE. A 5xx, or "Invalid column name" in the body = the slot-S9 class "the API cannot read follow-ups" (RB-1).
- (c) Start page = BEFORE; 8 of 8 plain sign-ins; walkthrough panel 0 on every one.
- (d) Route table BEFORE/AFTER per D-12 (`cmpwalk1466.py`: FAILS 0, S9 classes 0; plant: a route set to 500 reads S9 1).
- (e) **THE CHANGE LIVE, measured, in a SEEN table at 1440 and 390:**
  - **(S)** the sidebar label text, link height, line count and the next row's offset, BEFORE vs AFTER, on Partner home and on `/assessments` for every level (expected: "Playbook Partner Readiness", 2 lines, 56 px, +12; S15 states the values);
  - **(R)** the readiness hub fields as B1460 D-13 (R), now with the sidebar label (S15);
  - **(D)** Demo alias counts (real names shown to Demo: AFTER 0) and the overview row;
  - **(L)** the logo link height;
  - **(G)** the Roadmap sentence, if reached, or "not reached by the walk";
  - (C)/(A)/(W) as B1460 (equal to BEFORE now).

  Screenshots: `after-uat-home-partner-{1440x900,390x844}`, `after-uat-readiness-hub-{1440x900,390x844}`, `after-uat-home-demo-1440x900` (the alias rows; it shows aliases, not names). Open them yourself and describe the sidebar label as SEEN (one or two lines).
- (f) Security views; refusals (403 `uat.action-off` x2); the D-14 door: = BEFORE.
- (g) The words table (D-8) in STATUS.
- (h) **Build proof:**
  - live-check web and API = `TARGET`'s counts, site-only 0;
  - the live `BUILD_ID` = the package's, x1 on the public page; `q9tnDMDG__k92hFNCyYJ1` x0;
  - the live HpsmPoc DLLs embed `T8` x1;
  - the live `HpsmPoc.Modules.Assessment.dll` holds `followup.contact-purged` x1;
  - active deployments both new.
- (i) The platform lines of the new containers, verbatim.
- (j) Settings hashes equal (W4 vs W3); SQL firewall exactly `AllowAllWindowsAzureIps`. Databases on the server: `hpsmpoc`, `master`, plus `hpsmpoc-b1466-pre` (COPY form) and nothing else.
- (k) D-12 runner and results pages = BEFORE.
- (l) **The activity log since M2:** exactly the named writes (webapp stop/start of the API; the copy's `databases/write`; firewallRules write/delete x2 (or x4 with (n)); the two deploys' rows; `publishxml/action` reads). Anything else listed: STOP.
- (m) D-5 again (`CHECKPOINT DATABASE STILL AWAKE (after)`).
- (n) **SCHEMA READ-BACK** (one rule `b1466-read-20261110` under `trap`, SELECT only): `snap1466.sql` = **S2**.
  - History still +1 only; `audit_event` APPEND_ONLY and `audit_event_pre_ledger` NON_LEDGER;
  - `audit_event_pre_ledger` count and max id = S0's (nothing writes to it);
  - `audit_event` count >= S0's, and every row with `audit_id` <= S0's max equal to S1's (checksum over that range; the walks' sign-ins may add rows: count them);
  - `contact_purged_at` 0 non-null;
  - the `poc_app` read-back = M4's.

  Rule closed; list = before. `CHECKPOINT SCHEMA READ-BACK`.

**Healthy and all passed: `PART P VERDICT: PASSED` (`CHECKPOINT PART P PASSED`).**
- Unhealthy past a window, a deployed app not answering, the M1 probe failing, or a slot-S9 class: `rollback1466uat.sh rb1`, then `ROLLED BACK`.
- Any other miss on a healthy site: `STOPPED: NEEDS TUESDAY`, with the numbers and the one-command way back printed. **Still run PART F before the STOPPED line if the site is healthy.**

## PART F: the UAT feedback store (READ-ONLY; D-17)
Run only after `PART P VERDICT: PASSED`, or after a healthy-site STOP. Never after a way back.
- Run D-17. The only non-GET calls are 1 Admin sign-in POST and 1 sign-out POST, both counted.
- Write the counts and the table of items newer than 2026-11-10 11:04:40 AEDT under `## PART F: UAT feedback (read-only)`.
- `CHECKPOINT PART F DONE`.

## STANDING LINES
1. **PRIOR-WORK CHECK first, read WHOLE before the first `az` call; STATUS needs a `PRIOR WORK` section:**
   - this brief;
   - the B1460 kit (636 lines) and `Briefs/2026-11-10_B1460_STATUS.md` (319 lines);
   - `tuesday/briefs/2026-11-10_B1442_verify/VERDICT.md` (M1, m1, m2) and `Briefs/2026-11-10_B1442_STATUS.md` (its FOR THE DEPLOY read as WRONG at step 1);
   - `Briefs/2026-11-03_B1234_STATUS.md` (PART M `:114-149`, way back `:283-287`, Corrections) and `Briefs/2026-10-21_B410_STATUS.md:130-153` and `:404-500` (the UAT schema apply; the start-before-deploy record);
   - the five gate VERDICT files at their FINDINGS;
   - `tuesday/briefs/2026-11-10_B1463_verify/wrap-table.txt`;
   - `tuesday/briefs/2026-11-10_B1466_WORDS-FOR-KAM.md`;
   - `infra/README.md` at `TARGET` (`:50-105`, `:213-235`); `infra/sql/api-identity.sql` at `TARGET` and `PREV`; `scripts/deploy-from-ci.sh` at `TARGET`;
   - the project `CLAUDE.md`; `1_Project_Definition/CLARIFICATIONS.md` (C-07; a search of `migration`, `ledger`, `UAT`; control `C-07` hits, a no-such token 0).
2. **Never touch what the ruling does not name.** No `az` write and no HTTP except the named ones. No other group, not even a read (only the subscription-level `az group list`, names only). Never another subscription. Never `HP Reporting and Docs/`, any SOW, `2_Project_Files/HP Docs/`, `1_Project_Definition/Source_Documents/`, `.local/`, `4_Credentials/` (beyond `.azure` and `.gh-config`).
3. **Never delete** (`rm`, `rmdir`, `az ... delete` except the one temporary rule per D-4, `docker rm`, `--prune`). Quarantine by MOVE to `.tools/b1466/_quarantine/`. The copy database, a renamed database and the rehearsal container stay.
4. **No message to any human**; nothing to HP; no Jira write; no person's name or e-mail in STATUS ("the product owner"). Synthetic data only: print no customer content beyond counts, titles and hashes; no audit row content (counts, max ids and checksums only). PART F summaries follow D-17.
5. **Secrets:**
   - never on argv, never printed, never in a kept file, STATUS or screenshot. The SA password of the rehearsal container is generated in-process and passed by environment, never argv;
   - gitleaks over the evidence folder with a `ghp_`-shaped canary (rc 1; real rc 0);
   - `encryptionKey` values 0;
   - host names (`azurewebsites.net`, `scm.`, `vault.azure.net`, `database.windows.net`) 0 outside the STATUS last line (control 1);
   - dotted quads only `127.0.0.1` (the firewall address is `<ip>`; control 1).
6. **CodeQL policy.** This seat lands nothing and opens no PR.
7. **Shell:**
   - never type `cd`; absolute single-quoted paths (they contain `!`);
   - `/usr/bin/grep -i` with a positive control for every count;
   - zsh: `pipestatus` or `bash -c`; never an unquoted word starting `=`; brace every `${VAR}`;
   - no `timeout`, no `pgrep -f` (B1460 Corrections 5 (c)); wait by `kill -0` or done-markers;
   - `python3 -I -B` only; scratch in the session scratchpad, never `/tmp`;
   - hex and sha maps hand-edited, never by `sed`;
   - a `file:line` you cite is printed by `grep -n -i` or `awk NR==n` at `TARGET` just before you write it;
   - read a tool's usage from its header (or `az ... -h`), never by invoking it for effect;
   - **never `rm`** (B1460 Corrections 5 (g)).
8. **Records: none in this seat.** STATUS and evidence only; nothing committed or pushed.
9. **STATUS sections** (`1_Project_Definition/Briefs/2026-11-10_B1466_STATUS.md`, evidence in `.../2026-11-10_B1466_evidence/`), in this order:
   - Step 0
   - **BLUF.** Its first line states any way back or stop. It carries in one line: the sidebar label AS SEEN (text, line count, height) and the hub H1. In a second line: the migration applied (history id, ledger type, audit rows n = n = n) and the API down minutes. **Anything "not shown" goes in the BLUF.**
   - PRIOR WORK
   - PHASE 0 and LIVE-BEFORE
   - Target, gate and CI proof (incl. the `fc90f07...d49be881` proof, the appended-block proof, the SQL Server test counts)
   - The words (D-8)
   - Package checks and the local proof (seeder, web pair, #305, SCHEMA REHEARSAL with its controls)
   - The way back (copied; digests; `rollback1466uat.sh` stub runs)
   - PRE-DEPLOY SIGNALS and the database (before; backup facts)
   - **PART M: the window** (M2 stop time; S0; T0; the copy or PITR proof; the apply output; S1 compare; the identity read-back; rule open/close times and the refusal; M5 times; API down minutes)
   - PART P (BEFORE, deploy, AFTER: the SEEN table; the M1 probe; the build proof; the activity rows)
   - The schema read-back (S2) and the database (after)
   - **PART F**
   - Settings/access/spend (**the copy database is new spend: say so, with its sku**)
   - The way back (kept, NOT run; or run, with every step)
   - NOT TESTED
   - FOR TUESDAY, in six numbered items:
     1. UAT at `T8`; the main head at the deploy; the database migrated (id, time).
     2. **A short note for the product owner, 4-7 lines, plain words:** the sidebar label as SEEN; the Demo alias; nothing else visible changed; the database update done with a backup first; how long UAT's API was down; the feedback count and anything new since this morning.
     3. The tables.
     4. Records owed: a deploy C-entry for `TARGET` WITH the schema step (T0, the copy name, the rule times, the history id); landing C-entries for #304-#308; B1442 M1 recorded as the deploy order for every API deploy from now on.
     5. **The copy database `hpsmpoc-b1466-pre` (or a renamed one) is billed until someone deletes it: a decision for Tuesday / the product owner.** Not this seat's.
     6. Anything seen worth a ticket.
   - Processes (the last 5 heartbeat lines; the rehearsal container stopped, listeners 0)
   - Corrections

   Also the `CHECKPOINT` lines.

## PARTITION (named from both sides)
- **Yours:**
  - `.tools/b1466/` (incl. `repo`, `repo-rb`, `target/`, `rollback/`, `bin/`, `db/`, `live/`, `logs/`, `fb/`, `_quarantine/`) and `1_Project_Definition/Briefs/2026-11-10_B1466_*`;
  - the local container `b1466-mssql` on the port block;
  - read-only `az` on `hpsm-poc-uat-rg`; read-only GETs on the two UAT hosts (plus D-11's named non-GET calls); SELECT-only SQL on `hpsmpoc` and on the S14 backup database;
  - the D-2 write classes (w1)-(w8), nothing else.
- **Not yours:**
  - every other group, database and subscription; the template; any app setting, vault secret or other firewall rule; the demo data;
  - `.tools/b1460/` (read-only: copy by name) and every other seat's tree;
  - `2_Project_Files` content (read only); records repositories;
  - any PR, branch, Jira ticket or message;
  - every real feedback item;
  - deleting the copy database.
- **From the other side:**
  - Before you start, Tuesday has filled the slots and confirmed no other HPSM-POC deploy seat.
  - Tuesday deploys nothing to UAT and changes nothing in `hpsm-poc-uat-rg` until your STATUS ends `DEPLOYED` or `STOPPED`.
  - If anything lands on main while you run, you finish on `TARGET` (D-1).

## HOLDS (never, in this brief)
- No write START after the hard stop.
- No deploy of anything but `TARGET`'s two CI packages (or `PREV`'s in D-7).
- No what-if; no template deploy; no `az webapp show`.
- **No migration `Down`; no `feedback.sql`; no laptop-built bundle; no SQL statement other than `TARGET`'s `assessment.sql` (once + one idempotent re-run), the `api-identity.sql` of M4 or D-7, and SELECTs.**
- No `az sql db` write other than S14's copy and D-7's restore/rename/update. No pause or resume. No export or import. No database deleted or dropped.
- No firewall rule other than D-4's, each closed by `trap`.
- No app-setting or vault write. No web-app stop or restart except the API's M2 stop / M5 start and the deploy's own. No `delete`.
- No hosted demo-data reset, re-seed or edit. No customer created, renamed or deleted on UAT. No feedback item created, approved, deleted, moved or downloaded; no click on either feedback page; no screenshot of either.
- No narrative generated; no readiness self-assessment started; no walkthrough answer saved; no PDF opened; no account-menu level item clicked; no collapse control clicked.
- No new paid resource other than S14's copy. No CI re-run. No code edit. No word edited. No claim to HP.

## Stamp
Pane `Datasec/HPSM-POC-D59` (suffix `D59`). MEASURED at drafting: no `SEAT-D59` file and no `B1466` file in `tuesday/briefs/` before the drafter's three files (`ls | grep -c` 0). `.tools/b1466` absent. Seat level `BRIEF_SEAT_LEVEL=opus`.
- (S1) STAMP (Tuesday, `date`; kit read whole with its line count; CI at `TARGET` and `branches/main` re-read at source): RESTAMPED by Tuesday s264 at 21:14 AEDT 2026-11-10 (the first stamp 20:17 expired: the cool-load waiter released at 21:11:45 and Step 0 at 21:12:31 fired REFUSE 'Clock' correctly, nothing touched). Re-read 21:14:18 by date (gh api -X GET under the HPSM-POC GH_CONFIG_DIR): branches/main = 009421a28616c8b31dde86b59d4c4ca674c288fa = S4; ci 42773429652 completed/success, Push on main 42773429155 completed/success; B1466_ADDENDUM files 0; panes %0 coordinator, %1 fleet-monitor, %4 Datasec/HPSM-POC-D59 (you) only; load1 4.56; no unseen product-owner board message (kam_watch --pending: none). Kit read whole at the first stamp (738 lines); since then only this line changed (the earlier copy is kept beside the kit as .pre-restamp-2114). Every other slot stands.
- (S2) LAUNCH AUTHORITY (verbatim, with clocks: the terminal line, the card `hpsmpoc-uat-deploy-five-landings-1110` ruled `a` 19:40:52, the card `hpsmpoc-retention-migration-1110` ruled `a` 09:04:11; whether the product owner read WORDS-FOR-KAM, and his reply): The product owner, Tuesday terminal (a typed turn between the 18:11 #308 landing and the 19:40:52 card ruling, 2026-11-10; exact minute not recorded), verbatim: "go ahead and deploy to UAT". Card hpsmpoc-uat-deploy-five-landings-1110 ruled a at 2026-11-10T19:40:52+11:00: 'Deploy all five to UAT now, with the database update' (detail: 'One deploy seat, backup first, the update in the same window, then a live check of what you will see; told to you after.'). Card hpsmpoc-retention-migration-1110 ruled a at 09:04:11: 'Allow the one migration (gated, not deployed)'. Standing: terminal just after 09:08 'don't wait, deploy as soon as it's ready'. Words: WORDS-FOR-KAM was sent to him on the live board at 20:16:45 with the file in the drawer (bf-77d74df77bf2, file f-4d87b01d3d), saying 'Say stop and I hold'; he had NOT replied at the stamp. The card he tapped already named the sidebar label and its two-line wrap, the logo link and the Demo alias fixes; the Roadmap sentence change reaches him only in that message. A 'stop' from him before M2 = Tuesday writes B1466_ADDENDUM-1 and you STOP.
- (S3) HARD STOP (the rule): Step 0 plus 150 minutes, written by you as an absolute AEDT clock at Step 0; no write START after it; DONE no later than Step 0 plus 180 minutes; Step 0 within 45 minutes of slot S1.
- (S4) TARGET-SHA: 009421a28616c8b31dde86b59d4c4ca674c288fa (#308 squash; one parent `eb2e49c798e939491c8184e96cf056cc8a67ce0d`; = `branches/main` at 19:58:59 AEDT, MEASURED by the drafter; Tuesday re-reads at the stamp)
- (S5) CI RUN at TARGET (push run `ci`; and the CodeQL `Push on main` run; drafter measured `42773429652` / `42773429155`, both completed/success): ci push 42773429652 completed/success; CodeQL Push on main 42773429155 completed/success (both re-read at 20:16:59).
- (S6) WHICH PRs IN TARGET, their heads, their gate lines, and the open findings carried by id (drafter's reading: #305 `792c78f2` B1441 F1-F3 Minor, F4-F5 Info; #304 `d49be881` = gated `fc90f07` + 1 test commit, B1440-2 G1 Finding, G2-G3 Minor; #306 `4aff7ec4` B1464 F1-F3 Minor, F4-F5 Info; #307 `c16f422e` B1442 **M1 Major (the deploy order: this kit)**, m1-m3 Minor, i1-i2 Info; #308 `aa9bac75` B1463 1-4 Minor, 5 Info): Drafter's reading ACCEPTED: #305 792c78f2 (B1441 F1-F3 Minor, F4-F5 Info); #304 d49be881 = gated fc90f07 + 1 test-only commit (B1440-2 G1 Finding, G2-G3 Minor); #306 4aff7ec4 (B1464 F1-F3 Minor, F4-F5 Info); #307 c16f422e (B1442 M1 Major = the deploy order of this kit; m1-m3 Minor, i1-i2 Info); #308 aa9bac75 (B1463 1-4 Minor, 5 Info). Merge order 305, 304, 306, 307, 308 (the drafter's correction of Tuesday's order is accepted).
- (S7) RULING 1, the route: BACKUP FIRST; API STOPPED; ONE ASSESSMENT MIGRATION; API IDENTITY SCRIPT; BOTH PACKAGES; ONE TEMPORARY SQL RULE; NO WHAT-IF; NO TEMPLATE DEPLOY; NO APP SETTING WRITE; NO DATA RESET
- (S8) RULING 2, the site: UAT ONLY
- (S9) RULING 3, the misses. Drafter default: after M3, take the way back RB-1 and end ROLLED BACK when:
  - a level does not sign in;
  - a route that answered 200 before answers 5xx after;
  - **the M1 probe (`listFollowUps`) answers other than 200**;
  - `/health/ready` is not 200 past the API window;
  - a security view answers 5xx for the known customer, or 2xx other than the not-found page for no-such-id;
  - any non-GET request other than D-11's named calls is attempted from any walked page;
  - the walkthrough panel appears on a plain level sign-in;
  - the start page loses a level button, or the sidebar is absent on a signed-in page;
  - the account menu is absent;
  - a D-12 runner or results page differs from BEFORE, or the hub is absent, 5xx, or without its runs list;
  - any existing customer row is removed or replaced;
  - a horizontal scroll appears that BEFORE did not have;
  - reset or customer-delete answers anything but 403 `uat.action-off`;
  - the API refuses to start;
  - a D-14 gated admin page stops redirecting a visitor with no session.

  Every other miss on a healthy site (SEEN values differing from S15 included) = STOP, with the numbers and the one-command way back printed: DRAFTER DEFAULT ACCEPTED AS WRITTEN
- (S10) RULING 4, eight items, each CONFIRMED / NOT CONFIRMED:
  - (a) read-only copies by name from `.tools/b1460/` into `.tools/b1466/`, hand-edited;
  - (b) the clones into `.tools/b1466/repo` and `repo-rb`, and the go-sqlcmd v1.10.0 download into `.tools/b1466/bin/`;
  - (c) D-11, D-12, D-13 (S16), D-14, D-16 (no real feedback item touched; no customer, run or narrative created on UAT; a real Chromium walk, read-only);
  - (d) **the UAT API stopped for up to S17 minutes plus the deploy (a few minutes down, as the card said), with NEW API code, and whether an HP review session is under way**;
  - (e) ports 9970-9979 (or the block Tuesday names), and no other `Datasec/HPSM-POC-D*` pane present;
  - (f) PART F as D-17 (counts and items since 11:04:40);
  - (g) **the one temporary /32 SQL rule (plus the read-back one, and one in a way back), each closed by trap**;
  - (h) **the local SQL Server rehearsal container `b1466-mssql` (CI's image; amd64 emulated), left stopped, not removed**.

- (S10) Values: (a) CONFIRMED (b) CONFIRMED (c) CONFIRMED, S16 = A (d) CONFIRMED: the API down window is accepted as the card said ('a few minutes down'); whether an HP reviewer is in session is unmeasured (evening AEDT; say so in STATUS) (e) CONFIRMED, ports 9970-9979; at the stamp the panes were %0 coordinator, %1 fleet-monitor, %2 Datasec/Security-Composer-R205, %3 Datasec/HPSM-POC-R203 (records: Jira + analysis CLARIFICATIONS.md only, no az, no hosted host: not a REFUSE hit) (f) CONFIRMED (g) CONFIRMED (h) CONFIRMED
- (S11) RULING 5, the words on UAT: UAT WORDS: THE CLOSED LIST OF D-8, SENT TO THE PRODUCT OWNER BESIDE THE DEPLOY
- (S12) PULL REQUEST NUMBERS: 305 304 306 307 308
- (S13) RULING 6, the UAT hold: UAT HOLD LIFTED FOR THIS DEPLOY ONLY: ACCEPTED
- (S14) BACKUP FORM (exactly `COPY AND POINT-IN-TIME` (drafter default: one new serverless copy `hpsmpoc-b1466-pre`, billed until deleted) or `POINT-IN-TIME ONLY` (no new spend; no tested restore; slower way back)): COPY AND POINT-IN-TIME
- (S15) EXPECTATION AS SEEN (D-12 / P3 (e)): the sidebar label, its line count and height at 1440 x 900 and in the 390 x 844 drawer; the hub H1, title, eyebrow and first panel; the Demo alias count; the logo link height: Sidebar /assessments link: 'Playbook Partner Readiness', 2 lines, link 56 px high (from 44), rows below +12 px, at 1440 x 900 and in the 390 x 844 drawer, every level; collapsed rail unchanged (B1463 wrap-table, RELAYED). Hub: H1 'Playbook Partner Readiness', document title as BEFORE, eyebrow 'My readiness' (unchanged, AssessmentsHub.tsx:131), first panel as BEFORE. Demo level: real customer names shown on Home Upcoming activity and the overview 'Customer name' row AFTER 0 (BEFORE >= 1). Header logo link 44 px high at 390 and 1440.
- (S16) WINDOW ORDER (D-13; exactly `A: START PREV THEN DEPLOY` or `L: DEPLOY TO THE STOPPED API`): A: START PREV THEN DEPLOY
- (S17) API DOWN LIMIT in minutes before M3 (an integer 15-45; drafter default 30): 30

**Commission (read-only to you):** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1466_SEAT-D59_hpsmpoc-uat-deploy-main-migration.md`. **Step 0:** run the REFUSE checks in the order written, then copy this brief unchanged into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/` and record `cmp`, both sha256s and the slot count. Preflight: write "none (brief_seat launch)" or quote the launcher's warnings verbatim.
**Launch (Tuesday, ONE waiter, through the cool-load waiter, as a tracked background task; launch only after the stamp):** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/HPSM-POC-D59 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=opus WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1466_SEAT-D59_hpsmpoc-uat-deploy-main-migration.md'"` (the form RELAYED from B1460's kit `:630`; the drafter did not re-`ls` the two tools). **Never run /model in this pane.**
**Last line of STATUS, exactly one of:**
`DEPLOYED B1466: <sha40> <site url>` (the sha is `TARGET`; the site url is the UAT web site's public address, written once, as the last line only), or
`PARTIAL B1466: SCHEMA APPLIED, CODE NOT PROVEN, <reason>` (followed by a `STOPPED:` line only if it is the last), or
`STOPPED: NEEDS TUESDAY <one question>`.
(`ROLLED BACK` is a body line plus a final `STOPPED: NEEDS TUESDAY <one question>` last line.)

READ-WHOLE-BY-TUESDAY: DONE 20:17 by Tuesday s264 (738 lines)
