#1262 KS-1310: pin /transfer-custody's route-level rollback; KS-1311 app-role items
head 3b319485d1e3a58f30e4190a7898d7562cb80c3b

## BLUF
`C7` already proves the custody rollback **inside** a `withTenant` callback — a JS-side throw the route itself could never produce. The **route** path was unpinned: the real `documentsRouter` over the real `db`, where the fault must come from the **database** because there is no seam to throw from. Pinned here, red at BASE and green at head, with KS-1311's two app-role items alongside.

## KS-1310 — why the fault is a trigger and not the NUL byte
`/transfer-custody` writes twice inside one transaction: INSERT `custody_events`, then flip the owner. To prove a **rollback** the fault must hit the **flip**, so the INSERT has already succeeded and must be undone.

The NUL byte that #1239's `/share` cell uses is **deliberately not reused**: it is consumed by the INSERT, so the insert dies, nothing is ever written, and "0 custody rows" is true for the wrong reason — it proves insert-failure, not rollback. That is a vacuous cell wearing the right assertion. A `BEFORE UPDATE` trigger scoped to this one document fires on the flip and not the insert. Shape ruled by the coordinator after the alternatives were put to her; the trigger is a **test vehicle**, exactly as the NUL byte is, and the file header now says so.

| | result |
|---|---|
| **BASE `33ccff807eb2`** (#1239's parent, **0** `withTenant` calls in `documents.ts`) | 🔴 `Expected: 0, Received: 1` on the custody count, owner unflipped — the row persists because there is no transaction |
| **head** | green |
| **CONTROL at both** | passes — so the red is the missing transaction, not a broken environment |

That test file **does not exist at BASE at all** (#1239 added it), so the BASE run is this new cell against BASE's product code — the correct comparison rather than a diff of two versions of the same file.

### The five conditions, each discharged in the cell
1. **Scoped** — function and trigger named `ks1310_flipfault_<run>`, and the raise is gated on this cell's document id, so no other row on the database can trip it.
2. **Always dropped** — in a `finally` that runs on failure, then **proven gone** from `pg_trigger` **and** `pg_proc` (0 rows, asserted, and re-checked from the catalogue after the run).
3. **Proven to fire** — the route's own logged error is asserted to carry the trigger's message, so a connection error or a 404 cannot pass as the fault. The HTTP body is deliberately generic (`'Failed to transfer custody'`), which is why the assertion is made on what the route actually received.
4. **Disposable database only** — the cell **refuses to run** unless the connection is `127.0.0.1` on this seat's own port range. A cell that writes DDL must be *unable* to reach a shared database, so this is a refusal and not a warning.
5. **Isolation both ways** — the trigger's presence measured while the cell holds it (2 catalogue rows) and after teardown (0), and every other integration cell in the file green in the same run.

### The CONTROL earned its place
`../repositories/documentRepo` is mocked for this whole file, and its canned document belongs to the `/share` describe carrying **no `owner`** — so `doc.owner.id` threw before the transaction was reached and the request 500'd for a reason unrelated to the rollback. **The CONTROL caught it.** Without it the red cell's "0 custody rows" would have been green for exactly the wrong reason.

The mock is now scoped by external id so the sibling describe keeps the document it expects, whatever order the describes run in. **The writes were never mocked** — the custody INSERT resolves `document_id` with a subquery against Postgres and the flip is `tx.$executeRaw UPDATE documents`, both inside `withTenant`, which is what makes a DB-side trigger able to fault the flip at all. That was verified before the cell was written, not assumed.

## KS-1311 — the two items
- **The header now names the vehicles as vehicles.** The NUL byte raises 22021 at the *second* write and is chosen because it fails DB-side and late, which is the only way to tell a rollback from a no-op. No caller sends it, nothing accepts it: **not a validation gap and not the defect under test.** The same sentence covers any cell-installed trigger — so the note lands *before* the trigger this PR adds rather than after it.
- **The MODE T guard now proves the tenant configs loaded**, not merely that a manager object exists. A manager with an empty config map routes every checkout to the default pool — MODE T's object wearing MODE F's behaviour, the same class as the PLATFORM-URL-TRAP one level down. `tenantConfigs` is private, so `getTenantStatus()` is used as an observable proxy after a refresh; it sits after the seed because the tenant only exists there. **Red-proved**: against an empty platform database the guard fires by name, naming the invisible tenant. Nothing in `packages/shared` touched — `getTenantStatus` is public surface.

## Also: KS-1293's second criterion, for this file
`ANCHORING_SERVICE_URL` moves from `127.0.0.1:1` to `:2`. Port 1 is on the Fetch bad-port list, refused **before** any socket, so the "closed port" this file relied on never happened. Measured on node 24: `:2` → `cause.code ECONNREFUSED`; `:1` → no `cause.code` at all.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts`. 1 file, +283 −1. Test-only; no runtime file, no migration, no config.

**Ran:**
- **Integration, at head** (`jest --config jest.integration.config.js`, MT=true, against a disposable Postgres): **7 passed / 7** — the 5 pre-existing cells plus both new ones.
- **Integration, at BASE `33ccff807eb2`** (own worktree, own `npm ci`, same Postgres): the new red cell fails with `Expected: 0, Received: 1`; the CONTROL passes. #1239's own `/share` red cell also fails there, as it should.
- **KS-1311 guard, red-proved:** with an empty platform database the new configs assertion fires by name (rc 1); the vehicle database was then dropped and proven gone from `pg_database`.
- `npx jest --runInBand` (originate unit): **869 / 869, 74 suites**, rc 0 — unaffected, as this file runs only under the integration config.
- `npm run lint`: rc 0. `npx tsc --noEmit`: rc 0.
- Push: rc 0. `pre_push_hook_base` 28/0, `pre_push_hook_base_fixture_guard` 6/0, shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.
- **Environment:** port proven free immediately before binding against a control that fires; image `postgres:15-alpine` read from `docker-compose.yml` (the script refuses `:latest`); `APP_DB_PASSWORD` a generated throwaway asserted ≠ the compose default; anonymous volume; migrations `applied=49, failed=0` with the tracker table read **independently** of the runner's own summary; 048 present.

**NOT run / NOT covered:**
- **MODE F (the Prisma branch of `withTenant`) NOT RUN** — a fresh worktree has no generated Prisma client (`Cannot find module '.prisma/client/default'`); residual, ticket **KS-1305**. This PR does not claim both modes.
- **Preflight INCOMPLETE — 12/15 legs ran, 3 SKIPPED** (legs 3, 4, 8 — local stack down). A skip is not a pass.
- These cells prove the **transaction boundary**. They do not prove the anchoring or provenance side effects that follow a successful transfer.
- The integration suite is not wired into any automatic run; it executes only when pointed at a database.

Refs KS-1310
Refs KS-1311

🤖 Generated with [Claude Code](https://claude.com/claude-code)

