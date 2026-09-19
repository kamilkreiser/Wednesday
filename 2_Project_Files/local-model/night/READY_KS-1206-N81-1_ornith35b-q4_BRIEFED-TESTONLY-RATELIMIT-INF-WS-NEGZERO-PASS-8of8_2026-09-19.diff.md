# READY — KS-1206-N81-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1206-ornith35b-night4/out.md.checker/patch.diff`** (from `ls`, 19:56).

**Held 19:56 2026-09-19 by the 18:0x Wednesday seat after a source read** (late: passed 19:0x, found unheld at the 19:56 G7 tap). Tip `ba1210afc`. Pins Infinity (raw 1e999), " 100" and -0 refused 400 (N81-1). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control (the other three round-14 briefs) mostly absent. Source: the #1077-#1083 gate's NOT-PINNED rows. Raise: Refs KS-1206, never Closes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[NEGZEROPASSES] every control green under the tamper
T6 summary: 3/3 tamper(s) red exactly their declared set
T7 summary: controls green under all 3 tamper(s)
T8 summary: all 3 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/originate/src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts mode=modify runner=jest cells=19 tampers=3 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts
@@ -147,1 +147,15 @@
+  it('RED KS-1206 N81-1: rateLimit Infinity (1e999 in the raw JSON body) is refused 400 before the INSERT', async () => {
+    const inf = await fetch(base + '/api/admin/api-keys', { method: 'POST', headers: { 'content-type': 'application/json', 'x-test-principal': JSON.stringify(PLATFORM) }, body: '{"name":"ks1206","rateLimit":1e999}' });
+    const infBody: any = await inf.json().catch(() => null);
+    expect([inf.status, infBody?.error?.code ?? null, mockQueryRaw.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0]);
+  });
+  it('RED KS-1206 N81-1: a space-padded numeric-string rateLimit (" 100") is refused 400 before the INSERT', async () => {
+    const r = await mint({ name: 'ks1206', rateLimit: ' 100' });
+    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
+  });
+  it('RED KS-1206 N81-1: rateLimit -0 (-0 in the raw JSON body) is refused 400 before the INSERT', async () => {
+    const negz = await fetch(base + '/api/admin/api-keys', { method: 'POST', headers: { 'content-type': 'application/json', 'x-test-principal': JSON.stringify(PLATFORM) }, body: '{"name":"ks1206","rateLimit":-0}' });
+    const negzBody: any = await negz.json().catch(() => null);
+    expect([negz.status, negzBody?.error?.code ?? null, mockQueryRaw.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0]);
+  });
 });
```
