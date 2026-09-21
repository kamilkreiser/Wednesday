# KS-1265 R16-EARLYGUARD - Wednesday's task for Ornith: the "@"-issuerName refusal moves BEFORE the save (code_patch, jest, MODIFY THE EXISTING TEST IN PLACE) at develop 64ab10513 (written 02:03 on 2026-09-22 by Wednesday's feed3 drafter from services/originate/src/routes/documents.ts:555-870 read whole and ks549-documents-create-issuer-name-persist.test.ts, 163 lines read whole)
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `jest`

## Premises (measured by the feed3 drafter at 02:03:44 AEST, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- Ticket KS-1265 (P3, Backlog, kamil.kreiser@secuura.ai, no PR attachment): "Move the issuerName check above the save, so a refused create writes nothing. Regression cell: issuerName 'someone@example.com' gives 400, 0 documents saved and 0 provenance rows." The ticket's line numbers (:845-851 / :699 at 52df64f84) are :836-841 / :687 at 64ab10513.
- At the tip the create handler ALREADY computes `topLevelIssuerName` at :612-613 (`typeof req.body?.issuerName === 'string' ? req.body.issuerName.trim() : ''`), 74 lines BEFORE `const saved = await saveDocument(...)` at :687; the E-01 guard `if (suppliedIssuerName.includes('@'))` sits at :836-841 in the anchoring scope, AFTER the save and the provenance write. So the fix is ONE insertion at :614: the same refusal on `topLevelIssuerName`, before anything is written.
- The late guard at :836-841 is LEFT IN PLACE (it becomes unreachable for an "@" value and stays the anchoring-scope backstop). Drafter's reason: its message line :839 carries a non-ASCII em dash, and a `-` line the model must reproduce byte for byte with a non-ASCII character is the KS-1133 / KS-1180 escape class; the ticket's outcome ("a refused create writes nothing") is met by the early guard alone. Wednesday may veto this shape.
- The regression cell: `ks549-documents-create-issuer-name-persist.test.ts` already drives `POST /api/documents` in-process (express + `documentsRouter`, `saveDocument` mocked as `mockSaveDocument`, SIMULATE_ANCHORING=true) and its third cell (:137-151) sends exactly `issuerName: 'someone@example.com'` and accepts `[201, 400]` with the save unasserted. The test hunk tightens that cell's BODY (:144-150) to `400` and `saveDocument` called 0 times; its title (:137) stays and is declared under `## Red cells`. At the tip the route answers 400 AFTER calling saveDocument once (the guard at :836 runs before the `if (simulateAnchoring)` branch at :861), so the tightened cell is RED at the tip by assertion (`toHaveBeenCalledTimes(0)` sees 1) and GREEN after E1. Provenance rows: `recordActionProvenance` at :711 runs only `if (onBehalfOf)` and this cell sends none, so "0 provenance rows" holds by construction on both trees; it is not asserted separately.
- Both fences are ASCII-only and backslash-free in every `+` line; no blank context line; the product insertion ends with trailing context (:614-616, all non-blank).

## What is wrong (one paragraph)
`POST /api/documents` (`services/originate/src/routes/documents.ts`) saves the document at :687 (`saveDocument`), fires the platform-registry and event hops, and only THEN, at :836, refuses a supplied `issuerName` that contains "@" with 400 BAD_REQUEST. The caller is told the write failed when it happened: a retry without `documentUuid` duplicates the document and the saved draft is never anchored. The fix is the refusal BEFORE the save: the handler already has `topLevelIssuerName` at :612-613, so ONE inserted guard at :614 refuses an "@"-carrying value before anything is written. NOT in this task: the late guard at :836-841 (stays), any other route, any other file.

