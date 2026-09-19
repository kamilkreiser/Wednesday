# READY — KS-739-N89-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks739-ornith35b-night7/out.md.checker/patch.diff`** (from `ls`, 23:51).

**Held 23:51 2026-09-19 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `4273adfac`. Pins non-JSON 422/502/504 from the recipient lookup (N89-1). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control (the other round-16 briefs) mostly absent. Source: the #1084-#1091 gate's NOT-PINNED rows. Raise: NO Refs (KS-739 archived).

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[NOJSON504] every control green under the tamper
T6 summary: 3/3 tamper(s) red exactly their declared set
T7 summary: controls green under all 3 tamper(s)
T8 summary: all 3 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts mode=modify runner=jest cells=25 tampers=3 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts
@@ -294,1 +294,19 @@
+  it('RED KS-739 N89-1: a 422 whose body is not JSON (json() rejects) is still 400 VALIDATION_ERROR, never 502', async () => {
+    const notJson422 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
+    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 422, json: notJson422 } as any) : realFetch(url, init))) as any;
+    const r422 = await transferByEmail();
+    expect([r422.status, r422.payload.error?.code]).toEqual([400, 'VALIDATION_ERROR']);
+  });
+  it('RED KS-739 N89-1: a 502 whose body is not JSON (json() rejects) is still 502 BAD_GATEWAY from the upstream branch, not the catch', async () => {
+    const notJson502 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
+    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 502, json: notJson502 } as any) : realFetch(url, init))) as any;
+    const r502 = await transferByEmail();
+    expect([r502.status, r502.payload.error?.code, r502.payload.error?.message]).toEqual([502, 'BAD_GATEWAY', 'Could not resolve recipient email via users/lookup']);
+  });
+  it('RED KS-739 N89-1: a 504 whose body is not JSON (json() rejects) is still 502 BAD_GATEWAY from the upstream branch, not the catch', async () => {
+    const notJson504 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
+    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 504, json: notJson504 } as any) : realFetch(url, init))) as any;
+    const r504 = await transferByEmail();
+    expect([r504.status, r504.payload.error?.code, r504.payload.error?.message]).toEqual([502, 'BAD_GATEWAY', 'Could not resolve recipient email via users/lookup']);
+  });
   it('no anchor is minted and no custody row is written on a 403', async () => {
```
