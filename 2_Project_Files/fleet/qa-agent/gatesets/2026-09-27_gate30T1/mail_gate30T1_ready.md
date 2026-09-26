# CAPTURE for gate30T1 (QA/Secuura-batch1292) — 2026-09-26T13:40:11Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR's seat
claims are captured from its PR BODY, its COMMIT MESSAGES and the Seat B 32nd raise records below, each verbatim with its TEXT_SHA256.

## #1292 KS-1341 (Seat B 32nd (local-model patch, Spark, byte-identical to brief-C rev C golden; re-verified by the seat), T1) — head ef821d2e27bf06ae1420bdb830ec7fffd7b8c732

#1292 ticket line: #1292 is KS-1341.

### PR BODY (gh_body_1292.md) TEXT_SHA256 53ab0d87952101588c6965014e24c3586ca351b397b4b44993aecf8e50eb2bd3

#1292 KS-1341 part C: route the last two webhooks 500s through the fail500 helper
head ef821d2e27bf06ae1420bdb830ec7fffd7b8c732

## BLUF
`POST /:id/test` and `GET /:id/deliveries` were the last two of the seven unconditional 500s in `routes/webhooks.ts` that answered with the thrown error's own text and no `NODE_ENV` guard. Both now go through the `fail500` helper parts A (#1288) and B (#1290) introduced — both merged. This is **part C of 3**, and it finishes the seven.

Refs KS-1341

## What changed
Two files, +171/−2.

- `services/originate/src/routes/webhooks.ts` (+2/−2) — the two `res.status(500).json({ … message: err.message })` sites at `:391` and `:416` become `fail500(res, '<context>', err)`.
- `services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (+169, new) — 5 red-first cells and 3 controls.

Measured on the patched file, by me:

| | tip | after |
|---|---|---|
| `message: err.message` | 2 | **0** |
| `fail500(` | 6 | **8** — 1 declaration (`:562`) + 7 calls (`:200 :267 :325 :337 :352 :391 :416`), each a distinct context |

`err.message` still appears twice, and **neither is in a response**: `:544` (`logger.warn('Webhook dispatch failed', …)`) and `:563` (the helper's own server-side log).

## Provenance
The patch was produced by the local model under a Wednesday brief and **re-verified by this seat, not taken on trust**. The diff block is **byte-identical** to the brief's golden and to the run's canonical patch: 188 lines, 9,564 B, sha256 `78fd00567f5f31e0a94a8508f80a82867fb437199d309cca3710e668020e24e2`, `cmp` rc 0 against both (control: `cmp` against an unrelated golden → rc 1). It applies **strictly** at `3f70224a069b` — `git apply --check -p1` per file, no `--recount`, no fuzz — and a tampered copy of each section is refused (section 1 rc 1 "patch failed … :414"; section 2 with a corrupted hunk count rc 128 "corrupt patch").

## Test Evidence
Run by the author, locally, in this worktree at head `ef821d2e27bf06ae1420bdb830ec7fffd7b8c732` (base `3f70224a069b`, confirmed an ancestor). Node/jest via the repo's own scripts; `packages/shared` built.

**Touched:** `services/originate/src/routes/webhooks.ts`, `services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts`

**Ran:**
- **RED (the cell alone, product hunks reverted — revert confirmed by blob id `a2ad9e05…` = the tip):** `Tests: 5 failed, 3 passed, 8 total`. The 5 failures are exactly the declared cells, **each on its own `expect(...).toEqual` assertion**, not a crash — zero `TypeError`/`ReferenceError`/`is not a function` in the output, and 8 tests ran (0 passed + 0 failed would be a load failure, not a red):
  - `RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset`
  - `RED KS-1341 C1 GET /:id/deliveries: …` (same assertion, other route)
  - `RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named`
  - `RED KS-1341 C2 GET /:id/deliveries: …`
  - `RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts`
  - The 3 controls stayed green, including `control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch`.
- **GREEN (both files):** `Tests: 8 passed, 8 total`, after restoring the product patch **verified byte-identical by sha256**.
- **REACHED, per route, with the mechanism named:** `GET /:id/deliveries`'s query carries its own `.catch(() => [])` at `:412`, so a *rejected* query is swallowed into a 200 and never reaches the catch — control C0 pins exactly that. The cell therefore arms that route with a **synchronous throw** and `POST /:id/test` with a rejection. Both catches are shown reached by their reds.
- **The KS1344 lesson is closed in this cell, proven not declared.** C1 clears the logger per environment and asserts the whole call list. Tamper: make `fail500` log only under `NODE_ENV === 'production'` → `Tests: 2 failed, 6 passed, 8 total`, and the red set is **exactly the two C1 rows** by title; C2, C3 and all three controls stay green. Restored by content, verified by sha256.
- **originate suite, serial (`jest --runInBand`):** **bare 962 passed / 0 failed (82 suites)** at the tip, **patched 970 passed / 0 failed (83 suites)** at this head. **0 new reds** — the failing-suite sets are identical and both empty; the +8 is this cell.
- **`tsc --noEmit` over a program PROVEN to contain the new cell:** the service tsconfig excludes `src/__tests__`, so a bare `tsc` covers **0** test files (measured: `--listFilesOnly` finds the cell 0 times). With a config extending it and `exclude: []` the program is **715 files and contains the cell (1 occurrence, proven)** → **rc 0, 0 errors**.
- **`packages/shared` (vitest) at this head:** **48 files, 945 passed**, rc 0 — it is run because its guard suites read originate sources by text.
- **ESLint, the package's own `npm run lint` (`eslint src`), at BOTH trees:** tip **22 problems (0 errors, 22 warnings)**, head **22 problems (0 errors, 22 warnings)** — identical per-file breakdown across the same 14 files, delta 0. **Neither of my two files contributes a single problem.** Control: a planted `debugger` in the new cell produces `no-debugger` **error** at its line and rc 1, so lint does see the new file.
- **Push gate — quoting only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `OK — 13 code guards passed` · zero lines starting `FIXTURE BUILD FAILED`. Counts were parsed per suite block by exact basename: `pre_push_hook_base` is a **prefix** of two other suites (`…_fixture_guard`, `…_leg_comment` 4/0) and a prefix parser silently misreads them.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 did **not** run (local stack not up).

**NOT run / NOT covered:**
- No local stack, so preflight legs 3, 4 and 8 did not run, and there is **no live sweep**. This is runtime code, so under the test-discipline rule the ticket does **not** move to Done on this evidence alone — a live sweep is owed.
- No deploy of any kind: not demo, not UAT, not kintsugi.
- No integration/e2e run against a real database; the cell mocks at the route boundary.
- `tsc` invoked on the test file **directly** with ad-hoc flags reports 7 pre-existing `TS2339` errors in `webhooks.ts` at lines `221, 298, 474, 475, 480, 483, 488`. **Control: the identical 7 appear at the untouched tip** (revert confirmed by blob id), **0 are in the new cell**, and none is at a line this patch touches (`391`, `416`). They are an artefact of compiling without the project config, not a finding — the authoritative check is the program-proven `tsc` above.
- **Three sentences in the helper's docblock (`:549`–`:561`) are not corrected here, deliberately.** Part C does not touch them, and amending them would forfeit byte-identity to the golden:
  1. *"the only place in this router that turns a caught error into a 500"* — false after parts A and B, and **becomes true only with this change** (the C3 SOURCE cell pins it).
  2. *"Declared at the END of the file"* — it sits immediately before `export default webhooksRouter;` (`:567`).
  3. *"Seven catch blocks above put the thrown error's own text in the 500 body"* — after this change that describes history, not the file.
  A follow-up docs ticket is owed for the rewording.

## Review notes
- Base is `develop` at `3f70224a069b`; this branch is a fast-forward on it. No merge-in.
- Foreign keys are un-hyphenated in this title, body and commit message (`KS730`, `KS1344`). The cell's own `KS730` reference is file content and is unchanged.
- Parts A (#1288) and B (#1290) are merged; this completes the seven sites.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 dd21974682f0ea2ae62d19474d8380e05f9fddcbe12b206bf9597bcf8fe58008

--- commit ef821d2e27bf06ae1420bdb830ec7fffd7b8c732
KS-1341 part C: route the last two webhooks 500s through the fail500 helper

POST /:id/test and GET /:id/deliveries were the last two of the seven
unconditional 500s in routes/webhooks.ts that put the thrown error's own text
in the response body, with no NODE_ENV guard. Both now call the fail500 helper
that parts A and B introduced: the thrown text is logged server-side with the
route named, and the client gets the constant INTERNAL_ERROR body.

After this change webhooks.ts carries `message: err.message` 0 times (2 before)
and `fail500(` 8 times (6 before): one declaration and seven calls, each with a
distinct context. The two remaining `err.message` occurrences are both
server-side logs, not responses.

The patch was produced by the local model under a Wednesday brief and
re-verified by this seat: the diff is byte-identical to the brief's golden and
to the run's canonical patch, and it applies strictly at develop with no
recount and no fuzz.

Test evidence is in the pull request body. The new cell also closes the KS1344
gap in its own C1 rows: it clears the logger per environment and asserts the
whole call list, so a fail500 that logged only under production reds them.
The cell's own KS730 reference is file content and is unchanged.



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1341c-ef821d2e27bf-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1341c-ef821d2e27bf-push.out",
 "lines": 1305,
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
 "start": "2026-09-26T12:08:36Z PUSH START",
 "end": "2026-09-26T12:15:35Z push rc=0"
}
```

## #1294 KS-1334 (Seat B 32nd (local-model patch, Spark on an EXCERPTED input, byte-identical to brief-A golden; re-verified by the seat), T1) — head c43d5bb18f046a78cb8f2e4a39fe22fe8f9e3324

#1294 ticket line: #1294 is KS-1334.

### PR BODY (gh_body_1294.md) TEXT_SHA256 a16371f404d5f1fb71dfec327220277ddd29c8cd9fc10d12588ee9aacbf1cbc4

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



### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 1e3edd6db75168f0d7166b09655e9865e62df9c2baf6c84383eab35f19f68f46

--- commit c43d5bb18f046a78cb8f2e4a39fe22fe8f9e3324
KS-1334 part A: route the two unconditional adminConfig 500s through fail500

POST /api/admin/refresh-tenants and POST /api/admin/backfill-certification-metadata
answered a 500 carrying the thrown error's own text, with no NODE_ENV guard, so it
reached the client in every environment including production. Both now call the
fail500 helper: the thrown text is logged server-side with the route named, and the
client gets the constant INTERNAL_ERROR body.

Two files, +56/-4. The ks730c cell's SOURCE assertions move with the fix by design:
helperCalls and distinctContexts 46 -> 48, and the C4 list of UNCONDITIONAL sites
drops the two this change converts. A new part A block drives both routes across
production, development, demo, test and unset, clearing the logger mock per
environment and asserting the whole call list.

Sites 2 of 4. Part B covers seed-demo-users and migrate-tenant-data, and edits the
same ks730c lines, so it comes after this merges.

The patch was produced by the local model under a brief and re-verified by this seat:
byte-identical to the brief's golden and to the run's canonical patch, applying
strictly at develop with no recount and no fuzz.



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1334a-c43d5bb18f04-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1334a-c43d5bb18f04-push.out",
 "lines": 1305,
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
 "start": "2026-09-26T12:45:08Z PUSH START",
 "end": "2026-09-26T12:52:04Z push rc=0"
}
```

## #1296 KS-1346 (Seat B 32nd (WIDEN: raised from brief KS-1346-A golden; the model block differs by one trailing context line; re-verified by the seat), T1) — head eff979b3d493b973aaa4f91defe2c58f960c3f11

#1296 ticket line: #1296 is KS-1346.

### PR BODY (gh_body_1296.md) TEXT_SHA256 0a63e6b90843b08dd111c0cc972f88a1571545c7a397f7d3fcea7278b8b053d9

#1296 KS-1346 part A: log a non-Error throw from systemErrors fail500 with inspect
head eff979b3d493b973aaa4f91defe2c58f960c3f11

## BLUF
`fail500` in `routes/systemErrors.ts` rendered a caught value with `String(err)` when it was not an `Error`, so a thrown **plain object** reached the log as `[object Object]` and its content was lost. It now uses `inspect(err)`. The 500 **body** was already constant, so this changes only what is **logged**.

Refs KS-1346

## ⚠ READ THIS BEFORE MERGING — what this change widens
The gate asked whether inspecting a thrown object can put a secret or PII field into the log. **It can, and nothing on this path redacts it.** I measured both halves:

1. **The rendering.** For a thrown object `{ code, password, apiKey, email }`: the tip logs `"[object Object]"`; this head logs `"{ code: 'P0001', password: 'hunter2', apiKey: 'sk_live_DEADBEEF', email: 'subject@example.test' }"`. A nested `{ outer: { inner: { ssn: … } } }` likewise logs the SSN. The `Error`, `string` and `null` paths are byte-for-byte unchanged.
2. **The sink.** `systemErrors.ts` imports `logger` from `../utils/logger` (line 18) — the service's own winston logger. I read that module in full (77 lines): **it performs no redaction of any kind, in any environment.** The redacting logger (`packages/shared/src/logger/index.ts`, with `SENSITIVE_KEYS` and `redactValue`) is **not on this path**.

And a nuance that matters if anyone proposes routing this through the shared logger as a mitigation: **that redactor keys off the field NAME**, and after `inspect()` the secret is inside a *string value* under the key `error`. Modelling its rules, a thrown object carrying an SSN and no email **survives redaction**; the flat example above is caught only incidentally, by the unrelated "value contains `@` and `.`" email rule, which then redacts the whole string. So the shared logger would not be a reliable fix either. (That second part is a *reimplementation* of its rules for a hypothetical, not a run of the real module — the load-bearing fact is #2 above, which I measured by reading the actual logger this route uses.)

**This is inherent to the ticket, not a defect in the patch** — the whole point is to stop losing the thrown content, and `[object Object]` has no diagnostic value. But it is a real widening of what reaches log storage on an admin surface, and whether that is acceptable depends on who can read those logs. **That call is not mine, and I have filed no ticket for it.** Part B (`gdpr.ts`) makes the same change on a subject-data surface, where it matters more.

## What changed
Two files, +99/−1.
- `services/originate/src/routes/systemErrors.ts` (+2/−1) — the `inspect` import and the one rendering expression.
- `services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts` (+97, new).

## Provenance
**Raised from the brief's golden**, which the hold record names as the canonical patch: 111 lines, 6,053 B, sha256 `7002806683950f9c325318954ba6901f540ed780e586b1b414aee72a875fc8f6`.
**The model's own block is NOT byte-identical to it, and I measured the difference rather than repeating the claim:** the model's diff is 112 lines / 6,056 B and differs by exactly **one extra trailing context line** (` }` at line 12) and nothing else. That matches the hold record. My tooling refused the raise until I pointed it at the golden — it will not silently accept a near-match.
Strict `git apply --check -p1` per section at `3f70224a069b`: rc 0, no `--recount`, no fuzz. **Both tamper controls fire:** `String(err)`→`String(errZZ)` rc 1; and for the new-file section a corrupted hunk count `+1,97`→`+1,999` rc 128.

## Test Evidence
Author-run, locally, in this worktree at head `eff979b3d493b973aaa4f91defe2c58f960c3f11` (base `3f70224a069b`). `packages/shared` built.

- **RED (cell alone, product reverted — confirmed by blob id):** `Tests: 4 failed, 7 passed, 11 total`. The four are the A1 rows, one per admin route — `GET /stats`, `GET /`, `PATCH /:errorId/resolve`, `POST /resolve-by-service` — each driven by making that route's own service call reject on a real loopback listener. Zero crash signatures; 11 ran, so not a load failure.
- **Control A5 makes A1 non-vacuous:** it asserts that `String()` of the thrown object really is the lossy text. Controls A3 and A4 pin that the `Error` and `string` paths log exactly what they logged before.
- **GREEN:** `Tests: 11 passed, 11 total` after a sha256-verified restore.
- **originate suite, serial:** **bare 962 passed / 0 failed (82 suites)**, **patched 973 passed / 0 failed (83 suites)**. 0 new reds; +11 is this cell.
- **`tsc --noEmit` over a program PROVEN to contain both touched files** (`exclude: []`, **715 files**, each present once by `--listFilesOnly`) → **rc 0, 0 errors**.
- **`packages/shared`:** 48 files, **945 passed**.
- **ESLint (`npm run lint`) at BOTH trees:** **22 problems (0 errors, 22 warnings)** each; **0 lines name either touched file** at either tree. Control: a planted `debugger` gives a `no-debugger` error and rc 1.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 of 60** · `OK — 13 code guards passed` · zero `FIXTURE BUILD FAILED`.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`

