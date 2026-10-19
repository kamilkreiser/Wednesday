# READY — KS-1661-SIMULATEDHEAL-1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1/out.md.checker/patch.diff`** (from `ls` at 00:18 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in verification.ts (run 6 vs golden 7 body lines — context, since the change lines are equal), verificationV2.ts (run 7 vs golden 8 body lines — context, since the change lines are equal) (identical in ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 00:18 2026-10-20 by Wednesday (overnight 10-20) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4a065fb7535080190c407237f948d0af3538f2dd`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/verification.ts , Blockchain/Dev/services/originate/src/routes/verificationV2.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/originate/src/routes/verification.ts
2	1	Blockchain/Dev/services/originate/src/routes/verificationV2.ts
153	0	Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verification.ts verificationV2.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/verification.ts`, `Blockchain/Dev/services/originate/src/routes/verificationV2.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/verification.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/routes/verificationV2.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts 153 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1661 - a simulated chain reply never heals a stale pending row RED KS-1661 H1: v1 refuses to heal on a simulated chain reply: the row stays pending and nothing is persisted', 'KS-1661 - a simulated chain reply never heals a stale pending row RED KS-1661 H2: v2 refuses to heal on a simulated chain reply: the row stays pending and nothing is persisted', 'KS-1661 - a simulated chain reply never heals a stale pending row RED KS-1661 H3: both paths apply a TRUTHY test, not === true: a string "true" flag refuses the heal too']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1510 failed=0 | after: total=1515 failed=0` · `NEW reds: []` [baseline_suite.json total=1510 failed=0; after_suite.json total=1515 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verification.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts` (+153/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/verification.ts, Blockchain/Dev/services/originate/src/routes/verificationV2.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `4a065fb7535080190c407237f948d0af3538f2dd` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1661_p1/KS-1661.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1661_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/verification.ts b/Blockchain/Dev/services/originate/src/routes/verification.ts
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -453,3 +453,4 @@
     const chainTx = typeof chain?.txHash === 'string' ? chain.txHash : null;
-    if (chain?.verified !== true || !chainTx || !REAL_TXHASH_RE.test(chainTx)) return blob;
+    // KS-1661: the guard on the STORED blob above never sees the incoming reply; a simulated chain reply (any truthy flag) never heals a row.
+    if (chain?.verified !== true || chain.simulated || !chainTx || !REAL_TXHASH_RE.test(chainTx)) return blob;
     // The chain answer confirms THIS document's anchoring when it is the same
