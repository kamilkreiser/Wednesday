# READY — KS-739-N82-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks739-ornith35b-night6/out.md.checker/patch.diff`** (from `ls`, 19:56).

**Held 19:56 2026-09-19 by the 18:0x Wednesday seat after a source read** (late: passed 19:0x, found unheld at the 19:56 G7 tap). Tip `ba1210afc`. Pins a non-JSON 400 and 503 from the recipient lookup (N82-1). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control (the other three round-14 briefs) mostly absent. Source: the #1077-#1083 gate's NOT-PINNED rows. Raise: NO Refs (KS-739 archived).

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[NOJSON503] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts mode=modify runner=jest cells=22 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts
@@ -282,1 +282,13 @@
+  it('RED KS-739 N82-1: a 400 whose body is not JSON (json() rejects) is still 400 VALIDATION_ERROR, never 502', async () => {
+    const notJson400 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
+    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 400, json: notJson400 } as any) : realFetch(url, init))) as any;
+    const r400 = await transferByEmail();
+    expect([r400.status, r400.payload.error?.code]).toEqual([400, 'VALIDATION_ERROR']);
+  });
+  it('RED KS-739 N82-1: a 503 whose body is not JSON (json() rejects) is still 502 BAD_GATEWAY from the upstream branch, not the catch', async () => {
+    const notJson503 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
+    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 503, json: notJson503 } as any) : realFetch(url, init))) as any;
+    const r503 = await transferByEmail();
+    expect([r503.status, r503.payload.error?.code, r503.payload.error?.message]).toEqual([502, 'BAD_GATEWAY', 'Could not resolve recipient email via users/lookup']);
+  });
   it('no anchor is minted and no custody row is written on a 403', async () => {
```
