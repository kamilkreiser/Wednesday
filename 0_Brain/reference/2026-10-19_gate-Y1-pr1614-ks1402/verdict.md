VERDICT: GO at head ddd54b8363946511acae231aa1889acaadf5912e (develop 722e07f19cee683ea037930e601e380a9491f7b5, both re-read 07:47:12Z) - 0 blockers, 5 non-blocking notes

# GATE Y1 (re-run): PR #1614 (KS-1402), Opus, tier 1, round 1 of 2

Gate seat: Y1 re-run, commissioned by Wednesday. The first Y1 run died in the 17:31 AEDT reboot and wrote no verdict. This one is independent: its own clone, its own PostgreSQL, its own runs.
- Head `ddd54b8363946511acae231aa1889acaadf5912e`, tree `31133804bddcc5ca6db1b593edd9b59904a1345b`.
- Develop `722e07f19cee683ea037930e601e380a9491f7b5`.
- Both read by `ls-remote` at 07:37:10Z (start) and again at 07:47:12Z (before this verdict). Neither moved.
- Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/y1r/` (`repo/` clone, `wt/` worktree at the head, `logs/`, `setup_pg.sh`, `run_cells.sh`).
- Nothing was written under `!CODING`, and nothing went to GitHub or Linear. The only operations run against the project repo were `ls-remote` and a read-only `git clone` source.

## BLUF
**GO.** I found no blockers.
- The fix does what it claims in both tenancy modes, and every cell turns red for the stated reason when its half of the fix is removed.
- 052 has exactly 043's shape and is idempotent.
- No code anywhere in the repo reads `custody_events.transferred_by_id`, so a NULL actor cannot reach a reader that dereferences it.
- The landing is clean: merge-tree = the head tree, the 3-dot diff is the 4 files, unit 122/1481, tsc rc 0.

Five non-blocking notes are listed below.

## Q1. Is 052 safe and exactly 043's shape?  YES
- **Line by line against 043:** the same structure. There is one `ALTER TABLE … ALTER COLUMN … DROP NOT NULL`, then one `COMMENT ON COLUMN` built from the same two-literal concatenation. The header is the same ("Attribution", "Reversible: forward-only"), with the table, column, ticket and the 039/041/043 lineage substituted. There is no DO block, no data change and no down path. This matches 043.
- **Idempotent:** I applied 052 twice more by hand to a database that already had it. Both runs returned rc 0 (`ALTER TABLE` / `COMMENT`). Positive control: an `ALTER … DROP NOT NULL` on a missing column returned rc 1 with an ERROR, which shows the instrument reports failures. Afterwards `is_nullable = YES` and the column comment is present.
- **Runner pickup:** both runners sort `migrations/*.sql` lexically and track by filename in `_secuura_migrations`:
  - `scripts/run-migrations.sh` (the loop at :149);
  - api-gateway Stage 1 (`startup-migrations.ts` :92-97, `.sort()`).
  052 is the only `052_` file and sorts after `051_`. The name has no "platform" in it, so both runners route it to the main DB, which is where `custody_events` lives (023). On a fresh cluster (`docker/init/0[1-9]-*.sql`, then all 54 migrations in lex order, applied as run-migrations.sh does): applied=54, failed=0, `transferred_by_id|YES`. The same run excluding only 052 gave applied=53 and `NO`.
  Stage 2's legacy inline `CREATE TABLE custody_events (… NOT NULL)` (:600-629) is guarded by `IF NOT EXISTS` and runs after Stage 1 (:1046), so it is a no-op wherever 023 or 052 has already run.
- **Readers of the column:** I searched case-insensitively for `transferred_?by` across the whole tree at the head, including the frontends, docs, prisma and every service. The hits:
  - `migrations/023` and `052`;
  - `startup-migrations.ts:614` (DDL);
  - `documents.ts` (the INSERT, the comment and the bind);
  - two integration tests;
  - `BACKLOG.md`.
  No SELECT, join, report, export or Verify page reads it, and Prisma does not model `custody_events`.
  A second search, PCRE `(from|join|update|into)\s+custody_events`, finds only the route's INSERT plus test setup and teardown.
  - Positive control for this search: `from\s+shares` hits shareRepo.ts, gdprService.ts and the ks1263 test.
  - Note: my first attempt used `\s` in git-grep ERE, which returned a FALSE zero. I caught it with that control and redid the search in PCRE.

## Q2. Is (a) right for every caller shape?  YES
`toActorUuid(principalId, resolvedUserId)` (`utils/principalId.ts`): it returns `resolvedUserId` if that is a UUID, else `principalId` if that is a UUID, else null. `checkOnBehalfOf` → `extractOnBehalfOf` refuses `onBehalfOf` from any non-connector caller with 400 (`provenance.ts`, the `role !== 'connector'` check). `resolveOnBehalfOf` returns a same-org `users.id`, null, or a 403 for a cross-org user.

| caller shape | result (by code) | result (measured, both modes) |
|---|---|---|
| interactive user | own uuid (onBehalfOf impossible: 400) | CONTROL: `by = INTERACTIVE_ACTOR` |
| connector + resolved same-org onBehalfOf | that user | same-org cell: `by = SAME_ORG_PERSON` |
| connector + unresolved onBehalfOf | NULL | S-shape cell: `by = null` |
| bare connector | NULL | bare cell: `by = null` |

This is identical to the /share site (`documents.ts:2269`, `toActorUuid(user.id, shareObo.resolvedUserId)`). The bind is computed after holder resolution and the document read, and before `withTenant`. No other line in the handler changed (+8/−1).

## Q3. Attribution is not lost.  VERIFIED (code + runs)
`recordOnBehalfOf` returns early when `!checked.obo`. Otherwise it writes an `action_provenance` row with `connectorId = req.user.userId` and `resolvedUserId`.
- **Measured in both modes:** S-shape → one row `{connector_id: connector:platform-s:<run>, resolved: null}`; same-org → one row `{connector_id, resolved: SAME_ORG_PERSON}`; bare → zero rows after the full 2 s window. In every cell, `provenanceFailures()` was empty.
- The bare-connector gap is pre-existing and documented: BACKLOG.md:363, now extended to name `/transfer-custody`.

## Q4. Red-first, and the controls are real.  VERIFIED
These runs used two scratch PG 15 clusters, 127.0.0.1:55412 (with 052) and :55413 (without 052). Both were in the 55410-55419 band and away from 55415. The product connection was `secuura_app` (rolsuper=f, rolbypassrls=f; the SETUP cell passes). MT=true pointed `TEST_PLATFORM_DATABASE_URL` at the same DB, and the suite's own guard refuses to run if the tenant did not load into the pool manager.

| run | MT=false | MT=true |
|---|---|---|
| head code + 052 | **6/6 pass** | **6/6 pass** |
| develop `documents.ts` (blob 44884629) + no 052 | 3 RED fail, `22P02 invalid input syntax for type uuid: "connector:platform-s:…"`; 3 controls pass | same 3 fail on the same message |
| revert (a) alone: develop `documents.ts` + 052 | same 3 fail on 22P02 | same |
| revert (b) alone: head code + no 052 | S-shape and bare fail on `23502 null value in column "transferred_by_id" … violates not-null constraint`; same-org passes | same (message only; see note N4) |
| **Y1 mutation 1:** `toActorUuid(...) ?? resolvedHolderId` | S-shape and bare red on `"by": null` vs the holder uuid; the other 4 pass | same |
| **Y1 mutation 2:** fabricate an `obo` for a bare connector in `recordOnBehalfOf` | ONLY bare red, at `expect(await provenanceRows(0)).toEqual([])` | same |

After every swap or mutation, I restored `documents.ts` and checked it against the committed blob `ddceb43f63d08fdaa40e8013a7c266a449cb13d3` with `git hash-object`. The worktree ended clean at `ddd54b836394`.
The author's controls also reproduce: revert (b) gives 23502 with same-org green, and revert (a) gives 22P02. I did not re-run the author's M3 or provenance tamper; my two mutations replace them.

## Q5. No widening.  VERIFIED
- The KINTSUGI cell (connector, unknown holder by email → `404 RECIPIENT_NOT_FOUND`, zero custody rows, owner still NULL) passes at develop and at the head, in both modes.
- The documents.ts diff is one `const` and one bind, both after the holder 404s. Nothing creates, stubs or inserts a holder or user.

## Q6. Landing.  CLEAN
- `git merge-tree --write-tree origin/develop pr/1614` gives `31133804bddc…`, identical to the head tree. Develop is the merge base, so the landing tree equals the head tree.
- The 3-dot file list is exactly the 4 files: `BACKLOG.md`, `migrations/052_…sql`, `ks1402-…integration.test.ts`, `routes/documents.ts` (+395/−3).
- Originate unit suite (`npm test`, landing/head tree): **122 suites / 1481 tests, all pass**. With develop's `documents.ts` it is also 122/1481. That is expected, because the new file is an integration test and the unit config excludes it.
- `tsc --noEmit` (originate): rc 0. Positive control: a planted type error gives rc 2 with TS2322.
- Extra: `ks1263-multi-write-rolls-back.integration` passes 11/11 in each mode at the head.

## Non-blocking notes
- **N1. Per-tenant databases** (`startup-migrations.ts:1250`, KS-1055) receive only CORE_MIGRATIONS, and Stage 2 creates `transferred_by_id NOT NULL`. So 052 never reaches a per-tenant DB, and a connector transfer there would still 500, now with 23502. 043 has the same limitation for shares. The author discloses it, and KS-1055 is dormant.
- **N2.** `publishEvent('document.ownership_transferred', { transferredById: user.id })` (`documents.ts:1906`) carries the raw `connector:<id>` principal. That path is reachable for connectors for the first time. No consumer of the event exists in the repo (search: publish site plus test mocks only), so nothing breaks. Anyone adding a consumer should know the value is not a UUID.
- **N3. Deploy:** the api-gateway image also bundles `migrations/` (`services/api-gateway/Dockerfile:75`), and Stage 1 applies new files from it. The PR's Deploy note names the migrations image. Rebuilding either path lands 052. Check `is_nullable = YES` afterwards, as the author says.
- **N4.** In MT=true, the pg-pool branch's logged error carries the message but no SQLSTATE field. In that mode, 22P02 and 23502 are identified by their message text ("invalid input syntax for type uuid" / "violates not-null constraint").
- **N5.** The argument order of `toActorUuid` is effectively symmetric here, because `onBehalfOf` is connector-only and a connector principal is never a UUID. This is not a defect. It does mean a swapped-argument mutation would be equivalent and would not red any cell, which is why I did not use one.

## Not run (named)
- `scripts/run-migrations.sh` itself was not run, because the session forbids `cd` and the script uses relative `migrations/*.sql`. I emulated it file for file in `setup_pg.sh`: the same psql `ON_ERROR_STOP` `-f` per file in lex order, and the same tracker.
- I did not boot the api-gateway Stage 1/Stage 2 runner. Its ordering was read from code only.
- I did not re-measure the Kintsugi `65d7722f8` dynamic claim.
- Not run: ESLint, the push preflight, Schemathesis, Akto, Playwright, k6, and a live S↔K pair. There was no stack, and Docker is forbidden.
- I did not re-run the author's M3 or provenance-tamper controls (replaced by Y1 mutations 1 and 2).
- I did not check the outer-catch rollback directly on the red runs. The red cells fail on the status assertion before the owner read.

Both scratch clusters are stopped (`pg_ctl stop`). Their data directories are left in the scratch, which has no `rm`.
89d8879cf8f39bda704702d5dbc34b8c95590c93379e3a093d1dacbb55c8f58a
