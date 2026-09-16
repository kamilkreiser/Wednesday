# READY — KS-1158 R3 (TEST-ONLY, tamper-graded: a SECOND independent pin on the network carry at anchorStateSync.ts:166) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE. Held by Wednesday at 22:49 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1158-ornith35b-night.
# Source read by me (Wednesday): ONE new file ks1158-r3-network-carry-second-pin.test.ts; product untouched; cells 🔴1 hashless keeps network 'preprod', 🔴2 hashed keeps its own 'mainnet' (not a constant), 🟢3 three anchor_failed writes + txHash carried, 🟢4 no-network prior gains no key, + COMPLETENESS; under the tamper 2 red by assertion / 5 run, at the tip 5/5; whole originate suite no new red; tsc rc 0.
# PR NOTES: one test-only PR; its file name is DISTINCT from KS-1158 R1's held diff (both can land). Leave KS-1158 per its scope sentence (R1/R2/R3 status) at raise.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1158-r3-network-carry-second-pin.test.ts
@@ -0,0 +1,96 @@
+/**
+ * KS-1158 R3 — a SECOND, independent pin for the `network` carry in markDocumentAnchorFailed.
+ *
+ * anchorStateSync.ts writes the anchor_failed blob with
+ * `...(prior?.network ? { network: prior.network } : {})`. The L3a gate's Tg-E
+ * tamper removed that spread and exactly ONE cell in the suite went red — the
+ * ks1004 carry cell, which pins hash, height, network and anchor time on one
+ * hashed prior. These cells pin the network carry on its own: a hashless prior
+ * and a hashed prior on a different network each keep theirs, and a prior with
+ * no network gains none.
+ */
+
+const mockGetDocument = jest.fn();
+const mockUpdateDocument = jest.fn();
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: mockGetDocument,
+  updateDocument: mockUpdateDocument,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import { markDocumentAnchorFailed } from '../services/anchorStateSync';
+import type { DocumentRecord } from '../repositories/documentRepo';
+
+const EXPECTED_CELLS = 4;
+let CELLS_RUN = 0;
+const REAL_TX = '9c2e4a6b8d0f1e3a5c7b9d2f4a6c8e0b1d3f5a7c9e2b4d6f8a0c2e4b6d8f0a1c';
+const HASHLESS_PRIOR = { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_r3', network: 'preprod' };
+const HASHED_PRIOR = { txHash: REAL_TX, blockHeight: 7, status: 'submitted', anchorId: 'anchor_r3', network: 'mainnet' };
+const NO_NETWORK_PRIOR = { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_r3' };
+let writes = 0;
+let hashlessBlob: Record<string, unknown> = {};
+let hashedBlob: Record<string, unknown> = {};
+let noNetworkBlob: Record<string, unknown> = {};
+
+function docWith(blockchain: Record<string, unknown>): DocumentRecord {
+  return {
+    id: 'doc-ks1158-r3',
+    type: 'general',
+    status: 'anchored',
+    owner: { id: 'user-1' },
+    data: {},
+    contentHash: 'b'.repeat(64),
+    signatures: [],
+    blockchain,
+    createdAt: '2026-01-01T00:00:00.000Z',
+    updatedAt: '2026-01-01T00:00:00.000Z',
+  } as unknown as DocumentRecord;
+}
+
+beforeAll(async () => {
+  mockUpdateDocument.mockResolvedValue(null);
+  mockGetDocument.mockResolvedValueOnce(docWith(HASHLESS_PRIOR));
+  mockGetDocument.mockResolvedValueOnce(docWith(HASHED_PRIOR));
+  mockGetDocument.mockResolvedValueOnce(docWith(NO_NETWORK_PRIOR));
+  await markDocumentAnchorFailed('doc-ks1158-r3', 'tenant-1', 'anchor_r3', 'failed on chain');
+  await markDocumentAnchorFailed('doc-ks1158-r3', 'tenant-1', 'anchor_r3', 'failed on chain');
+  await markDocumentAnchorFailed('doc-ks1158-r3', 'tenant-1', 'anchor_r3', 'failed on chain');
+  writes = mockUpdateDocument.mock.calls.length;
+  hashlessBlob = writes > 0 ? mockUpdateDocument.mock.calls[0][2].blockchain : {};
+  hashedBlob = writes > 1 ? mockUpdateDocument.mock.calls[1][2].blockchain : {};
+  noNetworkBlob = writes > 2 ? mockUpdateDocument.mock.calls[2][2].blockchain : {};
+});
+
+describe('KS-1158 R3 — the anchor_failed write carries the prior network', () => {
+  it('🔴 KS-1158 R3 1 — a HASHLESS failed anchor keeps its network', () => {
+    CELLS_RUN += 1;
+    expect(hashlessBlob.network).toBe('preprod');
+  });
+
+  it('🔴 KS-1158 R3 2 — a HASHED failed anchor keeps its own network value, not a constant', () => {
+    CELLS_RUN += 1;
+    expect(hashedBlob.network).toBe('mainnet');
+  });
+
+  it('🟢 KS-1158 R3 3 CONTROL — all three writes happened, each anchor_failed, and the hash still carries', () => {
+    CELLS_RUN += 1;
+    expect(writes).toBe(3);
+    expect(hashlessBlob.status).toBe('anchor_failed');
+    expect(hashedBlob.status).toBe('anchor_failed');
+    expect(hashedBlob.txHash).toBe(REAL_TX);
+  });
+
+  it('🟢 KS-1158 R3 4 CONTROL — a prior with NO network gains no network key', () => {
+    CELLS_RUN += 1;
+    expect(noNetworkBlob.status).toBe('anchor_failed');
+    expect('network' in noNetworkBlob).toBe(false);
+  });
+
+  it('COMPLETENESS: every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
