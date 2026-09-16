# READY — KS-1182 F4 ONLY (demo-service errorHandler: headersSent → next(err); only an integer 400–599 is a status, else 500; the error's own headers when its status survives; a 4xx marked expose:false answers 'Request error') + NEW test ks1182-demo-service-errorhandler-unchecked-err-status.test.ts — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (03:57:57). Held by Wednesday at 04:14 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1182-ornith35b-night
# Source read by me (Wednesday): product 12 `+` / 5 `-` lines IDENTICAL in sequence to the brief's ONE hunk; the new test's 108 lines IDENTICAL to the brief's test block (python compare); apply STRICT; A4 7 red by assertion / 9 run, controls green; A6 demo-service no new red; A7 tsc rc 0.
# NOT GRADED BY THE CHECKER (brief P7): packages/shared ks727-errorhandler-class-guard + ks781-p3-3-body-parser-order (334/334 pre-measured with the golden) — the raising seat runs them.
# PR NOTES: "Refs KS-1182 (F4)" — F7 (the ks844 test name/markers) stays open. Runtime behaviour → the ticket stays In Progress on merge (§5f, Wednesday 03:5x). TIER 1 gate (a redaction change). Flag the writer's two decisions in the PR: the 'Request error' constant; headers applied only when the status survives the clamp. demo-service/src = partition-clear at 03:42 (0 open PRs).

