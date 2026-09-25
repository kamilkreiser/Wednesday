#1272 KS-849: the kyc mock timers re-read the verification before they write
head 34980b8e9ee22a36c658a03d9d763c48caeb9064

## What and why

Both kyc mock timers closed over the verification object **as it was at request time** and wrote the **whole of it** back when they fired.

The mechanism, confirmed at source before building:

- the store is **DB-only** — `index.ts` says so in its own section header ("DATABASE HELPER FUNCTIONS (DB-only — no in-memory Maps)") — and `dbGetVerification` rebuilds an object through `rowToVerification` on **every call**. So every request holds its own object; there is no shared identity to save a stale writer.
- `dbSaveVerification` is a full upsert whose `ON CONFLICT … DO UPDATE SET` names `liveness_completed`, `liveness_score`, `checks`, `status` and `documents` among others.

So a selfie arriving inside the 1500 ms document window had its liveness result silently overwritten. Both timers now **re-read inside the callback** and mutate what is in the database at that moment. The document is located **by id** in the re-read object, because the DB round-trip rebuilds the `documents` array and the captured reference is not in it.

## What this does NOT fix — pinned in code, not left to be rediscovered

At the 3000 ms auto-approve timer the re-read protects every field that timer does not own: `reviewedBy`, `reviewNotes`, `documents`, liveness, and checks that are no longer `pending`. It does **not** protect `status` or `currentLevel`, because **the timer sets those itself** — an admin **rejection** inside the window is still overwritten to `approved`.

Cell **S3 asserts `status === 'approved'` after a rejection**, with a comment saying this is not fixed. Tracked as **KS-1327**; closing it needs a partial UPDATE or row locking, which is a design.

This also corrects KS-849's own fix-shape text, which offers *"narrow the timer's write to the document fields it actually owns"* as an alternative. **That would not have been sufficient:** `documents` and `checks` are each a single whole-blob column and the document timer mutates **both**, so "the fields it owns" is still the entire `checks` array — where a selfie's facial/liveness passes live.

## Red proof, measured at develop first

| cell | at develop `4db87c3e4b98` | with the fix |
|---|---|---|
| **S1** selfie INSIDE the 1500 ms window | **RED** — `livenessCompleted: expected false to be true` | pass |
| **S2** selfie AFTER the window | green | pass |
| **S3** reviewer's notes across the 3 s timer | **RED** — `reviewed_by: expected null to be 'admin'` | pass |

S2 is green on both sides **on purpose** — it is the control saying the fix is not "the timer stopped working".

**S1 carries a vacuity control:** it asserts the document timer really fired (`validationStatus 'valid'`, `extractedData` present, document check `passed`), so the liveness assertions cannot pass because nothing happened.

**Assertions are on the persisted ROW, not the HTTP body.** `formatVerificationResponse` exposes neither `documents`, `livenessScore`, `reviewedBy` nor `reviewNotes` — and the defect is about *which columns* the stale upsert overwrites. The mock models the real `DO UPDATE SET` column list exactly.

## Mock surface, named rather than implied

`services/kyc/src/__tests__/ks386-…test.ts` records a predecessor's decision **not** to drive these routes, because "mocking that surface to reach one INSERT would make a brittle test whose failures would mostly be about the mock". That warning is respected by keeping the surface small and declaring it — the service issues only **five** SQL statements, so it stayed small.

Mocked: `../db` (an in-memory table modelling the upsert faithfully), `../subjectDeks`, and **four** functions out of `@secuura/shared` — three crypto pass-throughs plus `authenticate`, since `app.use('/api', jwtAuthenticate())` guards every route used. **So this file says nothing about authorisation.** Everything else stays real: the real error handler, the real `assertSupportedImage` (the cells post a genuine 1×1 PNG), real validation — and the app is driven over an HTTP listener **bound to `127.0.0.1`**.

## Test Evidence

**Touched**
- `services/kyc/src/index.ts` — the two mock timers only.
- `services/kyc/src/__tests__/ks849-mock-timer-stale-write.test.ts` — new.

**Ran**
- kyc **30/30 at develop `4db87c3e4b98` → 33/33 here**, `npx vitest run --no-file-parallelism`, `packages/shared` BUILT. Bare taken in a separate worktree detached at develop.
- The red proof above.
- **`packages/shared` 941/941** (48 files), identical to develop's 941/941. Its guards read this lane's sources by TEXT, and the **ks860 loopback guard was proven to see this new file**: tampering it to bind `0.0.0.0` turned that guard red naming this file by path and line, and green again on restore.
- `npx tsc --noEmit`: **rc 0**.
- Push preflight: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up). Nothing failed.** Not a pass, not quoted as one.
- Fleet STOP counts — **this worktree does NOT contain `d7cdecf1d2ee`; its base is `4db87c3e4b98`**, so these describe that tree: `pre_push_hook_base` **28/0** · `pre_push_hook_base_fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Zero `FIXTURE BUILD FAILED`. Each read from its suite's own region, bounded between consecutive `=== <path> ===` headers.

**NOT run**
- No real PostgreSQL; the DB layer is mocked. No authorisation coverage (see the mock surface).
- **The live-provider path is untouched and untested** — the timers are gated on `KYC_PROVIDER === 'mock'`, so this is the mock/demo path only. **The whole-row upsert itself is NOT mock-gated** and is the wider class: KS-1327.
- Preflight legs 3, 4, 8. Nothing deployed.

**Migrations + config**
- None. No migration, no config, no `package.json`, no lockfile, no `*.openapi.ts`.

Refs KS-849

🤖 Generated with [Claude Code](https://claude.com/claude-code)
