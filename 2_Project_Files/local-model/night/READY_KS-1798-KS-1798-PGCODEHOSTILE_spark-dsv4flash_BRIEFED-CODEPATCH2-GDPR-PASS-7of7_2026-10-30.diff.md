# READY — KS-1798-KS-1798-PGCODEHOSTILE (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1798_p1_gdpr_pgcode_hostile/out.md.checker/patch.diff`** (from `ls` at 07:03 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1798_p1_gdpr_pgcode_hostile/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1798_p1_gdpr_pgcode_hostile/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 07:03 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1798_p1_gdpr_pgcode_hostile/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7152ac669d2d6af08be5b9dcd35132818377155d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/gdpr.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/gdpr.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/originate/src/routes/gdpr.ts
50	0	Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: gdpr.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/gdpr.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/gdpr.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts 50 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/gdpr.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 20 run; controls green; assertion reds)` [red_first.json: failed=3 of total=20; red cell(s): ['KS-445 POST /api/gdpr/dsr RED KS-1798 D1 POST /api/gdpr/dsr answers the constant 500 when the service rejects with a revoked Proxy', 'KS-445 POST /api/gdpr/dsr RED KS-1798 D2 POST /api/gdpr/dsr answers the constant 500 when the rejected Error has a pgCode getter that throws', 'KS-445 POST /api/gdpr/dsr RED KS-1798 D3 POST /api/gdpr/consent answers the constant 500 when the service rejects with a revoked Proxy']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (20 passed / 20 run)` [green_after.json: failed=0 of total=20, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1821 failed=0 | after: total=1826 failed=0` · `NEW reds: []` [baseline_suite.json total=1821 failed=0; after_suite.json total=1826 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/gdpr.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts` (+50/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/gdpr.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7152ac669d2d6af08be5b9dcd35132818377155d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1798_p1_gdpr_pgcode_hostile/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1798_p1_gdpr_pgcode_hostile/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/gdpr.ts
+++ b/Blockchain/Dev/services/originate/src/routes/gdpr.ts
@@ -136,7 +136,14 @@
  * if (mapGdprWriteDbError(err, res)) return;
  */
 function mapGdprWriteDbError(err: unknown, res: Response): boolean {
-  const pgCode = (err as { pgCode?: string } | null)?.pgCode ?? extractPgCode(err);
+  // KS-1798: the `pgCode` read touches the thrown value itself, so a revoked Proxy or a throwing getter would throw out of this function, out of the caller's catch, and the request would get no answer. A value that cannot be read has no `pgCode`.
+  let ownPgCode: string | undefined;
+  try {
+    ownPgCode = (err as { pgCode?: string } | null)?.pgCode;
+  } catch {
+    ownPgCode = undefined;
+  }
+  const pgCode = ownPgCode ?? extractPgCode(err);
   // FK violation (user_id → users) or a uuid cast failure: the subject user
   // does not exist → 404, never a 500.
   if (pgCode === '23503' || pgCode === '22P02') {
--- a/Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts
@@ -179,4 +179,54 @@
     const res = await post('dsr', { type: 'access', userId: USER_ID, email: 'subject@example.com' });
     expect(res.status).toBe(400);
   });
+
+  // KS-1798 (gate 12 finding 1795-2): mapGdprWriteDbError read `err.pgCode` before extractPgCode, so a thrown value whose property read throws escaped the catch of both callers and the request got NO answer.
+  // A request with no answer in 1500 ms is reported as the string NO ANSWER, so a hang is a red assertion, not a stuck run.
+  async function answerFor(path: string, body: unknown, reject: (thrown: unknown) => void, thrown: unknown): Promise<number | string> {
+    reject(thrown);
+    try {
+      const res = await fetch(`${baseUrl}/api/gdpr/${path}`, {
+        method: 'POST',
+        headers: { 'content-type': 'application/json' },
+        body: JSON.stringify(body),
+        signal: AbortSignal.timeout(1500),
+      });
+      return res.status;
+    } catch {
+      return 'NO ANSWER';
+    }
+  }
+  const dsrBody = { type: 'access', userId: USER_ID, email: 'subject@example.com' };
+  const consentBody = { userId: USER_ID, purpose: 'marketing' };
+  const revokedProxy = (): object => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    return proxy;
+  };
+  const throwingPgCodeGetter = (): object =>
+    Object.defineProperty(new Error('ks1798 pgCode getter'), 'pgCode', {
+      get(): string {
+        throw new Error('ks1798 pgCode getter threw');
+      },
+    });
+
+  it('RED KS-1798 D1 POST /api/gdpr/dsr answers the constant 500 when the service rejects with a revoked Proxy', async () => {
+    expect(await answerFor('dsr', dsrBody, (t) => mockCreateDSR.mockRejectedValueOnce(t), revokedProxy())).toBe(500);
+  });
+
+  it('RED KS-1798 D2 POST /api/gdpr/dsr answers the constant 500 when the rejected Error has a pgCode getter that throws', async () => {
+    expect(await answerFor('dsr', dsrBody, (t) => mockCreateDSR.mockRejectedValueOnce(t), throwingPgCodeGetter())).toBe(500);
+  });
+
+  it('RED KS-1798 D3 POST /api/gdpr/consent answers the constant 500 when the service rejects with a revoked Proxy', async () => {
+    expect(await answerFor('consent', consentBody, (t) => mockRecordConsent.mockRejectedValueOnce(t), revokedProxy())).toBe(500);
+  });
+
+  it('control KS-1798 D4 an ordinary Error from the DSR service is still answered 500', async () => {
+    expect(await answerFor('dsr', dsrBody, (t) => mockCreateDSR.mockRejectedValueOnce(t), new Error('ks1798 ordinary'))).toBe(500);
+  });
+
+  it('control KS-1798 D5 a tagged pgCode 23503 from the DSR service is still answered 404, read before the message text', async () => {
+    expect(await answerFor('dsr', dsrBody, (t) => mockCreateDSR.mockRejectedValueOnce(t), taggedDbError('Failed to create data subject request', '23503'))).toBe(404);
+  });
 });
```
