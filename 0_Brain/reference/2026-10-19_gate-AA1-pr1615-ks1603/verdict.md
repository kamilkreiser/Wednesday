VERDICT: GO WITH NOTE at head 4db96203546b76e383b40b4e3806cca8ba4171b0 (tier 1, round 1 of 2; landing tree 8b67dde74820b61e746b2837f32f726b965755ca on develop 80868551e67934cb951d28eec44ce3bdf835944c; 0 blockers, 5 notes)

# GATE AA1: PR #1615 (KS-1603), the interim anchor-write ownership check

Gate: AA1, Opus, tier 1, round 1 of 2. Independent. Commissioned by Wednesday's GATE_BRIEF.md. The author's claim (J15_READY_0759Z.txt) was treated as claims to verify.
Run: 2026-10-19 08:01Z to 08:17Z. Everything ran in my own clone at `scratchpad/aa1/repo`. Nothing was written under `!CODING`, and nothing was written to GitHub or Linear.

## Heads, read at start and again before this verdict

| read | develop | #1615 head |
|---|---|---|
| ls-remote 08:01:07Z (start) | `31cfb44dce840caf8ae8a6a4c1468efa7e78e247` | `4db96203546b76e383b40b4e3806cca8ba4171b0` |
| ls-remote 08:14:07Z (pre-verdict) | **`80868551e67934cb951d28eec44ce3bdf835944c`**: develop MOVED during the gate | `4db96203546b` (unchanged) |
| ls-remote 08:17:07Z (final) | `80868551e679` (stable) | `4db96203546b` (unchanged) |

- `31cfb44d` = "Refs KS-1195: send the one-hour window explicitly". Parent `722e07f19cee`. Committed by kksecura at 18:59:50+11:00. Its body names "#1613's first round" and it touches only `api-gateway/src/routes/platform.ts` and one api-gateway test. That fits #1613 merging. I did NOT confirm the PR number through the GitHub API.
- `80868551` = "Refs KS-1402: a Platform-S custody transfer whose holder resolves is recorded". Parent `31cfb44d`. Committed at 19:03:49+11:00. It touches BACKLOG.md, a new migration `052_custody_events_connector_actor.sql`, one originate test and `originate/src/routes/documents.ts`.
- Between the two develops: 0 files under `services/anchoring`, `packages/` or `package-lock.json`. Control: the same diff over `migrations/` reads 1.
- **The author's predicted landing tree `1cd95487cc12` (on `722e07f19cee`) is void, as the brief said.**
  - Landing on `31cfb44d`: `git merge-tree --write-tree` gives rc 0 and tree **`e3af797c6a73bc2fff27ef5f838b1db268e7f1fb`**, with no conflicts.
  - Landing on `80868551` (live): rc 0 and tree **`8b67dde74820b61e746b2837f32f726b965755ca`**, with no conflicts.
- I measured every suite on BOTH landing trees. The figures are identical.

## Q1: Does the bypass stay inside its transaction? YES

**Code read.**
- `readIdOwners` runs `SELECT set_config('app.tenant_scope_bypass','platform_admin', true)` and then ONE `SELECT external_id, id, tenant_id FROM documents WHERE external_id = ANY($1) OR id = ANY($2::uuid[])`, inside `db.transaction()`.
- `db.transaction()` (db.ts:53-66) is BEGIN, fn, COMMIT. Any throw gives ROLLBACK and then rethrows. `release()` is always called. `is_local = true` means the setting dies at COMMIT or ROLLBACK.
- Every `set_config` in anchoring/src is `true`: guard :254 and :499, provenance.ts:84. Grep with the instrument live: 3 hits.
- The `documents` policy reads (measured): `(... app.current_tenant_id ...) OR current_setting('app.tenant_scope_bypass', true) = 'platform_admin'`. That is FORCE RLS, `t,t`.

**Author's D1:** green at both landing trees.

