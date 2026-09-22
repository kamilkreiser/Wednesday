# READY — KS-730-730INGEST500-R16B (Ornith, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks730-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 13:15 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks730-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks730-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/originate/src/routes/systemErrors.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/originate/src/routes/systemErrors.ts): `error: corrupt patch at line 8` (apply with the options recorded in section_<k>.opts; the raise seat states which); CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed11-drafter-precheck/INGEST500/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in systemErrors.ts (run 18 vs golden 19 body lines — context, since the change lines are equal) (identical in ks730a-ingest-500-never-answers-err-message.test.ts); hunk headers differ (systemErrors.ts: golden `@@ -14,3 +14,5 @@` vs run `@@ -14,3 +14,5 @@ import { z } from 'zod';`; systemErrors.ts: golden `@@ -93,5 +93,6 @@` vs run `@@ -93,5 +93,6 @@ systemErrorsRouter.post('/ingest', async (req: Request, res: Response) => {`; systemErrors.ts: golden `@@ -123,5 +123,6 @@` vs run `@@ -123,5 +124,6 @@ systemErrorsRouter.post('/client-errors', async (req: Request, res: Response) =`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 13:15 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks730-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/systemErrors.ts , Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	2	Blockchain/Dev/services/originate/src/routes/systemErrors.ts
113	0	Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (6 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 6 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/systemErrors.ts byte-exact incl. leading whitespace (apply mode lenient): OK 6 line(s) byte-exact incl. leading whitespace (of 6; 6 line(s) added by the apply)` [a3i_indent.out: `OK 6 line(s) byte-exact incl. leading whitespace (of 6; 6 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/originate/src/routes/systemErrors.ts: hunk 1 (@@ -14,3 +14,5 @@ import { z } from 'zod';) declared old=3 new=5 but actual old=2 new=4`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (hunks=3, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: corrupt patch at line 8`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts fails at the untouched tip (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-730 part A: the system-errors ingest routes never answer a 500 with err.message RED KS-730 A1: POST /ingest: the thrown message is not in the 500 body under development, demo, test or unset', 'KS-730 part A: the system-errors ingest routes never answer a 500 with err.message RED KS-730 A2: POST /client-errors: the thrown message is not in the 500 body under development, demo, test or unset', 'KS-730 part A: the system-errors ingest routes never answer a 500 with err.message RED KS-730 A3: POST /ingest: the thrown message is logged once, server-side', 'KS-730 part A: the system-errors ingest routes never answer a 500 with err.message RED KS-730 A4: POST /client-errors: the thrown message is logged once, server-side']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=835 failed=0 | after: total=841 failed=0` · `NEW reds: []` [baseline_suite.json total=835 failed=0; after_suite.json total=841 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +119/-2 test=src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (+6/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts` (+113/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks730-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks730-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
+++ b/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
@@ -14,3 +14,5 @@ import { z } from 'zod';
 import * as errorTracking from '../services/errorTrackingService';
+// KS-730: an inline 500 logs err.message server-side and answers the constant text, in every NODE_ENV.
+import { logger } from '../utils/logger';
 import { authenticate, requireRole } from '../middleware/auth';
@@ -93,5 +93,6 @@ systemErrorsRouter.post('/ingest', async (req: Request, res: Response) => {
     res.status(201).json({ success: true });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('System error ingest failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
@@ -123,5 +124,6 @@ systemErrorsRouter.post('/client-errors', async (req: Request, res: Response) =
     res.status(201).json({ success: true });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('Client error ingest failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts
@@ -0,0 +1,113 @@
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
