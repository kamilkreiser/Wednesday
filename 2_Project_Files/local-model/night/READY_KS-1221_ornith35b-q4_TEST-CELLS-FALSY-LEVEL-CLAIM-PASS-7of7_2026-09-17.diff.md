# READY — KS-1221 (test-only, api-gateway ks744 test — cells R4 (empty-string) + R5 (null) verificationLevel claims forward no x-verification-level; completeness 4 -> 6)
# Source read by Wednesday 22:18: the model's 13 +/- lines (+12/-1) IDENTICAL to the brief's two fences (python sequence compare; a mutated copy unequal); checker RESULT PASS (7/7) first sample, apply_mode=FUZZY; A4 R4+R5 red by assertion under the :398 undefined-only tamper; A6 no new red; A7 tsc rc 0. Tip = develop 0a2b1603f.
# PR NOTES: `Closes KS-1221` defensible once merged (the ticket's recommendation is exactly these two cells; confirm at raise); KS-744 stays In Progress (§5f). TIER 2. Re-derive hunk headers at raise (fuzzy apply). Not in scope, candidate follow-up: a falsy EMAIL claim (:393) and 0/false. Run: runs/2026-09-17_ks1221-ornith35b-night/out.md.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks744-a-token-missing-a-claim-is-proxied-not-500.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks744-a-token-missing-a-claim-is-proxied-not-500.test.ts
@@ -16,7 +16,7 @@ import type { AddressInfo } from 'net';
 import { createProxyMiddleware } from 'http-proxy-middleware';
 import { authenticateToken } from '../middleware/auth';
 
-const EXPECTED_CELLS = 4;
+const EXPECTED_CELLS = 6;
 let CELLS_RUN = 0;
 const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';
 const FULL: Record<string, string> = { userId: 'u-ks744', email: 'ks744@example.test', role: 'user', verificationLevel: 'basic', tenantId: 't-ks744' };
@@ -82,6 +82,17 @@ describe('KS-744 - a verified token missing a claim is proxied, not answered 50
 
     CELLS_RUN += 1;
     expect(await verdict(tokenWithout('verificationLevel'), 'x-verification-level', { 'x-verification-level': 'enhanced' })).toEqual([200, 1, null]);
   });
+  it('KS-744 R4 - an empty-string verificationLevel claim: 200, one upstream hit, no x-verification-level forwarded', async () => {
+    CELLS_RUN += 1;
+    // KS-1221: a FALSY claim is dropped exactly like a missing one, so a guard that tests only for undefined reds here.
+    const emptyLevel = jwt.sign({ ...FULL, verificationLevel: '' }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
+    expect(await verdict(emptyLevel, 'x-verification-level', {})).toEqual([200, 1, null]);
+  });
+  it('KS-744 R5 - a null verificationLevel claim: 200, one upstream hit, no x-verification-level forwarded', async () => {
+    CELLS_RUN += 1;
+    const nullLevel = jwt.sign({ ...FULL, verificationLevel: null }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
+    expect(await verdict(nullLevel, 'x-verification-level', {})).toEqual([200, 1, null]);
+  });
   it('KS-744 CONTROL - a token carrying every claim forwards the email and the level', async () => {
     CELLS_RUN += 1;
     expect(await verdict(tokenWithout('none'), 'x-user-email', {})).toEqual([200, 1, 'ks744@example.test']);
```
