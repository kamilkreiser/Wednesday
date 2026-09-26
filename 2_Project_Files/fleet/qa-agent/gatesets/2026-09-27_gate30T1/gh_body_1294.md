#1294 KS-1334 part A: route the two unconditional adminConfig 500s through fail500
head c43d5bb18f046a78cb8f2e4a39fe22fe8f9e3324

## BLUF
`POST /api/admin/refresh-tenants` and `POST /api/admin/backfill-certification-metadata` answered a 500 carrying the thrown error's own text with **no `NODE_ENV` guard**, so it reached the client in every environment, production included. Both now go through the `fail500` helper. **Sites 2 of 4** — part B covers `seed-demo-users` and `migrate-tenant-data`.

Refs KS-1334

## What changed
Two files, +56/−4.

- `services/originate/src/routes/adminConfig.ts` (+2/−2) — the sites at `:113` and `:1859`.
- `services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (+54/−2).

**The test file's existing SOURCE assertions move with the fix, by design.** `helperCalls` and `distinctContexts` go **46 → 48**, and the C4 list of UNCONDITIONAL sites drops the two this change converts. That coupling is the point: those assertions exist so a conversion cannot happen silently, and they are what make this patch un-fakeable.

## Provenance
Produced by the local model under a brief and **re-verified by this seat**. The diff block is **byte-identical to the brief's golden AND to the run's canonical patch** — 80 lines, 4,906 B, sha256 `72500e4585ec6f69b011d039a46751496a6546f69455e971af9696c0bebcce28`, `cmp` rc 0 against both. Split into two file sections whose rejoin is byte-identical to the whole block. Strict `git apply --check -p1` per section at `3f70224a069b`: rc 0, no `--recount`, no fuzz. **Both tamper controls fire:** `res.status(500)`→`res.status(501)` on the product section rc 1, and `KNOWN`→`KNOWNX` on the test section rc 1.

## Test Evidence
Run by the author, locally, in this worktree at head `c43d5bb18f046a78cb8f2e4a39fe22fe8f9e3324` (base `3f70224a069b`). `packages/shared` built.

**Touched:** `services/originate/src/routes/adminConfig.ts`, `services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`

**Ran:**
- **RED (test edits applied, product reverted — revert confirmed by blob id):** `Tests: 4 failed, 15 passed, 19 total`. The four are the two new part-A rows **and** the two pre-existing SOURCE assertions that the fix moves:
  - `RED KS-1334 A1 POST /refresh-tenants: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it`
  - `RED KS-1334 A1 POST /backfill-certification-metadata: …`
  - the existing **C3 SOURCE** row (all forty-six sites routed through the helper, each with a distinct context)
  - the existing **C4 SOURCE** row (the four unconditional `err.message` sites are named, not silently left)
  Zero `TypeError`/`ReferenceError`/`Test suite failed to run` in the output, and 19 tests ran — so these are assertion reds, not a load failure.
- **GREEN (both files):** `Tests: 19 passed, 19 total`, after restoring the product **verified byte-identical by sha256**.
- **Per-environment coverage:** the new rows drive `production`, `development`, `demo`, `test` and unset, clearing the logger mock **inside** the loop and asserting the whole call list — the same shape KS1344 is fixing on the part-A webhooks cell, built in here from the start.
- **originate suite, serial (`jest --runInBand`), both measured in THIS worktree:** **bare 962 passed / 0 failed (82 suites)**, **patched 967 passed / 0 failed (82 suites)**. **0 new reds**; the +5 is this cell.
- **`tsc --noEmit` over a program PROVEN to contain BOTH touched files** (the service tsconfig excludes `src/__tests__`; a config extending it with `exclude: []` gives **714 files**, `adminConfig.ts` ×1 and the ks730c cell ×1 by `--listFilesOnly`) → **rc 0, 0 errors**.
- **`packages/shared` (vitest):** 48 files, **945 passed**, rc 0, 0 startup errors.
- **ESLint, the package's own `npm run lint`, at BOTH trees:** tip **22 problems (0 errors, 22 warnings)**, head **22 problems (0 errors, 22 warnings)** — same totals, same file set. The touched **test** file contributes **0 lines at either tree**; `adminConfig.ts`'s own pre-existing warnings are unchanged. Control: a planted `debugger` in the test file yields a `no-debugger` **error** and rc 1, so lint sees it.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `OK — 13 code guards passed` · zero lines starting `FIXTURE BUILD FAILED`. Parsed per suite block by exact basename.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — no local stack.)

**NOT run / NOT covered:**
- No local stack (preflight legs 3, 4, 8 did not run) and **no live sweep**. This is runtime code on an admin surface, so the ticket should not move to Done on this evidence alone.
- No deploy of any kind.
- No integration/e2e against a real database; the cell mocks at the route boundary.
- **Sites 3 and 4 are not touched** (`seed-demo-users`, `migrate-tenant-data`). KS-1334 stays open for part B, which edits the same ks730c count lines and therefore must follow this merge rather than run beside it.
- The gate asked for a check that inspecting a thrown object cannot leak a secret or PII field into the log — that applies to the KS1346 pair, not here: this change passes `err` to an existing helper whose logging shape is unchanged.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in.
- Foreign keys un-hyphenated in title, body and commit message (`KS730`, `KS1344`, `KS1346`). The cell's existing
  rows carry that ticket's key hyphenated in their titles; that is **file content** and is unchanged. This body
  names those two rows as **C3 SOURCE** and **C4 SOURCE** rather than quoting the titles, so no hyphenated
  foreign key appears here — misquoting a test name to satisfy a scanner would be the worse trade.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

