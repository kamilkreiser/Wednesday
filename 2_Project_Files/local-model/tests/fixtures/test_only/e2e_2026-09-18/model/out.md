```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts
@@ -506,12 +506,17 @@ describe('KS-679 — the E7 benign-shape widening is pinned (the seven-case control)', () => {
     ['uuidV1', 'anchor_3f2b1c9e-7d4a-1b6c-8e1f-2a3b4c5d6e7f', true],
     ['uuidNil', 'anchor_00000000-0000-0000-0000-000000000000', true],
     ['variant7', 'anchor_3f2b1c9e-7d4a-4b6c-7e1f-2a3b4c5d6e7f', true],
+    // KS-1254: the variant nibble is lower-case only. Only the nibble differs from V4.
+    ['variantLowerA', 'anchor_3f2b1c9e-7d4a-4b6c-ae1f-2a3b4c5d6e7f', false],
+    ['variantUpperA', 'anchor_3f2b1c9e-7d4a-4b6c-Ae1f-2a3b4c5d6e7f', true],
     ['hexRun36', 'anchor_0123456789abcdef-0123456789abcdef-ab', true],
     ['noSeparator', `abcd${V4}`, true],
     ['twoSegments', `evt_test_${V4}`, true],
     ['digitPrefix', `k8s_${V4}`, true],
     ['trailingJunk', `req_${V4}SECRETSUFFIX`, true],
     ['batchForm', `anchor_${V4}_0`, true],
+    // KS-1254: `cred` is refused as an exact prefix only (denycred below), so credit_ stays benign.
+    ['credit', `credit_${V4}`, false],
   ];
```
