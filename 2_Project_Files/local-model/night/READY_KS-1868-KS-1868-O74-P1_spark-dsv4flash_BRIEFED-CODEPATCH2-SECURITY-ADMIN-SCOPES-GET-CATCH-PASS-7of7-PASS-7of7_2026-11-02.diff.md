# READY — KS-1868-KS-1868-O74-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 12:29 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:29 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `92a26320e30ad680459cdb96c5b68b91a5f175a5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/security/src/index.ts } + { Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/security/src/index.ts
127	0	Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/security/src/index.ts`; test(s): `Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/security/src/index.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts 127 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1868 the catch of the admin-scopes read route reads the thrown value safely RED ks1868 R1 a revoked Proxy from the scope query answers 500 INTERNAL_ERROR']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=393 failed=0 | after: total=397 failed=0` · `NEW reds: []` [baseline_suite.json total=393 failed=0; after_suite.json total=397 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts` (+127/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/security/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `92a26320e30ad680459cdb96c5b68b91a5f175a5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p1_security_admin_scopes_get_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/index.ts b/Blockchain/Dev/services/security/src/index.ts
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -1823,7 +1823,13 @@
     ));
     return res.json({ success: true, data: { userId, tenantId, organizationIds: r.rows.map((x) => x.o) } });
   } catch (error) {
-    if (error instanceof z.ZodError) return badRequestFromZod(res, error);
+    let isZod: boolean;
+    try {
+      isZod = error instanceof z.ZodError;
+    } catch {
+      return next(new Error('unreadable thrown value'));
+    }
+    if (isZod) return badRequestFromZod(res, error as z.ZodError);
     return next(error);
   }
 });
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-admin-scopes-get-catch-unreadable-throw.test.ts
@@ -0,0 +1,127 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach, afterEach } from 'vitest';
+import crypto from 'crypto';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+// KS-1868: the catch of the admin-scopes READ route (GET /api/keys/admin-scopes/:userId) must still answer when
+// the scope query rejects with a value that cannot be read (a revoked Proxy throws on `instanceof`). Today the
+// catch itself throws in an async handler, so no answer is sent. After the fix such a value is handed to the
+// error handler as an ordinary Error, which is exactly what an ordinary non-infrastructure Error gets
+// (500 INTERNAL_ERROR). The route's own 400 for a query the schema refuses (a ZodError) is pinned by C3, the
+// cell the PUT route's suite added after gate 94 (G94-F2).
+// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
+// itself fail on a revoked Proxy before the code under test saw it. The route runs on a real loopback listener
+// with a real RS256 token, as in ks888.
+const ctl = vi.hoisted(() => ({
+  boom: undefined as unknown,
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  initDb: async () => true,
+  query: async (statement: string) => {
+    if (/^\s*SELECT\s+1\s+FROM\s+users/i.test(String(statement))) return { rows: [{ one: 1 }], rowCount: 1 };
+    if (/admin_organisation_scopes/i.test(String(statement)) && ctl.boom !== undefined) return Promise.reject(ctl.boom);
+    return { rows: [], rowCount: 0 };
+  },
+  transaction: async (run: (client: unknown) => Promise<unknown>) =>
+    run({
+      query: () => Promise.resolve({ rows: [], rowCount: 0 }),
+    }),
+}));
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const SIGNING_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const VERIFY_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+
+const USER_ID = '18680000-0000-4000-8000-000000000074';
+const TENANT_ID = 'c0000000-0000-4000-8000-000000001868';
+
+let listener: Server;
+let root = '';
+
+function platformToken(): string {
+  const now = Math.floor(Date.now() / 1000);
+  const head = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
+  const claims = Buffer.from(JSON.stringify({ sub: 'ks1868-test', iat: now, exp: now + 300, role: 'super_admin' })).toString('base64url');
+  const sig = crypto.sign('RSA-SHA256', Buffer.from(head + '.' + claims), SIGNING_PEM).toString('base64url');
+  return head + '.' + claims + '.' + sig;
+}
+
+async function getScopes(tenantId: string = TENANT_ID): Promise<{ status: number; text: string; body: any }> {
+  try {
+    const res = await fetch(root + '/api/keys/admin-scopes/' + USER_ID + '?tenantId=' + encodeURIComponent(tenantId), {
+      method: 'GET',
+      headers: { Authorization: 'Bearer ' + platformToken() },
+      signal: AbortSignal.timeout(3000),
+    });
+    const text = await res.text();
+    let body: any;
+    try {
+      body = JSON.parse(text);
+    } catch {
+      body = undefined;
+    }
+    return { status: res.status, text, body };
+  } catch {
+    return { status: 0, text: '', body: undefined };
+  }
+}
+
+const summary = (r: { status: number; body: any }) => ({ status: r.status, code: r.body?.error?.code });
+
+beforeAll(async () => {
+  process.env.JWT_PUBLIC_KEY = Buffer.from(VERIFY_PEM, 'utf8').toString('base64');
+  delete process.env.JWT_JWKS_URL;
+  delete process.env.AUTH_SERVICE_URL;
+  const app = (await import('../index')).default;
+  await new Promise<void>((resolve) => {
+    listener = app.listen(0, '127.0.0.1', resolve);
+  });
+  root = 'http://127.0.0.1:' + (listener.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => listener.close(() => resolve()));
+});
+
+beforeEach(() => {
+  ctl.boom = undefined;
+  vi.spyOn(console, 'log').mockImplementation(() => undefined);
+});
+
+afterEach(() => {
+  vi.restoreAllMocks();
+});
+
+describe('KS-1868 the catch of the admin-scopes read route reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error from the scope query answers 500 INTERNAL_ERROR', async () => {
+    ctl.boom = new Error('db down');
+    const r = await getScopes();
+    expect(summary(r)).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  });
+
+  it('control ks1868 C2 a read whose query lands answers 200 with the organisation ids', async () => {
+    const r = await getScopes();
+    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 200, success: true });
+    expect(r.body?.data?.organizationIds).toEqual([]);
+  });
+
+  it('control ks1868 C3 a query the schema refuses (a ZodError) still answers 400 BAD_REQUEST with the validation body', async () => {
+    const r = await getScopes('not-a-uuid');
+    expect(summary(r)).toEqual({ status: 400, code: 'BAD_REQUEST' });
+    expect(r.body?.success).toBe(false);
+    expect(r.body?.error?.message).toBe('Validation failed');
+    expect(r.body?.error?.details).toEqual(expect.arrayContaining([expect.objectContaining({ path: ['tenantId'] })]));
+  });
+
+  it('RED ks1868 R1 a revoked Proxy from the scope query answers 500 INTERNAL_ERROR', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    ctl.boom = proxy;
+    const r = await getScopes();
+    expect(summary(r)).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  });
+});
```
