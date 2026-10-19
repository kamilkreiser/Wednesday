VERDICT: GO WITH NOTE at head c210733f6592bdbff88b1dae9263d80e74143361 (tier 2, round 1 of 2; landing tree 86281b3d808e57c23d280bc66fcf0efb5bfaf07d on develop a4187f0f66228603df211628d6d8ae239d6147d0; 0 blockers, 4 notes)

model: claude-sonnet-5-5 (Sonnet 5.5) -- gate BA1 -- PR #1640 -- wall-clock 16:36Z -> about 16:50Z (see the end)

## BLUF

- **The new file does what the author says.** On a real engine (PGlite 0.4.1, compiling, `tsc` rc 0 every time) AX1's GX1, GX2 and the delete `OR TRUE` each red exactly ONE cell (R1, R2, R3 respectively) and nothing else; the owner controls R1c/R2c/R3c stay green; the 16-cell mock file stays 16/0 under all three. Reproduced myself.
- **Two widenings of my own survive, both on DELETE** (N1): `OR organization_id IS NULL` and `OR length(organization_id) = 7` (the wizard's 'default' rows) on the delete UPDATE leave all 8 cells green, because R3 only ever targets A's row, never the seeded null-org or 'default' row. The same two widenings on list and notify ARE caught (R1, R2).
- 0 blockers. 4 notes. Head, develop and landing tree re-read at the end: unchanged and equal to the brief.

## Heads and landing (read at start and again before writing)

- `ls-remote`: `refs/pull/1640/head` = c210733f6592bdbff88b1dae9263d80e74143361; `refs/heads/develop` = a4187f0f66228603df211628d6d8ae239d6147d0. Both identical at start and end, equal to the brief.
- merge-base(develop, head) = a4187f0f... (head is a strict descendant). `merge-tree --write-tree develop head` = **86281b3d808e57c23d280bc66fcf0efb5bfaf07d** = head's own tree (`rev-parse HEAD^{tree}`). Two-dot and three-dot diffs are identical: 3 files, +219/-6.

## Notes

### N1 -- Delete widenings to null-org / 'default' rows survive the real-engine cells (and the mock file)

Mutants on the delete UPDATE (`WHERE id = $1 AND organization_id = $2`), tsc rc 0:

| mutant | new file | mock file |
| -- | -- | -- |
| OWN3 `AND (organization_id = $2 OR organization_id IS NULL)` | **8/8 survives** | 16/16 survives |
| OWN4 `AND (organization_id = $2 OR length(organization_id) = 7)` ('default' = 7 chars; UUIDs are 36) | **8/8 survives** | 16/16 survives |

Cause by reading: R3/R3c seed-delete only `ID_A_DEL`. The null-org row (`...220`) and the 'default' row (`...22d`) are seeded every cell but no cell ever sends DELETE at them. AX1's N3 says those rows must be "never deletable by anyone through the API". A suggested fix-forward cell: B (and A) DELETE the null-org and 'default' ids, then read `is_active` from the DB. The author's table names the generic `OR TRUE` and so does not claim this; it is a residual blind spot in the same class, not a defect of the PR. Test only.

### N2 -- "The only DDL" is not true: a second copy runs in production, and the new file does not read it

The file header says `06-m365-tables.sql` is "the only DDL for svc_teams_webhooks". `git grep` finds a second: `services/api-gateway/src/startup-migrations.ts:384` (a CREATE TABLE IF NOT EXISTS with the same columns) and lines 551-562 (four ALTER ... ADD COLUMN guards for is_active, last_sent_at, last_attempted_at, events). By reading, the columns and types are the same today (and the repo's `migrations/` has nothing: see Q2). But the cells can stay green if only the gateway's copy drifts. Same class as the author's own P0 argument, one source further out. Comment fix or a P0 assert against that file; not blocking.

### N3 -- PGlite is not a declared dependency of m365 (author discloses it)

`@electric-sql/pglite` appears in neither the root `package.json` nor `services/m365-integration/package.json` (positive control: the lockfile does carry it, 0.4.1, lines 3477/3485/7622, via a dev dependency chain). Removing the package makes the suite fail loudly (Q4), so it cannot silently skip; but a lockfile change that drops that chain turns this suite red for a reason unrelated to the code. Declaring it as a devDependency of m365 is the durable fix; the PR leaves it transitive by design.

### N4 -- Wrong-table-name reds the SUITE, not P0; and the notify spec sentences are accurate but not exhaustive

- Pointing the parse at a wrong table name (`svc_teams_webhooksX` on the CREATE only) makes `INDEX_DDL` execute against a missing relation in `beforeAll`: **Failed Suites 1, 8 skipped, rc 1** -- loud, but P0 itself never runs. Only a fully empty parse (table and index renamed) gets P0 and all 7 other cells to run and fail (8 failed). Either way the file cannot go green.
- Notify's new summary/description are true against the route (Q5). Not stated: only webhooks subscribed to the event receive it, and at most the row bound is notified (`truncated`). Not false; a reader could want it.

## Q1 -- AX1's mutants on the real engine (each: `tsc -p tsconfig.json --noEmit` rc 0, then new file and 16-cell file, `index.ts` restored and `cmp`-verified after each; script and logs in scratchpad)

Red cells are read from the `×` lines of the vitest verbose logs.

| mutant | tsc | new file (8 cells) | 16-cell mock file |
| -- | -- | -- | -- |
| GX1 list `AND (organization_id = $1 OR organization_id IS NULL)` | 0 | **R1 only** (7 pass incl. R1c) | 16/0 survives |
| GX2 notify `AND (organization_id = $3 OR TRUE)` | 0 | **R2 only** (R2c green) | 16/0 survives |
| delete `AND (organization_id = $2 OR TRUE)` | 0 | **R3 only** (R3c green) | 16/0 survives |
| OWN1 list `OR length(organization_id) = 7` ('default' rows) | 0 | R1 only | 16/0 survives |
| OWN2 notify `OR organization_id IS NULL` | 0 | R2 only | 16/0 survives |
| OWN6 notify `OR length(organization_id) = 7` | 0 | R2 only | 16/0 survives |
| OWN5 list `organization_id <> $1` | 0 | R1, R1c | T1, T2b, T13 |
| REG1 register stores `null` | 0 | R4 | T4, T6 |
| REG2 register: body org wins | 0 | R4 | T4 |
| **OWN3 delete `OR organization_id IS NULL`** | 0 | **none -- survives** | none -- survives |
| **OWN4 delete `OR length(organization_id) = 7`** | 0 | **none -- survives** | none -- survives |
| OWN7 notify drops `is_active = true` (not an ownership widening) | 0 | none | none |

The author's table reproduces row for row (GX1 R1, GX2 R2, delete R3, register R4; mock file survives the first three). The register has no "ownership read" (the INSERT binds the token's org); REG1/REG2 are my register mutants. First attempt of OWN1/OWN4/OWN6 used a quoted `'default'` literal inside a single-quoted JS string and did not compile (tsc rc 2); I rewrote them with `length(organization_id) = 7` and re-ran, only the compiling results are reported.

## Q2 -- The DDL is the real one

- P0 reads `docker/init/06-m365-tables.sql` at test time; the regexes extract the CREATE TABLE and CREATE INDEX statements.
- Mutations of that SQL in my clone (restored by `cmp` after each): (a) table name `svc_teams_webhooksX` on the CREATE only: rc 1, Failed Suites 1 (N4); (b) both table and index renamed (empty parse): **rc 1, all 8 cells fail incl. P0** (`expected '' to contain ...`, relation does not exist); (c) `last_attempted_at` line deleted: rc 1, 3 red (P0, R2, R2c); (d) index line commented out: rc 1, 1 red (P0). Restored: 8/8.
- Migrations: `git grep -il svc_teams_webhooks` over `Blockchain` at the head = 6 files (06-m365-tables.sql, startup-migrations.ts, index.ts, 3 test files); **0 in `migrations/`** (positive control: `svc_api_keys` hits 5 files there, and 41 of the 56 files contain ALTER TABLE). Only DDL alterations of this table are the api-gateway startup ALTERs (N2).

## Q3 -- The uuid shim

- `TABLE_DDL` and `INDEX_DDL` are file slices executed with `exec` unmodified; the shim is a separate prior `CREATE OR REPLACE FUNCTION uuid_generate_v4()`. Confirmed by reading and by removing the shim line: `error: function uuid_generate_v4() does not exist`, Failed Suites 1, 8 skipped -- so the shim is what lets the real DDL run, and the DDL is not edited around it.
- No cell depends on a generated id: every seed INSERT supplies its id, the route generates `crypto.randomUUID()` for register, and R4 reads the row back by the id the response returned. Restored by `cmp`; 8/8.

## Q4 -- Loud failure

- `node_modules/@electric-sql/pglite` renamed away: **rc 1**, `Test Files 1 failed (1)`, `Failed Suites 1`, `Error: Cannot find package '@electric-sql/pglite'`, and the summary line `Tests  no tests`. Restored: 1 passed, 8/8 (re-run after restore).
- The `Tests no tests` line is literally true but sounds like "nothing to run, fine"; the line above it (`Test Files 1 failed`) and the exit code are the signal. Anyone reading only the Tests line would be misled; CI reads the exit code.

## Q5 -- N2 spec change

- `check:openapi` (`generate-openapi -- --check` then `check:spec-examples`): rc 0, "CHECK PASS: on-disk YAML matches generated", 413 example blocks resolve. Control: planted " (planted)" in the new description in the .ts source: `--check` rc 1 "CHECK FAIL: generated YAML differs"; restored by `cmp`.
- YAML delta (`diff develop...head -- secuura-api.yaml`): one hunk at line 26158, 4+/3-, entirely inside the `/api/teams/notify` operation (summary + description). TS delta: summary, description, one comment.
- New sentences against the route: "active webhooks" -> `is_active = true`; "caller's own organisation -- taken from the signed token, never from the body" -> `requireCallerOrg(req, res)` runs before the body parse and `organization_id = $3`; "token with no organisation refused with 403" -> `requireCallerOrg` returns 403 FORBIDDEN 'Token carries no organisation'; "document lifecycle event (certified/revoked/verified)" -> `event` is any non-empty string (the Zod schema is `z.string().min(1)`), matched against each row's `events`; the three names are the registration defaults. Accurate; see N4 for what is not said.

## Q6 -- The 16-cell mock file and ks934

- The three-dot diff touches exactly the new test file, `m365-integration.openapi.ts` and the YAML: zero diff lines for `ks1673-teams-webhooks-are-bound-to-the-callers-organisation.test.ts` and `ks934-teams-notify-request-path-bound.test.ts`. Counts at the head: mock file 19 `expect(` / 16 `it(`; ks934 49 `expect(`.

## Q7 -- Landing

- The landing tree equals the head tree (merge-base = develop), so the suite at the head IS the suite at the landing. Full m365 suite: **15 files, 147/147, rc 0** (db.retry 8, exchangeTokenErrorMapping 6, ks1364-sites 6, ks1364-onedrive 4, ks1364-teams 6, ks1641 10, ks1671-drops-a-non-string-code 6, ks1671-reads-only-string 7, ks1673-m365-resources 36, **ks1673-teams-statements-on-a-real-engine 8**, ks1673-teams-webhooks 16, ks934 9, smoke 1, teamsNotifyRequest 8, tokenCrypto 16). Matches the author.
- Product `tsc -p tsconfig.json --noEmit` rc 0.
- The new file type-checked separately (KS-1090): override tsconfig (`extends ./tsconfig.json`, `include src/**/*`, `types node, vitest/globals`): **rc 0**; `--listFilesOnly` lists the new file **1** time in the override program and **0** in the default program (positive control for the KS-1090 gap).

## How it was run

- `git clone --shared` of Wednesday's cache clone into `scratchpad/gate_ba1/clone`, detached at the head; `npm ci --ignore-scripts` (1937 packages) and `npm run build` in `packages/shared`, all via `--prefix` or `node <clone>/node_modules/.bin/<tool> --root <m365 dir>`. Nothing ran from Wednesday's tree. No Docker, no rm, no push, no GitHub/Linear write, no `.env`.
- Mutation script `scratchpad/gate_ba1/mut.py` (each mutant asserts its pattern matches exactly once, restores from a copy and `cmp`s); logs `scratchpad/gate_ba1/logs/` (`m_<mutant>_{new,mock}.log`, `p0_*.log`, `noshim.log`, `loud.log`, `openapi_*.log`, `full_m365.log`). My only extra file in the clone is the untracked override `tsconfig.gate.json`.

## NOT RUN

- Preflight legs 3, 4, 8 (need the stack on Docker) and the four platform suites; leg 8 (served-spec) bears on the spec line.
- Real `uuid-ossp` (contrib) extension; the shim is what I tested.
- Real Teams webhooks, live Postgres (kintsugi/demo); production DDL actually applied by the gateway's startup migrations (N2 is by reading).
- The PR body and KS-1673 comment `ec2c962c...` (no GitHub/Linear access): the author's two "deviations" were assessed from the READY text and the code only.
- Stamp UPDATEs (`last_attempted_at`/`last_sent_at`, id-only): transitively bound, no route-level cell can kill a mutant there; none planted.

## Wall-clock

Start 16:36Z (brief read), final head/landing re-check 16:42Z for the last command, verdict written about 16:50Z: about 14 minutes.

34f28527c310203ebf00c13865ff5688e52eede1496b896333638577bac0f1bd
