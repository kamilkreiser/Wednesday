# READY — KS-1009 (auth routes/wallet.ts: public GET /api/auth/wallet/status/:walletAddress stops disclosing the owner's userId/role/createdAt — :428 → `{ exists: true }` + 4 tsc-forced deletions :409 :410 :419 :420; + a new vitest file) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, 2026-09-17 13:29 (auth tier; checker f3ce186c with A3i)
# Source read by Wednesday (scratchpad cmp_brief.py, positive control = KS-623's known shift detected): product `-` 5/5 and `+` 1/1 IDENTICAL to the brief incl. indentation (A3i OK); apply was REANCHORED (the model's hunk headers). Test: 75 of 76 lines identical; line 42 is a COMMENT where the model dropped the quotes around 'no-body' and 'next-not-called'. **NORMALISED BY WEDNESDAY:** the product section below is regenerated from the tip (d7e95cd9f `git show`) with the brief's five edits and is BYTE-IDENTICAL to the checker's applied file (cmp, i.e. exactly what was tested 7/7); the test section is the brief's fence verbatim (only the line-42 comment differs from what ran). Both sections apply STRICT with `patch -F0`. Raw model output stays in local-model/runs/2026-09-17_ks1009-ornith35b-night.
# PR NOTES: `Refs KS-1009` (NOT Closes — the unregistered branch's `message` is kept; dropping it was a 6th edit). TIER 1. RESPONSE-SHAPE CHANGE for consumers OUTSIDE this repo (userId/role/createdAt no longer returned) — UNMEASURED; the published WalletStatusResponse requires only `exists` (spec unchanged). Follow-up for a Claude seat after #922: the route description text in auth.openapi.ts:1864-1868 and secuura-api.yaml:17732-17736 goes stale. Brief night/briefs/KS-1009.md; report night/briefs/NEXT_SEARCH_2026-09-17h.REPORT.md.

```diff
--- a/Blockchain/Dev/services/auth/src/routes/wallet.ts
+++ b/Blockchain/Dev/services/auth/src/routes/wallet.ts
@@ -406,8 +406,6 @@
 
     // Check DB for user with this wallet address
     let userId: string | null = null;
-    let role: string | null = null;
-    let createdAt: string | null = null;
 
     // KS-458: pre-auth wallet lookup — SECURITY DEFINER carve-out.
     const result = await query(
@@ -416,8 +414,6 @@
     );
     if (result.rows.length > 0) {
       userId = result.rows[0].id;
-      role = result.rows[0].role;
-      createdAt = result.rows[0].created_at;
     }
 
     if (!userId) {
@@ -425,7 +421,7 @@
       return;
     }
 
-    res.json({ exists: true, userId, role, createdAt });
+    res.json({ exists: true });
   } catch (error) {
     next(error);
   }
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1009-security-get-api-auth-wallet-status.test.ts
@@ -0,0 +1,76 @@
+/**
+ * KS-1009: GET /api/auth/wallet/status/:walletAddress tells a caller only
+ * whether the wallet is registered.
+ *
+ * The route is public by design (KS-720), so anyone holding a public Cardano
+ * address could resolve a REGISTERED wallet to the internal user id, role and
+ * creation time of its owner. Nothing in the repo consumes those three fields.
+ */
+import { describe, it, expect, vi } from 'vitest';
+
+vi.mock('../db', () => ({
+  query: vi.fn(async (sql: string, params: unknown[] = []) => {
+    if (String(sql).includes('auth_find_user_by_wallet') && params[0] === 'addr_test1ks1009registered') {
+      return { rows: [{ id: 'ks1009-user', role: 'OWNER', created_at: '2026-01-01T00:00:00.000Z' }], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 'ks1009-session' })),
+}));
+
+vi.mock('../services/jwt', () => ({
+  generateTokenPair: vi.fn(() => ({ accessToken: 'ks1009-access', refreshToken: 'ks1009-refresh', expiresIn: 900 })),
+}));
+
+vi.mock('../repositories/userRepo', () => ({}));
+
+import { query } from '../db';
+import { walletRoutes } from '../routes/wallet';
+
+const EXPECTED_CELLS = 2;
+let CELLS_RUN = 0;
+const REGISTERED = 'addr_test1ks1009registered';
+const UNREGISTERED = 'addr_test1ks1009unregistered';
+
+// [the JSON body the status route sent, or 'no-body'; the error next() received, or 'next-not-called']
+async function statusOf(walletAddress: string): Promise<unknown[]> {
+  const layer: any = (walletRoutes as any).stack.find((l: any) => l.route && l.route.path === '/status/:walletAddress');
+  let body: unknown = 'no-body';
+  let failed = 'next-not-called';
+  const req: any = { params: { walletAddress }, headers: {} };
+  const res: any = {
+    json: (b: unknown) => {
+      body = b;
+      return res;
+    },
+  };
+  await layer.route.stack[0].handle(req, res, (err?: any) => {
+    failed = err ? String(err.message) : 'next-called';
+  });
+  return [body, failed];
+}
+
+describe('KS-1009 - the public wallet status route answers exists and nothing else', () => {
+  it('KS-1009 R1 - a REGISTERED wallet answers exactly exists true, with no userId, role or createdAt', async () => {
+    CELLS_RUN += 1;
+    expect(await statusOf(REGISTERED)).toEqual([{ exists: true }, 'next-not-called']);
+  });
+  it('KS-1009 CONTROL - the route looks the address up, a registered wallet is exists true and an unregistered one exists false', async () => {
+    CELLS_RUN += 1;
+    vi.mocked(query).mockClear();
+    const registered: any = (await statusOf(REGISTERED))[0];
+    const unregistered: any = (await statusOf(UNREGISTERED))[0];
+    const looked = vi.mocked(query).mock.calls.map((c: any[]) => String(c[0]).includes('auth_find_user_by_wallet') && c[1][0]);
+    expect([registered.exists, unregistered.exists, 'userId' in unregistered, looked]).toEqual([true, false, false, [REGISTERED, UNREGISTERED]]);
+  });
+  it('KS-1009 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
