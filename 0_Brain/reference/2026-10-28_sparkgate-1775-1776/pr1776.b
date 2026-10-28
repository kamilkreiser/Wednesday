diff --git a/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts b/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts
--- a/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts
+++ b/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts
@@ -138,5 +138,8 @@
  * @returns true for SYSTEM_ADMIN / SUPER_ADMIN, false for everything else.
  */
 export function isPlatformRole(role: string | undefined): boolean {
-  return PLATFORM_ROLES.has(String(role || '').toUpperCase());
+  // KS-1591: `String(role).toUpperCase()` is not an identity test. U+0131 (dotless i) upper-cases to `I`, U+017F (long s) upper-cases to `S`, and an ARRAY role stringifies to its element, so all three
+  // read as SUPER_ADMIN. Only an ASCII fold is applied (a-z to A-Z, every other character untouched), and a role that is not a string is refused outright.
+  if (typeof role !== 'string') return false;
+  return PLATFORM_ROLES.has(role.replace(/[a-z]/g, (ch) => ch.toUpperCase()));
 }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts
@@ -0,0 +1,78 @@
+// KS-1591 (packages/shared security/keyRevokePolicy.ts isPlatformRole): the predicate decided "platform administrator" with `String(role || '').toUpperCase()`, which is not an identity test.
+// U+0131 (dotless i) upper-cases to `I` and U+017F (long s) upper-cases to `S`, so `super_admin` spelled with either read as SUPER_ADMIN; and a role ARRAY stringifies to its element, so
+// `['SUPER_ADMIN']` read as SUPER_ADMIN too. R1 to R5 pin that each of those is refused; C1 to C6 pin that every spelling the platform really uses is still admitted and that an ordinary role,
+// an empty role and an absent role are still refused; D1 and D2 go through decideTenantAccess, the caller of the predicate, so the refusal is seen where the decision is made.
+// All non-ASCII characters are written as \u escapes so this file is pure ASCII.
+import { describe, it, expect } from 'vitest';
+import { isPlatformRole, decideTenantAccess } from '../index';
+
+const DOTLESS_I = '\u0131';
+const LONG_S = '\u017f';
+
+function asRole(value: unknown): string | undefined {
+  return value as string | undefined;
+}
+
+describe('KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role', () => {
+  it('RED KS-1591 R1 a role spelled with a dotless i is not a platform role', () => {
+    expect(isPlatformRole('super_adm' + DOTLESS_I + 'n')).toBe(false);
+  });
+
+  it('RED KS-1591 R2 a role spelled with a long s is not a platform role', () => {
+    expect(isPlatformRole(LONG_S + 'uper_admin')).toBe(false);
+  });
+
+  it('RED KS-1591 R3 a role array holding SUPER_ADMIN is not a platform role', () => {
+    expect(isPlatformRole(asRole(['SUPER_ADMIN']))).toBe(false);
+  });
+
+  it('RED KS-1591 R4 a role array holding system_admin is not a platform role', () => {
+    expect(isPlatformRole(asRole(['system_admin']))).toBe(false);
+  });
+
+  it('RED KS-1591 R5 a system admin role spelled with a long s is not a platform role', () => {
+    expect(isPlatformRole(LONG_S + 'ystem_admin')).toBe(false);
+  });
+
+  it('control KS-1591 C1 SUPER_ADMIN and SYSTEM_ADMIN are platform roles', () => {
+    expect(isPlatformRole('SUPER_ADMIN')).toBe(true);
+    expect(isPlatformRole('SYSTEM_ADMIN')).toBe(true);
+  });
+
+  it('control KS-1591 C2 super_admin and system_admin are platform roles', () => {
+    expect(isPlatformRole('super_admin')).toBe(true);
+    expect(isPlatformRole('system_admin')).toBe(true);
+  });
+
+  it('control KS-1591 C3 a mixed-case spelling is a platform role', () => {
+    expect(isPlatformRole('Super_Admin')).toBe(true);
+    expect(isPlatformRole('sYsTeM_aDmIn')).toBe(true);
+  });
+
+  it('control KS-1591 C4 ordinary roles are not platform roles', () => {
+    expect(isPlatformRole('ADMIN')).toBe(false);
+    expect(isPlatformRole('ISSUER_ADMIN')).toBe(false);
+    expect(isPlatformRole('user')).toBe(false);
+  });
+
+  it('control KS-1591 C5 an empty role and an absent role are not platform roles', () => {
+    expect(isPlatformRole('')).toBe(false);
+    expect(isPlatformRole(undefined)).toBe(false);
+    expect(isPlatformRole(asRole(null))).toBe(false);
+  });
+
+  it('control KS-1591 C6 a role with surrounding whitespace is still not a platform role', () => {
+    expect(isPlatformRole(' SUPER_ADMIN')).toBe(false);
+    expect(isPlatformRole('SUPER_ADMIN ')).toBe(false);
+  });
+
+  it('RED KS-1591 D1 decideTenantAccess does not give a dotless-i role the platform-admin pass', () => {
+    const decision = decideTenantAccess({ role: 'super_adm' + DOTLESS_I + 'n', tenantId: 'tenant-a' }, 'tenant-b');
+    expect(decision.allow).toBe(false);
+  });
+
+  it('control KS-1591 D2 decideTenantAccess still gives super_admin the platform-admin pass', () => {
+    const decision = decideTenantAccess({ role: 'super_admin', tenantId: 'tenant-a' }, 'tenant-b');
+    expect(decision).toEqual({ allow: true, reason: 'platform-admin' });
+  });
+});
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
