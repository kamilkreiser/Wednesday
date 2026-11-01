# READY — KS-1868-KS-1868-O50-P2 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-r2/out.md.checker/patch.diff`** (from `ls` at 01:26 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/auth/src/routes/auth.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/auth/src/routes/auth.ts): `error: patch failed: Blockchain/Dev/services/auth/src/routes/auth.ts:609` (apply with the options recorded in section_<k>.opts; the raise seat states which); CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 01:26 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8afcf256ed5fb38d05f7273e08e1b912446bac5c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/auth.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	1	Blockchain/Dev/services/auth/src/routes/auth.ts
210	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (9 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: auth.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/auth.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/auth.ts 9 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts 210 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/auth/src/routes/auth.ts:609`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 the login publish catch handler reads the rejection value safely RED ks1868 R1 a revoked Proxy rejection logs a constant reason and leaves no unhandled rejection', 'KS-1868 the login publish catch handler reads the rejection value safely RED ks1868 R2 an Error whose message getter throws logs a constant reason and leaves no unhandled rejection']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1459 failed=3 | after: total=1463 failed=2` · `NEW reds: []` [baseline_suite.json total=1459 failed=3; after_suite.json total=1463 failed=2]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+9/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts` (+210/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/auth.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8afcf256ed5fb38d05f7273e08e1b912446bac5c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o50_p2_auth_login_publish_event_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw-r2/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -609,4 +609,12 @@
       email: user.email,
       role: user.role,
       ip: req.ip,
-    }).catch(err => logger.error('Failed to publish event', { error: err instanceof Error ? err.message : String(err) }));
+    }).catch(err => {
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to publish event', { error: reason });
+    });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts
@@ -0,0 +1,210 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1868: POST /login publishes user.login fire-and-forget; when that publish REJECTS, the route's `.catch`
+// handler must still log its line `Failed to publish event` even if the rejection value cannot be read (a
+// revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`). Today such
+// a value makes the `.catch` handler itself throw, so the derived promise rejects with nothing attached and Node
+// sees an UNHANDLED REJECTION (the login response was already sent). The cells count unhandled rejections
+// themselves instead of letting the runner report them. Harness: the ks1157 route test (real router and error
+// handler; repository, password, session, jwt, lockout, mail and event bus mocked). The event bus stand-in
+// rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could itself fail on a
+// revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  publishRejects: false,
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  unhandled: 0,
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
+  updateUser: vi.fn(async () => ({ ...ACTIVE_USER })),
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
+  shouldRehashAfterVerify: vi.fn(() => false),
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
+  decodeToken: vi.fn(() => ({})),
+}));
+
+vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
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
+  publishEvent: () => (h.publishRejects ? Promise.reject(h.toThrow) : Promise.resolve(undefined)),
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
+  h.publishRejects = false;
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  h.unhandled = 0;
+});
+
+const LINES = () => h.logged.filter((c) => c[0] === 'Failed to publish event');
+
+async function login(): Promise<{ status: number; minted: boolean }> {
+  const res = await fetch(baseUrl + '/api/auth/login', {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ email: LOGIN_EMAIL, password: 'pw-correct-horse' }),
+  });
+  const text = await res.text();
+  return { status: res.status, minted: text.includes('MINTED_1868_LOGIN') };
+}
+
+/** The publish is fire-and-forget: wait until its outcome shows (a log line or an unhandled rejection), then a little longer. */
+async function settled(): Promise<void> {
+  const deadline = Date.now() + 1500;
+  while (Date.now() < deadline && LINES().length === 0 && h.unhandled === 0) {
+    await new Promise((resolve) => setTimeout(resolve, 10));
+  }
+  await new Promise((resolve) => setTimeout(resolve, 60));
+}
+
+describe('KS-1868 the login publish catch handler reads the rejection value safely', () => {
+  it('control ks1868 C1 an ordinary Error still logs its message and the login still answers 200 with tokens', async () => {
+    h.publishRejects = true;
+    h.toThrow = new Error('bus down');
+    expect(await login()).toEqual({ status: 200, minted: true });
+    await settled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'bus down' });
+  });
+
+  it('control ks1868 C2 a publish that succeeds logs no failure line and answers 200 with tokens', async () => {
+    expect(await login()).toEqual({ status: 200, minted: true });
+    await settled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(0);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy rejection logs a constant reason and leaves no unhandled rejection', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.publishRejects = true;
+    h.toThrow = proxy;
+    expect(await login()).toEqual({ status: 200, minted: true });
+    await settled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and leaves no unhandled rejection', async () => {
+    h.publishRejects = true;
+    h.toThrow = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(await login()).toEqual({ status: 200, minted: true });
+    await settled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```

## OPERATOR 50 NOTES (appended by the operator, not by hold_ready)
- SECURITY SURFACE: services/auth/src/routes/auth.ts. The raise of this pass will be gated tier 1.
- Behaviour change the raise PR must state: a rejection from publishEvent that cannot be read today throws inside the .catch handler, giving an UNHANDLED REJECTION in the auth process after the response was sent (auth installs no unhandledRejection handler; node:24-alpine; only the gateway sets UNHANDLED_REJECTION_MODE=survive), so under Node's default the process would exit; after the fix it logs 'unreadable thrown value'. The HTTP response is unchanged. publishEvent (src/events.ts) swallows its own errors, so at this tip the handler is defence in depth and is not reached today. Read from source and the Dockerfile, not run. (LOGIN route, :612, runs on every successful password login)
- Apply with: git apply -C1 <patch.diff> (the plain strict apply and plain patch both refuse the product hunk: the hunk has 3 leading and 0 trailing context lines because the next line is blank and build_input refuses blank context; git treats that as anchored to end of file). Canonical run is the -r2 re-run: the first real round's patch was byte-identical to the golden but its A6 went red on the ks949 timeout; r2's model output omitted the 'diff --git' line of section 1 (content equals the golden; golden-compare says DIFFERS only for that header line).
- Combined with the other two passes (applied in order P3, P1, P2 to a scratch clone at the tip): the 3 new test files 12/12 green together; tsc -p tsconfig.test.json 42 errors = the 42 baseline errors, 0 in the new files. Whole-suite combined run UNMEASURED.
- The checker's whole-suite step A6 can go red on ks949-platform-admin-seed-identity.test.ts ('enumeration actually finds seed sites' / 'no executable seed site ... real address'): those two cells run 3.4-4.1 s at baseline against a 5 s timeout and timed out under load in 4 of 10 whole-suite runs of this session (see report). It is a pre-existing timing flake, not caused by the patch; re-run before reading it as a red.
