# KS-1231 R16-PARTB-INFOREADER - Wednesday's task for Ornith, PART B of two: the INFO reader (GET /api/connector/info) reads the integrations container FAIL CLOSED (code_patch, vitest, ONE NEW test file) at develop 64ab10513 (written 04:28 on 2026-09-22 by Wednesday's feed4 drafter from services/api-gateway/src/services/health.ts:1-62 read at the tip and ks480-connector-auth.test.ts, 151 lines read whole)
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the feed4 drafter at 04:28:48 AEST, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- Ticket KS-1231 (P2, Backlog, kamil.kreiser@secuura.ai, no PR attachment; #1035 gate N-1): "Read side, fail closed, in both readers: verification.ts:1212-1219 (the create path) and health.ts:45-52 (the info reader)." The ticket names TWO product files, so it is SPLIT: THIS PART edits ONLY `services/api-gateway/src/services/health.ts` (the info reader). PART A (`KS-1231-R16-PARTA-CREATEPATH.md`) edits ONLY `services/api-gateway/src/routes/verification.ts` with its own test file (`ks1231-a-connector-allow-list-fails-open.test.ts`). Each part stands alone against the tip; this part MUST NOT touch verification.ts and MUST NOT create or touch Part A's test file.
- The ticket's line numbers hold at 64ab10513: the parse is `health.ts:45-52`, inside the `/api/connector/info` handler at :38, after the connector-role check at :40-43 and before the `res.json({` answer at :54.
- Fix shape: the SAME four refusals as Part A, the same reading (absent `integrations` stays no restriction; an explicit `null` is a non-array; "a duplicate id" = a SECOND entry carrying the CALLING connector id; an array-valued config is non-object), the same 403 FORBIDDEN refusal shape as the create path (KS-1204's message idiom). What "refuse" means for a GET: a 403 with the same body shape as the create path, so the connector is told the same thing on both routes - the drafter's reading of "for the calling connector, any of these should refuse"; Wednesday may veto. The refusal sits INSIDE the `try` (a `return` inside `try` is ordinary) so that line 52 - `} catch { /* swallow - non-critical */ }`, whose comment carries a NON-ASCII en dash at the tip - is a CONTEXT line, never a `-` or `+` line; the hunk has ONE trailing context line (that line), which is what strict `git apply` needs, and no leading context (line 44 is blank; a blank context line is refused by the builder). A Redis THROW still falls through to `{}` (KS-1256's ticket, not this one).
- Red-first MEASURED in the clone: the test file alone at the tip -> 1 failed / 2 passed (the RED cell fails by assertion: the tip answers `[0, []]` - `res.json` with no status call and `allowedDocumentTypes: []` - for all six malformed containers where `[403, 'FORBIDDEN']` is expected; both controls green); with E1 applied -> 3/3 green. Logs: the drafter scratchpad `feed4/ks1231/redfirst_B.log`, `green_B.log`; the golden under `runs/2026-09-22_feed4-drafter-precheck/1231PARTB-R16/`.
- Typecheck (the 16th round's per-file method, test file + product AFTER the patch): 0 errors IN THE FILE; the per-file program reports 4 errors ELSEWHERE (`auth.ts:321/362/400`, `health.ts:40`: `Property 'user' does not exist on type 'Request'`) that are the instrument's own incomplete program (the express `req.user` augmentation is not in a `files=[one test]` program) - REPRODUCED byte for byte on the tip's untouched `ks480-connector-auth.test.ts` through the same program (`feed4/logs/typecheck-tipcontrol-ks480.out`), and the golden's A7 (whole-service `tsc --noEmit`) is rc 0. A planted TS2322 CAUGHT.
- Every `+` line of both fences is ASCII-only, backslash-free and carries NO double-quote character (measured: 0 / 0 / 0 over 108 test lines and 20 product lines).
- The test file name is NOT the input's `suggested_test_file` (the builder derives the same slug for both parts from the ticket title, and Part A owns that name): this part's file is `ks1231-info-reader-malformed-container-refused.test.ts` - write that path in the `+++ b/` header, exactly as the `File:` line below spells it.
- Collision check: no PR of the 16th round touches health.ts or creates this test file (Seat C 16th touches api-gateway TEST files only: ks864c/ks1123/ks1073/ks1185/ks1199/ks1204). The reference `ks480-connector-auth.test.ts` is read-only here and is nobody's this round. Held READYs on health.ts: none at 64ab10513 (the KS-1232 INFOEMPTY READY's cell is already in the ks480 file at the tip, :134-150, and stays green: its containers are clean arrays with leaf values `''`, `0`, `false`).

## What is wrong (one paragraph)
`GET /api/connector/info` (`services/api-gateway/src/services/health.ts:38-62`) reads the calling connector's allow-list from the platform-settings `integrations` container at :45-52 with the same blind parse the create path had: a non-array container (`{0: entry}` - what one ordinary admin Settings save stores - a string, `null`), a `null` entry (`.find` throws), a second entry with the same id (first wins, `config: {}`) or a string config all leave `connectorConfig = {}`, and the route answers `allowedDocumentTypes: []` - telling a restricted connector it is unrestricted, silently. The fix is the read FAIL CLOSED: the same walk as Part A, ending in a 403 FORBIDDEN refusal inside the `try`, before the `res.json` at :54. NOT in this task: `routes/verification.ts` (PART A), the portal, the write side (KS-1230), a Redis throw (KS-1256).

## The exact change - ONE EDIT in the product file (one hunk: context :45, 4 inserted comment lines, context :46-48, the three `-` lines :49-51 replaced by 16 `+` lines, then ONE trailing context line :52)
E1 - `services/api-gateway/src/services/health.ts`: lines 49-51 (the three `-` lines) are REPLACED and 20 lines are inserted (4 comment lines after :45, 16 lines in place of :49-51). The hunk header is `@@ -45,8 +45,25 @@` - copy it. The last line of the hunk is the tip's line 52 as CONTEXT (one leading space, then the line exactly as `files[product_file]` has it - it carries a non-ASCII dash inside its comment; copy it from the file, never retype it):
```
@@ -45,8 +45,25 @@
     let connectorConfig: Record<string, unknown> = {};
+    // KS-1231 (#1035 gate N-1): the stored container is read FAIL CLOSED for the calling connector,
+    // the same rule as the create path. A non-array integrations, a non-object entry, a second entry
+    // with this connector id, or a non-object config on this connector entry refuses the read (403)
+    // instead of answering allowedDocumentTypes [] - which told the connector it was unrestricted.
     try {
       const settingsRaw = await redisService.getNotificationSettings('platform-settings');
       const settings = (settingsRaw || {}) as Record<string, unknown>;
-      const integrations = ((settings as any)?.integrations || []) as Array<Record<string, unknown>>;
-      const found = integrations.find((i: any) => i.id === meta.connectorId);
-      if (found?.config) connectorConfig = found.config as Record<string, unknown>;
+      const ints: unknown = (settings as any)?.integrations === undefined ? [] : (settings as any).integrations;
+      let containerBad = !Array.isArray(ints);
+      let matched = 0;
+      for (const entry of Array.isArray(ints) ? ints : []) {
+        if (entry === null || typeof entry !== 'object' || Array.isArray(entry)) { containerBad = true; break; }
+        const e = entry as Record<string, unknown>;
+        if (e.id !== meta.connectorId) continue;
+        matched += 1;
+        const cfg = e.config;
+        if (matched > 1 || (cfg !== undefined && cfg !== null && (typeof cfg !== 'object' || Array.isArray(cfg)))) { containerBad = true; break; }
+        if (cfg) connectorConfig = cfg as Record<string, unknown>;
+      }
+      if (containerBad) {
+        res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector allow-list container is malformed; refusing until it is corrected' } });
+        return;
+      }
     } catch { /* swallow – non-critical */ }
```
Four-space indent on `let` / `try`, six inside `try`, eight inside the `for` and the `if (containerBad)` block, ten inside the refusal. Copy every `+` line byte for byte; the three `-` lines are the tip's :49-51 exactly.

## The test - ONE NEW vitest file, in-process (the ks480 KS-1232 cell's harness, as its own file)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts`
This path is NOT the input's `suggested_test_file` - use THIS path (Part A owns the suggested name). NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts` then ONE hunk `@@ -0,0 +1,108 @@`, every line `+`. Do NOT modify the reference test (`ks480-connector-auth.test.ts`); copy its shape from this fence only. Every file-scope declaration the cells use is in the fence (fetchMock, CONNECTOR_ID, META, RESTRICTED, stored, router, makeReq, makeRes, info).
```
+// =============================================================================
+// KS-1231 - a connector allow-list fails open when platform-settings integrations
+//           is not a clean array (#1035 gate N-1); the INFO reader reads it FAIL CLOSED
+// =============================================================================
+//
+// GET /api/connector/info (services/health.ts) reads the allow-list from the
+// platform-settings integrations container with the same blind parse the create
+// path had: a non-array container, a null entry, a second entry with the caller
+// id or a string config all left connectorConfig = {} and the route answered
+// allowedDocumentTypes [] - telling a restricted connector it was unrestricted.
+// Now those shapes refuse the read: 403 FORBIDDEN. A clean array still answers
+// the stored list, and an absent container is still [].
+//
+// Harness: the ks480-connector-auth pattern - the real authenticateToken(true)
+// with the sk_ key pre-seeded in apiKeyCache / connectorBearerCache (no fetch),
+// the real createHealthRoutes over a redis-like object whose
+// getNotificationSettings answers whatever the cell put in `stored`.
+// =============================================================================
+
+import { describe, it, expect, vi, beforeAll } from 'vitest';
+import type { Request, Response, Router } from 'express';
+import { apiKeyCache, connectorBearerCache } from '../middleware/auth';
+
+const fetchMock = vi.fn();
+vi.stubGlobal('fetch', fetchMock);
+
+const CONNECTOR_ID = 'ks1231-c1';
+const META = { connectorId: CONNECTOR_ID, scopes: ['documents:write'], organizationId: 'org-1', tenantId: 'ten-1', rateLimit: 100, rateLimitWindow: 60 };
+/** The restricted entry for the calling connector: SSD_DOCUMENT only. */
+const RESTRICTED = { id: CONNECTOR_ID, config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } };
+/** What getNotificationSettings hands back for the current cell (the whole platform-settings object, or null). */
+let stored: unknown = { integrations: [RESTRICTED] };
+
+let router: Router;
+
+function makeReq(headers: Record<string, string>): Request {
+  return {
+    headers,
+    method: 'GET',
+    url: '/api/connector/info',
+    get: function (name: string) {
+      return (this as any).headers[name?.toLowerCase()];
+    },
+  } as unknown as Request;
+}
+
+function makeRes(): Response & { _status: number } {
+  const res: any = {
+    _status: 0,
+    status(code: number) { res._status = code; return res; },
+    json(body: unknown) { return body; },
+    setHeader() { return res; },
+  };
+  return res;
+}
+
+beforeAll(async () => {
+  apiKeyCache.set('sk_ks1231', { result: META, expiresAt: Date.now() + 60000 });
+  connectorBearerCache.set('sk_ks1231', { token: 'connector.jwt.token', expiresAt: Date.now() + 60000 });
+  const { createHealthRoutes } = await import('../services/health');
+  const redisLike = { getNotificationSettings: async () => stored, getRedisClient: () => null };
+  router = createHealthRoutes({}, redisLike as any);
+});
+
+/** GET /api/connector/info as the connector; answers [status (0 = res.json without a status call), allowedDocumentTypes or the error code]. */
+async function info(): Promise<[number, unknown]> {
+  const req = makeReq({ 'x-api-key': 'sk_ks1231' });
+  const res = makeRes();
+  const body = await new Promise<any>((resolve) => {
+    res.json = (b: unknown) => { resolve(b); return res; };
+    router(req, res, () => resolve({ fellThrough: true }));
+  });
+  return [res._status, body?.allowedDocumentTypes ?? body?.error?.code ?? body];
+}
+
+describe('KS-1231 N-1 - GET /api/connector/info refuses a malformed integrations CONTAINER (fail closed)', () => {
+  const MALFORMED: Array<[string, unknown]> = [
+    ['the object {0: entry} an admin Settings save stores', { integrations: { 0: RESTRICTED } }],
+    ['the string x', { integrations: 'x' }],
+    ['null', { integrations: null }],
+    ['a null entry before the caller entry', { integrations: [null, RESTRICTED] }],
+    ['a second entry with the caller id (first wins today)', { integrations: [{ id: CONNECTOR_ID, config: {} }, RESTRICTED] }],
+    ['a string config on the caller entry', { integrations: [{ id: CONNECTOR_ID, config: 'SSD_DOCUMENT' }] }],
+  ];
+
+  it('RED KS-1231 - a non-array container, a non-object entry, a duplicate caller id or a non-object config answers 403 FORBIDDEN, not allowedDocumentTypes []', async () => {
+    const answers: unknown[] = [];
+    for (const [label, value] of MALFORMED) {
+      stored = value;
+      answers.push([label, await info()]);
+    }
+    expect(answers).toEqual(MALFORMED.map(([label]) => [label, [403, 'FORBIDDEN']]));
+  });
+
+  it('control: a clean array [entry] still answers the stored allow-list', async () => {
+    stored = { integrations: [RESTRICTED] };
+    expect(await info()).toEqual([0, ['SSD_DOCUMENT']]);
+  });
+
+  it('control: no platform-settings, no integrations key, or an entry for another connector only still answers []', async () => {
+    const answers: unknown[] = [];
+    for (const value of [null, {}, { integrations: [{ id: 'ks1231-other', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] }]) {
+      stored = value;
+      answers.push(await info());
+    }
+    expect(answers).toEqual([[0, []], [0, []], [0, []]]);
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-1231 - a non-array container, a non-object entry, a duplicate caller id or a non-object config answers 403 FORBIDDEN, not allowedDocumentTypes []')` - six malformed containers. At the tip: `[0, []]` for all six (the red, by assertion); after E1: `[403, 'FORBIDDEN']`.
- CONTROL `it('control: a clean array [entry] still answers the stored allow-list')` - `[0, ['SSD_DOCUMENT']]` on both trees.
- CONTROL `it('control: no platform-settings, no integrations key, or an entry for another connector only still answers []')` - `[0, []]` x3 on both trees.

## Red cells
- RED KS-1231 - a non-array container, a non-object entry, a duplicate caller id or a non-object config answers 403 FORBIDDEN, not allowedDocumentTypes []

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:49` - **must change**: `      const integrations = ((settings as any)?.integrations || []) as Array<Record<string, unknown>>;`
* `:50` - **must change**: `      const found = integrations.find((i: any) => i.id === meta.connectorId);`
* `:51` - **must change**: `      if (found?.config) connectorConfig = found.config as Record<string, unknown>;`
* `:45` - (correct) `    let connectorConfig: Record<string, unknown> = {};` - stays (the leading context)
* `:52` - (correct) the `} catch { ... }` line - stays as the ONE trailing context line (its comment carries a non-ASCII dash: copy it from the file)
* `:54` - (correct) `    res.json({` - stays; reached only through a clean container after E1

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/services/health.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/services/health.ts` with the E1 hunk (header `@@ -45,8 +45,25 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts` with the one new-file hunk (header `@@ -0,0 +1,108 @@` - 108 is the count of `+` lines); no double quote, no `\$` / `\u` / backslash of any kind in a `+` line; the one context line of the product hunk keeps its leading space.
