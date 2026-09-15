```diff
--- a/services/api-gateway/src/middleware/csrf.ts
+++ b/services/api-gateway/src/middleware/csrf.ts
@@ -95,6 +95,8 @@ const DEFAULT_CONFIG: CsrfConfig = {
     // (startsWith match covers /verify, /verify-file, /verify-batch.)
     '/api/verification/verify',
+    // KS-1165: the v2 twins are published anonymous (security: []) like v1 — same exclusion, same startsWith rule.
+    '/api/v2/verification/verify',
     // Client-side logger sink — sendBeacon fires-and-forgets a JSON batch
     // of warn/error events from the SPA's logger. No session auth, no
     // CSRF interaction; the body is already sanitised client-side. Origin
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts
@@ -0,0 +1,101 @@
+/**
+ * Regression tests for KS-1165: excludedPaths must carry an entry that
+ * matches `/api/v2/verification/*` so cookie-bearing browser callers to the
+ * v2 verify endpoints aren't rejected with `CSRF_TOKEN_MISSING`.
+ */
+
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+import type { Request, Response } from 'express';
+import { createCsrfMiddleware } from '../middleware/csrf';
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    warn: vi.fn(),
+    error: vi.fn(),
+    info: vi.fn(),
+  },
+}));
+
+// ---------------------------------------------------------------------------
+// Helpers
+// ---------------------------------------------------------------------------
+
+function makeReq(overrides: Partial<Request> = {}): Request {
+  return {
+    headers: {},
+    cookies: {},
+    body: {},
+    query: {},
+    path: '/api/documents',
+    method: 'POST',
+    ip: '127.0.0.1',
+    ...overrides,
+  } as unknown as Request;
+}
+
+function makeRes(): Response & { _status: number; _json: any } {
+  const res: any = {
+    _status: 0,
+    _json: null,
+    status(code: number) {
+      this._status = code;
+      return this;
+    },
+    json(payload: any) {
+      this._json = payload;
+      return this;
+    },
+    cookie: vi.fn(),
+    setHeader: vi.fn(),
+  };
+  return res;
+}
+
+const { protect } = createCsrfMiddleware();
+
+describe('KS-1165 — v2 verification paths are excluded from CSRF', () => {
+  let next: ReturnType<typeof vi.fn>;
+
+  beforeEach(() => {
+    next = vi.fn();
+  });
+
+  it('🔴 KS-1165 — POST /api/v2/verification/verify-file with a cookie is excluded from CSRF', () => {
+    // Cookie-bearing caller of the v2 verify-file endpoint must be excluded
+    // by the same startsWith rule that excludes v1's /api/verification/verify.
+    const req = makeReq({
+      path: '/api/v2/verification/verify-file',
+      headers: { cookie: 'session=ambient', origin: 'http://localhost:6882' },
+      cookies: { session: 'ambient' },
+    });
+    const res = makeRes();
+
+    protect(req, res, next);
+
+    expect(next).toHaveBeenCalledOnce();
+    expect(res._status).toBe(0);
+  });
+
+  it('🔴 KS-1165 — POST /api/v2/verification/verify with a cookie is excluded from CSRF', () => {
+    const req = makeReq({
+      path: '/api/v2/verification/verify',
+      headers: { cookie: 'session=ambient', origin: 'http://localhost:6882' },
+      cookies: { session: 'ambient' },
+    });
+    const res = makeRes();
+
+    protect(req, res, next);
+
+    expect(next).toHaveBeenCalledOnce();
+    expect(res._status).toBe(0);
+  });
+
+  it('KS-1165 control — the v1 path is excluded (before and after) and an unrelated cookie write is still rejected', () => {
+    const reqV1 = makeReq({
+      path: '/api/verification/verify-file',
+      headers: { cookie: 'session=ambient', origin: 'http://localhost:6882' },
+      cookies: { session: 'ambient' },
+    });
+    const resV1 = makeRes();
+    protect(reqV1, resV1, next);
+    expect(next).toHaveBeenCalledOnce();
+    expect(resV1._status).toBe(0);
+
+    next.mockClear();
+    const reqOther = makeReq({
+      path: '/api/documents',
+      headers: { cookie: 'session=ambient', origin: 'http://localhost:6882' },
+      cookies: { session: 'ambient' },
+    });
+    const resOther = makeRes();
+    protect(reqOther, resOther, next);
+    expect(next).not.toHaveBeenCalled();
+    expect(resOther._status).toBe(403);
+    expect(resOther._json.error.code).toBe('CSRF_TOKEN_MISSING');
+  });
+});
```
