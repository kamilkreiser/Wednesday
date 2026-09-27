# READY — KS-908-KS-908-R2 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-908-R2/out.md.checker/patch.diff`** (from `ls` at 06:37 2026-09-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-908-R2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-908-R2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-908-R2/out.md.checker/patch.diff /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/golden_908/out.md.checker/patch.diff` rc 0, Wednesday morning 4901153c).

**Held 06:37 2026-09-28 by Wednesday morning 4901153c after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-908-R2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/index.ts , Blockchain/Dev/services/security/src/__tests__/ks908-connector-id-read-back.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks908-connector-id-read-back.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/security/src/index.ts
98	0	Blockchain/Dev/services/security/src/__tests__/ks908-connector-id-read-back.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks908-connector-id-read-back.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks908-connector-id-read-back.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-908: connectorId is readable through the API that accepted it RED KS-908 A1: POST /api/keys returns the connectorId it was given, in its 201 body', 'KS-908: connectorId is readable through the API that accepted it RED KS-908 A2: GET /api/keys lists that key with its connectorId']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks908-connector-id-read-back.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=247 failed=0 | after: total=251 failed=0` · `NEW reds: []` [baseline_suite.json total=247 failed=0; after_suite.json total=251 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +100/-0 test=src/__tests__/ks908-connector-id-read-back.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks908-connector-id-read-back.test.ts` (+98/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-908-R2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-908-R2/checker.out`.

```diff
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -1153,4 +1153,5 @@
         scopes: apiKey.scopes,
         rateLimit: apiKey.rateLimit,
         createdAt: apiKey.createdAt,
+        connectorId: apiKey.connectorId || null,
         // KS-577: reported, not assumed. `null` means the revoke was attempted
@@ -1214,4 +1215,5 @@
       usageCount: k.usageCount,
       isActive: k.isActive,
       createdAt: k.createdAt,
+      connectorId: k.connectorId || null,
     }));
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks908-connector-id-read-back.test.ts
@@ -0,0 +1,98 @@
+// KS-908: POST /api/keys persists connectorId (KS-869), but its 201 body never returned it, and GET /api/keys
+// mapped each key to a view without it. A caller that set connectorId read back nothing, and could not tell
+// persisted-but-hidden from not-persisted: the two have opposite remedies. This file drives the REAL app on a
+// loopback listener, exactly as ks742-keys-tenancy-route-contract.test.ts does: a real RS256 token signed with
+// node crypto, the real router, and no database (dbSaveApiKey writes memApiKeys before its isDbAvailable early
+// return, so the whole family works in memory).
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import crypto from 'crypto';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+// Opt-IN boot guard: keeps the import of ../index from binding its port and dialling postgres.
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+const TENANT = 'c0000000-0000-4000-8000-000000000908';
+const ORG = '90800000-0000-4000-8000-000000000908';
+const CONNECTOR = 'platform-s:ks908-probe-connector';
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+
+function token(claims: Record<string, unknown>): string {
+  const now = Math.floor(Date.now() / 1000);
+  const header = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
+  const payload = Buffer.from(JSON.stringify({ sub: 'ks908-test', iat: now, exp: now + 300, ...claims })).toString('base64url');
+  const signature = crypto.sign('RSA-SHA256', Buffer.from(header + '.' + payload), PRIVATE_PEM).toString('base64url');
+  return header + '.' + payload + '.' + signature;
+}
+
+const PLATFORM = () => token({ role: 'super_admin' });
+
+type KeyView = Record<string, unknown> & { id: string };
+
+let server: Server;
+let base = '';
+
+async function mint(name: string, connectorId?: string): Promise<{ status: number; data: KeyView }> {
+  const body: Record<string, unknown> = { name, organizationId: ORG, tenantId: TENANT, scopes: ['documents:read'] };
+  if (connectorId !== undefined) body.connectorId = connectorId;
+  const res = await fetch(base + '/api/keys', {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + PLATFORM() },
+    body: JSON.stringify(body),
+  });
+  const json = (await res.json()) as { data: KeyView };
+  return { status: res.status, data: json.data };
+}
+
+async function listed(id: string): Promise<KeyView | undefined> {
+  const res = await fetch(base + '/api/keys?organizationId=' + ORG, { headers: { Authorization: 'Bearer ' + PLATFORM() } });
+  expect(res.status).toBe(200);
+  const json = (await res.json()) as { data: KeyView[] };
+  return json.data.find((k) => k.id === id);
+}
+
+beforeAll(async () => {
+  // The static-key path of the shared RS256 verifier: base64-encoded PEM, no JWKS.
+  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
+  delete process.env.JWT_JWKS_URL;
+  delete process.env.AUTH_SERVICE_URL;
+  const app = (await import('../index')).default;
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', resolve);
+  });
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+describe('KS-908: connectorId is readable through the API that accepted it', () => {
+  it('RED KS-908 A1: POST /api/keys returns the connectorId it was given, in its 201 body', async () => {
+    const r = await mint('ks908 with connector', CONNECTOR);
+    expect({ status: r.status, connectorId: r.data.connectorId }).toEqual({ status: 201, connectorId: CONNECTOR });
+  });
+
+  it('RED KS-908 A2: GET /api/keys lists that key with its connectorId', async () => {
+    const r = await mint('ks908 listed with connector', CONNECTOR);
+    const row = await listed(r.data.id);
+    expect({ found: row !== undefined, connectorId: row?.connectorId }).toEqual({ found: true, connectorId: CONNECTOR });
+  });
+
+  it('control KS-908 C1: a key minted WITHOUT a connectorId reads back null in both responses', async () => {
+    const r = await mint('ks908 no connector');
+    const row = await listed(r.data.id);
+    expect({ status: r.status, found: row !== undefined, post: r.data.connectorId ?? null, list: row?.connectorId ?? null }).toEqual({ status: 201, found: true, post: null, list: null });
+  });
+
+  it('control KS-908 C2: the 201 body and the list row keep every field they had, and neither carries the key hash', async () => {
+    const r = await mint('ks908 fields', CONNECTOR);
+    const row = await listed(r.data.id);
+    expect(Object.keys(r.data)).toEqual(expect.arrayContaining(['id', 'key', 'prefix', 'name', 'scopes', 'rateLimit', 'createdAt']));
+    expect(Object.keys(row ?? {})).toEqual(expect.arrayContaining(['id', 'name', 'prefix', 'scopes', 'usageCount', 'isActive', 'createdAt']));
+    expect({ post: 'keyHash' in r.data, list: 'keyHash' in (row ?? {}) }).toEqual({ post: false, list: false });
+  });
+});
```
