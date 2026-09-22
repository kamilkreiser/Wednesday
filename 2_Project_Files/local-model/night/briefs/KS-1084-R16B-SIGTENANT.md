# KS-1084 R16B-SIGTENANT (part A of 2, the READ site) - Wednesday's task for Ornith: `GET /api/signatories` in api-gateway `routes/proxy.ts` hand-builds its fetch to originate with `Authorization` only, so the caller's verified tenant (which `authenticateToken` has already written onto `req.headers['x-tenant-id']`, `middleware/auth.ts:418`) never reaches originate and single-tenant originate's KS-458 block scopes the read to `DEFAULT_TENANT_ID` - forward `x-tenant-id` on that ONE fetch (ONE product hunk at `proxy.ts:677`: one `-` line, four `+` lines) and pin it with ONE NEW vitest file that drives the real gateway app against a stub originate in-process (code_patch, VITEST). Tip: `3bad652d17cf111c1e2e1bed1ae7686894637487`. Written 2026-09-22 19:06:10 AEST by Wednesday's feed16 drafter.

**Kam chose c; Wednesday advised against (the 09-16 rule); the diff is HELD and GATED like every other Ornith output - it merges on nothing but a QA gate + a signed GO.** (Card `secuura-ks1084-gateway-originate-no-tenant-header-p0`, ruled 2026-09-22 18:11: option c "Let the local model attempt a fix unmeasured".) The ticket is P0 and marked "READ ONLY / unverified" since 2026-09-11; NOBODY has measured the cross-tenant effect on a two-tenant stack, and this brief does not either - it proves ONLY that the header the ticket says is missing IS missing at the tip and IS forwarded after the hunk. **NOT an auth/MFA/OAuth surface:** the change is a tenant-scoping header on an INTERNAL gateway->originate call inside `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:670-686`; `middleware/auth.ts` (which verifies the JWT and writes the header) is NOT touched; originate is NOT touched.

Tip: `3bad652d17cf111c1e2e1bed1ae7686894637487`
Runner: `vitest`

