# READY — KS-1232-INFOEMPTY-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 00:02 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS.

**Held 00:02 2026-09-21 by the 23:4x Wednesday seat after a source read.** Tip `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`. Adds ONE cell to `api-gateway/src/__tests__/ks480-connector-auth.test.ts` pinning that GET /api/connector/info answers `allowedDocumentTypes: []` for a stored `""`, `0` or `false` (health.ts:58 `|| []`) — today's behaviour, pinned as a red-under-tamper cell. The ticket's raw-echo half and the MCP relays (tools/info.ts:144, http-server.ts:258) are NOT pinned by this cell (drafter's stated gap).

**Source read (Wednesday, same action):** 16 `+` lines, all 16 byte-present in `night/briefs/KS-1232-INFOEMPTY-1.md`; 0 `-`; one test file (T2); sibling KS-880 control 1/16. Model wall 13 s, first sample, round 1.

**Collision (measured by the drafter, stated here so nobody re-derives the stale flag):** the "health.ts carries unmerged READYs (KS-1248/KS-1258)" note was FALSE — all 7 of those READYs target `routes/system-status.ts`; every KS-1248/1258 commit is already in develop (#1039/#1044/#1053/#1068/#1077/#1085) and none touches health.ts (`git log` at the tip). No sequencing needed.

**Tampers (T6 each reds exactly the cell; T8 restored by bytes):** NULLISHRAW and NOTALIST, both on `health.ts:58` (`allowedDocumentTypes: connectorConfig.allowedDocumentTypes || [],` — byte-checked by Wednesday at the tip, count 1). Controls (full titles) at :72 and :121 green under both.

**Checker (00:01):** `RESULT: PASS (8/8)`; whole api-gateway suite with the cell 675/675 (drafter's precheck, `runs/2026-09-21_ks1232-drafter-precheck/full_suite.log`).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); api-gateway vitest 675 expected; `Refs KS-1232`. Partition: the ks480 test file is disjoint from every live seat's files. **Banked: FIVE for the next raise seat — KS-1234, KS-1279, KS-1223, KS-880, KS-1232.**

---
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-connector-auth.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-connector-auth.test.ts
@@ -135,1 +135,17 @@
+  it('RED KS-1232: GET /api/connector/info answers allowedDocumentTypes [] for a stored "", 0 or false - the three shapes every create refuses', async () => {
+    const META = { connectorId: 'platform-s:ext-1', scopes: ['documents:write'], organizationId: 'org-1', tenantId: 'ten-1', rateLimit: 100, rateLimitWindow: 60 };
+    apiKeyCache.set('sk_ks1232', { result: META, expiresAt: Date.now() + 60000 });
+    connectorBearerCache.set('sk_ks1232', { token: 'connector.jwt.token', expiresAt: Date.now() + 60000 });
+    const { createHealthRoutes } = await import('../services/health');
+    const answers: unknown[] = [];
+    for (const stored of ['', 0, false]) {
+      const redisLike = { getNotificationSettings: async () => ({ integrations: [{ id: META.connectorId, config: { allowedDocumentTypes: stored } }] }), getRedisClient: () => null };
+      const router = createHealthRoutes({}, redisLike as any);
+      const req = Object.assign(makeReq({ 'x-api-key': 'sk_ks1232' }), { method: 'GET', url: '/api/connector/info' });
+      const res: any = Object.assign(makeRes(), { setHeader: () => undefined });
+      const body = await new Promise<any>((resolve) => { res.json = (b: unknown) => { resolve(b); return res; }; router(req, res, () => resolve({ fellThrough: true })); });
+      answers.push([body.id, body.allowedDocumentTypes]);
+    }
+    expect(answers).toEqual([['platform-s:ext-1', []], ['platform-s:ext-1', []], ['platform-s:ext-1', []]]);
+  });
 });
