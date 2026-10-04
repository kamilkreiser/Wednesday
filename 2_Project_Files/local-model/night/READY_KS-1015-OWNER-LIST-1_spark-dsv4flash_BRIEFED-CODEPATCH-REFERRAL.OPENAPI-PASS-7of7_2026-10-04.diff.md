# READY — KS-1015-OWNER-LIST-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-04_KS-1015-owner-list/out.md.checker/patch.diff`** (from `ls` at 19:08 2026-10-04; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-04_KS-1015-owner-list/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-04_KS-1015-owner-list/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-04_KS-1015-owner-list/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1015-owner-list/precheck/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 19:08 2026-10-04 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-04_KS-1015-owner-list/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/referral/src/referral.openapi.ts , Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/referral/src/referral.openapi.ts` (product) and `Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
31	4	Blockchain/Dev/services/referral/src/referral.openapi.ts
48	3	Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (31 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 31 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 4.
- A3i line absent from checker.out (not claimed)
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/referral/src/referral.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts fails at the untouched tip (3 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=3 of total=10; red cell(s): ['KS-1015: GET /api/referrals/{code} publishes the envelope its handler returns RED gate52 N-1367-1 O1: the owner list 200 is the success/data envelope over two shapes, not a codes array', 'KS-1015: GET /api/referrals/{code} publishes the envelope its handler returns RED gate52 N-1367-1 O2: the no-code shape is hasCode false with a message', 'KS-1015: GET /api/referrals/{code} publishes the envelope its handler returns RED gate52 N-1367-1 O3: the has-code shape carries the code, its stats and the milestone progress']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts passes with the product hunk (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=34 failed=0 | after: total=38 failed=0` · `NEW reds: []` [baseline_suite.json total=34 failed=0; after_suite.json total=38 failed=0]
- A6 [verbatim]: `PASS A6 whole services/referral suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/referral: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +79/-7 test=src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/referral/src/referral.openapi.ts` (+31/-4 per numstat.out) and the test file `Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts` (+48/-3); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-04_KS-1015-owner-list/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-04_KS-1015-owner-list/checker.out`.

```diff
--- a/Blockchain/Dev/services/referral/src/referral.openapi.ts
+++ b/Blockchain/Dev/services/referral/src/referral.openapi.ts
@@ -44,4 +44,5 @@
-const ReferralCodeSchema = sharedRegistry.register(
+// gate52 N-1367-1: no operation returns the ReferralCode record any more; it stays a published component.
+sharedRegistry.register(
   'ReferralCode',
   z
     .object({
@@ -539,16 +540,42 @@
   method: 'get',
   path: '/api/referrals/user/{userId}',
   tags: ['Referrals'],
-  summary: 'List referral codes owned by a user',
+  summary: 'Get the referral code and stats of a user',
   security: [{ bearerAuth: [] }],
   request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
   responses: {
     400: commonErrorResponses[400],
     200: {
-      description: 'Codes',
+      description: 'Referral code and stats, or hasCode false when the user has none',
+      // gate52 N-1367-1: the handler (routes/referrals.ts, GET /user/:userId) answers a success/data envelope
+      // in one of two shapes told apart by hasCode: { hasCode: false, message } when the user has no code,
+      // else the primary code, its stats and the milestone progress. It never returns a codes array, so the
+      // spec follows the runtime (the issuer ReferralDashboard reads data.hasCode and data.referralCode).
       content: {
         'application/json': {
-          schema: z.object({ codes: z.array(ReferralCodeSchema) }),
+          schema: successEnvelope(
+            z.union([
+              z.object({ hasCode: z.literal(false), message: z.string() }),
+              z.object({
+                hasCode: z.literal(true),
+                referralCode: z.object({
+                  code: z.string(),
+                  shareUrl: z.string(),
+                  isActive: z.boolean(),
+                  expiresAt: z.string().optional(),
+                }),
+                stats: z.object({
+                  totalReferrals: z.number().int(),
+                  qualifiedReferrals: z.number().int(),
+                  conversionRate: z.string(),
+                  totalRewardsEarned: z.string(),
+                  pendingRewards: z.string(),
+                }),
+                milestoneProgress: z.record(z.string(), z.unknown()),
+                pendingRewardsCount: z.number().int(),
+              }),
+            ]),
+          ),
         },
       },
     },
--- a/Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts
+++ b/Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts
@@ -64,4 +64,49 @@
+  it('RED gate52 N-1367-1 O1: the owner list 200 is the success/data envelope over two shapes, not a codes array', () => {
+    const s = body('/api/referrals/user/{userId}', 'get', '200');
+    expect({ codes: s?.properties?.codes, required: s?.required, shapes: s?.properties?.data?.anyOf?.length }).toEqual({
+      codes: undefined,
+      required: ['success', 'data'],
+      shapes: 2,
+    });
+  });
+
+  it('RED gate52 N-1367-1 O2: the no-code shape is hasCode false with a message', () => {
+    const shapes: AnyObj[] = body('/api/referrals/user/{userId}', 'get', '200')?.properties?.data?.anyOf ?? [];
+    const none = shapes.find((b) => b?.properties?.hasCode?.enum?.[0] === false);
+    expect({ required: none?.required, message: none?.properties?.message?.type }).toEqual({
+      required: ['hasCode', 'message'],
+      message: 'string',
+    });
+  });
+
+  it('RED gate52 N-1367-1 O3: the has-code shape carries the code, its stats and the milestone progress', () => {
+    const shapes: AnyObj[] = body('/api/referrals/user/{userId}', 'get', '200')?.properties?.data?.anyOf ?? [];
+    const has = shapes.find((b) => b?.properties?.hasCode?.enum?.[0] === true);
+    const stats: AnyObj = has?.properties?.stats?.properties ?? {};
+    expect({
+      required: [...(has?.required ?? [])].sort(),
+      code: [...(has?.properties?.referralCode?.required ?? [])].sort(),
+      stats: Object.fromEntries(Object.entries(stats).map(([k, v]) => [k, (v as AnyObj).type])),
+    }).toEqual({
+      required: ['hasCode', 'milestoneProgress', 'pendingRewardsCount', 'referralCode', 'stats'],
+      code: ['code', 'isActive', 'shareUrl'],
+      stats: {
+        totalReferrals: 'integer',
+        qualifiedReferrals: 'integer',
+        conversionRate: 'string',
+        totalRewardsEarned: 'string',
+        pendingRewards: 'string',
+      },
+    });
+  });
+
+  it('control gate52 N-1367-1 C4: the owner list keeps bearerAuth, its path parameter userId, and its 403', () => {
+    const op = operation('/api/referrals/user/{userId}', 'get');
+    expect(op?.security).toEqual([{ bearerAuth: [] }]);
+    expect((op?.parameters ?? []).map((q: AnyObj) => q.in + ':' + q.name + ':' + q.required)).toEqual(['path:userId:true']);
+    expect(Object.keys(op?.responses ?? {})).toEqual(expect.arrayContaining(['200', '403']));
+  });
+
-  it('control KS-1015 C2: the ReferralCode component stays published and the owner list still returns it', () => {
-    expect(doc.components?.schemas?.ReferralCode).toBeDefined();
-    expect(body('/api/referrals/user/{userId}', 'get', '200')?.properties?.codes?.items?.$ref).toBe('#/components/schemas/ReferralCode');
+  it('control KS-1015 C2: the ReferralCode component stays published though no operation returns it', () => {
+    expect(Object.keys(doc.components?.schemas ?? {})).toContain('ReferralCode');
   });
```
