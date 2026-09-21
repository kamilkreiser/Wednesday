# KS-1229 R16B-LOOSE - re-brief of the STALE READY at develop 3916eacd1 (written 08:48:41 AEST on 2026-09-22 by Wednesday's feed7 drafter from the file at the tip - 309 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`
Tip: `3916eacd12af23bfd464440b4c770f7da0f2dd96`
Runner: `jest`

## Premises (measured by the feed7 drafter in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1229-LOOSE_ornith35b-q4_TESTONLY-JEST-NONSTRING-CARRIER-ROWS-PASS-7of7_2026-09-18.diff.md` (Ornith PASS 7/7 at tip 34cdcfb26; the census18 row reads `corrupt patch at line 11` because the model wrote an escaped double quote into a CONTEXT line - the fence's + lines are the model's, verbatim). The run dir is gone (`work/embeds/d0349162cbf5.diff` absent); the READY fence is the patch.
- The old READY's 2 `+` lines at the tip: ABSENT (whole-line match 0 of 2; the issue `it.each` at :252-:255 carries exactly the three tip rows, no non-string row). Content absent - un-merged.
- The test file at the tip: EXISTS (309 lines) - MODIFY IN PLACE. Mode: **MODIFY**. The issue table opener `  it.each([` (2-space indent) is at :252 only (the writers table at :222 is 4-space indented).
- Tamper source: the old brief `night/briefs/split_1229loose/KS-1229.md` (its `## Tamper` line/from/to, converted to the `### ID` shape). The one-line From occurs EXACTLY ONCE in `routes/certifications.ts` at the tip (`grep -c -F` = 1, at :201, the file 1426 lines).
- Ticket KS-1229: In Progress (started), not archived (board read at drafting time). File ownership: `services/originate/` is Seat B 18th's directory, but this test file and `routes/certifications.ts` are NOT on Seat B 18th's GROUPING list (its originate files: ks1058 / ks1103 / ks549 tests and `routes/documents.ts`) - a test-only pin in a file that is not theirs.
- Sibling pins already AT the tip in this file (do not repeat them): X-SIGNCERT-AFTER-UPSTREAM (:117), Q-SIGNWALLET-AFTER-VERIFY (:148), X-VERSION-TRIM (:171), X-SIGNWALLET-SERVED (:201), Q-SIGNCERT-UNTYPED-SOURCE-SKIP (:298). This brief adds ONLY the X-ISSUE-LOOSE rows.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these rows once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1229 X-ISSUE-LOOSE (TEST-ONLY, jest, originate: two rows in the ks1213 issue it.each pin that a NON-STRING data.documentType is refused)
> # FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — insert the two `+` rows directly under `  it.each([` (tip line 181), i.e. as the FIRST two rows of the issue table.
> # PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-ISSUE-LOOSE only). TIER 2 (test-only). Under the tamper (`:201` `!== undefined` -> `typeof === 'string'`) exactly these two rows x3 principals go red by assertion; 91/91 green at the untouched tip.
`POST /api/certifications/issue` with `parentDocumentId` refuses a `data.documentType` that differs from the certification type at `routes/certifications.ts:201` with the comparison `derivedDataDocumentType !== undefined && derivedDataDocumentType !== (type || 'verification_certificate')` - a NON-STRING carrier (the number 7, an object) is unequal to the string type, so it is refused 400 BAD_REQUEST. The three issue rows at the tip carry string carriers only; loosening the guard to `typeof derivedDataDocumentType === 'string'` would accept every non-string carrier and keep the whole file green. This task asks for the SAME two rows, re-derived at develop `3916eacd1`, as the FIRST two rows of the issue table (:252). Nothing in the product changes.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the ONE hunk below (context lines byte-for-byte from the tip; no blank context line; no blank + line; the insertion ends with a context line). No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`. The two new rows use the SAME tuple shape as the three rows below them (`[label, body]`), single quotes only.

## The exact change
```
@@ -252,2 +252,4 @@
   it.each([
+    ['a non-string number carrier (type DOCUMENT, data.documentType 7)', { type: 'DOCUMENT', data: { title: 'c', documentType: 7 } }], // KS-1229 X-ISSUE-LOOSE
+    ['an object carrier (type DOCUMENT, data.documentType an object)', { type: 'DOCUMENT', data: { title: 'c', documentType: { name: 'DOCUMENT' } } }], // KS-1229 X-ISSUE-LOOSE
     ['type DOCUMENT, data.documentType PROPERTY_DEED', { type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' } }],
```

## Cells (every cell RED or CONTROL; the names below are the EXACT rendered it.each titles - `RED %s: refused 400, no certification and no derived document written` with the row label substituted; each renders once per principal of the enclosing describe.each, three cells per name)
- `RED a non-string number carrier (type DOCUMENT, data.documentType 7): refused 400, no certification and no derived document written`
- `RED an object carrier (type DOCUMENT, data.documentType an object): refused 400, no certification and no derived document written`
- `control - data.documentType equal to the certification type is written and served as that type`  (CONTROL - an existing cell at :263, green on both trees)

## Tampers
### LOOSE
File: `Blockchain/Dev/services/originate/src/routes/certifications.ts`
Line: 201
From:
```
      if (req.body.parentDocumentId && derivedDataDocumentType !== undefined && derivedDataDocumentType !== (type || 'verification_certificate')) {
```
To:
```
      if (req.body.parentDocumentId && typeof derivedDataDocumentType === 'string' && derivedDataDocumentType !== (type || 'verification_certificate')) { // TAMPER: KS-1229 X-ISSUE-LOOSE red-proof, the gate's loosening - a non-string data.documentType is no longer refused
```
Reds: `RED a non-string number carrier (type DOCUMENT, data.documentType 7): refused 400, no certification and no derived document written`, `RED an object carrier (type DOCUMENT, data.documentType an object): refused 400, no certification and no derived document written`
(From located at the tip: 1 match, :201; statement_ok: the From line opens `if (...) {` whose body is :202 - `return res.status(400).json({ ... BAD_REQUEST ... })` - and whose block closes at :203; the tamper changes ONE operand, so every string carrier behaves exactly as at the tip and only a non-string carrier changes from refused 400 to accepted 201; `derivedDataDocumentType` is `unknown`, so the `typeof` guard compiles.)

## Controls
- `control - data.documentType equal to the certification type is written and served as that type`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`); the hunk header exactly `@@ -252,2 +252,4 @@`; no `$` / `\u` / backslash / double-quote character in a `+` line; the row labels EXACTLY as listed (the checker matches the full rendered title).