**My own cells (G1, G2), pinned to the SAME pooled connection by backend pid.** I spied on `pool.connect`, in both its callback and promise forms, recorded the `processID` of every client the product checked out, and then checked out exactly that pid again.
- **G1b.** A real guarded write: tenant A's flat anchor through `POST /api/anchors`, giving 202. On every connection that write used, the fresh check was run as `current_user = secuura_app` against ANOTHER tenant's (B's) `documents` row:
  - GUC = `<unset>`
  - plain read = **0 rows** (refused by FORCE RLS)
  - positive control on the same connection (BEGIN + local escape) = **1 row**
  - after COMMIT = **0 rows** again
- **G1c.** The same check after a REFUSED write (B onto A, 403) gave the same result: `<unset>`, 0 / 1 / 0.
- **Discrimination.** I planted a mutation, `set_config(..., false)` at guard :499 (session-scoped). G1b, G1c and the author's D1 all go RED: `expected 'platform_admin' to be '<unset>'` and `expected 1 to be +0`. So the cells detect exactly the blocker class. I restored the file and proved it byte-identical by sha256 (`882cd948d7e6cfd5…`).

## Q2: Is the narrowing right for every caller shape? YES

| shape | instrument | result |
|---|---|---|
| same tenant | A2, B2, AA1 G4a (own tenant via `external_id`) | 202, row written (count +1) |
| another tenant's document | A1, A3 (12-column fingerprint unchanged), AA1 G3 flat via `external_id` and via UPPERCASE pk | 403 `FORBIDDEN`. Body never contains the owner tenant id |
| `document_id` names NO document (S flat) | A4, A5 (retry of the same id) | 202, as develop |
| batch with a mix | B1. AA1 G3 counted **all** `anchor_store` and `anchor_batches` rows before and after, for foreign FIRST, foreign LAST and foreign as UPPERCASE pk | 403, and totals **unchanged** in every case. Control G4b: an all-unknown batch moves totals by exactly +2 anchors and +1 batch |

- The batch route accepts uuid ids only (`z.string().uuid()`, index.ts:279). An `external_id`-form id is refused 400 by the schema before any write, with totals unchanged (G3). The `external_id` arm is therefore reachable on the flat route only, and it is refused there (G3).
- The mutation that drops tenant equality (the `foreign` finder never matches) turns A1, A3, B1 and AA1's four G3 cells RED. All other cells stay green.
- **Code note: no attacker-induced probe fault.** Can an id make the `::uuid` cast throw, which would fail open? No. `UUID_SHAPE` is strict hex 8-4-4-4-12, and the flat schema's `documentId` regex is equally strict. No id can pass the schema, fail the cast, and still equal a victim row's `document_id`.

## Q3: Fail-open is bounded. YES

- **Author's P1–P4:** green at both landing trees.
  - P1: the read really throws against `127.0.0.1:1`.
  - P2: the gate returns `{allow:true, reason:'ownership-probe-unavailable'}` and logs exactly 1 warn containing `KS-1603` and `fail-open`.
- **My planted fault (G2), a harder case than P2.** The fault fires INSIDE the probe transaction, AFTER `set_config` has run. The probe client's `query` was wrapped to throw on `FROM documents d`. Results:
  - The call is tenant B onto DOC_A, which would otherwise be refused. With the fault it returns `allow / ownership-probe-unavailable`, with 1 warn naming KS-1603 and fail-open.
  - The query log shows the escape was set and then `ROLLBACK` ran.
  - On that same pid afterwards: GUC `<unset>`, RLS 0 / 1 / 0.
  - Control: the same call without the fault gives `allow:false`.
- **Mutation (catch made fail-closed):** P2 and G2 go RED. G4a and G4b also go RED, but only as a cascade: under the mutation, G2 exits before it un-wraps its client.

## Q4: Red-first and controls are real. YES

- The two product files were parked at develop's copies. The stat is `2 files changed, 1 insertion(+), 290 deletions(-)`, the exact inverse of the PR. Test files were left in place.
- Result: **8 failed | 6 passed (14)**, rc 1, at BOTH landing trees.
  - RED: A1, A3, B1 (`expected 202 to be 403` ×3); P1, P2, P3, D1 and P4 (`readIdOwners is not a function` ×3, `mayWriteAnchorRows is not a function` ×2).
  - GREEN: S1, A2, A4, A5, A6, B2.
  - This is identical to the author's buckets.
- I planted 3 mutations of my own:
  1. Drop tenant equality: 3 RED (A1, A3, B1).
  2. Session-scoped GUC: D1 RED, and G1b/G1c RED.
  3. Fail-closed catch: P2 and G2 RED.
- Every restore was proved byte-identical by sha256: `index.ts` `04eb96d3b6dc9ae8…`, guard `882cd948d7e6cfd5…`, with before equal to after. Working tree 0 dirty files.
- One-byte control: appending one `\n` changes the hash to `74ff976db9b349f2`, which is not equal to `04eb96d3…`.

## Q5: Suites on the LANDING tree. PASS

**Harness.**
- Scratch PostgreSQL 15.14 (Homebrew) on **port 55411**, TCP on 127.0.0.1 only, no unix socket. Superuser `secuura`. `secuura_app` was created by the repo's own `01-create-app-role.sh`.
- No Docker. I emulated docker-entrypoint: every file in `docker/init/*` ran in lex order, `.sql` with `ON_ERROR_STOP`. One change: `00-init-platform-db.sh` had its container path `/docker-entrypoint-initdb.d/platform` mapped to the repo's `docker/init-platform`, which is the mount compose declares.
- The server ran with `PGUSER/PGHOST/PGPORT/PGPASSWORD` in its environment so that `00-create-platform-db.sql`'s dblink loops back to itself. The real entrypoint exports PGUSER the same way.
- Migrations used the repo's `scripts/run-migrations.sh`, UNMODIFIED, spawned with cwd = Blockchain/Dev.
- Measured on the DB: `documents` `relrowsecurity,relforcerowsecurity = t,t`; `anchor_store` `f,f` with 0 tenant/organisation/owner columns (control: 22 columns); `secuura` super/bypassrls `t,t`; `secuura_app` `f,f`; `users.tenant_id` nullable `YES`.

**Migration runs.**
- On `31cfb44d`: `applied=53 failed=0 skipped=0`. Per-file lines: **52 `[main] Applying` + 1 `[platform] Applying` = 53**, including `[main] Applying 039_rls_fail_closed.sql...` and `050_`, `051_`. Control `Applying 999` = 0, read on a live instrument.
- On `80868551`: fresh DB, `applied=54`, **53 `[main]` + 1 `[platform]`**, including `[main] Applying 052_custody_events_connector_actor.sql...`.

**Suite results.**

| suite | landing parent `31cfb44d` | landing `e3af797c` | landing parent `80868551` | landing `8b67dde7` |
|---|---|---|---|---|
| anchoring integration | 3 files, **89/89** | 5 files, **103/103** | **89/89** | **103/103** |
| anchoring unit | 32 files, **379/380**, 1 fail | **379/380**, 1 fail | **379/380**, 1 fail | **379/380**, 1 fail |
| tsc as configured | — | rc 0, 0 lines | — | rc 0, 0 lines |
| tsc incl. `src/__tests__` | — | rc 0, 0 lines | — | rc 0, 0 lines |
| AA1 own cells (11) | — | 11/11 | — | 11/11 |

- **89 + 14 = 103.**
- **Unit red:** the single failure is `threadTokenMint.test.ts`, `Could not serialize the data: Error: Unsupported type` (lucid-evolution `applyParamsToScript`). It fails identically at the landing parent run alone (1 failed / 1), so it pre-exists and is not #1615's.
- **Integration control:** with the owner and app DSNs pointed at dead port 55419, rc 1, 4 files failed, 99 skipped. The suite really depends on the DB.
- **tsc pass 2:** the program includes both new test files (pass 1: 0 of 2; pass 2: 2 of 2; control `anchorOverwriteGuard.ts` = 1 in both). Positive control: a planted `const x: number = 'string'` in `__tests__` gives rc 2 with TS2322. I quarantined it afterwards.
- **Three-dot file list** against live develop is exactly 4 files, +711/−1: the 2 test files, `anchorOverwriteGuard.ts` (+238) and `index.ts` (+52/−1). The merge-base is `722e07f19cee`. landing^{tree} vs develop^{tree} gives the same 4 files.

## Q6: Overlap with #995 (KS-741). Not made worse

- #995 head `b8155636e8e6`, base `0f37b85c80b6`.
- `merge-tree` of #995 onto develop: rc 1, **one** conflict hunk, in `services/originate/src/index.ts` lines 13–22. This is the import block: develop's `createGatewayProvenanceMiddleware, describeState` + `resolveRequestTenantId`, against #995's multi-line import adding `createEmitterMarkerStrip`.
- `merge-tree` of #995 onto the landing tree: rc 1, the SAME single hunk. The file is byte-identical apart from the marker label.
- `services/anchoring/src/index.ts` (the shared file) **auto-merges in both**, with 0 conflict markers.
- #1615 adds no conflict to #995. This is a note, not a blocker.

## Blockers

None.

## Notes

1. **A caller with no usable tenant claim bypasses the gate.** This is pinned GREEN by cell A6 and described in the guard's own block as "as develop".
   - `users.tenant_id` is nullable (measured), and auth signs `tenantId: user.tenantId`. Any interactive user without a tenant can therefore still overwrite another tenant's anchor row, exactly as on develop.
   - Connector keys are covered: `svc_api_keys.tenant_id` is NOT NULL.
   - This is a narrowing and no worse than develop. But it is a residual the brief's residue list (TOCTOU, originate's second upsert to KS-1650, flat rows to KS-1384) does not name. Wednesday should confirm it is inside the 05:55:40Z ruled predicate, or ticket it.
