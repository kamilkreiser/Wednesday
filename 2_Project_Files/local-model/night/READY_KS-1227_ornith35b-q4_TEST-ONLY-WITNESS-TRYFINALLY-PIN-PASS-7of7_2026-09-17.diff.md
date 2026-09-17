# READY — KS-1227 (test-only, api-gateway ks1072 test: try/finally around postTier2's witness listener + R1 env-pointed witness pin + R2 listener-leak cell)
# Source read by Wednesday 23:40: the model's 32 +/- lines (+24/-8) IDENTICAL to the brief (python sequence compare; a mutated copy unequal); checker RESULT PASS (7/7) first sample; A4 red-first by assertion. Tip = develop 27e53ec3a. HELD LATE: PASS at 23:14, held 23:4x (the seat was on gate verdicts; ledger row).
# PR NOTES: `Refs KS-1227: R1 pins the counting rule AS MERGED; the keep-vs-filter decision stays open on the ticket`; the :128 reword half not done. TIER 2 (test-only). Run: runs/2026-09-17_ks1227-ornith35b-night/out.md.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts
@@ -115,14 +115,14 @@ async function postTier2(rows: Array<Record<string, unknown>>): Promise<any> {
   const anchorStoreUrls: string[] = []; // KS-1180 (P-1016-1): the requests the stub anchor store receives during this verify
   const onAnchorStoreRequest = (req: { url?: string }): void => { anchorStoreUrls.push(String(req.url)); };
   anchorServer.on('request', onAnchorStoreRequest);
-  const res = await fetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
-    method: 'POST',
-    headers: { 'Content-Type': 'application/json' },
-    body: JSON.stringify({ purpose: 'test' }),
-  });
-  expect(res.status).toBe(200);
-  const body = await res.json();
-  anchorServer.off('request', onAnchorStoreRequest);
+  let body: unknown;
+  try {
+    const res = await fetch('http://127.0.0.1:' + String(gatewayPort) + '/api/documents/' + DOC_ID + '/verify', { method: 'POST', headers: jsonHead, body: JSON.stringify({ purpose: 'test' }) });
+    expect(res.status).toBe(200); // KS-1227 (R-1029-3): inside the try, so a status red still reaches the finally
+    body = await res.json();
+  } finally {
+    anchorServer.off('request', onAnchorStoreRequest); // KS-1227: detached on every path, as the KS-1180 control detaches before it asserts
+  }
   // KS-1180 (P-1016-1): the tier witness. blockchain.source reads 'persisted' on BOTH tiers, so it cannot say which tier
   // answered. Tier 2 answered only if the stub anchor store served this document exactly once.
   expect(anchorStoreUrls, 'KS-1180: tier 2 answered, one anchor-store read of this document').toEqual(['/api/anchors/document/' + DOC_ID]);
@@ -187,4 +187,20 @@ describe('KS-1072 — latest-anchor selector confirmedAt tiebreak', () => {
     ]);
     expect(body.blockchain.txHash).toBe('e'.repeat(64));
   });
+  it('KS-1227 R1 - a second request reaching the stub anchor store reds the postTier2 witness even though tier 2 answered', async () => {
+    // KS-1227 (R-1029-2, R-1029-4): the witness counts EVERY stub request, as merged at 27e53ec3a, so a hit-only URL filter
+    // in postTier2 reds here. The live chain scan reads ANCHORING_SERVICE_URL; pointing it at the stub adds a non-hit request.
+    vi.stubEnv('ANCHORING_SERVICE_URL', 'http://127.0.0.1:' + String((anchorServer.address() as AddressInfo).port));
+    try {
+      const witness = await postTier2([{ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transaction_hash: '5'.repeat(64), status: 'confirmed' }]).then(() => 'no red', (e: Error) => e.message);
+      expect(witness).toContain('KS-1180: tier 2 answered, one anchor-store read of this document');
+    } finally {
+      vi.unstubAllEnvs();
+    }
+  }); // KS-1227 R1
+  it('KS-1227 R2 - a status red inside postTier2 still detaches its anchor-store listener', async () => {
+    // KS-1227 (R-1029-3): an empty store answers 404, so the helper reds at its status read; only the stub handler stays attached.
+    const statusRed = await postTier2([]).then(() => 'no red', (e: Error) => e.message);
+    expect([statusRed.startsWith('expected 404 to be 200'), anchorServer.listenerCount('request')]).toEqual([true, 1]);
+  }); // KS-1227 R2
 });
```
