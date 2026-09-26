# KS-1346-B GDPRFAIL500LOG — gdpr.ts's fail500 logs a NON-Error throw with its content (util.inspect), not as [object Object]

File: `Blockchain/Dev/services/originate/src/routes/gdpr.ts`  (product, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts`  (NEW)
Tip: `3f70224a069b944334480478ad5d16a5ed33eeae`
Runner: `jest` (ts-jest; `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)

Written 2026-09-26 21:50:26 AEST (shell `date`) by a Spark brief-writer sub-agent for Wednesday, from develop `3f70224a069b`, read in a `--no-local` scratch clone. `gdpr.ts` read at `:1-:30` and `:186-:214` and grepped whole (632 lines, blob `008719a71b6b`, last changed `4751c1bd2 KS-730 #1283, 2026-09-26`). **RUNG 3: every `-`, `+` and context line and every header is given byte for byte. Brief B of 2 for KS-1346 (A = `routes/systemErrors.ts`, B = `routes/gdpr.ts`); the two touch DIFFERENT files and are independent — either may run first.**

## The mode — read this twice

CODE+TEST, TWO files. File 1 is the product `Blockchain/Dev/services/originate/src/routes/gdpr.ts`, MODIFIED IN PLACE (`--- a/…` / `+++ b/…` with that exact path), EXACTLY the 2 hunks in `## The exact change`. File 2 is a NEW jest file (`--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts`), ONE hunk `@@ -0,0 +1,95 @@`. There is no third file. You never touch `routes/webhooks.ts`, `routes/adminConfig.ts` (both in flight on other briefs), the other KS-1346 file (A (`routes/systemErrors.ts`)), `utils/logger.ts`, any existing test, nor the reference test `ks730b-gdpr-500-never-answers-err-message.test.ts`.

## What is wrong (one paragraph)

`fail500(res, context, err)` at `:210-:212` (KS-730) logs the caught value as `err instanceof Error ? err.message : String(err)`. For a thrown PLAIN OBJECT, `String(err)` is the literal text `[object Object]`, so the object's content — the only place the detail can live now that the 500 body is constant — is LOST from the log (KS-1346, measured at runtime by gate29 on the #1290 routes). An Error must keep logging its message and a thrown string must keep logging itself exactly (both correct today). The fix, one of the two the ticket names: for a value that is neither an Error nor a string, log `inspect(err)` from Node's built-in `util` module, which renders an object's fields (and survives circular values, where `JSON.stringify` would throw). The helper is called 15 times in this file; changing the helper fixes every one of them. Inline sites: none (every 500 in this router goes through the helper).

## The exact change

Edit 1 — a pure INSERTION of ONE import line between `:15` and `:16` (both non-blank; one leading and one trailing context line — a trailing-only insertion is refused by macOS `patch -F0`, and a leading-only one by the builder).

```diff
@@ -15,2 +15,3 @@
 import { z } from 'zod';
+import { inspect } from 'util';
 import * as gdpr from '../services/gdprService';
```

Edit 2 — line `:211`, ONE line out, ONE line in (indent: 2 spaces, as the file has it). Edit 1 added one line above, so the NEW side starts one later.

```diff
@@ -210,3 +211,3 @@
 function fail500(res: Response, context: string, err: unknown): void {
-  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : inspect(err) });
   res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
```

**Do NOT touch:** the helper's signature `:210` and its 500 line `:212`, its KS-730 docblock, every `fail500(res, …)` call, every other import (`Response` and `logger` are already imported; add ONLY the `inspect` import), and every other line. Use `'util'` (the file imports no `node:`-prefixed module). The nested ternary is deliberate: a thrown string must NOT go through `inspect` (it would be logged quoted — control B4 pins that).

## The test

File: `Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts`

