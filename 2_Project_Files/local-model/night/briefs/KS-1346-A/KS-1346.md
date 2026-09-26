# KS-1346-A SYSERRFAIL500LOG — systemErrors.ts's fail500 logs a NON-Error throw with its content (util.inspect), not as [object Object]

File: `Blockchain/Dev/services/originate/src/routes/systemErrors.ts`  (product, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts`  (NEW)
Tip: `3f70224a069b944334480478ad5d16a5ed33eeae`
Runner: `jest` (ts-jest; `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)

Written 2026-09-26 21:50:26 AEST (shell `date`) by a Spark brief-writer sub-agent for Wednesday, from develop `3f70224a069b`, read in a `--no-local` scratch clone. `systemErrors.ts` read at `:1-:30` and `:186-:214` and grepped whole (214 lines, blob `829d7c8c1bd5`, last changed `970c3f241 KS-730 #1282, 2026-09-26`). **RUNG 3: every `-`, `+` and context line and every header is given byte for byte. Brief A of 2 for KS-1346 (A = `routes/systemErrors.ts`, B = `routes/gdpr.ts`); the two touch DIFFERENT files and are independent — either may run first.**

## The mode — read this twice

CODE+TEST, TWO files. File 1 is the product `Blockchain/Dev/services/originate/src/routes/systemErrors.ts`, MODIFIED IN PLACE (`--- a/…` / `+++ b/…` with that exact path), EXACTLY the 2 hunks in `## The exact change`. File 2 is a NEW jest file (`--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts`), ONE hunk `@@ -0,0 +1,97 @@`. There is no third file. You never touch `routes/webhooks.ts`, `routes/adminConfig.ts` (both in flight on other briefs), the other KS-1346 file (B (`routes/gdpr.ts`)), `utils/logger.ts`, any existing test, nor the reference test `ks730a-ingest-500-never-answers-err-message.test.ts`.

## What is wrong (one paragraph)

`fail500(res, context, err)` at `:93-:95` (KS-730) logs the caught value as `err instanceof Error ? err.message : String(err)`. For a thrown PLAIN OBJECT, `String(err)` is the literal text `[object Object]`, so the object's content — the only place the detail can live now that the 500 body is constant — is LOST from the log (KS-1346, measured at runtime by gate29 on the #1290 routes). An Error must keep logging its message and a thrown string must keep logging itself exactly (both correct today). The fix, one of the two the ticket names: for a value that is neither an Error nor a string, log `inspect(err)` from Node's built-in `util` module, which renders an object's fields (and survives circular values, where `JSON.stringify` would throw). The helper is called 4 times in this file; changing the helper fixes every one of them. Inline sites: :121 and :152 (the two ingest handlers log inline with the same `String(err)`; they are NOT the helper and are out of this brief).

## The exact change

Edit 1 — a pure INSERTION of ONE import line between `:14` and `:15` (both non-blank; one leading and one trailing context line — a trailing-only insertion is refused by macOS `patch -F0`, and a leading-only one by the builder).

```diff
@@ -14,2 +14,3 @@
 import { z } from 'zod';
+import { inspect } from 'util';
 import * as errorTracking from '../services/errorTrackingService';
```

Edit 2 — line `:94`, ONE line out, ONE line in (indent: 4 spaces, as the file has it). Edit 1 added one line above, so the NEW side starts one later.

```diff
@@ -93,3 +94,3 @@
 function fail500(res: Response, context: string, err: unknown): void {
-    logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+    logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : inspect(err) });
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
```

**Do NOT touch:** the helper's signature `:93` and its 500 line `:95`, its KS-730 docblock, every `fail500(res, …)` call, every other import (`Response` and `logger` are already imported; add ONLY the `inspect` import), and every other line. Use `'util'` (the file imports no `node:`-prefixed module). The nested ternary is deliberate: a thrown string must NOT go through `inspect` (it would be logged quoted — control A4 pins that).

## The test

File: `Blockchain/Dev/services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts`

