# READY — KS-1345-LIST-1 (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1345-list/out.md.checker/patch.diff`** (from `ls` at 02:25 2026-10-05; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1345-list/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1345-list/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1345-list/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1345-list/precheck/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 02:25 2026-10-05 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1345-list/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2d85b84e1012961c880daa3de70d8491fc0a2ff9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/webhooks.ts , Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	3	Blockchain/Dev/services/originate/src/routes/webhooks.ts
23	10	Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/webhooks.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts fails at the untouched tip (1 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=1 of total=9; red cell(s): ['KS-1341 part A: GET / and POST / never answer a 500 with the thrown text RED KS-1345 A0: a REJECTED list query reaches the catch: a constant 500, logged once, never a 200 []']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts passes with the product hunk (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1062 failed=0 | after: total=1063 failed=0` · `NEW reds: []` [baseline_suite.json total=1062 failed=0; after_suite.json total=1063 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +28/-13 test=src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+5/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (+23/-10); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2d85b84e1012961c880daa3de70d8491fc0a2ff9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1345-list/input.json`. Brief (given by --brief; its `# ` heading names KS-1345): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1345-list/KS-1345.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1345-list/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -187,14 +187,16 @@
     // KS-466: organization_id is a uuid column, so the bind param needs an
     // explicit ::uuid cast — without it Postgres raises 42883 (uuid = text has
-    // no operator). The error was silently swallowed by the .catch below, so
+    // no operator). The error was silently swallowed by a .catch on this query, so
     // this list ALWAYS returned [] (a pre-existing bug, independent of RLS).
+    // KS-1345: that .catch is gone. A failed list query now reaches fail500 below
+    // (a constant 500, the error logged), never a 200 with an empty list.
     const rows = await db.$queryRaw`
       SELECT id, url, events, is_active, description, created_at, updated_at
       FROM svc_webhooks
       WHERE organization_id = ${userId}::uuid OR app_id IS NOT NULL
       ORDER BY created_at DESC
-    `.catch((e: any) => { logger.warn('webhooks list query failed', { error: e?.message }); return []; });
-
+    `;
+
     res.json({ success: true, webhooks: rows });
   } catch (err: any) {
     fail500(res, 'Webhook list failed (GET /api/webhooks)', err);
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
@@ -4,11 +4,11 @@
 // file's fail500 helper and converts the first two sites; parts B and C convert the other five.
 // Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
 //
-// THE GET / TRAP. GET / chains .catch() onto its list query, so a REJECTED $queryRaw is swallowed into
-// a 200 with an empty list and never reaches the catch under test. The GET / cell therefore makes
-// $queryRaw THROW SYNCHRONOUSLY, and every red cell asserts the catch was REACHED (the logger received
-// this route's context with the thrown text), not only that the body is clean. control A0 pins the
-// swallowing branch so the trap cannot come back silently.
+// THE GET / TRAP (until KS-1345). GET / chained .catch() onto its list query, so a REJECTED $queryRaw was
+// swallowed into a 200 with an empty list and never reached the catch under test. The GET / cell therefore
+// makes $queryRaw THROW SYNCHRONOUSLY, and every red cell asserts the catch was REACHED (the logger received
+// this route's context with the thrown text), not only that the body is clean. KS-1345 removed that .catch:
+// cell A0 now pins that a REJECTED list query reaches the same catch, so the swallow cannot come back silently.
 const mockQueryRaw = jest.fn();
 const mockExecuteRaw = jest.fn();
 const mockLoggerError = jest.fn();
@@ -125,14 +125,27 @@
     expect(reply.status).toBe(500);
     expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
   });
-
-  it('control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch', async () => {
-    // PRE-EXISTING behaviour this change must NOT alter, and the reason the GET / cell throws
-    // synchronously: same route, same message, a rejected promise instead, a different answer.
+
+  it('RED KS-1345 A0: a REJECTED list query reaches the catch: a constant 500, logged once, never a 200 []', async () => {
+    // KS-1345: the list query's .catch swallowed a rejection into 200 { success: true, webhooks: [] }, so a
+    // database failure read as "no webhooks". Same route, same message, a rejected promise instead of the
+    // synchronous throw A1/A2 use: the answer must be the same.
     setNodeEnv('production');
     mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
     const res = await fetch(baseUrl + '/api/webhooks');
+    const text = await res.text();
+    expect({ status: res.status, leaked: text.includes(LEAK) }).toEqual({ status: 500, leaked: false });
+    expect(JSON.parse(text)).toEqual(CONSTANT_BODY);
+    expect(mockLoggerError.mock.calls).toEqual([['Webhook list failed (GET /api/webhooks)', { error: LEAK }]]);
+  });
+
+  it('control KS-1345 C: a list query that RESOLVES still answers 200 with its rows and logs nothing', async () => {
+    // Without this, A0 is consistent with GET / answering 500 always.
+    setNodeEnv('production');
+    const row = { id: '6f0e2c1a-1b2c-4d3e-8f40-5a6b7c8d9e0f', url: 'https://partner.example.com/hooks' };
+    mockQueryRaw.mockResolvedValueOnce([row]);
+    const res = await fetch(baseUrl + '/api/webhooks');
     expect(res.status).toBe(200);
-    expect(JSON.parse(await res.text())).toEqual({ success: true, webhooks: [] });
+    expect(JSON.parse(await res.text())).toEqual({ success: true, webhooks: [row] });
     expect(mockLoggerError).not.toHaveBeenCalled();
   });
```
