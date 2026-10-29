# READY — KS-1836-KS-1836 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p1_log_foreign_selector_no_rows-r2/out.md.checker/patch.diff`** (from `ls` at 10:38 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p1_log_foreign_selector_no_rows-r2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 10:38 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p1_log_foreign_selector_no_rows-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `a786e06e6f6ec66245a0d0d6d36959e247f7c989`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
154	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (136 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 154 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 136 line(s) byte-exact incl. leading whitespace (of 136; 155 line(s) added by the apply)` [a3i_indent.out: `OK 136 line(s) byte-exact incl. leading whitespace (of 136; 155 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `4f3357604893b0aa` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts:244)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1836_p1_log_foreign_selector_no_rows-r2_102205/clone/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts:244: '    if (withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {' -> '    if (withheld > 0) {'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 244. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1836 log contract: the foreign-selector arm of the narrowed-list warning RED KS-1836 L1 a caller with no rows who names someone else in ?userId gets the empty 200 and exactly one narrowed-list warning naming the selector']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=107 failed=0 | after: total=111 failed=0` · `NEW reds: []` [baseline_suite.json total=107 failed=0; after_suite.json total=111 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +154/-0 test=src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts` (+154/-0 per numstat.out); the product `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` is the tamper target and is byte-unchanged (sha256 4f3357604893b0aa, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `a786e06e6f6ec66245a0d0d6d36959e247f7c989` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p1_log_foreign_selector_no_rows-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p1_log_foreign_selector_no_rows-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-log-foreign-selector-with-no-rows.test.ts
@@ -0,0 +1,154 @@
+// KS-1836 (gate 23 finding F1): GET /api/nft/certificates writes one warning, 'NFT certificate list narrowed to the caller', when
+// `withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)`. The first disjunct (a row was withheld) is pinned
+// by the PR's own R17. The SECOND disjunct only matters when the caller's fetched set is EMPTY and ?userId names someone else: nothing
+// is withheld then, so only the foreign-selector arm can log it. No cell exercised that, so dropping the arm stayed green.
+// The router runs on a small express app over an ephemeral port with a test-only req.user middleware; the REAL minting service
+// runs on a fake table, and the logger is spied. Harness copied from ks1836-nft-list-owner-bound.test.ts.
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+import express from 'express';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+type Row = Record<string, unknown>;
+
+const table = vi.hoisted(() => ({ rows: [] as Record<string, unknown>[] }));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: async (text: string, params: unknown[] = []) => {
+    const sql = text.replace(/\s+/g, ' ').trim();
+    if (sql === 'SELECT * FROM svc_nft_certificates') return { rows: table.rows.slice() };
+    if (sql === 'SELECT * FROM svc_nft_certificates WHERE id = $1') {
+      return { rows: table.rows.filter(r => r.id === params[0]) };
+    }
+    if (sql === 'SELECT * FROM svc_nft_certificates WHERE user_id = $1 ORDER BY created_at DESC') {
+      return { rows: table.rows.filter(r => r.user_id === params[0]) };
+    }
+    if (sql === 'SELECT * FROM svc_nft_certificates WHERE wallet_address = $1 ORDER BY created_at DESC') {
+      return { rows: table.rows.filter(r => r.wallet_address === params[0]) };
+    }
+    throw new Error(`ks1836 log fake table: unexpected SQL: ${sql.slice(0, 80)}`);
+  },
+}));
+
+vi.mock('../cardano', () => ({
+  isCardanoNFTReady: () => false,
+  mintNFTOnChain: vi.fn(),
+  getPolicyId: () => null,
+  waitForNFTConfirmation: vi.fn(),
+}));
+
+vi.mock('../services/blockchain-verifier.service', () => ({
+  blockchainVerifier: { verifyTransaction: vi.fn() },
+}));
+
+const W_A = 'addr_test1_ks1836log_wallet_a';
+const W_B = 'addr_test1_ks1836log_wallet_b';
+const B_KEY = 'ENC-KEY-B1-ks1836log';
+const NARROWED = 'NFT certificate list narrowed to the caller';
+
+function row(id: string, userId: string, wallet: string, minute: number, encryptedKey: string | null = null): Row {
+  return {
+    id, certification_id: `cert-${id}`, user_id: userId, chain: 'cardano', wallet_address: wallet,
+    policy_id: null, asset_name: null, asset_id: null, transaction_hash: null,
+    storage_tier: 'basic', privacy_level: 'full_privacy', public_fields: '[]', status: 'minted',
+    ipfs_cid: null, encrypted_key: encryptedKey, minting_cost: null, platform_fee: null, total_cost: null,
+    error_message: null, created_at: new Date(Date.UTC(2026, 9, 29, 12, minute)),
+    updated_at: new Date(Date.UTC(2026, 9, 29, 12, minute)), minted_at: null,
+  };
+}
+
+const FIXTURE: Row[] = [
+  row('a1', 'user-A', W_A, 1, 'ENC-KEY-A1-ks1836log'),
+  row('a2', 'user-A', W_A, 2),
+  row('b1', 'user-B', W_B, 3, B_KEY),
+];
+
+const CALLER_A = { userId: 'user-A', email: 'a@example.test', role: 'ISSUER', tenantId: 'tenant-1', verificationLevel: 'basic' };
+// user-Z owns no row in the fixture: its fetched set is empty on every path.
+const CALLER_Z = { userId: 'user-Z', email: 'z@example.test', role: 'ISSUER', tenantId: 'tenant-1', verificationLevel: 'basic' };
+const EMPTY_BODY = JSON.stringify({ success: true, data: { certificates: [], count: 0 } });
+
+let server: Server;
+let base = '';
+const logCalls: Array<{ level: string; message: unknown; meta: unknown }> = [];
+
+beforeEach(async () => {
+  vi.resetModules();
+  table.rows = FIXTURE.map(r => ({ ...r }));
+  logCalls.length = 0;
+  const logger: any = (await import('../utils/logger')).logger;
+  for (const level of ['error', 'warn', 'info', 'debug'] as const) {
+    vi.spyOn(logger, level).mockImplementation(((message: unknown, meta: unknown) => {
+      logCalls.push({ level, message, meta });
+      return logger;
+    }) as any);
+  }
+  const routes = (await import('../routes/nft.routes')).default;
+  const app = express();
+  app.use((req, _res, next) => {
+    const h = req.headers['x-ks1836-user'];
+    if (typeof h === 'string') (req as any).user = JSON.parse(h);
+    next();
+  });
+  app.use('/api/nft', routes);
+  server = await new Promise<Server>(resolve => {
+    const s = app.listen(0, '127.0.0.1', () => resolve(s));
+  });
+  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+});
+
+afterEach(async () => {
+  vi.restoreAllMocks();
+  await new Promise<void>(resolve => server.close(() => resolve()));
+});
+
+async function get(path: string, user?: unknown): Promise<{ status: number; text: string; json: any }> {
+  const res = await fetch(`${base}${path}`, {
+    headers: user === undefined ? {} : { 'x-ks1836-user': JSON.stringify(user) },
+  });
+  const text = await res.text();
+  let json: any;
+  try { json = JSON.parse(text); } catch { json = undefined; }
+  return { status: res.status, text, json };
+}
+
+const ids = (r: { json: any }) => (r.json?.data?.certificates ?? []).map((c: any) => c.id);
+const narrowedLogs = () => logCalls.filter(c => c.level === 'warn' && c.message === NARROWED);
+
+describe('KS-1836 log contract: the foreign-selector arm of the narrowed-list warning', () => {
+  it('RED KS-1836 L1 a caller with no rows who names someone else in ?userId gets the empty 200 and exactly one narrowed-list warning naming the selector', async () => {
+    const r = await get('/api/nft/certificates?userId=user-B', CALLER_Z);
+    expect(r.status).toBe(200);
+    expect(r.text).toBe(EMPTY_BODY);
+    const logs = narrowedLogs();
+    expect(logs).toHaveLength(1);
+    expect(logs[0].meta).toMatchObject({ ownerId: 'user-Z', userIdSelector: 'user-B', returned: 0, withheld: 0 });
+    const serialised = JSON.stringify(logCalls);
+    expect(serialised.includes(B_KEY)).toBe(false);
+    expect(serialised.includes('encryptedKey')).toBe(false);
+  });
+
+  it('CONTROL KS-1836 L2 a caller with no rows and no selector logs no narrowed-list warning', async () => {
+    const r = await get('/api/nft/certificates', CALLER_Z);
+    expect(r.status).toBe(200);
+    expect(r.text).toBe(EMPTY_BODY);
+    expect(narrowedLogs()).toHaveLength(0);
+  });
+
+  it('CONTROL KS-1836 L3 a caller with no rows whose ?userId names itself logs no narrowed-list warning', async () => {
+    const r = await get('/api/nft/certificates?userId=user-Z', CALLER_Z);
+    expect(r.status).toBe(200);
+    expect(r.text).toBe(EMPTY_BODY);
+    expect(narrowedLogs()).toHaveLength(0);
+  });
+
+  it('CONTROL KS-1836 L4 a caller with rows who names someone else in ?userId gets the empty 200 and one warning that counts the withheld rows', async () => {
+    const r = await get('/api/nft/certificates?userId=user-B', CALLER_A);
+    expect(r.status).toBe(200);
+    expect(r.text).toBe(EMPTY_BODY);
+    const logs = narrowedLogs();
+    expect(logs).toHaveLength(1);
+    expect(logs[0].meta).toMatchObject({ ownerId: 'user-A', userIdSelector: 'user-B', returned: 0, withheld: 2 });
+  });
+});
```
