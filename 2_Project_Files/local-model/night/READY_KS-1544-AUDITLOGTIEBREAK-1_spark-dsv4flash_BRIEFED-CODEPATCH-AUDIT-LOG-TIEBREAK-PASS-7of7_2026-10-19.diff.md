# READY — KS-1544-AUDITLOGTIEBREAK-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1/out.md.checker/patch.diff`** (from `ls` at 09:58 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:58 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `78cb3c3939e319332e387ffecb075a169edd4a39`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/tenant-provisioning/src/index.ts , Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (product) and `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/tenant-provisioning/src/index.ts
93	0	Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/tenant-provisioning/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1544 - the platform audit log is paged in a total order RED KS-1544 O1: the page query orders by created_at DESC and then by id DESC']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=17 failed=0 | after: total=21 failed=0` · `NEW reds: []` [baseline_suite.json total=17 failed=0; after_suite.json total=21 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tenant-provisioning suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tenant-provisioning: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +94/-1 test=src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts` (+93/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `78cb3c3939e319332e387ffecb075a169edd4a39` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1544_p1/KS-1544.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1544_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/index.ts b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
index 82a6f8d4b..65ed14465 100644
--- a/Blockchain/Dev/services/tenant-provisioning/src/index.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
@@ -557,3 +557,3 @@ app.get('/api/audit-log', async (req, res) => {
     const result = await platformQuery(
-      `SELECT * FROM platform_audit_log ORDER BY created_at DESC LIMIT $1 OFFSET $2`,
+      `SELECT * FROM platform_audit_log ORDER BY created_at DESC, id DESC LIMIT $1 OFFSET $2`,
       [limit, offset],
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts
new file mode 100644
index 000000000..dd2381526
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1544-audit-log-is-paged-in-a-total-order.test.ts
@@ -0,0 +1,93 @@
+/**
+ * KS-1544 - GET /api/audit-log pages `platform_audit_log` with `LIMIT $1 OFFSET $2`. Its ORDER BY named
+ * `created_at DESC` only, so rows sharing a timestamp (now() is the transaction start, one transaction can write
+ * several) had no defined order between two queries, and a gateway reading the log in sequential windows could
+ * repeat or skip them. The ORDER BY now ends in the primary key: `ORDER BY created_at DESC, id DESC`.
+ * The service entry module is imported for real, with `pg` replaced by a recorder and the JWT middleware by a
+ * pass-through, so the cells see the SQL the route really sends and the parameters it binds.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import net from 'node:net';
+import type { AddressInfo } from 'node:net';
+
+const sent = vi.hoisted(() => ({ calls: [] as Array<{ text: string; params: unknown[] | undefined }> }));
+
+vi.mock('pg', () => {
+  class Pool {
+    async query(text: string, params?: unknown[]) {
+      sent.calls.push({ text, params });
+      if (/COUNT\(\*\)/i.test(text)) return { rows: [{ total: '3' }], rowCount: 1 };
+      if (/FROM platform_audit_log/i.test(text)) return { rows: [{ id: 'a' }, { id: 'b' }, { id: 'c' }], rowCount: 3 };
+      return { rows: [], rowCount: 0 };
+    }
+    async connect() { return { query: async () => ({ rows: [] }), release: () => undefined }; }
+    on() { return this; }
+    async end() { return undefined; }
+  }
+  return { default: { Pool }, Pool };
+});
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const real = (await importOriginal()) as Record<string, unknown>;
+  return { ...real, authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next() };
+});
+
+let base = '';
+
+async function freePort(): Promise<number> {
+  const s = net.createServer();
+  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
+  const port = (s.address() as AddressInfo).port;
+  await new Promise<void>((r) => s.close(() => r()));
+  return port;
+}
+
+beforeAll(async () => {
+  const port = await freePort();
+  process.env.PORT = String(port);
+  process.env.PLATFORM_DATABASE_URL = 'postgres://platform:pw@127.0.0.1:5432/platform';
+  process.env.DATABASE_URL = 'postgres://app:pw@127.0.0.1:5432/app';
+  await import('../index');
+  base = `http://127.0.0.1:${port}`;
+  for (let i = 0; i < 100; i += 1) {
+    try { await fetch(base + '/health'); break; } catch { await new Promise((r) => setTimeout(r, 30)); }
+  }
+});
+afterAll(() => { /* the listener dies with the worker */ });
+
+/** The SQL texts of the audit-log page query and the count query, from one request. */
+async function auditLog(query = ''): Promise<{ status: number; page?: { text: string; params: unknown[] | undefined }; count?: string; body: any }> {
+  sent.calls.length = 0;
+  const r = await fetch(`${base}/api/audit-log${query}`);
+  const body = await r.json().catch(() => ({}));
+  return {
+    status: r.status,
+    page: sent.calls.find((c) => /FROM platform_audit_log/i.test(c.text) && /LIMIT/i.test(c.text)),
+    count: sent.calls.find((c) => /COUNT\(\*\)/i.test(c.text))?.text,
+    body,
+  };
+}
+
+describe('KS-1544 - the platform audit log is paged in a total order', () => {
+  it('RED KS-1544 O1: the page query orders by created_at DESC and then by id DESC', async () => {
+    const r = await auditLog('?limit=10&offset=20');
+    expect(r.status).toBe(200);
+    expect(r.page?.text.replace(/\s+/g, ' ')).toContain('ORDER BY created_at DESC, id DESC');
+  });
+
+  it('CONTROL KS-1544 O2: the page query still pages with LIMIT $1 OFFSET $2 and binds the clamped values', async () => {
+    const r = await auditLog('?limit=500&offset=7');
+    expect(r.page?.text.replace(/\s+/g, ' ')).toContain('LIMIT $1 OFFSET $2');
+    expect(r.page?.params).toEqual([200, 7]);
+  });
+
+  it('CONTROL KS-1544 O3: the response keeps its shape, the rows and the total from the count query', async () => {
+    const r = await auditLog();
+    expect(r.body).toEqual({ success: true, entries: [{ id: 'a' }, { id: 'b' }, { id: 'c' }], total: 3 });
+    expect(r.count).toMatch(/SELECT COUNT\(\*\) as total FROM platform_audit_log/);
+  });
+
+  it('CONTROL KS-1544 O4: the page query still reads platform_audit_log newest first', async () => {
+    const r = await auditLog();
+    expect(r.page?.text).toMatch(/FROM platform_audit_log ORDER BY created_at DESC/);
+  });
+});
```
