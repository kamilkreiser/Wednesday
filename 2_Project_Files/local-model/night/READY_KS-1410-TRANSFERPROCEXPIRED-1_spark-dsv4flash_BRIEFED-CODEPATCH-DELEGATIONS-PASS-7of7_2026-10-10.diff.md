# READY — KS-1410-TRANSFERPROCEXPIRED-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500/out.md.checker/patch.diff`** (from `ls` at 00:36 2026-10-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 00:36 2026-10-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/transfer/src/routes/delegations.ts , Blockchain/Dev/services/transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/transfer/src/routes/delegations.ts` (product) and `Blockchain/Dev/services/transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	2	Blockchain/Dev/services/transfer/src/routes/delegations.ts
116	0	Blockchain/Dev/services/transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/transfer/src/routes/delegations.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/transfer/src/routes/delegations.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1410-delegations-process-expired-500.test.ts fails at the untouched tip (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1410 transfer delegations: a 500 never answers the thrown text RED KS-1410 T1 NODE_ENV=production: the thrown message is not in the 500 body', 'KS-1410 transfer delegations: a 500 never answers the thrown text RED KS-1410 T1 NODE_ENV=development: the thrown message is not in the 500 body', 'KS-1410 transfer delegations: a 500 never answers the thrown text RED KS-1410 T1 NODE_ENV=test: the thrown message is not in the 500 body', 'KS-1410 transfer delegations: a 500 never answers the thrown text RED KS-1410 T2: the thrown message is logged once, server-side, with the route named']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1410-delegations-process-expired-500.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=79 failed=0 | after: total=85 failed=0` · `NEW reds: []` [baseline_suite.json total=79 failed=0; after_suite.json total=85 failed=0]
- A6 [verbatim]: `PASS A6 whole services/transfer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/transfer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +120/-2 test=src/__tests__/ks1410-delegations-process-expired-500.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/transfer/src/routes/delegations.ts` (+4/-2 per numstat.out) and the test file `Blockchain/Dev/services/transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts` (+116/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500/checker.out`.

```diff
--- a/Blockchain/Dev/services/transfer/src/routes/delegations.ts
+++ b/Blockchain/Dev/services/transfer/src/routes/delegations.ts
@@ -10,5 +10,6 @@
 import { CreateDelegationRequest, DelegationType } from '../types/delegation.types';
 import { isoDateTimeSchema } from '@secuura/shared';
 import { DOCUMENT_ID_PATTERN } from '../utils/ids';
+import { logger } from '../utils/logger';
-
+
 const router = Router();
@@ -281,6 +282,7 @@
   } catch (error) {
     if (error instanceof Error) {
-      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });
+      logger.error('Process expired delegations failed (POST /api/delegations/admin/process-expired)', { error: error.message });
+      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
     }
     next(error);
   }
--- /dev/null
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts
@@ -0,0 +1,116 @@
+/**
+ * KS-1410 (transfer routes/delegations.ts): the POST /admin/process-expired catch block answered a 500 whose body
+ * carried the thrown error's own text (`message: error.message`) with NO NODE_ENV guard, so it reached the client in
+ * every environment, production included. The fix logs the thrown text server-side with the route named and answers
+ * the constant body, the shape of api-gateway's KS-1410 pass and originate's fail500 (KS-1334, KS-730).
+ *
+ * Harness: the KS-444 route test's (a real express app on an ephemeral port, the delegation service mocked).
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, afterEach, vi } from 'vitest';
+import http from 'http';
+import type { AddressInfo } from 'net';
+
+const mockLoggerError = vi.hoisted(() => vi.fn());
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: mockLoggerError, debug: vi.fn() },
+}));
+
+const processExpiredDelegations = vi.fn();
+const revokeDelegation = vi.fn();
+vi.mock('../services/delegationService', () => ({
+  delegationService: {
+    get processExpiredDelegations() {
+      return processExpiredDelegations;
+    },
+    get revokeDelegation() {
+      return revokeDelegation;
+    },
+  },
+}));
+
+import express from 'express';
+import { delegationRoutes } from '../routes/delegations';
+
+// THE FIXTURE IS LOAD-BEARING: a private host:port and a marker no other code path could produce.
+const LEAK = 'connect ECONNREFUSED 10.0.4.17:5432 ks1410-transfer-private-detail';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const CONTEXT = 'Process expired delegations failed (POST /api/delegations/admin/process-expired)';
+
+describe('KS-1410 transfer delegations: a 500 never answers the thrown text', () => {
+  let server: http.Server;
+  let baseUrl: string;
+
+  function post(path: string, body?: unknown): Promise<{ status: number; data: any }> {
+    return new Promise((resolve, reject) => {
+      const url = new URL(path, baseUrl);
+      const req = http.request(
+        { hostname: url.hostname, port: url.port, path: url.pathname, method: 'POST', headers: { 'Content-Type': 'application/json' } },
+        (res) => {
+          let raw = '';
+          res.on('data', (c) => (raw += c));
+          res.on('end', () => {
+            try {
+              resolve({ status: res.statusCode || 500, data: JSON.parse(raw) });
+            } catch {
+              resolve({ status: res.statusCode || 500, data: raw });
+            }
+          });
+        },
+      );
+      req.on('error', reject);
+      if (body !== undefined) req.write(JSON.stringify(body));
+      req.end();
+    });
+  }
+
+  beforeAll(async () => {
+    const app = express();
+    app.use(express.json());
+    app.use((req: any, _res, next) => {
+      req.user = { userId: '00000000-0000-4000-8000-000000000001' };
+      next();
+    });
+    app.use('/api/delegations', delegationRoutes);
+    await new Promise<void>((resolve) => {
+      server = app.listen(0, '127.0.0.1', () => resolve());
+    });
+    baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+  });
+
+  afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));
+
+  beforeEach(() => {
+    processExpiredDelegations.mockReset();
+    revokeDelegation.mockReset();
+    mockLoggerError.mockClear();
+  });
+  afterEach(() => vi.unstubAllEnvs());
+
+  it.each(['production', 'development', 'test'])('RED KS-1410 T1 NODE_ENV=%s: the thrown message is not in the 500 body', async (nodeEnv) => {
+    vi.stubEnv('NODE_ENV', nodeEnv);
+    processExpiredDelegations.mockRejectedValue(new Error(LEAK));
+    const res = await post('/api/delegations/admin/process-expired');
+    expect({ status: res.status, leaked: JSON.stringify(res.data).includes(LEAK) }).toEqual({ status: 500, leaked: false });
+    expect(res.data).toEqual(CONSTANT_BODY);
+  });
+
+  it('RED KS-1410 T2: the thrown message is logged once, server-side, with the route named', async () => {
+    processExpiredDelegations.mockRejectedValue(new Error(LEAK));
+    const res = await post('/api/delegations/admin/process-expired');
+    expect(res.status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([[CONTEXT, { error: LEAK }]]);
+  });
+
+  it('control KS-1410 TC1: success still answers 200 with the expired count and logs nothing', async () => {
+    processExpiredDelegations.mockResolvedValue(3);
+    const res = await post('/api/delegations/admin/process-expired');
+    expect([res.status, res.data.success, res.data.data.expiredCount]).toEqual([200, true, 3]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1410 TC2: the revoke route still answers 404 NOT_FOUND with its business message', async () => {
+    revokeDelegation.mockRejectedValue(new Error('Delegation not found'));
+    const res = await post('/api/delegations/d-ks1410/revoke', { reason: 'cleanup' });
+    expect([res.status, res.data.error.code, res.data.error.message]).toEqual([404, 'NOT_FOUND', 'Delegation not found']);
+  });
+});
```