```diff
--- a/Blockchain/Dev/services/demo-service/src/middleware/errorHandler.ts
+++ b/Blockchain/Dev/services/demo-service/src/middleware/errorHandler.ts
@@ -22,18 +22,25 @@
 /**
  * Terminal JSON error middleware. Mounted last in `createApp()`, after the 404
  * handler. Express recognises error middleware by its four declared
- * parameters, so the unused `_next` must stay.
+ * parameters; `next` also takes an error that arrives after the response has started.
  */
 export function errorHandler(
-  err: Error & { status?: number; statusCode?: number },
+  err: Error & { status?: number; statusCode?: number; expose?: boolean; headers?: Record<string, string> },
   _req: Request,
   res: Response,
-  _next: NextFunction,
+  next: NextFunction,
 ): void {
-  const status = err.status ?? err.statusCode ?? 500;
+  // KS-1182: a response that has started cannot be answered again; express's own handler closes the socket.
+  if (res.headersSent) return next(err);
+  const raw = err.status ?? err.statusCode;
+  // KS-1182: only an integer from 400 to 599 is an error status; 200, 302, 600, 99, NaN and '400' all answer 500.
+  const status = typeof raw === 'number' && Number.isInteger(raw) && raw >= 400 && raw <= 599 ? raw : 500;
+  // KS-1182: the error's own headers (Allow on a 405) go out with its own status, as express's finalhandler sends them.
+  if (status === raw && err.headers && typeof err.headers === 'object') res.set(err.headers);
   const code = status === 400 ? 'BAD_REQUEST' : status === 413 ? 'PAYLOAD_TOO_LARGE' : status >= 500 ? 'INTERNAL_ERROR' : 'REQUEST_ERROR';
   res.status(status).json({
     success: false,
-    error: { code, message: status >= 500 ? 'Internal server error' : err.message },
+    // KS-1182: a 4xx marked expose:false keeps its message private, as a 5xx always does.
+    error: { code, message: status >= 500 ? 'Internal server error' : err.expose === false ? 'Request error' : err.message },
   });
 }

--- /dev/null
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/ks1182-demo-service-errorhandler-unchecked-err-status.test.ts
@@ -0,0 +1,108 @@
+// KS-1182 (KS-844 gate F4): each cell hands ONE synthetic error to the REAL errorHandler in a real express app on loopback.
+// A backstop error handler mounted after it records the error that reached it, and answers when the handler throws.
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import http from 'http';
+import express, { NextFunction, Request, Response } from 'express';
+import type { AddressInfo } from 'net';
+import { errorHandler } from '../middleware/errorHandler';
+
+type Reply = { status: number; allow: string | undefined; backstop: boolean; body: string };
+let currentErr: unknown = null;
+let startBody = false;
+let backstopSaw: unknown = null;
+let server: http.Server;
+let port = 0;
+
+beforeAll(async () => {
+  const app = express();
+  app.get('/boom', (_req: Request, res: Response, next: NextFunction) => {
+    if (startBody) {
+      res.writeHead(200, { 'content-type': 'text/plain' });
+      res.write('partial');
+    }
+    next(currentErr);
+  });
+  app.use(errorHandler);
+  app.use(((e: unknown, _req: Request, res: Response, _next: NextFunction) => {
+    backstopSaw = e;
+    if (res.headersSent) return void res.end();
+    res.statusCode = 500;
+    res.removeHeader('content-length');
+    res.setHeader('x-backstop', '1');
+    res.end('backstop answered');
+  }) as express.ErrorRequestHandler);
+  server = await new Promise<http.Server>((resolve) => { const s = app.listen(0, '127.0.0.1', () => resolve(s)); });
+  port = (server.address() as AddressInfo).port;
+});
+afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));
+
+function drive(err: unknown, beginBody = false): Promise<Reply> {
+  currentErr = err;
+  startBody = beginBody;
+  backstopSaw = null;
+  return new Promise((resolve, reject) => {
+    http.get({ host: '127.0.0.1', port, path: '/boom', agent: false }, (res) => {
+      let body = '';
+      res.setEncoding('utf8');
+      res.on('data', (chunk: string) => (body += chunk));
+      res.on('end', () => resolve({ status: res.statusCode ?? 0, allow: res.headers.allow, backstop: res.headers['x-backstop'] === '1', body }));
+    }).on('error', reject);
+  });
+}
+function withStatus(message: string, fields: Record<string, unknown>): Error {
+  return Object.assign(new Error(message), fields);
+}
+
+describe('KS-1182 — demo-service errorHandler answers only a real error status', () => {
+  it('🔴 KS-1182 H1 — an error carrying status 200 answers 500, never 200', async () => {
+    const reply = await drive(withStatus('msg-200', { status: 200 }));
+    expect(reply.status).toBe(500);
+  });
+  it('🔴 KS-1182 H2 — an error carrying status 302, or status 600 (H3), answers 500', async () => {
+    const redirectReply = await drive(withStatus('msg-302', { status: 302 }));
+    expect(redirectReply.status, 'KS-1182 H2: status 302').toBe(500);
+    const highReply = await drive(withStatus('msg-600', { status: 600 }));
+    expect(highReply.status, 'KS-1182 H3: status 600').toBe(500);
+  });
+  it('🔴 KS-1182 H4 — a string status of 400 is not a status and answers 500', async () => {
+    const reply = await drive(withStatus('msg-string', { status: '400' }));
+    expect(reply.status).toBe(500);
+  });
+  it('🔴 KS-1182 H5 — a NaN status, and a status of 99, are answered 500 by the handler itself, not by the backstop', async () => {
+    const nanReply = await drive(withStatus('msg-nan', { status: Number.NaN }));
+    expect(nanReply.backstop, 'KS-1182 H5: the handler threw on NaN, so the backstop answered').toBe(false);
+    expect(nanReply.body).toContain('INTERNAL_ERROR');
+    const lowReply = await drive(withStatus('msg-99', { status: 99 }));
+    expect(lowReply.backstop, 'KS-1182 H11: the handler threw on 99, so the backstop answered').toBe(false);
+    expect(lowReply.status).toBe(500);
+  });
+  it('🔴 KS-1182 H9 — a 405 keeps the Allow header the error carries', async () => {
+    const reply = await drive(withStatus('Method Not Allowed', { status: 405, headers: { Allow: 'GET' } }));
+    expect(reply.status).toBe(405);
+    expect(reply.allow).toBe('GET');
+  });
+  it('🔴 KS-1182 H12 — a 400 marked expose false does not echo its message', async () => {
+    const reply = await drive(withStatus('private detail ks1182', { status: 400, expose: false }));
+    expect(reply.status).toBe(400);
+    expect(reply.body).not.toContain('private detail ks1182');
+  });
+  it('🔴 KS-1182 H10 — an error after the response started is handed on unchanged', async () => {
+    const late = withStatus('late ks1182', { status: 500 });
+    const reply = await drive(late, true);
+    expect(reply.body).toBe('partial');
+    expect(backstopSaw, 'KS-1182 H10: the backstop must receive the ORIGINAL error').toBe(late);
+  });
+  it('🟢 KS-1182 control — a 400 with a client message is echoed by the handler', async () => {
+    const reply = await drive(withStatus('provider and code are required', { statusCode: 400 }));
+    expect(reply.backstop).toBe(false);
+    expect(reply.status).toBe(400);
+    expect(reply.body).toContain('provider and code are required');
+  });
+  it('🟢 KS-1182 control — a 503 with an internal message answers 503 and the constant text', async () => {
+    const reply = await drive(withStatus('db password ks1182', { status: 503 }));
+    expect(reply.backstop).toBe(false);
+    expect(reply.status).toBe(503);
+    expect(reply.body).toContain('Internal server error');
+    expect(reply.body).not.toContain('db password ks1182');
+  });
+});
```