## Premises (measured by the feed16 drafter in a `git clone --shared` scratchpad clone at the tip; Wednesday re-derives before queueing)
- Ticket KS-1084 (Backlog, P0, assignee kamil.kreiser@secuura.ai, no PR attached; board read at boot, `fetch_tickets.log`): "api-gateway calls originate directly - outside `createProxyRoutes` - at several sites and sends only `Authorization`. With no `x-tenant-id`, originate's KS-458 block ... sets `req.tenantId` to `DEFAULT_TENANT_ID` in single-tenant mode, so those calls **may** read or write in the default tenant rather than the caller's." Fix shape (verbatim): "route gateway->originate calls through one helper that forwards the verified tenant". This part forwards it at the ONE read site the ticket lists first; the write site (`routes/batch.ts`, batch certify) is part B, a separate brief on a separate file.
- The site at the tip: `proxy.ts:670` `router.get('/api/signatories',`, `:671` `authenticateToken(true),`, `:674` `const originateUrl = services.originate?.url || 'http://originate:4000';`, `:676` the `fetch(` line, **`:677` `headers: { 'Authorization': req.headers.authorization || '' },` (the ONE `-` line; byte-unique in the file - the twin at `:700` reads `_req.headers...`)**, `:678` `});`. The sibling read site `:694-:709` (`/api/third-party-verifiers`) has the same defect and is NOT in this task (the commission scoped one read + one write).
- Where the tenant comes from, measured: `middleware/auth.ts:399` defaults a missing JWT tenant to `DEFAULT_TENANT_ID`; `:418` `if (decoded.tenantId) req.headers['x-tenant-id'] = decoded.tenantId;` writes the VERIFIED tenant onto the request before `next()` (`:423`), so at `:677` the header is already on `req.headers` - the hunk merely forwards it. `x-tenant-id` has 0 mentions in `proxy.ts` at the tip (control: `Authorization` 10); `verification.ts:1325` forwards it in exactly this shape for the documents POST (KS-39 #4) - the precedent the comment names.
- The test is a NEW vitest file in the shape of `src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts` (the reference: it boots the REAL gateway app from `../index` against a stub originate `http.createServer` on 127.0.0.1:0, with `../db` and `@secuura/shared`'s `isSessionActive` mocked, and records what originate received). This suite records `x-tenant-id` on `/api/signatories`. No database, no docker, no fixed port: the stub listens on port 0. Red at the tip BY ASSERTION: originate receives `x-tenant-id` = `none` (the stub's marker for an absent header) where the cell expects the caller's tenant.
- Every `+` line (product and test) is ASCII-only, backslash-free and carries NO double-quote character (asserted by the writer script); strings are single-quoted; no test title carries an apostrophe. The context line `:676` carries a backtick and a `$` - it is CONTEXT, copied byte for byte.
- Collision check (`union.log`): `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` is in NONE of the 21 round-19 PR heads' file sets (0 of 38 union paths; control `Blockchain/Dev/CONTRIBUTING.md` = 1); no `services/api-gateway/` path is in the union at all. Not a Claude-sent ticket. The `api-gateway` DIRECTORY was Seat C 19th's lane by FEED 12's note - Wednesday rules the lane at queue time.

## What is wrong (one paragraph)
`Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:670-686` serves `GET /api/signatories` by calling originate directly with `fetch`, sending `{ 'Authorization': req.headers.authorization || '' }` and nothing else. By the time the handler runs, `authenticateToken(true)` has verified the caller's JWT and written the verified tenant onto `req.headers['x-tenant-id']` (`middleware/auth.ts:418`) - but the hand-built fetch never copies it, so originate's KS-458 block sees no tenant header and, in single-tenant mode, scopes the read to `DEFAULT_TENANT_ID`: a caller in another tenant may get the default tenant's signatories. The fix forwards `x-tenant-id` when it is present, in the shape `verification.ts:1325` already uses. Nothing else changes: the `Authorization` forward, the query-string relay, the status relay and the 502 branch are untouched.

## The exact change - ONE EDIT in the product file (one hunk; copy the header)
E1 (hunk 1, header `@@ -674,7 +674,10 @@`) - the one `-` line is the tip's `:677`; the four `+` lines are two KS-1084 comment lines and the same `headers:` object split over two lines with the conditional `x-tenant-id` spread added. Leading context `:674-:676` (`const originateUrl`, `const qs`, the `fetch(` line - all three STAY), trailing context `:678-:680` (`});`, `const body`, `return res.status` - all STAY). Old side 7 lines, new side 10.
```
@@ -674,7 +674,10 @@
         const originateUrl = services.originate?.url || 'http://originate:4000';
         const qs = req.url.includes('?') ? req.url.slice(req.url.indexOf('?')) : '';
         const upstream = await fetch(`${originateUrl}/api/signatories${qs}`, {
-          headers: { 'Authorization': req.headers.authorization || '' },
+          // KS-1084: forward the tenant authenticateToken verified (it writes x-tenant-id onto req.headers,
+          // middleware/auth.ts) so single-tenant originate does not scope this read to DEFAULT_TENANT_ID.
+          headers: { 'Authorization': req.headers.authorization || '',
+            ...(req.headers['x-tenant-id'] ? { 'x-tenant-id': String(req.headers['x-tenant-id']) } : {}) },
         });
         const body = await upstream.json().catch(() => ({}));
         return res.status(upstream.status).json(body);
```
There are exactly 4 `+` lines in the product hunk; the `-` line is the tip's `:677` exactly; every context line keeps its leading space (`:674` has eight spaces at the tip, so its context line has nine). Do NOT touch `:674-:676` or `:678-:680` beyond copying them as context. Do NOT edit `:694-:709` (the third-party-verifiers twin) - it is part of the ticket but NOT of this task.

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:677` - **must change** - `          headers: { 'Authorization': req.headers.authorization || '' },` - becomes the four `+` lines above
* `:676` - (correct) `        const upstream = await fetch(`${originateUrl}/api/signatories${qs}`, {` - stays (context)
* `:678` - (correct) `        });` - stays (context)

## THIS IS VITEST
`repo.test_runner` begins with `vitest`. `describe/it/expect/beforeAll/afterAll/vi` are imported from `'vitest'`; the two `vi.mock` factories are copied from the reference; NO `jest.*`.

## The test - one NEW vitest file that drives the real gateway against a stub originate (the ks1238 shape)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1084-signatories-forwards-x-tenant-id.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1084-signatories-forwards-x-tenant-id.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 82), every line with a leading `+` (a blank line is a lone `+`). Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only.
```
+/**
+ * KS-1084 (part A, the READ site): GET /api/signatories (routes/proxy.ts) hand-builds its fetch to originate with
+ * Authorization only. authenticateToken has already written the caller verified tenant onto req.headers x-tenant-id
+ * (middleware/auth.ts), but the fetch never forwards it, so single-tenant originate scopes the read to
+ * DEFAULT_TENANT_ID. The stub originate below records what it received; the RED cell asserts x-tenant-id.
+ * Shape: ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts (real gateway app, stub upstream on port 0).
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'net';
+
+vi.mock('../db', async (orig) => {
+  const real = (await orig()) as Record<string, unknown>;
+  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
+});
+vi.mock('@secuura/shared', async (orig) => {
+  const real = (await orig()) as Record<string, unknown>;
+  return { ...real, isSessionActive: async (id: string) => (id === 'ks1084-live' ? true : null) };
+});
+
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
+const CALLER_TENANT = 'b1084000-0000-4000-8000-000000001084';
+const SIG = '/api/signatories';
+type Seen = { url: string; tenant: string; bearer: string };
+const seen: Seen[] = [];
+
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+}
+function userJwt(sessionId: string): string {
+  return 'Bearer ' + jwt.sign({ userId: 'u-ks1084', email: 'ks1084-user@secuura.io', role: 'user', verificationLevel: 'email', authMethod: 'email', tenantId: CALLER_TENANT, sessionId },
+    PRIV, { algorithm: 'RS256', expiresIn: '10m' });
+}
+
+let upstream: http.Server | undefined;
+let gateway: http.Server | undefined;
+let gatewayUrl = '';
+beforeAll(async () => {
+  upstream = http.createServer((req, res) => {
+    const url = req.url || '';
+    if (url.startsWith(SIG)) seen.push({ url, tenant: String(req.headers['x-tenant-id'] ?? 'none'), bearer: String(req.headers.authorization ?? 'none') });
+    res.writeHead(200, { 'content-type': 'application/json' });
+    res.end(JSON.stringify({ success: true, data: [] }));
+  });
+  const upstreamUrl = await listen(upstream);
+  for (const name of ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
+    'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET']) vi.stubEnv(name + '_SERVICE_URL', upstreamUrl);
+  vi.stubEnv('NODE_ENV', 'test');
+  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
+  delete process.env.JWT_JWKS_URL;
+  vi.resetModules();
+  const app = (await import('../index')).default;
+  gateway = http.createServer(app as http.RequestListener);
+  gatewayUrl = await listen(gateway);
+}, 60000);
+afterAll(async () => {
+  for (const s of [gateway, upstream]) if (s) { s.closeAllConnections(); await new Promise<void>((r) => s.close(() => r())); }
+  vi.unstubAllEnvs();
+});
+
+/** GET a path through the real gateway as a live user of CALLER_TENANT; returns the status and what originate recorded. */
+async function get(path: string): Promise<[number, Seen[]]> {
+  const before = seen.length;
+  const res = await fetch(gatewayUrl + path, { headers: { authorization: userJwt('ks1084-live') } });
+  await res.text();
+  return [res.status, seen.slice(before)];
+}
+describe('KS-1084 part A: GET /api/signatories forwards the caller verified tenant to originate', () => {
+  it('RED KS-1084 - originate receives x-tenant-id equal to the caller JWT tenant, not none', async () => {
+    const [status, recorded] = await get(SIG);
+    expect(status).toBe(200);
+    expect(recorded.map((h) => h.tenant)).toEqual([CALLER_TENANT]);
+  });
+  it('CONTROL - the caller Bearer still reaches originate and the query string is relayed', async () => {
+    const [status, recorded] = await get(SIG + '?limit=5');
+    expect(status).toBe(200);
+    expect(recorded.map((h) => h.url)).toEqual([SIG + '?limit=5']);
+    expect(recorded.map((h) => h.bearer.startsWith('Bearer '))).toEqual([true]);
+  });
+});
```
Cells: `RED KS-1084 - originate receives x-tenant-id equal to the caller JWT tenant, not none` (RED at the tip: `hits.map(tenant)` is `['none']`; GREEN after: `[CALLER_TENANT]`) and `CONTROL - the caller Bearer still reaches originate and the query string is relayed` (passes on both trees).

## Red cells
- RED KS-1084 - originate receives x-tenant-id equal to the caller JWT tenant, not none

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` (1 hunk, copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1084-signatories-forwards-x-tenant-id.test.ts` (one hunk, `@@ -0,0 +1,82 @@`, every line a `+`). No prose before or after the block.

## Notes for the raise (not for the model)
- HELD and GATED (Kam's c, Wednesday's advice against, above). This diff proves the header is forwarded; it does NOT prove originate honours it or that any cross-tenant read happened at the tip - that measurement (a two-tenant stack) is still owed before anyone calls the P0 closed. The raise text says so.
- Part B (the WRITE site, `routes/batch.ts` batch certify via `proxyRequest`) is a separate brief on a separate file; the remaining ticket sites (`third-party-verifiers` `:694-:709`, `verification.ts` `:142`/`:180` `GET /api/documents/:id` via `http.request`, `batch.ts:194` batch verify, `platform.ts:252` refresh-tenants) are NOT in this task. **Refs KS-1084, does not close it.**
