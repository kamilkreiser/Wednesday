# READY — KS-1868-O143-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 18:05 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 18:05 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `fcd178ff34fa3b289baeb1c1fb6783161bec3e0d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/issuerCerts.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
235	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: issuerCerts.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/issuerCerts.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts 235 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the issuer-cert upload, rotate and sign catches read the rejection value safely RED ks1868 R1 upload: a revoked Proxy rejection logs a constant reason and the route answers the constant 500', 'KS-1868 the issuer-cert upload, rotate and sign catches read the rejection value safely RED ks1868 R2 upload: an Error whose message getter throws logs a constant reason and the route answers the constant 500', 'KS-1868 the issuer-cert upload, rotate and sign catches read the rejection value safely RED ks1868 R3 rotate: a revoked Proxy rejection logs a constant reason, the route answers the constant 500 and no event is published', 'KS-1868 the issuer-cert upload, rotate and sign catches read the rejection value safely RED ks1868 R4 rotate: an Error whose message getter throws logs a constant reason, the route answers the constant 500 and no event is published', 'KS-1868 the issuer-cert upload, rotate and sign catches read the rejection value safely RED ks1868 R5 sign: a revoked Proxy rejection logs a constant reason and the route answers the constant 500', 'KS-1868 the issuer-cert upload, rotate and sign catches read the rejection value safely RED ks1868 R6 sign: an Error whose message getter throws logs a constant reason and the route answers the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1839 failed=0 | after: total=1848 failed=0` · `NEW reds: []` [baseline_suite.json total=1839 failed=0; after_suite.json total=1848 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts` (+235/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/issuerCerts.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `fcd178ff34fa3b289baeb1c1fb6783161bec3e0d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o143_p1_auth_issuer_certs_upload_rotate_sign_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts b/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
--- a/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
+++ b/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
@@ -319,4 +319,10 @@
   } catch (err) {
+    let reason: string;
+    try {
+      reason = String(err instanceof Error ? err.message : err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('Issuer cert upload failed', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
@@ -688,4 +694,10 @@
   } catch (err) {
+    let reason: string;
+    try {
+      reason = String(err instanceof Error ? err.message : err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('Issuer cert rotate failed', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
@@ -841,4 +853,10 @@
   } catch (err) {
+    let reason: string;
+    try {
+      reason = String(err instanceof Error ? err.message : err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('Issuer cert sign failed', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-upload-rotate-sign-unreadable-throw.test.ts
@@ -0,0 +1,235 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1868: the catches of POST /api/issuer-certs (upload), POST /api/issuer-certs/:id/rotate and POST /api/issuer-certs/sign log
+// `{ error: <the thrown value's message, read inline> }` and then answer a constant 500 INTERNAL_ERROR. The catch must still do both
+// even if the rejection value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws
+// on `.message`). Today such a value makes the catch itself throw inside an async Express 4 handler: no response is sent (the
+// request hangs) and Node sees an UNHANDLED REJECTION. The cells count unhandled rejections themselves and give the client a short
+// timeout, so a hang shows as a failed assertion. Harness: the ks1868 issuer-certs list/revoke test (real router; the repository,
+// auth middleware, event bus and the cert service mocked; the caller is an ORG_ADMIN with a tenant). The repository stand-ins reject
+// with a plain function, not a vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy before the
+// code under test saw it. Each route is made to reach its OUTER catch directly: upload through the fingerprint lookup, rotate
+// through the old-cert lookup, sign through the active-cert lookup.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  unhandled: 0,
+  published: 0,
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: () => undefined,
+  error: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: capture, createLogger: () => capture }));
+vi.mock('../middleware/authenticate', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { role: 'ORG_ADMIN', tenantId: 'ten-1868', userId: 'user-1868' };
+    next();
+  },
+}));
+vi.mock('../services/issuerCert', () => ({
+  parseCert: () => ({
+    fingerprintSha256: 'f'.repeat(64),
+    certPem: 'cert-pem',
+    subject: 'CN=test',
+    issuer: 'CN=test',
+    serialNumber: '01',
+    validFrom: new Date('2020-01-01T00:00:00Z'),
+    validUntil: new Date('2099-01-01T00:00:00Z'),
+    keyAlgorithm: 'RSA',
+    keySizeBits: 2048,
+    trustLevel: 'self_signed',
+  }),
+  verifyKeyMatchesCert: () => undefined,
+  encryptPrivateKeyPem: () => 'encrypted',
+  signContentHashWithCert: () => {
+    throw new Error('sign must not be reached');
+  },
+  IssuerCertError: class IssuerCertError extends Error {
+    code = 'SIGN_FAILED';
+  },
+}));
+vi.mock('../repositories/issuerCertRepo', () => ({
+  createIssuerCert: vi.fn(),
+  rotateIssuerCert: vi.fn(),
+  listIssuerCerts: vi.fn(),
+  revokeIssuerCert: vi.fn(),
+  toSummary: (c: unknown) => c,
+  findIssuerCertByFingerprint: () => Promise.reject(h.toThrow),
+  getIssuerCertById: () => Promise.reject(h.toThrow),
+  findActiveIssuerCertForTenant: () => Promise.reject(h.toThrow),
+}));
+vi.mock('../events', () => ({
+  publishEvent: () => {
+    h.published += 1;
+    return Promise.resolve(undefined);
+  },
+  EventTypes: {},
+}));
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
+
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+let server: Server;
+let baseUrl = '';
+beforeAll(async () => {
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+  const { issuerCertsRoutes } = await import('../routes/issuerCerts');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/issuer-certs', issuerCertsRoutes);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+afterAll(async () => {
+  server.closeAllConnections();
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  h.unhandled = 0;
+  h.published = 0;
+});
+
+const LINES = (text: string) => h.logged.filter((c) => c[0] === text);
+
+async function post(path: string, body: unknown): Promise<{ status: number; code: string | undefined; message: string | undefined } | null> {
+  try {
+    const res = await fetch(baseUrl + path, {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json' },
+      body: JSON.stringify(body),
+      signal: AbortSignal.timeout(1500),
+    });
+    const text = await res.text();
+    let code: string | undefined;
+    let message: string | undefined;
+    try {
+      const parsed = JSON.parse(text);
+      code = parsed?.error?.code;
+      message = parsed?.error?.message;
+    } catch {
+      code = undefined;
+      message = undefined;
+    }
+    return { status: res.status, code, message };
+  } catch {
+    return null;
+  }
+}
+
+const upload = () => post('/api/issuer-certs', { name: 'ks1868 cert', certPem: 'cert-pem', privateKeyPem: 'key-pem' });
+const rotate = () => post('/api/issuer-certs/cert-1868/rotate', { certPem: 'cert-pem', privateKeyPem: 'key-pem' });
+const sign = () => post('/api/issuer-certs/sign', { contentHash: 'a'.repeat(64) });
+const UPLOAD_500 = { status: 500, code: 'INTERNAL_ERROR', message: 'Failed to upload issuer cert' };
+const ROTATE_500 = { status: 500, code: 'INTERNAL_ERROR', message: 'Failed to rotate issuer cert' };
+const SIGN_500 = { status: 500, code: 'INTERNAL_ERROR', message: 'Failed to sign content hash' };
+
+const getterThrows = () =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+const revokedProxy = () => {
+  const handle = Proxy.revocable({}, {});
+  handle.revoke();
+  return handle.proxy;
+};
+
+describe('KS-1868 the issuer-cert upload, rotate and sign catches read the rejection value safely', () => {
+  it('control ks1868 C1 upload: an ordinary Error still logs its message and the route answers the constant 500', async () => {
+    h.toThrow = new Error('db down');
+    expect(await upload()).toEqual(UPLOAD_500);
+    expect(h.unhandled).toBe(0);
+    expect(LINES('Issuer cert upload failed')).toHaveLength(1);
+    expect(LINES('Issuer cert upload failed')[0][1]).toEqual({ error: 'db down' });
+  });
+
+  it('control ks1868 C2 rotate: an ordinary Error still logs its message and the route answers the constant 500', async () => {
+    h.toThrow = new Error('db down');
+    expect(await rotate()).toEqual(ROTATE_500);
+    expect(h.unhandled).toBe(0);
+    expect(h.published).toBe(0);
+    expect(LINES('Issuer cert rotate failed')).toHaveLength(1);
+    expect(LINES('Issuer cert rotate failed')[0][1]).toEqual({ error: 'db down' });
+  });
+
+  it('control ks1868 C3 sign: an ordinary Error still logs its message and the route answers the constant 500', async () => {
+    h.toThrow = new Error('db down');
+    expect(await sign()).toEqual(SIGN_500);
+    expect(h.unhandled).toBe(0);
+    expect(LINES('Issuer cert sign failed')).toHaveLength(1);
+    expect(LINES('Issuer cert sign failed')[0][1]).toEqual({ error: 'db down' });
+  });
+
+  it('RED ks1868 R1 upload: a revoked Proxy rejection logs a constant reason and the route answers the constant 500', async () => {
+    h.toThrow = revokedProxy();
+    expect(await upload()).toEqual(UPLOAD_500);
+    expect(h.unhandled).toBe(0);
+    expect(LINES('Issuer cert upload failed')).toHaveLength(1);
+    expect(LINES('Issuer cert upload failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 upload: an Error whose message getter throws logs a constant reason and the route answers the constant 500', async () => {
+    h.toThrow = getterThrows();
+    expect(await upload()).toEqual(UPLOAD_500);
+    expect(h.unhandled).toBe(0);
+    expect(LINES('Issuer cert upload failed')).toHaveLength(1);
+    expect(LINES('Issuer cert upload failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 rotate: a revoked Proxy rejection logs a constant reason, the route answers the constant 500 and no event is published', async () => {
+    h.toThrow = revokedProxy();
+    expect(await rotate()).toEqual(ROTATE_500);
+    expect(h.unhandled).toBe(0);
+    expect(h.published).toBe(0);
+    expect(LINES('Issuer cert rotate failed')).toHaveLength(1);
+    expect(LINES('Issuer cert rotate failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 rotate: an Error whose message getter throws logs a constant reason, the route answers the constant 500 and no event is published', async () => {
+    h.toThrow = getterThrows();
+    expect(await rotate()).toEqual(ROTATE_500);
+    expect(h.unhandled).toBe(0);
+    expect(h.published).toBe(0);
+    expect(LINES('Issuer cert rotate failed')).toHaveLength(1);
+    expect(LINES('Issuer cert rotate failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R5 sign: a revoked Proxy rejection logs a constant reason and the route answers the constant 500', async () => {
+    h.toThrow = revokedProxy();
+    expect(await sign()).toEqual(SIGN_500);
+    expect(h.unhandled).toBe(0);
+    expect(LINES('Issuer cert sign failed')).toHaveLength(1);
+    expect(LINES('Issuer cert sign failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R6 sign: an Error whose message getter throws logs a constant reason and the route answers the constant 500', async () => {
+    h.toThrow = getterThrows();
+    expect(await sign()).toEqual(SIGN_500);
+    expect(h.unhandled).toBe(0);
+    expect(LINES('Issuer cert sign failed')).toHaveLength(1);
+    expect(LINES('Issuer cert sign failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```

> NOTE (operator o143, 2026-11-11): TIER 1 (Opus) gate required: routing v1.0 rule 4 (auth file). Read at source by Wednesday 18:0x: three hunks, each only replaces the log field with a guarded reason; site 427 deliberately skipped (adjacent err.code read also throws).
