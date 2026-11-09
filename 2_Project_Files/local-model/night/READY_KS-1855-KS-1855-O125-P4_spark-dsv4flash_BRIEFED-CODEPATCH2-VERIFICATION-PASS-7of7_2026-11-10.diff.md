# READY — KS-1855-KS-1855-O125-P4 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/out.md.checker/patch.diff`** (from `ls` at 03:41 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on-control-r2/out.md.checker/patch.diff` rc 0, Wednesday spark operator o125).

**Held 03:41 2026-11-10 by Wednesday spark operator o125 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/verification.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
20	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts
4	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verification.ts`
- CODE_PATCH2 (rung 3, 1 product files + 2 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts`, `Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/verification.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts 20 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts 4 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 22 run; controls green; assertion reds)` [red_first.json: failed=2 of total=22; red cell(s): ['KS-1628 — the gateway no longer serves POST /api/documents/:id/verify RED KS-1855 H1: with ENABLE_MOCK_ENDPOINTS unset the certifications twin is unanswered by the router', 'KS-1628 — the gateway no longer serves POST /api/documents/:id/verify RED KS-1855 H2: with ENABLE_MOCK_ENDPOINTS true but NODE_ENV production the certifications twin is unanswered by the router']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (22 passed / 22 run)` [green_after.json: failed=0 of total=22, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1882 failed=0 | after: total=1884 failed=0` · `NEW reds: []` [baseline_suite.json total=1882 failed=0; after_suite.json total=1884 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=1 tests=2 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` (+20/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/verification.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1855_o125_p4_gateway_certification_verify_stand_in_answers_only_when_mock_endpoints_are_on/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -377,3 +377,10 @@
   // Certification verify endpoint (for test compatibility)
-  router.post('/api/certifications/:id/verify', mockBodyParser, async (req: Request, res: Response) => {
+  // KS-1855 half two (Kam's card secuura-ks1855-gateway-standin-routes-1110 = c): this stand-in answers only when the gateway's own mock-endpoints
+  // flag is on (ENABLE_MOCK_ENDPOINTS=true and NODE_ENV not production, the gate of the mock wallet routes in index.ts). Otherwise the request goes on
+  // to the next router (the proxy) UNTOUCHED: the gate runs before mockBodyParser, which would consume the body the proxy needs.
+  const certificationVerifyStandInOn: RequestHandler = (_req, _res, next) => {
+    if (process.env.NODE_ENV !== 'production' && process.env.ENABLE_MOCK_ENDPOINTS === 'true') { next(); return; }
+    next('route');
+  };
+  router.post('/api/certifications/:id/verify', certificationVerifyStandInOn, mockBodyParser, async (req: Request, res: Response) => {
     const { id } = req.params;
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts
@@ -205,4 +205,7 @@
     // Same status, different answerer: that is the discriminator G2 relies on.
+    // KS-1855 half two: the twin answers only with the gateway's mock-endpoints flag on, so this control turns it on.
+    vi.stubEnv('ENABLE_MOCK_ENDPOINTS', 'true');
     const registered = pathsFor(verificationRouter, 'post');
     const r = await postToRouter(`/api/certifications/${DOC_ID}/verify`);
+    vi.unstubAllEnvs();
     expect([registered.includes('/api/certifications/:id/verify'), r.answeredByAHandler, r.status]).toEqual([true, true, 404]);
@@ -240,2 +243,19 @@
   });
+
+  // KS-1855 half two (Kam's card secuura-ks1855-gateway-standin-routes-1110 = c): "gate certification verify behind the test flag". With the
+  // flag unset, or set but NODE_ENV production, the twin does not answer: the request is left for the next router (here, express's HTML 404).
+  it('RED KS-1855 H1: with ENABLE_MOCK_ENDPOINTS unset the certifications twin is unanswered by the router', async () => {
+    vi.stubEnv('ENABLE_MOCK_ENDPOINTS', '');
+    const r = await postToRouter(`/api/certifications/${DOC_ID}/verify`);
+    vi.unstubAllEnvs();
+    expect([r.status, r.answeredByAHandler]).toEqual([404, false]);
+  });
+
+  it('RED KS-1855 H2: with ENABLE_MOCK_ENDPOINTS true but NODE_ENV production the certifications twin is unanswered by the router', async () => {
+    vi.stubEnv('ENABLE_MOCK_ENDPOINTS', 'true');
+    vi.stubEnv('NODE_ENV', 'production');
+    const r = await postToRouter(`/api/certifications/${DOC_ID}/verify`);
+    vi.unstubAllEnvs();
+    expect([r.status, r.answeredByAHandler]).toEqual([404, false]);
+  });
 });
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts
@@ -168,2 +168,6 @@
 describe('KS-815 — the proxyPaths verify route rejects a control byte in the body', () => {
+  // KS-1855 half two: this stand-in route is registered to answer only with the gateway's mock-endpoints flag on.
+  beforeAll(() => { vi.stubEnv('ENABLE_MOCK_ENDPOINTS', 'true'); });
+  afterAll(() => { vi.unstubAllEnvs(); });
+
   it('POST /api/certifications/:id/verify refuses a NUL', async () => {
```

---
## Operator o125 footer (appended after the hold; not generated by hold_ready.py)
**TIER 1 GATE OWED** (verification path; Kam's card secuura-ks1855-gateway-standin-routes-1110 = c, half two). FLAG = the gateway's existing `ENABLE_MOCK_ENDPOINTS=true` with `NODE_ENV !== 'production'` (index.ts 883-884), the operator's choice (the card says "the test flag" without naming one); read per request. Gate runs BEFORE `mockBodyParser` (the route's prefix is on proxyPaths; the parser would eat the body the proxy needs). First form (product + new test) turned 3 existing cells red (ks1628 G-C2, two ks815 NUL cells), so this carries edits to those two tests and no new file. Default behaviour change: with the flag unset the route reaches originate's real `POST /:id/verify` (certifications.ts 1247-1275); the stale comment at verification.ts 446-447 ("originate doesn't expose") is wrong and left. Peter's E2E (verifier-exhaustive.prelaunch.spec.ts:298) flag setting: UNMEASURED. Same file as the KS-1952 hold.