The shape copied is the merged KS-730 part A cell file `ks730a-ingest-500-never-answers-err-message.test.ts` (the input's reference test): the same `jest.mock` of the service, auth and logger modules, the router mounted at `/api/system-errors` on a loopback listener (`127.0.0.1:0`), driven with `fetch`. It drives the four admin routes (GET /stats, GET /, PATCH /:errorId/resolve, POST /resolve-by-service), each by making its OWN errorTrackingService call reject, and reads the WHOLE logger call list for that one request.

NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts`, ONE hunk `@@ -0,0 +1,97 @@` (97 `+` lines; a blank line is a lone `+`). Copy every line byte for byte.

```
+// KS-1346 part A (originate routes/systemErrors.ts): fail500 logged a NON-Error throw through String(),
+// so a thrown plain object reached the log as [object Object] and its content was lost. The 500 BODY was
+// already constant (KS-730); what this file pins is the LOG. The four admin routes go through fail500, so
+// each is driven by making ITS OWN service call reject, on a real loopback listener, exactly as the KS-730
+// part A cells do. Error and string throws must log exactly what they logged before.
+const mockLoggerError = jest.fn();
+const mockGetErrorStats = jest.fn();
+const mockGetRecentErrors = jest.fn();
+const mockResolveError = jest.fn();
+const mockResolveErrorsByService = jest.fn();
+
+jest.mock('../services/errorTrackingService', () => ({
+  trackError: jest.fn(),
+  resolveErrorsByService: mockResolveErrorsByService,
+  getErrorStats: mockGetErrorStats,
+  getRecentErrors: mockGetRecentErrors,
+  resolveError: mockResolveError,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { systemErrorsRouter } from '../routes/systemErrors';
+
+const DETAIL = 'ks1346-private-detail';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ROUTES = [
+  { label: 'GET /stats', method: 'GET', path: '/stats', mock: mockGetErrorStats, context: 'Error statistics read failed (GET /api/system-errors/stats)' },
+  { label: 'GET /', method: 'GET', path: '/', mock: mockGetRecentErrors, context: 'Error list read failed (GET /api/system-errors)' },
+  { label: 'PATCH /:errorId/resolve', method: 'PATCH', path: '/err-ks1346/resolve', mock: mockResolveError, context: 'Error resolve failed (PATCH /api/system-errors/:errorId/resolve)' },
+  { label: 'POST /resolve-by-service', method: 'POST', path: '/resolve-by-service', mock: mockResolveErrorsByService, context: 'Bulk error resolve failed (POST /api/system-errors/resolve-by-service)' },
+] as const;
+
+const app = express();
+app.use('/api/system-errors', express.json(), systemErrorsRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => server?.close());
+beforeEach(() => jest.clearAllMocks());
+
+async function callWithThrow(route: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number; text: string; calls: unknown[][] }> {
+  mockLoggerError.mockClear();
+  route.mock.mockRejectedValueOnce(thrown);
+  const res = await fetch(baseUrl + '/api/system-errors' + route.path, {
+    method: route.method,
+    headers: { 'content-type': 'application/json' },
+    ...(route.method === 'GET' ? {} : { body: JSON.stringify({ service: 'ks1346-svc' }) }),
+  });
+  return { status: res.status, text: await res.text(), calls: mockLoggerError.mock.calls };
+}
+
+describe('KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log', () => {
+  it.each(ROUTES)('RED KS-1346 A1 $label: a thrown plain object is logged with its content, once, under this route', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346_OBJECT', detail: DETAIL });
+    expect(reply.status).toBe(500);
+    expect(reply.calls.length).toBe(1);
+    const [context, meta] = reply.calls[0] as [string, { error: unknown }];
+    expect(context).toBe(route.context);
+    expect(typeof meta.error).toBe('string');
+    expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
+  });
+
+  it.each(ROUTES)('control KS-1346 A2 $label: the 500 body stays the constant text for an object throw', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346_OBJECT', detail: DETAIL });
+    expect({ status: reply.status, leaked: reply.text.includes(DETAIL) }).toEqual({ status: 500, leaked: false });
+    expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+  });
+
+  it('control KS-1346 A3: an Error throw still logs exactly its message', async () => {
+    const reply = await callWithThrow(ROUTES[0], new Error(DETAIL));
+    expect(reply.calls).toEqual([[ROUTES[0].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 A4: a string throw still logs exactly itself, not a quoted rendering', async () => {
+    const reply = await callWithThrow(ROUTES[1], DETAIL);
+    expect(reply.calls).toEqual([[ROUTES[1].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 A5: String() of the thrown object really is the lossy text, so A1 is not vacuous', () => {
+    expect(String({ code: 'KS1346_OBJECT', detail: DETAIL })).toBe('[object Object]');
+  });
+});
```

**Every test `+` line is ASCII only and carries NO backslash, NO backtick and NO double-quote** (counted: 0 of each); the two `$label` are jest's `it.each` row interpolation and are intended. Do not rename a cell.

## Red cells

- RED KS-1346 A1

(Title SUBSTRING. At the tip with ONLY the test file these FOUR `it.each` rows fail by assertion — the logged `error` is `[object Object]`, which carries neither the detail nor the code — and all seven controls stay green. With the product hunks all 11 are green.)

## Cells and controls

- `RED KS-1346 A1 $label: a thrown plain object is logged with its content, once, under this route` — 4 rows; ONE logger call, context equal to that route's own, `error` a string containing BOTH the object's `detail` and its `code`.
- `control KS-1346 A2 $label: the 500 body stays the constant text for an object throw` — 4 rows; green before and after (KS-730's constant body; the object's detail never reaches the client).
- `control KS-1346 A3: an Error throw still logs exactly its message` — whole call list equality; green before and after.
- `control KS-1346 A4: a string throw still logs exactly itself, not a quoted rendering` — whole call list equality; green before and after. It is what fails a fix that sends EVERY non-Error through `inspect` (measured, arm below).
- `control KS-1346 A5: String() of the thrown object really is the lossy text, so A1 is not vacuous`.

## The failing case (the "tamper")

On the FIXED tree, `:95` (the fixed helper line, literal count 1) → the same line with `inspect(err)` replaced by `inspect(String(err))` (the import stays used, so ts-jest still compiles the suite — a plain revert to `String(err)` leaves `inspect` unused and the SUITE fails to compile instead of a cell failing, measured). **Measured:** exactly the four `RED KS-1346 A1` rows red, all 7 controls green.

**Arm (the over-broad fix):** `: inspect(err)` for EVERY non-Error (no string branch). **Measured:** all four A1 rows green and `control KS-1346 A4` RED (the string is logged quoted). A green A4 under that arm would be a FAIL of this brief.

## Premises (each one measured, with where)

- Every quoted line was read with `git show 3f70224a069b:<path>`; the `-` line occurs exactly once in the file; `import { z } from 'zod';` once; `util`/`inspect` occur 0 times at the tip; non-ASCII is at :22,:36,:41,:47,:78,:79,:87,… — none on a hunk line.
- **Golden applies strictly:** `git apply --check` rc 0 and `patch -p1 -F0 --dry-run` rc 0 at `3f70224a`.
- **RED at tip, EXECUTED** (jest/ts-jest in the scratch clone, node_modules symlink-farmed from the Secuura checkout): test file only → `Tests: 4 failed, 7 passed, 11 total` = exactly the four declared rows, by assertion (`Expected - 2 / Received + 2` on the hasDetail/hasCode object).
- **GREEN after, EXECUTED:** golden applied (`git apply` strict rc 0; applied test `cmp`-equal to the golden) → new test + `ks730a` together green (`28 passed`); whole originate suite tip `82 suites / 962 tests passed` (measured at this same tip by the KS-1334-A round, 21:2x) → fixed `83 suites / 973 tests passed`, 0 failures.
- **Lint, EXECUTED:** `npm run lint` (`eslint src`) rc 0 (0 errors; the 22 warnings are all pre-existing, none on either file); `eslint --max-warnings 0` on the product and the new test rc 0; `tsc --noEmit -p tsconfig.json` rc 0.
- Tamper and Arm: EXECUTED as stated above.

## UNMEASURED — stated rather than glossed

1. `spark_checker.sh` was NOT run on the golden (no pre-probe).
2. node_modules come from the real checkout, not an install at `3f70224a`.
3. Real winston output was not inspected: the logger is mocked, so the cell pins the META the helper hands to `logger.error`, not the formatted line.
4. The builder was run against the scratch clone (`NIGHT_SOURCE_CHECKOUT`), whose `source_checkout` field therefore names a scratchpad path.

## Collision

KS-1346 is **Backlog**, Low, unassigned, no attachment, **0 rows in night/done.md** (counted), no brief dir before this round. Open PRs (24, GitHub API): none touches `routes/systemErrors.ts` or a KS-1346 test. `git ls-remote`: `feature/ks-730-systemerrors-prod-message-b29-7` is the pre-squash head of merged #1282. The ticket's other two helper files (`routes/webhooks.ts`, `routes/adminConfig.ts`) are IN FLIGHT on other briefs tonight and are deliberately NOT in this split.

## Scope

**Closes 1 of the 4 helper files; refs KS-1346, does NOT close it.** Brief B is the second file; `webhooks.ts` and `adminConfig.ts` follow once their in-flight work merges. The ticket's rotate-secret cell (Done-when 3) is `webhooks.ts`-only and is not here.

## Output

Exactly ONE fenced diff block with TWO files: first the product (2 hunks, headers `@@ -14,2 +14,3 @@` and `@@ -93,3 +94,3 @@`), then the NEW test (`--- /dev/null`, one hunk `@@ -0,0 +1,97 @@`). Paths exactly as the File: / Test file: lines give them, `a/` and `b/` prefixed. Every `+` line on its own physical line. Every context line keeps its single leading space. No prose outside the block.
