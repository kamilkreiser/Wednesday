# READY — KS-623 (auth middleware/authenticate.ts:21: test tokens refused unless NODE_ENV is in the ['development','test'] allowlist — the gateway's rule; + a new vitest file, R1 NODE_ENV unset, R2 staging, + control + completeness) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, 2026-09-17 13:07 (auth tier)
# Source read by Wednesday: the test file's 81 `+` lines IDENTICAL to the brief fence (a mutated copy unequal). The product hunk's `-`/`+` TEXT matches the brief, BUT the model shifted EVERY line of that hunk right by 2 spaces; the checker applied it FUZZY (-C1) and wrote the fixed line at 4-space indent into a 2-space block (read in the checker clone at :21). Code and semantics identical, suite 755/755, tsc rc 0. **NORMALISED BY WEDNESDAY:** the product section below is regenerated from the tip (d7e95cd9f, `git show`) with the brief's exact `+` line at 2-space indent — the model's text, the file's indentation. The raw model output stays in the run dir. IMPROVEMENTS row written (the fuzzy apply does not check leading whitespace).
# PR NOTES: `Refs KS-623` (NOT Closes — the 'one shared helper' half would touch gateway middleware/auth.ts, a partitioned file). TIER 1. BEHAVIOUR CHANGE: an auth service with NODE_ENV unset or e.g. 'staging' and ENABLE_TEST_TOKENS=true now REFUSES test tokens; the gateway's /api/auth mount does not authenticate, so this check is the only one there. Local compose sets NODE_ENV=development (unchanged). **kintsugi/demo NODE_ENV UNMEASURED — measure before any deploy.** Brief night/briefs/KS-623.md; report night/briefs/NEXT_SEARCH_2026-09-17g.REPORT.md.

```diff
--- a/Blockchain/Dev/services/auth/src/middleware/authenticate.ts
+++ b/Blockchain/Dev/services/auth/src/middleware/authenticate.ts
@@ -18,7 +18,7 @@
  */
 function parseTestToken(token: string): JwtPayload | null {
   // SECURITY: Never accept test tokens in production
-  if (process.env.NODE_ENV === 'production') {
+  if (!['development', 'test'].includes(process.env.NODE_ENV || '')) {
     return null;
   }
   // Require explicit opt-in for test tokens
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks623-test-token-env-guard-is-asymmetric.test.ts
@@ -0,0 +1,81 @@
+/**
+ * KS-623: the auth service's test-token guard is an ALLOWLIST, like the gateway's.
+ *
+ * services/auth parseTestToken refused test tokens only when NODE_ENV was
+ * exactly 'production', so with NODE_ENV unset (or 'staging') and
+ * ENABLE_TEST_TOKENS=true an unsigned test_token_ self-asserted a user and a
+ * role. The gateway already refuses unless NODE_ENV is 'development' or 'test'.
+ */
+import { describe, it, expect, vi } from 'vitest';
+
+vi.mock('../services/jwt', () => ({
+  verifyAccessToken: vi.fn(() => {
+    throw new Error('ks623-not-a-real-jwt');
+  }),
+  verifyConnectorToken: vi.fn(() => {
+    throw new Error('ks623-not-a-real-jwt');
+  }),
+}));
+
+vi.mock('../services/session', () => ({
+  validateSession: vi.fn(async () => true),
+  updateSessionActivity: vi.fn(async () => undefined),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+import { authenticate } from '../middleware/authenticate';
+
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+const UNSET = 'ks623-unset';
+const USER = 'ks623-user';
+const NOT_A_JWT = 'ks623-not-a-real-jwt';
+const TOKEN = 'test_token_' + Buffer.from(JSON.stringify({ sub: USER, role: 'ISSUER' })).toString('base64');
+const ACCEPTED = [USER, 'next-ok'];
+const REFUSED = ['no-user', NOT_A_JWT];
+
+// [the user authenticate() attached, or 'no-user'; the error next() received, or 'next-ok']
+async function verdict(nodeEnv: string, enable: string): Promise<string[]> {
+  const saved = { ...process.env };
+  if (nodeEnv === UNSET) delete process.env.NODE_ENV;
+  else process.env.NODE_ENV = nodeEnv;
+  if (enable === UNSET) delete process.env.ENABLE_TEST_TOKENS;
+  else process.env.ENABLE_TEST_TOKENS = enable;
+  try {
+    const req: any = { headers: { authorization: 'Bearer ' + TOKEN } };
+    let seen = 'next-not-called';
+    await authenticate()(req, {} as any, (err?: any) => {
+      seen = err ? String(err.message) : 'next-ok';
+    });
+    return [req.user ? String(req.user.userId) : 'no-user', seen];
+  } finally {
+    process.env = saved;
+  }
+}
+
+describe('KS-623 - the auth service refuses test tokens unless NODE_ENV is development or test', () => {
+  it('KS-623 R1 - NODE_ENV unset with ENABLE_TEST_TOKENS=true: the test token is refused', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(UNSET, 'true')).toEqual(REFUSED);
+  });
+  it('KS-623 R2 - NODE_ENV=staging with ENABLE_TEST_TOKENS=true: the test token is refused', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict('staging', 'true')).toEqual(REFUSED);
+  });
+  it('KS-623 CONTROL - development and test still accept the token; production and a missing opt-in still refuse it', async () => {
+    CELLS_RUN += 1;
+    const seen = [
+      await verdict('development', 'true'),
+      await verdict('test', 'true'),
+      await verdict('production', 'true'),
+      await verdict('test', UNSET),
+    ];
+    expect(seen).toEqual([ACCEPTED, ACCEPTED, REFUSED, REFUSED]);
+  });
+  it('KS-623 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
