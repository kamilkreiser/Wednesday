# READY — KS-730 PART A (originate `routes/systemErrors.ts` :95 + :125, the two unauthenticated ingest catches → `logger.error` + constant 500 text; import `utils/logger`) + NEW test ks730-security-71-inline-handlers-still-return.test.ts — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (05:52). Held by Wednesday at 06:01 AEST.
# Source read by me (Wednesday): model product +6/-2 in 3 hunks and the 111-line test IDENTICAL in sequence to the brief's fences (python compare; a mutated copy unequal). A4 4 red / 6 run by assertion, controls green; A6 originate NEW reds []; A7 tsc rc 0.
# ⚠ APPLY MODE LENIENT (--recount): the model's hunk headers are miscounted — the #1013 gate's R6 class. The raising seat re-emits the diff from the APPLIED tree (`git diff`) before the PR; `git apply --check` without --recount must pass on what it pushes.
# NOT GRADED BY THE CHECKER: an over-edit of the four identical admin catches (:136/:158/:168/:184) — A3e matches by text; the product section above is exactly the three named hunks (read).
# PR NOTES: "Refs KS-730 (part A)" — hardening: no caller reaches these catches today (errorTrackingService never throws). Tier 1 at raise. KS-730 stays open.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
+++ b/Blockchain/Dev/services/originate/src/routes/systemErrors.ts
@@ -14,6 +14,8 @@ import { Router, Request, Response } from 'express';
 import { z } from 'zod';
 import * as errorTracking from '../services/errorTrackingService';
 import { authenticate, requireRole } from '../middleware/auth';
+// KS-730: an inline 500 logs err.message server-side and answers the constant text, in every NODE_ENV.
+import { logger } from '../utils/logger';
 
 export const systemErrorsRouter = Router();
 
@@ -90,8 +92,9 @@ systemErrorsRouter.post('/ingest', async (req: Request, res: Response) => {
       metadata,
     });
 
     res.status(201).json({ success: true });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('System error ingest failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
 
@@ -120,8 +123,9 @@ systemErrorsRouter.post('/client-errors', async (req: Request, res: Response) =>
       metadata: { userAgent, source },
     });
 
     res.status(201).json({ success: true });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('Client error ingest failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
 

--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730-security-71-inline-handlers-still-return.test.ts
@@ -0,0 +1,111 @@
+// KS-730 (part A: originate routes/systemErrors.ts, POST /ingest and POST /client-errors). A thrown error must never
+// reach the 500 body in any NODE_ENV (the KS-727 doctrine), and its message must be logged instead of being lost.
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
+  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
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
+  const res = await fetch(`${baseUrl}/api/system-errors${path}`, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-730 part A — the system-errors ingest routes never answer a 500 with err.message', () => {
+  it('🔴 KS-730 A1 — POST /ingest: the thrown message is not in the 500 body under development, demo, test or unset', async () => {
+    for (const nodeEnv of NODE_ENVS) {
+      const reply = await post('/ingest', INGEST_BODY, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+    }
+  });
+
+  it('🔴 KS-730 A2 — POST /client-errors: the thrown message is not in the 500 body under development, demo, test or unset', async () => {
+    for (const nodeEnv of NODE_ENVS) {
+      const reply = await post('/client-errors', CLIENT_BODY, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+    }
+  });
+
+  it('🔴 KS-730 A3 — POST /ingest: the thrown message is logged once, server-side', async () => {
+    const reply = await post('/ingest', INGEST_BODY, 'development', true);
+    expect(reply.status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([['System error ingest failed', { error: LEAK }]]);
+  });
+
+  it('🔴 KS-730 A4 — POST /client-errors: the thrown message is logged once, server-side', async () => {
+    const reply = await post('/client-errors', CLIENT_BODY, 'development', true);
+    expect(reply.status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([['Client error ingest failed', { error: LEAK }]]);
+  });
+
+  it('🟢 KS-730 control — under production both routes already answer the constant text, and the service was reached', async () => {
+    const ingest = await post('/ingest', INGEST_BODY, 'production', true);
+    const client = await post('/client-errors', CLIENT_BODY, 'production', true);
+    expect([ingest.status, client.status]).toEqual([500, 500]);
+    expect([JSON.parse(ingest.text), JSON.parse(client.text)]).toEqual([CONSTANT_BODY, CONSTANT_BODY]);
+    expect(mockTrackError).toHaveBeenCalledTimes(2);
+  });
+
+  it('🟢 KS-730 control — a 400 keeps its own authored message, and a 201 logs nothing', async () => {
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

# SUPERSEDED-BY (feed11 drafter, 2026-09-22 12:57:28 AEST): re-briefed at develop 8c2f7b3fd as night/briefs/KS-730-R16B-INGEST500.md (golden PASS through the real checker in the feed11 precheck clone; Wednesday queues). This READY is STALE - do not raise it.
