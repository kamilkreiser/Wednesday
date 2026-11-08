# READY — KS-2055-KS-2055-O109-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from/out.md.checker/patch.diff`** (from `ls` at 06:21 2026-11-09; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 06:21 2026-11-09 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6c9a593df4abf746db612946a87839111ec5b7a9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/transfer/src/index.ts } + { Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/transfer/src/index.ts` (product) and `Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/transfer/src/index.ts
134	0	Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/transfer/src/index.ts`; test(s): `Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/transfer/src/index.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts 134 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/transfer/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-2055: the cancel door records the status it moved from RED ks2055 R1 cancelling a pending simple transfer records fromStatus pending_approval', 'KS-2055: the cancel door records the status it moved from RED ks2055 R2 cancelling a pending sale transfer records fromStatus pending_approval']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=460 failed=0 | after: total=465 failed=0` · `NEW reds: []` [baseline_suite.json total=460 failed=0; after_suite.json total=465 failed=0]
- A6 [verbatim]: `PASS A6 whole services/transfer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/transfer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/transfer/src/index.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts` (+134/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/transfer/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `6c9a593df4abf746db612946a87839111ec5b7a9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2055_o109_p1_transfer_cancel_history_records_the_status_it_moved_from/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/transfer/src/index.ts b/Blockchain/Dev/services/transfer/src/index.ts
--- a/Blockchain/Dev/services/transfer/src/index.ts
+++ b/Blockchain/Dev/services/transfer/src/index.ts
@@ -949,7 +949,8 @@
+  const previousStatus = transfer.status; // KS-2055: captured before the assignment below, so the history entry records the real from-status
   transfer.status = 'cancelled';
   transfer.updatedAt = new Date();
   transfer.statusHistory.push({
-    fromStatus: transfer.status,
+    fromStatus: previousStatus,
     toStatus: 'cancelled',
     changedBy: caller.userId, // KS-2038: requireCaller above means no fallback to 'unknown' is left
     reason: reason || 'Cancelled by user',
diff --git a/Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts b/Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-history-records-the-status-it-moved-from.test.ts
@@ -0,0 +1,134 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import http from 'http';
+import type { AddressInfo } from 'net';
+
+// KS-2055: POST /api/transfers/:id/cancel (src/index.ts) set transfer.status = 'cancelled' BEFORE it built the history entry
+// from transfer.status, so every cancel recorded fromStatus 'cancelled' and toStatus 'cancelled'. These cells cancel a pending
+// transfer through the real router and read the entry back from GET /api/transfers/:id/history. The caller is switched through
+// the stubbed authenticator (the real one is not what this pins). No DATABASE_URL: the in-memory Map is read.
+const who = vi.hoisted(() => ({
+  user: { userId: '', role: 'USER', tenantId: '', email: 'caller@example.test', verificationLevel: 'BASIC' } as Record<string, string>,
+}));
+
+vi.mock('@secuura/shared', async () => {
+  const actual = await vi.importActual<typeof import('@secuura/shared')>('@secuura/shared');
+  return {
+    ...actual,
+    authenticate: () => (req: { user?: unknown }, _res: unknown, next: () => void) => {
+      req.user = { ...who.user };
+      next();
+    },
+    enforceProductionConfig: () => undefined,
+  };
+});
+
+process.env.PORT = '0';
+delete process.env.DATABASE_URL;
+
+const OWNER = '00000000-0000-4000-8000-00000000a001';
+const RECIPIENT = '00000000-0000-4000-8000-00000000a002';
+const INITIATOR = '00000000-0000-4000-8000-00000000a003';
+const TENANT_A = 'a0000000-0000-4000-8000-000000000001';
+
+const asCaller = (userId: string) => {
+  who.user = { userId, tenantId: TENANT_A, role: 'USER', email: 'caller@example.test', verificationLevel: 'BASIC' };
+};
+
+type Entry = { fromStatus: string; toStatus: string; changedBy: string; reason: string };
+
+describe('KS-2055: the cancel door records the status it moved from', () => {
+  let server: http.Server;
+  let baseUrl = '';
+
+  function call(method: string, path: string, body?: unknown): Promise<{ status: number; data: any }> {
+    return new Promise((resolve, reject) => {
+      const url = new URL(path, baseUrl);
+      const r = http.request(
+        { hostname: url.hostname, port: url.port, path: url.pathname + url.search, method, headers: { 'Content-Type': 'application/json' } },
+        (res) => {
+          let raw = '';
+          res.on('data', (c) => (raw += c));
+          res.on('end', () => resolve({ status: res.statusCode || 0, data: raw ? JSON.parse(raw) : undefined }));
+        },
+      );
+      r.on('error', reject);
+      if (body) r.write(JSON.stringify(body));
+      r.end();
+    });
+  }
+
+  async function makeTransfer(over: object = {}): Promise<string> {
+    asCaller(INITIATOR);
+    const res = await call('POST', '/api/transfers', {
+      documentId: `doc-1700000000000-${Math.random().toString(16).slice(2, 10)}`,
+      transferType: 'simple',
+      currentOwnerId: OWNER,
+      newOwnerId: RECIPIENT,
+      documentHash: 'a'.repeat(64),
+      documentTitle: 'KS-2055 cell',
+      documentType: 'certificate',
+      ...over,
+    });
+    expect(res.status).toBe(201);
+    return res.data.data.id as string;
+  }
+
+  const lastEntry = async (id: string): Promise<Entry> => {
+    asCaller(INITIATOR);
+    const res = await call('GET', `/api/transfers/${id}/history`);
+    const history = res.data.data.history as Entry[];
+    return history[history.length - 1];
+  };
+
+  beforeAll(async () => {
+    const mod = await import('../index');
+    await new Promise<void>((resolve) => {
+      server = mod.default.listen(0, '127.0.0.1', () => resolve());
+    });
+    baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+  });
+  afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));
+  beforeEach(() => asCaller(INITIATOR));
+
+  it('control ks2055 C1 the initiator cancels a pending transfer: 200, status cancelled, entry ends at cancelled', async () => {
+    const id = await makeTransfer();
+    asCaller(INITIATOR);
+    const res = await call('POST', `/api/transfers/${id}/cancel`, { reason: 'changed my mind' });
+    expect(res.status).toBe(200);
+    expect(res.data.data.status).toBe('cancelled');
+    expect((await lastEntry(id)).toStatus).toBe('cancelled');
+  });
+
+  it('control ks2055 C2 the entry records the signed-in actor and the reason sent', async () => {
+    const id = await makeTransfer();
+    asCaller(INITIATOR);
+    await call('POST', `/api/transfers/${id}/cancel`, { reason: 'changed my mind' });
+    const entry = await lastEntry(id);
+    expect(entry.changedBy).toBe(INITIATOR);
+    expect(entry.reason).toBe('changed my mind');
+  });
+
+  it('control ks2055 C3 a cancel with no reason records the default reason', async () => {
+    const id = await makeTransfer();
+    asCaller(INITIATOR);
+    await call('POST', `/api/transfers/${id}/cancel`, {});
+    expect((await lastEntry(id)).reason).toBe('Cancelled by user');
+  });
+
+  it('RED ks2055 R1 cancelling a pending simple transfer records fromStatus pending_approval', async () => {
+    const id = await makeTransfer();
+    asCaller(INITIATOR);
+    await call('POST', `/api/transfers/${id}/cancel`, { reason: 'R1' });
+    const entry = await lastEntry(id);
+    expect(entry.fromStatus).toBe('pending_approval');
+    expect(entry.toStatus).toBe('cancelled');
+  });
+
+  it('RED ks2055 R2 cancelling a pending sale transfer records fromStatus pending_approval', async () => {
+    const id = await makeTransfer({ transferType: 'sale', saleAmount: 100, saleCurrency: 'USD' });
+    asCaller(INITIATOR);
+    const res = await call('POST', `/api/transfers/${id}/cancel`, { reason: 'R2' });
+    expect(res.status).toBe(200);
+    expect((await lastEntry(id)).fromStatus).toBe('pending_approval');
+  });
+});
```


**HOLD NOTE (Spark operator 109, 06:2x):** HALF of KS-2055 only: the history entry now records the status it moved from. The ticket's second half (validate `reason` as a bounded string) is the owner's decision and is NOT in this pass. Tier 2 raise; not an auth change (the KS-2038 caller gate is untouched). NOT covered: the draft path, a real PostgreSQL write of the entry.
