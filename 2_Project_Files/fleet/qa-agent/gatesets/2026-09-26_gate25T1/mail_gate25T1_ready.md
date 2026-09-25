# CAPTURE for gate25T1 (QA/Secuura-batch1267) — 2026-09-25T20:43:40Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR's seat
claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.

## #1267 KS-1295 (Seat L8, T1) — head 71f6f4d73cbde5b32f1564c9171eb1b705f77880

#1267 ticket line: #1267 is KS-1295.

### PR BODY (gh_body_1267.md) TEXT_SHA256 329066c6cbcf64fb9fcc4e81970447a5d3ce00abd6abf956d5f98df79de7dec0

#1267 KS-1295: store() no longer keeps a credential in memory silently
head 71f6f4d73cbde5b32f1564c9171eb1b705f77880

## What and why

`credentialRepo.store()` wrote the in-memory map and then returned on `if (!isDbAvailable()) return;` **with no log at all**. The caller is told the credential was stored, nothing reached PostgreSQL, and on restart it is gone — leaving no line to grep, no counter and no artefact, so the event cannot be investigated after the fact.

`#1231` made the **sibling** table-absent path loud (two WARNs per store). This is the path it did not touch, raised as **P-1** by that PR's gate.

**Shape (1) of the ticket only: LOG it**, naming the credential id and the reason. Shape (2) — refusing the write — is a behaviour change with its own decision and is deliberately **not** built here. (1) does not foreclose (2).

`loadFromDb()`'s identical early return at `:207` is a **startup read, not a store**, and is untouched. The file's bare silent returns go **2 → 1**.

## Why a new test file

`credentialRepo.test.ts` mocks `isDbAvailable` as a module-scope `vi.fn(() => false)`, so it **cannot produce the database-AVAILABLE arm** — and without that arm, "the WARN does not fire" would be untested. That file also carries 3 pre-existing `TS2339` (a KS-1090 residue) that are not this ticket's to disturb.

## Cells

| cell | asserts |
|---|---|
| **W1** database unavailable | exactly one WARN carrying `credentialId` and a non-empty reason; **no SQL issued at all** (so the WARN came from the fallback branch and not another); and the credential is still retrievable from memory |
| **W2** database available | **no such WARN** — *and* the INSERT is proven to have been issued with the expected parameters |
| **W3** two stores | two WARNs, in credential order — once per store, not once per process |

**W2's second half is the point.** Every cell asserting an absence needs a control proving the thing could have been present. Without it, W2 would also pass if `store()` had done nothing at all, or if the WARN text had simply been misspelled out of existence.

## Red proof

With the product reverted to develop:

| cell | reverted | with the fix |
|---|---|---|
| W1 | **RED** | pass |
| W3 | **RED** | pass |
| W2 | **green** | pass |

W2 staying green on both sides is correct, not a gap: it asserts an absence that holds before and after. It is the control, not a result.

## Test Evidence

**Touched**
- `services/vc-issuer/src/repositories/credentialRepo.ts` — the `store()` early return only.
- `services/vc-issuer/src/__tests__/ks1295-store-db-unavailable-warn.test.ts` — new.

**Ran**
- vc-issuer **129/129 at develop `4db87c3e4b98` → 132/132 here**, 14 files, `npx vitest run --no-file-parallelism`, **`packages/shared` BUILT**. The develop figure came from a separate worktree detached at develop.
- The red proof above.
- `npx tsc --noEmit`: **rc 0**. The new test file was additionally type-checked under a config with `exclude: []` (vc-issuer's program excludes `src/__tests__`): **0 errors in it**.
- Push preflight: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up). Nothing failed.** Not a pass, and not quoted as one.
- Fleet STOP counts, read from each suite's own header: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60/0 of 60**. Zero `FIXTURE BUILD FAILED`.

- **`packages/shared` 941/941** (48 files, `npx vitest run`) in this worktree, identical to develop `4db87c3e4b98`'s 941/941. That package's guards read this lane's service sources by TEXT (the ks860 listen-call guard, the ks879 control-byte guard and the entrypoint corpus), so they are a cross-lane reader of this change and are run on every head raised.

**NOT run**
- No run against a real PostgreSQL; `isDbAvailable`/`query` are mocked.
- **The ticket's severity rests on an UNMEASURED reach, and this PR does not measure it.** Whether `isDbAvailable()` is ever false in the deployed Azure environment, and whether the least-privilege role can perform the existence check at all, were not read — both need a deployed read. The kintsugi log observation owed against KS-1281 has not been made. A WARN is an improvement regardless; it is not evidence the path fires anywhere.
- Preflight legs 3, 4, 8. Nothing deployed.

**Migrations + config**
- None. No migration, no config, no `package.json`, no lockfile, no `*.openapi.ts`.

Refs KS-1295

