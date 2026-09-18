# READY — KS-1202 N-B (Ornith, briefed, TEST_ONLY) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = the fenced diff in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1202-ornith35b-night/out.md` (one test file; STRICT apply).**

**Held 2026-09-18 18:01 by the 14:4x Wednesday seat after a source read.** Tip `52df64f84`. Closes the #1024 tier-1 gate's N-B (DOCTYPEONLY + CASEFOLD at documents.ts:595 were 0 red).

## Source read
- Two cells inside describe.each(PRINCIPALS) (3 runs each): the legacy MATCHING shape → 201 stored/served as DEGREE; a data.documentType differing only in CASE → 400, nothing saved.
- '+' lines IDENTICAL to the brief, 0 '-'. T1-T8 PASS: green at tip 25/25; DOCTYPEONLY reds exactly the legacy runs; CASEFOLD exactly the case runs (assertions); controls green; documents.ts restored by sha256.
- **No product change.** Refs KS-1202 (G-TRIM not included). Test-only, tier 2.
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts
@@ -114,3 +114,9 @@
     expect(await create(principal, { title: 'qa', type: 'CERTIFICATE', data: { title: 'qa' } })).toEqual({ status: 201, code: null, saved: 1, storedType: 'CERTIFICATE', servedType: 'CERTIFICATE' });
   });
+  it('KS-1202 N-B - the legacy shape with a MATCHING data.documentType (type DEGREE, data DEGREE) is created and served as DEGREE', async () => {
+    expect(await create(principal, { title: 'qa', type: 'DEGREE', data: { title: 'qa', documentType: 'DEGREE' } })).toEqual({ status: 201, code: null, saved: 1, storedType: 'DEGREE', servedType: 'DEGREE' });
+  });
+  it('KS-1202 N-B - a data.documentType that differs only in CASE (type DEGREE, data degree) is refused 400, nothing saved', async () => {
+    expect(await create(principal, { title: 'qa', type: 'DEGREE', data: { title: 'qa', documentType: 'degree' } })).toEqual({ status: 400, code: 'BAD_REQUEST', saved: 0, storedType: null, servedType: null });
+  });
 });
```
