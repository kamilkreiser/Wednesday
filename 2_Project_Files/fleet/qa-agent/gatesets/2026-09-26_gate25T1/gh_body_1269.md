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
