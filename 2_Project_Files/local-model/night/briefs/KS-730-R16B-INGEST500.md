# KS-730 R16B-INGEST500 - Wednesday's task for Ornith, PART A of the KS-730 remainder (originate `routes/systemErrors.ts`, the two UNAUTHENTICATED ingest catches): a thrown error is logged server-side and the 500 body is the constant text in every NODE_ENV; plus a NEW jest suite (code_patch, JEST; re-brief of the STALE READY_KS-730-A at develop 8c2f7b3fd, written 12:41:30 AEST on 2026-09-22 by Wednesday's feed11 drafter from the file at the tip - `systemErrors.ts` :13-:20, :70-:100, :118-:130 read whole; 187 lines; the reference test `ks444-system-errors-body-guard.test.ts` (imports `routes/systemErrors`) present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `jest`

## Premises (measured by the feed11 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-730-A_ornith35b-q4_CODEPATCH-PASS-7of7_2026-09-17.diff.md` (Ornith PASS 7/7 first sample at 05:52 on 09-17, apply mode LENIENT `--recount` because its hunk headers were miscounted - this brief prints the exact headers). Part B (the admin catches) is a separate brief; KS-730 stays open after this PR ("Refs KS-730 (part A)").
- The product at the tip is UNCHANGED since the old READY (offset 0): `:14` `import { z } from 'zod';`, `:15` `import * as errorTracking from '../services/errorTrackingService';`, `:16` `import { authenticate, requireRole } from '../middleware/auth';`, `:17` blank, `:93` / `:123` `    res.status(201).json({ success: true });`, `:94` / `:124` `  } catch (err: any) {`, `:95` / `:125` the inline 500 line, `:96` / `:126` `  }`, `:97` / `:127` `});` - all byte-exact at 8c2f7b3fd. `utils/logger` is NOT imported at the tip (`grep utils/logger` = 0 hits).
- The inline 500 line at `:95` is byte-identical to FIVE other lines of the file (`:125`, `:136`, `:158`, `:168`, `:184` - measured: 6 identical lines). Only `:95` and `:125` are this task (the two unauthenticated ingest routes); the four ADMIN catches are Part B and must NOT change. The `## Where` below is LINE-KEYED so the checker grades the two `-` lines by their line NUMBERS.
- The old READY's test file is ABSENT at the tip (no `ks730*` under `services/originate/src/__tests__/`). `systemErrors.ts` is in Seat B's lane (originate) but NO round-18 PR and NO held R15/R16 READY touches it (seat_grep 0 / held_pool 0 on `systemErrors.ts`, re-measured this feed). Ticket KS-730: Backlog, not archived, no PR attached (board read at drafting time).
- The old READY's import hunk inserted after `:16` with the BLANK `:17` as trailing context (the fence-shape gate refuses blank context); this brief inserts the import between `:15` and `:16` instead, so the trailing context is the `middleware/auth` import. Import order is not semantic here. Same behaviour, different bytes.
- The test is REWRITTEN so every `+` line is ASCII, backslash-free, double-quote-free AND `$`-free: the two template literals (`baseUrl`, the fetch url) are string concatenation, the red/green glyphs are ASCII `RED KS-730 A1..A4` / `control:` titles, the reds declared under `## Red cells`. Same six cells, same meaning as the old READY.

## What is wrong (one paragraph)
`POST /api/system-errors/ingest` (`Blockchain/Dev/services/originate/src/routes/systemErrors.ts:70`-`:97`) and `POST /api/system-errors/client-errors` (`:100`-`:127`) are unauthenticated ingest routes whose catch blocks answer `res.status(500).json({ ..., message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message })` (`:95`, `:125`): off production the raw `err.message` (a Postgres relation name, a stack detail) goes to an anonymous caller, and on production it is dropped without a log - the KS-727 doctrine says a 500 answers constant text in EVERY environment and logs the detail server-side. Fix: import `logger` from `../utils/logger` (not imported today), and in each of the two catches log `err.message` (or `String(err)`) with a route-specific message, then answer the constant body. NOT in this task: the four admin catches (`:136`, `:158`, `:168`, `:184` - identical text, Part B), the 400 validation answers (`:76` keeps `'service and message are required'`), `errorTrackingService`, the middleware.

