# READY — KS-1345-WEBHOOKS-DELIVERIES-1 (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/out.md.checker/patch.diff`** (from `ls` at 02:53 2026-10-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/originate/src/routes/webhooks.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/originate/src/routes/webhooks.ts): `error: corrupt patch at line 27` (apply with the options recorded in section_<k>.opts; the raise seat states which); CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) DIFFER in webhooks.ts; body lines (context included) DIFFER in webhooks.ts (run 23 vs golden 22 body lines — context, since the change lines are equal) (identical in ks1341c-webhooks-500-never-answers-err-message.test.ts); hunk headers differ (webhooks.ts: golden `@@ -404,14 +404,21 @@ webhooksRouter.get('/:id/deliveries', async (req: Request, res: Response) => {` vs run `@@ -404,6 +404,10 @@ webhooksRouter.get('/:id/deliveries', async (req: Request, res: Response) => {`); RUN PATCH APPLY MODE: NOT STRICT (strict=False) — whole-file `git apply -p1` strict refused (error: corrupt patch at line 29); applied PER SECTION with the options the checker recorded for this LOOSE rung (miscounted hunk header): section 1: `git apply -p1 --recount --ignore-whitespace`; section 2: `git apply -p1`; APPLIED RESULT DIFFERS: the two patches yield different files for webhooks.ts — read the diff before raising.

