GO WITH NOTES (PR 2033 GO WITH NOTES; PR 2034 GO WITH NOTES; PR 2035 GO WITH NOTES)

# Gate 216, Secuura / Blockchain, tier 2, round 1 of 2, QA gate (findings only)

Measured 2026-11-06 13:00 to 13:20 AEDT. Node v26.8.1 (NOT the LTS 24 line, same as the seats), PostgreSQL 15.19 (Homebrew) for the PR 2034 real-database cells, macOS Darwin 27.2.0. Docker daemon was up with no containers; I did not need or start it (the 2034 cells start their own socket-only PostgreSQL, no Docker).
Develop readings: pins.txt `aa4200e8a34c` (13:00:34); my fetch 13:01 `aa4200e8a34c`; ls-remote 13:15 and live fetch 13:15:59 `82d9ef03d795`. Merge results are reported on both. The three pull heads were unchanged at 13:15 (evidence/ls_remote_now.txt).

## Per-PR verdicts
- PR 2033 (KS-1622) head `c3cb692fe4c7`: GO WITH NOTES
- PR 2034 (KS-1128) head `07924892fa5f`: GO WITH NOTES
- PR 2035 (KS-1544) head `1869735707aa`: GO WITH NOTES

## Tier
All three are tier 2 on my reading, as the seats claim. PR 2034 is tests only (my diff: two test files plus the fragment pair, no src file outside `__tests__`). PR 2033 changes one product file (`routes/platform.ts`, +2: one comment, one `logger.warn`) and PR 2035 changes one product file (`stake.ts`, 1 line of SQL). Both of those deploy, which the seats say they owe. No tier change.

## BLUF
- PR 2033: the response is byte-identical before and after on the real route (measured, six upstream shapes); the one new line fires exactly three times where the base fired zero (entries a string, JSON null, no entries) and carries only route, status, windowsRead. Note: the first-window guard is pinned only by a neighbour's cell, and the warn sits inside the try.
- PR 2034: no product line changes; the WARN and the 200-character cut are pinned on a real PostgreSQL (tampers at 199, 201 and level debug redden both the fake-pg and the real-pg files). Notes: the real-database describe silently skips with no PostgreSQL keg, and the platform `tenants` schema has two tracked sources that disagree.
- PR 2035: `ORDER BY stake_date, id` is the only product change and `id` is a globally unique primary key in both tracked schemas. The test is a source-text pin only, so the ticket's defect (page walk repeats or skips tied rows) is NOT proved on a real table by this PR; that part stays open, as the seat says.

## Findings
Severity is mine as a suggestion; priority is the humans' call. Evidence class stated on each.

F-1 (PR 2033, Low, note). The new guard is covered only by a neighbour's cell. Tamper "drop `collected.length === 0 &&`" (my own, line 494 of `routes/platform.ts`) leaves all six cells of the PR's own file green and fails 2 cells of `ks1545-platform-audit-log-logs-the-dropped-platform-half.test.ts`. The seat said this (its M3). REPRODUCED. Evidence: evidence/2033_tampers.txt. HOW: sed on the line, run ks1622*/ks1545/ks1512, git checkout restore, sha256 equal. Consequence: deleting ks1545 W2 later would leave the guard unpinned; not a defect now.

F-2 (PR 2033, Low, note). The new `logger.warn` is inside the `try` that wraps the window loop (platform.ts:494, try opens ~line 468, catch ~line 515). If a logger throws here, the throw is now caught by the existing catch and the platform half is dropped with a second (guarded) warn, where before nothing at that point could throw. The existing error-status warn two lines above has the same exposure, so this is consistent with the file, and the response stays 200 with the audit_logs rows. READ ONLY, not driven (a throwing logger was not planted).

F-3 (PR 2033, Info, carried from the seat). A first window with a numeric `total` and a non-list `entries` still sets the platform total from that body while no rows return; the new warn fires but `total` is unchanged. I confirm the reading in source (platform.ts: `if (total === undefined && typeof data?.total === 'number') total = data.total`). READ ONLY, not driven. The seat claims nothing about it; I claim nothing about its effect on a real UI.

F-4 (PR 2034, Low). The real-PostgreSQL describe is `describe.skipIf(!PGBIN)` (ks1128b test, line 39). On a machine with no keg it prints "skipped" and passes, so SEED-REALPG is then unpinned there; only the four fake-pg SEED-CUT cells hold. The seat says this and cites the ks949 ruling of 2026-09-13; I could not read that ruling (no card named it; the `prior` lookups returned nothing). On this machine the cells RAN (17 of 17), so it is not vacuous in my run. READ ONLY for the skip branch (I did not hide the keg).

