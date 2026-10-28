# READY — KS-1591-KS-1591-ks_1591_p2_security (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/out.md.checker/patch.diff`** (from `ls` at 14:15 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security-control-r2/out.md.checker/patch.diff` rc 0, Spark operator for Wednesday).

**Held 14:15 2026-10-28 by Spark operator for Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/index.ts , Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	1	Blockchain/Dev/services/security/src/index.ts
89	0	Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts fails at the untouched tip (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1591: requireKeyAdmin is an exact ASCII fold and refuses a non-string role RED KS-1591 R1 a role spelled with a dotless i is refused', 'KS-1591: requireKeyAdmin is an exact ASCII fold and refuses a non-string role RED KS-1591 R2 a role spelled with a long s is refused', 'KS-1591: requireKeyAdmin is an exact ASCII fold and refuses a non-string role RED KS-1591 R3 a role array holding ISSUER_ADMIN is refused']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=361 failed=0 | after: total=368 failed=0` · `NEW reds: []` [baseline_suite.json total=361 failed=0; after_suite.json total=368 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +93/-1 test=src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+4/-1 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts` (+89/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/input.json`. Brief (given by --brief; its `# ` heading names KS-1591): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1591_p2_security/KS-1591.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/index.ts b/Blockchain/Dev/services/security/src/index.ts
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -1098,7 +1098,10 @@
 // (seeded DB casing) and canonical `SYSTEM_ADMIN` shapes (KS-486 precedent).
 const KEY_ADMIN_ROLES = new Set(['SYSTEM_ADMIN', 'SUPER_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'ADMIN']);
 function requireKeyAdmin(req: Request, res: Response, next: NextFunction): void {
-  const role = String((req as any).user?.role || '').toUpperCase();
+  // KS-1591: `String(role).toUpperCase()` is not an identity test. U+0131 (dotless i) upper-cases to `I` and U+017F (long s) upper-cases to `S`, so a role spelled with a dotless i read as ISSUER_ADMIN, and a role
+  // ARRAY stringifies to its element. Only an ASCII fold is applied (a-z to A-Z, every other character untouched), and a role that is not a string is refused outright.
+  const claim = (req as any).user?.role;
+  const role = typeof claim === 'string' ? claim.replace(/[a-z]/g, (ch) => ch.toUpperCase()) : '';
   if (!KEY_ADMIN_ROLES.has(role)) {
     res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'API key management requires an admin role' } });
     return;
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts
@@ -0,0 +1,89 @@
+// KS-1591 (services/security src/index.ts requireKeyAdmin, the services/security half of the ticket): the gate in front of GET /api/keys compared `String(role).toUpperCase()` to the admin role set, which is
+// not an identity test. U+0131 (dotless i) upper-cases to `I`, U+017F (long s) upper-cases to `S`, and a role ARRAY stringifies to its element, so `\u0131ssuer_admin`, `\u017fuper_admin` and ['ISSUER_ADMIN'] were
+// admitted as key admins. R1 to R3 drive the real app over HTTP (the harness of ks742-keys-tenancy-route-contract.test.ts: a real RS256 token signed with node crypto, no database) and pin that each
+// is refused; C1 to C4 pin that the spellings the platform really uses are still admitted and that an ordinary role and no token are still refused. Non-ASCII characters are written as \u escapes (pure ASCII file).
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import crypto from 'crypto';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+// Opt-IN boot guard: keeps `import '../index'` from binding its port and dialling postgres. Must be set before the import.
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+const TENANT_A = 'a0000000-0000-4000-8000-0000000000aa';
+const ORG_A = '11111111-1111-4111-8111-111111111111';
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+
+const b64url = (b: Buffer): string => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
+
+/** Sign an RS256 JWT with node crypto, in the shape the auth service issues. */
+function token(claims: Record<string, unknown>): string {
+  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
+  const now = Math.floor(Date.now() / 1000);
+  const payload = b64url(Buffer.from(JSON.stringify({ sub: 'test-user', iat: now, exp: now + 300, ...claims })));
+  const signature = b64url(crypto.sign('RSA-SHA256', Buffer.from(header + '.' + payload), PRIVATE_PEM));
+  return header + '.' + payload + '.' + signature;
+}
+
+const withRole = (role: unknown): string => token({ role, tenantId: TENANT_A, organizationId: ORG_A });
+
+let server: Server;
+let base = '';
+
+const HOOK_BUDGET_MS = 60_000;
+
+beforeAll(async () => {
+  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
+  delete process.env.JWT_JWKS_URL;
+  delete process.env.AUTH_SERVICE_URL;
+  const app = (await import('../index')).default;
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', resolve);
+  });
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+}, HOOK_BUDGET_MS);
+
+afterAll(async () => {
+  if (!server) return;
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+async function listKeysAs(bearer: string | null): Promise<number> {
+  const headers: Record<string, string> = bearer ? { Authorization: 'Bearer ' + bearer } : {};
+  const res = await fetch(base + '/api/keys?organizationId=' + ORG_A, { headers });
+  return res.status;
+}
+
+describe('KS-1591: requireKeyAdmin is an exact ASCII fold and refuses a non-string role', () => {
+  it('RED KS-1591 R1 a role spelled with a dotless i is refused', async () => {
+    expect(await listKeysAs(withRole('\u0131ssuer_admin'))).toBe(403);
+  });
+
+  it('RED KS-1591 R2 a role spelled with a long s is refused', async () => {
+    expect(await listKeysAs(withRole('\u017fuper_admin'))).toBe(403);
+  });
+
+  it('RED KS-1591 R3 a role array holding ISSUER_ADMIN is refused', async () => {
+    expect([401, 403]).toContain(await listKeysAs(withRole(['ISSUER_ADMIN'])));
+  });
+
+  it('control KS-1591 C1 no token is refused by the auth middleware', async () => {
+    expect(await listKeysAs(null)).toBe(401);
+  });
+
+  it('control KS-1591 C2 an ISSUER_ADMIN of the tenant is still admitted', async () => {
+    expect(await listKeysAs(withRole('ISSUER_ADMIN'))).toBe(200);
+  });
+
+  it('control KS-1591 C3 a lower-case and a mixed-case spelling are still admitted', async () => {
+    expect(await listKeysAs(withRole('issuer_admin'))).toBe(200);
+    expect(await listKeysAs(withRole('Issuer_Admin'))).toBe(200);
+  });
+
+  it('control KS-1591 C4 an ordinary role is still refused', async () => {
+    expect(await listKeysAs(withRole('USER'))).toBe(403);
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD
- Source-read: ONE product line in `requireKeyAdmin` (services/security/src/index.ts) replaced by four lines (claim read, ASCII fold for a string, `''` for a non-string); the `if (!KEY_ADMIN_ROLES.has(role))` line and the 403 body untouched. The new test boots the real app over HTTP with a node-crypto RS256 token (ks742 harness): R1 dotless-i, R2 long-s, R3 array are refused; C1-C4 keep no-token 401, ISSUER_ADMIN/issuer_admin/Issuer_Admin 200, USER 403. Fails toward LESS access.
- Note for the raise seat: R3 accepts 401 OR 403 (the cell does not pin which layer refuses an array role); the cells assert refusal, not the layer.
- SEQUENCE: shares NO file with `ks_1591_p1` (packages/shared). Either order. Same ticket KS-1591: Refs on both, close-word on neither until both merge.
- Verdict: HOLD.
