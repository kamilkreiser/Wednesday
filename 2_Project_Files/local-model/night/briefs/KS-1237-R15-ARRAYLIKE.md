# KS-1237 R15-ARRAYLIKE - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 292 lines read whole)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `vitest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1237-ARRAYLIKE_ornith35b-q4_TESTONLY-VITEST-ARRAYLIKE-ALLOWLIST-NOT-A-LIST-PASS-7of7_2026-09-18.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 1500 B sha256[:16] `feffa0efd9172781`, +9/-1.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts` at the tip: EXISTS (292 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/split_1237arraylike/KS-1237.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1237: Backlog, assignee UNASSIGNED, PR attachments none (all merged); briefs already on disk: none.
- Generator notes: dropped 1 blank + line(s) (a blank + is refused in a modify fence); CONTROL INFERRED: an EXISTING cell in the fence context 'control: an ARRAY allow-list ["SSD_DOCUMENT"] admits SSD_DOC' (green on both trees by construction).

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1237 Q-ARRAYLIKE-OPEN (TEST-ONLY, VITEST, api-gateway: a new cell pins that an ARRAY-LIKE allow-list `{ 0: 'SSD_DOCUMENT', length: 1 }` is still "not a list" — 403 for a named type and an untyped body — plus its COMPLETENESS registration)
> # VERDICT: Ornith r1 RESULT: PASS (7/7) on the FIRST sample, no rebrief spent. A4 under the tamper 1 failed / 10 — exactly the declared cell `RED KS-1237 AL1`, by assertion; every control green INCLUDING `KS-1204 COMPLETENESS`. A5 10/10. A6 api-gateway 565 -> 566, 0 new red. A7 tsc rc 0.
> # Source read by Wednesday: the model's 9 `+` lines are IDENTICAL IN SEQUENCE to the brief fence, verified with a mutated control that discriminates on every non-blank line.
> # ⚠ APPLY MODE: the MODEL's diff applied `lenient` (its hunk header count needed --recount). **The fence below is the BRIEF's, which applies STRICT** — raise from this, not from the model's header. Same `+` lines either way.
> # TWO HUNKS, and the second is load-bearing: `KS-1204 COMPLETENESS` (`:285-292`) asserts `[...RAN].sort()` EQUALS an eight-entry list, so a cell that calls `RAN.add` without being listed turns that EXISTING control red. Hunk 2 adds the entry.
> # TAMPER (checker-only, not shipped): verification.ts:1226, deliberately NARROW — an OBJECT with a numeric `length` only. A tamper keyed on `.length` alone would also catch the two STRING cells and red them, which is why it is not written that way.
> # PR NOTES: Refs KS-1237 (NOT Closes — this is one of the ticket's three rows; X-MSG-MEMBER and X-INFO-ALWAYS-EMPTY remain). TIER 2 (test-only). Behaviour change: none. Written from develop 34cdcfb26 — re-read the ks1204 test and verification.ts at raise.
> # HARNESS NOTE: getting here found and fixed a real defect — `decl_splice.py` corrupted this diff (it is a NEW-FILE tool; it spliced a duplicate declaration into hunk 1 and recounted nothing). Fixed with a scope guard + arms; see IMPROVEMENTS 07:1x. Without that fix the model would have failed the same way and the ticket would have gone to a Claude seat for a harness bug.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. 

## The exact change
```
@@ -243,3 +243,10 @@
+  it('RED KS-1237 AL1 - an array-like allow-list is not a list: 403 FORBIDDEN for a named type and an untyped body', async () => {
+    RAN.add('non-array an array-like');
+    connectorAllowedTypes = { 0: 'SSD_DOCUMENT', length: 1 };
+    const named = await createDocumentWithBody(CONNECTOR, { documentType: 'DOCUMENT' });
+    const untyped = await createDocumentWithBody(CONNECTOR, {});
+    expect([named.status, named.body?.error?.code, untyped.status, untyped.body?.error?.code]).toEqual([403, 'FORBIDDEN', 403, 'FORBIDDEN']);
+  }); // KS-1237 AL1
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

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1237 AL1 - an array-like allow-list is not a list: 403 FORBIDDEN for a named type and an untyped body`
- `control: an ARRAY allow-list ["SSD_DOCUMENT"] admits SSD_DOCUMENT and refuses DOCUMENT, as before`  (CONTROL - green on both trees)

## Tampers
### ARRAYLIKE
File: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`
Line: 1226
From:
```
        if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) {
```
To:
```
        if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !(Array.isArray(rawAllowedTypes) || (typeof rawAllowedTypes === 'object' && rawAllowedTypes !== null && typeof (rawAllowedTypes as { length?: unknown }).length === 'number'))) { // TAMPER: KS-1237 red-proof, an object with a numeric length counts as a list (the #1035 gate row Q-ARRAYLIKE-OPEN)
```
Reds: `RED KS-1237 AL1 - an array-like allow-list is not a list: 403 FORBIDDEN for a named type and an untyped body`
(From located at the tip: 1 match(es); the old brief/input said line 1226)

## Controls
- `control: an ARRAY allow-list ["SSD_DOCUMENT"] admits SSD_DOCUMENT and refuses DOCUMENT, as before`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
