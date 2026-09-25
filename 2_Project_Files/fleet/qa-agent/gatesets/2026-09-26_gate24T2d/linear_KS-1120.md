KS-1120 GET /api/presentations/:id exact-or-404: the memory-path PREFIX class and the DB-miss → memory get are unpinned, and the test's `pgModel` under-reports the base disclosure (QA-966 F-1 + F-2 + F-3)
state In Progress

## BLUF

Three test-side gaps left by PR #966 (KS-1020 item 1, merged 2026-09-13), from its tier-1 gate; the code is correct at head on every measured row, and none held the merge. (F-1) Every memory-path partial-id cell is a SUFFIX or a MIDDLE of the stored id — no cell sends a PREFIX, so a `startsWith` scan re-inserted after `:129` runs 108/108 green while `GET /api/presentations/https%3A%2F%2Fabc0.issuer1.example` answers 200 again. (F-2) No cell constructs a row present in memory and absent from the DB, so a `return undefined` after the DB miss (skipping `memPresentationStore.get`) runs 108/108 green while the memory-only row flips 200 → 404. (F-3) The test's `pgModel` strips only a leading/trailing `%` and then uses `includes`; on real PostgreSQL `%`, `_`, `a%`, `%a`, `0_` … match EVERY row through `LIKE '%…%'` (the widest form of the base disclosure — one request, no id knowledge), so the header's "a model of PostgreSQL `=`/`LIKE` semantics" is not true as written and the PR's 16-red base set is a lower bound.

## Recommendation

One test pass in `ks1020-presentation-lookup-exact-or-404.test.ts`:

1. **F-1 — one memory-describe cell:** `GET /${encodeURIComponent('https://abc0.issuer1.example')}` (a PREFIX of the stored id, asserted with `expect(storedId.startsWith(id)).toBe(true)`) → 404. Optionally one DB-describe prefix cell (`STORED_ID.slice(0, 20)`), though S1 already pins the DB path by SQL text.
2. **F-2 — one DB-describe cell:** seed one row through the real `POST /` with `dbMock.query` rejecting the INSERT (the `storePresentation` `:104-106` path, so the row exists in memory and not in the DB), then `GET` that id → 200 with exactly one query whose SQL is `WHERE id = $1`.
3. **F-3 — reword the header** (`:29-31`, `:190-193`) to "a model of `=` and of a `%`-wrapped substring LIKE; `_`, interior `%` and escapes are not modelled", or translate the pattern faithfully (`%`→`.*`, `_`→`.`, `\` honoured, anchored, case-sensitive) as the gate's recorder does.

## Detail

* **Where:** `Blockchain/Dev/services/vc-issuer/src/routes/presentations.ts` (`getPresentation`, why-comment `:110-117` at `1f0d08841`; the memory get after the DB block; `storePresentation` `:104-106`); `src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts` (header `:29-31`, `pgModel` `:194-209`, the memory and DB describes; `freshModules()` leaves the Map empty at `:213`).
* **F-1 (MEASURED AT RUNTIME):** tamper T4 — `for (const [key, value] of memPresentationStore.entries()) { if (key.startsWith(id)) return value; }` after `:129` — tsc rc 0, FULL vc-issuer suite 108/108, ks1020 22/22, 0 red; with T4 applied the gate's HTTP instrument measured `…/https%3A%2F%2Fabc0.issuer1.example` → 200 with the seeded presentation, `…/https%3A%2F%2Fabc0` → 200, the first 20 chars of S → 200, the bare uuid (a suffix) 404. Evidence `evidence/rows/tamper-T4-memory.json`.
* **F-2 (MEASURED AT RUNTIME):** tamper T5 — `return undefined; // QA-T5` inside the `isDbAvailable()` block after the `catch` — 108/108, 0 red; with T5 the memory-only row flipped 200 → 404 on the DB path with exactly one `WHERE id = $1` query; the exact DB-stored id stayed 200. Evidence `evidence/rows/tamper-T5-db.json`.
* **F-3 (MEASURED + READ ONLY):** `pgModel` diverges from a faithful model on 7 of 14 probe ids (`evidence/rows/pgmodel-fidelity.txt`); at base on the DB path the gate's recorder measured `GET /api/presentations/%25` → 200 seed#1 via `WHERE id LIKE $1 LIMIT 1` with `['%%%']`, `%5F` → 200 via `['%_%']`, `a%25`, `%25a`, `0%5F` likewise; at head the same rows cost one `WHERE id = $1` with the literal bound and answer 404 — S1 pins that no LIKE is issued, so the model's LIKE branch is dead at head and the fix's greens do not rest on it.
* **Source:** `Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks1020-966-1f0d08841-tier1-r1/report.md`, §1 F-1, F-2, F-3; §2 the row table; §7 red-proof.
* **Related:** KS-1020 (PR #966); KS-1116 (item 2, the ownership model); KS-625 (`/presentations/verify`, the same file).
* **Dedupe, before filing (s200, 2026-09-13):** literal census over 1,106 KS issues (685 archived) and 899 comments — `pgModel` → 0; `VC_BASE_URL` → KS-1020 and KS-665 (comments only); `routes/presentations.ts` class → KS-1020, KS-1116, KS-625 (a different route). None describes these three pins. Controls: `LIKE` → KS-1020; a nonsense token → 0.