🤖 Generated with [Claude Code](https://claude.com/claude-code)


### HEAD COMMIT MESSAGE TEXT_SHA256 2b8d73d2c65ef4319b1ec9e514da300a3139bdba32d32bcefa7b02a7920bc1ed

KS-1295: store() no longer keeps a credential in memory SILENTLY

credentialRepo.store() wrote the in-memory map and returned on
`if (!isDbAvailable()) return;` with no log at all. The caller is told the
credential was stored, nothing reached PostgreSQL, and on restart it is gone --
leaving no line to grep and no artefact, so the event cannot be investigated
after the fact. #1231 made the sibling table-absent path loud; this is the path
it did not touch, raised as P-1 by that PR's gate.

Shape (1) of the ticket only: LOG it, naming the credential id and the reason.
Refusing the write is a behaviour change with its own decision and is NOT built
here. loadFromDb()'s identical early return is a startup read, not a store, and
is deliberately untouched: the file's bare silent returns go 2 -> 1.

Three cells in a new file, because credentialRepo.test.ts mocks isDbAvailable as
a module-scope vi.fn(() => false) and so cannot produce the database-AVAILABLE
arm -- without which "the WARN does not fire" would be untested.

  W1 database unavailable  -> exactly one WARN carrying credentialId and a
                              reason; no SQL issued at all; the credential is
                              still retrievable from memory
  W2 database available    -> no such WARN, AND the INSERT is proven to have
                              been issued with the expected parameters. That
                              control is the point: without it W2 would also
                              pass if store() had done nothing, or if the WARN
                              text had been misspelled out of existence.
  W3 two stores            -> two WARNs, in credential order (once per store,
                              not once per process)

Red proof: with the product reverted to develop, W1 and W3 go RED and W2 stays
GREEN -- correct, because W2 asserts an absence that holds on both sides.

vc-issuer 129/129 at develop 4db87c3e4b98 -> 132/132 here, vitest run
--no-file-parallelism with packages/shared BUILT. tsc --noEmit rc 0; the new
test file type-checked separately under exclude: [] (0 errors in it) because
vc-issuer's tsc program excludes src/__tests__.

Refs KS-1295

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks1295-71f6f4d73cbde5b32f1564c9171eb1b705f77880-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks1295-71f6f4d73cbde5b32f1564c9171eb1b705f77880-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T18:54:53Z PUSH START",
 "end": "2026-09-25T19:02:53Z push rc=0"
}
```

## #1269 KS-1182 (Seat L8, T1) — head df21c6fd159f2a707d698e418946911f019ca9a0

#1269 ticket line: #1269 is KS-1182.

### PR BODY (gh_body_1269.md) TEXT_SHA256 0cf932f7d24501e5d95e055fdfa3997ee76fca2cd84d7dfb62b9b0abe59620c8

#1269 KS-1182: bound the demo-service error status, honour headersSent/headers/expose
head df21c6fd159f2a707d698e418946911f019ca9a0

## What and why

demo-service's `errorHandler` applied `err.status` **unchecked** and ignored `headersSent`, `err.headers` and `expose`. The KS-844 tier-1 gate measured each row in its own node process (report §6c):

| row | head behaviour before this PR |
|---|---|
| H1 status 200 | **HTTP 200** on an error envelope — a failure reads as a success |
| H2 status 302 | 302 JSON, no `Location` |
| H3 status 600 | 600 — not a status |
| H4 status `'400'` | a **string** reached `res.status()`; express deprecates it |
| **H5 status NaN** | **NO RESPONSE; uncaught `RangeError [ERR_HTTP_INVALID_STATUS_CODE]`; process EXIT 1** |
| H9 405 + `err.headers {Allow: GET}` | `Allow` dropped — a 405 is meaningless without it |
| H12 400 `expose:false` | the message echoed anyway |

The gate's fix shape, applied in full: delegate on `headersSent`; `Number.isInteger` bounded to 400–599 else 500; apply `err.headers` as finalhandler does; echo `err.message` only when `expose !== false`. A 5xx still never carries the thrown message.

## H5 is pinned at the CAUSE, not the symptom — stated plainly

The gate's H5 is a **process crash**. It cannot be reproduced inside a test runner without taking the runner down, and running it in an isolated child process is exactly what the gate already did. So the cell pins that **the handler never hands a non-integer-error status to `res.status()`**; if that holds, the RangeError has no way to occur. The crash itself remains the gate's measurement, not this file's — the test file says so in its header.

## R1 — the response double is checked against real express

Twelve cells drive a response double. A double can drift from the real thing, so **R1 mounts the handler in a real express app over a listener bound to `127.0.0.1`** and drives the H1 row through it: it answers 500, and **R1 reds at develop too**. The double is not quietly disagreeing with express.

## Red proof

**At develop: 11 of 14 cells RED, 3 green.** The three green are exactly the controls that must hold on both sides:

- a legitimate 4xx (413) passes through unchanged with its message — so the bound is not "always 500";
- a 4xx **without** `expose:false` still carries its message — so H12 is not "never echo";
- with headers **not** sent it answers and does not delegate — so H10 is not "always delegate".

## Test Evidence

**Touched**
- `services/demo-service/src/middleware/errorHandler.ts`
- `services/demo-service/src/__tests__/ks1182-error-handler-status-and-headers.test.ts` — new.

**Ran**
- demo-service **72/72 at develop `4db87c3e4b98` → 86/86 here**, `npx vitest run --no-file-parallelism`, **`packages/shared` BUILT**. Bare taken in a separate worktree detached at develop.
- The red proof above (11 red / 3 green at develop; 14/14 here).
- **`packages/shared` 941/941** (48 files) in this worktree, identical to develop's 941/941. That package's guards read this lane's sources by TEXT (ks860 listen calls, ks879 control bytes, the entrypoint corpus), so they are a cross-lane reader of this change.
- `npx tsc --noEmit`: **rc 0**.
- Push preflight: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up). Nothing failed.** Not a pass, and not quoted as one.
- Fleet STOP counts, read from each suite's own `=== <path> ===` header: `pre_push_hook_base` **28/0** · `pre_push_hook_base_fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Zero `FIXTURE BUILD FAILED`.

