# READY — KS-1374 PART A: the global limiter pinned at the demo limit (spark-dsv4flash, briefed, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-29_KS-1374-R1/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1374/KS-1374.golden.diff` (`cmp` rc 0; a mutated-golden control DIFFERS, rc 1), measured by Wednesday at 16:35.

**Held BY HAND at 16:35 2026-09-29 by Wednesday seat 35f90900.** hold_ready.py refused: `hold_ready: REFUSE — checker.out has no 'mode: code_patch' line — the input says code_patch but the checker did not run it as one` (the owed test_only/code_patch gap, same as KS-888-VALIDATE-LOGONLY). Source at develop 2cb858335472 (ls-remote 16:20/16:27/16:34, unmoved).

- **Scope: PART A of three.** Kam's instruction (live board, Tuesday tab, routed by Tuesday: 16:17:55 "make the change"; 16:18:57 Peter's reply "for us to implement the change") = our KS-1374 comment's option 2 + one limiter test. Part A = that test only (new file, no product line). **Part B** (not Spark: outside services/): `env.example:192` and `.env.example:205` 2000 → 10000 for LOCAL stacks; `docker-compose.yml:497`'s `:-2000` fallback STAYS (the demo VM runs that compose file; this test pins it). **Part C** (not Spark: systemTest/): our comment's premise "the harness speeds up on its own" is FALSE — `systemTest/akto/src/setup/aktoRateLimit.ts:60` hard-codes `PLATFORM_REQUESTS_PER_MINUTE = 2000` and `derivedRateLimit()` (:199) derives from it (read by Wednesday at develop 2cb85833). B + C + a correction comment on KS-1374 go to a Claude raise seat with this READY.
- UNMEASURED (the brief-writer): the demo's real limit (2000 assumed from our comment); the behaviour cells use the same limiter settings, not the gateway's own limiter instance.
- Checker verdict [checker.out, verbatim]:
  - `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/index.ts:474)`
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts } — the product file is untouched, as the ticket requires`
  - `INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured`
  - `PASS A4 RED-FIRST: src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts fails at the untouched tip (1 failed / 7 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts passes with the product hunk (7 passed / 7 run)`
  - `INFO control cell present: 6 cell(s) passed BEFORE and 7 AFTER (the harness reaches the code both times)`
  - `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
  - `INFO tsc on the test file alone (--types node,vitest/globals): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)`
  - `SUMMARY files=1 +116/-0 test=src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts red_first=yes apply_mode=strict`
  - `RESULT: PASS (7/7)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=0 ok=0 bad=0 skipped_newfile=1)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts
@@ -0,0 +1,116 @@
+/**
+ * KS-1374 - local stacks may run the global limiter looser than the demo
+ * (RATE_LIMIT_MAX_REQUESTS raised for scanning), so this file pins the limiter
+ * at the DEMO figure: 2000 requests per 60 s window per address.
+ * Wiring cells read index.ts (the KS-733 shape: no gateway test boots it).
+ * Behaviour cells drive express-rate-limit with the same options at the demo
+ * figure and the REAL skip predicate over a local socket: request 2001 is
+ * refused with 429, and the read-only paths still skip.
+ */
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+import rateLimit from 'express-rate-limit';
+import { shouldSkipGlobalRateLimit } from '../middleware/rateLimitSkip';
+
+const DEMO_MAX = 2000;
+const GATEWAY_SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');
+const COMPOSE = readFileSync(join(__dirname, '..', '..', '..', '..', 'docker-compose.yml'), 'utf8');
+
+/** The global limiter call in index.ts, from app.use(rateLimit({ to its closing line. */
+function globalLimiterCall(): string {
+  const at = GATEWAY_SRC.indexOf('app.use(rateLimit({');
+  if (at === -1) return '';
+  return GATEWAY_SRC.slice(at, GATEWAY_SRC.indexOf('}));', at) + 4);
+}
+
+let server: Server;
+let base = '';
+
+beforeAll(async () => {
+  const app = express();
+  app.use(rateLimit({
+    windowMs: 60 * 1000,
+    max: DEMO_MAX,
+    message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many requests, please try again later.' } },
+    standardHeaders: true,
+    legacyHeaders: false,
+    skip: (req) => shouldSkipGlobalRateLimit({
+      authHeader: (req.headers.authorization as string) || '',
+      path: req.path,
+      nodeEnv: 'demo',
+      disableEnv: undefined,
+    }),
+  }));
+  app.use((_req, res) => { res.json({ ok: true }); });
+  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  server.closeAllConnections();
+  await new Promise<void>((resolve) => { server.close(() => resolve()); });
+});
+
+describe('KS-1374 global limiter wiring in index.ts', () => {
+  it('RED KS-1374 W1: the global limiter max reads RATE_LIMIT_MAX_REQUESTS', () => {
+    expect(globalLimiterCall()).toContain('max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS ||');
+  });
+
+  it('control KS-1374 W2: the global limiter keeps a 60 s window, standard headers, the shared skip and its 429 code', () => {
+    const call = globalLimiterCall();
+    expect(call).toContain('windowMs: 60 * 1000,');
+    expect(call).toContain('standardHeaders: true,');
+    expect(call).toContain('skip: (req) => shouldSkipGlobalRateLimit({');
+    expect(call).toContain('RATE_LIMIT_EXCEEDED');
+  });
+
+  it('control KS-1374 D1: the compose fallback stays at the demo figure, so a local raise lives in .env only', () => {
+    expect(COMPOSE).toContain('RATE_LIMIT_MAX_REQUESTS=${RATE_LIMIT_MAX_REQUESTS:-' + DEMO_MAX + '}');
+  });
+});
+
+describe('KS-1374 global limiter behaviour at the demo figure', () => {
+  it('control KS-1374 B1: the first 2000 requests in a window pass, under a 2000 per 60 s policy', async () => {
+    const statuses: number[] = [];
+    let policy = '';
+    for (let i = 0; i < DEMO_MAX; i += 100) {
+      const batch = await Promise.all(Array.from({ length: 100 }, () => fetch(base + '/api/v1/documents')));
+      for (const r of batch) { statuses.push(r.status); await r.text(); }
+      policy = batch[0].headers.get('ratelimit-policy') || '';
+    }
+    expect(statuses.filter((s) => s === 200).length).toBe(DEMO_MAX);
+    expect(policy).toBe(DEMO_MAX + ';w=60');
+  }, 60000);
+
+  it('control KS-1374 B2: request 2001 in the same window is refused with 429 RATE_LIMIT_EXCEEDED', async () => {
+    const r = await fetch(base + '/api/v1/documents');
+    const body = await r.json();
+    expect(r.status).toBe(429);
+    expect(body.error.code).toBe('RATE_LIMIT_EXCEEDED');
+  });
+
+  it('control KS-1374 B3: with the budget spent, the read-only paths still skip the limiter', async () => {
+    for (const path of ['/health', '/api/verification/abc']) {
+      const r = await fetch(base + path);
+      await r.text();
+      expect(r.status).toBe(200);
+    }
+  });
+
+  it('control KS-1374 B4: with the budget spent, a test_token bearer is still refused in demo, even with test tokens enabled', async () => {
+    const before = process.env.ENABLE_TEST_TOKENS;
+    process.env.ENABLE_TEST_TOKENS = 'true';
+    try {
+      const r = await fetch(base + '/api/v1/documents', { headers: { authorization: 'Bearer test_token_ks1374' } });
+      await r.text();
+      expect(r.status).toBe(429);
+    } finally {
+      if (before === undefined) delete process.env.ENABLE_TEST_TOKENS;
+      else process.env.ENABLE_TEST_TOKENS = before;
+    }
+  });
+});
```
