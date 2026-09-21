# READY — KS-1231-PARTA-R16 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 04:42 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed4-drafter-precheck/1231PARTA-R16/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:42 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `64ab105132eada0621622acf4d6053bc59926780`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/verification.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
196	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (24 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 24 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 24 line(s) byte-exact incl. leading whitespace (of 24; 24 line(s) added by the apply)` [a3i_indent.out: `OK 24 line(s) byte-exact incl. leading whitespace (of 24; 24 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1231 N-1 - a malformed integrations CONTAINER refuses the create (fail closed) RED KS-1231 - a non-array container (object, string, null) refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs', 'KS-1231 N-1 - a malformed integrations CONTAINER refuses the create (fail closed) RED KS-1231 - a non-object entry, a duplicate caller id or a non-object config refuses the typed and the untyped create: 403 FORBIDDEN, enforcement never runs']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=697 failed=0 | after: total=701 failed=0` · `NEW reds: []` [baseline_suite.json total=697 failed=0; after_suite.json total=701 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +220/-3 test=src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts` (+196/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `64ab105132eada0621622acf4d6053bc59926780` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1231-R16-PARTA-CREATEPATH.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
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
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts
@@ -0,0 +1,196 @@
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