The shape copied is the merged KS-730 part B cell file `ks730b-gdpr-500-never-answers-err-message.test.ts` (the input's reference test): the same `jest.mock` of the service, auth and logger modules, the router mounted at `/api/gdpr` on a loopback listener (`127.0.0.1:0`), driven with `fetch`. It drives four GDPR routes that reach their service with nothing to satisfy first (GET /dsr/pending, GET /retention, GET /deletion-log, GET /consent/check), each by making its OWN gdprService call reject, and reads the WHOLE logger call list for that one request.

NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts`, ONE hunk `@@ -0,0 +1,95 @@` (95 `+` lines; a blank line is a lone `+`). Copy every line byte for byte.

```
+// KS-1346 part B (originate routes/gdpr.ts): fail500 logged a NON-Error throw through String(), so a
+// thrown plain object reached the log as [object Object] and its content was lost. The 500 BODY was
+// already constant (KS-730); what this file pins is the LOG. Four GDPR routes that reach their service
+// with nothing to satisfy first are driven by making ITS OWN service call reject, on a real loopback
+// listener, exactly as the KS-730 part B cells do. Error and string throws must log exactly what they
+// logged before.
+const mockGetPendingDSRs = jest.fn();
+const mockGetRetentionPolicies = jest.fn();
+const mockGetDeletionLog = jest.fn();
+const mockHasValidConsent = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../services/gdprService', () => ({
+  getPendingDSRs: mockGetPendingDSRs,
+  getRetentionPolicies: mockGetRetentionPolicies,
+  getDeletionLog: mockGetDeletionLog,
+  hasValidConsent: mockHasValidConsent,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  hasAnyRole: () => true,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { gdprRouter } from '../routes/gdpr';
+
+const DETAIL = 'ks1346b-private-detail';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ROUTES = [
+  { label: 'GET /dsr/pending', path: '/dsr/pending', mock: mockGetPendingDSRs, context: 'GDPR pending DSR list failed (GET /api/gdpr/dsr/pending)' },
+  { label: 'GET /retention', path: '/retention', mock: mockGetRetentionPolicies, context: 'GDPR retention policy read failed (GET /api/gdpr/retention)' },
+  { label: 'GET /deletion-log', path: '/deletion-log', mock: mockGetDeletionLog, context: 'GDPR deletion log read failed (GET /api/gdpr/deletion-log)' },
+  { label: 'GET /consent/check', path: '/consent/check?userId=u-ks1346b&purpose=MARKETING', mock: mockHasValidConsent, context: 'GDPR consent check failed (GET /api/gdpr/consent/check)' },
+] as const;
+
+const app = express();
+app.use('/api/gdpr', express.json(), gdprRouter);
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
+  const res = await fetch(baseUrl + '/api/gdpr' + route.path, { method: 'GET' });
+  return { status: res.status, text: await res.text(), calls: mockLoggerError.mock.calls };
+}
+
+describe('KS-1346 part B: gdpr fail500 keeps a non-Error throw readable in the log', () => {
+  it.each(ROUTES)('RED KS-1346 B1 $label: a thrown plain object is logged with its content, once, under this route', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346B_OBJECT', detail: DETAIL });
+    expect(reply.status).toBe(500);
+    expect(reply.calls.length).toBe(1);
+    const [context, meta] = reply.calls[0] as [string, { error: unknown }];
+    expect(context).toBe(route.context);
+    expect(typeof meta.error).toBe('string');
+    expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346B_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
+  });
+
+  it.each(ROUTES)('control KS-1346 B2 $label: the 500 body stays the constant text for an object throw', async (route) => {
+    const reply = await callWithThrow(route, { code: 'KS1346B_OBJECT', detail: DETAIL });
+    expect({ status: reply.status, leaked: reply.text.includes(DETAIL) }).toEqual({ status: 500, leaked: false });
+    expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+  });
+
+  it('control KS-1346 B3: an Error throw still logs exactly its message', async () => {
+    const reply = await callWithThrow(ROUTES[0], new Error(DETAIL));
+    expect(reply.calls).toEqual([[ROUTES[0].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 B4: a string throw still logs exactly itself, not a quoted rendering', async () => {
+    const reply = await callWithThrow(ROUTES[1], DETAIL);
+    expect(reply.calls).toEqual([[ROUTES[1].context, { error: DETAIL }]]);
+  });
+
+  it('control KS-1346 B5: String() of the thrown object really is the lossy text, so B1 is not vacuous', () => {
+    expect(String({ code: 'KS1346B_OBJECT', detail: DETAIL })).toBe('[object Object]');
+  });
+});
```

**Every test `+` line is ASCII only and carries NO backslash, NO backtick and NO double-quote** (counted: 0 of each); the two `$label` are jest's `it.each` row interpolation and are intended. Do not rename a cell.

## Red cells

- RED KS-1346 B1

(Title SUBSTRING. At the tip with ONLY the test file these FOUR `it.each` rows fail by assertion — the logged `error` is `[object Object]`, which carries neither the detail nor the code — and all seven controls stay green. With the product hunks all 11 are green.)

## Cells and controls

- `RED KS-1346 B1 $label: a thrown plain object is logged with its content, once, under this route` — 4 rows; ONE logger call, context equal to that route's own, `error` a string containing BOTH the object's `detail` and its `code`.
- `control KS-1346 B2 $label: the 500 body stays the constant text for an object throw` — 4 rows; green before and after (KS-730's constant body; the object's detail never reaches the client).
- `control KS-1346 B3: an Error throw still logs exactly its message` — whole call list equality; green before and after.
- `control KS-1346 B4: a string throw still logs exactly itself, not a quoted rendering` — whole call list equality; green before and after. It is what fails a fix that sends EVERY non-Error through `inspect` (measured, arm below).
- `control KS-1346 B5: String() of the thrown object really is the lossy text, so B1 is not vacuous`.

## The failing case (the "tamper")

On the FIXED tree, `:212` (the fixed helper line, literal count 1) → the same line with `inspect(err)` replaced by `inspect(String(err))` (the import stays used, so ts-jest still compiles the suite — a plain revert to `String(err)` leaves `inspect` unused and the SUITE fails to compile instead of a cell failing, measured). **Measured:** exactly the four `RED KS-1346 B1` rows red, all 7 controls green.

**Arm (the over-broad fix):** `: inspect(err)` for EVERY non-Error (no string branch). **Measured:** all four B1 rows green and `control KS-1346 B4` RED (the string is logged quoted). A green B4 under that arm would be a FAIL of this brief.

## Premises (each one measured, with where)

- Every quoted line was read with `git show 3f70224a069b:<path>`; the `-` line occurs exactly once in the file; `import { z } from 'zod';` once; `util`/`inspect` occur 0 times at the tip; non-ASCII is at :29-:52, …, :207 (3 lines above the helper), … — none on a hunk line.
- **Golden applies strictly:** `git apply --check` rc 0 and `patch -p1 -F0 --dry-run` rc 0 at `3f70224a`.
- **RED at tip, EXECUTED** (jest/ts-jest in the scratch clone, node_modules symlink-farmed from the Secuura checkout): test file only → `Tests: 4 failed, 7 passed, 11 total` = exactly the four declared rows, by assertion (`Expected - 2 / Received + 2` on the hasDetail/hasCode object).
- **GREEN after, EXECUTED:** golden applied (`git apply` strict rc 0; applied test `cmp`-equal to the golden) → new test + `ks730b` together green (`23 passed`); whole originate suite tip `82 suites / 962 tests passed` (measured at this same tip by the KS-1334-A round, 21:2x) → fixed `83 suites / 973 tests passed`, 0 failures.
- **Lint, EXECUTED:** `npm run lint` (`eslint src`) rc 0 (0 errors; the 22 warnings are all pre-existing, none on either file); `eslint --max-warnings 0` on the product and the new test rc 0; `tsc --noEmit -p tsconfig.json` rc 0.
- Tamper and Arm: EXECUTED as stated above.

## UNMEASURED — stated rather than glossed

1. `spark_checker.sh` was NOT run on the golden (no pre-probe).
2. node_modules come from the real checkout, not an install at `3f70224a`.
3. Real winston output was not inspected: the logger is mocked, so the cell pins the META the helper hands to `logger.error`, not the formatted line.
4. The builder was run against the scratch clone (`NIGHT_SOURCE_CHECKOUT`), whose `source_checkout` field therefore names a scratchpad path.

## Collision

KS-1346 is **Backlog**, Low, unassigned, no attachment, **0 rows in night/done.md** (counted), no brief dir before this round. Open PRs (24, GitHub API): none touches `routes/gdpr.ts` or a KS-1346 test. `git ls-remote`: `feature/ks-730-gdpr-prod-message-b29-8` is the pre-squash head of merged #1283. The ticket's other two helper files (`routes/webhooks.ts`, `routes/adminConfig.ts`) are IN FLIGHT on other briefs tonight and are deliberately NOT in this split.

## Scope

**Closes 1 of the 4 helper files; refs KS-1346, does NOT close it.** Brief A is the second file; `webhooks.ts` and `adminConfig.ts` follow once their in-flight work merges. The ticket's rotate-secret cell (Done-when 3) is `webhooks.ts`-only and is not here.

## Output

Exactly ONE fenced diff block with TWO files: first the product (2 hunks, headers `@@ -15,2 +15,3 @@` and `@@ -210,3 +211,3 @@`), then the NEW test (`--- /dev/null`, one hunk `@@ -0,0 +1,95 @@`). Paths exactly as the File: / Test file: lines give them, `a/` and `b/` prefixed. Every `+` line on its own physical line. Every context line keeps its single leading space. No prose outside the block.
