# READY — KS-1114-HIDDENSTATUSES-2 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1114_p2/out.md.checker/patch.diff`** (from `ls` at 21:19 2026-10-18; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1114_p2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1114_p2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1114_p2-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in verification.ts (run 9 vs golden 12 body lines — context, since the change lines are equal) (identical in ks1114-title-lookup-hidden-statuses-case-and-space.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 21:19 2026-10-18 by Wednesday 2026-10-18 21:2x (read at source) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1114_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `833984fc94acf6bc00ff8e5d6642fa768dd44e09`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/verification.ts , Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	2	Blockchain/Dev/services/originate/src/routes/verification.ts
169	0	Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verification.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts fails at the untouched tip (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1114 follow-up - the title lookup hides draft, revoked, deleted and expired whatever the case or spacing RED KS-1114 N1 deleted - a document whose status is deleted is not found by title', 'KS-1114 follow-up - the title lookup hides draft, revoked, deleted and expired whatever the case or spacing RED KS-1114 N1 expired - a document whose status is expired is not found by title', 'KS-1114 follow-up - the title lookup hides draft, revoked, deleted and expired whatever the case or spacing RED KS-1114 N1 case - REVOKED, Draft, DELETED and Expired are hidden like their lower-case forms', 'KS-1114 follow-up - the title lookup hides draft, revoked, deleted and expired whatever the case or spacing RED KS-1114 N1 spaces - a status with a trailing or leading space is hidden like the trimmed one']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1376 failed=0 | after: total=1383 failed=0` · `NEW reds: []` [baseline_suite.json total=1376 failed=0; after_suite.json total=1383 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +172/-2 test=src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verification.ts` (+3/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts` (+169/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `833984fc94acf6bc00ff8e5d6642fa768dd44e09` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1114_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1114_p2/KS-1114.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1114_p2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -1439,3 +1439,4 @@ verificationRouter.post(
         //     afterwards, so a newer draft cannot shadow an older published document. A draft or a
-        //     revoked match answers the ordinary not-found. Every other document status can be a hit.
+        //     revoked match answers the ordinary not-found, and so does a deleted or an expired one (KS-1114
+        //     follow-up: the status is lower-cased and trimmed before it is compared). Every other status can be a hit.
         //   * the GDPR erasure sentinel never matches (Wednesday, 2026-10-13T10:52:44Z). Every erased
@@ -1465,3 +1466,3 @@ verificationRouter.post(
               AND d.tenant_id::text = ${tenantForTitle}
-              AND d.status NOT IN ('draft', 'revoked')
+              AND lower(btrim(d.status)) NOT IN ('draft', 'revoked', 'deleted', 'expired')
             LIMIT 1
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts
@@ -0,0 +1,169 @@
+/**
+ * =============================================================================
+ * KS-1114 follow-up - the title lookup's hidden statuses ignore case and spaces, and `deleted` and
+ * `expired` are hidden too
+ * =============================================================================
+ * Kam, card secuura-ks1114-deleted-status-found-by-title-1018 = a (2026-10-18 20:55): "Ship as built,
+ * hide 'deleted' in a follow-up" -- a small follow-up that makes the hidden set case- and
+ * space-insensitive and adds 'deleted' and 'expired'. Round 2's gate measured the defect (N1): the title
+ * strategy's WHERE excluded draft and revoked by an EXACT, case-sensitive match, so `deleted`, `expired`,
+ * `REVOKED`, `Draft` and `revoked ` (a trailing space) answered as hits.
+ *
+ * HARNESS. The sibling integration cells (ks1114-anonymous-title-lookup-one-tenant) need a real Postgres
+ * and are not in the default jest run. These cells run the REAL verificationRouter against a stand-in
+ * for `$queryRaw` that EVALUATES the status predicate of the query the route sends: it reads the
+ * expression and the NOT IN list out of the SQL text, applies lower() and btrim() the way Postgres does
+ * (btrim with no argument removes SPACES only), and answers a row only when the stored status survives.
+ * An expression it does not know throws, so a rewritten predicate fails loudly rather than passing.
+ * Postgres itself is exercised only by the integration cells.
+ * =============================================================================
+ */
+
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw },
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+jest.mock('../repositories/documentRepo', () => ({
+  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
+  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+import express from 'express';
+import { verificationRouter } from '../routes/verification';
+
+const TENANT = 'a0000000-0000-4000-8000-000000000001';
+const TITLE = 'KS-1114 follow-up title';
+const HIT_BODY = '{"verified":false,"checks":{"documentExists":true}}';
+const MISS_BODY =
+  '{"verified":false,"error":"Document not found in the registry","checks":{"documentExists":false,"hashValid":false,"integrityVerified":false}}';
+
+const app = express();
+app.use(express.json());
+app.use((req, _res, next) => {
+  (req as unknown as { tenantId: string }).tenantId = TENANT;
+  next();
+});
+app.use('/api/verification', verificationRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen> | undefined;
+const realFetch = global.fetch;
+
+/** The statuses of the stored documents that carry TITLE in the caller's tenant. */
+let stored: string[] = [];
+
+/** What Postgres does to a status expression: lower() and btrim() (spaces only) around d.status. */
+function applyExpr(expr: string, status: string): string {
+  if (expr === 'd.status') return status;
+  const m = /^(lower|btrim)\((.*)\)$/.exec(expr);
+  if (!m) throw new Error('unmodelled status expression: ' + expr);
+  const inner = applyExpr(m[2], status);
+  return m[1] === 'lower' ? inner.toLowerCase() : inner.replace(/^ +| +$/g, '');
+}
+
+/** The stand-in for db.$queryRaw: answers [{found:1}] when a stored status survives the query's own predicate. */
+function fakeQueryRaw(strings: TemplateStringsArray): Array<{ found: number }> {
+  const sql = strings.join('?');
+  const m = /AND\s+(\S+)\s+NOT IN\s*\(([^)]*)\)/.exec(sql);
+  if (!m) throw new Error('no status predicate in: ' + sql);
+  const hidden = m[2].split(',').map((s) => s.trim().replace(/^'|'$/g, ''));
+  return stored.some((st) => !hidden.includes(applyExpr(m[1], st))) ? [{ found: 1 }] : [];
+}
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server?.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => {
+  if (server) server.close();
+  global.fetch = realFetch;
+});
+
+beforeEach(() => {
+  mockQueryRaw.mockReset();
+  mockQueryRaw.mockImplementation(fakeQueryRaw);
+  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
+});
+
+/** POST a title-only body with one stored document per given status; return the raw response text. */
+async function answerFor(...statuses: string[]): Promise<string> {
+  stored = statuses;
+  const res = await realFetch(`${baseUrl}/api/verification/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ title: TITLE }),
+  });
+  return res.text();
+}
+
+describe('KS-1114 follow-up - the title lookup hides draft, revoked, deleted and expired whatever the case or spacing', () => {
+  it('RED KS-1114 N1 deleted - a document whose status is deleted is not found by title', async () => {
+    expect(await answerFor('deleted')).toBe(MISS_BODY);
+  });
+
+  it('RED KS-1114 N1 expired - a document whose status is expired is not found by title', async () => {
+    expect(await answerFor('expired')).toBe(MISS_BODY);
+  });
+
+  it('RED KS-1114 N1 case - REVOKED, Draft, DELETED and Expired are hidden like their lower-case forms', async () => {
+    const got: Record<string, string> = {};
+    const want: Record<string, string> = {};
+    for (const st of ['REVOKED', 'Draft', 'DELETED', 'Expired']) {
+      got[st] = await answerFor(st);
+      want[st] = MISS_BODY;
+    }
+    expect(got).toEqual(want);
+  });
+
+  it('RED KS-1114 N1 spaces - a status with a trailing or leading space is hidden like the trimmed one', async () => {
+    const got: Record<string, string> = {};
+    const want: Record<string, string> = {};
+    for (const st of ['revoked ', ' draft', ' Deleted ', 'expired  ']) {
+      got[st] = await answerFor(st);
+      want[st] = MISS_BODY;
+    }
+    expect(got).toEqual(want);
+  });
+
+  it('GREEN KS-1114 N1 control - draft and revoked stay hidden', async () => {
+    expect(await answerFor('draft')).toBe(MISS_BODY);
+    expect(await answerFor('revoked')).toBe(MISS_BODY);
+  });
+
+  it('GREEN KS-1114 N1 control - every other status is still a hit, with exactly the existence body', async () => {
+    const got: Record<string, string> = {};
+    const want: Record<string, string> = {};
+    for (const st of ['pending_signature', 'signed', 'anchored', 'anchor_failed', 'certified']) {
+      got[st] = await answerFor(st);
+      want[st] = HIT_BODY;
+    }
+    expect(got).toEqual(want);
+  });
+
+  it('GREEN KS-1114 N1 control - a hidden row beside a published one of the same title is still a hit', async () => {
+    expect(await answerFor('deleted', 'Expired', 'certified')).toBe(HIT_BODY);
+  });
+});
```
