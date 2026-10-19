# READY — KS-1634-V2SIMULATED-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1634_v2_p1/out.md.checker/patch.diff`** (from `ls` at 17:19 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1634_v2_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1634_v2_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 17:19 2026-10-19 by Wednesday 16:3x seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1634_v2_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `722e07f19cee683ea037930e601e380a9491f7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/verificationV2.ts , Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/originate/src/routes/verificationV2.ts
148	0	Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/verificationV2.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1634 L6 - the v2 chain-only fallback carries simulated RED KS-1634 L6 v2: a placeholder reply (simulated true, txHash null) reads NOT on-chain', 'KS-1634 L6 - the v2 chain-only fallback carries simulated RED KS-1634 L6 v2: simulated true with a real hash reads NOT on-chain']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1481 failed=0 | after: total=1486 failed=0` · `NEW reds: []` [baseline_suite.json total=1481 failed=0; after_suite.json total=1486 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +149/-0 test=src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts` (+148/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `722e07f19cee683ea037930e601e380a9491f7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1634_v2_p1/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1634_v2_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
@@ -238,2 +238,3 @@
     confirmedAt: chain.confirmedAt,
+    simulated: chain.simulated,
   }) as Record<string, unknown>;
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts
@@ -0,0 +1,148 @@
+/**
+ * KS-1634 L6 - the /v2 chain-first fallback site: chainOnlyMatch in routes/verificationV2.ts (POST /api/v2/verification/verify,
+ * a registry miss answered from the chain index) builds the blob it hands to presentBlockchainHonestly WITHOUT the reply's
+ * `simulated`. A reply that declares itself simulated was therefore presented as on-chain. The blob now carries
+ * `simulated: chain.simulated` and the existing presentBlockchainHonestly rule decides.
+ * Harness: the neighbouring ks584-p3-verify-list test (real v2 router on a real listener, mocked db / auth / shared, the
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
+  updateDocument: jest.fn().mockResolvedValue(undefined),
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+import express from 'express';
+import { verificationV2Router } from '../routes/verificationV2';
+
+const HASH = 'e'.repeat(64);
+const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
+
+const app = express();
+app.use(express.json());
+app.use('/api/v2/verification', verificationV2Router);
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
+  // No registration anywhere: the route falls to the chain-first fallback (chainOnlyMatch).
+  mockQueryRaw.mockResolvedValue([]);
+});
+
+/** Anchoring's reply to GET /api/anchors/verify/:hash: a confirmed on-chain anchor, with the given overrides. */
+function chainReply(over: Record<string, unknown> = {}) {
+  return {
+    verified: true,
+    source: 'chain',
+    network: 'preview',
+    txHash: REAL_TX,
+    cardanoScanUrl: `https://preview.cardanoscan.io/transaction/${REAL_TX}`,
+    blockNumber: 4547897,
+    confirmedAt: '2026-08-01T00:30:00.000Z',
+    metadata: { documentId: 'doc-cross-env' },
+    ...over,
+  };
+}
+
+/** Drive POST /api/v2/verification/verify with anchoring answering `reply`; resolves the JSON body. */
+async function callV2(reply: Record<string, unknown>): Promise<any> {
+  global.fetch = jest.fn().mockResolvedValue({ ok: true, status: 200, json: async () => reply }) as unknown as typeof fetch;
+  const res = await realFetch(`${baseUrl}/api/v2/verification/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ contentHash: HASH }),
+  });
+  return res.json();
+}
+
+describe('KS-1634 L6 - the v2 chain-only fallback carries simulated', () => {
+  it('RED KS-1634 L6 v2: a placeholder reply (simulated true, txHash null) reads NOT on-chain', async () => {
+    const body = await callV2(
+      chainReply({ simulated: true, txHash: null, simulatedTxRef: 'mock_tx_' + 'c'.repeat(64), cardanoScanUrl: null }),
+    );
+    expect(body.count).toBe(1);
+    const m = body.matches[0];
+    expect(m.blockchain.simulated).toBe(true);
+    expect(m.blockchain.anchored).toBe(false);
+    expect(m.simulated).toBe(true);
+    expect(m.checks.isAnchored).toBe(false);
+  });
+
+  it('RED KS-1634 L6 v2: simulated true with a real hash reads NOT on-chain', async () => {
+    const body = await callV2(chainReply({ simulated: true }));
+    expect(body.count).toBe(1);
+    const m = body.matches[0];
+    expect(m.blockchain.simulated).toBe(true);
+    expect(m.blockchain.anchored).toBe(false);
+    expect(m.blockchain.txHash).toBeNull();
+    expect(m.simulated).toBe(true);
+    expect(m.checks.isAnchored).toBe(false);
+  });
+
+  it('CONTROL KS-1634 v2: a real confirmed anchor stays on-chain', async () => {
+    const body = await callV2(chainReply());
+    expect(body.count).toBe(1);
+    const m = body.matches[0];
+    expect(m.blockchain.anchored).toBe(true);
+    expect(m.blockchain.txHash).toBe(REAL_TX);
+    expect(m.blockchain.blockHeight).toBe(4547897);
+    expect(m.simulated).toBeUndefined();
+    expect(m.checks.isAnchored).toBe(true);
+  });
+
+  it('CONTROL KS-1634 v2: simulated false stays on-chain', async () => {
+    const body = await callV2(chainReply({ simulated: false }));
+    expect(body.count).toBe(1);
+    const m = body.matches[0];
+    expect(m.blockchain.anchored).toBe(true);
+    expect(m.blockchain.txHash).toBe(REAL_TX);
+    expect(m.simulated).toBeUndefined();
+    expect(m.checks.isAnchored).toBe(true);
+  });
+
+  it('CONTROL KS-1634 v2: a reply whose verified is not true makes no match (the strict gate is unchanged)', async () => {
+    const body = await callV2(chainReply({ verified: 'false' }));
+    expect(body.count).toBe(0);
+    expect(body.matches).toEqual([]);
+  });
+});
```
