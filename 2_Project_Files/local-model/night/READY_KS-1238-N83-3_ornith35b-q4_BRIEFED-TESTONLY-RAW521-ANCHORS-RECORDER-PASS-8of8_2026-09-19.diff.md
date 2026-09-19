# READY — KS-1238-N83-3 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1238-ornith35b-night4/out.md.checker/patch.diff`** (from `ls`, 20:12).

**Held 20:12 2026-09-19 by the 18:0x Wednesday seat after a source read** (woken on the verdict by the background waiter). Tip `ba1210afc`. The ks1238 recorder also records /api/anchors/, so RAW521 (verification.ts:521) reds docslive+docsrevoked (N83-3; 2 +/2 - lines). Test-only: one file under `__tests__/`; every `+`/`-` line = the brief; crossed control (the other round-15 briefs) mostly absent. Source: the #1077-#1083 gate's NOT-PINNED rows. Raise: Refs KS-1238, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[RAW521] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts mode=modify runner=vitest cells=9 tampers=1 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts
@@ -69,2 +69,2 @@
-    if (url.startsWith(SIG) || url.startsWith(TPV) || url.startsWith(DOCS)) hits.push(bearerOf(req.headers.authorization as string | undefined));
+    if (url.startsWith(SIG) || url.startsWith(TPV) || url.startsWith(DOCS) || url.startsWith('/api/anchors/')) hits.push(bearerOf(req.headers.authorization as string | undefined));
     return json(200, { success: true, data: [] });
@@ -96,2 +96,2 @@
-/** POST documents/:id/verify through the real gateway; returns the distinct Authorizations originate received on /api/documents/. */
+/** POST documents/:id/verify through the real gateway; returns the distinct Authorizations originate (/api/documents/) and anchoring (/api/anchors/) received. */
 async function postVerify(headers: Record<string, string>): Promise<string[]> {
```
