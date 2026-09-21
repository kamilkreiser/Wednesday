# READY — KS-1229-SIGNCERT-R15 (Ornith, briefed, test_only, modify · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1229SIGNCERT-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 28/28 in the diff; reds matched 1/1; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 28/28 in the diff; reds matched 1/1; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night2/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` (modify). `+` lines 28 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 87/87 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `SIGNCERT` → red exactly ['RED KS-1229 SC1 - a refused sign-cert sends nothing to the i']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1229-SIGNCERT-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -115,3 +115,31 @@
   const s = stub.address(); process.env.AUTH_SERVICE_URL = 'http://127.0.0.1:' + String(typeof s === 'object' && s ? s.port : 0);
 });
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
 afterAll(() => {
```
