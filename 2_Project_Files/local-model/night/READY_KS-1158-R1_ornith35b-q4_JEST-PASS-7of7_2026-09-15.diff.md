# READY — KS-1158 R1 only (anchorStateSync: the anchoredAt carry keys on authoritativeTxHash(), not on hash-string truthiness) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, **jest** (services/originate), 2026-09-15 18:40 — tip develop M55 48e65c435. Run `2026-09-15_ks1158-ornith35b-night` (29 s). 2 🔴 red at the tip (tx_sim_ / mock_tx_ priors kept their anchor time) / control green (a REAL hash keeps it — the KS-1004 carry) / 3 green after / suite Δ 0 / tsc 0. R3 (the network pin) and R4 (KS-1073) are not in this diff.
# Source read by me (Wednesday): the one-line change at :170 exactly as briefed (plus a harmless `<KS-1158>` tag appended to the comment on :169 — keep or drop) (`prior?.anchoredAt && authoritativeTxHash(prior as unknown as AnchorReadState)`), :164's hash carry untouched; the test is the ks1004 driver (mocked documentRepo + logger) with three priors.

```diff
--- a/services/originate/src/__tests__/ks1158-l3a-gate-records-912-r2-937.test.ts
+++ b/services/originate/src/__tests__/ks1158-l3a-gate-records-912-r2-937.test.ts
@@ -0,0 +1,100 @@
+/**
+ * KS-1158 — L3a gate records (#912 r2 / #937): anchoredAt carry needs authoritativeTxHash.
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
+const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
+
+function baseDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
+  return {
+    id: 'doc-ks1158',
+    type: 'general',
+    status: 'anchored',
+    owner: { id: 'user-1' },
+    data: {},
+    contentHash: 'a'.repeat(64),
+    signatures: [],
+    blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1' },
+    createdAt: '2026-01-01T00:00:00.000Z',
+    updatedAt: '2026-01-01T00:00:00.000Z',
+    ...overrides,
+  } as DocumentRecord;
+}
+
+beforeEach(() => {
+  jest.clearAllMocks();
+  mockUpdateDocument.mockImplementation(async (_id, _tenant, updates) => ({ ...baseDoc(), ...updates }));
+});
+
+afterEach(() => {
+  // nothing to reset beyond clearAllMocks above
+});
+
+describe('KS-1158 — L3a gate records (#912 r2 / #937)', () => {
+  it('🔴 KS-1158 R1 — a tx_sim_ placeholder prior does NOT keep its anchoredAt', async () => {
+    const priorBlockchain = {
+      txHash: 'tx_sim_0001',
+      blockHeight: 0,
+      status: 'submitted',
+      anchorId: 'anchor_1',
+      network: 'preview',
+      anchoredAt: '2026-02-02T00:00:00.000Z',
+    };
+    mockGetDocument.mockResolvedValue(baseDoc({ blockchain: priorBlockchain }) as unknown as DocumentRecord);
+    await markDocumentAnchorFailed('doc-ks1158', 'tenant-1', 'anchor_1', 'failed on chain');
+    const [, , updates] = mockUpdateDocument.mock.calls[0];
+    expect('anchoredAt' in updates.blockchain).toBe(false);
+    expect(updates.blockchain.txHash).toBe('tx_sim_0001');
+  });
+
+  it('🔴 KS-1158 R1 — a mock_tx_ placeholder prior does NOT keep its anchoredAt either', async () => {
+    const priorBlockchain = {
+      txHash: 'mock_tx_0001',
+      blockHeight: 0,
+      status: 'submitted',
+      anchorId: 'anchor_1',
+      network: 'preview',
+      anchoredAt: '2026-02-02T00:00:00.000Z',
+    };
+    mockGetDocument.mockResolvedValue(baseDoc({ blockchain: priorBlockchain }) as unknown as DocumentRecord);
+    await markDocumentAnchorFailed('doc-ks1158', 'tenant-1', 'anchor_1', 'failed on chain');
+    const [, , updates] = mockUpdateDocument.mock.calls[0];
+    expect('anchoredAt' in updates.blockchain).toBe(false);
+  });
+
+  it('KS-1158 control — a REAL hash prior still keeps its anchoredAt (the KS-1004 carry)', async () => {
+    const priorBlockchain = {
+      txHash: REAL_TX,
+      blockHeight: 4242,
+      status: 'submitted',
+      anchorId: 'anchor_1',
+      network: 'preview',
+      anchoredAt: '2026-02-02T00:00:00.000Z',
+    };
+    mockGetDocument.mockResolvedValue(baseDoc({ blockchain: priorBlockchain }) as unknown as DocumentRecord);
+    await markDocumentAnchorFailed('doc-ks1158', 'tenant-1', 'anchor_1', 'failed on chain');
+    const [, , updates] = mockUpdateDocument.mock.calls[0];
+    expect(updates.blockchain.anchoredAt).toBe('2026-02-02T00:00:00.000Z');
+    expect(updates.blockchain.txHash).toBe(REAL_TX);
+  });
+});
--- a/services/originate/src/services/anchorStateSync.ts
+++ b/services/originate/src/services/anchorStateSync.ts
@@ -166,7 +166,7 @@ export async function markDocumentAnchorFailed(
       ...(prior?.network ? { network: prior.network } : {}),
       // KS-1004: an anchor time is retained only for a transaction that was
       // built and then failed — a no-hash fail-closed blob has none, which is
-      // the blob type's own contract (`documentRepo.ts:60-61`).
-      ...(prior?.txHash && prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {}),
+      // the blob type's own contract (`documentRepo.ts:60-61`). <KS-1158>
+      ...(prior?.anchoredAt && authoritativeTxHash(prior as unknown as AnchorReadState) ? { anchoredAt: prior.anchoredAt } : {}),
       ...(anchorId ? { anchorId } : {}),
```
