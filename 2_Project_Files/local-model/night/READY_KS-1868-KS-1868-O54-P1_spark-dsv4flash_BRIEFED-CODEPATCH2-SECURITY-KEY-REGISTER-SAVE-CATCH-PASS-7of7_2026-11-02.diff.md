# READY — KS-1868-KS-1868-O54-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 07:10 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 07:10 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/security/src/index.ts } + { Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	2	Blockchain/Dev/services/security/src/index.ts
150	0	Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (9 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/security/src/index.ts`; test(s): `Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/security/src/index.ts 9 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts 150 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 the save catch of the key-register route reads the thrown value safely RED ks1868 R1 a revoked Proxy from the INSERT logs the KS-888 line and answers 500 with no key', 'KS-1868 the save catch of the key-register route reads the thrown value safely RED ks1868 R2 an Error whose message getter throws logs the KS-888 line and answers 500 with no key']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=378 failed=0 | after: total=382 failed=0` · `NEW reds: []` [baseline_suite.json total=378 failed=0; after_suite.json total=382 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+9/-2 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts` (+150/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/security/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw/checker.out`.

```diff
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -1410,8 +1410,15 @@
       }
     } catch (saveErr: any) {
       memApiKeys.delete(apiKey.id);
-      const infra = isInfrastructureDbError(saveErr);
-      log('error', 'KS-888: API key mint refused, the key could not be saved', { keyId: apiKey.id, code: saveErr?.code, infra });
+      let infra = false;
+      let code: unknown;
+      try {
+        infra = isInfrastructureDbError(saveErr);
+        code = saveErr?.code;
+      } catch {
+        // A thrown value that cannot be read cannot be classified: no code, not infrastructure (500), as for any non-infrastructure error.
+      }
+      log('error', 'KS-888: API key mint refused, the key could not be saved', { keyId: apiKey.id, code, infra });
       return res.status(infra ? 503 : 500).json({
         success: false,
         error: { code: infra ? 'SERVICE_UNAVAILABLE' : 'INTERNAL_ERROR', message: 'The API key could not be saved, so no key was issued' },
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-key-register-save-catch-unreadable-throw.test.ts
@@ -0,0 +1,150 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach, afterEach } from 'vitest';
+import crypto from 'crypto';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+// KS-1868: the save catch of the key-register route (POST /api/keys with `rotate`) must still log its KS-888 line
+// and answer 500 with no key when the INSERT rejects with a value that cannot be read (a revoked Proxy throws on
+// any property read; an Error whose `message` getter throws, throws on `.message`).
+// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
+// itself fail on a revoked Proxy before the code under test saw it. The route runs on a real loopback listener
+// with a real RS256 token, as in ks888. The service logs through console.log (JSON lines).
+const ctl = vi.hoisted(() => ({
+  boom: undefined as unknown,
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  initDb: async () => true,
+  query: async () => ({ rows: [], rowCount: 0 }),
+  transaction: async (run: (client: unknown) => Promise<unknown>) =>
+    run({
+      query: (statement: string) => {
+        if (/^\s*INSERT\s+INTO\s+svc_api_keys/i.test(String(statement)) && ctl.boom !== undefined) return Promise.reject(ctl.boom);
+        return Promise.resolve({ rows: [], rowCount: 0 });
+      },
+    }),
+}));
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const SIGNING_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const VERIFY_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+
+const ORG_ID = '18680000-0000-4000-8000-000000001868';
+const TENANT_ID = 'c0000000-0000-4000-8000-000000001868';
+const captured: string[] = [];
+const refusalLines = () =>
+  captured.filter((s) => s.includes('KS-888: API key mint refused')).map((s) => JSON.parse(s) as { infra?: boolean; code?: unknown });
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
+async function rotateMint(): Promise<{ status: number; text: string; body: any }> {
+  try {
+    const res = await fetch(root + '/api/keys', {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + platformToken() },
+      body: JSON.stringify({ name: 'ks1868 rotate', organizationId: ORG_ID, tenantId: TENANT_ID, scopes: ['documents:read'], connectorId: 'ks1868-connector', rotate: true }),
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
+  captured.length = 0;
+  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
+    captured.push(String(args[0]));
+  });
+});
+
+afterEach(() => {
+  vi.restoreAllMocks();
+});
+
+describe('KS-1868 the save catch of the key-register route reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error from the INSERT logs the KS-888 line and answers 500 with no key', async () => {
+    ctl.boom = new Error('db down');
+    const r = await rotateMint();
+    expect({ status: r.status, code: r.body?.error?.code, key: r.body?.data?.key, skInBody: r.text.includes('sk_') }).toEqual({ status: 500, code: 'INTERNAL_ERROR', key: undefined, skInBody: false });
+    expect(refusalLines()).toHaveLength(1);
+    expect(refusalLines()[0].infra).toBe(false);
+  });
+
+  it('control ks1868 C2 a rotate whose INSERT lands answers 201 with the key', async () => {
+    const r = await rotateMint();
+    expect({ status: r.status, sk: String(r.body?.data?.key).startsWith('sk_') }).toEqual({ status: 201, sk: true });
+    expect(refusalLines()).toHaveLength(0);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy from the INSERT logs the KS-888 line and answers 500 with no key', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    ctl.boom = proxy;
+    const r = await rotateMint();
+    expect({ status: r.status, code: r.body?.error?.code, message: r.body?.error?.message, key: r.body?.data?.key, skInBody: r.text.includes('sk_') }).toEqual({
+      status: 500,
+      code: 'INTERNAL_ERROR',
+      message: 'The API key could not be saved, so no key was issued',
+      key: undefined,
+      skInBody: false,
+    });
+    expect(refusalLines()).toHaveLength(1);
+    expect(refusalLines()[0].infra).toBe(false);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs the KS-888 line and answers 500 with no key', async () => {
+    ctl.boom = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const r = await rotateMint();
+    expect({ status: r.status, code: r.body?.error?.code, message: r.body?.error?.message, key: r.body?.data?.key, skInBody: r.text.includes('sk_') }).toEqual({
+      status: 500,
+      code: 'INTERNAL_ERROR',
+      message: 'The API key could not be saved, so no key was issued',
+      key: undefined,
+      skInBody: false,
+    });
+    expect(refusalLines()).toHaveLength(1);
+    expect(refusalLines()[0].infra).toBe(false);
+  });
+});
```