## The exact change — ONE INSERT-ONLY EDIT in the product file (one hunk; the 8 `+` lines FIRST, then 3 lines of TRAILING context :614-616)
E1 — `services/originate/src/routes/documents.ts`: insert 8 lines BEFORE line 614 (context: line 613 is `        typeof req.body?.issuerName === 'string' ? req.body.issuerName.trim() : '';`, line 614 is `      if (topLevelIssuerName && !topLevelIssuerName.includes('@') && !data.issuerName) {`, line 616 is `      }`). The hunk header is `@@ -614,3 +614,11 @@` - copy it:
```
@@ -614,3 +614,11 @@
+      // KS-1265: refuse an "@"-carrying issuerName BEFORE the save below (it was refused at the anchoring
+      // step, AFTER saveDocument and the provenance row) - a refused create must write nothing.
+      if (topLevelIssuerName.includes('@')) {
+        return res.status(400).json({
+          success: false,
+          error: { code: 'BAD_REQUEST', message: 'issuerName must not contain "@" - it should be the organisation name, not a user email (audit E-01)' },
+        });
+      }
       if (topLevelIssuerName && !topLevelIssuerName.includes('@') && !data.issuerName) {
         data.issuerName = topLevelIssuerName;
       }
```
The 8 `+` lines are byte-exact - copy them; six-space indent on the `if`, eight on `return`, ten inside the object. No other line of documents.ts changes.

## The test — MODIFY THE EXISTING TEST FILE IN PLACE (jest; `--- a/` / `+++ b/` headers; ONE hunk)
File: `Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts`
Its FULL content is in `files[...]` - copy context byte for byte from it. Do NOT create a new test file, do NOT use `--- /dev/null`, do NOT copy the reference test's driver. ONE hunk replaces the BODY of the third cell (:144-150) and keeps its title (:137) and its request (:138-143). The hunk header is `@@ -141,11 +141,8 @@` - copy it:
```
@@ -141,11 +141,8 @@
       issuerName: 'someone@example.com',
       data: { title: 'Doc' },
     });
-    // The route's existing E-01 guard rejects "@"-carrying issuerName in the
-    // anchor scope; whatever the status, the blob must not carry the email.
-    if (mockSaveDocument.mock.calls.length > 0) {
-      const saved = mockSaveDocument.mock.calls[0][0];
-      expect(saved.data.issuerName).toBeUndefined();
-    }
-    expect([201, 400]).toContain(res.status);
+    // KS-1265: the E-01 guard now refuses BEFORE the save. A refused create writes nothing:
+    // 400, and saveDocument is never called (at the old tip it was called once, then 400).
+    expect(res.status).toBe(400);
+    expect(mockSaveDocument).toHaveBeenCalledTimes(0);
   });
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('never persists an email-shaped issuerName (E-01 guard parity)')` - the EXISTING title, body tightened: at the tip `saveDocument` was called once before the 400 (the red, by assertion); after E1 it is called 0 times.
- CONTROL `it('stores a top-level issuerName in the saved document data blob')`, `it('does not overwrite an issuerName already present inside data')`, `it('omits issuerName entirely when the caller does not send one')` - untouched, green on both trees (no "@" in any of them, so E1 never fires).

## Red cells
- never persists an email-shaped issuerName (E-01 guard parity)

## Where (an INSERT-ONLY edit names its anchor as (correct) and has NO must-change line - A3b cannot see an insertion; 2026-09-15 KS-747)
* `:614` — (correct) `      if (topLevelIssuerName && !topLevelIssuerName.includes('@') && !data.issuerName) {` — the anchor E1 inserts before; stays
* `:687` — (correct) `      const saved = await saveDocument(document, tenantId, (req as any).db, {` — the save E1 must precede; stays
* `:836` — (correct) `      if (suppliedIssuerName.includes('@')) {` — the late guard; stays (unreachable for an "@" value after E1)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/originate/src/routes/documents.ts` / `+++ b/...` with the E1 hunk, then `--- a/Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts` / `+++ b/...` with the test hunk; the two hunk headers as written above; no `\$` / `\u` / backslash escapes in a `+` line; blank context lines keep their leading space (there are none in these two hunks).
