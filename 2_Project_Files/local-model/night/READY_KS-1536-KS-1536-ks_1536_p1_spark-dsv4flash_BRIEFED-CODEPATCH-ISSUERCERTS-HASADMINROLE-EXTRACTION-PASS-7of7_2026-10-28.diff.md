# READY — KS-1536-KS-1536-ks_1536_p1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/out.md.checker/patch.diff`** (from `ls` at 16:10 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:10 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/issuerCerts.ts , Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
13	8	Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
115	0	Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (12 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 13 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 8.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/issuerCerts.ts byte-exact incl. leading whitespace (apply mode strict): OK 12 line(s) byte-exact incl. leading whitespace (of 12; 13 line(s) added by the apply)` [a3i_indent.out: `OK 12 line(s) byte-exact incl. leading whitespace (of 12; 13 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (hunks=4, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts fails at the untouched tip (3 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=3 of total=9; red cell(s): ['KS-1536 extraction: the issuer-cert admin role test is one helper RED KS-1536 R1 hasAdminRole is exported as a function', 'KS-1536 extraction: the issuer-cert admin role test is one helper RED KS-1536 R2 hasAdminRole keeps the truth table of the copied lines', 'KS-1536 extraction: the issuer-cert admin role test is one helper RED KS-1536 R3 the file holds the role test once: no gate copies the ADMIN_ROLES comparison any more']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts passes with the product hunk (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1200 failed=0 | after: total=1209 failed=0` · `NEW reds: []` [baseline_suite.json total=1200 failed=0; after_suite.json total=1209 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +128/-8 test=src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (+13/-8 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts` (+115/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1536): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1536_p1/KS-1536.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts b/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
--- a/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
+++ b/Blockchain/Dev/services/auth/src/routes/issuerCerts.ts
@@ -65,8 +65,16 @@
+/**
+ * The one role test the four gates below share: the role claim, read as text, is in ADMIN_ROLES either as it is or upper-cased.
+ * Behaviour-preserving extraction of the two lines that were copied into each gate.
+ */
+export function hasAdminRole(role: unknown): boolean {
+  const text = String(role ?? '');
+  return ADMIN_ROLES.includes(text) || ADMIN_ROLES.includes(text.toUpperCase());
+}
+
 function isAuthorisedForCertWrite(req: AuthenticatedRequest): boolean {
   const user = req.user as { role?: string; scopes?: string[] } | undefined;
   if (!user) return false;
-  const role = String(user.role ?? '');
-  if (ADMIN_ROLES.includes(role) || ADMIN_ROLES.includes(role.toUpperCase())) return true;
+  if (hasAdminRole(user.role)) return true;
   const scopes = Array.isArray(user.scopes) ? user.scopes : [];
   return scopes.includes('issuer-certs:write') || scopes.includes('issuer-certs:*') || scopes.includes('*');
 }
@@ -74,8 +82,7 @@
 function isAuthorisedForCertRead(req: AuthenticatedRequest): boolean {
   const user = req.user as { role?: string; scopes?: string[] } | undefined;
   if (!user) return false;
-  const role = String(user.role ?? '');
-  if (ADMIN_ROLES.includes(role) || ADMIN_ROLES.includes(role.toUpperCase())) return true;
+  if (hasAdminRole(user.role)) return true;
   const scopes = Array.isArray(user.scopes) ? user.scopes : [];
   return (
     scopes.includes('issuer-certs:read') ||
@@ -88,8 +95,7 @@
 function isAuthorisedForCertRevoke(req: AuthenticatedRequest): boolean {
   const user = req.user as { role?: string; scopes?: string[] } | undefined;
   if (!user) return false;
-  const role = String(user.role ?? '');
-  if (ADMIN_ROLES.includes(role) || ADMIN_ROLES.includes(role.toUpperCase())) return true;
+  if (hasAdminRole(user.role)) return true;
   const scopes = Array.isArray(user.scopes) ? user.scopes : [];
   return (
     scopes.includes('issuer-certs:revoke') ||
@@ -105,8 +111,7 @@
   // allow-list, plus a dedicated `issuer-certs:sign` scope for the
   // SSD connector path (originate calls this on behalf of the caller,
   // forwarding the Bearer token, so the caller's scopes apply).
-  const role = String(user.role ?? '');
-  if (ADMIN_ROLES.includes(role) || ADMIN_ROLES.includes(role.toUpperCase())) return true;
+  if (hasAdminRole(user.role)) return true;
   const scopes = Array.isArray(user.scopes) ? user.scopes : [];
   return (
     scopes.includes('issuer-certs:sign') ||
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts
@@ -0,0 +1,115 @@
+// Behaviour-preserving extraction in services/auth routes/issuerCerts.ts: the four gates (write, read, revoke, sign) each copied the same two lines, `const role = String(user.role ?? '')` and
+// `ADMIN_ROLES.includes(role) || ADMIN_ROLES.includes(role.toUpperCase())`. They now call one exported helper, hasAdminRole. R1 to R3 pin the helper (it exists, its truth table, and the file
+// holds the role test once). C1 to C6 drive the REAL router on a loopback listener through all four gates and must read the same before and after the extraction: an admitted caller with no tenant claim
+// gets 400 TENANT_REQUIRED (past the role gate), a refused caller gets 403. The role arrives in an x-test-user header that a mocked authenticate() turns into req.user.
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const silent = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() }));
+vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
+vi.mock('../middleware/authenticate', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    const raw = req.headers['x-test-user'];
+    req.user = typeof raw === 'string' ? JSON.parse(raw) : undefined;
+    next();
+  },
+}));
+vi.mock('../repositories/issuerCertRepo', () => ({
+  createIssuerCert: vi.fn(), getIssuerCertById: vi.fn(), findIssuerCertByFingerprint: vi.fn(), findActiveIssuerCertForTenant: vi.fn(),
+  listIssuerCerts: vi.fn(async () => []), revokeIssuerCert: vi.fn(), rotateIssuerCert: vi.fn(), toSummary: vi.fn(),
+}));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
+
+import * as certRoutes from '../routes/issuerCerts';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const SRC = readFileSync(join(__dirname, '..', 'routes', 'issuerCerts.ts'), 'utf8');
+
+let server: Server;
+let base = '';
+
+beforeAll(async () => {
+  const app = express();
+  app.use(express.json());
+  app.use('/api/issuer-certs', certRoutes.issuerCertsRoutes);
+  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });
+  const addr = server.address();
+  base = 'http://127.0.0.1:' + (typeof addr === 'object' && addr ? addr.port : 0);
+});
+afterAll(() => { server?.close(); });
+
+/** The helper under test, or a sentinel when it is not exported yet, so a missing helper is a red assertion and not a thrown error. */
+function helper(role: unknown): boolean | string {
+  const fn = (certRoutes as Record<string, unknown>).hasAdminRole;
+  return typeof fn === 'function' ? (fn as (r: unknown) => boolean)(role) : 'NO HELPER';
+}
+
+const ROUTES: Array<[string, string, string]> = [
+  ['write', 'POST', '/api/issuer-certs'],
+  ['read', 'GET', '/api/issuer-certs'],
+  ['revoke', 'POST', '/api/issuer-certs/abc/revoke'],
+  ['sign', 'POST', '/api/issuer-certs/sign'],
+];
+
+/** The status a caller gets from a route; the user carries no tenant claim, so a caller past the role gate is answered 400 TENANT_REQUIRED. */
+async function status(method: string, path: string, user: unknown): Promise<number> {
+  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
+  if (user !== undefined) headers['x-test-user'] = JSON.stringify(user);
+  const res = await fetch(base + path, { method, headers, body: method === 'GET' ? undefined : '{}' });
+  return res.status;
+}
+
+async function statuses(user: unknown): Promise<number[]> {
+  const out: number[] = [];
+  for (const [, method, path] of ROUTES) out.push(await status(method, path, user));
+  return out;
+}
+
+describe('KS-1536 extraction: the issuer-cert admin role test is one helper', () => {
+  it('RED KS-1536 R1 hasAdminRole is exported as a function', () => {
+    expect(typeof (certRoutes as Record<string, unknown>).hasAdminRole).toBe('function');
+  });
+
+  it('RED KS-1536 R2 hasAdminRole keeps the truth table of the copied lines', () => {
+    const rows = ['ORG_ADMIN', 'org_admin', 'SYSTEM_ADMIN', 'ISSUER_ADMIN', 'SUPER_ADMIN', 'admin', 'super_admin', 'Super_Admin', 'Admin', 'ADMIN', 'USER', '', undefined, null, 0];
+    expect(rows.map((r) => helper(r))).toEqual([true, true, true, true, true, true, true, true, false, false, false, false, false, false, false]);
+  });
+
+  it('RED KS-1536 R3 the file holds the role test once: no gate copies the ADMIN_ROLES comparison any more', () => {
+    expect(SRC.split('ADMIN_ROLES.includes(').length - 1).toBe(2);
+    expect(SRC).not.toContain("const role = String(user.role ?? '');");
+  });
+
+  it('control KS-1536 C1 an ORG_ADMIN is admitted by all four gates (400 TENANT_REQUIRED, past the role gate)', async () => {
+    expect(await statuses({ role: 'ORG_ADMIN' })).toEqual([400, 400, 400, 400]);
+  });
+
+  it('control KS-1536 C2 a lower-case super_admin and a mixed-case Super_Admin are admitted by all four gates', async () => {
+    expect(await statuses({ role: 'super_admin' })).toEqual([400, 400, 400, 400]);
+    expect(await statuses({ role: 'Super_Admin' })).toEqual([400, 400, 400, 400]);
+  });
+
+  it('control KS-1536 C3 an ordinary USER, a mixed-case Admin and a caller with no role are refused by all four gates', async () => {
+    expect(await statuses({ role: 'USER' })).toEqual([403, 403, 403, 403]);
+    expect(await statuses({ role: 'Admin' })).toEqual([403, 403, 403, 403]);
+    expect(await statuses({})).toEqual([403, 403, 403, 403]);
+  });
+
+  it('control KS-1536 C4 a request with no user at all is refused by all four gates', async () => {
+    expect(await statuses(undefined)).toEqual([403, 403, 403, 403]);
+  });
+
+  it('control KS-1536 C5 a USER holding only the read scope passes the read gate and no other', async () => {
+    expect(await statuses({ role: 'USER', scopes: ['issuer-certs:read'] })).toEqual([403, 400, 403, 403]);
+  });
+
+  it('control KS-1536 C6 a USER holding the write scope passes write and read, a revoke-scope USER passes revoke only, a sign-scope USER passes sign only', async () => {
+    expect(await statuses({ role: 'USER', scopes: ['issuer-certs:write'] })).toEqual([400, 400, 403, 403]);
+    expect(await statuses({ role: 'USER', scopes: ['issuer-certs:revoke'] })).toEqual([403, 403, 400, 403]);
+    expect(await statuses({ role: 'USER', scopes: ['issuer-certs:sign'] })).toEqual([403, 403, 403, 400]);
+  });
+});
```


## DECISION NOTE (source-read, Spark operator 3 for Wednesday, 2026-10-28 PM) - HOLD
- Source-read: golden.diff vs brief line by line, and vs auth `routes/issuerCerts.ts` at base 65bc2823 (and develop bd6697e0: file unchanged between them). One exported `hasAdminRole(role: unknown)` added after `ADMIN_ROLES`; each of the four gates' two copied lines (`const role = String(user.role ?? '')` + the `.includes(role) || .includes(role.toUpperCase())` test) become `if (hasAdminRole(user.role)) return true;`. The helper body is the same two expressions, so every spelling admitted or refused before is admitted or refused now (cells C1-C6 are green at the tip AND after; only the 3 red cells pin the helper and the removal of the copies).
- NO BOARD TICKET covers this: it hangs from KS-1536 only because the builder needs an open ticket in the header. The raise seat writes `Refs KS-1536` and never a close-word; the PR body must say 'behaviour-preserving extraction, groundwork for the KS-1591 class, not a fix for KS-1536'.
- Apply mode: STRICT on both sections (apply_mode=strict; `git apply --check` of the whole patch.diff also passes at develop bd6697e0).
- SEQUENCE: shares no file with any other held pass; no open PR touches it (checked 2026-10-28 16:xx against the 14 open PRs, 0 overlaps).
- Verdict: HOLD.
