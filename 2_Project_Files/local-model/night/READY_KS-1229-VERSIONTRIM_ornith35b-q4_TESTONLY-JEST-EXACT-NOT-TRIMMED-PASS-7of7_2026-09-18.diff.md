# READY — KS-1229 X-VERSION-TRIM (TEST-ONLY, jest, originate: /version compares EXACTLY, so a padded carrier is refused)
# FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — INSERT the block after line 147 (the `];` closing the WRITERS table), before the blank line 148. Hunk `@@ -145,6 +145,19 @@`, strict apply, no fuzzy.
# VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night6). A2 strict; A3c 12/12; A4 1 failed / 87 — the declared cell VT1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
# Source read by Wednesday: the model's 13 `+` lines IDENTICAL in sequence to the brief fence; **the single TRAILING SPACE inside `version('DOCUMENT ')` survived** (it is the whole point of the cell, and a mutated control with the space removed is unequal); its three context lines equal tip 145-147 exactly, backticks and `${SOURCE_ID}` included.
# TAMPER used to prove the red (NOT part of this diff): documents.ts:1980 — `!== source.type` -> `(typeof x !== 'string' || x.trim() !== source.type)`, LINE-PINNED because that guard text also sits at :2590 (/sign-cert) and :2859 (/sign-wallet).
# PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-VERSION-TRIM only). TIER 2 (test-only). Behaviour change: none.
# RAISE WITH the four siblings as ONE PR — this one (145-150) · SIGNWALLET (174-179) · LOOSE (179-184) · RECHECK (204-209) · SIGNCERT (EOF): `Refs KS-1229 (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR, X-ISSUE-LOOSE, X-SIGNCERT-AFTER-UPSTREAM, X-SIGNWALLET-SERVED, X-VERSION-TRIM)`. Apply lowest-line-first; later hunks take their offsets.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -145,6 +145,19 @@ const WRITERS: Array<[string, string, (metadata?: Record<string, unknown>) => R
   ['/sign-cert', `/api/documents/${SOURCE_ID}/sign-cert`, (metadata) => ({ ...(metadata ? { metadata } : {}) })],
   ['/sign-wallet', `/api/documents/${SOURCE_ID}/sign-wallet`, (metadata) => ({ walletAddress: 'addr_test1ks1213', signature: 'a1', key: 'a2', ...(metadata ? { metadata } : {}) })],
 ];
+
+describe('KS-1229 X-VERSION-TRIM - the /version guard compares EXACTLY, so a padded carrier is refused', () => {
+  const version = (documentType: string) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/version', { action: 'watermark', newContentHash: HASH, metadata: { documentType } });
+  it('RED KS-1229 VT1 - a trailing-space carrier is refused, never trimmed into a match', async () => {
+    // KS-1229 (X-VERSION-TRIM): trimming would store DOCUMENT and serve the padded label - a relabel by invisible whitespace.
+    seed('DOCUMENT');
+    expect(await version('DOCUMENT ')).toEqual(REFUSED);
+  }); // KS-1229 VT1
+  it('control - KS-1229 the exact carrier is accepted and served as that type', async () => {
+    seed('DOCUMENT');
+    expect(await version('DOCUMENT')).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
+  }); // KS-1229 VT control
+});
 
 describe.each(WRITERS)('KS-1213 %s', (_writer, path, body) => {
   describe.each(PRINCIPALS)('as %s', (_who, principal) => {
```
