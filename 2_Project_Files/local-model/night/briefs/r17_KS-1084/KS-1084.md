# KS-1084 R17-TPVTENANT (part C, the SECOND read site) - Wednesday's task for Ornith: `GET /api/third-party-verifiers` in api-gateway `routes/proxy.ts` hand-builds its fetch to originate with `Authorization` only, so the caller's verified tenant (which `authenticateToken` has already written onto `_req.headers['x-tenant-id']`, `middleware/auth.ts:418`) never reaches originate and single-tenant originate's KS-458 block scopes the read to `DEFAULT_TENANT_ID` - forward `x-tenant-id` on that ONE fetch (ONE product hunk at `proxy.ts:700`: one `-` line, four `+` lines - the SAME shape as part A's hunk at `:677`, held as READY_KS-1084-1084SIGTENANT-R16B) and pin it with ONE NEW vitest file that drives the real gateway app against a stub originate in-process (code_patch, VITEST). Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`. Written 2026-09-22 19:44:10 AEST by Wednesday's feed17 drafter.

**Kam chose c; Wednesday advised against (the 09-16 rule); the diff is HELD and GATED like every other Ornith output - it merges on nothing but a QA gate + a signed GO.** (Card `secuura-ks1084-gateway-originate-no-tenant-header-p0`, ruled 2026-09-22 18:11: option c "Let the local model attempt a fix unmeasured".) The ticket is P0 and marked "READ ONLY / unverified" since 2026-09-11; NOBODY has measured the cross-tenant effect on a two-tenant stack, and this brief does not either - it proves ONLY that the header the ticket says is missing IS missing at the tip and IS forwarded after the hunk. **NOT an auth/MFA/OAuth surface:** the change is a tenant-scoping header on an INTERNAL gateway->originate call inside `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:694-709`; `middleware/auth.ts` (which verifies the JWT and writes the header) is NOT touched; originate is NOT touched.

Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`
Runner: `vitest`

## Premises (measured by the feed17 drafter in a `git clone --shared` scratchpad clone at the tip; Wednesday re-derives before queueing)
- Ticket KS-1084 (Backlog, P0, assignee kamil.kreiser@secuura.ai, no PR attached; board read at boot, `fetch_tickets.log`): "api-gateway calls originate directly - outside `createProxyRoutes` - at several sites and sends only `Authorization`. With no `x-tenant-id`, originate's KS-458 block ... sets `req.tenantId` to `DEFAULT_TENANT_ID` in single-tenant mode, so those calls **may** read or write in the default tenant rather than the caller's." Fix shape (verbatim): "route gateway->originate calls through one helper that forwards the verified tenant". Part A (`/api/signatories`, `:677`) is a HELD READY diff; this part C forwards it at the ticket's SECOND read site, in the same one-line shape. The two hunks are region-disjoint (part A `:674-:680`; this one `:697-:703`) - if part A merges first this hunk re-anchors by +3 (the checker's reanchor path or a rebuild).
- The site at the tip: `proxy.ts:694` `router.get('/api/third-party-verifiers',`, `:695` `authenticateToken(true),`, `:696` `(async (_req: Request, res: Response) => {` (the request is named `_req` here - the `+` lines use `_req`), `:698` `const originateUrl = services.originate?.url || 'http://originate:4000';`, `:699` the `fetch(` line, **`:700` `headers: { 'Authorization': _req.headers.authorization || '' },` (the ONE `-` line; byte-unique in the file - the twin at `:677` reads `req.headers...`)**, `:701` `});`. This route relays NO query string (the fetch path is fixed).
- Where the tenant comes from, measured: `middleware/auth.ts:399` defaults a missing JWT tenant to `DEFAULT_TENANT_ID`; `:418` `if (decoded.tenantId) req.headers['x-tenant-id'] = decoded.tenantId;` writes the VERIFIED tenant onto the request before `next()` (`:423`), so at `:700` the header is already on `_req.headers` - the hunk merely forwards it. `x-tenant-id` has 0 mentions in `proxy.ts` at the tip (control: `Authorization` 7); `verification.ts:1325` forwards it in exactly this shape for the documents POST (KS-39 #4) - the precedent the comment names. `proxy.ts` is unchanged since `581c9db0d` (#1019); the round-19 merges (21 commits over 3bad652d1) did not touch it.
- The test is a NEW vitest file in the shape of `src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts` (the reference: it boots the REAL gateway app from `../index` against a stub originate `http.createServer` on 127.0.0.1:0, with `../db` and `@secuura/shared`'s `isSessionActive` mocked, and records what originate received). This suite records `x-tenant-id` on `/api/third-party-verifiers`. No database, no docker, no fixed port: the stub listens on port 0. Red at the tip BY ASSERTION: originate receives `x-tenant-id` = `none` (the stub's marker for an absent header) where the cell expects the caller's tenant.
- Every `+` line (product and test) is ASCII-only, backslash-free and carries NO double-quote character (asserted by the writer script); strings are single-quoted; no test title carries an apostrophe. The context line `:699` carries a backtick and a `$` - it is CONTEXT, copied byte for byte.
- Collision check: `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` was in NONE of the 21 round-19 heads (FEED 16 `union.log`, 0 of 38) and those 21 are now MERGED at this tip; the only other pending hunk on this file is part A's, region-disjoint (above). Not a Claude-sent ticket. The `api-gateway` DIRECTORY lane is Wednesday's ruling at queue time.

## What is wrong (one paragraph)
`Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:694-709` serves `GET /api/third-party-verifiers` by calling originate directly with `fetch`, sending `{ 'Authorization': _req.headers.authorization || '' }` and nothing else. By the time the handler runs, `authenticateToken(true)` has verified the caller's JWT and written the verified tenant onto `_req.headers['x-tenant-id']` (`middleware/auth.ts:418`) - but the hand-built fetch never copies it, so originate's KS-458 block sees no tenant header and, in single-tenant mode, scopes the read to `DEFAULT_TENANT_ID`: a caller in another tenant may get the default tenant's third-party verifiers. The fix forwards `x-tenant-id` when it is present, in the shape `verification.ts:1325` already uses and part A uses at `:677`. Nothing else changes: the `Authorization` forward, the status relay and the 502 branch are untouched.

## The exact change - ONE EDIT in the product file (one hunk; copy the header)
E1 (hunk 1, header `@@ -697,7 +697,10 @@`) - the one `-` line is the tip's `:700`; the four `+` lines are two KS-1084 comment lines and the same `headers:` object split over two lines with the conditional `x-tenant-id` spread added (reading `_req`, the name this handler binds). Leading context `:697-:699` (`try {`, `const originateUrl`, the `fetch(` line - all three STAY), trailing context `:701-:703` (`});`, `const body`, `return res.status` - all STAY). Old side 7 lines, new side 10.
```
@@ -697,7 +697,10 @@
       try {
         const originateUrl = services.originate?.url || 'http://originate:4000';
         const upstream = await fetch(`${originateUrl}/api/third-party-verifiers`, {
-          headers: { 'Authorization': _req.headers.authorization || '' },
+          // KS-1084: forward the tenant authenticateToken verified (it writes x-tenant-id onto req.headers,
+          // middleware/auth.ts) so single-tenant originate does not scope this read to DEFAULT_TENANT_ID.
+          headers: { 'Authorization': _req.headers.authorization || '',
+            ...(_req.headers['x-tenant-id'] ? { 'x-tenant-id': String(_req.headers['x-tenant-id']) } : {}) },
         });
         const body = await upstream.json().catch(() => ({}));
         return res.status(upstream.status).json(body);
```
There are exactly 4 `+` lines in the product hunk; the `-` line is the tip's `:700` exactly; every context line keeps its leading space (`:697` has six spaces at the tip, so its context line has seven). Do NOT touch `:697-:699` or `:701-:703` beyond copying them as context. Do NOT edit `:670-:686` (the signatories twin, part A) - it is a separate held diff, NOT part of this task.

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:700` - **must change** - `          headers: { 'Authorization': _req.headers.authorization || '' },` - becomes the four `+` lines above
* `:699` - (correct) `        const upstream = await fetch(`${originateUrl}/api/third-party-verifiers`, {` - stays (context)
* `:701` - (correct) `        });` - stays (context)

## THIS IS VITEST
`repo.test_runner` begins with `vitest`. `describe/it/expect/beforeAll/afterAll/vi` are imported from `'vitest'`; the two `vi.mock` factories are copied from the reference; NO `jest.*`.

## The test - one NEW vitest file that drives the real gateway against a stub originate (the ks1238 shape)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1084-third-party-verifiers-forwards-x-tenant-id.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1084-third-party-verifiers-forwards-x-tenant-id.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 82), every line with a leading `+` (a blank line is a lone `+`). Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only.
```
+/**
+ * KS-1084 (part C, the second READ site): GET /api/third-party-verifiers (routes/proxy.ts) hand-builds its fetch to
+ * originate with Authorization only. authenticateToken has already written the caller verified tenant onto
+ * req.headers x-tenant-id (middleware/auth.ts), but the fetch never forwards it, so single-tenant originate scopes
+ * the read to DEFAULT_TENANT_ID. The stub originate below records what it received; the RED cell asserts x-tenant-id.
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
+  return { ...real, isSessionActive: async (id: string) => (id === 'ks1084c-live' ? true : null) };
+});
+
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
+const CALLER_TENANT = 'c1084000-0000-4000-8000-000000001084';
+const TPV = '/api/third-party-verifiers';
+type Seen = { url: string; tenant: string; bearer: string };
+const seen: Seen[] = [];
+
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+}
+function userJwt(sessionId: string): string {
+  return 'Bearer ' + jwt.sign({ userId: 'u-ks1084c', email: 'ks1084c-user@secuura.io', role: 'user', verificationLevel: 'email', authMethod: 'email', tenantId: CALLER_TENANT, sessionId },
+    PRIV, { algorithm: 'RS256', expiresIn: '10m' });
+}
+
+let upstream: http.Server | undefined;
+let gateway: http.Server | undefined;
+let gatewayUrl = '';
+beforeAll(async () => {
+  upstream = http.createServer((req, res) => {
+    const url = req.url || '';
+    if (url.startsWith(TPV)) seen.push({ url, tenant: String(req.headers['x-tenant-id'] ?? 'none'), bearer: String(req.headers.authorization ?? 'none') });
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
+  const res = await fetch(gatewayUrl + path, { headers: { authorization: userJwt('ks1084c-live') } });
+  await res.text();
+  return [res.status, seen.slice(before)];
+}
+describe('KS-1084 part C: GET /api/third-party-verifiers forwards the caller verified tenant to originate', () => {
+  it('RED KS-1084 - originate receives x-tenant-id equal to the caller JWT tenant, not none', async () => {
+    const [status, recorded] = await get(TPV);
+    expect(status).toBe(200);
+    expect(recorded.map((h) => h.tenant)).toEqual([CALLER_TENANT]);
+  });
+  it('CONTROL - the caller Bearer still reaches originate on the fixed upstream path', async () => {
+    const [status, recorded] = await get(TPV);
+    expect(status).toBe(200);
+    expect(recorded.map((h) => h.url)).toEqual([TPV]);
+    expect(recorded.map((h) => h.bearer.startsWith('Bearer '))).toEqual([true]);
+  });
+});
```
Cells: `RED KS-1084 - originate receives x-tenant-id equal to the caller JWT tenant, not none` (RED at the tip: `recorded.map(tenant)` is `['none']`; GREEN after: `[CALLER_TENANT]`) and `CONTROL - the caller Bearer still reaches originate on the fixed upstream path` (passes on both trees).

## Red cells
- RED KS-1084 - originate receives x-tenant-id equal to the caller JWT tenant, not none

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` (1 hunk, copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1084-third-party-verifiers-forwards-x-tenant-id.test.ts` (one hunk, `@@ -0,0 +1,82 @@`, every line a `+`). No prose before or after the block.

## Notes for the raise (not for the model)
- HELD and GATED (Kam's c, Wednesday's advice against, above). This diff proves the header is forwarded; it does NOT prove originate honours it or that any cross-tenant read happened at the tip - that measurement (a two-tenant stack) is still owed before anyone calls the P0 closed. The raise text says so.
- Part A (`/api/signatories`, `:677`) is the held READY_KS-1084-1084SIGTENANT-R16B diff (hunk `@@ -674,7 +674,10 @@`); this part C's hunk `@@ -697,7 +697,10 @@` is region-disjoint from it. Part B (the WRITE site, `routes/batch.ts`) is TABLED by Kam's card; the remaining ticket sites (`verification.ts` `:142`/`:180` `GET /api/documents/:id` via `http.request`, `platform.ts:252` refresh-tenants) are NOT in this task. **Refs KS-1084, does not close it.**
