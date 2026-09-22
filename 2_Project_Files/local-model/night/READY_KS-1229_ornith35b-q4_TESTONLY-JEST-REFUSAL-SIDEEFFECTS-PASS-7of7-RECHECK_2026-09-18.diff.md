# READY — KS-1229 (TEST-ONLY, jest, originate: three cells in the ks1213 issue describe.each pin that a REFUSED derived issue sends nothing upstream — R1 no /api/users/stub call, R2 no anchoring job, plus a control that sees both calls; red under the tamper at routes/certifications.ts:201)
# VERDICT: Ornith r1 (and its retry) FAILED only because the harness mis-placed a correct hunk (fuzzy -C1 at :174 vs header :204). The harness fix (A2 CONTEXT-WS + FUZZY-MISPLACED guard, arms 16/16 re-run by Wednesday) RE-CHECKED the SAME out.md: RESULT: PASS (7/7), apply_mode=context-ws at 205 (retry: at 204). A harness re-check, NOT a model round.
# Source read by Wednesday: the model's 43 `+` lines IDENTICAL in sequence to the brief fence in BOTH samples (a one-character mutated copy unequal). The diff below is the brief's fence (tip-exact context lines); the model's own diff differs only in re-indenting one trailing context line (`});` -> `  });`).
# PR NOTES: Refs KS-1229 (NOT Closes: only rows X-ISSUE-AFTER-HOLDER + X-ISSUE-AFTER-ANCHOR are pinned). TIER 2 (test-only). originate 741 -> 750, no new red (A6). R2 and the control set and delete ANCHORING_SERVICE_URL in finally (unset today). Written from develop 3961c2add; the ks1213 test and certifications.ts are untouched by #1035 (merged 34cdcfb26) — re-read at raise.

```diff
     expect([r.status, r.saved]).toEqual([201, 0]);
     expect(mockSaveCertification).toHaveBeenCalledTimes(1);
   });
+  it('RED KS-1229 R1 - a refused issue with holderEmail sends nothing to the users/stub upstream', async () => {
+    // KS-1229 (X-ISSUE-AFTER-HOLDER): users/stub mints or resolves an INVITED user in auth, so the refusal must come first.
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    try {
+      const r = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' }, holderEmail: 'holder-ks1229@example.test', parentDocumentId: SOURCE_ID });
+      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
+    } finally {
+      stub.off('request', onUpstream);
+    }
+  }); // KS-1229 R1
+  it('RED KS-1229 R2 - a refused issue submits no anchoring job', async () => {
+    // KS-1229 (X-ISSUE-AFTER-ANCHOR): the anchoring base points at the loopback stub for this cell only.
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    process.env.ANCHORING_SERVICE_URL = process.env.AUTH_SERVICE_URL;
+    try {
+      const r = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' }, parentDocumentId: SOURCE_ID });
+      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
+    } finally {
+      stub.off('request', onUpstream);
+      delete process.env.ANCHORING_SERVICE_URL;
+    }
+  }); // KS-1229 R2
+  it('control - KS-1229 an accepted issue reaches /api/anchors and a holderEmail issue reaches /api/users/stub on the loopback stub', async () => {
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    process.env.ANCHORING_SERVICE_URL = process.env.AUTH_SERVICE_URL;
+    try {
+      const accepted = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'DOCUMENT' }, parentDocumentId: SOURCE_ID });
+      const invited = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'DOCUMENT' }, holderEmail: 'holder-ks1229@example.test', parentDocumentId: SOURCE_ID });
+      expect([accepted.status, invited.status, upstreamUrls]).toEqual([201, 404, ['/api/anchors', '/api/users/stub']]);
+    } finally {
+      stub.off('request', onUpstream);
+      delete process.env.ANCHORING_SERVICE_URL;
+    }
+  }); // KS-1229 control
 });
 
 describe('KS-1202 create guard - the properties its gate left unpinned (#1024 N-B)', () => {
```

# SUPERSEDED-BY: night/briefs/KS-1229-R16B-SIDEEFFECTS.md (feed7 drafter, 2026-09-22 08:56:00 AEST) - re-briefed at develop 3916eacd12af23bfd464440b4c770f7da0f2dd96; this READY stays as the record of the original PASS, never raise it as-is.
