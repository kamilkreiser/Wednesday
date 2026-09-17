# READY — KS-1220 (test-only, auth ks839 test — one new cell pinning five Unicode separators around the `*` wildcard, completeness count 6 -> 7)
# Source read by Wednesday 22:13: the model's RETRY 16 +/- lines (+15/-1) IDENTICAL to the brief's fences (python sequence compare; a mutated copy unequal). First sample FAILED A3c (no section for the brief's additions); RETRY-ONCE PASS (7/7), apply_mode=REANCHORED. A6 whole auth suite no new red; A7 tsc rc 0. Tip = develop 75ad0e55c.
# PR NOTES: `Closes KS-1220` defensible once merged (confirm at raise); KS-839 stays In Progress (§5f). TIER 2. Re-derive hunk headers at raise (reanchored apply). The pin covers 5 of the gate's 26 separators — stated in the brief, not in scope. Run: runs/2026-09-17_ks1220-ornith35b-night/retry/out.md.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts
@@ -25,7 +25,7 @@ vi.mock('../utils/logger', () => ({
 
 import { validateScopes, parseScopeString } from '../services/oauth';
 
-const EXPECTED_CELLS = 6;
+const EXPECTED_CELLS = 7;
 let CELLS_RUN = 0;
 const WILDCARD_APP = ['*'];
 const MIXED_APP = ['documents:read', '*'];
@@ -82,6 +82,20 @@ describe('KS-839 - an allow-list holding the wildcard grants nothing', () => {
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
