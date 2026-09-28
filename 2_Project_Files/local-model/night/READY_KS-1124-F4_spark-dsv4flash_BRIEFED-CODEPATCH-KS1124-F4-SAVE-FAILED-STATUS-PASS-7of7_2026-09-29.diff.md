# READY — KS-1124-F4 (spark-dsv4flash, briefed, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-F4/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1124-F4/KS-1124.golden.diff` (`cmp` rc 0; a mutated-golden control DIFFERS, rc 1), measured by Wednesday.

**Held BY HAND at 00:07 2026-09-29 by Wednesday overnight seat 24014037.** hold_ready.py refused: `hold_ready: REFUSE — product hunk '+' lines (6) are not ordered-equal (stripped) to the brief's expected_plus (32)` (the owed product-only / code_patch-mode assumption, the same class as KS-888-REVOKE on 2026-09-28). Source at develop 0d156d12cc0f (base porcelain 0 before and after).

- Contract: Kam ruled card secuura-ks1124-f4-failed-anchor-shows-pending = b (2026-09-28 20:22): both certification routes (issue :471, recertify :1206) save `status: 'failed'` in the blockchain blob when anchoring failed; the success leg stays statusless pending-onchain. UNMEASURED, for the raise seat's NOT COVERED: originate's own reads (documents.ts:1098, :1532; retry :1338) recognise 'anchor_failed', not 'failed', so a derived document still reads anchored and cannot be retried (same as today, nothing worse).
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/certifications.ts , Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts }`
  - `PASS A3c every '+' line the brief adds is in the product hunk (32 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks543-certify-boundary-strip.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks543-certify-boundary-strip.test.ts passes with the product hunk (5 passed / 5 run)`
  - `PASS A6 whole services/originate suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=2 +35/-0 test=src/__tests__/ks543-certify-boundary-strip.test.ts red_first=yes apply_mode=strict`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=3 ok=3 bad=0 skipped_newfile=0)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -470,4 +470,7 @@
           confidence: 'pending-onchain',
           anchoringStatus,
+          // KS-1124 F4 (Kam ruled b, 2026-09-28): an issue whose anchoring failed saves status 'failed', which the
+          // gateway maps to off-chain-only; a statusless 'pending-onchain' blob would show as pending forever.
+          ...(anchoringStatus === 'failed' ? { status: 'failed' } : {}),
         } as any,
       };
@@ -1205,4 +1208,7 @@
           confidence: 'pending-onchain',
           anchoringStatus,
+          // KS-1124 F4 (Kam ruled b, 2026-09-28): a recertify whose anchoring failed saves status 'failed', the same
+          // rule as the issue route: the gateway maps it to off-chain-only instead of pending forever.
+          ...(anchoringStatus === 'failed' ? { status: 'failed' } : {}),
         } as any,
       };
--- a/Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts
@@ -151,2 +151,31 @@
   });
+});
+
+describe('KS-1124 F4: a certification whose anchoring failed is saved with status failed', () => {
+  it('RED KS-1124 F4-1: an issue whose anchoring is unreachable saves status failed, not a statusless pending', async () => {
+    const res = await issue({ type: 'certificate', data: { grade: 'F4' } });
+    const bc = mockSaveCertification.mock.calls[0][0].blockchain;
+    expect({ status: res.status, saves: mockSaveCertification.mock.calls.length, saved: bc.status, anchoringStatus: bc.anchoringStatus, anchorId: bc.anchorId }).toEqual({ status: 201, saves: 1, saved: 'failed', anchoringStatus: 'failed', anchorId: null });
+  });
+
+  it('RED KS-1124 F4-2: a recertify whose anchoring is unreachable saves status failed, not a statusless pending', async () => {
+    jest.requireMock('../repositories/certificationRepo').getCertification.mockResolvedValueOnce({ id: 'cert-ks1124-f4', type: 'certificate', status: 'issued', issuer: { id: 'issuer-1' }, holder: { id: 'holder-1' } });
+    const res = await fetch(baseUrl + '/api/certifications/cert-ks1124-f4/recertify', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ note: 'f4' }) });
+    const bc = mockSaveCertification.mock.calls[0][0].blockchain;
+    expect({ status: res.status, saves: mockSaveCertification.mock.calls.length, saved: bc.status, anchoringStatus: bc.anchoringStatus, anchorId: bc.anchorId }).toEqual({ status: 201, saves: 1, saved: 'failed', anchoringStatus: 'failed', anchorId: null });
+  });
+
+  it('control KS-1124 F4-3: an issue whose anchoring is accepted stays statusless pending-onchain with its anchor id', async () => {
+    const stub = express().post('/api/anchors', (_req, r) => { r.status(202).json({ data: { id: 'anchor-ks1124-f4' } }); }).listen(0, '127.0.0.1');
+    await new Promise((resolve) => stub.once('listening', resolve));
+    process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:' + (stub.address() as { port: number }).port;
+    try {
+      const res = await issue({ type: 'certificate', data: { grade: 'F4' } });
+      const bc = mockSaveCertification.mock.calls[0][0].blockchain;
+      expect({ status: res.status, hasStatus: 'status' in bc, confidence: bc.confidence, anchoringStatus: bc.anchoringStatus, anchorId: bc.anchorId }).toEqual({ status: 201, hasStatus: false, confidence: 'pending-onchain', anchoringStatus: 'submitted', anchorId: 'anchor-ks1124-f4' });
+    } finally {
+      process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';
+      stub.close();
+    }
+  });
 });
```
