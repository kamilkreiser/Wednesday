# READY — KS-1238-N83-2 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1238-ornith35b-night/out.md.checker/patch.diff`** (from `ls`, 00:06).

**Held 00:06 2026-09-20 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `4273adfac`. POST /api/documents (verification.ts:1297) with a documents:write key + REVOKED JWT, exchange refused, reaches originate with no Bearer (N83-2). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control mostly absent. Both-order collision proofs against held N90-1 (ks1238 file) / N91-1 (ks1215 file) are in the brief. Source: the #1084-#1091 gate's NOT-PINNED rows. Raise: Refs KS-1238, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[RAW1297] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts mode=modify runner=vitest cells=10 tampers=1 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts
@@ -26,1 +26,2 @@
+const CREATE_KEY = 'sk_ks1238_create_401_00001';
 const SIG = '/api/signatories';
@@ -60,1 +61,2 @@
+      if (key === CREATE_KEY) return json(200, { data: { valid: true, connectorId: 'ks1238-create', scopes: ['documents:write'], organizationId: 'org-ks1238', tenantId: TENANT, rateLimit: 1000, rateLimitWindow: 60 } });
       return json(200, key === OK_KEY || key === REFUSED_KEY
@@ -69,1 +71,2 @@
+    if (req.method === 'POST' && url === '/api/documents') hits.push(bearerOf(req.headers.authorization as string | undefined));
     if (url.startsWith(SIG) || url.startsWith(TPV) || url.startsWith(DOCS) || url.startsWith('/api/anchors/')) hits.push(bearerOf(req.headers.authorization as string | undefined));
@@ -129,1 +132,7 @@
+  it('RED documents (create): a valid key + a REVOKED session JWT, exchange refused, reaches originate with no Bearer', async () => {
+    const createMark = hits.length;
+    const created = await fetch(gatewayUrl + '/api/documents', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': CREATE_KEY, authorization: userJwt('ks1238-revoked') }, body: JSON.stringify({ title: 'ks1238', contentHash: 'a'.repeat(64) }) });
+    await created.text();
+    expect([created.status, hits.slice(createMark)]).toEqual([200, ['none']]);
+  });
   it('control: documents/:id/verify with a LIVE user JWT alone reaches originate with the user own Bearer', async () => {
```
