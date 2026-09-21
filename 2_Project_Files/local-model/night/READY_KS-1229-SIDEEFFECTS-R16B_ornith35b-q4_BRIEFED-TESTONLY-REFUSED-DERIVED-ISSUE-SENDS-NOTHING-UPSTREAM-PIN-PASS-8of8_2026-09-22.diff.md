# READY — KS-1229-SIDEEFFECTS-R16B (Ornith, briefed, test_only, modify · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night6/out.md.checker/patch.diff`** (from `ls` at 09:34 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night6/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed7-drafter-precheck/1229SIDEEFFECTS-R16B/out.md.checker/patch.diff` rc 0, Wednesday (the 07:2x seat)).

**Held 09:34 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night6/out.md.checker`, not typed).** Tip `3916eacd12af23bfd464440b4c770f7da0f2dd96`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` (modify). `+` lines 43 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 104/104 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `SIDEEFFECTS` → red exactly ['RED KS-1229 R1 - a refused issue with holderEmail sends noth', 'RED KS-1229 R1 - a refused issue with holderEmail sends noth', 'RED KS-1229 R1 - a refused issue with holderEmail sends noth', 'RED KS-1229 R2 - a refused issue submits no anchoring job', 'RED KS-1229 R2 - a refused issue submits no anchoring job', 'RED KS-1229 R2 - a refused issue submits no anchoring job']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night6/input.json`. Brief: `night/briefs/KS-1229-SIDEEFFECTS-R16B.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night6/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -276,3 +276,46 @@
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
```