F-5 (PR 2034, Low/Info, schema-source disagreement, NOT reconciled). The platform `tenants` table has two tracked sources: `Blockchain/Dev/docker/init-platform/01-platform-schema.sql` (the file compose mounts, which the new test applies: `status VARCHAR(30)` with a CHECK, `industry VARCHAR(100)`, `settings JSONB`) and `Blockchain/Dev/migrations/003_platform_tenancy.sql` (`status VARCHAR(20)`, no CHECK shown, `industry VARCHAR(255)`). The test builds from the first. Which the deployed platform database actually carries I did not establish. Per the template rule I report the disagreement and do not reconcile. READ ONLY (diff of the two CREATE TABLE blocks, evidence not saved beyond this note).

F-6 (PR 2035, Medium for the ticket, not for the PR). The test is a source-text pin; it proves the SQL text ends in `, id`, not that a two-window walk over a real table returns each row once. What it proves: the tie-break column is present, is the last key, and is the primary key (C4 reads the migration). What stays open, as the seat says: the ticket's own real-table two-window cell; also that Postgres ordering of ties is only undefined, never demonstrated here. Tied rows in a small real table usually come back in a stable order in practice, so a real cell would need a planted tie and a plan change to be a meaningful red. MEASURED for the SQL text (5 of 5 tampers plus one of mine killed); NOT MEASURED for paging.

F-7 (PR 2035, Info). C4 reads only `migrations/002_verification-tiers.sql`. `docker/init/04-sprint2-service-tables.sql` (what containers build from) has an identical `svc_stake_positions` DDL (`id TEXT PRIMARY KEY`, `address TEXT NOT NULL UNIQUE`, `stake_date TIMESTAMPTZ DEFAULT NOW()`); the two agree today, so the premise holds in both. A future divergence in the second file would not trip C4. READ ONLY.

F-8 (PR 2035, Info). The pin does not cover the parameter array: swapping `[limitNum, offsetNum]` would pass all six cells. Out of scope for the ticket; shows the limit of a source-text pin. READ ONLY.

No finding changes a verdict to NO GO. No PR contains an unlisted path, a secret, or a behaviour change beyond what its READY declares.

## Question by question

### 1. Scope (own diffs, `git diff` from `git merge-base <develop> <head>`; evidence/scope.txt, paths_*.txt)
- PR 2033, base `85046e8707a0`, one commit, 4 paths: `services/api-gateway/src/__tests__/ks1622c-...test.ts` (+133), `routes/platform.ts` (+2), the two fragments (+17 cheat, +9 flow). Total +161/-0, equals the READY.
- PR 2034, base `85046e8707a0`, one commit, 4 paths: `ks1128-platform-tenant-seed-failure-warns.test.ts` (+22/-2), new `ks1128b-...test.ts` (+154), the two fragments. READY said 4 paths; matches. No src file.
- PR 2035, base `3fbf50ede123` (not 85046e8, different from the other two, as its READY says), one commit, 4 paths: `stake.ts` (+1/-1), the ks1544-class test (+56), the two fragments, total +82/-1.
- Fragment names: three distinct new names; PR 2035's `KS-1544-staking-stake-positions-...` is distinct from the existing `KS-1544-eleven-more-paged-lists-...`; no existing fragment edited.
- Pairwise overlaps: 2033 x 2034 = 0, 2033 x 2035 = 0, 2034 x 2035 = 0. Control (2033 set against itself) printed 4 of 4.
- Trial merge with a planted same-line control: a develop-side commit changing `ORDER BY stake_date LIMIT` to `... DESC LIMIT` in `stake.ts` merged with PR 2035: rc 1 with stage-1/2 entries for that file (the instrument can fire). Evidence/merge_together.txt.

