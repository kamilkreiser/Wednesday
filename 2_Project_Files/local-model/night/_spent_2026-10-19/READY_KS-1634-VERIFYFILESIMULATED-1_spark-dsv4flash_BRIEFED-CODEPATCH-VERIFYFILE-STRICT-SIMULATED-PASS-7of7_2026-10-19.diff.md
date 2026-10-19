# READY — KS-1634-VERIFYFILESIMULATED-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1/out.md.checker/patch.diff`** (from `ls` at 09:23 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); file headers DIFFER (run ['+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts', '+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts'] vs golden ['+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts', '+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1628-l1l6-verify-file-chain-first-strict-and-honest.test.ts']); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 09:23 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `f95ad12fe5c22f8d037e7139d052363422463c79`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/verification.ts , Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/originate/src/routes/verification.ts
142	0	Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verification.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1628 L1 and L6 - the verify-file chain-first fallback RED KS-1628 L1 verify-file: a string "false" verified is not a verified reply', 'KS-1628 L1 and L6 - the verify-file chain-first fallback RED KS-1628 L6 verify-file: simulated true with a real hash is not on-chain', 'KS-1628 L1 and L6 - the verify-file chain-first fallback RED KS-1628 L6 verify-file: the shape anchoring really sends (simulated true, txHash null) is not on-chain']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1442 failed=0 | after: total=1448 failed=0` · `NEW reds: []` [baseline_suite.json total=1442 failed=0; after_suite.json total=1448 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +144/-1 test=src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verification.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts` (+142/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `f95ad12fe5c22f8d037e7139d052363422463c79` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/verification.ts b/Blockchain/Dev/services/originate/src/routes/verification.ts
index 5bbf71983..fbf21ccda 100644
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -711,3 +711,3 @@
           const chain: any = await resp.json();
-          if (chain?.verified) {
+          if (chain?.verified === true) {
             logger.info('File hash verified via chain-first lookup', { hash: hashNorm.substring(0, 16), source: chain.source });
@@ -722,2 +722,3 @@
               confirmedAt: chain.confirmedAt,
+              simulated: chain.simulated,
             });
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts
new file mode 100644
index 000000000..f6f45b5e7
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts
@@ -0,0 +1,142 @@
+/**
+ * KS-1628 L1 + L6 - the POST /verify-file chain-first fallback site in routes/verification.ts (POST /api/verification/verify-file, the
+ * `rows.length === 0` path) trusted anchoring's reply too loosely.
+ *   L1: the gate was `if (chain?.verified)`, which is truthy for the STRING 'false'; the blob it builds hard-codes
+ *       `anchored: true`, and the response says `verified: true`. The gate is now `chain?.verified === true`.
+ *   L6: `chain.simulated` was never copied into the blob handed to presentBlockchainHonestly, so a reply that declares
+ *       itself simulated was presented as on-chain. The blob now carries `simulated: chain.simulated` and the existing
+ *       presentBlockchainHonestly rule decides.
+ * Harness: the neighbouring KS-563 / KS-584 tests (real router on a real listener, mocked db / auth / shared, the
+ * anchoring call answered through global.fetch, the test's own calls through the saved real fetch).
+ */
+
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw },
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+jest.mock('../repositories/documentRepo', () => ({
+  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
+  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+import express from 'express';
+import { verificationRouter } from '../routes/verification';
+
+const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
+
+const app = express();
+app.use(express.json());
+app.use('/api/verification', verificationRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+const realFetch = global.fetch;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => {
+  server?.close();
+  global.fetch = realFetch;
+});
+
+beforeEach(() => {
+  jest.clearAllMocks();
+  // No document row anywhere: the route falls to the chain-first fallback.
+  mockQueryRaw.mockResolvedValue([]);
+});
+
+/** Anchoring's reply to GET /api/anchors/verify/:hash: a base that is on-chain, with the given overrides. */
+function chainReply(over: Record<string, unknown> = {}) {
+  return {
+    verified: true,
+    source: 'chain',
+    network: 'preview',
+    txHash: REAL_TX,
+    cardanoScanUrl: `https://preview.cardanoscan.io/transaction/${REAL_TX}`,
+    blockNumber: 4242,
+    confirmedAt: '2026-10-01T00:00:00.000Z',
+    metadata: { documentId: 'doc-1' },
+    ...over,
+  };
+}
+
+/** Drive POST /api/verification/verify-file with anchoring answering `reply`; resolves the JSON body. */
+async function callSite(reply: Record<string, unknown>): Promise<any> {
+  global.fetch = jest.fn().mockResolvedValue({ ok: true, status: 200, json: async () => reply }) as unknown as typeof fetch;
+  const res = await realFetch(`${baseUrl}/api/verification/verify-file`, { method: 'POST', body: Buffer.from('ks1628 l1 l6 file bytes') });
+  return res.json();
+}
+
+describe('KS-1628 L1 and L6 - the verify-file chain-first fallback', () => {
+  it('RED KS-1628 L1 verify-file: a string "false" verified is not a verified reply', async () => {
+    const body = await callSite(chainReply({ verified: 'false' }));
+    expect(body.verified).toBe(false);
+    expect(body.blockchain).toBeUndefined();
+  });
+
+  it('RED KS-1628 L6 verify-file: simulated true with a real hash is not on-chain', async () => {
+    const body = await callSite(chainReply({ simulated: true }));
+    expect(body.blockchain.simulated).toBe(true);
+    expect(body.blockchain.anchored).toBe(false);
+    expect(body.blockchain.txHash).toBeNull();
+    expect(body.checks.isAnchored).toBe(false);
+  });
+
+  it('RED KS-1628 L6 verify-file: the shape anchoring really sends (simulated true, txHash null) is not on-chain', async () => {
+    const body = await callSite(
+      chainReply({ simulated: true, txHash: null, simulatedTxRef: 'mock_tx_' + 'c'.repeat(64), cardanoScanUrl: null }),
+    );
+    expect(body.blockchain.simulated).toBe(true);
+    expect(body.blockchain.anchored).toBe(false);
+    expect(body.checks.isAnchored).toBe(false);
+  });
+
+  it('CONTROL KS-1628 verify-file: a real hash, a positive integer height and verified true are verified and on-chain', async () => {
+    const body = await callSite(chainReply());
+    expect(body.verified).toBe(true);
+    expect(body.blockchain.anchored).toBe(true);
+    expect(body.blockchain.txHash).toBe(REAL_TX);
+    expect(body.blockchain.blockHeight).toBe(4242);
+    expect(body.blockchain.simulated).toBeUndefined();
+    expect(body.checks.isAnchored).toBe(true);
+  });
+
+  it('CONTROL KS-1628 verify-file: simulated false on a real reply stays on-chain', async () => {
+    const body = await callSite(chainReply({ simulated: false }));
+    expect(body.verified).toBe(true);
+    expect(body.blockchain.anchored).toBe(true);
+    expect(body.blockchain.txHash).toBe(REAL_TX);
+    expect(body.checks.isAnchored).toBe(true);
+  });
+
+  it('CONTROL KS-1628 verify-file: a boolean false verified is not a verified reply', async () => {
+    const body = await callSite(chainReply({ verified: false }));
+    expect(body.verified).toBe(false);
+    expect(body.blockchain).toBeUndefined();
+  });
+});
```