**Held 02:53 2026-10-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/webhooks.ts , Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/originate/src/routes/webhooks.ts
40	6	Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `[no PASS A3c line in checker.out — LOOSE BRIEF declared by `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1345-originate-deliveries-failed-query-500/KS-1345.md` (`RUNG 6, code_patch, jest: ONE product file described in PROSE`); checker.out INFO A3i verbatim: `INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured`]` — no expected_plus in the input; not re-measured here.
- A3i line absent from checker.out (not claimed)
- **APPLY MODE: NOT STRICT (strict=False) — recount only.** The run's `patch.diff` does not apply under strict `git apply -p1` (error: corrupt patch at line 29); it applies with [section 1: `git apply -p1 --recount --ignore-whitespace`; section 2: `git apply -p1`] (the options the checker recorded in section_<k>.opts for this LOOSE rung). Raise it with those options, or rewrite the hunk header and assert the blob equals the recounted result.
- **LOOSE BRIEF: product lines written by the model, not byte-checked against the brief; reviewer reads the hunk.** Declared by `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1345-originate-deliveries-failed-query-500/KS-1345.md` (`RUNG 6, code_patch, jest: ONE product file described in PROSE`); checker.out has `INFO A3i skipped` (no expected '+' lines) and no PASS A3c; A4-A7 passed (below). Golden comparison, as reported: CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) DIFFER in webhooks.ts; body lines (context included) DIFFER in webhooks.ts (run 23 vs golden 22 body lines — context, since the change lines are equal) (identical in ks1341c-webhooks-500-never-answers-err-message.test.ts); hunk headers differ (webhooks.ts: golden `@@ -404,14 +404,21 @@ webhooksRouter.get('/:id/deliveries', async (req: Request, res: Response) => {` vs run `@@ -404,6 +404,10 @@ webhooksRouter.get('/:id/deliveries', async (req: Request, res: Response) => {`); RUN PATCH APPLY MODE: NOT STRICT (strict=False) — whole-file `git apply -p1` strict refused (error: corrupt patch at line 29); applied PER SECTION with the options the checker recorded for this LOOSE rung (miscounted hunk header): section 1: `git apply -p1 --recount --ignore-whitespace`; section 2: `git apply -p1`; APPLIED RESULT DIFFERS: the two patches yield different files for webhooks.ts — read the diff before raising. Run's own golden_cmp.out [verbatim]: `golden tree 6efb0452e8687297aad491cb761ded770a8eee01 · patch tree not-built -> DIFFERS (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500_010847/*_cmp.index.out)`. A DIFFERS verdict is expected and acceptable for a loose brief — the verdict is A4-A7 plus the reviewer's read of the product hunk.
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/originate/src/routes/webhooks.ts: hunk 1 (@@ -404,6 +404,10 @@ webhooksRouter.get('/:id/deliveries', async (req: Request, res: Response) => {) declared old=6 new=10 but actual old=17 new=22`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (hunks=1, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: corrupt patch at line 27`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts fails at the untouched tip (3 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=3 of total=11; red cell(s): ['KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1345 D0: a REJECTED deliveries query reaches the catch: a constant 500, logged once, never a 200 []', 'KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1345 D4: a well-formed id that is not a UUID still answers 200 with an empty list, and the query is never run', 'KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text RED KS-1345 D3 SOURCE: exactly one best-effort .catch(() => []) is left in the router, the dispatchEvent subscription read']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts passes with the product hunk (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1093 failed=0 | after: total=1096 failed=0` · `NEW reds: []` [baseline_suite.json total=1093 failed=0; after_suite.json total=1096 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +46/-7 test=src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (+40/-6); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ae9bf6828f88131dfcc0b410f14c2f436903eb49` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -404,6 +404,10 @@ webhooksRouter.get('/:id/deliveries', async (req: Request, res: Response) => {
     if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(req.params.id)) {
       return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid webhook id format' } });
     }
+    // KS-1345: a well-formed id that is not a UUID must keep its current 200 [] answer, and the
+    // database query must not run for it (the ::uuid cast would otherwise 500 once the swallower is gone).
+    if (!UUID_PATTERN.test(req.params.id)) {
+      return res.json({ success: true, deliveries: [] });
+    }
     const db = (req as any).db || prisma;
     const rows = await db.$queryRaw`
       SELECT id, event_type, response_status, success, attempt, error, duration_ms, delivered_at
       FROM svc_webhook_deliveries
       WHERE webhook_id = ${req.params.id}::uuid
       ORDER BY delivered_at DESC
       LIMIT 50
-    `.catch(() => []);
+    `;
 
     res.json({ success: true, deliveries: rows });
   } catch (err: any) {
     fail500(res, 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)', err);
   }
 });
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts
@@ -4,9 +4,9 @@
 // also carries the whole-file SOURCE cell, which is RED until all seven are converted.
 // Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
 //
-// THE DELIVERIES TRAP. GET /:id/deliveries chains .catch(() => []) onto its query, so a REJECTED
-// $queryRaw is swallowed into a 200 with an empty list and never reaches the catch under test. That
-// cell therefore makes $queryRaw THROW SYNCHRONOUSLY; control C0 pins the swallowing branch.
+// THE DELIVERIES TRAP (closed by KS-1345). GET /:id/deliveries used to chain .catch(() => []) onto its query, so a
+// REJECTED $queryRaw was swallowed into a 200 with an empty list and never reached the catch under test; that
+// cell therefore makes $queryRaw THROW SYNCHRONOUSLY, and RED KS-1345 D0 now pins the REJECTED path too.
 // POST /:id/test awaits its query with no .catch, so a rejection reaches its catch directly.
 const mockQueryRaw = jest.fn();
 const mockLoggerError = jest.fn();
@@ -137,17 +137,51 @@ describe('KS-1341 part C: test-send and delivery history never answer a 500 with
     expect(contexts.filter((c) => !c)).toEqual([]);
   });
 
-  it('control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch', async () => {
-    // PRE-EXISTING behaviour this change must NOT alter, and the reason the deliveries cell throws
-    // synchronously: same route, same message, a rejected promise instead, a different answer.
+  it('RED KS-1345 D0: a REJECTED deliveries query reaches the catch: a constant 500, logged once, never a 200 []', async () => {
+    // KS-1345: the deliveries query's .catch swallowed a rejection into 200 { success: true, deliveries: [] }, so a
+    // database failure read as "no deliveries". Same route, same message, a rejected promise instead of the
+    // synchronous throw C1/C2 use: the answer must be the same.
     setNodeEnv('production');
     mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
     const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/deliveries');
+    const text = await res.text();
+    expect({ status: res.status, leaked: text.includes(LEAK) }).toEqual({ status: 500, leaked: false });
+    expect(JSON.parse(text)).toEqual(CONSTANT_BODY);
+    expect(mockLoggerError.mock.calls).toEqual([['Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)', { error: LEAK }]]);
+  });
+
+  it('control KS-1345 D: a deliveries query that RESOLVES still answers 200 with its rows and logs nothing', async () => {
+    // Without this, D0 is consistent with GET /:id/deliveries answering 500 always.
+    setNodeEnv('production');
+    const row = { id: '7a1f3d2b-2c3d-4e4f-9051-6b7c8d9e0f1a', event_type: 'document.created', success: true };
+    mockQueryRaw.mockResolvedValueOnce([row]);
+    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/deliveries');
+    expect(res.status).toBe(200);
+    expect(JSON.parse(await res.text())).toEqual({ success: true, deliveries: [row] });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('RED KS-1345 D4: a well-formed id that is not a UUID still answers 200 with an empty list, and the query is never run', async () => {
+    // With the swallow removed, "0" would reach the ::uuid cast and Postgres would answer 22P02, a 500. The route
+    // answered 200 [] for it before (the swallow). Moving it to 404, as the sibling write routes do, is a contract
+    // decision for another ticket, so it keeps its answer.
+    setNodeEnv('production');
+    const res = await fetch(baseUrl + '/api/webhooks/0/deliveries');
     expect(res.status).toBe(200);
     expect(JSON.parse(await res.text())).toEqual({ success: true, deliveries: [] });
+    expect(mockQueryRaw).not.toHaveBeenCalled();
     expect(mockLoggerError).not.toHaveBeenCalled();
   });
 
+  it('RED KS-1345 D3 SOURCE: exactly one best-effort .catch(() => []) is left in the router, the dispatchEvent subscription read', () => {
+    // dispatchEvent is a fire-and-forget fan-out and keeps its swallow on purpose; the two route reads do not.
+    // Zero means the fix went too far; two means the deliveries read still swallows.
+    const src = readFileSync(path.join(__dirname, '..', 'routes', 'webhooks.ts'), 'utf8');
+    const swallows = src.split('\n').filter((l) => !l.trim().startsWith('*') && !l.trim().startsWith('//') && l.includes('.catch(() => [])'));
+    expect(swallows.length).toBe(1);
+    expect(src.slice(src.indexOf('export async function dispatchEvent'))).toContain('.catch(() => [])');
+  });
+
   it('control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing', async () => {
     // Without this, every "not leaked" pass above is consistent with the router answering 500 always,
     // and it proves the helper did not flatten a message the route MEANT to return.
```
