# READY — KS-1645-AUDITTYPE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1/out.md.checker/patch.diff`** (from `ls` at 17:15 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1-control/out.md.checker/patch.diff` rc 0, Wednesday 16:3x seat).

**Held 17:15 2026-10-19 by Wednesday 16:3x seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `722e07f19cee683ea037930e601e380a9491f7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	5	Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
80	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (9 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 12 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 5.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts byte-exact incl. leading whitespace (apply mode strict): OK 9 line(s) byte-exact incl. leading whitespace (of 9; 9 line(s) added by the apply)` [a3i_indent.out: `OK 9 line(s) byte-exact incl. leading whitespace (of 9; 9 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts fails at the untouched tip (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1645 - the audit export refuses a type it cannot filter on RED KS-1645 T1: an unknown type is a 400 BAD_REQUEST and the security service is never asked', 'KS-1645 - the audit export refuses a type it cannot filter on RED KS-1645 T2: a repeated type parameter is a 400 BAD_REQUEST and the security service is never asked', 'KS-1645 - the audit export refuses a type it cannot filter on RED KS-1645 T3: an unknown type in csv format is a 400 with no attachment']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1132 failed=0 | after: total=1137 failed=0` · `NEW reds: []` [baseline_suite.json total=1132 failed=0; after_suite.json total=1137 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +92/-5 test=src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (+12/-5 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts` (+80/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `722e07f19cee683ea037930e601e380a9491f7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1645_p1/KS-1645.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1645_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
index 49ea090ff..4115e4ee1 100644
--- a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
@@ -49,5 +49,6 @@
 }
-
-type AuditType = 'all' | 'auth' | 'document' | 'admin' | 'billing';
-
+
+const AUDIT_TYPES = ['all', 'auth', 'document', 'admin', 'billing'] as const;
+type AuditType = (typeof AUDIT_TYPES)[number];
+
 // ---------------------------------------------------------------------------
@@ -114,4 +115,10 @@
     const toDate = req.query.to as string;
-    const type: AuditType = (req.query.type as AuditType) || 'all';
-
+    // KS-1645: `type` was a bare cast forwarded verbatim, so an unknown value got a 200 whose filename and meta.type named a filter nobody applied.
+    const rawType = req.query.type || 'all';
+    if (typeof rawType !== 'string' || !(AUDIT_TYPES as readonly string[]).includes(rawType)) {
+      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Type must be one of: ${AUDIT_TYPES.join(', ')}` } });
+      return;
+    }
+    const type = rawType as AuditType;
+
     if (!['csv', 'json'].includes(format)) {
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts
new file mode 100644
index 000000000..3e1a8a944
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1645-the-audit-export-refuses-an-unknown-type.test.ts
@@ -0,0 +1,80 @@
+/**
+ * KS-1645 (item 3 only) - GET /api/admin/audit/export read `type` as a bare cast and forwarded it verbatim, so an unknown
+ * value (or a repeated `type=` parameter) got a 200 whose filename and meta.type named a filter nobody applied. After the
+ * fix an unknown or repeated `type` is a 400 BAD_REQUEST before the security service is asked; the five known values and
+ * an absent `type` behave exactly as before. Harness: the ks745 pattern - the router mounted on a bare express app behind
+ * a stub admin, the security service replaced by a recording `fetch`.
+ */
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach } from 'vitest';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.SECURITY_SERVICE_URL = 'http://security.test:1';
+
+const ENTRY = { id: 'audit-ks1645-1', timestamp: '2026-09-01T10:00:00.000Z', type: 'auth', action: 'login', userId: 'u1' };
+const fetchMock = vi.fn(async (_input: unknown) => ({ ok: true, status: 200, json: async () => ({ success: true, data: { logs: [ENTRY], total: 1, limit: 100, offset: 0 } }) }) as unknown as Response);
+vi.stubGlobal('fetch', fetchMock);
+
+let server: ReturnType<ReturnType<typeof express>['listen']> | undefined; let port = 0;
+beforeAll(async () => {
+  const { default: router } = await import('../routes/audit-export');
+  const app = express();
+  app.use((req, _res, next) => { (req as any).user = { id: 'admin-ks1645', role: 'platform_admin' }; next(); });
+  app.use('/api/admin/audit', router);
+  await new Promise<void>((r) => {
+    const s = app.listen(0, '127.0.0.1', () => { port = (s.address() as AddressInfo).port; r(); });
+    server = s;
+  });
+}, 10_000);
+afterAll(async () => {
+  const s = server;
+  if (s) await new Promise<void>((r) => s.close(() => r()));
+  for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];
+  Object.assign(process.env, savedEnv);
+  vi.unstubAllGlobals();
+});
+beforeEach(() => { fetchMock.mockClear(); });
+function getText(path: string): Promise<{ status: number; text: string; disposition: string | undefined }> {
+  return new Promise((resolve, reject) => {
+    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
+      let data = ''; res.on('data', (c) => (data += c));
+      res.on('end', () => resolve({ status: res.statusCode ?? 0, text: data, disposition: res.headers['content-disposition'] }));
+    }).on('error', reject);
+  });
+}
+const RANGE = 'from=2026-09-01&to=2026-09-02';
+
+describe('KS-1645 - the audit export refuses a type it cannot filter on', () => {
+  it('RED KS-1645 T1: an unknown type is a 400 BAD_REQUEST and the security service is never asked', async () => {
+    const res = await getText(`/api/admin/audit/export?${RANGE}&type=bogus`);
+    expect([res.status, JSON.parse(res.text)?.error?.code, fetchMock.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0]);
+  });
+
+  it('RED KS-1645 T2: a repeated type parameter is a 400 BAD_REQUEST and the security service is never asked', async () => {
+    const res = await getText(`/api/admin/audit/export?${RANGE}&type=auth&type=admin`);
+    expect([res.status, JSON.parse(res.text)?.error?.code, fetchMock.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0]);
+  });
+
+  it('RED KS-1645 T3: an unknown type in csv format is a 400 with no attachment', async () => {
+    const res = await getText(`/api/admin/audit/export?${RANGE}&format=csv&type=bogus`);
+    expect([res.status, res.disposition, fetchMock.mock.calls.length]).toEqual([400, undefined, 0]);
+  });
+
+  it('CONTROL KS-1645 C1: each of the five known types answers 200 and is forwarded to the security service as given', async () => {
+    const seen: Array<[number, string | null]> = [];
+    for (const t of ['all', 'auth', 'document', 'admin', 'billing']) {
+      fetchMock.mockClear();
+      const res = await getText(`/api/admin/audit/export?${RANGE}&type=${t}`);
+      seen.push([res.status, new URL(String(fetchMock.mock.calls[0]?.[0])).searchParams.get('type')]);
+    }
+    expect(seen).toEqual([[200, 'all'], [200, 'auth'], [200, 'document'], [200, 'admin'], [200, 'billing']]);
+  });
+
+  it('CONTROL KS-1645 C2: no type at all still answers 200 and forwards type=all', async () => {
+    const res = await getText(`/api/admin/audit/export?${RANGE}`);
+    const body = JSON.parse(res.text) as { meta?: { type?: unknown } };
+    expect([res.status, body.meta?.type, new URL(String(fetchMock.mock.calls[0]?.[0])).searchParams.get('type')]).toEqual([200, 'all', 'all']);
+  });
+});
```
