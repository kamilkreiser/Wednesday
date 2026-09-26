# READY — KS-1341-WEBHOOKS500-C (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-C/out.md.checker/patch.diff`** (from `ls` at 20:46 2026-09-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-C/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-C/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 20:46 2026-09-26 by Wednesday evening seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-C/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3f70224a069b944334480478ad5d16a5ed33eeae`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/webhooks.ts , Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/originate/src/routes/webhooks.ts
169	0	Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/webhooks.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts fails at the untouched tip (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset', 'KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1341 C1 GET /:id/deliveries: the thrown message is not in the 500 body under production, development, test or unset', 'KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named', 'KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1341 C2 GET /:id/deliveries: the thrown message is logged once, server-side, with this route named', 'KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=962 failed=0 | after: total=970 failed=0` · `NEW reds: []` [baseline_suite.json total=962 failed=0; after_suite.json total=970 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +171/-2 test=src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (+169/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3f70224a069b944334480478ad5d16a5ed33eeae` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-C/input.json`. Brief (given by --brief; its `# ` heading names KS-1341): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1341/brief-C.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-C/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -389,5 +389,5 @@
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook test send failed (POST /api/webhooks/:id/test)', err);
   }
 });
@@ -414,5 +414,5 @@
     res.json({ success: true, deliveries: rows });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)', err);
   }
 });
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
@@ -0,0 +1,169 @@
+// KS-1341 part C (originate routes/webhooks.ts, POST /:id/test and GET /:id/deliveries): the last two
+// of the seven catch blocks that answered a 500 whose body carried the thrown error's own text in
+// every NODE_ENV. Parts A and B added the fail500 helper and converted the other five. This part
+// also carries the whole-file SOURCE cell, which is RED until all seven are converted.
+// Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
+//
+// THE DELIVERIES TRAP. GET /:id/deliveries chains .catch(() => []) onto its query, so a REJECTED
+// $queryRaw is swallowed into a 200 with an empty list and never reaches the catch under test. That
+// cell therefore makes $queryRaw THROW SYNCHRONOUSLY; control C0 pins the swallowing branch.
+// POST /:id/test awaits its query with no .catch, so a rejection reaches its catch directly.
+const mockQueryRaw = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: mockQueryRaw,
+    $executeRaw: jest.fn(),
+    $executeRawUnsafe: jest.fn(),
+  },
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: '11111111-2222-4333-8444-555555555555' };
+    next();
+  },
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    encryptField: jest.fn(() => 'v1:mock-ciphertext'),
+    decryptField: jest.fn(() => ''),
+    runWithTenantId: jest.fn(async (_tenantId: unknown, fn: () => unknown) => fn()),
+    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw) })),
+  }),
+);
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { readFileSync } from 'fs';
+import path from 'path';
+import { webhooksRouter } from '../routes/webhooks';
+
+// THE FIXTURE IS LOAD-BEARING. It must not contain 'does not exist' (the KS-730 PR3 trap) and must
+// carry no Postgres SQLSTATE token that utils/pgErrors.ts would classify.
+const LEAK = 'canceling statement due to statement timeout on svc_webhook_deliveries ks1341c-private-detail';
+const NODE_ENVS = ['production', 'development', 'test', undefined];
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
+const WEBHOOK_ID = 'a1b2c3d4-5678-4abc-9def-0123456789ab';
+
+const app = express();
+app.use('/api/webhooks', express.json(), webhooksRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => {
+  if (ORIGINAL_NODE_ENV === undefined) delete process.env.NODE_ENV;
+  else process.env.NODE_ENV = ORIGINAL_NODE_ENV;
+  server?.close();
+});
+beforeEach(() => jest.clearAllMocks());
+
+function setNodeEnv(v: string | undefined): void {
+  if (v === undefined) delete process.env.NODE_ENV;
+  else process.env.NODE_ENV = v;
+}
+
+// Each route is driven by making ITS OWN query throw, so a cell cannot pass because another handler
+// answered.
+const ROUTES = [
+  {
+    label: 'POST /:id/test',
+    method: 'POST',
+    path: '/' + WEBHOOK_ID + '/test',
+    arm: () => mockQueryRaw.mockRejectedValueOnce(new Error(LEAK)),
+    context: 'Webhook test send failed (POST /api/webhooks/:id/test)',
+  },
+  {
+    label: 'GET /:id/deliveries',
+    method: 'GET',
+    path: '/' + WEBHOOK_ID + '/deliveries',
+    arm: () => mockQueryRaw.mockImplementationOnce(() => { throw new Error(LEAK); }),
+    context: 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)',
+  },
+];
+
+async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  route.arm();
+  const res = await fetch(baseUrl + '/api/webhooks' + route.path, { method: route.method });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text', () => {
+  it.each(ROUTES)('RED KS-1341 C1 $label: the thrown message is not in the 500 body under production, development, test or unset', async (route) => {
+    for (const nodeEnv of NODE_ENVS) {
+      // Cleared PER ENVIRONMENT: without it the production call satisfies every later iteration,
+      // so a helper that logged only under production would stay green (gate 28, N-1288-2).
+      mockLoggerError.mockClear();
+      const reply = await call(route, nodeEnv);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+      // REACHED in THIS environment, not merely clean: exactly one call, this route's context, the thrown text.
+      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: LEAK }]] });
+    }
+  });
+
+  it.each(ROUTES)('RED KS-1341 C2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
+    const reply = await call(route, 'production');
+    expect(reply.status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
+  });
+
+  it('RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts', () => {
+    // Weaker than the behavioural cells, and deliberately so: it reads the file, not the behaviour.
+    // It is what proves the seven sites of parts A, B and C are all converted, and that nobody
+    // re-adds the shape. Comment lines are skipped so the helper's docblock cannot be counted.
+    const src = readFileSync(path.join(__dirname, '..', 'routes', 'webhooks.ts'), 'utf8');
+    const lines = src.split('\n').filter((l) => !l.trim().startsWith('*') && !l.trim().startsWith('//'));
+    const leaks = lines.filter((l) => /message: *err\??\.?message/.test(l));
+    const helperCalls = lines.filter((l) => l.includes('fail500(res,'));
+    const contexts = helperCalls.map((l) => (l.match(/fail500\(res, '([^']+)'/) ?? [])[1]);
+    const definitions = lines.filter((l) => l.startsWith('function fail500('));
+    expect({ leaks: leaks.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size, definitions: definitions.length })
+      .toEqual({ leaks: 0, helperCalls: 7, distinctContexts: 7, definitions: 1 });
+    expect(contexts.filter((c) => !c)).toEqual([]);
+  });
+
+  it('control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch', async () => {
+    // PRE-EXISTING behaviour this change must NOT alter, and the reason the deliveries cell throws
+    // synchronously: same route, same message, a rejected promise instead, a different answer.
+    setNodeEnv('production');
+    mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
+    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/deliveries');
+    expect(res.status).toBe(200);
+    expect(JSON.parse(await res.text())).toEqual({ success: true, deliveries: [] });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing', async () => {
+    // Without this, every "not leaked" pass above is consistent with the router answering 500 always,
+    // and it proves the helper did not flatten a message the route MEANT to return.
+    setNodeEnv('production');
+    mockQueryRaw.mockResolvedValueOnce([]);
+    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/test', { method: 'POST' });
+    expect(res.status).toBe(404);
+    expect(JSON.parse(await res.text()).error.message).toBe('Webhook not found');
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1341 C: the LEAK string is the thrown text and dodges every benign branch', () => {
+    // If LEAK were absent from the thrown error, every leaked: false above would hold trivially.
+    expect(new Error(LEAK).message).toBe(LEAK);
+    expect(LEAK.length).toBeGreaterThan(20);
+    expect(LEAK).not.toContain('does not exist');
+    expect(LEAK).not.toMatch(/\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/);
+  });
+});
```
