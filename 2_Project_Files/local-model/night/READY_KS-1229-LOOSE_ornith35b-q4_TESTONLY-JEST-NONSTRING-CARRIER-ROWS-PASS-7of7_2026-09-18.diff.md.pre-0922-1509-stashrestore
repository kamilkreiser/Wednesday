# READY — KS-1229 X-ISSUE-LOOSE (TEST-ONLY, jest, originate: two rows in the ks1213 issue it.each pin that a NON-STRING data.documentType is refused)
# FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — insert the two `+` rows directly under `  it.each([` (tip line 181), i.e. as the FIRST two rows of the issue table (applied lines 182-183 at tip 34cdcfb26).
# VERDICT: Ornith round 2 PASS 7/7 first sample (run 2026-09-18_ks1229-ornith35b-night3). Round 1 (rows appended after :184) FAILED A3c twice — a BRIEF defect (look-alike context rows), rebriefed once under Kam's counter; no rounds left.
# Source read by Wednesday: the model's 2 `+` lines IDENTICAL in sequence to the brief fence (a one-character mutated copy unequal); placement re-derived independently (-C1 anchor unique at tip line 181, rows land 182-183, directly under the table opener).
# ⚠ MODEL DIALECT, harmless here but read before applying: the model dropped one upper context line AND wrote `\"` (an escaped double quote) in the `["type certificate…` CONTEXT line, so strict apply fails and the checker applied with -C1. Context lines are matched, never written, so the file's own line is untouched — verified: no backslash-escaped quote exists in the applied file. APPLY WITH `-C1`, or re-type the hunk headers by hand.
# PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-ISSUE-LOOSE only). TIER 2 (test-only). originate 741 -> 747, no new red; tsc rc 0. Under the tamper (`:201` `!== undefined` -> `typeof === 'string'`) exactly these two rows x3 principals go red by assertion (6 / 91); 91/91 green at the untouched tip.
# RAISE WITH its sibling READY_KS-1229_…-RECHECK (hunks 182-187 vs 204-209 at the tip do NOT overlap) as ONE PR: `Refs KS-1229 (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR, X-ISSUE-LOOSE)`. Apply this one FIRST (the other's anchor then shifts by +2) or apply with offset.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -179,6 +179,8 @@ describe.each(PRINCIPALS)('KS-1213 POST /api/certifications/issue with parentDoc
 
   it.each([
+    ['a non-string number carrier (type DOCUMENT, data.documentType 7)', { type: 'DOCUMENT', data: { title: 'c', documentType: 7 } }], // KS-1229 X-ISSUE-LOOSE
+    ['an object carrier (type DOCUMENT, data.documentType an object)', { type: 'DOCUMENT', data: { title: 'c', documentType: { name: 'DOCUMENT' } } }], // KS-1229 X-ISSUE-LOOSE
     ['type DOCUMENT, data.documentType PROPERTY_DEED', { type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' } }],
     [\"type certificate, data.documentType DOCUMENT (the parent's type)\", { type: 'certificate', data: { title: 'c', documentType: 'DOCUMENT' } }],
     ['a case variant (type DOCUMENT, data.documentType document)', { type: 'DOCUMENT', data: { title: 'c', documentType: 'document' } }],
```
