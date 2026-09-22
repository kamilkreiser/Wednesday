# KS-1160 R16B-POSTNORMURL - Wednesday's task for Ornith: `POST /api/webhooks` persists AND echoes the SSRF guard's NORMALISED url (`urlValidation.url`), exactly as PATCH already does - two one-token edits in `routes/webhooks.ts` plus a NEW jest suite (code_patch, JEST; re-brief of the STALE READY_KS-1160 at develop 8c2f7b3fd, written 12:44:53 AEST on 2026-09-22 by Wednesday's feed11 drafter from the file at the tip - `webhooks.ts` :167-:171, :212-:269, :290-:302 read; 550 lines; the reference test `ks444-webhooks-create-description-guard.test.ts` (imports `routes/webhooks`) present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `jest`

## Premises (measured by the feed11 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1160_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md` (Ornith PASS 7/7 first sample at develop 48e65c435; paths lacked the `Blockchain/Dev/` prefix). Same two edits here; the test rewritten under the `+`-line rule.
- The product at the tip is UNCHANGED since the old READY (offset 0): `:219` `    const urlValidation = await validateWebhookUrl(url);`, `:255` the `await runWithTenantId(tenantId, () => db.$executeRaw` line (ends with a backtick), `:256` the INSERT column list, `:257` the VALUES line binding `${url}`, `:258` the closing backtick-paren line, `:259` blank, `:260` `    res.status(201).json({`, `:261` `      success: true,`, `:262` `      webhook: { id, url, events, description, isActive: true },`, `:263` `      secret,`, `:264` the warning line (em-dash) - all byte-exact at 8c2f7b3fd. The PATCH path (`:296`-`:300`) already does `values.push(urlValidation.url)` - untouched.
- The old READY's test file is ABSENT at the tip (no `ks1160*` under `services/originate/src/__tests__/`). `webhooks.ts` is in Seat B's lane (originate) but NO round-18 PR and NO held R15/R16 READY touches it (seat_grep 0 / held_pool 0 on `webhooks.ts`, re-measured this feed). Ticket KS-1160: Backlog, not archived, no PR attached (board read at drafting time).
- `validateWebhookUrl` (`:167`-`:171`) returns `assertSafeOutboundUrl(raw)` from `@secuura/shared`, whose `.url` is the normalised form. The shared mock in the suite makes the guard TRIM so the defect is observable in-process (the ks444 driver's mock returned the raw string, which is why nothing caught this).
- The test is REWRITTEN so every `+` line is ASCII, backslash-free and double-quote-free: the old title's escaped apostrophe (`guard\'s`) is gone, the two template literals are concatenation, the red glyphs are ASCII `RED KS-1160 A/B` titles declared under `## Red cells`. The three `$queryRaw` / `$executeRaw` / `$executeRawUnsafe` keys are Prisma's own names (3 `+` lines carry `$`; unavoidable). Same three cells, same meaning.

## What is wrong (one paragraph)
`POST /api/webhooks` (`Blockchain/Dev/services/originate/src/routes/webhooks.ts:200`-`:269`) validates the request url through the SSRF guard (`:219` `const urlValidation = await validateWebhookUrl(url);`) and then DISCARDS the guard's normalised result: `:257` binds the RAW `${url}` into the INSERT and `:262` echoes the raw `url` in the 201 body, while `PATCH /:id` (`:296`-`:300`) persists `urlValidation.url`. Two rows for the same endpoint can therefore differ by whitespace/case/trailing-slash form depending on which verb wrote them, and the deliverer later calls the raw string the guard never approved as-is. Fix: on the POST path persist and echo `urlValidation.url` - two one-token edits. NOT in this task: `validateWebhookUrl`, the PATCH path, the KS-444 description guard (`:216`-`:218`), the events check, the secret.

## The exact change - TWO edits in `Blockchain/Dev/services/originate/src/routes/webhooks.ts`, each its own hunk (headers `@@ -255,4 +255,4 @@` and `@@ -260,4 +260,4 @@`); no blank context line anywhere
E1 - line 257 (the VALUES line): `${url}` becomes `${urlValidation.url}` (1 `-`, 1 `+`; leading context `:255`-`:256`, trailing context `:258` - the blank `:259` is NOT included):
```
@@ -255,4 +255,4 @@
     await runWithTenantId(tenantId, () => db.$executeRaw`
       INSERT INTO svc_webhooks (id, organization_id, tenant_id, url, secret_v2, events, description, is_active)
-      VALUES (${id}::uuid, ${userId}::uuid, ${tenantId}::uuid, ${url}, ${encrypted}, ${events}, ${description || null}, true)
+      VALUES (${id}::uuid, ${userId}::uuid, ${tenantId}::uuid, ${urlValidation.url}, ${encrypted}, ${events}, ${description || null}, true)
     `);
```
E2 - line 262 (the 201 body): the shorthand `url` becomes `url: urlValidation.url` (1 `-`, 1 `+`; leading context `:260`-`:261`, trailing context `:263` - the em-dash warning line `:264` is NOT included):
```
@@ -260,4 +260,4 @@
     res.status(201).json({
       success: true,
-      webhook: { id, url, events, description, isActive: true },
+      webhook: { id, url: urlValidation.url, events, description, isActive: true },
       secret,
```
Do not touch any other line. The `+` line of E1 carries `$` in its Prisma bindings exactly as the `-` line does (copy it, change only the one binding); `:255` and `:258` carry a backtick each and are context lines - copy them byte for byte with their leading space. Old sides 4 / 4 lines; new sides 4 / 4.

## THIS IS JEST, NOT VITEST
`repo.test_runner` begins with `jest` (ts-jest). `describe/it/expect/beforeAll/afterAll/beforeEach` are globals; `jest.fn` / `jest.mock` / `jest.requireMock` (auto-hoisted); NO `vi.*`, NO `import ... from 'vitest'`. The `@secuura/shared` mock goes through `./helpers/sharedModuleMock` exactly as the reference test does; `assertSafeOutboundUrl` MUST be in that factory (the ks927 note in the reference test).

## The test - one NEW jest file, the ks444 driver with a trimming guard mock
File: `Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 97), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only (the three Prisma `$...Raw` property names are the only `$`).
```
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
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-1160 A: POST persists the guard NORMALISED url, not the raw request string')` - at the tip the 5th binding of the INSERT (`mock.calls[0][4]`) is `RAW` (with its spaces), so `toBe(NORMALISED)` fails by assertion; after E1 it is the trimmed url.
- RED `it('RED KS-1160 B: the 201 body echoes the normalised url')` - at the tip `webhook.url` is `RAW`; after E2 it is `NORMALISED`.
- CONTROL `it('control: the guard is consulted once with the raw request url, before and after')` - `:219` is untouched on both trees.

## Red cells
- RED KS-1160 A: POST persists the guard NORMALISED url, not the raw request string
- RED KS-1160 B: the 201 body echoes the normalised url

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:257` - **must change**: the VALUES line of the INSERT, binding `${url}` - E1's `-` line (copied from the fence byte for byte)
* `:262` - **must change**: `      webhook: { id, url, events, description, isActive: true },` - E2's `-` line
* `:219` - (correct) `    const urlValidation = await validateWebhookUrl(url);` - stays (the guard call whose result the fix now uses)
* `:256` - (correct) the INSERT column list - stays (E1's leading context)
* `:261` - (correct) `      success: true,` - stays (E2's leading context)
* `:300` - (correct) the PATCH path's `values.push(urlValidation.url)` line - stays (the PATCH path that already persists the normalised url - the model for this fix)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts` (TWO hunks, headers `@@ -255,4 +255,4 @@` and `@@ -260,4 +260,4 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts` (one `@@ -0,0 +1,97 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
