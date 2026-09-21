# READY — KS-1118-F2-R15 (Ornith, briefed, test_only, new · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1118-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 21:10 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; golden not located — no byte-identity claim is made.

**Held 21:10 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1118-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1118-verify-documenthash-over-hash.test.ts` (new). `+` lines 150 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 3/3 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F2` → red exactly ['RED KS-1118 F-2 {documentHash:A, hash:B} - the lookup sees A', 'RED KS-1118 F-2 {documentHash:A, hash:B} answers exactly as ']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1118-ornith35b-night/input.json`. Brief: `night/briefs/KS-1118-F2-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1118-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1118-verify-documenthash-over-hash.test.ts
@@ -0,0 +1,150 @@
+/**
+ * =============================================================================
+ * KS-1118 F-2 - documentHash over hash precedence pin
+ * =============================================================================
+ * The handler resolves `hashToVerify` through an alias chain. This task pins
+ * that `{documentHash: A, hash: B}` body answers exactly as `{documentHash: A}`
+ * alone does - i.e. the lookup sees A only and never falls through to B.
+ *
+ * Harness mirrors ks1103's shape so the same mock surface drives both tickets.
+ * =============================================================================
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
+const HASH = 'f'.repeat(64);
+const OTHER = 'e'.repeat(64);
+const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
+const DOC_ID = 'doc-1754000000000-original';
+
+function anchoredRow(): Record<string, unknown> {
+  return {
+    id: '11111111-1111-1111-1111-111111111111',
+    external_id: DOC_ID,
+    title: 'Grad cert',
+    document_type: 'DOCUMENT',
+    content_hash: HASH,
+    status: 'anchored',
+    certification_metadata: { blockchain: { txHash: REAL_TX, status: 'confirmed', blockHeight: 4547897 } },
+    metadata: {},
+    created_at: '2026-08-01T00:00:00.000Z',
+    certified_at: null,
+    organization_name: 'Acme Ltd',
+  };
+}
+
+const app = express();
+app.use(express.json());
+app.use('/api/verification', verificationRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen> | undefined;
+const realFetch = global.fetch;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server?.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => {
+  if (server) server.close();
+  global.fetch = realFetch;
+});
+
+beforeEach(() => {
+  mockQueryRaw.mockReset();
+  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
+});
+
+interface Answer {
+  status: number;
+  json: Record<string, unknown>;
+  lookups: number;
+  sawHASH: boolean;
+  sawOTHER: boolean;
+}
+
+async function verify(body: unknown, rows: 'none' | 'anchored'): Promise<Answer> {
+  mockQueryRaw.mockReset();
+  mockQueryRaw.mockResolvedValue(rows === 'anchored' ? [anchoredRow()] : []);
+  const res = await realFetch(`${baseUrl}/api/verification/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+  const json = (await res.json()) as Record<string, unknown>;
+  const values = mockQueryRaw.mock.calls.flatMap((c: unknown[]) => c.slice(1)).map((v: unknown) => String(v));
+  return {
+    status: res.status,
+    json,
+    lookups: mockQueryRaw.mock.calls.length,
+    sawHASH: values.some((v) => v.includes(HASH)),
+    sawOTHER: values.some((v) => v.includes(OTHER)),
+  };
+}
+
+function compared(a: Answer) {
+  return {
+    status: a.status,
+    verified: a.json.verified,
+    checks: a.json.checks,
+    documentId: a.json.documentId,
+    error: a.json.error,
+  };
+}
+
+describe('KS-1118 F-2 - documentHash over hash precedence pin', () => {
+  it('RED KS-1118 F-2 {documentHash:A, hash:B} - the lookup sees A only (hash is read last)', async () => {
+    const p = await verify({ documentHash: HASH, hash: OTHER }, 'none');
+    expect(p.status).toBe(200);
+    expect(p.lookups).toBe(1);
+    expect(p.sawHASH).toBe(true);
+    expect(p.sawOTHER).toBe(false);
+  });
+
+  it('RED KS-1118 F-2 {documentHash:A, hash:B} answers exactly as {documentHash:A} alone', async () => {
+    const a = await verify({ documentHash: HASH, hash: OTHER }, 'none');
+    const b = await verify({ documentHash: HASH }, 'none');
+    expect(compared(a)).toEqual(compared(b));
+    expect(a.sawOTHER).toBe(false);
+  });
+
+  it('KS-1118 control - {contentHash:A, hash:B} still sees A only (P1, unchanged by the tamper)', async () => {
+    const c = await verify({ contentHash: HASH, hash: OTHER }, 'none');
+    expect(c.status).toBe(200);
+    expect(c.sawHASH).toBe(true);
+    expect(c.sawOTHER).toBe(false);
+  });
+});
```
