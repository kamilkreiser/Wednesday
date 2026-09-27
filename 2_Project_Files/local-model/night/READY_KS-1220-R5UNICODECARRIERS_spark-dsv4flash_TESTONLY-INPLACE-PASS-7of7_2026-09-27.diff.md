# READY — KS-1220 (test-only, auth ks839 test: new cell R5, five non-ASCII / vertical-tab padded wildcards grant nothing; EXPECTED_CELLS 6 -> 7) — Spark deepseek-v4-flash-0731, ORIGINAL Spark round (rev 2 brief), SPARK RESULT: PASS (checker 7/7 + A2a), apply STRICT, held BY HAND 14:03 AEST 2026-09-27 by Wednesday (hold_ready.py refuses test_only mode on a code_patch input: known gap, IMPROVEMENTS)
# Source read by Wednesday: the model's 16 +/- lines are IDENTICAL, in order, to the rev-2 brief's two fences (python sequence compare over out.md vs night/briefs/KS-1220-r2/KS-1220.md); hunks @@ -28,4 +28,4 @@ and @@ -82,6 +82,20 @@ as briefed; A2a anchor 2/2 ok. Checker (tip 94c9c7aa9be7): A4 1 failed / 8 run under the oauth.ts:353 tamper (R5 by assertion, controls green); A5 8/8; A6 services/auth 835 baseline, no new red; A7 tsc rc 0. Model wall 24.48 s, 17,618 prompt / 566 completion tokens. patch.diff sha256 prefix 629ced187055f0d3. Run: runs/spark_secuura_2026-09-27_KS-1220-r2.
# PR NOTES: `Refs KS-1220`, NO closing keyword at raise (the GO moves the ticket). TIER 2 (test-only coverage pin). The parent (KS839) stays In Progress. The pin covers 5 of the 26 JS whitespace separators (brief notes). Re-derive nothing: strict at 94c9c7aa9be7.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts
@@ -28,4 +28,4 @@
-const EXPECTED_CELLS = 6;
+const EXPECTED_CELLS = 7;
 let CELLS_RUN = 0;
 const WILDCARD_APP = ['*'];
 const MIXED_APP = ['documents:read', '*'];
@@ -82,6 +82,20 @@
     expect(PADDED_CARRIERS.map(([name, allowList]) => [name, validateScopes(named, allowList)]))
       .toEqual(PADDED_CARRIERS.map(([name]) => [name, []]));
   });
+  it('KS-839 R5 - a wildcard padded with non-ASCII or vertical-tab whitespace grants nothing, scope omitted or named', () => {
+    CELLS_RUN += 1;
+    // KS-1220: each carrier is built by code point: no-break space, vertical tab, ideographic space, line separator, byte-order mark.
+    const UNICODE_CARRIERS: Array<[string, string[]]> = [
+      ['nbsp-star', [String.fromCharCode(0xa0) + '*']],
+      ['vtab-star', [String.fromCharCode(0x0b) + '*']],
+      ['ideographic-space-star', [String.fromCharCode(0x3000) + '*']],
+      ['star-line-separator', ['*' + String.fromCharCode(0x2028)]],
+      ['openid-then-bom-star', ['openid', String.fromCharCode(0xfeff) + '*']],
+    ];
+    const named = parseScopeString('openid documents:read admin:everything *');
+    expect(UNICODE_CARRIERS.map(([name, allowList]) => [name, validateScopes(allowList, allowList), mintedWithScopeOmitted(allowList), validateScopes(named, allowList)]))
+      .toEqual(UNICODE_CARRIERS.map(([name]) => [name, [], [], []]));
+  });
   it('KS-839 CONTROL 2 - look-alike stars stay literal, and explicit, empty and documents:* lists are unchanged', () => {
     CELLS_RUN += 1;
     expect([
```
