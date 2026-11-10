GATE B1442: GO WITH FINDINGS @ c16f422 on main 6b0c5f2

Tier 1 (retention + audit ledger + one migration per provider). Independent gate, 2026-11-10 14:45-15:5x AEDT.
Own clone and worktrees under this session's scratchpad (`.../scratchpad/v1442/`), push URL `invalid://no-push-v1442`, never pushed.
Nothing hosted touched: no az, no PR, no Jira, no mail. Two read-only GitHub reads (`git ls-remote`, `gh api -X GET pulls`).
The only databases: my local SQL Server container (CI's image by digest) on 127.0.0.1:9842, Azurite on 9843, and SQLite in memory.

## Refs and partition (step 1)
- `git ls-remote`: `refs/heads/b1442/hpsmpoc-retention-ledger-audit` = c16f422e5b04f8a25f73ad5d8ae7dd7451aff945 = READY sha. main = 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb (merge-base of head = main).
- 4 commits (601db07, 5dfd22e, 493da72, c16f422). 17 changed paths, 17 of 17 inside OWNS (Persistence/** 10, FollowUp/FollowUpRetentionPurge.cs new, Feedback FeedbackDbContext.cs by ANSWER-1, 3 new test files, infra/sql/api-identity.sql, infra/README.md). Not changed: PersonalDataEndpoints.cs (ERASE HOLD), appsettings.json (RETENTION NONE), AssessmentModule.cs, any workflow, any web path.
- Open PRs (`gh api -X GET pulls?state=open`): 1, #304 head d49be881; control `state=all` lists 3. Overlap with #304: 0 of 17 (#304 has 13 paths, all `web/`). Overlap with the API branch 792c78f2 head 792c78f2: 0 of 17 (the API branch 792c78f2 has 8 paths; control: this branch against itself 17).
- The ANSWER-1 patch went in exactly as approved: `git patch-id --stable` of `.tools/b1442/needs-shared/feedback-ledger-safe-inserts.patch` = that of `git diff 493da72 c16f422 -- api/src` = d0ab9c01.

## Merge (step 2)
- `git merge-tree --write-tree main head`: rc 0, tree b2d3ba22 = head tree (0 paths differ; control: main vs merge tree 17 paths).
- Landing order (the API branch 792c78f2 first, then #304, then this), simulated in my clone: each merge-tree rc 0. The stacked merge adds exactly this branch's 17 paths with the same patch-id (bc1eda62 at main and on the stack).

## CI (step 3) - counts by program
| Job (predicate as in ci.yml at head) | main 6b0c5f2 | head c16f422 (= merge tree) |
|---|---|---|
| api: `dotnet test HpsmPoc.slnx -c Release --no-build` (SQLite, Azurite on) | 3936 passed 0 failed 0 skipped (Rules 164, Assessment 300, Reporting 850, Feedback 414, Api 2208) | 3952 passed 0 failed 0 skipped (Feedback 415, Api 2223) |
| api: Blob/Azurite tests (trx, `BlobReportStore*`) | 37 passed, no other outcome | 37 passed, no other outcome |
| api on SQL Server (api-assessment): `~Assessment.\|~Hosting.` | 1349 passed 0 failed (fresh container) | 1353 passed 0 failed (fresh container) |
| api on SQL Server (api-other-and-feedback): the rest of Api.Tests | 859 passed 0 failed (fresh container) | 870 passed 0 failed (fresh container) |
| same shard: Feedback.Tests | 414 passed 0 failed | 415 passed 0 failed |
| infra: `bash infra/scripts/validate.sh` (bicep 0.47.16 = CI pin, Python 3.14) | rc 0, 317 tests OK, ResourceWarnings 0 | rc 0, 317 tests OK, ResourceWarnings 0 (also rc 0 on the landing-order stack) |
| hidden characters (repo-wide, `infra/tests/test_hidden_characters.py`) | 14 OK | 14 OK (stack: 14 OK) |
| Release build | 0 warnings 0 errors | 0 warnings 0 errors (stack: 0 / 0) |

Migration up and down, local only:
- Idempotent scripts made by `scripts/build-migration-bundles.sh --sql-only` at main and at head, applied with `sqlcmd -b -I` on my container.
  - Fresh database: head assessment.sql + feedback.sql rc 0, and a re-run rc 0. Result: `audit_event` APPEND_ONLY_LEDGER_TABLE, `audit_event_pre_ledger` NON_LEDGER_TABLE.
  - Upgrade: main scripts rc 0; 2 audit rows (one has non-ASCII text); table NON_LEDGER. Then head scripts rc 0 twice. Both tables: count 2, max id 2. EXCEPT diff 0 rows. `contact_purged_at` set on 0 rows. The next insert gets id 3. An UPDATE is refused with Msg 37359.
- Down and then Up again: `LedgerAuditTests.The_migration_copies_every_audit_row...` passes on SQL Server (it runs Up, Down, Up with per-row SHA-256 checks, and `sp_verify_database_ledger`).
- Numeric `ledger_type` of an append-only table is 3 (scratch database; control: a plain table reads 0). The kit's "2" is wrong; the builder's correction is right.

## Red without the fix (step 4), in a scratch copy, restored to 0 dirty after each change
| Row | Mutation | Result |
|---|---|---|
| C0 | none | SQL Server: ledger and purge tests pass; Feedback new test + N7: 7 of 7. SQLite: 15 of 15 |
| R1 | LEDGER clause removed from the migration | LedgerAuditTests (SQL Server): 4 of 4 failed |
| R2 | Feedback context's generator line removed | SQL Server: 2 of 7 failed (FeedbackLedgerInsertTests and Hpsmpoc99Tests.N7) |
| R3 | purge cutoff moved 2 minutes (`<= cutoff.AddMinutes(2)`) | SQLite: 1 of 11 failed (the one-minute-inside control) |
| R4 | no period read as 12 | SQLite: 5 of 11 failed |
At main, the new test files do not compile (they use the new types).

## Probes (step 6)
- P1 (scratch test, SQL Server): head code on a database migrated only to `ImportFileStoredSha256` (today's hosted schema). `db.FollowUps.ToListAsync()` FAILS: `SqlException: Invalid column name 'contact_purged_at'`. P2 control (full migrate): passes. P3 (head code, old schema, two audit rows in one save): passes.
- `infra/sql/api-identity.sql` line `DENY UPDATE, DELETE ON poc.audit_event_pre_ledger` on a database without the migration fails with Msg 15151, under the script's `SET XACT_ABORT ON`. The batch aborts there: the `finding_disposition` DENY, the role membership and the read-back do not run (measured on a scratch database: only audit_event's two DENYs were present afterwards).
- Merge triggers no deploy: ci.yml has no deploy job. `Assessment:MigrateOnStartup` is true only in `appsettings.Development.json` (`git grep`), so a hosted API never migrates at startup.
- Product write paths with UPDATE or DELETE on audit rows: none outside tests (the builder's grep, re-read at the cited lines). The ledger refuses UPDATE, DELETE and TRUNCATE for the owner (13545 for TRUNCATE). These are LedgerAuditTests assertions, green on my SQL Server.
- Purge: idle (no period shipped, nothing registers it). It refuses null, "", spaces, 0, -1, 12.5, twelve and 1201. It never touches an open follow-up. It blanks fields and keeps the rows. A rejected question's reason is kept by design (ck_fuq_reject; HELD for the records).

## Scans (step 7)
- 6855 added lines plus every commit message, all clean:
  - Ban-list names (underscore-aware): 0 (planted underscore-wrapped ban-list control: 3 hits).
  - Secrets: 0. GUIDs (tenant or subscription): 0. Hosts or IPs: 0. Cf characters: 0. The only non-ASCII is printable punctuation and test data, plus BOMs at byte 0 of the 2 EF migration files, which the repo rule allows.
  - Each category had a planted control line, and each control fired.
- CodeQL pre-scan over the added lines, test files included: `new RegExp(` from a variable 0; hand-escape `.replace(/[...]/g, "\\$&")` 0; innerHTML/dangerouslySetInnerHTML 0; child_process 0. No JS or TS file changed. C#: no `FromSqlRaw($`/`ExecuteSqlRaw($`. The interpolated SQL in the tests builds only from constants (no user-input source).
- Commit metadata: the 4 branch commits carry the project's git author name. The squash replaces the commit message (squash-*.txt below carries no name). The author identity is the merging account's.

## Claims (step 8)
| Builder claim | Grade |
|---|---|
| SQLite main 3936 / head 3952, 0 failed | true |
| SQL Server head 1353 / 870 / 415, 0 failed | true |
| SQL Server main 1349 / 859 / 414 | true (my run: 1349 / 859 / 414) |
| infra validate rc 0, 317 tests | true |
| ledger_type 3, not 2 | true |
| idempotent script: fresh, over main schema with 2 rows (2 and 2, ledger), re-run | true |
| red proofs M1 (4 of 4), M6 (5 of 11), M8 (1 of 11), the Feedback red (2 of 7) | true (R1, R4, R3, R2 reproduce the same counts) |
| other red rows (M2, M2+2b, M3, M4, M5, M7, M9, M10) | not shown (not re-run) |
| "The new statement shape works on the plain table too" | true (P3) |
| FOR THE DEPLOY step 1: "Deploy that API build. It runs on the old schema." | FALSE (P1: Invalid column name 'contact_purged_at') |
| partition: only the listed files; patch applied exactly; open PRs and the API branch 792c78f2 disjoint | true |
| migration file counts 35/37 at main | true (37/39 at head) |
| containers stopped, 9960-9969 free | true (all b1442-* Exited; lsof 0 rows) |

## Findings
| # | Sev | Finding | Evidence | Action |
|---|---|---|---|---|
| M1 | Major | The deploy order in STATUS `## FOR THE DEPLOY` is wrong. Step 1 ("deploy that API build; it runs on the old schema") breaks every follow-up read: the new model maps `follow_up.contact_purged_at`. The reverse order breaks too: the old API's multi-row audit saves hit Msg 37359 on the ledger (the builder's measurement). So once this lands, **any API deploy from main needs this migration in the same window**, with the API stopped: stop the API, run the migration, deploy the API, start it, re-run api-identity.sql. The code is right; the deploy record and the release plan must change. | Probe P1 (fails), P2 control (passes), P3 | Correct `## FOR THE DEPLOY` before any hosted deploy. Tell the records seat. Any API deploy wanted WITHOUT the migration (e.g. the API branch 792c78f2 to UAT) must be cut from a main sha before this squash. |
| m1 | Minor | `infra/sql/api-identity.sql` can no longer run on a database without the migration. Msg 15151 + XACT_ABORT aborts the rest of the script (finding_disposition DENY, membership, read-back). Its header already says "run after the bundles". | Probe on a scratch database | Run it only after the migration (FOR THE DEPLOY step 6 does), or guard the line later. |
| m2 | Minor | The migration's Down drops `follow_up.contact_purged_at`. That column holds purge marks once the purge runs; after Down and Up, purged rows would be purged and audited again. The ledger table itself is kept by SQL Server, and its rows are copied back. A dev-only path, disclosed by the builder. | Source, Down | None now; never run Down on a hosted database (FOR THE DEPLOY step 8). |
| m3 | Minor | The `Entities.cs` comment says the table "is" a ledger on Azure SQL. That is true only after the migration is applied there; no hosted database has it yet. infra/README.md states this exactly. | Source | Optional wording fix later. |
| i1 | Info | The dead gate left containers `g1442-mssql-3` (127.0.0.1:9840) and `g1442-azurite` (9841) RUNNING, plus `g1442-mssql-1`/`-2` exited. I did not start them, so I did not stop them. | `docker ps -a`, lsof | Tuesday may `docker stop` them. |
| i2 | Info | Scratchpad `.../scratchpad/repo` and other files are another agent's (created 14:42-14:46). Not used; my work is under `.../scratchpad/v1442/`. | ls | none |

No Blocker: no path outside the lane, no secret, no name, no red at head or merge, no hosted touch, no deploy triggered by the merge.

Landing-order stack (the API branch 792c78f2 + #304 + this), SQLite `dotnet test HpsmPoc.slnx`: 4093 passed, 0 failed, 0 skipped (Rules 164, Assessment 300, Reporting 850, Feedback 478, Api 2301).

## Housekeeping
- I started `v1442-mssql`, `-head-a`, `-head-b`, `-main-a`, `-main-b` (SQL Server, each on 127.0.0.1:9842) and `v1442-azurite` (9843). All are stopped and none removed. `lsof` on 9842-9849 shows 0 listeners. Ports 9840-9841 are held by the dead gate's containers (i1).

## NOT RUN
- SQL Server shards at the landing-order stack. That stack's SQLite run is green (above). Hosted CI on the PR is the proof once it is rebased or updated after the API branch 792c78f2.
- shellcheck (not installed). No `*.sh` changed.
- gitleaks (CI's `secrets` job is the proof). My added-line secret scan is 0.
- CodeQL itself: hosted CodeQL on the PR is the proof. Pre-scan 0.
- Web jobs: no `web/` path changed.
- Anything on Azure SQL: the ledger is measured on SQL Server 2025 CU9 locally only.
- Builder red rows M2, M2+2b, M3, M4, M5, M7, M9, M10 (not re-run; R1-R4 cover each ticket's core).
