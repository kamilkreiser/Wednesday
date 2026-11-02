# READY — KS-1868-KS-1868-O82-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 21:25 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message-control-r5/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 21:25 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `0e3a9b65cdd632fbc1783257c6cb9833934e1404`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/auth.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	2	Blockchain/Dev/services/auth/src/routes/auth.ts
310	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: auth.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/auth.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/auth.ts 4 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts 310 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (8 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=8 of total=12; red cell(s): ['KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R1 login: a rehash rejection whose message is a revoked Proxy logs the constant reason and the login answers 200 with tokens', 'KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R2 login: a rehash rejection whose message is an object whose toString throws logs the constant reason and the login answers 200 with tokens', 'KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R3 login: a rehash rejection whose message is a null-prototype object logs the constant reason and the login answers 200 with tokens', 'KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R4 login: a rehash rejection whose message is a Symbol logs the Symbol text and the login answers 200 with tokens', 'KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R5 logout: a denylist rejection whose message is a revoked Proxy logs the constant reason and the logout answers 200 and clears the cookie', 'KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R6 logout: a denylist rejection whose message is an object whose toString throws logs the constant reason and the logout answers 200 and clears the cookie', 'KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R7 logout: a denylist rejection whose message is a null-prototype object logs the constant reason and the logout answers 200 and clears the cookie', 'KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message RED ks1868 R8 logout: a denylist rejection whose message is a Symbol logs the Symbol text and the logout answers 200 and clears the cookie']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1492 failed=3 | after: total=1504 failed=1` · `NEW reds: []` [baseline_suite.json total=1492 failed=3; after_suite.json total=1504 failed=1]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+4/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts` (+310/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/auth.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `0e3a9b65cdd632fbc1783257c6cb9833934e1404` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p1_auth_login_rehash_logout_denylist_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/auth.ts b/Blockchain/Dev/services/auth/src/routes/auth.ts
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -554,7 +554,8 @@
       } catch (err: any) {
         let reason: string;
         try {
-          reason = err?.message;
+          const m = err?.message;
+          reason = m === undefined || m === null ? m : String(m);
         } catch {
           reason = 'unreadable thrown value';
         }
@@ -789,7 +790,8 @@
         await denylistRefreshJti(decoded.jti, remaining).catch((err) => {
           let reason: string;
           try {
-            reason = err?.message;
+            const m = err?.message;
+            reason = m === undefined || m === null ? m : String(m);
           } catch {
             reason = 'unreadable thrown value';
           }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,310 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1868 (QA gate 113, G113-F1): the login UPGRADE-ON-VERIFY rehash catch and the logout denylist `.catch` in routes/auth.ts
+// log `{ error: reason }` where `reason` is whatever `err?.message` returned. PR 1931 guards the READ; a message that is
+// readable but not a string (a revoked Proxy, an object whose toString throws, a null-prototype object, a Symbol) is passed
+// to the logger as is, and the real winston throws while formatting it. The cells reject with an Error whose `message`
+// getter RETURNS such a value and assert the logged reason is text (the constant when it cannot be turned into text), with
+// the login still 200 with tokens and the logout still 200 with the cookie cleared (the outcome an ordinary Error gets).
+// A thrown plain string has no message and is logged with no `error`; that is pinned too. Harness: the ks1868 rehash and
+// logout test (real router and error handler; the repository, password, session, jwt, lockout, mail and bus mocked; the
+// stand-ins reject with a plain function, not a vi.fn()).
+const h = vi.hoisted(() => ({
+  rehashRejects: false,
+  denylistRejects: false,
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  unhandled: 0,
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  error: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: capture, createLogger: () => capture }));
+
+const LOGIN_EMAIL = 'ks1868-login@secuura.local';
+const ACTIVE_USER = {
+  id: 'user-1868-login', email: LOGIN_EMAIL, status: 'ACTIVE', role: 'OWNER',
+  verificationLevel: 'BASIC', mfaEnabled: false, mfaSecret: null, mfaBackupCodes: null,
+  passwordHash: '$argon2id$stub', tenantId: 'ten-1', organizationId: 'org-1',
+};
+
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [], rowCount: 0 })) }));
+
+vi.mock('../repositories/userRepo', () => ({
+  getPlatformAdmin: vi.fn(async () => null),
+  getUserByEmail: vi.fn(async (email: string) =>
+    email.toLowerCase().trim() === LOGIN_EMAIL ? { ...ACTIVE_USER } : null),
+  getUserById: vi.fn(async () => null),
+  getUserByIdPreAuth: vi.fn(async () => ({ ...ACTIVE_USER })),
+  getUserBySocialId: vi.fn(async () => null),
+  createUser: vi.fn(async () => null),
+  updateUser: (_id: string, patch: Record<string, unknown>) =>
+    patch && 'passwordHash' in patch && h.rehashRejects ? Promise.reject(h.toThrow) : Promise.resolve({ ...ACTIVE_USER }),
+  updateUserOrThrow: vi.fn(async () => ({ ...ACTIVE_USER })),
+  updateUserPlatformScope: vi.fn(async () => null),
+  updatePlatformAdminPassword: vi.fn(async () => undefined),
+  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
+  reencryptPlatformAdminMfaSecretIfLegacy: vi.fn(async () => undefined),
+}));
+
+vi.mock('../services/password', () => ({
+  verifyPassword: vi.fn(async () => true),
+  hashPassword: vi.fn(async () => '$argon2id$stub'),
+  checkPasswordStrength: vi.fn(() => ({ ok: true })),
+  generateResetToken: vi.fn(() => 'tok'),
+  shouldRehashAfterVerify: vi.fn(() => true),
+}));
+
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 'sess-1868-login' })),
+  revokeSession: vi.fn(async () => undefined),
+  revokeAllUserSessions: vi.fn(async () => 0),
+  getSession: vi.fn(async () => null),
+  rotateSessionRefreshToken: vi.fn(async () => undefined),
+  getRedisClient: vi.fn(() => null),
+  validateSession: vi.fn(async () => true),
+  updateSessionActivity: vi.fn(async () => undefined),
+  isRedisAvailable: vi.fn(() => true),
+}));
+
+vi.mock('../services/jwt', () => ({
+  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_1868_LOGIN', refreshToken: 'MINTED_1868_LOGIN_R', expiresIn: 900 })),
+  verifyRefreshToken: vi.fn(() => ({})),
+  decodeToken: vi.fn(() => ({ jti: 'jti-1868', exp: Math.floor(Date.now() / 1000) + 3600 })),
+}));
+
+vi.mock('../services/refreshDenylist', () => ({
+  isRefreshJtiDenylisted: vi.fn(async () => false),
+  denylistRefreshJti: (_jti: string, _ttl: number) => (h.denylistRejects ? Promise.reject(h.toThrow) : Promise.resolve(undefined)),
+}));
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => 1),
+  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
+}));
+vi.mock('../services/email', () => ({
+  sendVerificationEmail: vi.fn(async () => undefined),
+  sendPasswordResetEmail: vi.fn(async () => undefined),
+}));
+
+// Used BOTH as mounted middleware and as a factory across the route tree; this stub detects which shape it was
+// given (the ks781 / ks1157 harness pattern).
+const passThrough = (...args: unknown[]) => {
+  if (args.length >= 3 && typeof args[2] === 'function') return (args[2] as () => void)();
+  return (_r: unknown, _s: unknown, n: () => void) => n();
+};
+vi.mock('../middleware/authenticate', () => ({
+  authenticate: passThrough, authenticateToken: passThrough,
+  authenticateAccessOrConnector: passThrough, optionalAuthenticate: passThrough,
+  requireRole: passThrough,
+}));
+vi.mock('../middleware/tenantGuc', () => ({ seedTenantGuc: (_r: unknown, _s: unknown, n: () => void) => n() }));
+vi.mock('../events', () => ({
+  publishEvent: () => Promise.resolve(undefined),
+  EventTypes: { USER_LOGIN: 'user.login' },
+}));
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
+  const { authRoutes } = await import('../routes/auth');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  const app = express();
+  app.use(express.json());
+  app.use((req, _res, next) => {
+    (req as unknown as { cookies: Record<string, string> }).cookies = { refresh_token: 'RT_1868' };
+    next();
+  });
+  app.use('/api/auth', authRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+beforeEach(() => {
+  h.rehashRejects = false;
+  h.denylistRejects = false;
+  h.toThrow = undefined;
+  h.logged = [];
+  h.unhandled = 0;
+});
+
+const REHASH_LINES = () => h.logged.filter((c) => c[0] === 'UPGRADE-ON-VERIFY rehash failed (non-fatal)');
+const LOGOUT_LINES = () => h.logged.filter((c) => c[0] === 'Logout denylist failed (non-fatal)');
+
+async function login(): Promise<{ status: number; minted: boolean } | null> {
+  try {
+    const res = await fetch(baseUrl + '/api/auth/login', {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json' },
+      body: JSON.stringify({ email: LOGIN_EMAIL, password: 'pw-correct-horse' }),
+      signal: AbortSignal.timeout(2000),
+    });
+    const text = await res.text();
+    return { status: res.status, minted: text.includes('MINTED_1868_LOGIN') };
+  } catch {
+    return null;
+  }
+}
+
+async function logout(): Promise<{ status: number; clearedCookie: boolean; ok: boolean } | null> {
+  try {
+    const res = await fetch(baseUrl + '/api/auth/logout', { method: 'POST', signal: AbortSignal.timeout(2000) });
+    const text = await res.text();
+    return {
+      status: res.status,
+      clearedCookie: (res.headers.get('set-cookie') || '').includes('refresh_token=;'),
+      ok: text.includes('Logged out successfully'),
+    };
+  } catch {
+    return null;
+  }
+}
+
+const LOGIN_OK = { status: 200, minted: true };
+const LOGOUT_OK = { status: 200, clearedCookie: true, ok: true };
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const toStringThrows = (): unknown => ({
+  toString() {
+    throw new Error('ts boom');
+  },
+});
+/** An Error whose `message` getter succeeds and returns the (non-string) value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+const SHAPES: Array<[string, () => unknown, string]> = [
+  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
+  ['an object whose toString throws', toStringThrows, 'unreadable thrown value'],
+  ['a null-prototype object', () => Object.create(null), 'unreadable thrown value'],
+  ['a Symbol', () => Symbol('ks1868'), 'Symbol(ks1868)'],
+];
+
+describe('KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message', () => {
+  it('control ks1868 C1 login: an ordinary Error from the rehash write is logged with its message and the login answers 200 with tokens', async () => {
+    h.rehashRejects = true;
+    h.toThrow = new Error('db down');
+    expect(await login()).toEqual(LOGIN_OK);
+    expect(REHASH_LINES()).toHaveLength(1);
+    expect(reasonOf(REHASH_LINES()[0])).toBe('db down');
+  });
+
+  it('control ks1868 C2 logout: an ordinary Error from the denylist write is logged with its message and the logout answers 200 and clears the cookie', async () => {
+    h.denylistRejects = true;
+    h.toThrow = new Error('redis down');
+    expect(await logout()).toEqual(LOGOUT_OK);
+    expect(LOGOUT_LINES()).toHaveLength(1);
+    expect(reasonOf(LOGOUT_LINES()[0])).toBe('redis down');
+  });
+
+  it('control ks1868 C3 login: a thrown plain string has no message and is logged with no error field (not the text undefined)', async () => {
+    h.rehashRejects = true;
+    h.toThrow = 'plain boom';
+    expect(await login()).toEqual(LOGIN_OK);
+    expect(REHASH_LINES()).toHaveLength(1);
+    expect(reasonOf(REHASH_LINES()[0])).toBe('<undefined>');
+  });
+
+  it('control ks1868 C4 logout: a thrown plain string has no message and is logged with no error field (not the text undefined)', async () => {
+    h.denylistRejects = true;
+    h.toThrow = 'plain boom';
+    expect(await logout()).toEqual(LOGOUT_OK);
+    expect(LOGOUT_LINES()).toHaveLength(1);
+    expect(reasonOf(LOGOUT_LINES()[0])).toBe('<undefined>');
+  });
+
+  it('RED ks1868 R1 login: a rehash rejection whose message is a revoked Proxy logs the constant reason and the login answers 200 with tokens', async () => {
+    h.rehashRejects = true;
+    h.toThrow = withMessage(SHAPES[0][1]());
+    expect(await login()).toEqual(LOGIN_OK);
+    expect(REHASH_LINES()).toHaveLength(1);
+    expect(reasonOf(REHASH_LINES()[0])).toBe(SHAPES[0][2]);
+  });
+
+  it('RED ks1868 R2 login: a rehash rejection whose message is an object whose toString throws logs the constant reason and the login answers 200 with tokens', async () => {
+    h.rehashRejects = true;
+    h.toThrow = withMessage(SHAPES[1][1]());
+    expect(await login()).toEqual(LOGIN_OK);
+    expect(REHASH_LINES()).toHaveLength(1);
+    expect(reasonOf(REHASH_LINES()[0])).toBe(SHAPES[1][2]);
+  });
+
+  it('RED ks1868 R3 login: a rehash rejection whose message is a null-prototype object logs the constant reason and the login answers 200 with tokens', async () => {
+    h.rehashRejects = true;
+    h.toThrow = withMessage(SHAPES[2][1]());
+    expect(await login()).toEqual(LOGIN_OK);
+    expect(REHASH_LINES()).toHaveLength(1);
+    expect(reasonOf(REHASH_LINES()[0])).toBe(SHAPES[2][2]);
+  });
+
+  it('RED ks1868 R4 login: a rehash rejection whose message is a Symbol logs the Symbol text and the login answers 200 with tokens', async () => {
+    h.rehashRejects = true;
+    h.toThrow = withMessage(SHAPES[3][1]());
+    expect(await login()).toEqual(LOGIN_OK);
+    expect(REHASH_LINES()).toHaveLength(1);
+    expect(reasonOf(REHASH_LINES()[0])).toBe(SHAPES[3][2]);
+  });
+
+  it('RED ks1868 R5 logout: a denylist rejection whose message is a revoked Proxy logs the constant reason and the logout answers 200 and clears the cookie', async () => {
+    h.denylistRejects = true;
+    h.toThrow = withMessage(SHAPES[0][1]());
+    expect(await logout()).toEqual(LOGOUT_OK);
+    expect(LOGOUT_LINES()).toHaveLength(1);
+    expect(reasonOf(LOGOUT_LINES()[0])).toBe(SHAPES[0][2]);
+  });
+
+  it('RED ks1868 R6 logout: a denylist rejection whose message is an object whose toString throws logs the constant reason and the logout answers 200 and clears the cookie', async () => {
+    h.denylistRejects = true;
+    h.toThrow = withMessage(SHAPES[1][1]());
+    expect(await logout()).toEqual(LOGOUT_OK);
+    expect(LOGOUT_LINES()).toHaveLength(1);
+    expect(reasonOf(LOGOUT_LINES()[0])).toBe(SHAPES[1][2]);
+  });
+
+  it('RED ks1868 R7 logout: a denylist rejection whose message is a null-prototype object logs the constant reason and the logout answers 200 and clears the cookie', async () => {
+    h.denylistRejects = true;
+    h.toThrow = withMessage(SHAPES[2][1]());
+    expect(await logout()).toEqual(LOGOUT_OK);
+    expect(LOGOUT_LINES()).toHaveLength(1);
+    expect(reasonOf(LOGOUT_LINES()[0])).toBe(SHAPES[2][2]);
+  });
+
+  it('RED ks1868 R8 logout: a denylist rejection whose message is a Symbol logs the Symbol text and the logout answers 200 and clears the cookie', async () => {
+    h.denylistRejects = true;
+    h.toThrow = withMessage(SHAPES[3][1]());
+    expect(await logout()).toEqual(LOGOUT_OK);
+    expect(LOGOUT_LINES()).toHaveLength(1);
+    expect(reasonOf(LOGOUT_LINES()[0])).toBe(SHAPES[3][2]);
+  });
+});
```
