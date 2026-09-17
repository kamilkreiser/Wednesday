# READY — KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP (TEST-ONLY, jest, originate: a new top-level describe pins that /sign-cert still refuses a relabel when the source row has NO type — red under a line-pinned tamper at documents.ts:2590)
# VERDICT: Ornith r2 RESULT: PASS (7/7), apply_mode=STRICT. r1 FAILED A4 (a BRIEF defect, not the model: the fence's leading context contained a BLANK line, the model substituted non-blank context, header and context disagreed, the harness reanchored one line early and the block landed inside the issue describe — 3 existing controls red). The ONE rebrief under Kam's counter (email 2026-09-16 07:57Z) was spent on it and PASSED.
# Source read by Wednesday: the model's 13 `+` lines are IDENTICAL IN SEQUENCE to the brief fence, verified with a working mutated control (every single-character mutation of every non-blank line compares unequal — the first control written was a no-op on a line that did not contain the needle, and was re-run).
# Checker detail: A2 strict; A3 touched set = the ks1213 test only; A3c 12/12, A3d clean; A4 under the tamper 1 failed / 87 — exactly the declared cell `RED KS-1229 U1`, by assertion, controls green; A5 87/87; A6 originate 741 -> 743, 0 new red; A7 tsc rc 0.
# PLACEMENT: hunk at 209-211 (trailing, all-non-blank context). Disjoint from all six KS-1229 rows held earlier today (118-123, 145-150, 174-179, 179-184, 204-206, EOF 224-226) — all SEVEN can raise as ONE PR.
# PR NOTES: Refs KS-1229 (NOT Closes — this is the ticket's Q-SIGNCERT-UNTYPED-SOURCE-SKIP row). TIER 2 (test-only). Behaviour change: none. In-memory only: `fromDbRow` gives `type = document_type || 'document'`, so an untyped source is unreachable through Postgres — this pins the handler's own guard. Written from develop 34cdcfb26; re-read the ks1213 test and documents.ts at raise.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -209,3 +209,16 @@ describe.each(PRINCIPALS)('KS-1213 POST /api/certifications/issue with parentDocum
+describe('KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP - the sign-cert guard still refuses when the source has no type', () => {
+  const signCert = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-cert', { metadata });
+  it('RED KS-1229 U1 - an untyped source is refused a relabel, nothing saved', async () => {
+    // KS-1229 (Q-SIGNCERT-UNTYPED-SOURCE-SKIP): an untyped in-memory source must not skip the guard.
+    seed(undefined as unknown as string);
+    expect(await signCert({ documentType: 'DEGREE' })).toEqual(REFUSED);
+  }); // KS-1229 U1
+  it('control - KS-1229 a typed source is still refused a differing relabel', async () => {
+    seed('DOCUMENT');
+    expect(await signCert({ documentType: 'PROPERTY_DEED' })).toEqual(REFUSED);
+  }); // KS-1229 U control
+});
+
 describe('KS-1202 create guard - the properties its gate left unpinned (#1024 N-B)', () => {
   const create = async (b: Record<string, unknown>) => {
     const r = await write(ISSUER, '/api/documents', b);
```
