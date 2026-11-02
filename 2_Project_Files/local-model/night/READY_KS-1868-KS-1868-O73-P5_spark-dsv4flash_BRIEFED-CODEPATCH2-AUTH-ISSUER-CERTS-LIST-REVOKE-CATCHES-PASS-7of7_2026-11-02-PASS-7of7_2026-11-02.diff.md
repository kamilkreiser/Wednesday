# READY — KS-1868-KS-1868-O73-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-r2/out.md.checker/patch.diff`** (from `ls` at 12:49 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:49 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `92a26320e30ad680459cdb96c5b68b91a5f175a5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/issuerCerts.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
192	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: issuerCerts.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/issuerCerts.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts 192 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 the issuer-cert list and revoke catches read the rejection value safely RED ks1868 R1 list: a revoked Proxy rejection logs a constant reason and the route answers the constant 500', 'KS-1868 the issuer-cert list and revoke catches read the rejection value safely RED ks1868 R2 list: an Error whose message getter throws logs a constant reason and the route answers the constant 500', 'KS-1868 the issuer-cert list and revoke catches read the rejection value safely RED ks1868 R3 revoke: a revoked Proxy rejection logs a constant reason, the route answers the constant 500 and no event is published', 'KS-1868 the issuer-cert list and revoke catches read the rejection value safely RED ks1868 R4 revoke: an Error whose message getter throws logs a constant reason, the route answers the constant 500 and no event is published']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1471 failed=2 | after: total=1477 failed=2` · `NEW reds: []` [baseline_suite.json total=1471 failed=2; after_suite.json total=1477 failed=2]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts` (+192/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/issuerCerts.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `92a26320e30ad680459cdb96c5b68b91a5f175a5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts b/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
--- a/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
+++ b/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
@@ -362,8 +362,14 @@
       pagination: { total, limit, offset },
     });
   } catch (err) {
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('Issuer cert list failed', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
     return res.status(500).json({
       success: false,
@@ -507,8 +513,14 @@
       cert: publicResponse(toSummary(updated)),
     });
   } catch (err) {
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('Issuer cert revoke failed', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
     return res.status(500).json({
       success: false,
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts
@@ -0,0 +1,192 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1868: GET /api/issuer-certs (list) and POST /api/issuer-certs/:id/revoke answer a constant 500 INTERNAL_ERROR
+// when the repository call REJECTS, after logging their line. The catch must still do both even if the rejection
+// value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on
+// `.message`). Today such a value makes the catch itself throw inside an async Express 4 handler: no response is
+// sent (the request hangs) and Node sees an UNHANDLED REJECTION. The cells count unhandled rejections themselves
+// and give the client a short timeout, so a hang shows as a failed assertion. Harness: the ks1536 issuer-certs
+// route test (real router; the repository, auth middleware and event bus mocked; the caller is an ORG_ADMIN with a
+// tenant). The repository stand-ins reject with a plain function, not a vi.fn(): a spy inspects what it rejects
+// with and could itself fail on a revoked Proxy before the code under test saw it. On the revoke path the cert is
+// found active and the revoke UPDATE is the call that rejects: no cert is revoked and no event is published.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  unhandled: 0,
+  revokeCalls: 0,
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
+vi.mock('../repositories/issuerCertRepo', () => ({
+  createIssuerCert: vi.fn(), findIssuerCertByFingerprint: vi.fn(), findActiveIssuerCertForTenant: vi.fn(),
+  rotateIssuerCert: vi.fn(), toSummary: (c: unknown) => c,
+  listIssuerCerts: () => Promise.reject(h.toThrow),
+  getIssuerCertById: async () => ({ id: 'cert-1868', status: 'active' }),
+  revokeIssuerCert: () => {
+    h.revokeCalls += 1;
+    return Promise.reject(h.toThrow);
+  },
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
+  h.revokeCalls = 0;
+  h.published = 0;
+});
+
+const LIST_LINES = () => h.logged.filter((c) => c[0] === 'Issuer cert list failed');
+const REVOKE_LINES = () => h.logged.filter((c) => c[0] === 'Issuer cert revoke failed');
+
+async function call(method: string, path: string): Promise<{ status: number; code: string | undefined; message: string | undefined } | null> {
+  try {
+    const res = await fetch(baseUrl + path, {
+      method,
+      headers: { 'Content-Type': 'application/json' },
+      body: method === 'GET' ? undefined : '{}',
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
+const list = () => call('GET', '/api/issuer-certs');
+const revoke = () => call('POST', '/api/issuer-certs/cert-1868/revoke');
+const LIST_500 = { status: 500, code: 'INTERNAL_ERROR', message: 'Failed to list issuer certs' };
+const REVOKE_500 = { status: 500, code: 'INTERNAL_ERROR', message: 'Failed to revoke issuer cert' };
+
+const getterThrows = () =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the issuer-cert list and revoke catches read the rejection value safely', () => {
+  it('control ks1868 C1 list: an ordinary Error still logs its message and the route answers the constant 500', async () => {
+    h.toThrow = new Error('db down');
+    expect(await list()).toEqual(LIST_500);
+    expect(h.unhandled).toBe(0);
+    expect(LIST_LINES()).toHaveLength(1);
+    expect(LIST_LINES()[0][1]).toEqual({ error: 'db down' });
+  });
+
+  it('control ks1868 C2 revoke: an ordinary Error still logs its message, the route answers the constant 500 and no event is published', async () => {
+    h.toThrow = new Error('db down');
+    expect(await revoke()).toEqual(REVOKE_500);
+    expect(h.unhandled).toBe(0);
+    expect(h.revokeCalls).toBe(1);
+    expect(h.published).toBe(0);
+    expect(REVOKE_LINES()).toHaveLength(1);
+    expect(REVOKE_LINES()[0][1]).toEqual({ error: 'db down' });
+  });
+
+  it('RED ks1868 R1 list: a revoked Proxy rejection logs a constant reason and the route answers the constant 500', async () => {
+    const { proxy, revoke: revokeProxy } = Proxy.revocable({}, {});
+    revokeProxy();
+    h.toThrow = proxy;
+    expect(await list()).toEqual(LIST_500);
+    expect(h.unhandled).toBe(0);
+    expect(LIST_LINES()).toHaveLength(1);
+    expect(LIST_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 list: an Error whose message getter throws logs a constant reason and the route answers the constant 500', async () => {
+    h.toThrow = getterThrows();
+    expect(await list()).toEqual(LIST_500);
+    expect(h.unhandled).toBe(0);
+    expect(LIST_LINES()).toHaveLength(1);
+    expect(LIST_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 revoke: a revoked Proxy rejection logs a constant reason, the route answers the constant 500 and no event is published', async () => {
+    const { proxy, revoke: revokeProxy } = Proxy.revocable({}, {});
+    revokeProxy();
+    h.toThrow = proxy;
+    expect(await revoke()).toEqual(REVOKE_500);
+    expect(h.unhandled).toBe(0);
+    expect(h.revokeCalls).toBe(1);
+    expect(h.published).toBe(0);
+    expect(REVOKE_LINES()).toHaveLength(1);
+    expect(REVOKE_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 revoke: an Error whose message getter throws logs a constant reason, the route answers the constant 500 and no event is published', async () => {
+    h.toThrow = getterThrows();
+    expect(await revoke()).toEqual(REVOKE_500);
+    expect(h.unhandled).toBe(0);
+    expect(h.revokeCalls).toBe(1);
+    expect(h.published).toBe(0);
+    expect(REVOKE_LINES()).toHaveLength(1);
+    expect(REVOKE_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