## The exact change - THREE edits in `Blockchain/Dev/services/originate/src/routes/systemErrors.ts`, each its own hunk (headers `@@ -14,3 +14,5 @@`, `@@ -93,5 +93,6 @@`, `@@ -123,5 +123,6 @@`); no blank context line anywhere
E1 - the import, INSERTED between `:15` and `:16` (0 `-`, 2 `+`; leading context `:14`-`:15`, trailing context `:16`):
```
@@ -14,3 +14,5 @@
 import { z } from 'zod';
 import * as errorTracking from '../services/errorTrackingService';
+// KS-730: an inline 500 logs err.message server-side and answers the constant text, in every NODE_ENV.
+import { logger } from '../utils/logger';
 import { authenticate, requireRole } from '../middleware/auth';
```
E2 - line 95 (the `/ingest` catch) replaced by a log line + the constant answer (1 `-`, 2 `+`; leading context `:93`-`:94`, trailing `:96`-`:97`):
```
@@ -93,5 +93,6 @@
     res.status(201).json({ success: true });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('System error ingest failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
```
E3 - line 125 (the `/client-errors` catch), the same shape with its own log message (1 `-`, 2 `+`; leading context `:123`-`:124`, trailing `:126`-`:127`):
```
@@ -123,5 +123,6 @@
     res.status(201).json({ success: true });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('Client error ingest failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
```
Do not touch any other line: the four admin catches at `:136`, `:158`, `:168`, `:184` carry the SAME text as `:95` / `:125` and stay exactly as they are (Part B). The two log messages differ (`'System error ingest failed'` vs `'Client error ingest failed'`) - the cells pin each. `:20` and `:130` carry em-dashes and are not context lines of any hunk. Old sides 3 / 5 / 5 lines; new sides 5 / 6 / 6.

## THIS IS JEST, NOT VITEST
`repo.test_runner` begins with `jest` (ts-jest). `describe/it/expect/beforeAll/afterAll/beforeEach/afterEach` are globals; `jest.fn` / `jest.mock` (auto-hoisted); NO `vi.*`, NO `import ... from 'vitest'`. The suite mounts the router on a real loopback listener (`app.listen(0, '127.0.0.1')`) and drives it with the global `fetch` (node 18+), exactly as the old READY did.

