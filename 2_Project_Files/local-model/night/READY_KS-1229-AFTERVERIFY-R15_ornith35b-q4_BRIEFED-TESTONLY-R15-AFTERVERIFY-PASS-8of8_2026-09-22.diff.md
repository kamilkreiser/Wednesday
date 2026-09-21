# READY — KS-1229-AFTERVERIFY-R15 (Ornith, briefed, test_only, modify · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1229AFTERVERIFY-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 19/19 in the diff; reds matched 1/1; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 19/19 in the diff; reds matched 1/1; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` (modify). `+` lines 19 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 87/87 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `AFTERVERIFY` → red exactly ['RED KS-1229 AV1 - a mislabelled request with a bad signature']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night/input.json`. Brief: `night/briefs/KS-1229-AFTERVERIFY-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -118,3 +118,22 @@
   server?.close(); stub?.close();
 });
+describe('KS-1229 Q-SIGNWALLET-AFTER-VERIFY - the label refusal comes BEFORE the wallet signature check', () => {
+  it('RED KS-1229 AV1 - a mislabelled request with a bad signature is refused BAD_REQUEST, not INVALID_WALLET_SIGNATURE', async () => {
+    // KS-1229 (Q-SIGNWALLET-AFTER-VERIFY): the cheap, caller-fixable refusal must precede the CIP-8 check.
+    const shared = jest.requireMock('@secuura/shared') as { verifyMessageSignature: jest.Mock };
+    seed('DOCUMENT');
+    shared.verifyMessageSignature.mockImplementation(() => false);
+    try {
+      const r = await write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata: { documentType: 'PROPERTY_DEED' } });
+      expect([r.status, r.code, r.saved]).toEqual([400, 'BAD_REQUEST', 0]);
+    } finally {
+      shared.verifyMessageSignature.mockImplementation(() => true);
+    }
+  }); // KS-1229 AV1
+  it('control - KS-1229 the same mislabelled request with a good signature is refused BAD_REQUEST', async () => {
+    seed('DOCUMENT');
+    const r = await write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata: { documentType: 'PROPERTY_DEED' } });
+    expect([r.status, r.code, r.saved]).toEqual([400, 'BAD_REQUEST', 0]);
+  }); // KS-1229 AV control
+});
 beforeEach(() => { store.clear(); saved.length = 0; mockSaveCertification.mockClear(); });
```