2. **D1 does not pin the connection.**
   - It reads through `db.query`, i.e. any pool member. It discriminates in practice only because pg-pool hands back the most recently released client: under the session-scoped mutation it did go red.
   - AA1 G1 and G2 pin by backend pid and pass. Consider pinning D1 in a later round.
3. **The batch route runs the probe N+1 times.**
   - It reads once up front, then once more per item inside `dbPersistAnchor`. A 100-item batch is up to 101 short transactions plus the per-item KS-1385 reads.
   - This is correct, and the per-item gate is the guarantee. It is a performance note only.
4. **Develop moved twice relative to the author's READY:** first `722e07f19cee` to `31cfb44d` (KS-1195, likely #1613), then `80868551` (KS-1402) during this gate.
   - The live landing tree is `8b67dde74820`. Suites, red-first, AA1 cells and tsc were re-run on it with a fresh DB including migration 052, and all figures are unchanged.
   - A further develop move before merge voids this tree. Re-predict at the merge moment.
5. **#995:** a single pre-existing conflict hunk in `originate/src/index.ts` (import block, lines 13–22). It is identical with and without #1615. The anchoring file auto-merges either way.

## Gate disclosures (my own instrument faults, each caught)

- **First DB init touched another session's server.** On my first init, `00-create-platform-db.sql`'s dblink (`dbname=postgres`, no host) connected through the default unix socket `/tmp/.s.PGSQL.5432`. That socket belongs to another session's PostgreSQL. The connection failed with `role "secuura" does not exist`, so **no write landed there**. I quarantined that data dir and fixed the problem by giving my server a loopback libpq environment.
- **AA1 G3/G4b first used `doc-…` ids on the batch route** and read 400, because the batch schema accepts uuids only. I corrected them to uuids and kept a 400 cell as the schema control.
- **Project working tree.** The project working tree at `!CODING/Secuura/Blockchain/2_Project_Files` showed 17 dirty files. They pre-exist this gate: I ran only read verbs there (ls-remote, config --get, for-each-ref, status, and clone as the source).
- **Deploy key used for fetch.** My scratch clone fetched from GitHub with the project's deploy key (`-c core.sshCommand`, a read-only fetch). The global key was refused.
- **Cleanup.** The scratch DBs are stopped and quarantined under `scratchpad/aa1/quarantine/`, along with the AA1 test file (`aa1-gate-own-cells.integration.test.ts`) and the tsc control. Nothing was deleted.

