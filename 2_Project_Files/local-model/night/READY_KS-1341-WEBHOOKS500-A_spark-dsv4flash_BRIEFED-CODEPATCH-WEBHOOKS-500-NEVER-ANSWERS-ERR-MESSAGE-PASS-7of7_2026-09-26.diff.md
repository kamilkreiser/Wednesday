# READY — KS-1341-WEBHOOKS500-A (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/out.md.checker/patch.diff`** (from `ls` at 15:17 2026-09-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/golden_probe/out.md.checker/patch.diff` rc 0, Wednesday (Spark harness runner)).

**Held 15:17 2026-09-26 by Wednesday (Spark harness runner) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `e080174c86c671349c508560744644fc0ef33388`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/webhooks.ts , Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
20	2	Blockchain/Dev/services/originate/src/routes/webhooks.ts
173	0	Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (19 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 20 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/webhooks.ts byte-exact incl. leading whitespace (apply mode strict): OK 19 line(s) byte-exact incl. leading whitespace (of 19; 20 line(s) added by the apply)` [a3i_indent.out: `OK 19 line(s) byte-exact incl. leading whitespace (of 19; 20 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts fails at the untouched tip (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1341 part A: GET / and POST / never answer a 500 with the thrown text RED KS-1341 A1 GET /: the thrown message is not in the 500 body under production, development, test or unset', 'KS-1341 part A: GET / and POST / never answer a 500 with the thrown text RED KS-1341 A1 POST /: the thrown message is not in the 500 body under production, development, test or unset', 'KS-1341 part A: GET / and POST / never answer a 500 with the thrown text RED KS-1341 A2 GET /: the thrown message is logged once, server-side, with this route named', 'KS-1341 part A: GET / and POST / never answer a 500 with the thrown text RED KS-1341 A2 POST /: the thrown message is logged once, server-side, with this route named']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=943 failed=0 | after: total=951 failed=0` · `NEW reds: []` [baseline_suite.json total=943 failed=0; after_suite.json total=951 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +193/-2 test=src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+20/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (+173/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `e080174c86c671349c508560744644fc0ef33388` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/input.json`. Brief (given by --brief; its `# ` heading names KS-1341): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1341/brief.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1341-A-r4/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -198,5 +198,5 @@
     res.json({ success: true, webhooks: rows });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook list failed (GET /api/webhooks)', err);
   }
 });
@@ -265,5 +265,5 @@
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook create failed (POST /api/webhooks)', err);
   }
 });
