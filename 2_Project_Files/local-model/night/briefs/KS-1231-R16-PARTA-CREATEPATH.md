# KS-1231 R16-PARTA-CREATEPATH - Wednesday's task for Ornith, PART A of two: the CREATE path reads the integrations container FAIL CLOSED (code_patch, vitest, ONE NEW test file) at develop 64ab10513 (rewritten 04:23 after the first golden; written 04:20 on 2026-09-22 by Wednesday's feed4 drafter from services/api-gateway/src/routes/verification.ts:1200-1240 read at the tip and ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts, 292 lines read whole)
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the feed4 drafter at 04:20:56 AEST, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- Ticket KS-1231 (P2, Backlog, kamil.kreiser@secuura.ai, no PR attachment; #1035 gate N-1): "Read side, fail closed, in both readers: verification.ts:1212-1219 (the create path) and health.ts:45-52 (the info reader). For the calling connector, any of these should refuse instead of reading as no restriction: a non-array integrations; a non-object entry; a duplicate id; a non-object config." The ticket names TWO product files, so it is SPLIT: THIS PART edits ONLY `services/api-gateway/src/routes/verification.ts` (the create path). PART B (`KS-1231-R16-PARTB-INFOREADER.md`) edits ONLY `services/api-gateway/src/services/health.ts` (the info reader) with its own test file. Each part stands alone against the tip; this part MUST NOT touch health.ts, and the portal (`frontend/admin/src/pages/Settings.tsx`, the ticket's third item) is nobody's here.
- The ticket's line numbers hold at 64ab10513: the parse is `verification.ts:1212-1219`, inside the `if (connectorMeta)` block at :1202, after the scope check at :1207-1211 and before the KS-1204 allow-list VALUE check at :1220-1229.
- Fix shape, from the ticket's four refusals read against the file: `integrations` ABSENT (no key, or no platform-settings at all) stays no restriction - every existing suite that returns `null` or `{}` from getNotificationSettings depends on it; an explicit `null` is a non-array and refuses (the ticket lists `null` among the measured fail-open containers). "A duplicate id" is read as a SECOND entry carrying the CALLING connector id (the ticket's measured case `[{id, config: {}}, entry]` - first wins); an array-valued config counts as non-object. The `catch {}` stays: a Redis THROW is KS-1256's separate ticket, not this one. Refusal code and message shape mirror the KS-1204 refusal at :1226-1229 (403 FORBIDDEN, "refusing until it is corrected"). Wednesday may veto any of these readings.
- Red-first MEASURED in the clone: the test file alone at the tip -> 2 failed / 2 passed (both RED cells fail by assertion: the tip answers `201 past-enforcement, enforcement called 1` where `403 FORBIDDEN, 0` is expected; both controls green); with E1 applied -> 4/4 green. Log: `runs/2026-09-22_feed4-drafter-precheck/1231PARTA-R16/` (golden) and the drafter scratchpad `feed4/ks1231/redfirst_A.log`, `green_A.log`.
- Typecheck (the 16th round's per-file method, test file + product AFTER the patch): 0 errors in the file, 0 total; a planted TS2322 CAUGHT. First draft carried an unused `import http` (TS6133) - removed. Second draft FAILED its first golden at A4 with a LOAD error that was the checker's own `decl_splice` accommodation: the words `principal` (in a doc comment) and `originate` (an object key) matched two file-scope `let` declarations of the reference file, so the checker spliced `let principal = CONNECTOR;` above CONNECTOR's declaration (a TDZ ReferenceError). Fixed in the fence: the comment no longer says principal, and `const originate = { url: ... }` is declared at file scope and used as `{ originate, anchoring: originate }`. Golden re-run after that. Log: `runs/2026-09-22_feed4-drafter-precheck/typecheck/typecheck_feed4.log`.
- Every `+` line of both fences is ASCII-only, backslash-free and carries NO double-quote character (measured: 0 / 0 / 0 over 196 test lines and 29 product lines); no blank context line in the product hunk (it is a mixed hunk with `-` lines, so it applies STRICT).
- Collision check: no PR of the 16th round (Seat B: originate/shared/anchoring/security test files; Seat C: api-gateway ks864c/ks1123/ks1073/ks1185/ks1199/ks1204 test files + auth test files + scripts) touches verification.ts or creates this test file. The held READY `KS-1185-F1` (TIMEOUT-OVERRIDE-FALLBACK) edits verification.ts at OTHER lines (the workflow-approve forward, :700s) - disjoint hunks; the raise seat re-measures both orders.

## What is wrong (one paragraph)
`POST /api/documents` under a connector key (`services/api-gateway/src/routes/verification.ts`, the `if (connectorMeta)` block at :1202) reads the connector allow-list from the platform-settings `integrations` container at :1212-1219. The parse sits inside `try { ... } catch {}` and casts blindly: a non-array container (`{0: entry}` - what one ordinary admin Settings save stores - a string, `null`), a `null` entry (`.find` throws on `null.id`), a second entry with the same id (first wins, `config: {}`) or a string config all leave `connectorConfig = {}`, which reads as NO restriction, and the restricted connector creates any document type: 201, forwarded to originate. The fix is the read FAIL CLOSED: the same block now walks the container, sets `containerBad` on any of the four shapes, and refuses the create with 403 FORBIDDEN before the KS-1204 value check and before enforcement. NOT in this task: `services/health.ts` (PART B), the portal, the write side (KS-1230), a Redis throw (KS-1256).

## The exact change - ONE EDIT in the product file (one hunk: 3 lines of leading context :1210-1212, then the block :1213-1219 becomes 26 lines, then 3 lines of trailing context :1220-1222)
E1 - `services/api-gateway/src/routes/verification.ts`: lines 1216-1218 (the three `-` lines) are REPLACED and 21 lines are inserted around them (context: line 1212 is `        let connectorConfig: Record<string, unknown> = {};`, line 1219 is `        } catch {}`, line 1220 is the `// KS-1204 (#1014 gate N-2)` comment). The hunk header is `@@ -1210,13 +1210,34 @@` - copy it:
```
@@ -1210,13 +1210,34 @@
           return;
         }
         let connectorConfig: Record<string, unknown> = {};
+        // KS-1231 (#1035 gate N-1): the stored container is read FAIL CLOSED for the calling connector.
+        // A non-array integrations, a non-object entry, a second entry with this connector id, or a
+        // non-object config on this connector entry refuses the create instead of reading as no
+        // restriction (the parse used to leave connectorConfig = {} on any throw or miss).
+        let containerBad = false;
         try {
           const sRaw = await redisService.getNotificationSettings('platform-settings');
           const sAll = (sRaw || {}) as Record<string, unknown>;
-          const ints = ((sAll as any)?.integrations || []) as Array<Record<string, unknown>>;
-          const found = ints.find((i: any) => i.id === connectorMeta.connectorId);
-          if (found?.config) connectorConfig = found.config as Record<string, unknown>;
+          const ints: unknown = (sAll as any)?.integrations === undefined ? [] : (sAll as any).integrations;
+          if (!Array.isArray(ints)) {
+            containerBad = true;
+          } else {
+            let matched = 0;
+            for (const entry of ints) {
+              if (entry === null || typeof entry !== 'object' || Array.isArray(entry)) { containerBad = true; break; }
+              const e = entry as Record<string, unknown>;
+              if (e.id !== connectorMeta.connectorId) continue;
+              matched += 1;
+              const cfg = e.config;
+              if (matched > 1 || (cfg !== undefined && cfg !== null && (typeof cfg !== 'object' || Array.isArray(cfg)))) { containerBad = true; break; }
+              if (cfg) connectorConfig = cfg as Record<string, unknown>;
+            }
+          }
         } catch {}
+        if (containerBad) {
+          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector allow-list container is malformed; refusing until it is corrected' } });
+          return;
+        }
         // KS-1204 (#1014 gate N-2): the allow-list is stored by PUT /api/admin/settings,
         // which merges the body verbatim, so it is not guaranteed to be an array. Cast
         // to string[], a STRING made `.includes` a substring match ("SSD_DOCUMENT"
```
Eight-space indent on the `let` / `try` / `if (containerBad)` lines, ten inside `try`, twelve inside the `else`, fourteen inside the `for`. Copy every `+` line byte for byte; the three `-` lines are the tip's :1216-1218 exactly.

## The test - ONE NEW vitest file, in-process (the ks1204 harness, trimmed)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts`
This is the input's `suggested_test_file`. NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts` then ONE hunk `@@ -0,0 +1,196 @@`, every line `+`. Do NOT modify the reference test (`ks1204-...test.ts`) - it is Seat C 16th's file this round; copy its shape from this fence only. Every file-scope declaration the cells use is in the fence (catalogue, CONNECTOR, CONNECTOR_META, SSD_DOCUMENT, DOCUMENT_TYPE, RESTRICTED, stored, enforceSpy, workflowSpy, gateway, gatewayPort, realFetch, create).
```
+// =============================================================================
+// KS-1231 - a connector allow-list fails open when platform-settings integrations
+//           is not a clean array (#1035 gate N-1); the create path reads it FAIL CLOSED
+// =============================================================================
+//
+// POST /api/documents under a connector key reads the allow-list from the
+// platform-settings integrations container. The parse sat inside try/catch and
+// any throw or miss left connectorConfig = {} - no restriction. One ordinary
+// admin Settings save stores integrations as {0: entry}, so a restricted
+// connector became unrestricted. Now a non-array container, a non-object entry,
+// a second entry with the caller id, or a non-object config on the caller entry
+// refuses the create: 403 FORBIDDEN before enforcement. A clean array keeps the
+// KS-1204 behaviour, and an absent container is still no restriction.
+//
+// Harness: the ks1204 / ks1176 pattern - the real verification router and the
+// real enforceDocumentTypeRules over the seeded catalogue; the workflow gate is
+// a spy that answers 201 past-enforcement. The stored container is whatever the
+// cell put in `stored` (the settings object handed back by getNotificationSettings).
+// =============================================================================
+
+import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
+import express from 'express';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+const catalogue = vi.hoisted(() => ({ types: [] as Array<Record<string, unknown>> }));
+
+// enforceDocumentTypeRules resolves document types through this module directly.
+vi.mock('../services/redis', () => ({
+  getAllDocumentTypes: vi.fn(async () => catalogue.types),
+}));
+
+import { meetsVerificationLevel, enforceDocumentTypeRules } from '../services/enforcement';
+import { SEED_DOCUMENT_TYPES } from '../routes/admin';
+
+const CONTENT_HASH = 'c'.repeat(64);
+const CONNECTOR_ID = 'ks1231-c1';
+
+/** The user object authenticateToken builds for an sk_ key (middleware/auth.ts). */
+const CONNECTOR = {
+  userId: 'connector:ks1231-c1',
+  email: 'connector@secuura.io',
+  role: 'connector',
+  organizationId: 'org-1',
+  verificationLevel: 'api_key',
+  authMethod: 'api_key',
+  connectorId: CONNECTOR_ID,
+  rateLimit: 100,
+  rateLimitWindow: 60,
+  scopes: ['documents:write'],
+  tenantId: 't1',
+};
+const CONNECTOR_META = {
+  connectorId: CONNECTOR_ID,
+  scopes: ['documents:write'],
+  organizationId: 'org-1',
+  tenantId: 't1',
+  rateLimit: 100,
+  rateLimitWindow: 60,
+};
+
+const SSD_DOCUMENT = SEED_DOCUMENT_TYPES.find((dt) => (dt as { code?: string }).code === 'SSD_DOCUMENT') as Record<string, unknown>;
+const DOCUMENT_TYPE = SEED_DOCUMENT_TYPES.find((dt) => (dt as { code?: string }).code === 'DOCUMENT') as Record<string, unknown>;
+
+/** The restricted entry for the calling connector: SSD_DOCUMENT only. */
+const RESTRICTED = { id: CONNECTOR_ID, config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } };
+/** What getNotificationSettings hands back for the current cell (the whole platform-settings object, or null). */
+let stored: unknown = { integrations: [RESTRICTED] };
+
+const enforceSpy = vi.fn(enforceDocumentTypeRules);
+const workflowSpy = vi.fn(async () => ({ gated: true as const, response: { success: true, data: { ks1231: 'past-enforcement' } } }));
+
+let gateway: Server;
+let gatewayPort: number;
+const realFetch = globalThis.fetch;
+/** No upstream is ever reached: the workflow spy answers before the forward. */
+const originate = { url: 'http://127.0.0.1:1' };
+
+beforeAll(async () => {
+  catalogue.types = [SSD_DOCUMENT, DOCUMENT_TYPE];
+  // The verify route chain scan answers no live hit (never reached by these cells).
+  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
+
+  const { createVerificationRoutes } = await import('../routes/verification');
+  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
+
+  const app = express();
+  app.use(
+    createVerificationRoutes({
+      authenticateToken: () => (req, _res, next) => {
+        (req as { user?: unknown }).user = { ...CONNECTOR };
+        (req as { connectorMeta?: unknown }).connectorMeta = { ...CONNECTOR_META };
+        next();
+      },
+      mockBodyParser,
+      query: vi.fn(async () => ({ rows: [] })) as never,
+      isDbAvailable: () => false,
+      redisService: {
+        getPendingDocument: vi.fn(async () => null),
+        deletePendingDocument: vi.fn(async () => undefined),
+        getAllDocumentTypes: vi.fn(async () => catalogue.types),
+        getAllWorkflowInstances: vi.fn(async () => []),
+        // KS-1231: the route reads the allow-list container exactly as the admin write left it.
+        getNotificationSettings: vi.fn(async () => stored),
+        getRejectedDocument: vi.fn(async () => null),
+        setRejectedDocument: vi.fn(async () => undefined),
+        getWorkflowDocumentMapping: vi.fn(async () => null),
+        getWorkflowInstance: vi.fn(async () => null),
+        setWorkflowInstance: vi.fn(async () => undefined),
+      } as never,
+      services: { originate, anchoring: originate } as never,
+      log: () => undefined,
+      memWorkflowToDocumentMap: new Map(),
+      memRejectedDocuments: new Map(),
+      dbSaveRejection: vi.fn(async () => undefined),
+      ADMIN_ROLES: ['ADMIN', 'admin'],
+      enforceDocumentTypeRules: enforceSpy as never,
+      createWorkflowInstanceIfRequired: workflowSpy as never,
+      meetsVerificationLevel,
+    }),
+  );
+
+  gateway = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => gateway.once('listening', () => r()));
+  gatewayPort = (gateway.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  globalThis.fetch = realFetch;
+  await new Promise<void>((r) => gateway.close(() => r()));
+});
+
+afterEach(() => {
+  stored = { integrations: [RESTRICTED] };
+});
+
+/** POST /api/documents as the connector with the given body keys; returns status, error code and the enforcement call count. */
+async function create(body: Record<string, unknown>): Promise<[number, unknown, number]> {
+  enforceSpy.mockClear();
+  workflowSpy.mockClear();
+  const r = await realFetch('http://127.0.0.1:' + gatewayPort + '/api/documents', {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
+    body: JSON.stringify({ title: 'KS-1231', contentHash: CONTENT_HASH, ...body }),
+  });
+  const json = (await r.json()) as { error?: { code?: unknown }; data?: { ks1231?: unknown } };
+  return [r.status, json.error?.code ?? json.data?.ks1231, enforceSpy.mock.calls.length];
+}
+
+describe('KS-1231 N-1 - a malformed integrations CONTAINER refuses the create (fail closed)', () => {
+  const CONTAINERS: Array<[string, unknown]> = [
+    ['the object {0: entry} an admin Settings save stores', { integrations: { 0: RESTRICTED } }],
+    ['the string x', { integrations: 'x' }],
+    ['null', { integrations: null }],
+  ];
+
+  it('RED KS-1231 - a non-array container (object, string, null) refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs', async () => {
+    const answers: unknown[] = [];
+    for (const [label, value] of CONTAINERS) {
+      stored = value;
+      answers.push([label, await create({ documentType: 'DOCUMENT' }), await create({})]);
+    }
+    expect(answers).toEqual(CONTAINERS.map(([label]) => [label, [403, 'FORBIDDEN', 0], [403, 'FORBIDDEN', 0]]));
+  });
+
+  const ENTRIES: Array<[string, unknown[]]> = [
+    ['a null entry before the caller entry', [null, RESTRICTED]],
+    ['a second entry with the caller id (first wins today)', [{ id: CONNECTOR_ID, config: {} }, RESTRICTED]],
+    ['a string config on the caller entry', [{ id: CONNECTOR_ID, config: 'SSD_DOCUMENT' }]],
+  ];
+
+  it('RED KS-1231 - a non-object entry, a duplicate caller id or a non-object config refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs', async () => {
+    const answers: unknown[] = [];
+    for (const [label, integrations] of ENTRIES) {
+      stored = { integrations };
+      answers.push([label, await create({ documentType: 'DOCUMENT' }), await create({})]);
+    }
+    expect(answers).toEqual(ENTRIES.map(([label]) => [label, [403, 'FORBIDDEN', 0], [403, 'FORBIDDEN', 0]]));
+  });
+
+  it('control: a clean array [entry] still admits SSD_DOCUMENT and refuses DOCUMENT (KS-1204 unchanged)', async () => {
+    stored = { integrations: [RESTRICTED] };
+    expect([await create({ documentType: 'SSD_DOCUMENT' }), await create({ documentType: 'DOCUMENT' })])
+      .toEqual([[201, 'past-enforcement', 1], [403, 'FORBIDDEN', 0]]);
+  });
+
+  it('control: no platform-settings, no integrations key, or an entry for another connector only is still no restriction', async () => {
+    const answers: unknown[] = [];
+    for (const value of [null, {}, { integrations: [{ id: 'ks1231-other', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] }]) {
+      stored = value;
+      answers.push(await create({ documentType: 'DOCUMENT' }));
+    }
+    expect(answers).toEqual([[201, 'past-enforcement', 1], [201, 'past-enforcement', 1], [201, 'past-enforcement', 1]]);
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-1231 - a non-array container (object, string, null) refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs')` - three containers x typed/untyped. At the tip: `[201, 'past-enforcement', 1]` for all six (the red, by assertion); after E1: `[403, 'FORBIDDEN', 0]`.
- RED `it('RED KS-1231 - a non-object entry, a duplicate caller id or a non-object config refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs')` - three entry shapes x typed/untyped. At the tip 201 x6 (the red); after E1 403 x6.
- CONTROL `it('control: a clean array [entry] still admits SSD_DOCUMENT and refuses DOCUMENT (KS-1204 unchanged)')` - green on both trees.
- CONTROL `it('control: no platform-settings, no integrations key, or an entry for another connector only is still no restriction')` - green on both trees (`null`, `{}` and a foreign-id-only array all answer 201).

## Red cells
- RED KS-1231 - a non-array container (object, string, null) refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs
- RED KS-1231 - a non-object entry, a duplicate caller id or a non-object config refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:1216` - **must change**: `          const ints = ((sAll as any)?.integrations || []) as Array<Record<string, unknown>>;`
* `:1217` - **must change**: `          const found = ints.find((i: any) => i.id === connectorMeta.connectorId);`
* `:1218` - **must change**: `          if (found?.config) connectorConfig = found.config as Record<string, unknown>;`
* `:1212` - (correct) `        let connectorConfig: Record<string, unknown> = {};` - stays (the leading context)
* `:1219` - (correct) `        } catch {}` - stays (a Redis throw is KS-1256, not this task)
* `:1226` - (correct) `        if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) {` - the KS-1204 VALUE check; stays, now reached only through a clean container

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts` with the E1 hunk (header `@@ -1210,13 +1210,34 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts` with the one new-file hunk (header `@@ -0,0 +1,196 @@` - 196 is the count of `+` lines); no double quote, no `\$` / `\u` / backslash of any kind in a `+` line; blank context lines keep their leading space (the product hunk has none).
