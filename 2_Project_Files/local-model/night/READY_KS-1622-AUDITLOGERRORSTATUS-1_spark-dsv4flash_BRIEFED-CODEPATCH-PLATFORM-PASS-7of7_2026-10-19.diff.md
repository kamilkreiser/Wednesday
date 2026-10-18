# READY — KS-1622-AUDITLOGERRORSTATUS-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1622_platform-r2/out.md.checker/patch.diff`** (from `ls` at 07:16 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1622_platform-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1622_platform-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1622_platform/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 07:16 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1622_platform-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/platform.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/api-gateway/src/routes/platform.ts
137	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/platform.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1622 - the audit-log route logs it when the upstream answers its first window with an error status RED KS-1622 E1 a first window that answers 500 with a JSON body: 200 with the audit_logs rows only, and ONE warn naming the route with status 500 and windowsRead 0', 'KS-1622 - the audit-log route logs it when the upstream answers its first window with an error status RED KS-1622 E2 a first window that answers 401 with a JSON body: ONE warn with status 401 and windowsRead 0, never the body text']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1195 failed=0 | after: total=1200 failed=0` · `NEW reds: []` [baseline_suite.json total=1195 failed=0; after_suite.json total=1200 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +138/-0 test=src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts` (+137/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1622_platform-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1622_platform-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/platform.ts b/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
index eee7fe895..b44ccc9c1 100644
--- a/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
@@ -420,2 +420,3 @@
           }, Math.min(UPSTREAM_TIMEOUT_MS, remaining));