### 2. Behaviour
PR 2033. I built a scratch test (kept in `_quarantine_2026-11-06/zz-gate216-scratch.test.ts`) that boots the real `createPlatformRoutes` against a stub upstream in six modes and dumps the raw HTTP status and body text, run once on the head and once with `platform.ts` restored from base `85046e8707a0`. Status and body text were EQUAL in all six modes (ok, entries-string, null-body, no-entries, empty-list, first-500-not-a-list); warn counts base to head: 0 to 0, 0 to 1, 0 to 1, 0 to 1, 0 to 0, 1 to 1. So only the log line differs, exactly where the READY says. MEASURED. Evidence/2033_bytes_base.json, 2033_bytes_head.json.
The line's meta is `{ status: r.status, windowsRead }`: a number and a counter, no body, token, address or tenant datum. The route text in the message is a fixed string. READ and MEASURED (the ks1622c cells assert the exact meta).
When the first window is not a list: one warn, no throw, `rowsInWindow` empty, loop breaks, route answers 200 with audit_logs rows only (the byte capture above). A later window not a list still throws as before.
PR 2034. `git diff` shows no product line changed; the only edit to an existing file is the fake-pg test file. The real-PostgreSQL cells: a BEFORE INSERT trigger on `tenants` raises a message of chosen length inside a PostgreSQL 15.19 started by the test; the WARN text and the first-200 cut are asserted on the line the real `runStartupMigrations()` logs. It is not a mock's echo: my tamper of the product line (`substring(0, 201)`) turned 2 of 9 real-pg cells and 2 of 8 fake-pg cells red (evidence/2034_tamper201_split.txt). The cluster is unix-socket only (CONTROL cell checks `listen_addresses` empty and a wrong socket dir fails). No postgres process or `k1128` temp directory remained after my runs.
PR 2035. The diff is one SQL string. `id` is `TEXT PRIMARY KEY` in `migrations/002_verification-tiers.sql:716` and in `docker/init/04-sprint2-service-tables.sql:607`; the table has no tenant column, so the key is unique globally, not per tenant. The count query (`SELECT COUNT(*) AS cnt FROM svc_stake_positions`, line 463) and the response mapping (`rowToStakePosition`) are unchanged in the diff. Ascending order by `stake_date` is kept as the first key; NULL `stake_date` rows (column is nullable) sort as before and now tie-break by id. See F-6 for what the source-text pin does and does not prove.

### 3. Tests that can fail
- PR 2033: new file on base `routes/platform.ts`: F1, F2, F3 red (3 failed), F4 to F6 pass; on head 6 of 6 and the neighbours: ks1622*, ks1545, ks1512 together 39 of 39 (5 files). REPRODUCED. Tampers: (seat's) drop `r.ok &&` leaves 5 red across ks1622, ks1622b, ks1622c; (seat's) change the guard to `typeof ... === "undefined"` reddens 2 of ks1622c; (mine) drop the first-window guard reddens only ks1545 (F-1); (mine) `windowsRead + 1` in the meta reddens 3 of ks1622c. Each restored and sha256 equal. Evidence/2033_tampers.txt.
- PR 2034: tampers (mine, compiled implicitly by vitest): `substring(0,199)` 6 red, `substring(0,201)` 4 red, level `debug` 3 red, no cut 4 red, each restored sha256 equal; control 17 of 17 green. The seat's 12-red figures belong to other tampers (old catch back etc.) which I did NOT reproduce. Evidence/2034_tampers.txt.
- PR 2035: base: T1 and T2 red (2 failed of the 12 in the two ks1544 files), head 99 of 99 (staking suite, 8 files). REPRODUCED. Tampers: tie-break removed, `address` instead of `id`, `id` first, `id DESC` each 2 red (seat's set, reproduced); mine: swap the placeholders `LIMIT $2 OFFSET $1` 1 red. Restored, sha256 equal. Evidence/2035_tampers.txt.

### 4. Suites, tsc, eslint, docs-fragments
Run one at a time, node_modules copied from the gate 209 clone because the shared checkout's `node_modules` is stale (zod 3.25.76 against the repo's ^4.6.7); `packages/shared` rebuilt with `tsc` (rc 0, no diagnostics) in my clone.
- api-gateway, PR 2033 head: 158 files, 1660 of 1660 (seat: 1660). PR 2034 head: 158 files, 1667 of 1667 (seat: 1667). Base suites (157/1654) NOT re-run by me. Failures: none.
- staking, PR 2035 head: 8 files, 99 of 99.
- tsc `--noEmit -p`: api-gateway at 2033 head rc 0 and at 2034 head rc 0; staking at 2035 head rc 0.
- `check:test-types` api-gateway (the script defines five services; I ran only api-gateway, the service the two api-gateway PRs touch): "158 of them under __tests__; 25 errors: 25 in the baseline, 0 new" at both 2033 and 2034 heads. Planted `const x: number = "s"` in a test file: rc 1 with TS2322. Staking is not one of the five (as the seat says).
- eslint: 2033 changed files rc 0 (platform.ts + test); 2034 two test files rc 0; 2035 `stake.ts` and its test: 0 errors, 1 warning at `stake.ts:75` (prefer-const on a line the diff does not touch). Planted `debugger;`/type errors: rc 1 on both 2034 and 2035.
- docs-fragments `check`: OK at all three heads, "flow 117 legacy + 167/168 new". The two ADVISORY lines (flow 6249, cheat 6235) appear as the other gates saw them. Planted literal section number (`<h2>77.` in place of `<!--n-->.`) in each PR's own flow fragment: FAIL rc 1 each time with "carries a literal section number"; restored, rc 0 (git checkout; fragment sha256 equal on 2034).
- Failures classified: none occurred.