**NOT run**
- **The H5 process crash itself.** See above — the cause is pinned, the symptom is the gate's measurement.
- **H11 (status 99) and H6/H7/H8/H10/H13 are not added as cells.** The scoped set is H1–H5, H9, H12; H11 is covered incidentally by the 400–599 bound but has no cell of its own.
- No run against a live demo-service deployment. **Unreachable today:** body-parser, raw-body and http-errors set only 400, 403, 413, 415 or 500, and no route or middleware in demo-service calls `next(err)` (the gate's §6a READ). This is a guard against a future producer, not a fix for a live defect — the NaN row is the one that would matter if one appeared.
- Preflight legs 3, 4, 8. Nothing deployed.

**Migrations + config**
- None. No migration, no config, no `package.json`, no lockfile, no `*.openapi.ts`.

Refs KS-1182

🤖 Generated with [Claude Code](https://claude.com/claude-code)


### HEAD COMMIT MESSAGE TEXT_SHA256 023f75f09f6fa623b04b1ae38207e29be65b5e5c9a2c85e6745f8531b4757b71

KS-1182: bound the demo-service error status and honour headersSent/headers/expose

demo-service's errorHandler applied err.status UNCHECKED and ignored headersSent,
err.headers and expose. The KS-844 tier-1 gate measured each row in its own node
process:

  H1  status 200   -> HTTP 200 on an error envelope: a failure reads as success
  H2  status 302   -> 302 with no Location
  H3  status 600   -> 600, which is not a status
  H4  status '400' -> a STRING reached res.status(); express deprecates it
  H5  status NaN   -> NO RESPONSE, uncaught RangeError, PROCESS EXIT 1
  H9  405 + err.headers {Allow: GET} -> Allow dropped
  H12 400 expose:false -> the message echoed anyway

The gate's fix shape, applied in full: delegate on headersSent; bound the status
with Number.isInteger and 400-599 or else 500; apply err.headers as finalhandler
does; echo err.message only when expose !== false. A 5xx still never carries the
thrown message.

H5 IS PINNED AT THE CAUSE, NOT THE SYMPTOM, and the file says so. The crash cannot
be reproduced inside a test runner without taking the runner down, and running it
in an isolated child process is what the gate already did. The cell pins that the
handler never hands a non-integer-error status to res.status(); if that holds the
RangeError has no way to occur.

14 cells: H1-H5, H9, H12, five controls, and R1. R1 mounts the handler in a REAL
express app over a listener bound to 127.0.0.1 and drives the same row, so the
response double cannot quietly disagree with express.

Red proof: at develop 11 of 14 red, 3 green. The 3 green are exactly the controls
that must hold on both sides -- a legitimate 4xx passes through unchanged, an
exposed 4xx keeps its message, and headers-not-sent still answers. R1 reds at
develop too, which is what says the double is faithful.

UNREACHABLE TODAY, stated rather than glossed: body-parser, raw-body and
http-errors set only 400, 403, 413, 415 or 500, and no route or middleware in
demo-service calls next(err). This is a guard against a future producer. The NaN
row is the one with a runtime consequence if one appears.

demo-service 72/72 at develop 4db87c3e4b98 -> 86/86 here, vitest run
--no-file-parallelism with packages/shared BUILT. tsc --noEmit rc 0.

Refs KS-1182

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks1182-df21c6fd159f2a707d698e418946911f019ca9a0-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks1182-df21c6fd159f2a707d698e418946911f019ca9a0-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T19:10:48Z PUSH START",
 "end": "2026-09-25T19:17:54Z push rc=0"
}
```

## #1272 KS-849 (Seat L8, T1) — head 34980b8e9ee22a36c658a03d9d763c48caeb9064

#1272 ticket line: #1272 is KS-849.

### PR BODY (gh_body_1272.md) TEXT_SHA256 f82f882661249d196c48c570541f8bb170f7f2240b1cad4e972a013e72cc4c09

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


### HEAD COMMIT MESSAGE TEXT_SHA256 db7656f78e8df3af3e992d6a8ef3be278f1b915c1db7ea1fe9628051c482b24b

KS-849: the kyc mock timers re-read the verification before they write

Both mock timers closed over the verification object as it was at REQUEST time and
wrote the WHOLE of it back when they fired. The store is DB-only (no in-memory
Map), so every request rebuilds its own object and there is no shared identity to
save a stale writer; dbSaveVerification is a full upsert whose DO UPDATE SET names
liveness_completed, liveness_score, checks, status and documents. So a selfie
arriving inside the 1500 ms document window had its liveness result silently
overwritten.

Both timers now re-read inside the callback and mutate what is in the database at
that moment. The document is located BY ID in the re-read object, because the DB
round-trip rebuilds the documents array and the captured reference is not in it.

WHAT THIS DOES NOT FIX, pinned in the code rather than left to be rediscovered.
At the 3000 ms auto-approve timer the re-read protects every field that timer does
not own -- reviewedBy, reviewNotes, documents, liveness, and checks that are no
longer pending. It does NOT protect status or currentLevel, because the timer sets
those itself: an admin REJECTION inside the window is still overwritten to
'approved'. Cell S3 asserts exactly that, with a comment saying it is not fixed.
Closing it needs a partial UPDATE or row locking, which is a design.

Red proof, measured at develop first:
  S1 selfie INSIDE the 1500 ms window   RED at develop
     (livenessCompleted expected false to be true) -> passes here
  S2 selfie AFTER the window            green both sides (the control: the fix is
     not "the timer stopped working")
  S3 reviewer's notes across the 3 s timer  RED at develop
     (reviewed_by expected null to be 'admin') -> passes here

S1 also carries a VACUITY CONTROL: it asserts the document timer really fired
(validationStatus 'valid', extractedData present, document check passed), so the
liveness assertions cannot pass because nothing happened.

Assertions are on the PERSISTED ROW, not the HTTP body: formatVerificationResponse
exposes neither documents, livenessScore, reviewedBy nor reviewNotes, and the
defect is about WHICH COLUMNS the stale upsert overwrites. The mock models the
real ON CONFLICT DO UPDATE SET column list exactly.

Mock surface, named in the file: ../db, ../subjectDeks, and four functions out of
@secuura/shared -- three crypto pass-throughs plus authenticate, since
app.use('/api', jwtAuthenticate()) guards every route used. So this file says
NOTHING about authorisation. Everything else stays real, including the error
handler, assertSupportedImage (the cells post a genuine 1x1 PNG) and validation,
and the app is driven over an HTTP listener bound to 127.0.0.1.

kyc 30/30 at develop 4db87c3e4b98 -> 33/33 here. packages/shared 941/941,
unchanged from develop. tsc --noEmit rc 0.

Refs KS-849

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks849-34980b8e9ee22a36c658a03d9d763c48caeb9064-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks849-34980b8e9ee22a36c658a03d9d763c48caeb9064-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T19:24:45Z PUSH START",
 "end": "2026-09-25T19:32:11Z push rc=0"
}
```

## #1274 KS-934 (Seat L8, T1) — head 1a37bde12d55563f77e192519ca7db62461dbf6f

#1274 ticket line: #1274 is KS-934.

### PR BODY (gh_body_1274.md) TEXT_SHA256 16553ef2496313d017a2e4fb6905015936bcf968b95588b9c3c34b5372feacad

#1274 KS-934: bound POST /api/teams/notify with a LIMIT and an aggregate deadline
head 1a37bde12d55563f77e192519ca7db62461dbf6f

## What and why

`POST /api/teams/notify` looped over every active webhook **serially, inside the request handler**, with **no `LIMIT`** on the query and **no aggregate deadline**. The call site passed no `timeoutMs`, so each row rode `safeOutboundRequest`'s **10 s default** (`packages/shared/src/security/ssrf-guard.ts:486`).

**Measured against the unfixed route: 25 rows took 10048 ms** with the HTTP request held open throughout.

## Both bounds, because neither is sufficient alone

- A **`LIMIT`** bounds the row set and the memory one request costs — but still allows `LIMIT × 10 s` of wall-clock.
- An **aggregate deadline** bounds the wall-clock — but still loads an unbounded row set.
- **Paging is deliberately not added.** It puts *more* work on the request path, which is the opposite of the fix. The un-attempted remainder is **reported** (`skipped`, `deadlineExceeded`) rather than silently dropped, so a caller is never told a partial run was a complete one.
- Each call is given **`min(per-row timeout, time remaining under the aggregate)`**, so one hanging peer cannot consume time the aggregate has already spent.

The three numbers carry their reason in the source rather than being bare constants, and all three are env-overridable because the right values depend on how many webhooks a tenant registers:

| constant | default | why that value |
|---|---|---|
| `TEAMS_NOTIFY_MAX_ROWS` | 50 | bounds the row set and the memory one request costs |
| `TEAMS_NOTIFY_DEADLINE_MS` | 10 000 | **equals the guard's existing single-call default**, so this route's worst case becomes what ONE row already cost — no request gets slower than it could already be, and the N× multiplier is gone |
| `TEAMS_NOTIFY_PER_ROW_TIMEOUT_MS` | 2 000 | one hanging peer cannot starve the rows behind it; at this value at least five rows are still attempted inside the aggregate deadline even if every one hangs |

## Red proof

| cell | at develop `4db87c3e4b98` | with the fix |
|---|---|---|
| **N1** the query carries a `LIMIT` | **RED** — `'SELECT * FROM svc_teams_webhooks WHER…' did not match /LIMIT \s+\$\d+/i` | pass |
| **N2** a slow peer set cannot hold the request past the aggregate deadline, and the remainder is reported | **RED** — **`expected 10048 to be less than 3000`** | pass |
| **N3** no per-call timeout exceeds the budget remaining | **RED** — `expected 'undefined' to be 'number'` | pass |
| **CONTROL** a small fast set still delivers every row | green | green |

The control is green on **both** sides on purpose: the bound is not "skip everything". N1 and N3 also assert their own inputs (more rows available than the limit; calls actually made), so neither can pass vacuously.

## Why `safeOutboundRequest` is stubbed, stated plainly

It is the **SSRF guard** and refuses loopback by design, so a webhook pointed at `127.0.0.1` returns `blocked` in microseconds and no timing cell would measure anything. The stub models the guard's documented contract (`timeoutMs` is a total deadline on the whole operation) and **records the `timeoutMs` it is handed** — which is what makes N3 an assertion about **this route** rather than about the guard. That the guard honours its own deadline is `packages/shared`'s to prove, and it is not re-proved here.

## Test Evidence

**Touched**
- `services/m365-integration/src/index.ts` — the notify route and three new constants.
- `services/m365-integration/src/__tests__/ks934-teams-notify-request-path-bound.test.ts` — new.

**Ran**
- m365-integration **38/38 at develop `4db87c3e4b98` → 42/42 here**, `npx vitest run --no-file-parallelism`, `packages/shared` BUILT. Bare taken in a separate worktree detached at develop.
- The red proof above.
- **`packages/shared` 941/941** (48 files), identical to develop's 941/941. The **ks860 loopback guard was proven to see this new file**: tampering its listener to `0.0.0.0` turned that guard red naming this file by path and line (`…ks934-…test.ts:108`), and green again on restore.
- `npx tsc --noEmit`: **rc 0**.
- Push preflight: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up). Nothing failed.**
- Fleet STOP counts — **this worktree does NOT contain `d7cdecf1d2ee`; base `4db87c3e4b98`**, so these describe that tree: `pre_push_hook_base` **28/0** · `pre_push_hook_base_fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Zero `FIXTURE BUILD FAILED`. Each read from its suite's region, bounded between consecutive `=== <path> ===` headers.

**NOT run**
- No real Teams endpoint and no real `safeOutboundRequest` call — see the stub note above.
- **The `LIMIT` is not paged.** Beyond `MAX_ROWS`, rows are simply not attempted on that request and are reported as such. A caller needing all of them must call again; making that automatic is the "off the request path" design, which is **not** this change.
- **Observed and deliberately NOT changed:** `GET /api/teams/webhook-config` (`index.ts:1163`) also selects active webhooks with no `LIMIT`. It is a different exposure — it makes **no outbound calls**, so there is no `N × 10 s` wall-clock risk, only response size — and it sits behind `requireM365`, which the notify route does not. Out of KS-934's scope; named here rather than silently widened.
- Preflight legs 3, 4, 8. Nothing deployed.

**Migrations + config**
- None. No migration, no config file, no `package.json`, no lockfile, no `*.openapi.ts`. The three new constants read from `process.env` with defaults, so no environment must change for the bound to apply.

Refs KS-934

🤖 Generated with [Claude Code](https://claude.com/claude-code)


### HEAD COMMIT MESSAGE TEXT_SHA256 de63d1d7031efff2a688adc38c6fdf391730eebd1053e276c30549582a8098a8

KS-934: bound POST /api/teams/notify with a LIMIT and an aggregate deadline

The webhook SELECT had no LIMIT, the loop was serial inside the request handler,
and the call site passed no timeoutMs -- so each row rode safeOutboundRequest's
10 s default and the worst case was rows x 10 s with the HTTP request held open
throughout. Measured against the unfixed route: 25 rows took 10048 ms.

Both bounds, because neither is sufficient alone. A LIMIT bounds the row set and
the memory one request costs but still allows LIMIT x 10 s of wall-clock; an
aggregate deadline bounds the wall-clock but still loads an unbounded row set.
Paging is deliberately NOT added: it puts MORE work on the request path, which is
the opposite of the fix. The un-attempted remainder is REPORTED rather than
silently dropped, so a caller is never told a partial run was a complete one.

Each call is also given min(per-row timeout, time REMAINING under the aggregate),
so one hanging peer cannot consume time the aggregate has already spent.

The three numbers carry their reason in the source rather than being bare
constants, and all three are env-overridable because the right values depend on
how many webhooks a tenant registers:
  MAX_ROWS 50            bounds the row set
  DEADLINE_MS 10 000     the aggregate budget, chosen to EQUAL the guard's
                         existing single-call default -- so this route's worst
                         case becomes what ONE row already cost, and the N x
                         multiplier is gone
  PER_ROW_TIMEOUT_MS 2000  so one hanging peer cannot starve the rows behind it;
                         at this value at least five rows are still attempted
                         inside the aggregate deadline even if every one hangs

Four cells pinning the ROUTE's four obligations, which are the route's own:
  N1 the query carries a LIMIT          RED at develop
     ("SELECT * FROM svc_teams_webhooks WHER..." did not match /LIMIT \$\d+/)
  N2 a slow peer set cannot hold the request past the aggregate deadline, and
     the remainder is reported          RED at develop (expected 10048 to be
     less than 3000)
  N3 no per-call timeout exceeds the budget remaining  RED at develop
     (expected 'undefined' to be 'number')
  CONTROL a small fast set still delivers every row    green BOTH sides, so the
     bound is not "skip everything"

safeOutboundRequest is STUBBED in the cells and the file says why: it is the SSRF
guard and REFUSES loopback by design, so a webhook pointed at 127.0.0.1 returns
`blocked` in microseconds and no timing cell would measure anything. The stub
models the guard's documented contract and RECORDS the timeoutMs it is handed,
which is what makes N3 an assertion about this route rather than about the guard.
That the guard honours its own deadline is packages/shared's to prove.

m365-integration 38/38 at develop 4db87c3e4b98 -> 42/42 here. packages/shared
941/941, unchanged from develop. tsc --noEmit rc 0.

Refs KS-934

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks934-1a37bde12d55563f77e192519ca7db62461dbf6f-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/raise/s-l8-ks934-1a37bde12d55563f77e192519ca7db62461dbf6f-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T19:40:16Z PUSH START",
 "end": "2026-09-25T19:47:09Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatL8-2026-09-26.md TEXT_SHA256 cb7e9abe4a735acdf95b8e33017e30235137e99c714c7b11d9768f8272830584

# HANDOVER — Seat L8, pane `Secuura/Blockchain-D`, round 25 (small-services lane)

**Written to be read COLD.** Lane: `services/vc-issuer`, `services/kyc`, `services/demo-service`,
`services/m365-integration` — four services no other round-25 seat touches.

**Nothing merged by me. Nothing deployed. No ticket state moved.**

---

## 1. Where things stand

| # | Ticket | PR | Head | State |
|---|---|---|---|---|
| 1 | KS-1281 | **#1264** | `2e95121dfc475a09c81d61d61f9a81148b6bb0b9` | READY FOR QA |
| 2 | KS-1120 | **#1266** | `952f4329de97cd7f94ab6363e670248c456d0a54` | READY FOR QA |
| 3 | KS-1295 | **#1267** | `71f6f4d73cbde5b32f1564c9171eb1b705f77880` | READY FOR QA |
| 4 | KS-1182 | **#1269** | `df21c6fd159f2a707d698e418946911f019ca9a0` | READY FOR QA |
| 5 | KS-849  | (see §6) | `34980b8e9ee22a36c658a03d9d763c48caeb9064` | pushed / PR per §6 |
| 6 | KS-934  | (see §6) | `1a37bde12d55563f77e192519ca7db62461dbf6f` | committed, push per §6 |

**Filed:** **KS-1327** (KS-849 residual — the whole-row read-modify-write class) and **KS-1328**
(kyc `db.retry.test.ts` exceeding vitest's 5 s default under fleet load). Both Backlog, both with
the board searched first and controls that fire.

**Every ticket left In Progress / Backlog as found.** I moved no ticket state.

---

## 2. The base, and why the figures still stand

All figures were measured at develop **`4db87c3e4b98`**. develop has since moved to
**`d7cdecf1d2ee`** (Seat M1's merges). Measured via the compare API rather than a fetch, so no ref
write was made in the shared checkout: **5 commits, 6 files, ZERO in my lane**, against a control
prefix that fires. `packages/shared` also untouched.

So the figures remain true of what they measured, and the PR bodies name `4db87c3e4b98` honestly.
**They are not restated as current.** If a gate wants them on the new tip, they must be re-run.

⚠ **Two of those six files are preflight shell suites**
(`scripts/__tests__/run_migrations_failure_exit_code.test.sh`,
`scripts/__tests__/no_tracked_credentials_root.test.sh`). My first four pushes all read
`run_shell_suites` **49/0** and shell suites **60/0 of 60** — measured BEFORE that merge. A seat that
now sees different numbers should check this cause before calling a STOP; the brief already says the
coordinator re-declares the count after such a merge.

---

## 3. What each change is, in one line

1. **KS-1281** — comment-only. `credentialRepo.ts:8`/`:24` no longer claim the table is
   "auto-created"; #1231 removed the runtime DDL. AST-equivalence proven with a control.
2. **KS-1120** — two test cells (X1, X2) pinning the memory PREFIX class and the DB-miss to
   memory-get fallback. Test-only; no product file touched.
3. **KS-1295** — a WARN when `store()` keeps a credential in memory because the database is
   unavailable. `loadFromDb`'s identical early return is untouched; bare silent returns 2 -> 1.
4. **KS-1182** — the demo-service error handler: `headersSent` delegation, a 400-599 integer bound,
   `err.headers`, `expose`.
5. **KS-849** — both kyc mock timers re-read the verification before mutating it.
6. **KS-934** — `POST /api/teams/notify` gets a LIMIT, an aggregate deadline, and a per-call timeout
   no larger than the budget remaining; the un-attempted remainder is reported.

---

## 4. The four things I would most want the next seat to have

**A green suite is silent about files its corpus does not contain.** `packages/shared` read 941/941
on all six of my heads — which says nothing about my NEW test files until you prove the guard sees
them. I tampered my own file to bind `0.0.0.0`; the ks860 guard went red and named it by path and
line, then green again on restore. Only then was the 941/941 a statement about my work.

**A containment proof can pass by writing nothing at all.** My first merge25.py proof put both arms
in ONE scratch repo, uncontained first — so the object already existed, `merge-tree` wrote nothing
ANYWHERE, and shared delta 0 AND contained delta 0 both "passed". One FRESH repo per arm gives the
real answer: uncontained **+1**, contained **0 shared / +1 contained**, same predicted tree. This is
B 28th's recorded trap arriving in a different costume, which is the point: **knowing the lesson did
not stop me reproducing it.**

**A default that makes a factual claim is a hardcoded claim.** `merge24.py`'s `merge_note` DEFAULT
still asserted *"the author had already wrapped, so this is not the author merging their own PR"* —
false whenever a build seat merges its own PR, and it lands on develop permanently. B 28th NAMED
this class and closed only the seat-name half. Fixed in `merge25.py`: the default now states only
what the run itself verifies, and authorship must come from the addendum.

**A flat grep can miss a count that is right there.** `pre_push_hook_base` and `fixture_guard` read
"NOT FOUND" on my first pass because the summary line is INDENTED beneath a `=== <path> ===` header.
Re-anchoring on the headers found all four STOP counts. Parse by the header, never by a bare prefix.

---

## 5. Instruments and where they live

`5_Project_History/2026-09-26_seatL8/`
- `raise/` — `lock25.sh` (**proven 21/21**), `push25.sh` (**19/19**), `merge25.py` (re-keyed;
  containment proven two-sided, see `measurements/merge25-containment-proof.md`), `ast_equiv.cjs`,
  the two proof harnesses, `tamper_ks1120.py`, and every push log **named by head sha** (KS-1323).
- `measurements/` — every suite run, both arms of every red proof, the tamper JSON.

`push25.sh` re-keys that mattered: its two lock calls pointed at `lock24.sh` (would have dangled AT
THE LOCK TAKE); `PUSH24_*` -> `PUSH25_*`; logs named `$TAG-$HEAD_SHA-*` per KS-1323.

**`merge25.py` has never been used to merge.** It is proven for containment only.

---

## 6. Live at handover — read this before acting

**Five PRs are READY FOR QA. None is merged. Nothing is deployed.**

| PR | ticket | head | note |
|---|---|---|---|
| **#1264** | KS-1281 | `2e95121dfc475a09c81d61d61f9a81148b6bb0b9` | comment-only |
| **#1266** | KS-1120 | `952f4329de97cd7f94ab6363e670248c456d0a54` | test-only |
| **#1267** | KS-1295 | `71f6f4d73cbde5b32f1564c9171eb1b705f77880` | |
| **#1269** | KS-1182 | `df21c6fd159f2a707d698e418946911f019ca9a0` | |
| **#1272** | KS-849 | `34980b8e9ee22a36c658a03d9d763c48caeb9064` | |

**KS-934** is committed at `1a37bde12d55563f77e192519ca7db62461dbf6f` in `worktrees/s-l8-ks934`,
pushing at handover time. If its push did not complete, the branch is
`feature/ks-934-teams-notify-request-path-bound-l8r25-6` and it needs: push -> PR -> ticket comment.
Its PR body content is in the KS-934 commit message, which is written to carry it.

All five PRs verified `linkKind='contributes'` in Linear, so **none closes its ticket on merge**, and
every ticket reads In Progress or Backlog as found.

### The one outstanding job that is NOT mine but was accepted from the coordinator

Wednesday asked (19:30Z, DKIM verified) for the **fleet's d7cdecf1 preflight measurement**, because
her earlier "the first seat to push over it is the measurement" was wrong — a push measures its own
WORKTREE's base. The job, in order:

1. `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` is **NOT present in the local object store** (verified,
   with a control). So it needs **one `git fetch origin develop` in `2_Project_Files`, taken under
   `.push-lock-25`** — the only ref write the brief permits there.
2. A throwaway worktree **detached** at that sha.
3. `npm ci` **and** `npm run build -w packages/shared` in it — a fresh worktree has no deps and the
   preflight's leg 1 refuses without them.
4. `bash scripts/preflight/preflight.sh`, **without pushing**.
5. Mail the four numbers **with `merge-base --is-ancestor d7cdecf1d2ee HEAD` stated**.
6. `git worktree remove` it — it holds no work.

**Expected (an expectation, NOT a measurement):** `pre_push_hook_base` 28/0 ·
`pre_push_hook_base_fixture_guard` 6/0 · `run_shell_suites` 49/0 · shell suites 60 of 60.
Corroborated two ways (gate24T2c's report; and all six changed files are `modified`, none `added`,
and none is a counted suite's own file). **If the measurement differs, that is news — do not explain
it away with the merge.**
For comparison, from my PRE-merge tree: `no_tracked_credentials_root.test.sh` **15/0** and
`run_migrations_failure_exit_code.test.sh` **5/0**; the merge added +31 and +77 lines to those files,
so both should read higher on d7cdecf1 while the four named counts hold.

### State of the shared checkout, measured at handover
`2_Project_Files` HEAD **`3bad652d17cf`**, **17 untracked / 0 modified** — byte-identical to boot.
I never pulled, fetched, committed or checked out there; the only writes were `worktree add` in my
own `s-l8-*` namespace, each measured at **0 lines of change to the shared `.git/config`**.

### Parse push logs by BOUNDED REGION, not by prefix
A push log carries **two** summary forms — prefixed (`run_shell_suites: 49 passed, 0 failed`, 28
occurrences) and indented under a `=== <path> ===` header (26 occurrences). A parser anchored on
either alone under-reports, and an under-reported STOP count reads as a missing gate rather than a
parser bug. Bound each suite's region **between consecutive `=== … ===` headers** and take the
summary inside it; that is form-agnostic and immune to the neighbouring-summary trap.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/measurements/fleet-measurement-RESULT-d7cdecf1.md TEXT_SHA256 a4c421c21ef366bfca8c8c580c187edd16433d0f2bf2d5e306d162fe6de7f576

# FLEET MEASUREMENT — preflight on the COMBINED tree d7cdecf1 (Seat L8, 2026-09-26)

Run at Wednesday's request (19:30Z ANSWER), because her 19:27Z declaration's line
"the first seat to push over it is the measurement" was wrong — a push measures its own
WORKTREE's base. This is the first tree that actually contains the merge.

**Base, stated per the new rule:** `merge-base --is-ancestor d7cdecf1d2ee HEAD` = **YES**.
HEAD = `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`, detached, throwaway worktree, **no push**.

## The four named counts — ALL MATCH the declaration

| count | measured | declared | |
|---|---|---|---|
| `pre_push_hook_base` | **28 / 0** | 28/0 | MATCH |
| `pre_push_hook_base_fixture_guard` | **6 / 0** | 6/0 | MATCH |
| `run_shell_suites` | **49 / 0** | 49/0 | MATCH |
| shell suites | **60 passed, 0 failed, 0 skipped (of 60)** | 60 of 60 | MATCH |

Zero lines starting `FIXTURE BUILD FAILED`. Preflight rc **0**;
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack
not up). That verdict is not a pass and is not quoted as one.

**The expectation is now a measurement.**

## The tree is proven to be the combined one, not a stale checkout

Three independent signs, each measured rather than assumed:

1. `merge-base --is-ancestor d7cdecf1d2ee HEAD` = YES.
2. The two suites the merge modified are the POST-merge copies:
   `run_migrations_failure_exit_code.test.sh` **180 lines** (105 pre-merge) and
   `no_tracked_credentials_root.test.sh` **352 lines** (324 pre-merge) — matching the compare's
   +77 and +31 exactly.
3. Their CELL counts moved with the content — **both of them**:
   `run_migrations_failure_exit_code` **5/0 -> 7/0** (+2 cells, from +77 lines) and
   `no_tracked_credentials_root` **15/0 -> 16/0** (+1 cell, from +31 lines).
   So the new content really RAN; the suites were not merely present in the tree.

That third point is what makes the four unchanged counts meaningful rather than vacuous: the
preflight demonstrably executed changed content and still produced the same quadruple.

## Method notes
- `d7cdecf1` was ABSENT locally, so one `git fetch origin develop` was taken **under
  `.push-lock-25`** — the lock honoured this seat's own 90 s cool-off first, and was held
  **3 seconds** (19:48:39Z -> 19:48:42Z).
- The fetch disturbed nothing another session owns: shared checkout HEAD and the **local `develop`
  branch both still `3bad652d17cf`** (only `origin/develop`, a remote-tracking ref, advanced);
  working tree still 17 untracked / 0 modified; shared `.git/config` sha unchanged.
- Counts read by **bounded region** between consecutive `=== <path> ===` headers, because the log
  carries two summary forms and either parser alone under-reports.


