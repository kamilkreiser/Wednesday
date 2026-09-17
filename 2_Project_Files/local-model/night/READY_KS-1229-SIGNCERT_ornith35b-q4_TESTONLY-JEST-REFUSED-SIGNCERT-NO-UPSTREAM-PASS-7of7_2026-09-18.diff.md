# READY — KS-1229 X-SIGNCERT-AFTER-UPSTREAM (TEST-ONLY, jest, originate: a refused /sign-cert must reach no upstream)
# FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — APPEND the block at EOF (context = the file's last three lines, 224-226 at tip 34cdcfb26). Hunk `@@ -224,3 +224,32 @@`, strict apply, no fuzzy.
# VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night4). A2 strict; A3c 28/28; A4 1 failed / 87 — the declared cell SC1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
# Source read by Wednesday: the model's 29 `+` lines IDENTICAL in sequence to the brief fence (a one-word mutated copy unequal); its three context lines equal the file's last three lines exactly (no dialect corruption this time).
# TAMPER used to prove the red (NOT part of this diff): documents.ts:2590 — the sign-cert KS-1213 guard, LINE-PINNED because that exact guard text also sits at :1980 (/version) and :2859 (/sign-wallet), which stay untouched.
# PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-SIGNCERT-AFTER-UPSTREAM only). TIER 2 (test-only). Behaviour change: none.
# RAISE WITH the two siblings as ONE PR — READY_KS-1229_…-RECHECK (hunk 204-209) and READY_KS-1229-LOOSE (179-184) — this one appends at EOF, so no hunk overlaps another: `Refs KS-1229 (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR, X-ISSUE-LOOSE, X-SIGNCERT-AFTER-UPSTREAM)`. Apply lowest-line-first and let later hunks take their offsets.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -224,3 +224,32 @@ describe('KS-1202 create guard - the properties its gate left unpinned (#1024 N-B)', () => {
     expect(await create({ data: { title: 'nb', documentType: 'DOCUMENT' } })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
   });
 });
+
+describe('KS-1229 X-SIGNCERT-AFTER-UPSTREAM - a refused sign-cert reaches no upstream', () => {
+  const signCert = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-cert', { metadata });
+  it('RED KS-1229 SC1 - a refused sign-cert sends nothing to the issuer-certs upstream', async () => {
+    // KS-1229 (X-SIGNCERT-AFTER-UPSTREAM): the sign request is a real upstream call, so the refusal must come first.
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    try {
+      const r = await signCert({ documentType: 'PROPERTY_DEED' });
+      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
+    } finally {
+      stub.off('request', onUpstream);
+    }
+  }); // KS-1229 SC1
+  it('control - KS-1229 an accepted sign-cert does reach the issuer-certs upstream', async () => {
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    try {
+      const r = await signCert({ documentType: 'DOCUMENT' });
+      expect([r.status, upstreamUrls]).toEqual([201, ['/api/issuer-certs/sign']]);
+    } finally {
+      stub.off('request', onUpstream);
+    }
+  }); // KS-1229 SC control
+});
```
