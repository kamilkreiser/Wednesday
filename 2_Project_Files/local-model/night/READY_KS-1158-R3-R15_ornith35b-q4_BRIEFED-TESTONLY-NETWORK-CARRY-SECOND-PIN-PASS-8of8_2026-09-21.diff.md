# READY — KS-1158-R3-R15 (Ornith, briefed, test_only, new · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1158-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 21:35 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -0,0 +1,97 @@ declared old=0 new=97 actual old=0 new=96 ); every line byte-exact` — STRICT APPLY REFUSED: `error: corrupt patch at line 100` (apply with --recount or rewrite the header; the raise seat states which); golden not located — no byte-identity claim is made.

**Held 21:35 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1158-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1158-r3-network-carry-second-pin.test.ts` (new). `+` lines 96 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 5/5 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `R3` → red exactly ['RED KS-1158 R3 1 - a HASHLESS failed anchor keeps its networ', 'RED KS-1158 R3 2 - a HASHED failed anchor keeps its own netw']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` WITH --recount (strict apply refuses: miscounted hunk header — every line byte-exact per the T3 line) — or rewrite the header and assert the blob equals the --recount result at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1158-ornith35b-night/input.json`. Brief: `night/briefs/KS-1158-R3-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1158-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1158-r3-network-carry-second-pin.test.ts
@@ -0,0 +1,97 @@
+/**
+ * KS-1158 R3 - a SECOND, independent pin for the `network` carry in markDocumentAnchorFailed.
+ *
+ * anchorStateSync.ts writes the anchor_failed blob with
+ * `...(prior?.network ? { network: prior.network } : {})`. The L3a gate's Tg-E
+ * tamper removed that spread and exactly ONE cell in the suite went red - the
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
+describe('KS-1158 R3 - the anchor_failed write carries the prior network', () => {
+  it('RED KS-1158 R3 1 - a HASHLESS failed anchor keeps its network', () => {
+    CELLS_RUN += 1;
+    expect(hashlessBlob.network).toBe('preprod');
+  });
+
+  it('RED KS-1158 R3 2 - a HASHED failed anchor keeps its own network value, not a constant', () => {
+    CELLS_RUN += 1;
+    expect(hashedBlob.network).toBe('mainnet');
+  });
+
+  it('GREEN KS-1158 R3 3 CONTROL - all three writes happened, each anchor_failed, and the hash still carries', () => {
+    CELLS_RUN += 1;
+    expect(writes).toBe(3);
+    expect(hashlessBlob.status).toBe('anchor_failed');
+    expect(hashedBlob.status).toBe('anchor_failed');
+    expect(hashedBlob.txHash).toBe(REAL_TX);
+  });
+
+  it('GREEN KS-1158 R3 4 CONTROL - a prior with NO network gains no network key', () => {
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