@@ -549,1 +549,19 @@
+/**
+ * KS-1341: the only place in this router that turns a caught error into a 500.
+ *
+ * Seven catch blocks above put the thrown error's own text in the 500 body with NO NODE_ENV
+ * guard, so it reached the client in every environment, production included (measured by the
+ * 2026-09-26 gate: DELETE /:id returned the thrown text, rotate-secret returned internal
+ * encryption-configuration text). Same helper as routes/gdpr.ts and routes/systemErrors.ts
+ * (KS-730): log the thrown text server-side with the route named, answer the constant body.
+ *
+ * Declared at the END of the file on purpose: a function declaration is hoisted, and the
+ * handlers above only call it at request time (deliverWebhook is called above its own
+ * declaration the same way). Placing it here leaves every line above it where it was.
+ */
+function fail500(res: Response, context: string, err: unknown): void {
+  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+}
+
 export default webhooksRouter;
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
@@ -0,0 +1,173 @@
+// KS-1341 part A (originate routes/webhooks.ts, GET / and POST /): seven catch blocks answered a 500
+// whose body carried the thrown error's own text, with NO NODE_ENV guard, so it reached the client in
+// every environment, production included (measured by the 2026-09-26 batch1280 gate). Part A adds the
+// file's fail500 helper and converts the first two sites; parts B and C convert the other five.
+// Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
+//
+// THE GET / TRAP. GET / chains .catch() onto its list query, so a REJECTED $queryRaw is swallowed into
+// a 200 with an empty list and never reaches the catch under test. The GET / cell therefore makes
+// $queryRaw THROW SYNCHRONOUSLY, and every red cell asserts the catch was REACHED (the logger received
+// this route's context with the thrown text), not only that the body is clean. control A0 pins the
+// swallowing branch so the trap cannot come back silently.
+const mockQueryRaw = jest.fn();
+const mockExecuteRaw = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: mockQueryRaw,
+    $executeRaw: mockExecuteRaw,
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
+import { webhooksRouter } from '../routes/webhooks';
+
+// THE FIXTURE IS LOAD-BEARING. It must not contain 'does not exist' (the KS-730 PR3 trap) and must
+// carry no Postgres SQLSTATE token that utils/pgErrors.ts would classify, so no benign or 4xx branch
+// can claim it. The last control below pins both properties.
+const LEAK = 'connect ECONNREFUSED 10.0.4.17:5432 ks1341a-private-detail';
+const NODE_ENVS = ['production', 'development', 'test', undefined];
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
+const CREATE_BODY = { url: 'https://partner.example.com/hooks', events: ['certification.issued'] };
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
+// Each route is driven by making ITS OWN db call throw, so a cell cannot pass because another
+// handler answered.
+const ROUTES = [
+  {
+    label: 'GET /',
+    method: 'GET',
+    body: undefined,
+    arm: () => mockQueryRaw.mockImplementationOnce(() => { throw new Error(LEAK); }),
+    context: 'Webhook list failed (GET /api/webhooks)',
+  },
+  {
+    label: 'POST /',
+    method: 'POST',
+    body: CREATE_BODY,
+    arm: () => mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK)),
+    context: 'Webhook create failed (POST /api/webhooks)',
+  },
+];
+
+async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  route.arm();
+  const res = await fetch(baseUrl + '/api/webhooks', {
+    method: route.method,
+    headers: { 'content-type': 'application/json' },
+    ...(route.body === undefined ? {} : { body: JSON.stringify(route.body) }),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-1341 part A: GET / and POST / never answer a 500 with the thrown text', () => {
+  it.each(ROUTES)('RED KS-1341 A1 $label: the thrown message is not in the 500 body under production, development, test or unset', async (route) => {
+    for (const nodeEnv of NODE_ENVS) {
+      const reply = await call(route, nodeEnv);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+      // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
+      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
+    }
+  });
+
+  it.each(ROUTES)('RED KS-1341 A2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
+    const reply = await call(route, 'production');
+    expect(reply.status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
+  });
+
+  it('control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch', async () => {
+    // PRE-EXISTING behaviour this change must NOT alter, and the reason the GET / cell throws
+    // synchronously: same route, same message, a rejected promise instead, a different answer.
+    setNodeEnv('production');
+    mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
+    const res = await fetch(baseUrl + '/api/webhooks');
+    expect(res.status).toBe(200);
+    expect(JSON.parse(await res.text())).toEqual({ success: true, webhooks: [] });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1341 A: a create that does NOT throw answers 201 and logs nothing', async () => {
+    // Without this, every "not leaked" pass above is consistent with the router answering 500 always.
+    setNodeEnv('production');
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    const res = await fetch(baseUrl + '/api/webhooks', {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify(CREATE_BODY),
+    });
+    expect(res.status).toBe(201);
+    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1341 A: an authored 400 keeps its own text and logs nothing', async () => {
+    // The risk of a blanket helper is that it swallows messages a route MEANT to return.
+    setNodeEnv('production');
+    const res = await fetch(baseUrl + '/api/webhooks', {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify({ url: 'https://partner.example.com/hooks' }),
+    });
+    expect(res.status).toBe(400);
+    expect(JSON.parse(await res.text()).error.message).toBe('url and events (array) are required');
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1341 A: the LEAK string is the thrown text and dodges every benign branch', () => {
+    // If LEAK were absent from the thrown error, every leaked: false above would hold trivially.
+    expect(new Error(LEAK).message).toBe(LEAK);
+    expect(LEAK.length).toBeGreaterThan(20);
+    expect(LEAK).not.toContain('does not exist');
+    expect(LEAK).not.toMatch(/\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/);
+  });
+});
```