+          if (!r.ok && collected.length === 0) logger.warn('GET /api/platform/audit-log upstream answered an error status', { status: r.status, windowsRead });
           const data = await r.json() as { entries?: any[]; total?: number };
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts
new file mode 100644
index 000000000..9cfe0e6a2
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts
@@ -0,0 +1,137 @@
+/**
+ * KS-1622 (the KS-1545 follow-up: the audit-log route logs nothing for an upstream error STATUS) -
+ * GET /api/platform/audit-log merges the tenant-provisioning platform_audit_log half with audit_logs. KS-1545 step 1 logs a
+ * warn when the platform half is dropped by a THROW (a refused connection, a later window that is not a list, the spent
+ * budget). An upstream that answers its FIRST window with an error status and a JSON body (a 500, a 401 'No token provided')
+ * throws nothing: `r.ok` was never read, the missing list was taken as an empty one, and the route answered 200 with the
+ * audit_logs rows only and logged NOTHING. It now logs ONE warn naming the route, the status and windowsRead 0. The response
+ * is unchanged. A LATER window that answers an error status still ends in the existing catch (ONE warn, not two).
+ *
+ * Same harness as ks1545: the REAL createPlatformRoutes on 127.0.0.1 against a stub upstream and an in-memory audit_logs query.
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express, { type RequestHandler } from 'express';
+import http from 'http';
+import type { AddressInfo } from 'net';
+import { createPlatformRoutes } from '../routes/platform';
+import { logger } from '../utils/logger';
+
+const T0 = Date.UTC(2026, 0, 1);
+/** The stub upstream's behaviour for the current cell. */
+let mode: 'ok' | 'destroy' | 'first-500' | 'first-401' | 'second-503' = 'ok';
+const PLATFORM = Array.from({ length: 3 }, (_, i) => ({ id: `P-${i}`, action: 'tenant_created', created_at: new Date(T0 - (10 + i) * 1000).toISOString() }));
+const APP_IDS = ['A-0', 'A-1'];
+let calls = 0;
+
+let upstream: http.Server;
+let gateway: http.Server;
+let base = '';
+const warnSpy = vi.spyOn(logger, 'warn').mockImplementation((() => logger) as never);
+
+beforeAll(async () => {
+  upstream = http.createServer((req, res) => {
+    calls += 1;
+    if (mode === 'destroy') { req.socket.destroy(); return; }
+    if (mode === 'first-500') {
+      res.writeHead(500, { 'Content-Type': 'application/json' }).end(JSON.stringify({ success: false, error: 'upstream broke' }));
+      return;
+    }
+    if (mode === 'first-401') {
+      res.writeHead(401, { 'Content-Type': 'application/json' }).end(JSON.stringify({ success: false, error: 'No token provided' }));
+      return;
+    }
+    if (mode === 'second-503' && calls === 2) {
+      res.writeHead(503, { 'Content-Type': 'application/json' }).end(JSON.stringify({ success: false }));
+      return;
+    }
+    const url = new URL(req.url ?? '/', 'http://x');
+    const limit = Number(url.searchParams.get('limit')) || 50;
+    const offset = Number(url.searchParams.get('offset')) || 0;
+    // second-503: the first window is short of the total, so the route must ask for a second one
+    const rowsOut = mode === 'second-503' ? PLATFORM.slice(offset, offset + 1) : PLATFORM.slice(offset, offset + limit);
+    res.writeHead(200, { 'Content-Type': 'application/json' }).end(JSON.stringify({ success: true, entries: rowsOut, total: PLATFORM.length }));
+  });
+  await new Promise<void>((r) => upstream.listen(0, '127.0.0.1', () => r()));
+  const superAdmin = (() => ((req, _res, next) => {
+    (req as unknown as { user: object }).user = { userId: 'u-ks1622', email: 'a@b.c', role: 'super_admin', verificationLevel: 'none' };
+    next();
+  }) as RequestHandler) as (required?: boolean) => RequestHandler;
+  const app = express();
+  app.use(createPlatformRoutes({
+    authenticateToken: superAdmin,
+    tenantProvisioningUrl: 'http://127.0.0.1:' + (upstream.address() as AddressInfo).port,
+    setTenantKey: () => {},
+    getTenantKey: () => undefined,
+    removeTenantKey: () => {},
+    query: async (sql: string) => {
+      if (sql.includes('COUNT(*)')) return { rows: [{ total: APP_IDS.length }] };
+      return { rows: APP_IDS.map((id, i) => ({ id, user_id: null, action: 'doc_verified', resource_type: null, resource_id: null, details: null, ip_address: null, success: true, created_at: new Date(T0 - i * 1000) })) };
+    },
+  }));
+  gateway = http.createServer(app);
+  await new Promise<void>((r) => gateway.listen(0, '127.0.0.1', () => r()));
+  base = 'http://127.0.0.1:' + (gateway.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  upstream.closeAllConnections();
+  await new Promise<void>((r) => gateway.close(() => r()));
+  await new Promise<void>((r) => upstream.close(() => r()));
+  warnSpy.mockRestore();
+});
+
+beforeEach(() => {
+  mode = 'ok';
+  calls = 0;
+  warnSpy.mockClear();
+});
+
+async function auditLog(): Promise<{ status: number; ids: string[]; total: number }> {
+  const r = await fetch(`${base}/api/platform/audit-log?limit=50&offset=0`);
+  const body = (await r.json()) as { entries?: Array<{ id: string }>; total?: number };
+  return { status: r.status, ids: (body.entries ?? []).map((e) => String(e.id)), total: body.total ?? -1 };
+}
+
+/** Every warn call, as [context, meta]. */
+function warnings(): Array<[unknown, unknown]> {
+  return (warnSpy.mock.calls as unknown as unknown[][]).map((c) => [c[0], c[1]] as [unknown, unknown]);
+}
+
+describe('KS-1622 - the audit-log route logs it when the upstream answers its first window with an error status', () => {
+  it('RED KS-1622 E1 a first window that answers 500 with a JSON body: 200 with the audit_logs rows only, and ONE warn naming the route with status 500 and windowsRead 0', async () => {
+    mode = 'first-500';
+    const page = await auditLog();
+    expect([page.status, page.ids, page.total]).toEqual([200, APP_IDS, APP_IDS.length]);
+    expect(warnings()).toEqual([[expect.stringContaining('/api/platform/audit-log'), { status: 500, windowsRead: 0 }]]);
+  });
+
+  it('RED KS-1622 E2 a first window that answers 401 with a JSON body: ONE warn with status 401 and windowsRead 0, never the body text', async () => {
+    mode = 'first-401';
+    const page = await auditLog();
+    expect([page.status, page.ids, page.total]).toEqual([200, APP_IDS, APP_IDS.length]);
+    expect(warnings()).toEqual([[expect.stringContaining('/api/platform/audit-log'), { status: 401, windowsRead: 0 }]]);
+    expect(JSON.stringify(warnSpy.mock.calls)).not.toContain('No token provided');
+  });
+
+  it('CONTROL KS-1622 E3 a second window that answers 503: still ONE warn, the existing catch with windowsRead 1', async () => {
+    mode = 'second-503';
+    const page = await auditLog();
+    expect([page.status, page.ids, page.total]).toEqual([200, APP_IDS, APP_IDS.length]);
+    expect(warnings()).toEqual([[expect.stringContaining('/api/platform/audit-log'), { error: 'tenant-provisioning audit-log window was not a list', windowsRead: 1 }]]);
+  });
+
+  it('CONTROL KS-1622 E4 an upstream that refuses the connection: still ONE warn from the catch with windowsRead 0', async () => {
+    mode = 'destroy';
+    const page = await auditLog();
+    expect([page.status, page.ids, page.total]).toEqual([200, APP_IDS, APP_IDS.length]);
+    expect(warnings()).toEqual([[expect.stringContaining('/api/platform/audit-log'), { error: 'fetch failed', windowsRead: 0 }]]);
+  });
+
+  it('CONTROL KS-1622 E5 a healthy upstream: both halves merged, no warn', async () => {
+    const page = await auditLog();
+    expect(page.status).toBe(200);
+    expect([...page.ids].sort()).toEqual([...APP_IDS, ...PLATFORM.map((p) => p.id)].sort());
+    expect(page.total).toBe(APP_IDS.length + PLATFORM.length);
+    expect(warnings()).toEqual([]);
+  });
+});
```
