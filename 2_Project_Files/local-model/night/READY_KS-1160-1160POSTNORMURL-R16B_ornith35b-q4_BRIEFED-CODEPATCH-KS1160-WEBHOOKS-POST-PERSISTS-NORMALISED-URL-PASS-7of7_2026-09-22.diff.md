# READY — KS-1160-1160POSTNORMURL-R16B (Ornith, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1160-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 13:15 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1160-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1160-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed11-drafter-precheck/POSTNORMURL/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers differ (webhooks.ts: golden `@@ -255,4 +255,4 @@` vs run `@@ -255,4 +255,4 @@ webhooksRouter.post('/', async (req: Request, res: Response) => {`; webhooks.ts: golden `@@ -260,4 +260,4 @@` vs run `@@ -260,4 +260,4 @@ webhooksRouter.post('/', async (req: Request, res: Response) => {`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 13:15 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1160-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/webhooks.ts , Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/originate/src/routes/webhooks.ts
97	0	Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/webhooks.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts fails at the untouched tip (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1160 POST /api/webhooks: url normalisation persistence RED KS-1160 A: POST persists the guard NORMALISED url, not the raw request string', 'KS-1160 POST /api/webhooks: url normalisation persistence RED KS-1160 B: the 201 body echoes the normalised url']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=835 failed=0 | after: total=838 failed=0` · `NEW reds: []` [baseline_suite.json total=835 failed=0; after_suite.json total=838 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +99/-2 test=src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts` (+97/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1160-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1160-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -255,4 +255,4 @@ webhooksRouter.post('/', async (req: Request, res: Response) => {
     await runWithTenantId(tenantId, () => db.$executeRaw`
       INSERT INTO svc_webhooks (id, organization_id, tenant_id, url, secret_v2, events, description, is_active)
-      VALUES (${id}::uuid, ${userId}::uuid, ${tenantId}::uuid, ${url}, ${encrypted}, ${events}, ${description || null}, true)
+      VALUES (${id}::uuid, ${userId}::uuid, ${tenantId}::uuid, ${urlValidation.url}, ${encrypted}, ${events}, ${description || null}, true)
     `);
@@ -260,4 +260,4 @@ webhooksRouter.post('/', async (req: Request, res: Response) => {
     res.status(201).json({
       success: true,
-      webhook: { id, url, events, description, isActive: true },
+      webhook: { id, url: urlValidation.url, events, description, isActive: true },
       secret,
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts
@@ -0,0 +1,97 @@
+// KS-1160: POST /api/webhooks persists and echoes the RAW request url where PATCH persists the
+// SSRF guard's NORMALISED one. The create handler consults validateWebhookUrl (webhooks.ts:219)
+// and then DISCARDS its .url: :257 binds the raw url into the INSERT and :262 echoes it. The
+// harness mirrors ks444-webhooks-create-description-guard.test.ts with ONE change inside the
+// @secuura/shared mock: assertSafeOutboundUrl NORMALISES (trims), so the defect is observable.
+
+const mockExecuteRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: jest.fn(),
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
+    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw).trim() })),
+  }),
+);
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { webhooksRouter } from '../routes/webhooks';
+
+const shared = jest.requireMock('@secuura/shared') as { assertSafeOutboundUrl: jest.Mock };
+
+const app = express();
+app.use('/api/webhooks', express.json(), webhooksRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+
+afterAll(() => server?.close());
+beforeEach(() => {
+  mockExecuteRaw.mockReset();
+  shared.assertSafeOutboundUrl.mockClear();
+});
+
+function createWebhook(body: unknown): Promise<Response> {
+  return fetch(baseUrl + '/api/webhooks', {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+}
+
+const RAW = '  https://partner.example.com/hooks  ';
+const NORMALISED = 'https://partner.example.com/hooks';
+
+describe('KS-1160 POST /api/webhooks: url normalisation persistence', () => {
+  it('RED KS-1160 A: POST persists the guard NORMALISED url, not the raw request string', async () => {
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    const res = await createWebhook({ url: RAW, events: ['certification.issued'] });
+    expect(res.status).toBe(201);
+    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
+    const boundUrl = mockExecuteRaw.mock.calls[0][4];
+    expect(boundUrl).toBe(NORMALISED);
+  });
+
+  it('RED KS-1160 B: the 201 body echoes the normalised url', async () => {
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    const res = await createWebhook({ url: RAW, events: ['certification.issued'] });
+    expect(res.status).toBe(201);
+    const body = (await res.json()) as { webhook?: { url?: string } };
+    expect(body.webhook?.url).toBe(NORMALISED);
+  });
+
+  it('control: the guard is consulted once with the raw request url, before and after', async () => {
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    await createWebhook({ url: RAW, events: ['certification.issued'] });
+    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledTimes(1);
+    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledWith(RAW);
+  });
+});
```
