# READY — KS-1229 X-SIGNWALLET-SERVED (TEST-ONLY, jest, originate: sign-wallet compares with the STORED type, not the served label)
# FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — INSERT the block after line 176 (the `});` closing describe.each(WRITERS)), before the blank line 177. Hunk `@@ -174,6 +174,19 @@`, strict apply, no fuzzy.
# VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night5). A2 strict; A3c 12/12; A4 1 failed / 87 — the declared cell SW1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
# Source read by Wednesday: the model's 13 `+` lines IDENTICAL in sequence to the brief fence (a mutated copy unequal); its three context lines equal tip lines 174-176 exactly.
# TAMPER used to prove the red (NOT part of this diff): documents.ts:2859 — `source.type` -> `source.data?.documentType ?? source.type`, LINE-PINNED because that guard text also sits at :1980 (/version) and :2590 (/sign-cert).
# WHY THE CONTROL IS SOUND: it uses an ordinary source with no `data.documentType`, so the tampered expression reduces to the tip's — green on BOTH trees by construction, which is what lets A4's "controls green" mean something here.
# PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-SIGNWALLET-SERVED only). TIER 2 (test-only). Behaviour change: none.
# RAISE WITH the three siblings as ONE PR: READY_KS-1229-SIGNWALLET (174-179) · READY_KS-1229-LOOSE (179-184) · READY_KS-1229_…-RECHECK (204-209) · READY_KS-1229-SIGNCERT (EOF) — `Refs KS-1229 (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR, X-ISSUE-LOOSE, X-SIGNCERT-AFTER-UPSTREAM, X-SIGNWALLET-SERVED)`. Apply lowest-line-first; later hunks take their offsets. NOTE: this hunk's lower context (177-179) is the LOOSE hunk's upper neighbourhood — apply this one FIRST, then LOOSE, and let patch offset.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -174,6 +174,19 @@ describe.each(WRITERS)('KS-1213 %s', (_writer, path, body) => {
     });
   });
 });
+
+describe('KS-1229 X-SIGNWALLET-SERVED - sign-wallet compares with the STORED type, not the served label', () => {
+  const signWallet = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata });
+  it('RED KS-1229 SW1 - a legacy source served as DEGREE still refuses metadata.documentType DEGREE', async () => {
+    // KS-1229 (X-SIGNWALLET-SERVED): the new row would be STORED CERTIFICATE and SERVED DEGREE - the relabel KS-1213 closed.
+    seed('CERTIFICATE', { documentType: 'DEGREE' });
+    expect(await signWallet({ documentType: 'DEGREE' })).toEqual(REFUSED);
+  }); // KS-1229 SW1
+  it('control - KS-1229 an ordinary source accepts a metadata.documentType equal to its stored type', async () => {
+    seed('DOCUMENT');
+    expect(await signWallet({ documentType: 'DOCUMENT' })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
+  }); // KS-1229 SW control
+});
 
 describe.each(PRINCIPALS)('KS-1213 POST /api/certifications/issue with parentDocumentId as %s', (_who, principal) => {
   const issue = (b: Record<string, unknown>) => write(principal, '/api/certifications/issue', b);
```
