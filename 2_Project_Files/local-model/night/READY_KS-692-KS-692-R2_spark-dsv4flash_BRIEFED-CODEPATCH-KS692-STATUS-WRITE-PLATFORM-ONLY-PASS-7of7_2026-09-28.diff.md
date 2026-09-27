# READY — KS-692-KS-692-R2 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-692-R2/out.md.checker/patch.diff`** (from `ls` at 06:37 2026-09-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-692-R2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-692-R2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-692-R2/out.md.checker/patch.diff /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/golden_692/out.md.checker/patch.diff` rc 0, Wednesday morning 4901153c).

**Held 06:37 2026-09-28 by Wednesday morning 4901153c after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-692-R2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/vc-issuer/src/routes/status.ts , Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/vc-issuer/src/routes/status.ts` (product) and `Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	4	Blockchain/Dev/services/vc-issuer/src/routes/status.ts
81	0	Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (8 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 8 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 4.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/vc-issuer/src/routes/status.ts byte-exact incl. leading whitespace (apply mode strict): OK 8 line(s) byte-exact incl. leading whitespace (of 8; 8 line(s) added by the apply)` [a3i_indent.out: `OK 8 line(s) byte-exact incl. leading whitespace (of 8; 8 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/vc-issuer/src/routes/status.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks692-status-write-platform-only.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-692: status list writes are platform-only until a list has an owner RED KS-692 A1: the write gate holds the platform roles and nothing else', 'KS-692: status list writes are platform-only until a list has an owner RED KS-692 A2: an ISSUER_ADMIN is refused 403 on revoke and on unrevoke']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks692-status-write-platform-only.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=136 failed=0 | after: total=140 failed=0` · `NEW reds: []` [baseline_suite.json total=136 failed=0; after_suite.json total=140 failed=0]
- A6 [verbatim]: `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +89/-4 test=src/__tests__/ks692-status-write-platform-only.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/vc-issuer/src/routes/status.ts` (+8/-4 per numstat.out) and the test file `Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts` (+81/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-692-R2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-692-R2/checker.out`.

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/routes/status.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/routes/status.ts
@@ -32,6 +32,10 @@
 // file is covered by default instead of shipping open.
 //
-// Tenant scoping is NOT enforced here yet: status lists live in a
-// process-local Map with no tenant linkage, and the ownership model is the
-// KS-539/KS-547/KS-586 joint authorization decision — tracked on KS-586.
+// KS-692 (Kam 2026-09-16, card secuura-ks692-status-revoke-interim-posture, option a:
+// Narrow now, bind-creator later). Tenant scoping still cannot be enforced here: a status
+// list lives in a process-local Map with no owning tenant, so there is no tenant to compare
+// a caller against, and an ISSUER_ADMIN in ANY tenant could revoke or un-revoke ANY
+// tenant's credential (reproduced live). Until a list carries an owner, writes are for the
+// platform roles only. When lists gain an owner, ISSUER_ADMIN comes back together with a
+// per-list ownership check. Tracked on KS-692; KS-586 is Done and no longer tracks this.
 // 'SUPER_ADMIN'/'super_admin' are the legacy JWT variants the existing admin
@@ -39,4 +43,4 @@
 // (see services/auth/src/routes/users.ts:90 and issuerCerts.ts ADMIN_ROLES).
-export const STATUS_WRITE_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin', 'ISSUER_ADMIN'] as const;
+export const STATUS_WRITE_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin'] as const;
 
 router.use((req: Request, res: Response, next: NextFunction) => {
--- /dev/null
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts
@@ -0,0 +1,81 @@
+// KS-692: /api/status writes are PLATFORM-ONLY (the interim posture Kam ruled 2026-09-16, card
+// secuura-ks692-status-revoke-interim-posture, option a: Narrow now, bind-creator later).
+// A status list lives in a process-local Map with no owning tenant, so there is no tenant to compare a
+// caller against, and an ISSUER_ADMIN in ANY tenant could revoke or un-revoke ANY tenant's credential.
+// Until a list carries an owner, the write gate admits the platform roles only. The harness is the one
+// ks586-status-write-authorization.test.ts uses: a real express app, the real router, the real
+// errorHandler, and an x-test-role header standing in for jwtAuthenticate. No database, no network.
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import express, { NextFunction, Request, Response } from 'express';
+import type { Server } from 'http';
+import { statusRoutes, STATUS_WRITE_ROLES } from '../routes/status';
+import { errorHandler } from '../middleware/errorHandler';
+
+const PLATFORM_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin'];
+
+function buildApp(): express.Express {
+  const app = express();
+  app.use(express.json());
+  app.use((req: Request, _res: Response, next: NextFunction) => {
+    const role = req.header('x-test-role');
+    if (role) {
+      (req as Request & { user: unknown }).user = { userId: 'u-1', role, organizationId: 'org-1' };
+    }
+    next();
+  });
+  app.use('/api/status', statusRoutes);
+  app.use(errorHandler);
+  return app;
+}
+
+let server: Server;
+let baseUrl = '';
+
+async function call(method: string, path: string, role?: string): Promise<number> {
+  const headers: Record<string, string> = { 'content-type': 'application/json' };
+  if (role) headers['x-test-role'] = role;
+  const res = await fetch(baseUrl + '/api/status' + path, method === 'GET' ? { headers } : { method, headers, body: '{}' });
+  return res.status;
+}
+
+beforeAll(async () => {
+  const app = buildApp();
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  if (address === null || typeof address === 'string') throw new Error('no ephemeral port');
+  baseUrl = 'http://127.0.0.1:' + address.port;
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+describe('KS-692: status list writes are platform-only until a list has an owner', () => {
+  it('RED KS-692 A1: the write gate holds the platform roles and nothing else', () => {
+    expect([...STATUS_WRITE_ROLES].sort()).toEqual([...PLATFORM_ROLES].sort());
+  });
+
+  it('RED KS-692 A2: an ISSUER_ADMIN is refused 403 on revoke and on unrevoke', async () => {
+    const seen = { revoke: await call('POST', '/default/revoke', 'ISSUER_ADMIN'), unrevoke: await call('POST', '/default/unrevoke', 'ISSUER_ADMIN') };
+    expect(seen).toEqual({ revoke: 403, unrevoke: 403 });
+  });
+
+  it('control KS-692 C1: every platform role still gets past the gate on revoke (never 401 or 403)', async () => {
+    const blocked: string[] = [];
+    for (const role of PLATFORM_ROLES) {
+      const status = await call('POST', '/default/revoke', role);
+      if (status === 401 || status === 403) blocked.push(role + ':' + status);
+    }
+    expect(blocked).toEqual([]);
+  });
+
+  it('control KS-692 C2: a non-admin OWNER is still 403 and an anonymous caller is still 401', async () => {
+    expect({ owner: await call('POST', '/default/revoke', 'OWNER'), anonymous: await call('POST', '/default/revoke') }).toEqual({ owner: 403, anonymous: 401 });
+  });
+
+  it('control KS-692 C3: reads stay authenticated-only, so an ISSUER_ADMIN is not 403 on GET revoked', async () => {
+    expect(await call('GET', '/default/revoked', 'ISSUER_ADMIN')).not.toBe(403);
+  });
+});
```