## NOT RUN

- ESLint over the 4 files: not asked by the brief. The author's claim of 0 problems is unverified.
- GitHub API reads (`gh`):
  - I did not confirm that `31cfb44d` is #1613's squash.
  - I did not read #995's `mergeable_state` or #1615's API additions/deletions.
  - I did not repeat the 25-PR overlap census. Only #995, as the brief named, was checked.
- pgbouncer transaction pooling: not exercised. The pool was pg-pool direct to PostgreSQL. The "safe through pgbouncer" claim rests on SET LOCAL semantics, not on a measurement.
- A pre-039 (011 fail-open policy) database: not built. Probe behaviour under the 011 policy was not measured.
- The real `startup()` / `app.listen` boot path: not run. Cells spy on `listen` and call `initDb()`, as the author's do.
- The author's "`TEST_APP_DATABASE_URL` unset fails, not skips" control: not run. The dead-DSN control was run, on port 55419.
- The TOCTOU race and originate's `saveAnchorToDb` second upsert (KS-1650): not tested. They are out of scope by ruling.
- Suites for api-gateway and originate, where develop moved: not run. #1615 touches only anchoring.
- Docker, demo and kintsugi: not touched.
- Nothing was written to GitHub, Linear or `!CODING`.
sha256: d970081a169611bd31b641e295424959b6213293ef17fffbb482459e774afa90
