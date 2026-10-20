# READY — KS-1689-NEEDSREAUTH-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1/out.md.checker/patch.diff`** (from `ls` at 14:48 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 14:48 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `561a6c5b528289f4d7ecd19f9c069501e925e9ea`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/m365-integration/src/index.ts , Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/index.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/m365-integration/src/index.ts
148	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/m365-integration/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts fails at the untouched tip (7 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=7 of total=9; red cell(s): ['KS-1689: the connection status read says when the user must sign in again RED KS-1689 R1: a connected connection that holds a refresh token does not need to sign in again', 'KS-1689: the connection status read says when the user must sign in again RED KS-1689 R2: a connected connection with no refresh token needs to sign in again', 'KS-1689: the connection status read says when the user must sign in again RED KS-1689 R3: a connected connection whose stored refresh token cannot be decrypted needs to sign in again', 'KS-1689: the connection status read says when the user must sign in again RED KS-1689 R4: a disconnected connection (token cleared) is not flagged', 'KS-1689: the connection status read says when the user must sign in again RED KS-1689 R5: a connection in the error status with no token is not flagged', 'KS-1689: the connection status read says when the user must sign in again RED KS-1689 R6: a pending connection with no token is not flagged', 'KS-1689: the connection status read says when the user must sign in again RED KS-1689 R7: disconnecting a connected connection that held a token clears the token and the status read then says disconnected, not flagged']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts passes with the product hunk (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=252 failed=0 | after: total=261 failed=0` · `NEW reds: []` [baseline_suite.json total=252 failed=0; after_suite.json total=261 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +150/-0 test=src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/index.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts` (+148/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `561a6c5b528289f4d7ecd19f9c069501e925e9ea` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1689_p1/KS-1689.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/m365-integration/src/index.ts b/Blockchain/Dev/services/m365-integration/src/index.ts
--- a/Blockchain/Dev/services/m365-integration/src/index.ts
+++ b/Blockchain/Dev/services/m365-integration/src/index.ts
@@ -794,2 +794,4 @@
       tokenExpired: connection.tokenExpiresAt ? connection.tokenExpiresAt < new Date() : true,
+      // KS-1689: derived, not stored. A connected connection with no usable refresh token (a fail-closed exchange stores none; a token that cannot be decrypted reads as none) can never refresh, so the user must sign in again.
+      needsReauth: connection.status === 'connected' && !connection.refreshToken,
     },
diff --git a/Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts
@@ -0,0 +1,148 @@
+/**
+ * KS-1689 - the m365 connection STATUS read says when the user must sign in again.
+ *
+ * A Microsoft 365 sign-in that fails closed stores NO refresh token but still leaves the connection
+ * 'connected'; about an hour later it is stuck for good and nothing says so. The status read
+ * (GET /api/connections/:id) now carries a derived flag `needsReauth`, true exactly when the stored
+ * status is 'connected' and the connection holds no usable refresh token (absent, or a stored token
+ * that cannot be decrypted, which reads as absent). It is not a stored status: no write path changes.
+ *
+ * Mocked: `../db` (so rows arrive through the service's own loadFromDb), `authenticate` out of
+ * `@secuura/shared` (so a cell can choose the caller) and express's `listen`. Everything else stays real
+ * and is driven over an HTTP listener on 127.0.0.1.
+ */
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'http';
+
+process.env.NODE_ENV = 'test';
+process.env.FRONTEND_URL = 'http://frontend.test';
+process.env.ENTRA_CLIENT_ID = 'test-client-id';
+process.env.ENTRA_CLIENT_SECRET = 'test-client-secret';
+process.env.ENTRA_TENANT_ID = 'test-entra-tenant';
+
+const ORG = '00000000-0000-4000-8000-0000000000a1';
+const seen = vi.hoisted(() => ({ warmed: false }));
+const now = '2026-10-01T00:00:00.000Z';
+const row = (id: string, status: string, refreshToken: string | null) => ({
+  id, organization_id: ORG, tenant_id: 'entra-dir', tenant_name: `tenant of ${id}`, status,
+  access_token: `plaintext-access-${id}`, refresh_token: refreshToken,
+  token_expires_at: '2099-01-01T00:00:00.000Z', scopes: ['User.Read'],
+  connected_at: now, last_sync_at: null, error_message: null, created_at: now, updated_at: now,
+});
+
+const C_TOKEN = 'conn_with_token';
+const C_NONE = 'conn_no_token';
+const C_BAD = 'conn_undecryptable';
+const C_DISCONNECTED = 'conn_disconnected';
+const C_ERROR = 'conn_error';
+const C_PENDING = 'conn_pending';
+const C_DELETE = 'conn_to_disconnect';
+
+vi.mock('../db', () => ({
+  initDb: async (onReady?: () => Promise<void>) => { await onReady?.(); },
+  isDbAvailable: () => true,
+  query: async (sql: string) => {
+    if (/SELECT \* FROM svc_m365_connections\s*$/.test(String(sql))) {
+      seen.warmed = true;
+      return { rows: [
+        row(C_TOKEN, 'connected', 'plain-refresh-token'),
+        row(C_NONE, 'connected', null),
+        row(C_BAD, 'connected', 'v1:this-is-not-a-ciphertext-for-this-row'),
+        row(C_DISCONNECTED, 'disconnected', null),
+        row(C_ERROR, 'error', null),
+        row(C_PENDING, 'pending', null),
+        row(C_DELETE, 'connected', 'plain-refresh-token-2'),
+      ] };
+    }
+    return { rows: [] };
+  },
+}));
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    authenticate: () => (req: any, _res: any, next: any) => { req.user = { userId: 'tester', role: 'ADMIN', organizationId: ORG }; next(); },
+  };
+});
+
+vi.mock('express', async (importOriginal) => {
+  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
+  const factory: any = (...args: any[]) => {
+    const app = actual(...args);
+    app.listen = (_p: any, cb?: () => void) => { setTimeout(() => cb?.(), 0); return { close: (c?: () => void) => c?.(), address: () => ({ port: 0 }), on() { return this; } }; };
+    return app;
+  };
+  Object.assign(factory, actual);
+  return { ...actual, default: factory };
+});
+
+let server: http.Server;
+let base = '';
+
+beforeAll(async () => {
+  const app = (await import('../index')).default as any;
+  for (let i = 0; i < 200 && !seen.warmed; i++) await new Promise((r) => setTimeout(r, 20));
+  await new Promise((r) => setTimeout(r, 50));
+  server = http.createServer(app);
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  base = `http://127.0.0.1:${(server.address() as any).port}`;
+}, 30_000);
+
+afterAll(async () => {
+  if (server) await new Promise<void>((r) => server.close(() => r()));
+});
+
+async function status(id: string) {
+  const res = await fetch(`${base}/api/connections/${id}`);
+  const json: any = await res.json();
+  return { http: res.status, data: json?.data };
+}
+
+describe('KS-1689: the connection status read says when the user must sign in again', () => {
+  it('CONTROL KS-1689 C0: the seam warmed the connections through the real loadFromDb path', () => {
+    expect(seen.warmed).toBe(true);
+  });
+
+  it('CONTROL KS-1689 C1: the stored status and tokenExpired keep their meaning: a connection with no token still says connected', async () => {
+    const withToken = await status(C_TOKEN);
+    const noToken = await status(C_NONE);
+    expect({ a: [withToken.http, withToken.data?.status, withToken.data?.tokenExpired], b: [noToken.http, noToken.data?.status, noToken.data?.tokenExpired] })
+      .toEqual({ a: [200, 'connected', false], b: [200, 'connected', false] });
+  });
+
+  it('RED KS-1689 R1: a connected connection that holds a refresh token does not need to sign in again', async () => {
+    expect((await status(C_TOKEN)).data?.needsReauth).toBe(false);
+  });
+
+  it('RED KS-1689 R2: a connected connection with no refresh token needs to sign in again', async () => {
+    expect((await status(C_NONE)).data?.needsReauth).toBe(true);
+  });
+
+  it('RED KS-1689 R3: a connected connection whose stored refresh token cannot be decrypted needs to sign in again', async () => {
+    expect((await status(C_BAD)).data?.needsReauth).toBe(true);
+  });
+
+  it('RED KS-1689 R4: a disconnected connection (token cleared) is not flagged', async () => {
+    const r = await status(C_DISCONNECTED);
+    expect([r.data?.status, r.data?.needsReauth]).toEqual(['disconnected', false]);
+  });
+
+  it('RED KS-1689 R5: a connection in the error status with no token is not flagged', async () => {
+    const r = await status(C_ERROR);
+    expect([r.data?.status, r.data?.needsReauth]).toEqual(['error', false]);
+  });
+
+  it('RED KS-1689 R6: a pending connection with no token is not flagged', async () => {
+    const r = await status(C_PENDING);
+    expect([r.data?.status, r.data?.needsReauth]).toEqual(['pending', false]);
+  });
+
+  it('RED KS-1689 R7: disconnecting a connected connection that held a token clears the token and the status read then says disconnected, not flagged', async () => {
+    expect((await status(C_DELETE)).data?.needsReauth).toBe(false);
+    const del = await fetch(`${base}/api/connections/${C_DELETE}`, { method: 'DELETE' });
+    expect(del.status).toBe(200);
+    const after = await status(C_DELETE);
+    expect([after.data?.status, after.data?.needsReauth]).toEqual(['disconnected', false]);
+  });
+});
```