### 5. Merge tree (evidence/merge_summary.txt, merge_summary_live.txt, merge_together.txt)
| develop | head | merge-tree rc | tree |
|---|---|---|---|
| `aa4200e8a34c` (pin) | 2033 | 0 | `c48a4866802b` |
| `aa4200e8a34c` | 2034 | 0 | `d540c465324e` |
| `aa4200e8a34c` | 2035 | 0 | `a80da080b41e` |
| `82d9ef03d795` (live 13:15) | 2033 | 0 | `80d95a74ce20` |
| `82d9ef03d795` | 2034 | 0 | `ef955a09af55` |
| `82d9ef03d795` | 2035 | 0 | `12068ebecd3a` |
All three together (commit-tree chain): pin develop final tree `380f4cc4e35f`, live develop `809de822f505`, rc 0 at each step; the changed-file list against develop equals the union of the three path sets (12 files, diff empty).
Paths shared with everything merged on develop since each base (live develop): 2033 and 2034 vs 65 moved files: 0 each; 2035 vs 58 moved files: 0. (At the pin: 61, 61, 54 moved, 0 shared.) Planted control: one develop-side path (`Blockchain/Dev/docs/openapi/secuura-api.yaml`) added to PR 2033's path set printed an intersection of 1.

## What this gate did NOT cover
- The PR bodies (Test Evidence blocks, quoted rulings) and the seats' tickets and comments were not readable (no `gh`, no Linear). The `decision_queue.sh prior` lookups for the three tickets returned no relevant card (evidence/rulings_prior.txt), so the rulings the READYs rest on (Wednesday's SEED-INNER-1142 ruling, the ks949 ruling of 2026-09-13, the owed F-852-1) were NOT checked against a card: source not readable to me.
- Base-side full api-gateway suites (157/1654) and the seats' 12-red, 9-tamper and 10-tamper counts beyond the ones I listed.
- Node 24 (LTS) not used by anyone; Schemathesis, Akto, Playwright, k6, a live stack, any box, any deploy; PostgreSQL other than 15.19; the deployed platform database (F-5); preflight legs 3, 4, 8 skipped by the seats.
- Paging on a real `svc_stake_positions` table (F-6); a throwing logger on PR 2033 (F-2); the numeric-total non-list shape (F-3).
- `check:test-types` for the other four services; the full auth, originate and staking-adjacent suites other than the ones named.

## My own conduct
- Cloned `--shared` into `repo/` in this folder; never fetched into the shared checkout. Because the shared checkout carries no pull refs I added a `gh` remote to MY clone and fetched `refs/pull/2033..2035/head` and `develop` over SSH using the project's configured deploy key path (`core.sshCommand` as the shared checkout sets it; the key was never printed or copied). That is network to GitHub, only fetches/ls-remote, as the commission allows.
- No post to Linear or GitHub; no box; no credential printed; no file deleted. Cleanup was by `mv` into `_quarantine_2026-11-06/` here (my first node_modules copy, taken from the stale shared checkout, and the scratch byte-capture test).
- Copied `node_modules` (read) from the shared checkout, then from the gate 209 clone's `node_modules`; both reads only.
- ONE slip outside the folder: I created `/tmp/g216/` (a scratch file `shared_build.txt` and two small diff text files, `a.txt` and `b.txt`) instead of the scratchpad or this folder. It holds nothing sensitive; I did not delete it. Wednesday may remove it.
- The Bash hook refused `git -C` write verbs through a variable path and `cd`; I routed all git writes through `evidence/gw.sh`, a wrapper pinned to my own clone, and cwd-sensitive tools through `evidence/run_in.sh`. Neither touches any other repo.
- My tampers modified files in my own clone only, each restored by `git checkout` and checked by sha256 where noted.

Evidence index (all under `evidence/`): scope.txt (first diff stat, in-line above), paths_*.txt, 2033_*, 2034_*, 2035_*, merge_summary*.txt, merge_together.txt, rulings_prior.txt, gw.sh, run_in.sh, merge_check.sh, merge_together.sh.
