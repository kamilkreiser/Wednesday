# READY — KS-1676-V1SETTLEDFAILED-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-r2/out.md.checker/patch.diff`** (from `ls` at 03:23 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-r2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-control-r2/out.md.checker/patch.diff` rc 0, Wednesday overnight 2026-10-20).

**Held 03:23 2026-10-20 by Wednesday overnight 2026-10-20 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `f7d35d628cdcf1df88a6b55665f3cd2e5e2b7696`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
136	0	Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `[no PASS A3c line in checker.out — TEST_ONLY with no expected '+' lines: the run's patch is BYTE-IDENTICAL to the control golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-control-r2/out.md.checker/patch.diff` (byte compare in hold_ready); checker.out INFO A3i verbatim: `INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured`]` — no expected_plus in the input; not re-measured here.
- A3i line absent from checker.out (not claimed)
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/routes/verification.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `19e4e9ee65eae338` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/verification.ts:437)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-20_ks_1676_p2-r2_031517/clone/Blockchain/Dev/services/originate/src/routes/verification.ts:437: '  if (settled || failed) return blob;' -> '  if ((settled && false) || (failed && false)) return blob;'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/routes/verification.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 437. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts fails at the untouched tip (4 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=4 of total=5; red cell(s): ['KS-1676 - the v1 heal never rewrites a settled or failed stored anchor RED KS-1676 S1: a stored status "failed" row is left failed, the chain is not read and nothing is persisted', 'KS-1676 - the v1 heal never rewrites a settled or failed stored anchor RED KS-1676 S2: a stored status "anchor_failed" row is left anchor_failed, the chain is not read and nothing is persisted', 'KS-1676 - the v1 heal never rewrites a settled or failed stored anchor RED KS-1676 S3: a stored status "confirmed" row keeps its stored block height and network, and the chain is not read', 'KS-1676 - the v1 heal never rewrites a settled or failed stored anchor RED KS-1676 S4: a stored "anchored: true" row whose status still reads pending is left pending, the chain is not read and nothing is persisted']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1526 failed=0 | after: total=1531 failed=0` · `NEW reds: []` [baseline_suite.json total=1526 failed=0; after_suite.json total=1531 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +136/-0 test=src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts` (+136/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/routes/verification.ts` is the tamper target and is byte-unchanged (sha256 19e4e9ee65eae338, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `f7d35d628cdcf1df88a6b55665f3cd2e5e2b7696` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1676): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1676_p2/KS-1676.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p2-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts
new file mode 100644
index 000000000..d35091bb1
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1676-v1-settled-and-failed-rows-never-heal.test.ts
@@ -0,0 +1,136 @@
+/**
+ * KS-1676 - the v1 stale-anchor heal (`confirmStalePendingAnchor`, verification.ts) returns a SETTLED or FAILED stored blob
+ * untouched, before it reads the chain: status 'confirmed', `anchored: true`, status 'failed' or 'anchor_failed'. Nothing pinned those
+ * four early-returns, so a regression could show a failed anchor as 'confirmed' and write that back through `persistHealedAnchor`.
+ * Every RED cell gives the row a chain reply that names its own tx, so only the guard under test keeps it from healing; the
+ * control cell shows the same row, stale pending, DOES heal and persist once.
+ * Harness: the real v1 router; the database, the auth middleware and the repository are mocked; `fetch` answers the anchoring
+ * chain lookup. Copied from ks1661-a-simulated-chain-reply-never-heals-a-stale-pending-row.test.ts.
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
+import { verificationRouter } from '../routes/verification';
+
+const HASH = 'f'.repeat(64);
+const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
+const ROW_ID = 'doc-target';
+const TENANT = '11111111-2222-4333-8444-555555555555';
+
+/** A registration whose stored chain blob is `blob`. */
+function rowWith(blob: Record<string, unknown>) {
+  return {
+    id: '22222222-2222-2222-2222-222222222222',
+    external_id: ROW_ID,
+    tenant_id: TENANT,
+    title: 'Grad cert',
+    document_type: 'DOCUMENT',
+    content_hash: HASH,
+    status: 'anchored',
+    certification_metadata: { blockchain: blob },
+    metadata: {},
+    created_at: '2026-08-01T00:00:00.000Z',
+    certified_at: null,
+    organization_name: 'Acme Ltd',
+  };
+}
+
+/** A verified, non-simulated chain reply for the row's tx. */
+const chainReply = () => ({ verified: true, txHash: REAL_TX, blockNumber: 4242, network: 'preview' });
+
+const app = express();
+app.use(express.json());
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
+});
+
+/** Verify the hash over v1 with the given stored blob; returns the presented blockchain object, the fetch count and the persist calls. */
+async function verifyWith(blob: Record<string, unknown>): Promise<{ blockchain: any; fetchCalls: number; persistCalls: number }> {
+  mockQueryRaw.mockResolvedValue([rowWith(blob)]);
+  const fetchMock = jest.fn().mockResolvedValue({ ok: true, json: async () => chainReply() });
+  global.fetch = fetchMock as unknown as typeof fetch;
+  const res = await realFetch(`${baseUrl}/api/verification/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ contentHash: HASH }),
+  });
+  const body: any = await res.json();
+  return { blockchain: body.blockchain, fetchCalls: fetchMock.mock.calls.length, persistCalls: mockUpdateDocument.mock.calls.length };
+}
+
+describe('KS-1676 - the v1 heal never rewrites a settled or failed stored anchor', () => {
+  it('RED KS-1676 S1: a stored status "failed" row is left failed, the chain is not read and nothing is persisted', async () => {
+    const r = await verifyWith({ txHash: REAL_TX, status: 'failed' });
+    expect([r.blockchain.status, r.fetchCalls, r.persistCalls]).toEqual(['failed', 0, 0]);
+  });
+
+  it('RED KS-1676 S2: a stored status "anchor_failed" row is left anchor_failed, the chain is not read and nothing is persisted', async () => {
+    const r = await verifyWith({ txHash: REAL_TX, status: 'anchor_failed' });
+    expect([r.blockchain.status, r.fetchCalls, r.persistCalls]).toEqual(['anchor_failed', 0, 0]);
+  });
+
+  it('RED KS-1676 S3: a stored status "confirmed" row keeps its stored block height and network, and the chain is not read', async () => {
+    const r = await verifyWith({ txHash: REAL_TX, status: 'confirmed', blockHeight: 111, network: 'mainnet' });
+    expect([r.blockchain.status, r.blockchain.blockHeight, r.blockchain.network, r.fetchCalls]).toEqual(['confirmed', 111, 'mainnet', 0]);
+  });
+
+  it('RED KS-1676 S4: a stored "anchored: true" row whose status still reads pending is left pending, the chain is not read and nothing is persisted', async () => {
+    const r = await verifyWith({ txHash: REAL_TX, status: 'pending', anchored: true, blockHeight: 111 });
+    expect([r.blockchain.status, r.blockchain.blockHeight, r.fetchCalls, r.persistCalls]).toEqual(['pending', 111, 0, 0]);
+  });
+
+  it('CONTROL KS-1676 C1: the same row stale pending DOES read the chain, heal to confirmed and persist once, so the cells above fail by the guard alone', async () => {
+    const r = await verifyWith({ txHash: REAL_TX, status: 'pending' });
+    expect([r.blockchain.status, r.fetchCalls, r.persistCalls]).toEqual(['confirmed', 1, 1]);
+  });
+});
```
