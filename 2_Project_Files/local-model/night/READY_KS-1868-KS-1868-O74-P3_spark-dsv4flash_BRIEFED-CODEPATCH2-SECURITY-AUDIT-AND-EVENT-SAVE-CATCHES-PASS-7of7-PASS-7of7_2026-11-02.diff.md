# READY — KS-1868-KS-1868-O74-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 13:00 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:00 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `92a26320e30ad680459cdb96c5b68b91a5f175a5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/security/src/index.ts } + { Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/security/src/index.ts
184	0	Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/security/src/index.ts`; test(s): `Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/security/src/index.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts 184 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1868 the save catches of dbSaveAuditLog and dbSaveSecurityEvent read the thrown value safely RED ks1868 R1 a revoked Proxy from the audit insert is logged as the constant and POST /api/audit answers 201', 'KS-1868 the save catches of dbSaveAuditLog and dbSaveSecurityEvent read the thrown value safely RED ks1868 R2 an Error whose message getter throws from the audit insert is logged as the constant and POST /api/audit answers 201', 'KS-1868 the save catches of dbSaveAuditLog and dbSaveSecurityEvent read the thrown value safely RED ks1868 R3 a revoked Proxy from the event insert is logged as the constant and POST /api/events answers 201', 'KS-1868 the save catches of dbSaveAuditLog and dbSaveSecurityEvent read the thrown value safely RED ks1868 R4 an Error whose message getter throws from the event insert is logged as the constant and POST /api/events answers 201']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=393 failed=0 | after: total=400 failed=0` · `NEW reds: []` [baseline_suite.json total=393 failed=0; after_suite.json total=400 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts` (+184/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/security/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `92a26320e30ad680459cdb96c5b68b91a5f175a5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p3_security_audit_and_event_save_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/index.ts b/Blockchain/Dev/services/security/src/index.ts
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -174,6 +174,12 @@
        a.newState ? JSON.stringify(a.newState) : null, a.success, a.errorMessage || null, a.createdAt]
     ));
   } catch (err: any) {
-    logger.error('DB save audit log failed', { error: err?.message });
+    let reason: string;
+    try {
+      reason = err?.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('DB save audit log failed', { error: reason });
   }
 }
@@ -190,6 +196,12 @@
        JSON.stringify(e.details || {}), e.resolved, e.resolvedAt || null, e.resolvedBy || null, e.createdAt]
     );
   } catch (err: any) {
-    logger.error('DB save event failed', { error: err?.message });
+    let reason: string;
+    try {
+      reason = err?.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('DB save event failed', { error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts
@@ -0,0 +1,184 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach, afterEach } from 'vitest';
+import crypto from 'crypto';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+// KS-1868: the save catches of dbSaveAuditLog and dbSaveSecurityEvent (src/index.ts) log `err?.message` and swallow the
+// failure. When the insert rejects with a value whose message cannot be read (a revoked Proxy, an Error whose
+// `message` getter throws) that read throws INSIDE the catch: the failure line is never logged, the helper rejects,
+// and the route (POST /api/audit, POST /api/events) answers 500 for a record that was already kept in memory.
+// After the fix the line is logged with the constant 'unreadable thrown value' and the helper swallows the failure
+// exactly as it does for an ordinary Error, so the routes answer the 201 an ordinary Error already gets. Nothing
+// is stored in the database either way.
+// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with. The logger is
+// replaced by plain functions that record the line. The routes run on a real loopback listener with a real RS256
+// token, as in ks888.
+const ctl = vi.hoisted(() => ({
+  boom: undefined as unknown,
+  errors: [] as Array<{ message: string; error: unknown }>,
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    error: (message: string, meta?: { error?: unknown }) => {
+      ctl.errors.push({ message, error: meta?.error });
+    },
+    warn: () => undefined,
+    info: () => undefined,
+    debug: () => undefined,
+  },
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  initDb: async () => true,
+  query: async (statement: string) => {
+    if (/^\s*INSERT\s+INTO\s+(audit_logs|svc_security_events)/i.test(String(statement)) && ctl.boom !== undefined) return Promise.reject(ctl.boom);
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
+const captured: string[] = [];
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
+async function call(method: string, path: string, payload?: unknown): Promise<{ status: number; text: string; body: any }> {
+  try {
+    const res = await fetch(root + path, {
+      method,
+      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + platformToken() },
+      body: payload === undefined ? undefined : JSON.stringify(payload),
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
+const AUDIT = { action: 'ks1868.probe', resourceType: 'ks1868' };
+const EVENT = { eventType: 'ks1868.probe', severity: 'low', source: 'ks1868' };
+const postAudit = () => call('POST', '/api/audit', AUDIT);
+const postEvent = () => call('POST', '/api/events', EVENT);
+const failLines = (message: string) => ctl.errors.filter((e) => e.message === message);
+const AUDIT_FAIL = 'DB save audit log failed';
+const EVENT_FAIL = 'DB save event failed';
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const messageGetterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
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
+  ctl.errors.length = 0;
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
+describe('KS-1868 the save catches of dbSaveAuditLog and dbSaveSecurityEvent read the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error from the audit insert is logged with its message and POST /api/audit answers 201', async () => {
+    ctl.boom = new Error('db down');
+    const r = await postAudit();
+    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 201, success: true });
+    expect(failLines(AUDIT_FAIL)).toEqual([{ message: AUDIT_FAIL, error: 'db down' }]);
+  });
+
+  it('control ks1868 C2 an ordinary Error from the event insert is logged with its message and POST /api/events answers 201', async () => {
+    ctl.boom = new Error('db down');
+    const r = await postEvent();
+    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 201, success: true });
+    expect(failLines(EVENT_FAIL)).toEqual([{ message: EVENT_FAIL, error: 'db down' }]);
+  });
+
+  it('control ks1868 C3 inserts that land answer 201 and log no failure', async () => {
+    const a = await postAudit();
+    const e = await postEvent();
+    expect([a.status, e.status]).toEqual([201, 201]);
+    expect(failLines(AUDIT_FAIL)).toHaveLength(0);
+    expect(failLines(EVENT_FAIL)).toHaveLength(0);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy from the audit insert is logged as the constant and POST /api/audit answers 201', async () => {
+    ctl.boom = revokedProxy();
+    const r = await postAudit();
+    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 201, success: true });
+    expect(failLines(AUDIT_FAIL)).toEqual([{ message: AUDIT_FAIL, error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws from the audit insert is logged as the constant and POST /api/audit answers 201', async () => {
+    ctl.boom = messageGetterThrows();
+    const r = await postAudit();
+    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 201, success: true });
+    expect(failLines(AUDIT_FAIL)).toEqual([{ message: AUDIT_FAIL, error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R3 a revoked Proxy from the event insert is logged as the constant and POST /api/events answers 201', async () => {
+    ctl.boom = revokedProxy();
+    const r = await postEvent();
+    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 201, success: true });
+    expect(failLines(EVENT_FAIL)).toEqual([{ message: EVENT_FAIL, error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R4 an Error whose message getter throws from the event insert is logged as the constant and POST /api/events answers 201', async () => {
+    ctl.boom = messageGetterThrows();
+    const r = await postEvent();
+    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 201, success: true });
+    expect(failLines(EVENT_FAIL)).toEqual([{ message: EVENT_FAIL, error: 'unreadable thrown value' }]);
+  });
+});
```
