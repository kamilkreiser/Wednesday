# READY — KS-1229 Q-SIGNWALLET-AFTER-VERIFY (TEST-ONLY, jest, originate: the label refusal precedes the wallet-signature check)
# FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — INSERT the block after line 120 (the `beforeEach(...)` one-liner), before the blank line 121. Hunk `@@ -118,6 +118,26 @@`, strict apply, no fuzzy.
# VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night7). A2 strict; A3c 19/19; A4 1 failed / 87 — the declared cell AV1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
# Source read by Wednesday: the model's 20 `+` lines IDENTICAL in sequence to the brief fence (a mutated copy unequal), including the `finally` restore line; its three context lines equal tip 118-120 exactly.
# HOW THE RED IS PROVEN: tamper at documents.ts:2859 (LINE-PINNED; the same guard text sits at :1980 and :2590) replaces the guard line with TWO statements — an early CIP-8 check that returns INVALID_WALLET_SIGNATURE, then the original guard line unchanged. The cell makes the suite's shared `verifyMessageSignature` stub return false for its own duration and restores it in `finally`.
# ⚠ READ BEFORE MOVING IT: the block sits ABOVE the declarations it uses (`write`, `seed`, `ISSUER`, `SOURCE_ID`). That is deliberate and measured — `write`/`seed` are hoisted function declarations and the consts are read only inside `it` bodies. A5 87/87 at the tip is the proof; do not "fix" it by relocating the block.
# THE RESTORE is proven only INDIRECTLY (A5 87/87 in-file and A6 743 suite-wide, so no later cell inherited a false signature) — there is no separate assertion for it.
# PR NOTES: Refs KS-1229 (NOT Closes: this is the row Q-SIGNWALLET-AFTER-VERIFY only). TIER 2 (test-only). Behaviour change: none.
# RAISE WITH the five siblings as ONE PR — this one (118-123) · VERSIONTRIM (145-150) · SIGNWALLET (174-179) · LOOSE (179-184) · RECHECK (204-209) · SIGNCERT (EOF). Apply lowest-line-first; later hunks take their offsets.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -118,6 +118,26 @@ afterAll(() => {
   server?.close(); stub?.close();
 });
 beforeEach(() => { store.clear(); saved.length = 0; mockSaveCertification.mockClear(); });
+
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
 
 
 const SOURCE_ID = 'doc-src-1213';
```
