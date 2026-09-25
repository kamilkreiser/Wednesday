#1220 KS-1129 BIGNUM: the anchoring verify body reports blockNumber as a number
head 9c2021ba3e770abc9ad464b62fdc245a920389cb

## What changed — ONE of KS-1129's three sites, the anchoring one

`anchor_store.block_number` is a `BIGINT`, and node-postgres returns int8 as a **string** by default. There
is no int8 `setTypeParser` anywhere in `Blockchain/Dev`, so the raw row value left the
`GET /api/anchors/verify/:hash` body as a **string** — while the same column is converted with `Number()`
elsewhere in `index.ts`, the control that says the authors already knew the shape.

`toBlockNumber()` converts it, null-safe: absent stays `null` (never `0`, never `NaN`), the empty string
stays `null` rather than becoming `Number('') === 0`, and a value that does not convert stays `null` — which
`JSON.stringify` already does to `NaN`, so this **states** the wire behaviour rather than changing it, and
lets a unit cell assert the shape. The `||` in the caller is untouched: switching it to `??` would start
accepting a `0` height, a separate behaviour change, and this ticket is about the **type**.

## Correction to the ticket — the site has MOVED

The ticket locates this at `services/anchoring/src/index.ts:604`. **It is not there.** KS-1175 extracted the
body builder into `anchorReadback.ts` (pure, unit-testable without a boot — which is why these are pure
cells), so the raw pass is at **`anchorReadback.ts:103`**. Measured at develop `6ab9d5021e96`:
`git grep "row?.block_number" -- services/anchoring/src/index.ts` → **0**; the control,
`Number(row.block_number)` at `index.ts:1317` → **1**.

## Still open on KS-1129 — NOT in this PR, and not this seat's files

- **originate's KS-584 heal path** (`services/originate/src/routes/verification.ts`) persists this reply's
  `blockNumber` into the document blob unshaped.
- **the api-gateway's live chain-scan readers** have no shape rule at all (the ticket's O1).
- **the JSONB round-trip**, to be measured in both directions against a real Postgres.

## Test Evidence

**Touched:** `services/anchoring/src/anchorReadback.ts` (+1 exported helper, 1 changed call line);
`services/anchoring/src/__tests__/ks1129-blocknumber-is-a-number.test.ts` (NEW, 10 pure cells).

**Ran (locally, by the author, BARE and SERIAL — `npx vitest run --no-file-parallelism`):**
- `services/anchoring`: **bare 334 passed / 1 failed over 24 files → patched 344 passed / 1 failed over 25
  files** (+10 = the cells added).
- ⚠ **The one failure is IDENTICAL either side and PRE-EXISTING at develop `6ab9d5021`**:
  `src/__tests__/threadTokenMint.test.ts > threadTokenMint emulator round-trip > parameterises mint + spend
  with a deterministic per-seed policyId` — `Could not serialize the data: Error: Unsupported type`.
  **The same cell fails bare**, deterministic across 2 of 2 runs, and it is **not caused by this change**.
  It is **KS-562**, with today's re-measurement recorded there (comment `3caf329b`). This is an **exception,
  not a timeout**, so it is not the under-load false-red class.
- `npx tsc --noEmit` in `services/anchoring`: **rc 0** before and after.
- **Red proof** with `toBlockNumber` still exported (so the file LOADS and the pure cells still run) and only
  the **call site** read back out of the object store: **2 failed / 8 passed at develop**, exactly the two
  RED cells, **every control green at develop**. With the call site applied: **10/10 green**.

**NOT run:** preflight legs **3, 4 and 8** — `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing
failed.`, three identical `SKIP — local stack not up on http://localhost:6882` lines. **Legs 3/4/8 are OWED
at the gate**: this changes a **response field's type** on a live route. The four platform suites
(Schemathesis · Akto · Playwright · k6) were **not run** — the local stack is not up this round by fleet rule.

**Migrations + config:** none. No migration, no env var, no dependency change, `docs/openapi/` untouched.

Refs KS-1129

🤖 Generated with [Claude Code](https://claude.com/claude-code)

