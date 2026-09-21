# READY — KS-1231-PARTB-R16 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 04:43 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/api-gateway/src/services/health.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=0]` — STRICT APPLY NOT CLAIMED: the checker applied a rewritten/accommodated section (see section_<k>.opts) (apply with the options recorded in section_<k>.opts; the raise seat states which); CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed4-drafter-precheck/1231PARTB-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in health.ts (run 29 vs golden 28 body lines — context, since the change lines are equal) (identical in ks1231-info-reader-malformed-container-refused.test.ts); hunk headers differ (health.ts: golden `@@ -45,8 +45,25 @@` vs run `@@ -45,8 +45,25 @@ export function createHealthRoutes(`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 04:43 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `64ab105132eada0621622acf4d6053bc59926780`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/services/health.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
20	3	Blockchain/Dev/services/api-gateway/src/services/health.ts
108	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (20 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 20 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/services/health.ts byte-exact incl. leading whitespace (apply mode lenient): OK 20 line(s) byte-exact incl. leading whitespace (of 20; 20 line(s) added by the apply)` [a3i_indent.out: `OK 20 line(s) byte-exact incl. leading whitespace (of 20; 20 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/api-gateway/src/services/health.ts: hunk 1 (@@ -45,8 +45,25 @@ export function createHealthRoutes() declared old=8 new=25 but actual old=9 new=26`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/health.ts` (hunks=1, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-1231 N-1 - GET /api/connector/info refuses a malformed integrations CONTAINER (fail closed) RED KS-1231 - a non-array container, a non-object entry, a duplicate caller id or a non-object config answers 403 FORBIDDEN, not allowedDocumentTypes []']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=697 failed=0 | after: total=700 failed=0` · `NEW reds: []` [baseline_suite.json total=697 failed=0; after_suite.json total=700 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +128/-3 test=src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (+20/-3 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts` (+108/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `64ab105132eada0621622acf4d6053bc59926780` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night2/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1231-R16-PARTB-INFOREADER.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1231-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/services/health.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/health.ts
@@ -45,8 +45,25 @@ export function createHealthRoutes(
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
 
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts
@@ -0,0 +1,108 @@
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
