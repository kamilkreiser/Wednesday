# READY — KS-593-SIGNATORIES-NON-UUID-ID-1 (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-593-signatories-non-uuid-id/out.md.checker/patch.diff`** (from `ls` at 10:48 2026-10-06; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-593-signatories-non-uuid-id/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-593-signatories-non-uuid-id/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 10:48 2026-10-06 by Spark review agent after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-593-signatories-non-uuid-id/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/signatories.ts , Blockchain/Dev/services/originate/src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/signatories.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/originate/src/routes/signatories.ts
95	0	Blockchain/Dev/services/originate/src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/signatories.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/signatories.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-593: the signatory list and check routes refuse a non-UUID id with 400 before any query runs RED KS-593 SG1: GET /api/signatories?organizationId=abc answers 400 and runs no query', 'KS-593: the signatory list and check routes refuse a non-UUID id with 400 before any query runs RED KS-593 SG2: GET /api/signatories/check with a non-UUID organizationId answers 400 and runs no query', 'KS-593: the signatory list and check routes refuse a non-UUID id with 400 before any query runs RED KS-593 SG3: GET /api/signatories/check with a non-UUID userId answers 400 and runs no query']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1063 failed=0 | after: total=1069 failed=0` · `NEW reds: []` [baseline_suite.json total=1063 failed=0; after_suite.json total=1069 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +98/-3 test=src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/signatories.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts` (+95/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-593-signatories-non-uuid-id/input.json`. Brief (given by --brief; its `# ` heading names KS-593): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-593-signatories-non-uuid-id/KS-593.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-593-signatories-non-uuid-id/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/signatories.ts
+++ b/Blockchain/Dev/services/originate/src/routes/signatories.ts
@@ -142,5 +142,5 @@
 signatoriesRouter.get(
   '/',
-  [query('organizationId').isString().notEmpty().withMessage('Organization ID is required')],
+  [query('organizationId').isString().notEmpty().withMessage('Organization ID is required').isUUID().withMessage('Organization ID must be a UUID')],
   async (req: Request, res: Response) => {
     try {
@@ -193,6 +193,6 @@
   '/check',
   [
-    query('organizationId').isString().notEmpty().withMessage('Organization ID is required'),
-    query('userId').isString().notEmpty().withMessage('User ID is required'),
+    query('organizationId').isString().notEmpty().withMessage('Organization ID is required').isUUID().withMessage('Organization ID must be a UUID'),
+    query('userId').isString().notEmpty().withMessage('User ID is required').isUUID().withMessage('User ID must be a UUID'),
   ],
   async (req: Request, res: Response) => {
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts
@@ -0,0 +1,95 @@
+// KS-593 (not_a_server_error register; the ninth operation, GET /api/signatories, measured 2026-08-28):
+// `?organizationId=abc` passed the route's validator (isString + notEmpty only) and reached
+// `s.organization_id = ${organizationId}::uuid`, where Postgres refuses it (22P02) and the catch answers
+// 500 INTERNAL_ERROR. GET /api/signatories/check casts organizationId AND userId the same way. The fix adds
+// isUUID() to those three validators, so a malformed id is a 400 from the route's own validationResult
+// branch and no query runs. Harness: the real signatoriesRouter on a loopback listener, prisma mocked,
+// authenticate() stubbed. No database, no network beyond 127.0.0.1.
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw },
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: 'u-ks593-sig', email: 'sig@example.test', role: 'ORG_ADMIN' };
+    next();
+  },
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { signatoriesRouter } from '../routes/signatories';
+
+const ORG = 'a0000000-0000-4000-8000-000000000001';
+const USER = 'b0000000-0000-4000-8000-000000000002';
+
+const app = express();
+app.use('/api/signatories', express.json(), signatoriesRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => {
+  server?.close();
+});
+beforeEach(() => {
+  jest.clearAllMocks();
+  mockQueryRaw.mockResolvedValue([]);
+});
+
+async function get(pathAndQuery: string): Promise<{ status: number; body: any }> {
+  const res = await fetch(baseUrl + '/api/signatories' + pathAndQuery);
+  return { status: res.status, body: await res.json() };
+}
+
+describe('KS-593: the signatory list and check routes refuse a non-UUID id with 400 before any query runs', () => {
+  it('RED KS-593 SG1: GET /api/signatories?organizationId=abc answers 400 and runs no query', async () => {
+    const r = await get('/?organizationId=abc');
+    expect(r.status).toBe(400);
+    expect(r.body.success).toBe(false);
+    expect(mockQueryRaw).not.toHaveBeenCalled();
+  });
+
+  it('RED KS-593 SG2: GET /api/signatories/check with a non-UUID organizationId answers 400 and runs no query', async () => {
+    const r = await get('/check?organizationId=abc&userId=' + USER);
+    expect(r.status).toBe(400);
+    expect(mockQueryRaw).not.toHaveBeenCalled();
+  });
+
+  it('RED KS-593 SG3: GET /api/signatories/check with a non-UUID userId answers 400 and runs no query', async () => {
+    const r = await get('/check?organizationId=' + ORG + '&userId=abc');
+    expect(r.status).toBe(400);
+    expect(mockQueryRaw).not.toHaveBeenCalled();
+  });
+
+  it('control KS-593 SGC1: a well-formed organizationId still lists (200) and runs the query once', async () => {
+    const r = await get('/?organizationId=' + ORG);
+    expect(r.status).toBe(200);
+    expect(r.body).toEqual({ success: true, signatories: [], total: 0 });
+    expect(mockQueryRaw).toHaveBeenCalledTimes(1);
+  });
+
+  it('control KS-593 SGC2: a well-formed check still answers 200 authorised false when no row matches', async () => {
+    const r = await get('/check?organizationId=' + ORG + '&userId=' + USER);
+    expect(r.status).toBe(200);
+    expect(r.body).toEqual({ success: true, authorised: false });
+    expect(mockQueryRaw).toHaveBeenCalledTimes(1);
+  });
+
+  it('control KS-593 SGC3: a missing organizationId is still refused with 400', async () => {
+    const r = await get('/');
+    expect(r.status).toBe(400);
+    expect(mockQueryRaw).not.toHaveBeenCalled();
+  });
+});
```
