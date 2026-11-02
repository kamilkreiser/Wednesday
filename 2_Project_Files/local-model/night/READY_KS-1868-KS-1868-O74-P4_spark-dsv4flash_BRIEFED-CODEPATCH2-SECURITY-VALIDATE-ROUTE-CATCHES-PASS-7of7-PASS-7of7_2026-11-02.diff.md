# READY — KS-1868-KS-1868-O74-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 13:03 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:03 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `92a26320e30ad680459cdb96c5b68b91a5f175a5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/security/src/index.ts } + { Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/security/src/index.ts
242	0	Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/security/src/index.ts`; test(s): `Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/security/src/index.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts 242 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=6 of total=10; red cell(s): ['KS-1868 the catches of the validate route read the thrown value safely RED ks1868 R1 a revoked Proxy from the stored-state read is logged as the constant and answers 503', 'KS-1868 the catches of the validate route read the thrown value safely RED ks1868 R2 an Error whose message getter throws from the stored-state read is logged as the constant and answers 503', 'KS-1868 the catches of the validate route read the thrown value safely RED ks1868 R3 a revoked Proxy from the cache-miss lookup is logged as the constant and answers Key not found', 'KS-1868 the catches of the validate route read the thrown value safely RED ks1868 R4 an Error whose message getter throws from the cache-miss lookup is logged as the constant and answers Key not found', 'KS-1868 the catches of the validate route read the thrown value safely RED ks1868 R5 a revoked Proxy from the usage write is logged as the constant and the valid key is answered valid', 'KS-1868 the catches of the validate route read the thrown value safely RED ks1868 R6 an Error whose message getter throws from the usage write is logged as the constant and the valid key is answered valid']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=393 failed=0 | after: total=403 failed=0` · `NEW reds: []` [baseline_suite.json total=393 failed=0; after_suite.json total=403 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts` (+242/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/security/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `92a26320e30ad680459cdb96c5b68b91a5f175a5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o74_p4_security_validate_route_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/index.ts b/Blockchain/Dev/services/security/src/index.ts
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -512,6 +512,12 @@
       [k.id, k.lastUsedAt || null]
     ));
   } catch (err: any) {
-    logger.error('DB save API key failed', { error: err?.message });
+    let reason: string;
+    try {
+      reason = err?.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('DB save API key failed', { error: reason });
   }
 }
@@ -1894,7 +1900,13 @@
       if (revokedInMemory) apiKey.isActive = false;
       memApiKeys.set(apiKey.id, apiKey);
     } catch (err: any) {
-      logger.error('KS-1370: stored API key state could not be read', { error: err?.message });
+      let reason: string;
+      try {
+        reason = err?.message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('KS-1370: stored API key state could not be read', { error: reason });
       return res.status(503).json({
         success: false,
         error: { code: 'SERVICE_UNAVAILABLE', message: 'Unable to verify key' },
@@ -1917,6 +1929,12 @@
         memApiKeys.set(apiKey.id, apiKey);
       }
     } catch (err: any) {
-      logger.warn('DB fallback for api-key validation failed', { error: err?.message });
+      let reason: string;
+      try {
+        reason = err?.message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.warn('DB fallback for api-key validation failed', { error: reason });
     }
   }
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-validate-route-catches-unreadable-throw.test.ts
@@ -0,0 +1,242 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach, afterEach } from 'vitest';
+import crypto from 'crypto';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+// KS-1868: three catches on the POST /api/keys/validate path (src/index.ts) read `err?.message` of a rejected database
+// call: the stored-state read of a cached key (KS-1370, answers 503 'Unable to verify key'), the cache-miss lookup
+// (logs a warning, answers 'Key not found') and dbRecordApiKeyUsage (the usage write, log-only by Kam's ruling).
+// When the call rejects with a value whose message cannot be read (a revoked Proxy, an Error whose `message` getter
+// throws) that read throws INSIDE the catch; the validate handler takes no `next`, so the request is never answered
+// and an unhandled rejection is raised. After the fix each catch logs the constant 'unreadable thrown value' and
+// continues exactly as it does for an ordinary Error: 503 for the stored read, 'Key not found' for the lookup,
+// valid:true for the usage write. Nothing is stored either way.
+// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with. The logger is
+// replaced by plain functions that record the lines. The route runs on a real loopback listener with a real RS256
+// token, as in ks888 (the key is minted through POST /api/keys first, the stand-in then serves the stored row).
+const ctl = vi.hoisted(() => ({
+  storedBoom: undefined as unknown,
+  lookupBoom: undefined as unknown,
+  usageBoom: undefined as unknown,
+  row: undefined as Record<string, unknown> | undefined,
+  lines: [] as Array<{ level: string; message: string; error: unknown }>,
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    error: (message: string, meta?: { error?: unknown }) => {
+      ctl.lines.push({ level: 'error', message, error: meta?.error });
+    },
+    warn: (message: string, meta?: { error?: unknown }) => {
+      ctl.lines.push({ level: 'warn', message, error: meta?.error });
+    },
+    info: () => undefined,
+    debug: () => undefined,
+  },
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  initDb: async () => true,
+  query: async (statement: string) => {
+    const s = String(statement);
+    if (/security_find_api_key_by_hash/i.test(s)) {
+      if (ctl.storedBoom !== undefined) return Promise.reject(ctl.storedBoom);
+      if (ctl.lookupBoom !== undefined) return Promise.reject(ctl.lookupBoom);
+      return { rows: ctl.row ? [ctl.row] : [], rowCount: ctl.row ? 1 : 0 };
+    }
+    if (/^\s*UPDATE\s+svc_api_keys\s+SET\s+last_used_at/i.test(s) && ctl.usageBoom !== undefined) return Promise.reject(ctl.usageBoom);
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
+const ORG_ID = '18680000-0000-4000-8000-000000001868';
+const TENANT_ID = 'c0000000-0000-4000-8000-000000001868';
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
+const MESSAGES = {
+  stored: 'KS-1370: stored API key state could not be read',
+  lookup: 'DB fallback for api-key validation failed',
+  usage: 'DB save API key failed',
+};
+const linesOf = (message: string) => ctl.lines.filter((l) => l.message === message).map((l) => ({ level: l.level, error: l.error }));
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
+// Mint a key, then make the stand-in serve its stored row; returns the plaintext key to validate.
+async function mintKey(): Promise<string> {
+  const minted = await call('POST', '/api/keys', { name: 'ks1868 validate', organizationId: ORG_ID, tenantId: TENANT_ID, scopes: ['documents:read'] });
+  const key = String(minted.body?.data?.key);
+  ctl.row = {
+    id: String(minted.body?.data?.id),
+    organization_id: ORG_ID,
+    tenant_id: TENANT_ID,
+    name: 'ks1868 validate',
+    key_hash: crypto.createHash('sha256').update(key).digest('hex'),
+    key_prefix: String(minted.body?.data?.prefix),
+    scopes: '["documents:read"]',
+    rate_limit: 1000,
+    rate_limit_window: 3600,
+    usage_count: 0,
+    is_active: true,
+    created_at: new Date().toISOString(),
+  };
+  return key;
+}
+const validate = (key: string) => call('POST', '/api/keys/validate', { key });
+const verdict = (r: { status: number; body: any }) => ({ status: r.status, valid: r.body?.data?.valid, reason: r.body?.data?.reason, code: r.body?.error?.code, message: r.body?.error?.message });
+const STORED_REFUSED = { status: 503, valid: undefined, reason: undefined, code: 'SERVICE_UNAVAILABLE', message: 'Unable to verify key' };
+const NOT_FOUND = { status: 200, valid: false, reason: 'Key not found', code: undefined, message: undefined };
+const VALID = { status: 200, valid: true, reason: undefined, code: undefined, message: undefined };
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
+  ctl.storedBoom = undefined;
+  ctl.lookupBoom = undefined;
+  ctl.usageBoom = undefined;
+  ctl.row = undefined;
+  ctl.lines.length = 0;
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
+describe('KS-1868 the catches of the validate route read the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error from the stored-state read logs its message and answers 503', async () => {
+    const key = await mintKey();
+    ctl.storedBoom = new Error('db down');
+    expect(verdict(await validate(key))).toEqual(STORED_REFUSED);
+    expect(linesOf(MESSAGES.stored)).toEqual([{ level: 'error', error: 'db down' }]);
+  });
+
+  it('control ks1868 C2 an ordinary Error from the cache-miss lookup logs its message and answers Key not found', async () => {
+    ctl.lookupBoom = new Error('db down');
+    expect(verdict(await validate('sk_ks1868_never_minted'))).toEqual(NOT_FOUND);
+    expect(linesOf(MESSAGES.lookup)).toEqual([{ level: 'warn', error: 'db down' }]);
+  });
+
+  it('control ks1868 C3 an ordinary Error from the usage write logs its message and the valid key is still answered valid', async () => {
+    const key = await mintKey();
+    ctl.usageBoom = new Error('db down');
+    expect(verdict(await validate(key))).toEqual(VALID);
+    expect(linesOf(MESSAGES.usage)).toEqual([{ level: 'error', error: 'db down' }]);
+  });
+
+  it('control ks1868 C4 a key whose reads and write land is answered valid and logs no failure', async () => {
+    const key = await mintKey();
+    expect(verdict(await validate(key))).toEqual(VALID);
+    expect(ctl.lines.filter((l) => Object.values(MESSAGES).includes(l.message))).toHaveLength(0);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy from the stored-state read is logged as the constant and answers 503', async () => {
+    const key = await mintKey();
+    ctl.storedBoom = revokedProxy();
+    expect(verdict(await validate(key))).toEqual(STORED_REFUSED);
+    expect(linesOf(MESSAGES.stored)).toEqual([{ level: 'error', error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws from the stored-state read is logged as the constant and answers 503', async () => {
+    const key = await mintKey();
+    ctl.storedBoom = messageGetterThrows();
+    expect(verdict(await validate(key))).toEqual(STORED_REFUSED);
+    expect(linesOf(MESSAGES.stored)).toEqual([{ level: 'error', error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R3 a revoked Proxy from the cache-miss lookup is logged as the constant and answers Key not found', async () => {
+    ctl.lookupBoom = revokedProxy();
+    expect(verdict(await validate('sk_ks1868_never_minted'))).toEqual(NOT_FOUND);
+    expect(linesOf(MESSAGES.lookup)).toEqual([{ level: 'warn', error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R4 an Error whose message getter throws from the cache-miss lookup is logged as the constant and answers Key not found', async () => {
+    ctl.lookupBoom = messageGetterThrows();
+    expect(verdict(await validate('sk_ks1868_never_minted'))).toEqual(NOT_FOUND);
+    expect(linesOf(MESSAGES.lookup)).toEqual([{ level: 'warn', error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R5 a revoked Proxy from the usage write is logged as the constant and the valid key is answered valid', async () => {
+    const key = await mintKey();
+    ctl.usageBoom = revokedProxy();
+    expect(verdict(await validate(key))).toEqual(VALID);
+    expect(linesOf(MESSAGES.usage)).toEqual([{ level: 'error', error: 'unreadable thrown value' }]);
+  });
+
+  it('RED ks1868 R6 an Error whose message getter throws from the usage write is logged as the constant and the valid key is answered valid', async () => {
+    const key = await mintKey();
+    ctl.usageBoom = messageGetterThrows();
+    expect(verdict(await validate(key))).toEqual(VALID);
+    expect(linesOf(MESSAGES.usage)).toEqual([{ level: 'error', error: 'unreadable thrown value' }]);
+  });
+});
```
