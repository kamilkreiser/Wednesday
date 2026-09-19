# READY — KS-1238-N90-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1238-ornith35b-night7/out.md.checker/patch.diff`** (from `ls`, 23:51).

**Held 23:51 2026-09-19 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `4273adfac`. A found-document double makes the anchoring-verify forward :598 reachable; RAW598 (2-line block tamper) reds the new cell (N90-1). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control (the other round-16 briefs) mostly absent. Source: the #1084-#1091 gate's NOT-PINNED rows. Raise: Refs KS-1238, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[RAW598] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts mode=modify runner=vitest cells=10 tampers=1 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts
@@ -70,1 +70,2 @@
+    if (url === '/api/documents/doc-ks1238-found') return json(200, { id: 'doc-ks1238-found', contentHash: 'ks1238hash', status: 'anchored' });
     return json(200, { success: true, data: [] });
@@ -132,1 +133,7 @@
+  it('RED documents/:id/verify (document found): a valid key + a REVOKED session JWT, exchange refused, sends no Bearer to originate or to anchoring verify', async () => {
+    const foundMark = hits.length;
+    const found = await fetch(gatewayUrl + DOCS + 'doc-ks1238-found/verify', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': REFUSED_KEY, authorization: userJwt('ks1238-revoked') }, body: '{}' });
+    await found.text();
+    expect([found.status, hits.slice(foundMark)]).toEqual([200, ['none', 'none']]);
+  });
 });
```