**NOT run / NOT covered:**
- **No assessment of who can read originate's logs**, which is what decides whether the widening above is acceptable. Flagged, not resolved.
- No redaction is added by this change, and none exists on this path.
- No local stack (legs 3, 4, 8), no live sweep, no deploy, no integration/e2e against a real database.
- Part B (`gdpr.ts`) is a separate PR; the same widening applies there on a subject-data surface.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in. Foreign keys un-hyphenated throughout.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 7021ac848f63f058d07c7771aa4273cc2ca6f2a6dfe69b1b1667efa5e436efcc

--- commit eff979b3d493b973aaa4f91defe2c58f960c3f11
KS-1346 part A: log a non-Error throw from systemErrors fail500 with inspect

fail500 rendered a caught value with String(err) when it was not an Error, so a
thrown plain object reached the log as [object Object] and its content was lost.
The 500 body was already constant, so this changes only what is LOGGED.

It now uses inspect(err) for values that are neither an Error nor a string.
Error and string throws render exactly as before.

Two files, +98/-1: the product line plus its import, and a new cell that drives
all four admin routes on a real loopback listener by making each route's own
service call reject, with controls pinning the Error path, the string path, and
that String() of the thrown object really is lossy.

Raised from the brief's golden, which is the canonical patch for this change.
The model's own diff differs from it by one extra trailing context line and is
otherwise identical; the golden applies strictly at develop.



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1346a-eff979b3d493-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1346a-eff979b3d493-push.out",
 "lines": 1305,
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
 "start": "2026-09-26T13:04:36Z PUSH START",
 "end": "2026-09-26T13:11:26Z push rc=0"
}
```

## #1297 KS-1346 (Seat B 32nd (WIDEN: raised from brief KS-1346-B golden, byte-identical to the run canonical patch; re-verified by the seat), T1) — head f6565fa66532fa0a60e968ae22f664c71e22da08

#1297 ticket line: #1297 is KS-1346.

### PR BODY (gh_body_1297.md) TEXT_SHA256 ee05ff45bcd9a13356cf24813b9468f738164dc79980b5af312f6341ad042b93

#1297 KS-1346 part B: log a non-Error throw from gdpr fail500 with inspect
head f6565fa66532fa0a60e968ae22f664c71e22da08

## BLUF
`fail500` in `routes/gdpr.ts` rendered a caught value with `String(err)` when it was not an `Error`, so a thrown **plain object** reached the log as `[object Object]` and its content was lost. It now uses `inspect(err)`. The 500 **body** was already constant, so this changes only what is **logged**. Companion to part A (`systemErrors.ts`).

Refs KS-1346

## ⚠ READ THIS BEFORE MERGING — and it matters more here than on part A
This is the same rendering change as part A, on a **subject-data surface**. I measured both halves again for this file:

1. **The rendering.** A thrown object logs its contents where it previously logged `[object Object]` — including fields such as `password`, `apiKey`, `email`, and a nested `ssn`. The `Error`, `string` and `null` paths are byte-for-byte unchanged.
2. **The sink.** `gdpr.ts:22` imports `logger` from `../utils/logger` — the service's own winston logger, which performs **no redaction of any kind, in any environment**. The redacting logger (`packages/shared/src/logger/index.ts`) is not on this path; and because it keys off the **field name**, it would not reliably help even if it were, since after `inspect()` the content sits inside a string value under the key `error`.

On these routes the object a repository or service throws can plausibly carry **the data subject's own identifiers**. The change is still correct for the ticket — `[object Object]` has no diagnostic value and losing the content is the defect being fixed — but it widens what reaches log storage on the one surface where that is most sensitive. **Whether that is acceptable depends on who can read originate's logs; that is not this seat's call, and no ticket has been filed for it.** It is raised here and mailed so the gate can decide with the measurement in hand.

## What changed
Two files, +97/−1: `services/originate/src/routes/gdpr.ts` (+2/−1) and the new cell `ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts` (+95).

## Provenance
Raised from the brief's golden: 5,869 B, sha256 `6530f63a6e8814fdcef4be02211ff5dc350b1f7991e309da37cb96f8820da08e`, **`cmp` rc 0 against BOTH the golden and the run's canonical patch** (unlike part A, where the model's block carried one extra context line). Strict `git apply --check -p1` per section at `3f70224a069b`: rc 0, no `--recount`, no fuzz. **Both tamper controls fire:** `String(err)`→`String(errZZ)` rc 1; new-file hunk count `+1,95`→`+1,999` rc 128.

## Test Evidence
Author-run, locally, at head `f6565fa66532fa0a60e968ae22f664c71e22da08` (base `3f70224a069b`). `packages/shared` built.

- **RED (cell alone, product reverted — confirmed by blob id):** `Tests: 4 failed, 7 passed, 11 total` — the four B1 rows, one per route: `GET /dsr/pending`, `GET /retention`, `GET /deletion-log`, `GET /consent/check`, each driven by making that route's own service call reject on a real loopback listener. Zero crash signatures; 11 ran.
- **Control B5 makes B1 non-vacuous** (`String()` of the thrown object really is the lossy text); B3 and B4 pin the `Error` and `string` paths as unchanged.
- **GREEN:** `Tests: 11 passed, 11 total` after a sha256-verified restore.
- **originate suite, serial:** **bare 962 / 0 failed (82 suites)**, **patched 973 / 0 failed (83 suites)**, 0 new reds.
- **`tsc --noEmit` over a program PROVEN to contain both touched files** (715 files, each once by `--listFilesOnly`) → rc 0, 0 errors.
- **`packages/shared`:** 945 passed.
- **ESLint at BOTH trees:** 22 problems (0 errors, 22 warnings) each; 0 lines name either touched file. Control: planted `debugger` → `no-debugger` error, rc 1.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `..._fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 of 60** · `OK — 13 code guards passed` · zero `FIXTURE BUILD FAILED`.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`

**NOT run / NOT covered:**
- **No assessment of who can read originate's logs** — the question above, unresolved by design.
- No redaction added; none exists on this path.
- No stack (legs 3, 4, 8), no live sweep, no deploy, no integration/e2e against a real database.
- No cell asserts that a *real* GDPR repository error carries subject identifiers — the cells throw a synthetic object. The widening is demonstrated at the rendering level, not by capturing a production throw.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in. Foreign keys un-hyphenated throughout.
- Part A is a separate PR on `systemErrors.ts`; the two touch different files and do not overlap.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 ecd45938df7b56fcbe5b5456c3adeebab22cde2ed322919562bf0320ab7d7a9a

--- commit f6565fa66532fa0a60e968ae22f664c71e22da08
KS-1346 part B: log a non-Error throw from gdpr fail500 with inspect

fail500 in routes/gdpr.ts rendered a caught value with String(err) when it was
not an Error, so a thrown plain object reached the log as [object Object] and
its content was lost. It now uses inspect(err). The 500 body was already
constant, so this changes only what is LOGGED. Error and string throws render
exactly as before.

Two files, +97/-1: the product line plus its import, and a new cell driving the
four GDPR read routes on a real loopback listener by making each route's own
service call reject, with controls pinning the Error path, the string path, and
that String() of the thrown object really is lossy.

Raised from the brief's golden, byte-identical to the run's canonical patch.

Note for the reviewer, measured and recorded in the pull request body: this
route file logs through the service's own winston logger, which performs no
redaction, so an inspected thrown object reaches the log verbatim. That is the
intended effect of the change, but this is a subject-data surface.



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1346b-f6565fa66532-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-b32-ks1346b-f6565fa66532-push.out",
 "lines": 1305,
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
 "start": "2026-09-26T13:16:14Z PUSH START",
 "end": "2026-09-26T13:23:03Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB32-2026-09-26.md TEXT_SHA256 360ecddd008ede512989b1f943819db77acc9e5fa68661d7b93cb10bf7e495ab

# HANDOVER — Seat B 32nd, Secuura/Blockchain, round 28 (2026-09-26 11:17Z → ongoing)

Written to be read COLD. Nothing here assumes you were in the room.

## STATE IN ONE LINE
**SIX PRs raised and READY, none merged; a SEVENTH (KS-1347) built and STOPPED unpushed; four PRs closed unmerged on Kam's rulings; nothing deployed;
the shared checkout is byte-for-byte as I found it apart from one authorised fetch.** Two raises of the
six Wednesday listed are NOT started: **KS-1347 and KS-1339**.

## MY SIX OPEN PRs — all awaiting ONE gate
| PR | ticket | head | tier | base |
|---|---|---|---|---|
| **#1292** | KS-1341 part C | `ef821d2e27bf06ae1420bdb830ec7fffd7b8c732` | T1 | `3f70224a069b` |
| **#1293** | KS-1344 | `0ddffb6a52dbfa89ab71d7297c737c8b4d8722fd` | T2 | `3f70224a069b` |
| **#1294** | KS-1334 part A | `c43d5bb18f046a78cb8f2e4a39fe22fe8f9e3324` | T1 | `3f70224a069b` |
| **#1295** | KS-1337 akto site | `0faf41d63a75dfa348ed74ea328701646eea9c49` | T2 | `3f70224a069b` |
| **#1296** | KS-1346 part A | `eff979b3d493b973aaa4f91defe2c58f960c3f11` | T1 | `3f70224a069b` |
| **#1297** | KS-1346 part B | `f6565fa66532fa0a60e968ae22f664c71e22da08` | T1 | `3f70224a069b` |

Every one: raised byte-identical to its golden (measured by me, with a control), strict apply with no
recount and no fuzz, my own red/green, suites bare/patched, `tsc` over a program **proven** to contain
the touched files, the package's own lint at **both** trees with a planted-`debugger` control, and only
the gate lines that push actually printed. Full evidence is in each PR body.

## NOT STARTED — the two that remain, in order
1. 🔴 **KS-1347 — BUILT, VERIFIED, STOPPED AND UNPUSHED, awaiting Wednesday's (a)/(b).**
   Worktree `s-b32-ks1347` holds the golden applied, **uncommitted, no branch, no PR** (0 heads at
   origin matching `ks-1347`). **Do not remove that worktree until the answer lands.**
   Everything verifies except one thing: my `tsc` over a **test-inclusive** program finds **one NEW
   error, in the golden's own new cell** — `ks1347-…test.ts(24,40) TS6133: 'line' is declared but its
   value is never read` (the `.filter((line, i) => …)` callback uses only `i`). Proven new, not
   inherited: tip **37** errors vs head **38**, and the four `ks732` rows only MOVED by one line
   because my patch adds an import (`(293,37)→(294,51)` etc.) — a count-only comparison would have
   mis-reported this. **Every gate the repo actually runs is GREEN:** plain `tsc` rc 0 (it excludes
   `src/__tests__`), `npm run lint` rc 0 / 15 problems / 0 errors at both trees, vitest **bare 832 /
   patched 835, 0 new reds**; RED 1 of 3 with the edit reverted (no-spaces control green), GREEN 16/16;
   `cmp` rc 0 against **both** golden and canonical (5,407 B, sha256 `ce9ab6c59386b515…`).
   **Options mailed 13:3xZ:** (a) raise byte-identical and disclose; (b) rename the unused parameter
   (breaks byte-identity, as the KS-1337 `eslint --fix` did). Wednesday's last ruling on this shape was (b).
   ⚠ **`services/auth` runs VITEST, not jest.** My first run used jest and produced `Tests: 0 total`
   with a crash — a LOADFAIL, not a red.
   Original READY:
   `WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1347-KS732SPECPATHS_spark-dsv4flash_RUNG4-STRICT-R2-CODEPATCH-KS732-SPEC-PATHS-FILEURLTOPATH-PASS-7of7_2026-09-26.diff.md`
   (ADDENDUM 3, 12:07:18Z). Byte-identical to its golden per the hold record — **re-measure it yourself**.
   Run the **auth** package's own lint. No overlap with anything else in this stream.
2. **KS-1339** — ks1293 offender list before the count, originate TEST files only, **T2**. READY:
   `…/READY_KS-1339-KS1293OFFENDERFIRST_spark-dsv4flash_RUNG4-STRICT-CODEPATCH-OFFENDER-LIST-BEFORE-COUNT-PASS-7of7_2026-09-26.diff.md`
   (ADDENDUM 4, 12:24:35Z). Originate lint.

Neither has a worktree, a branch, a commit or a PR. **Nothing of mine is half-finished anywhere.**

## THE FINDING THAT NEEDS A DECISION ABOVE THIS SEAT
🔴 **KS-1346 A and B widen what reaches the log, and nothing on that path redacts it.** Wednesday asked
the gate to check whether inspecting a thrown object can put a secret or PII field in the log. It can:
- **Rendering:** a thrown `{ code, password, apiKey, email }` logged as `[object Object]` at the tip and
  logs its full contents at my head; a nested `ssn` likewise. `Error`, `string`, `null` paths unchanged.
- **Sink:** `systemErrors.ts:18` and `gdpr.ts:22` both import `logger` from `../utils/logger` — the
  service's own winston logger. I read all 77 lines: **no redaction, any environment.**
- The redacting logger (`packages/shared/src/logger/index.ts`) is **not on this path**, and keys off the
  **field name** — after `inspect()` the secret is a string value under the key `error`, so a thrown
  object with an SSN and no email survives its rules. (That last part is a reimplementation of its rules
  against a hypothetical, not a run of the real module — the load-bearing fact is the one above it.)

**This is inherent to the ticket, not a defect in the patch** — `[object Object]` has no diagnostic value.
But it is a real widening on an admin surface and, for part B, a **subject-data** surface. Whether it is
acceptable turns on who can read originate's logs. **No ticket has been filed** (the brief names none).
Mailed to Wednesday 13:0xZ and 13:2xZ; unanswered at the time of writing.

## TRAPS — the ones that cost me something tonight
1. 🔴 **A vacuous control is worse than no control, and I shipped two before catching them.**
   (a) My first tip-vs-head `tsc` comparison used `git -C <worktree> checkout -- <relpath>` from inside a
   subdirectory. The path did not resolve, the revert **silently failed**, and I compared the patched tree
   **against itself** — a guaranteed "IDENTICAL". (b) Twice I ran a key-scan "control" on a body that was
   already failing, so both arms FAILED identically and told me nothing. **Fix: confirm the revert by
   blob id before the second run, and run a control only against a subject that already PASSES.**
2. 🔴 **`grep 'ks1341c'` matched every path in the lint output** — my worktree is `s-b32-ks1341c`, so the
   token was in every absolute path. I briefly read "14 lint problems in the new cell"; the truth was 0.
   **Search on the real FILENAME, and pair the zero with a control that fires.**
3. 🔴 **A new-file section cannot be controlled by a path tamper** — a new file applies at any path, so
   that control passes and proves nothing. Corrupt the **hunk line count** instead (`+1,79` → `+1,999`,
   rc 128 "corrupt patch"). Used on every new-file section after I hit it on part C.
4. 🔴 **A quoted test title embeds a foreign ticket key.** Three PR bodies in a row failed the key scan
   because the evidence standard asks me to name a red set by title and those titles contain e.g.
   `KS-730 C3 SOURCE: …`. Un-hyphenating inside a quotation **falsifies the quotation**. My convention:
   name such rows descriptively (`C3 SOURCE`, `A1 GET /`) and say in the body that the cell's titles carry
   the key as file content. **Wednesday has been asked to rule; she had not when I wrote this.**
5. 🔴 **I created #1293 before its key scan passed.** The scan is now a **separate gating step whose PASS
   I read before the PR call**. It then refused #1294 twice, correctly, both times.
6. **A control that runs the real guard runs its side effects.** My new lock arm A11 performs a real
   release, which writes the rule-B cool-off stamp; the next arm then slept 90 s and died on its own
   30 s bound, and I briefly read that as "the inherited defect is live". It was not. A11 now asserts
   where the stamp landed and clears it.
7. **`packages/shared` rc 1 was my own bad flag** (`--reporter=basic` is not a reporter here): a startup
   error with **zero tests run**, not a red. A load failure and a red look nothing alike — check for
   `Startup Error` before reporting a suite as failing.
8. **Two goldens can share a name-stem.** `briefs/KS-1337.golden/KS-1337.golden.diff` is the **k6** site's
   and does NOT match the akto block; the matching one is `briefs/KS-1337/golden/KS-1337-akto.golden.diff`.
   **Pick by `cmp`, never by name.**
9. **The READY block is not always the canonical patch.** For KS-1346-A the hold record names the GOLDEN,
   and the model's own block differs by one extra trailing context line. My driver REFUSED the raise until
   pointed at the golden. Do not let a near-match through.

## MY TOOLS — all re-keyed and PROVEN before use, in `5_Project_History/2026-09-26_seatB-32nd/raise/`
`lock28.sh` `push28.sh` `push28_ff.sh` `namecheck28.py` `rekey_check28.py` `inbox_watch28.sh`
`inbox_match28.py` `merge28.py` `arms28.py` `keyscan28.py` + `raise28.py` (new) and `gatelines28.py` (new).
**Proofs:** watchproof28 **12/12** · lockproof28 **34/34** (incl. new arm **A11**, the release-from-another-
shell defect: it **refuses loudly, rc 3, lock intact**, and the holder-file pid is the recovery) ·
pushproof28 **22/22** · ffproof28 **28/28** · namecheck28 0 bad, **8/8** controls · rekey_check28
**0 DEFECT-LIVE over 13 files, 14/14 controls**, control A seeing 126 hits on B 31st's originals.
- **`raise28.py`** does the mechanical half of a raise and REFUSES loudly: extract, cmp vs golden and
  canonical, split into sections and prove the rejoin is byte-identical, `worktree add --detach` asserting
  `.git/config` is unchanged, strict apply-check per section **each with a tamper control that must fail**,
  apply, restore modes. `--patch` raises a golden instead of the READY block while still recording the diff.
- **`gatelines28.py`** parses the fleet STOP counts **per suite block by exact basename** — `pre_push_hook_base`
  is a prefix of `…_fixture_guard` (6/0) and `…_leg_comment` (4/0), and the log carries **two** count-line
  formats. My first parser read `None` for two of the three STOP suites and would have reported a MISMATCH
  that did not exist.
- 🔴 **Three inherited provenance lines were FALSE and I repaired them.** `lockproof27.sh:10`,
  `pushproof27.sh:10`, `ffproof27.sh:9` each RECORD Seat B 30th but a whole-file sed had rewritten them to
  name the 27-series scripts. B 30th's files are `lockproof26.sh`, `pushproof26.sh`, `ffproof26.sh` (measured
  by `ls`). **B 31st's own copies still carry the false lines** — Wednesday ruled: leave them, they are that
  seat's record. My sed is scoped to the live region so the class cannot recur.
- 🔴 **`rekey_check27.py`'s classifier was blind in BOTH directions** — it guessed Python prose from how a
  line starts/ends, so any LIVE line opening with `"The "` read as a comment. Now measured with `tokenize`.

## THE FLEET STOP COUNT — measured, not declared
On every `Blockchain/Dev` push of mine (#1292, #1293, #1294, #1296, #1297):
`pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** ·
`run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`OK — 13 code guards passed` · zero `^FIXTURE BUILD FAILED` ·
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — no local stack).
⚠ **#1295 (akto) is the exception and must not be quoted with those figures.** It touches no
`Blockchain/Dev` path, so the platform preflight **never ran**; what ran was
`[format-gate] systemTest/akto — format:check OK`, `1 package(s) checked, 0 skipped, 0 failed`.
Measured with a control: those preflight tokens appear **0** times in that push's log and **4 / 1 / 4**
times in a `Blockchain/Dev` push. A missing gate is not a passing gate.

## ITEM 3 — the four closes, done and verified
**#1268, #1278, #1245, #1241 closed unmerged** on Kam's two rulings of 2026-09-26 21:04, each with one
facts-only comment approved verbatim by Wednesday. After each: `state: closed`, `merged: false`,
`merged_at: null`, head UNCHANGED, and the branch refs still at origin (verified by `ls-remote`).
Comment URLs are in my mail of 12:33Z. Residue: #1268→KS1338 (+KS1316), #1278→KS1314's own 04:44:47Z
comment, #1245→KS1326+KS1313, #1241→KS1313 (+KS1226 item 1, the `:127` budget, still open).

## STATE AT WRAP — measured
Shared checkout **never written** beyond the one authorised fetch: HEAD `3bad652d17cf`, local `develop`
`3bad652d17cf`, **17 `??` / 0 non-`??`**, `.git/config` sha256 `870a35e2163629ca…` — all identical to boot.
`origin/develop` `3f70224a069b` (moved only by my ITEM-0 fetch: exactly **one** ref value of 1468, reflog
confirming a fast-forward). **No `.push-lock-*` exists.** All six `s-b32-*` worktrees are **porcelain 0,
pushed, idle and removable**. All six branches sit at origin at exactly my heads.
**Nothing deployed. No ticket filed. No ticket state moved by me** (KS-1344 walked Backlog → In Progress
on PR open, which is the bot's expected behaviour).

## THE ONE THING I WOULD MOST WANT A SUCCESSOR TO INHERIT
🔴 **Every check I ran tonight that turned out to be worthless was worthless in the same way: it could not
have failed.** A revert that silently did not happen. A control run against an already-failing subject. A
grep whose token was in every path. A path tamper on a new file. In each case the output looked like
success and meant nothing. **Before you believe a green, make it go red on purpose once** — and when a
control and its subject agree, check that they *can* disagree. That single habit caught four bad
measurements tonight, and it is the only reason the numbers in those six PR bodies are worth reading.

## THE AUDIT FUSE — still Kam's
🔴 **Both audit rows lapse `2026-09-30T00:00Z`.** From then every `Blockchain/Dev` push AND merge is
refused, from every author. Nothing tonight touched it and nothing in my queue averts it. It needs
**Kam's own typed word** — his line in the pane, or mail carrying `dmarc=pass header.from=me.com`. A
Wednesday relay does not substitute. Also his: **KS-1267**, **KS-1304**, and the two audit re-dates
(frvp under KS-530, mwp4 under KS-729).

## ALSO INHERITED, NOT MINE TO FIX
⚠ **This project's `MEMORY.md` is 215 lines against its own 200-line limit**, so the loader truncates the
tail — and the first line cut is "Never pull OR fetch the shared checkout in seat rounds", which is exactly
the rule governing ITEM 0. I only had it because I opened the file directly. B 31st flagged this at 213
lines; it has grown since. Flagged to Wednesday again tonight.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/c-RED.out TEXT_SHA256 3dda2ad6649100a9c7593a331e83ab316ac2c1cbeddfb3da1f2a9155a19c0e26

FAIL src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts (6.844 s)
  KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text
    ✕ RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset (22 ms)
    ✕ RED KS-1341 C1 GET /:id/deliveries: the thrown message is not in the 500 body under production, development, test or unset (3 ms)
    ✕ RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named (2 ms)
    ✕ RED KS-1341 C2 GET /:id/deliveries: the thrown message is logged once, server-side, with this route named (1 ms)
    ✕ RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts (2 ms)
    ✓ control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch (6 ms)
    ✓ control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing (2 ms)
    ✓ control KS-1341 C: the LEAK string is the thrown text and dodges every benign branch

  ● KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text › RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset

    expect(received).toEqual(expected) // deep equality

    - Expected  - 1
    + Received  + 1

      Object {
    -   "leaked": false,
    +   "leaked": true,
        "nodeEnv": "production",
        "status": 500,
      }

      110 |       mockLoggerError.mockClear();
      111 |       const reply = await call(route, nodeEnv);
    > 112 |       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
          |                                                                                    ^
      113 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      114 |       // REACHED in THIS environment, not merely clean: exactly one call, this route's context, the thrown text.
      115 |       expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: LEAK }]] });

      at src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts:112:84

  ● KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text › RED KS-1341 C1 GET /:id/deliveries: the thrown message is not in the 500 body under production, development, test or unset

    expect(received).toEqual(expected) // deep equality

    - Expected  - 1
    + Received  + 1

      Object {
    -   "leaked": false,
    +   "leaked": true,
        "nodeEnv": "production",
        "status": 500,
      }

      110 |       mockLoggerError.mockClear();
      111 |       const reply = await call(route, nodeEnv);
    > 112 |       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
          |                                                                                    ^
      113 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      114 |       // REACHED in THIS environment, not merely clean: exactly one call, this route's context, the thrown text.
      115 |       expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: LEAK }]] });

      at src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts:112:84

  ● KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text › RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named

    expect(received).toEqual(expected) // deep equality

    - Expected  - 8
    + Received  + 1

    - Array [
    -   Array [
    -     "Webhook test send failed (POST /api/webhooks/:id/test)",
    -     Object {
    -       "error": "canceling statement due to statement timeout on svc_webhook_deliveries ks1341c-private-detail",
    -     },
    -   ],
    - ]
    + Array []

      120 |     const reply = await call(route, 'production');
      121 |     expect(reply.status).toBe(500);
    > 122 |     expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
          |                                        ^
      123 |   });
      124 |
      125 |   it('RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts', () => {

      at src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts:122:40

  ● KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text › RED KS-1341 C2 GET /:id/deliveries: the thrown message is logged once, server-side, with this route named

    expect(received).toEqual(expected) // deep equality

    - Expected  - 8
    + Received  + 1

    - Array [
    -   Array [
    -     "Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)",
    -     Object {
    -       "error": "canceling statement due to statement timeout on svc_webhook_deliveries ks1341c-private-detail",
    -     },
    -   ],
    - ]
    + Array []

      120 |     const reply = await call(route, 'production');
      121 |     expect(reply.status).toBe(500);
    > 122 |     expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
          |                                        ^
      123 |   });
      124 |
      125 |   it('RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts', () => {

      at src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts:122:40

  ● KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text › RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts

    expect(received).toEqual(expected) // deep equality

    - Expected  - 3
    + Received  + 3

      Object {
        "definitions": 1,
    -   "distinctContexts": 7,
    -   "helperCalls": 7,
    -   "leaks": 0,
    +   "distinctContexts": 5,
    +   "helperCalls": 5,
    +   "leaks": 2,
      }

      134 |     const definitions = lines.filter((l) => l.startsWith('function fail500('));
      135 |     expect({ leaks: leaks.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size, definitions: definitions.length })
    > 136 |       .toEqual({ leaks: 0, helperCalls: 7, distinctContexts: 7, definitions: 1 });
          |        ^
      137 |     expect(contexts.filter((c) => !c)).toEqual([]);
      138 |   });
      139 |

      at Object.<anonymous> (src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts:136:8)

Test Suites: 1 failed, 1 total
Tests:       5 failed, 3 passed, 8 total
Snapshots:   0 total
Time:        7.159 s
Ran all test suites matching /src\/__tests__\/ks1341c-webhooks-500-never-answers-err-message.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/c-GREEN.out TEXT_SHA256 bfe39989e8fed0dedd2859d2fe25fc47064bc003a530cea64904d829066d3868

PASS src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
  KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text
    ✓ RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset (18 ms)
    ✓ RED KS-1341 C1 GET /:id/deliveries: the thrown message is not in the 500 body under production, development, test or unset (3 ms)
    ✓ RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ RED KS-1341 C2 GET /:id/deliveries: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts
    ✓ control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch (1 ms)
    ✓ control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing (1 ms)
    ✓ control KS-1341 C: the LEAK string is the thrown text and dodges every benign branch

Test Suites: 1 passed, 1 total
Tests:       8 passed, 8 total
Snapshots:   0 total
Time:        2.574 s, estimated 7 s
Ran all test suites matching /src\/__tests__\/ks1341c-webhooks-500-never-answers-err-message.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/c-TAMPER-C1.out TEXT_SHA256 e51fb5e75919f4a44ac37b697e85c194044b55f1c00f630358a0da6e2c532007

FAIL src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
  KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text
    ✕ RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset (21 ms)
    ✕ RED KS-1341 C1 GET /:id/deliveries: the thrown message is not in the 500 body under production, development, test or unset (3 ms)
    ✓ RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ RED KS-1341 C2 GET /:id/deliveries: the thrown message is logged once, server-side, with this route named
    ✓ RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts (1 ms)
    ✓ control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch (1 ms)
    ✓ control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing (1 ms)
    ✓ control KS-1341 C: the LEAK string is the thrown text and dodges every benign branch

  ● KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text › RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset

    expect(received).toEqual(expected) // deep equality

    - Expected  - 8
    + Received  + 1

      Object {
    -   "calls": Array [
    -     Array [
    -       "Webhook test send failed (POST /api/webhooks/:id/test)",
    -       Object {
    -         "error": "canceling statement due to statement timeout on svc_webhook_deliveries ks1341c-private-detail",
    -       },
    -     ],
    -   ],
    +   "calls": Array [],
        "nodeEnv": "development",
      }

      113 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      114 |       // REACHED in THIS environment, not merely clean: exactly one call, this route's context, the thrown text.
    > 115 |       expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: LEAK }]] });
          |                                                              ^
      116 |     }
      117 |   });
      118 |

      at src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts:115:62

  ● KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text › RED KS-1341 C1 GET /:id/deliveries: the thrown message is not in the 500 body under production, development, test or unset

    expect(received).toEqual(expected) // deep equality

    - Expected  - 8
    + Received  + 1

      Object {
    -   "calls": Array [
    -     Array [
    -       "Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)",
    -       Object {
    -         "error": "canceling statement due to statement timeout on svc_webhook_deliveries ks1341c-private-detail",
    -       },
    -     ],
    -   ],
    +   "calls": Array [],
        "nodeEnv": "development",
      }

      113 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      114 |       // REACHED in THIS environment, not merely clean: exactly one call, this route's context, the thrown text.
    > 115 |       expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: LEAK }]] });
          |                                                              ^
      116 |     }
      117 |   });
      118 |

      at src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts:115:62

Test Suites: 1 failed, 1 total
Tests:       2 failed, 6 passed, 8 total
Snapshots:   0 total
Time:        2.365 s, estimated 3 s
Ran all test suites matching /src\/__tests__\/ks1341c-webhooks-500-never-answers-err-message.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/c-lint-HEAD.out TEXT_SHA256 e32d7eb1d5152af8389588a91f74246c982a7c49eaa30c3e299cbde4a92a3ceb


> @secuura/originate@0.1.0 lint
> eslint src


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts
  145:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  326:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  549:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts
  19:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts
  36:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks566-g1-split.test.ts
  32:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts
  45:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unused-vars')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks587-anchors-honest-simulated.test.ts
  16:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts
   87:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
   89:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  102:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts
  38:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/rightsHolders.tenant-scope.integration.test.ts
  122:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  124:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  126:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  128:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
  62:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
  143:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
  2089:13  warning  'copied' is never reassigned. Use 'const' instead  prefer-const
  2129:20  warning  'e' is defined but never used                      @typescript-eslint/no-unused-vars

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/routes/anchors.ts
  53:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
  128:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

✖ 22 problems (0 errors, 22 warnings)
  0 errors and 14 warnings potentially fixable with the `--fix` option.



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/c-lint-CONTROL.out TEXT_SHA256 acdfad77fe0cca477f2f3ebb81ccf0b2739aaf278eeae8b0e50862ff06db9314


> @secuura/originate@0.1.0 lint
> eslint src


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts
  145:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  326:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  549:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
  171:1  error  Unexpected 'debugger' statement  no-debugger

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts
  19:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts
  36:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks566-g1-split.test.ts
  32:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts
  45:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unused-vars')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks587-anchors-honest-simulated.test.ts
  16:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts
   87:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
   89:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  102:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts
  38:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/__tests__/rightsHolders.tenant-scope.integration.test.ts
  122:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  124:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  126:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  128:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
  62:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
  143:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
  2089:13  warning  'copied' is never reassigned. Use 'const' instead  prefer-const
  2129:20  warning  'e' is defined but never used                      @typescript-eslint/no-unused-vars

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/routes/anchors.ts
  53:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
  128:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

✖ 23 problems (1 error, 22 warnings)
  0 errors and 14 warnings potentially fixable with the `--fix` option.

npm error Lifecycle script `lint` failed with error:
npm error code 1
npm error path /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate
npm error workspace @secuura/originate@0.1.0
npm error location /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1341c/Blockchain/Dev/services/originate
npm error command failed
npm error command sh -c eslint src


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/c-tsc-testfile.out TEXT_SHA256 de11974a9266f2be636a34276623fb66eab65be8c608a7ba116247715a0d23fa

src/routes/webhooks.ts(221,131): error TS2339: Property 'error' does not exist on type '{ ok: true; url: string; } | { ok: false; error: string; }'.
  Property 'error' does not exist on type '{ ok: true; url: string; }'.
src/routes/webhooks.ts(298,133): error TS2339: Property 'error' does not exist on type '{ ok: true; url: string; } | { ok: false; error: string; }'.
  Property 'error' does not exist on type '{ ok: true; url: string; }'.
src/routes/webhooks.ts(474,16): error TS2339: Property 'reason' does not exist on type 'SafeOutboundResult'.
  Property 'reason' does not exist on type '{ ok: true; response: SafeOutboundResponse; }'.
src/routes/webhooks.ts(475,83): error TS2339: Property 'error' does not exist on type 'SafeOutboundResult'.
  Property 'error' does not exist on type '{ ok: true; response: SafeOutboundResponse; }'.
src/routes/webhooks.ts(480,49): error TS2339: Property 'error' does not exist on type 'SafeOutboundResult'.
  Property 'error' does not exist on type '{ ok: true; response: SafeOutboundResponse; }'.
src/routes/webhooks.ts(483,66): error TS2339: Property 'error' does not exist on type 'SafeOutboundResult'.
  Property 'error' does not exist on type '{ ok: true; response: SafeOutboundResponse; }'.
src/routes/webhooks.ts(488,21): error TS2339: Property 'error' does not exist on type 'SafeOutboundResult'.
  Property 'error' does not exist on type '{ ok: true; response: SafeOutboundResponse; }'.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/a-RED.out TEXT_SHA256 249494ad1ed60c5c635db984420c50900b36b9be069aa5ba47603b18c8907c84

FAIL src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
  KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message
    ✓ RED KS-730 C1 GET /settings: the thrown message is not in the 500 body under development, demo, test or unset (19 ms)
    ✓ RED KS-730 C1 GET /document-types: the thrown message is not in the 500 body under development, demo, test or unset (3 ms)
    ✓ RED KS-730 C1 GET /workflows: the thrown message is not in the 500 body under development, demo, test or unset (3 ms)
    ✓ RED KS-730 C1 GET /organizations: the thrown message is not in the 500 body under development, demo, test or unset (2 ms)
    ✓ RED KS-730 C2 GET /settings: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ RED KS-730 C2 GET /document-types: the thrown message is logged once, server-side, with this route named
    ✓ RED KS-730 C2 GET /workflows: the thrown message is logged once, server-side, with this route named
    ✓ RED KS-730 C2 GET /organizations: the thrown message is logged once, server-side, with this route named
    ✕ KS-730 C3 SOURCE: all forty-six sites are routed through the helper, each with a DISTINCT context (2 ms)
    ✓ control KS-730 C0: a "does not exist" error still answers 200 and never reaches fail500 (2 ms)
    ✕ KS-730 C4 SOURCE: the four UNCONDITIONAL err.message sites are named, not silently left (1 ms)
    ✓ control KS-730 C: under production these routes already answered the constant text (2 ms)
    ✓ control KS-730 C: a route that does NOT throw answers 200 and logs nothing
    ✓ control KS-730 C: the LEAK string really is the thrown text, so "not leaked" is not vacuous
  KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message
    ✕ RED KS-1334 A1 POST /refresh-tenants: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it (22 ms)
    ✕ RED KS-1334 A1 POST /backfill-certification-metadata: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it (1 ms)
    ✓ control KS-1334 A0 POST /refresh-tenants: a call that does not throw answers 200 and logs nothing
    ✓ control KS-1334 A0 POST /backfill-certification-metadata: a call that does not throw answers 200 and logs nothing (1 ms)
    ✓ control KS-1334 A2: KS1334_LEAK survives JSON encoding, so leaked: false above is not vacuous

  ● KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message › KS-730 C3 SOURCE: all forty-six sites are routed through the helper, each with a DISTINCT context

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "distinctContexts": 48,
    -   "helperCalls": 48,
    +   "distinctContexts": 46,
    +   "helperCalls": 46,
        "liveTernaries": 0,
      }

      140 |     // it sends a reader to the wrong handler. 46 generated strings could silently collide.
      141 |     expect({ liveTernaries: liveTernaries.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size })
    > 142 |       .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });
          |        ^
      143 |     expect(contexts.filter((c) => !c)).toEqual([]);
      144 |   });
      145 |

      at Object.<anonymous> (src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts:142:8)

  ● KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message › KS-730 C4 SOURCE: the four UNCONDITIONAL err.message sites are named, not silently left

    expect(received).toEqual(expected) // deep equality

    - Expected  - 0
    + Received  + 2

      Array [
    +   "POST /refresh-tenants",
    +   "POST /backfill-certification-metadata",
        "POST /seed-demo-users",
        "POST /migrate-tenant-data",
      ]

      179 |       if (/message: *err\??\.?message/.test(line)) found.push(route);
      180 |     }
    > 181 |     expect(found).toEqual(KNOWN);
          |                   ^
      182 |   });
      183 |
      184 |   it('control KS-730 C: under production these routes already answered the constant text', async () => {

      at Object.<anonymous> (src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts:181:19)

  ● KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message › RED KS-1334 A1 POST /refresh-tenants: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it

    expect(received).toEqual(expected) // deep equality

    - Expected  - 1
    + Received  + 1

      Object {
    -   "leaked": false,
    +   "leaked": true,
        "nodeEnv": "production",
        "status": 500,
      }

      238 |       mockLoggerError.mockClear();
      239 |       const reply = await post1334(route, nodeEnv, true);
    > 240 |       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
          |                                                                                           ^
      241 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      242 |       expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
      243 |     }

      at src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts:240:91

  ● KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message › RED KS-1334 A1 POST /backfill-certification-metadata: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it

    expect(received).toEqual(expected) // deep equality

    - Expected  - 1
    + Received  + 1

      Object {
    -   "leaked": false,
    +   "leaked": true,
        "nodeEnv": "production",
        "status": 500,
      }

      238 |       mockLoggerError.mockClear();
      239 |       const reply = await post1334(route, nodeEnv, true);
    > 240 |       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
          |                                                                                           ^
      241 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      242 |       expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
      243 |     }

      at src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts:240:91

Test Suites: 1 failed, 1 total
Tests:       4 failed, 15 passed, 19 total
Snapshots:   0 total
Time:        3.416 s
Ran all test suites matching /src\/__tests__\/ks730c-adminconfig-500-never-answers-err-message.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/a-GREEN.out TEXT_SHA256 b326d23272432bfe98d20d92376bc05a3df25d5d97d821c9bd3f3ae91c1d84c9

PASS src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
  KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message
    ✓ RED KS-730 C1 GET /settings: the thrown message is not in the 500 body under development, demo, test or unset (16 ms)
    ✓ RED KS-730 C1 GET /document-types: the thrown message is not in the 500 body under development, demo, test or unset (3 ms)
    ✓ RED KS-730 C1 GET /workflows: the thrown message is not in the 500 body under development, demo, test or unset (5 ms)
    ✓ RED KS-730 C1 GET /organizations: the thrown message is not in the 500 body under development, demo, test or unset (2 ms)
    ✓ RED KS-730 C2 GET /settings: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ RED KS-730 C2 GET /document-types: the thrown message is logged once, server-side, with this route named
    ✓ RED KS-730 C2 GET /workflows: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ RED KS-730 C2 GET /organizations: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ KS-730 C3 SOURCE: all forty-six sites are routed through the helper, each with a DISTINCT context
    ✓ control KS-730 C0: a "does not exist" error still answers 200 and never reaches fail500 (1 ms)
    ✓ KS-730 C4 SOURCE: the four UNCONDITIONAL err.message sites are named, not silently left (1 ms)
    ✓ control KS-730 C: under production these routes already answered the constant text (1 ms)
    ✓ control KS-730 C: a route that does NOT throw answers 200 and logs nothing
    ✓ control KS-730 C: the LEAK string really is the thrown text, so "not leaked" is not vacuous
  KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message
    ✓ RED KS-1334 A1 POST /refresh-tenants: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it (9 ms)
    ✓ RED KS-1334 A1 POST /backfill-certification-metadata: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it (3 ms)
    ✓ control KS-1334 A0 POST /refresh-tenants: a call that does not throw answers 200 and logs nothing
    ✓ control KS-1334 A0 POST /backfill-certification-metadata: a call that does not throw answers 200 and logs nothing
    ✓ control KS-1334 A2: KS1334_LEAK survives JSON encoding, so leaked: false above is not vacuous

Test Suites: 1 passed, 1 total
Tests:       19 passed, 19 total
Snapshots:   0 total
Time:        2.25 s, estimated 4 s
Ran all test suites matching /src\/__tests__\/ks730c-adminconfig-500-never-answers-err-message.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/a-lint-HEAD.out TEXT_SHA256 4f7f829a8d317da90a1604989de8d753145f548715e56bbea9cf5384e540c0b3


> @secuura/originate@0.1.0 lint
> eslint src


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts
  145:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  326:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  549:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts
  19:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts
  36:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks566-g1-split.test.ts
  32:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts
  45:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unused-vars')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks587-anchors-honest-simulated.test.ts
  16:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts
   87:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
   89:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  102:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts
  38:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/rightsHolders.tenant-scope.integration.test.ts
  122:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  124:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  126:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  128:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
  62:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
  143:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
  2089:13  warning  'copied' is never reassigned. Use 'const' instead  prefer-const
  2129:20  warning  'e' is defined but never used                      @typescript-eslint/no-unused-vars

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/routes/anchors.ts
  53:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
  128:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

✖ 22 problems (0 errors, 22 warnings)
  0 errors and 14 warnings potentially fixable with the `--fix` option.



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/a-lint-CONTROL.out TEXT_SHA256 758f2ac8846c6b84598b744289eb638586a336f4a08fa1bb6a9b36777c8c081b


> @secuura/originate@0.1.0 lint
> eslint src


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts
  145:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  326:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  549:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts
  19:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts
  36:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks566-g1-split.test.ts
  32:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts
  45:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unused-vars')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks587-anchors-honest-simulated.test.ts
  16:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts
   87:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
   89:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  102:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
  258:1  error  Unexpected 'debugger' statement  no-debugger

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts
  38:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/__tests__/rightsHolders.tenant-scope.integration.test.ts
  122:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  124:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  126:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  128:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
  62:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
  143:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
  2089:13  warning  'copied' is never reassigned. Use 'const' instead  prefer-const
  2129:20  warning  'e' is defined but never used                      @typescript-eslint/no-unused-vars

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/routes/anchors.ts
  53:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
  128:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

✖ 23 problems (1 error, 22 warnings)
  0 errors and 14 warnings potentially fixable with the `--fix` option.

npm error Lifecycle script `lint` failed with error:
npm error code 1
npm error path /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate
npm error workspace @secuura/originate@0.1.0
npm error location /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1334a/Blockchain/Dev/services/originate
npm error command failed
npm error command sh -c eslint src


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-RED.out TEXT_SHA256 9f3a6ac7de42ac1b1276543838b4601d55a57011bbc4b48089b725e53399148b

FAIL src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts
  KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log
    ✕ RED KS-1346 A1 GET /stats: a thrown plain object is logged with its content, once, under this route (14 ms)
    ✕ RED KS-1346 A1 GET /: a thrown plain object is logged with its content, once, under this route (2 ms)
    ✕ RED KS-1346 A1 PATCH /:errorId/resolve: a thrown plain object is logged with its content, once, under this route (21 ms)
    ✕ RED KS-1346 A1 POST /resolve-by-service: a thrown plain object is logged with its content, once, under this route (1 ms)
    ✓ control KS-1346 A2 GET /stats: the 500 body stays the constant text for an object throw
    ✓ control KS-1346 A2 GET /: the 500 body stays the constant text for an object throw
    ✓ control KS-1346 A2 PATCH /:errorId/resolve: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 A2 POST /resolve-by-service: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 A3: an Error throw still logs exactly its message (1 ms)
    ✓ control KS-1346 A4: a string throw still logs exactly itself, not a quoted rendering
    ✓ control KS-1346 A5: String() of the thrown object really is the lossy text, so A1 is not vacuous

  ● KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log › RED KS-1346 A1 GET /stats: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      73 |     expect(context).toBe(route.context);
      74 |     expect(typeof meta.error).toBe('string');
    > 75 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                       ^
      76 |   });
      77 |
      78 |   it.each(ROUTES)('control KS-1346 A2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts:75:119

  ● KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log › RED KS-1346 A1 GET /: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      73 |     expect(context).toBe(route.context);
      74 |     expect(typeof meta.error).toBe('string');
    > 75 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                       ^
      76 |   });
      77 |
      78 |   it.each(ROUTES)('control KS-1346 A2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts:75:119

  ● KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log › RED KS-1346 A1 PATCH /:errorId/resolve: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      73 |     expect(context).toBe(route.context);
      74 |     expect(typeof meta.error).toBe('string');
    > 75 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                       ^
      76 |   });
      77 |
      78 |   it.each(ROUTES)('control KS-1346 A2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts:75:119

  ● KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log › RED KS-1346 A1 POST /resolve-by-service: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      73 |     expect(context).toBe(route.context);
      74 |     expect(typeof meta.error).toBe('string');
    > 75 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                       ^
      76 |   });
      77 |
      78 |   it.each(ROUTES)('control KS-1346 A2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts:75:119

Test Suites: 1 failed, 1 total
Tests:       4 failed, 7 passed, 11 total
Snapshots:   0 total
Time:        2.951 s
Ran all test suites matching /src\/__tests__\/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-GREEN.out TEXT_SHA256 4f32388228fcf61fde2452c0074a8d170f4df14b1d95372152211b34f4d99543

PASS src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts
  KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log
    ✓ RED KS-1346 A1 GET /stats: a thrown plain object is logged with its content, once, under this route (13 ms)
    ✓ RED KS-1346 A1 GET /: a thrown plain object is logged with its content, once, under this route (2 ms)
    ✓ RED KS-1346 A1 PATCH /:errorId/resolve: a thrown plain object is logged with its content, once, under this route (9 ms)
    ✓ RED KS-1346 A1 POST /resolve-by-service: a thrown plain object is logged with its content, once, under this route (1 ms)
    ✓ control KS-1346 A2 GET /stats: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 A2 GET /: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 A2 PATCH /:errorId/resolve: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 A2 POST /resolve-by-service: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 A3: an Error throw still logs exactly its message (1 ms)
    ✓ control KS-1346 A4: a string throw still logs exactly itself, not a quoted rendering
    ✓ control KS-1346 A5: String() of the thrown object really is the lossy text, so A1 is not vacuous (1 ms)

Test Suites: 1 passed, 1 total
Tests:       11 passed, 11 total
Snapshots:   0 total
Time:        1.939 s, estimated 3 s
Ran all test suites matching /src\/__tests__\/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-inspect-probe.mjs TEXT_SHA256 738204a7551f8593fef50a51c5223aa76158301dfe1c0b4d360e82443e026919

import { inspect } from 'util';
// The two renderings, copied from the tip and the head of systemErrors.ts fail500.
const TIP  = (err) => (err instanceof Error ? err.message : String(err));
const HEAD = (err) => (err instanceof Error ? err.message : typeof err === 'string' ? err : inspect(err));
const cases = [
  ['plain object with secret-looking fields',
     { code: 'P0001', password: 'hunter2', apiKey: 'sk_live_DEADBEEF', email: 'subject@example.test' }],
  ['nested object',            { outer: { inner: { ssn: '123-45-6789' } } }],
  ['Error (unchanged path)',   new Error('an ordinary error message')],
  ['string (unchanged path)',  'a plain string throw'],
  ['null',                     null],
];
const NEEDLES = ['hunter2','sk_live_DEADBEEF','subject@example.test','123-45-6789'];
for (const [label, v] of cases) {
  const t = TIP(v), h = HEAD(v);
  const leakT = NEEDLES.filter(n => String(t).includes(n));
  const leakH = NEEDLES.filter(n => String(h).includes(n));
  console.log(`  ${label}`);
  console.log(`     tip  -> ${JSON.stringify(String(t)).slice(0,110)}   secrets: ${leakT.length ? leakT.join(',') : 'none'}`);
  console.log(`     head -> ${JSON.stringify(String(h)).slice(0,110)}   secrets: ${leakH.length ? leakH.join(',') : 'none'}`);
  console.log(`     CHANGED: ${t === h ? 'no' : 'YES'}`);
}


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-inspect-probe.out TEXT_SHA256 3ae282bbc3ead2b6586a4db491b6f5cfec5197496ae22aa221f46bafc36ed49b

  plain object with secret-looking fields
     tip  -> "[object Object]"   secrets: none
     head -> "{\n  code: 'P0001',\n  password: 'hunter2',\n  apiKey: 'sk_live_DEADBEEF',\n  email: 'subject@example.test'\n   secrets: hunter2,sk_live_DEADBEEF,subject@example.test
     CHANGED: YES
  nested object
     tip  -> "[object Object]"   secrets: none
     head -> "{ outer: { inner: { ssn: '123-45-6789' } } }"   secrets: 123-45-6789
     CHANGED: YES
  Error (unchanged path)
     tip  -> "an ordinary error message"   secrets: none
     head -> "an ordinary error message"   secrets: none
     CHANGED: no
  string (unchanged path)
     tip  -> "a plain string throw"   secrets: none
     head -> "a plain string throw"   secrets: none
     CHANGED: no
  null
     tip  -> "null"   secrets: none
     head -> "null"   secrets: none
     CHANGED: no


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-redact-probe.mjs TEXT_SHA256 31aa64166866c92ec23ce50482b6895373f6a475ff57b3a6a28b2f28da8b0390

import { inspect } from 'util';
// Reproduce the shared redactor's rule shape: it keys off the FIELD NAME, plus an email substring rule.
const SENSITIVE = new Set(['password','apikey','api_key','secret','token','ssn','email']);
function redactValue(key, value) {
  if (typeof value !== 'string') return value;
  const lk = key.toLowerCase();
  if (SENSITIVE.has(key) || SENSITIVE.has(lk)) return '***REDACTED***';
  if (value.includes('@') && value.includes('.')) return '***REDACTED***';
  return value;
}
const thrown = { code:'P0001', password:'hunter2', apiKey:'sk_live_DEADBEEF', email:'subject@example.test' };
const nested = { outer:{ inner:{ ssn:'123-45-6789' } } };
for (const [label, obj] of [['flat',thrown],['nested',nested]]) {
  const asString = inspect(obj);                 // what fail500 now passes
  const meta = { error: asString };              // the shape logger.error receives
  const out = Object.fromEntries(Object.entries(meta).map(([k,v]) => [k, redactValue(k,v)]));
  const shown = String(out.error);
  console.log(`  ${label}: key is ${JSON.stringify(Object.keys(meta))} -> redactor sees key 'error', not 'password'`);
  for (const n of ['hunter2','sk_live_DEADBEEF','123-45-6789','subject@example.test'])
    if (asString.includes(n)) console.log(`     '${n}' ${shown.includes(n) ? 'SURVIVES redaction' : 'redacted'}`);
}


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-redact-probe.out TEXT_SHA256 852a429f5cdeb4d08445ddcf55ec74ea4ccc3064812757defa8df0cfea7e0613

  flat: key is ["error"] -> redactor sees key 'error', not 'password'
     'hunter2' redacted
     'sk_live_DEADBEEF' redacted
     'subject@example.test' redacted
  nested: key is ["error"] -> redactor sees key 'error', not 'password'
     '123-45-6789' SURVIVES redaction


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/s-lint-HEAD.out TEXT_SHA256 1f5044e0a2688249bfdcc52cfc83d2cc1896a9752c77f9e7cf9026e782595b7f


> @secuura/originate@0.1.0 lint
> eslint src


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts
  145:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  326:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  549:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts
  19:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts
  36:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/ks566-g1-split.test.ts
  32:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts
  45:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unused-vars')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/ks587-anchors-honest-simulated.test.ts
  16:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts
   87:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
   89:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  102:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts
  38:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/__tests__/rightsHolders.tenant-scope.integration.test.ts
  122:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  124:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  126:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  128:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
  62:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
  143:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
  2089:13  warning  'copied' is never reassigned. Use 'const' instead  prefer-const
  2129:20  warning  'e' is defined but never used                      @typescript-eslint/no-unused-vars

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/routes/anchors.ts
  53:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346a/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
  128:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

✖ 22 problems (0 errors, 22 warnings)
  0 errors and 14 warnings potentially fixable with the `--fix` option.



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/g-RED.out TEXT_SHA256 76dabb9bfffb354dc5bad5c4029ffbdf8d3ccaf92c9ae2f6ec2566db4a3ea868

FAIL src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts
  KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log
    ✕ RED KS-1346 B1 GET /dsr/pending: a thrown plain object is logged with its content, once, under this route (14 ms)
    ✕ RED KS-1346 B1 GET /retention: a thrown plain object is logged with its content, once, under this route (2 ms)
    ✕ RED KS-1346 B1 GET /deletion-log: a thrown plain object is logged with its content, once, under this route (1 ms)
    ✕ RED KS-1346 B1 GET /consent/check: a thrown plain object is logged with its content, once, under this route (2 ms)
    ✓ control KS-1346 B2 GET /dsr/pending: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 B2 GET /retention: the 500 body stays the constant text for an object throw
    ✓ control KS-1346 B2 GET /deletion-log: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 B2 GET /consent/check: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 B3: an Error throw still logs exactly its message
    ✓ control KS-1346 B4: a string throw still logs exactly itself, not a quoted rendering (1 ms)
    ✓ control KS-1346 B5: String() of the thrown object really is the lossy text, so B1 is not vacuous

  ● KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log › RED KS-1346 B1 GET /dsr/pending: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      71 |     expect(context).toBe(route.context);
      72 |     expect(typeof meta.error).toBe('string');
    > 73 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346B_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                        ^
      74 |   });
      75 |
      76 |   it.each(ROUTES)('control KS-1346 B2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts:73:120

  ● KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log › RED KS-1346 B1 GET /retention: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      71 |     expect(context).toBe(route.context);
      72 |     expect(typeof meta.error).toBe('string');
    > 73 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346B_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                        ^
      74 |   });
      75 |
      76 |   it.each(ROUTES)('control KS-1346 B2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts:73:120

  ● KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log › RED KS-1346 B1 GET /deletion-log: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      71 |     expect(context).toBe(route.context);
      72 |     expect(typeof meta.error).toBe('string');
    > 73 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346B_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                        ^
      74 |   });
      75 |
      76 |   it.each(ROUTES)('control KS-1346 B2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts:73:120

  ● KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log › RED KS-1346 B1 GET /consent/check: a thrown plain object is logged with its content, once, under this route

    expect(received).toEqual(expected) // deep equality

    - Expected  - 2
    + Received  + 2

      Object {
    -   "hasCode": true,
    -   "hasDetail": true,
    +   "hasCode": false,
    +   "hasDetail": false,
      }

      71 |     expect(context).toBe(route.context);
      72 |     expect(typeof meta.error).toBe('string');
    > 73 |     expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346B_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
         |                                                                                                                        ^
      74 |   });
      75 |
      76 |   it.each(ROUTES)('control KS-1346 B2 $label: the 500 body stays the constant text for an object throw', async (route) => {

      at src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts:73:120

Test Suites: 1 failed, 1 total
Tests:       4 failed, 7 passed, 11 total
Snapshots:   0 total
Time:        2.861 s
Ran all test suites matching /src\/__tests__\/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/g-GREEN.out TEXT_SHA256 791a0e4188cbe606c780c07d417985df0b5223d2a26679f7d8483375de94651e

PASS src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts
  KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log
    ✓ RED KS-1346 B1 GET /dsr/pending: a thrown plain object is logged with its content, once, under this route (13 ms)
    ✓ RED KS-1346 B1 GET /retention: a thrown plain object is logged with its content, once, under this route (2 ms)
    ✓ RED KS-1346 B1 GET /deletion-log: a thrown plain object is logged with its content, once, under this route (1 ms)
    ✓ RED KS-1346 B1 GET /consent/check: a thrown plain object is logged with its content, once, under this route (1 ms)
    ✓ control KS-1346 B2 GET /dsr/pending: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 B2 GET /retention: the 500 body stays the constant text for an object throw
    ✓ control KS-1346 B2 GET /deletion-log: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 B2 GET /consent/check: the 500 body stays the constant text for an object throw (1 ms)
    ✓ control KS-1346 B3: an Error throw still logs exactly its message
    ✓ control KS-1346 B4: a string throw still logs exactly itself, not a quoted rendering (1 ms)
    ✓ control KS-1346 B5: String() of the thrown object really is the lossy text, so B1 is not vacuous

Test Suites: 1 passed, 1 total
Tests:       11 passed, 11 total
Snapshots:   0 total
Time:        2.059 s, estimated 3 s
Ran all test suites matching /src\/__tests__\/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/g-lint-HEAD.out TEXT_SHA256 dc8d11d8ce7fcc84864bc1698e2c04c3fe4a2bde003eca9246dffed0550b3568


> @secuura/originate@0.1.0 lint
> eslint src


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts
  145:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  326:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  549:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts
  19:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts
  36:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks566-g1-split.test.ts
  32:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts
  45:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unused-vars')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks587-anchors-honest-simulated.test.ts
  16:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts
   87:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
   89:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  102:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts
  38:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/rightsHolders.tenant-scope.integration.test.ts
  122:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  124:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  126:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  128:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
  62:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
  143:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
  2089:13  warning  'copied' is never reassigned. Use 'const' instead  prefer-const
  2129:20  warning  'e' is defined but never used                      @typescript-eslint/no-unused-vars

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/routes/anchors.ts
  53:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
  128:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

✖ 22 problems (0 errors, 22 warnings)
  0 errors and 14 warnings potentially fixable with the `--fix` option.



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-32nd/raise/g-lint-CTL.out TEXT_SHA256 2caac2eb059e0e90ecd55468b5d3d2789ecaf8585f09cfdfe48089f5c47f7fdc


> @secuura/originate@0.1.0 lint
> eslint src


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts
  145:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  326:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  549:7  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts
  97:1  error  Unexpected 'debugger' statement  no-debugger

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts
  19:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts
  36:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks566-g1-split.test.ts
  32:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts
  45:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unused-vars')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks587-anchors-honest-simulated.test.ts
  16:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts
   87:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
   89:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  102:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts
  38:1  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/__tests__/rightsHolders.tenant-scope.integration.test.ts
  122:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  124:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  126:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')
  128:5  warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-var-requires')

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
  62:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
  143:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
  2089:13  warning  'copied' is never reassigned. Use 'const' instead  prefer-const
  2129:20  warning  'e' is defined but never used                      @typescript-eslint/no-unused-vars

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/routes/anchors.ts
  53:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
  128:5  warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error

✖ 23 problems (1 error, 22 warnings)
  0 errors and 14 warnings potentially fixable with the `--fix` option.

npm error Lifecycle script `lint` failed with error:
npm error code 1
npm error path /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate
npm error workspace @secuura/originate@0.1.0
npm error location /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b32-ks1346b/Blockchain/Dev/services/originate
npm error command failed
npm error command sh -c eslint src