diff --git a/Blockchain/Dev/services/originate/src/routes/verificationV2.ts b/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
--- a/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
@@ -128,3 +128,4 @@
 ): Record<string, unknown> | null {
-  if (!blob || blob.simulated === true || !chain) return blob;
+  // KS-1661: the guard on the STORED blob never sees the incoming reply; a simulated chain reply (any truthy flag) never heals a row.
+  if (!blob || blob.simulated === true || !chain || chain.simulated) return blob;
   const tx = typeof blob.txHash === 'string' ? blob.txHash : null;
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts
@@ -0,0 +1,153 @@
+/**
+ * KS-1661 (gate AG1's N4 on #1621) - both stale-anchor heal paths guard on the STORED blob's `simulated` flag, never on
+ * the INCOMING chain reply's. v1 heals through `confirmStalePendingAnchor` and v2 through `healBlobWithChainFact`; each
+ * returns the blob untouched when `blob.simulated === true`, but a simulated chain reply carrying a real transaction hash
+ * would still heal a pending row to `confirmed` and persist it. After the fix each path refuses to heal when the INCOMING
+ * `chain.simulated` is truthy (a truthy test, not `=== true`). The control cells keep what must not change: a genuine
+ * (non-simulated) chain reply still heals, and still persists exactly once.
+ * Harness: the real v1 and v2 routers; the database, the auth middleware and the repository are mocked; `fetch` answers the
+ * anchoring chain lookup. Copied from ks1129-heal-persists-a-number.test.ts.
+ */
+
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+const mockUpdateDocument = jest.fn().mockResolvedValue(undefined);
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
+  updateDocument: mockUpdateDocument,
+}));
+
+import express from 'express';
+import type { Server } from 'http';
+import { verificationV2Router } from '../routes/verificationV2';
+import { verificationRouter } from '../routes/verification';
+
+const HASH = 'f'.repeat(64);
+const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
+const TENANT = '11111111-2222-4333-8444-555555555555';
+
+/** A registration whose blob is STALE 'pending' with a REAL tx - the heal precondition. */
+function staleRow() {
+  return {
+    id: '11111111-1111-1111-1111-111111111111',
+    external_id: 'doc-1754000000000-original',
+    tenant_id: TENANT,
+    title: 'Grad cert',
+    document_type: 'DOCUMENT',
+    content_hash: HASH,
+    status: 'anchored',
+    certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending' } },
+    metadata: {},
+    created_at: '2026-08-01T00:00:00.000Z',
+    certified_at: null,
+    organization_name: 'Acme Ltd',
+  };
+}
+
+/** The anchoring chain reply: verified, the SAME real tx, with the given `simulated` flag. */
+function chainReply(simulated: unknown) {
+  return { verified: true, txHash: REAL_TX, blockNumber: 4242, network: 'preview', simulated };
+}
+
+const app = express();
+app.use(express.json());
+app.use('/api/v2/verification', verificationV2Router);
+app.use('/api/verification', verificationRouter);
+
+const realFetch = global.fetch;
+let server: Server;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(async () => {
+  global.fetch = realFetch;
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+beforeEach(() => {
+  mockQueryRaw.mockReset();
+  mockUpdateDocument.mockReset().mockResolvedValue(undefined);
+  mockQueryRaw.mockResolvedValue([staleRow()]);
+});
+
+function answerChainWith(reply: unknown) {
+  const fetchMock = jest.fn().mockResolvedValue({ ok: true, json: async () => reply });
+  global.fetch = fetchMock as unknown as typeof fetch;
+  return fetchMock;
+}
+
+async function verify(path: string): Promise<any> {
+  const res = await realFetch(`${baseUrl}${path}`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ contentHash: HASH }),
+  });
+  return res.json();
+}
+const v1 = async () => (await verify('/api/verification/verify')).blockchain;
+const v2 = async () => (await verify('/api/v2/verification/verify')).matches[0].blockchain;
+
+describe('KS-1661 - a simulated chain reply never heals a stale pending row', () => {
+  it('RED KS-1661 H1: v1 refuses to heal on a simulated chain reply: the row stays pending and nothing is persisted', async () => {
+    const fetchMock = answerChainWith(chainReply(true));
+    const blockchain = await v1();
+    expect(fetchMock).toHaveBeenCalledTimes(1);
+    expect([blockchain.status, mockUpdateDocument.mock.calls.length]).toEqual(['pending', 0]);
+  });
+
+  it('RED KS-1661 H2: v2 refuses to heal on a simulated chain reply: the row stays pending and nothing is persisted', async () => {
+    const fetchMock = answerChainWith(chainReply(true));
+    const blockchain = await v2();
+    expect(fetchMock).toHaveBeenCalledTimes(1);
+    expect([blockchain.status, mockUpdateDocument.mock.calls.length]).toEqual(['pending', 0]);
+  });
+
+  it('RED KS-1661 H3: both paths apply a TRUTHY test, not === true: a string "true" flag refuses the heal too', async () => {
+    answerChainWith(chainReply('true'));
+    const first = await v1();
+    answerChainWith(chainReply('true'));
+    const second = await v2();
+    expect([first.status, second.status, mockUpdateDocument.mock.calls.length]).toEqual(['pending', 'pending', 0]);
+  });
+
+  it('CONTROL KS-1661 C1: v1 still heals on a genuine (non-simulated) chain reply, and persists exactly once', async () => {
+    answerChainWith(chainReply(false));
+    const blockchain = await v1();
+    expect([blockchain.status, mockUpdateDocument.mock.calls.length]).toEqual(['confirmed', 1]);
+  });
+
+  it('CONTROL KS-1661 C2: v2 still heals on a genuine chain reply with no simulated flag at all, and persists exactly once', async () => {
+    answerChainWith({ verified: true, txHash: REAL_TX, blockNumber: 4242, network: 'preview' });
+    const blockchain = await v2();
+    expect([blockchain.status, mockUpdateDocument.mock.calls.length]).toEqual(['confirmed', 1]);
+  });
+});
```