## The test - one NEW jest file
File: `Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 113), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, no `$`, ASCII only.
```
+// KS-730 part A (originate routes/systemErrors.ts, POST /ingest and POST /client-errors): a thrown error must
+// never reach the 500 body in ANY NODE_ENV (the KS-727 doctrine), and its message must be logged server-side
+// instead of being lost. The two routes are unauthenticated ingest paths; the router is mounted on a real
+// loopback listener and driven with fetch (no auth stub needed - the mocked middleware is a pass-through).
+const mockTrackError = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../services/errorTrackingService', () => ({
+  trackError: mockTrackError,
+  resolveErrorsByService: jest.fn(),
+  getErrorStats: jest.fn(),
+  getRecentErrors: jest.fn(),
+  resolveError: jest.fn(),
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
+const LEAK = 'relation system_errors does not exist ks730-private-detail';
+const NODE_ENVS = ['development', 'demo', 'test', undefined];
+const INGEST_BODY = { service: 'ks730-svc', message: 'ks730 reported error' };
+const CLIENT_BODY = { error: 'ks730 render error', source: 'ks730-frontend' };
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
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
+afterEach(() => setNodeEnv(ORIGINAL_NODE_ENV));
+
+function setNodeEnv(value: string | undefined): void {
+  if (value === undefined) delete process.env.NODE_ENV;
+  else process.env.NODE_ENV = value;
+}
+
+async function post(path: string, body: object, nodeEnv: string | undefined, throwInService: boolean): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  if (throwInService) mockTrackError.mockRejectedValueOnce(new Error(LEAK));
+  const res = await fetch(baseUrl + '/api/system-errors' + path, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-730 part A: the system-errors ingest routes never answer a 500 with err.message', () => {
+  it('RED KS-730 A1: POST /ingest: the thrown message is not in the 500 body under development, demo, test or unset', async () => {
+    for (const nodeEnv of NODE_ENVS) {
+      const reply = await post('/ingest', INGEST_BODY, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+    }
+  });
+
+  it('RED KS-730 A2: POST /client-errors: the thrown message is not in the 500 body under development, demo, test or unset', async () => {
+    for (const nodeEnv of NODE_ENVS) {
+      const reply = await post('/client-errors', CLIENT_BODY, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+    }
+  });
+
+  it('RED KS-730 A3: POST /ingest: the thrown message is logged once, server-side', async () => {
+    const reply = await post('/ingest', INGEST_BODY, 'development', true);
+    expect(reply.status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([['System error ingest failed', { error: LEAK }]]);
+  });
+
+  it('RED KS-730 A4: POST /client-errors: the thrown message is logged once, server-side', async () => {
+    const reply = await post('/client-errors', CLIENT_BODY, 'development', true);
+    expect(reply.status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([['Client error ingest failed', { error: LEAK }]]);
+  });
+
+  it('control: under production both routes already answer the constant text, and the service was reached', async () => {
+    const ingest = await post('/ingest', INGEST_BODY, 'production', true);
+    const client = await post('/client-errors', CLIENT_BODY, 'production', true);
+    expect([ingest.status, client.status]).toEqual([500, 500]);
+    expect([JSON.parse(ingest.text), JSON.parse(client.text)]).toEqual([CONSTANT_BODY, CONSTANT_BODY]);
+    expect(mockTrackError).toHaveBeenCalledTimes(2);
+  });
+
+  it('control: a 400 keeps its own authored message, and a 201 logs nothing', async () => {
+    const refused = await post('/ingest', {}, 'development', false);
+    expect(refused.status).toBe(400);
+    expect(JSON.parse(refused.text).error.message).toBe('service and message are required');
+    const accepted = await post('/client-errors', CLIENT_BODY, 'development', false);
+    expect(accepted.status).toBe(201);
+    expect(mockTrackError).toHaveBeenCalledTimes(1);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-730 A1: POST /ingest: the thrown message is not in the 500 body under development, demo, test or unset')` - at the tip the body carries `LEAK` under every non-production NODE_ENV (`leaked: true`), so the `toEqual` fails by assertion; after E2 the body is `CONSTANT_BODY` in all four.
- RED `it('RED KS-730 A2: POST /client-errors: ...')` - the same for `:125` / E3.
- RED `it('RED KS-730 A3: POST /ingest: the thrown message is logged once, server-side')` - at the tip `logger.error` is never called (no import, no log); after E1+E2 exactly `[['System error ingest failed', { error: LEAK }]]`.
- RED `it('RED KS-730 A4: POST /client-errors: the thrown message is logged once, server-side')` - the same for E1+E3 with `'Client error ingest failed'`.
- CONTROL `it('control: under production both routes already answer the constant text, and the service was reached')` - green on both trees (the tip's ternary already answers the constant text under production; `trackError` called twice proves the harness reaches the catch).
- CONTROL `it('control: a 400 keeps its own authored message, and a 201 logs nothing')` - green on both trees (`:76` untouched; the happy path logs nothing).

## Red cells
- RED KS-730 A1: POST /ingest: the thrown message is not in the 500 body under development, demo, test or unset
- RED KS-730 A2: POST /client-errors: the thrown message is not in the 500 body under development, demo, test or unset
- RED KS-730 A3: POST /ingest: the thrown message is logged once, server-side
- RED KS-730 A4: POST /client-errors: the thrown message is logged once, server-side

## Where (line-keyed - every **must change** line must appear as a `-` line AT ITS NUMBER in your diff; the two `-` lines are byte-identical, so the checker grades them by line number)
* `:95` - **must change**: `    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });` - the `/ingest` catch (E2)
* `:125` - **must change**: `    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });` - the `/client-errors` catch (E3)
* `:15` - (correct) `import * as errorTracking from '../services/errorTrackingService';` - stays (E1's leading context; the new import goes directly below it)
* `:16` - (correct) `import { authenticate, requireRole } from '../middleware/auth';` - stays (E1's trailing context)
* `:94` - (correct) `  } catch (err: any) {` - stays (E2's leading context)
* `:124` - (correct) `  } catch (err: any) {` - stays (E3's leading context)
* `:136` - (correct) `    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });` - stays (an ADMIN catch, Part B - NOT this task)
* `:76` - (correct) `      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'service and message are required', details: parsed.error.errors } });` - stays (the 400 the control pins)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/originate/src/routes/systemErrors.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (THREE hunks, headers `@@ -14,3 +14,5 @@`, `@@ -93,5 +93,6 @@`, `@@ -123,5 +123,6 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts` (one `@@ -0,0 +1,113 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `$`, `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
