# READY — KS-1676-V2STOREDGUARDS-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3/out.md.checker/patch.diff`** (from `ls` at 03:23 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3-control/out.md.checker/patch.diff` rc 0, Wednesday overnight 2026-10-20).

**Held 03:23 2026-10-20 by Wednesday overnight 2026-10-20 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `c129c63cf777349bae8f8b6b76f045ae53b8aed9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
155	0	Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `[no PASS A3c line in checker.out — TEST_ONLY with no expected '+' lines: the run's patch is BYTE-IDENTICAL to the control golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3-control/out.md.checker/patch.diff` (byte compare in hold_ready); checker.out INFO A3i verbatim: `INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured`]` — no expected_plus in the input; not re-measured here.
- A3i line absent from checker.out (not claimed)
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `b426d2cb26566eaa` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/verificationV2.ts:130)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-20_ks_1676_p3_030927/clone/Blockchain/Dev/services/originate/src/routes/verificationV2.ts:130: '  if (!blob || blob.simulated === true || !chain || chain.simulated) return blob;' -> '  if (!blob || !chain || chain.simulated) return blob;'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/routes/verificationV2.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 130. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1676 - the v2 heal refuses a simulated or malformed anchor on the evidence alone RED KS-1676 G1: a stored blob flagged simulated is not healed and not persisted, though the chain names its registration']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1526 failed=0 | after: total=1530 failed=0` · `NEW reds: []` [baseline_suite.json total=1526 failed=0; after_suite.json total=1530 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +155/-0 test=src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts` (+155/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` is the tamper target and is byte-unchanged (sha256 b426d2cb26566eaa, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `c129c63cf777349bae8f8b6b76f045ae53b8aed9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3/input.json`. Brief (given by --brief; its `# ` heading names KS-1676): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1676_p3/KS-1676.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1676_p3/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts
new file mode 100644
index 000000000..1d0a4a5e0
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts
@@ -0,0 +1,155 @@
+/**
+ * KS-1676 - the v2 stale-anchor heal (`healBlobWithChainFact`, verificationV2.ts) refuses three things on the evidence alone: a stored
+ * blob flagged `simulated: true`, a stored `txHash` that is not 64 hex characters, and an INCOMING chain `txHash` that is not 64 hex
+ * characters. Nothing pinned any of the three, so dropping one would heal and persist a row it must leave alone. The route fetches
+ * the chain fact only when SOME row needs a heal, so every cell lists a stale-pending COMPANION row beside the row under test. The
+ * chain reply is attributed to the target by its `metadata.documentId` (the sameDoc arm), so attribution never decides a cell:
+ * only the guard under test keeps the target from healing. The control cell proves the target DOES heal and persist when no guard fires.
+ * Harness: the real v2 router; the database, the auth middleware and the repository are mocked; `fetch` answers the anchoring
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
+import { verificationV2Router } from '../routes/verificationV2';
+
+const HASH = 'f'.repeat(64);
+const TARGET_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
+const COMPANION_TX = '0f1e2d3c4b5a69788796a5b4c3d2e1f00f1e2d3c4b5a69788796a5b4c3d2e1f0';
+const TARGET_ID = 'doc-target';
+const COMPANION_ID = 'doc-companion';
+const TENANT = '11111111-2222-4333-8444-555555555555';
+
+/** A registration whose stored chain blob is `blob`. */
+function rowWith(externalId: string, id: string, blob: Record<string, unknown>) {
+  return {
+    id,
+    external_id: externalId,
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
+/** The companion: stale 'pending' with a real tx, so the route reads the chain fact. */
+const companion = () => rowWith(COMPANION_ID, '33333333-3333-3333-3333-333333333333', { txHash: COMPANION_TX, status: 'pending' });
+
+/** The target row, with the given stored chain blob; the chain reply below names its registration, so only a guard keeps it from healing. */
+const target = (blob: Record<string, unknown>) => rowWith(TARGET_ID, '22222222-2222-2222-2222-222222222222', blob);
+
+/** A verified, non-simulated chain reply carrying `txHash`; it names the TARGET's registration, and is the companion's own tx when it is a real hash. */
+const chainReply = (txHash: string) => ({
+  verified: true,
+  txHash,
+  blockNumber: 4242,
+  network: 'preview',
+  metadata: { documentId: TARGET_ID },
+});
+
+const app = express();
+app.use(express.json());
+app.use('/api/v2/verification', verificationV2Router);
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
+/** Verify the hash over v2 with the given stored target blob and the companion beside it; returns the target's blockchain object. */
+async function verifyTarget(blob: Record<string, unknown>, chainTx: string): Promise<{ blockchain: any; fetchCalls: number; persistedIds: string[] }> {
+  mockQueryRaw.mockResolvedValue([target(blob), companion()]);
+  const fetchMock = jest.fn().mockResolvedValue({ ok: true, json: async () => chainReply(chainTx) });
+  global.fetch = fetchMock as unknown as typeof fetch;
+  const res = await realFetch(`${baseUrl}/api/v2/verification/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ contentHash: HASH }),
+  });
+  const body: any = await res.json();
+  const match = body.matches.find((m: any) => m.documentId === TARGET_ID);
+  return {
+    blockchain: match.blockchain,
+    fetchCalls: fetchMock.mock.calls.length,
+    persistedIds: mockUpdateDocument.mock.calls.map((c) => String(c[0])),
+  };
+}
+
+describe('KS-1676 - the v2 heal refuses a simulated or malformed anchor on the evidence alone', () => {
+  it('RED KS-1676 G1: a stored blob flagged simulated is not healed and not persisted, though the chain names its registration', async () => {
+    const r = await verifyTarget({ txHash: TARGET_TX, status: 'pending', simulated: true }, COMPANION_TX);
+    expect(r.fetchCalls).toBe(1);
+    expect(r.persistedIds.includes(TARGET_ID)).toBe(false);
+  });
+
+  it('RED KS-1676 G2: a stored txHash that is not 64 hex characters is not healed and not persisted', async () => {
+    const r = await verifyTarget({ txHash: 'not-a-real-tx-hash', status: 'pending' }, COMPANION_TX);
+    expect(r.fetchCalls).toBe(1);
+    expect([r.blockchain.status, r.persistedIds.includes(TARGET_ID)]).toEqual(['pending', false]);
+  });
+
+  it('RED KS-1676 G3: a chain reply whose txHash is not 64 hex characters heals nothing, though it names the registration', async () => {
+    const r = await verifyTarget({ txHash: TARGET_TX, status: 'pending' }, 'not-a-real-tx-hash');
+    expect(r.fetchCalls).toBe(1);
+    expect([r.blockchain.status, r.persistedIds.includes(TARGET_ID)]).toEqual(['pending', false]);
+  });
+
+  it('CONTROL KS-1676 C1: with a genuine stored blob and a real 64-hex chain reply naming the registration, the target DOES heal and persist', async () => {
+    const r = await verifyTarget({ txHash: TARGET_TX, status: 'pending' }, COMPANION_TX);
+    expect(r.fetchCalls).toBe(1);
+    expect([r.blockchain.status, r.blockchain.txHash, r.persistedIds.includes(TARGET_ID)]).toEqual(['confirmed', COMPANION_TX, true]);
+  });
+});
```
