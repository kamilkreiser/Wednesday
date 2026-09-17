# READY — KS-1237 Q-ARRAYLIKE-OPEN (TEST-ONLY, VITEST, api-gateway: a new cell pins that an ARRAY-LIKE allow-list `{ 0: 'SSD_DOCUMENT', length: 1 }` is still "not a list" — 403 for a named type and an untyped body — plus its COMPLETENESS registration)
# VERDICT: Ornith r1 RESULT: PASS (7/7) on the FIRST sample, no rebrief spent. A4 under the tamper 1 failed / 10 — exactly the declared cell `RED KS-1237 AL1`, by assertion; every control green INCLUDING `KS-1204 COMPLETENESS`. A5 10/10. A6 api-gateway 565 -> 566, 0 new red. A7 tsc rc 0.
# Source read by Wednesday: the model's 9 `+` lines are IDENTICAL IN SEQUENCE to the brief fence, verified with a mutated control that discriminates on every non-blank line.
# ⚠ APPLY MODE: the MODEL's diff applied `lenient` (its hunk header count needed --recount). **The fence below is the BRIEF's, which applies STRICT** — raise from this, not from the model's header. Same `+` lines either way.
# TWO HUNKS, and the second is load-bearing: `KS-1204 COMPLETENESS` (`:285-292`) asserts `[...RAN].sort()` EQUALS an eight-entry list, so a cell that calls `RAN.add` without being listed turns that EXISTING control red. Hunk 2 adds the entry.
# TAMPER (checker-only, not shipped): verification.ts:1226, deliberately NARROW — an OBJECT with a numeric `length` only. A tamper keyed on `.length` alone would also catch the two STRING cells and red them, which is why it is not written that way.
# PR NOTES: Refs KS-1237 (NOT Closes — this is one of the ticket's three rows; X-MSG-MEMBER and X-INFO-ALWAYS-EMPTY remain). TIER 2 (test-only). Behaviour change: none. Written from develop 34cdcfb26 — re-read the ks1204 test and verification.ts at raise.
# HARNESS NOTE: getting here found and fixed a real defect — `decl_splice.py` corrupted this diff (it is a NEW-FILE tool; it spliced a duplicate declaration into hunk 1 and recounted nothing). Fixed with a scope guard + arms; see IMPROVEMENTS 07:1x. Without that fix the model would have failed the same way and the ticket would have gone to a Claude seat for a harness bug.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts
@@ -243,3 +243,11 @@
+  it('RED KS-1237 AL1 - an array-like allow-list is not a list: 403 FORBIDDEN for a named type and an untyped body', async () => {
+    RAN.add('non-array an array-like');
+    connectorAllowedTypes = { 0: 'SSD_DOCUMENT', length: 1 };
+    const named = await createDocumentWithBody(CONNECTOR, { documentType: 'DOCUMENT' });
+    const untyped = await createDocumentWithBody(CONNECTOR, {});
+    expect([named.status, named.body?.error?.code, untyped.status, untyped.body?.error?.code]).toEqual([403, 'FORBIDDEN', 403, 'FORBIDDEN']);
+  }); // KS-1237 AL1
+
   it('control: an ARRAY allow-list ["SSD_DOCUMENT"] admits SSD_DOCUMENT and refuses DOCUMENT, as before', async () => {
     RAN.add('array control');
     connectorAllowedTypes = ['SSD_DOCUMENT'];
@@ -287,5 +287,5 @@
     expect([...RAN].sort()).toEqual([
       'string vs DOCUMENT', 'non-array the string "SSD_DOCUMENT"', 'non-array an object', 'non-array an empty string',
-      'array control', 'unrestricted control', 'precedence admits documentType', 'precedence refuses documentType',
+      'array control', 'unrestricted control', 'precedence admits documentType', 'precedence refuses documentType', 'non-array an array-like',
     ].sort());
   });
```
