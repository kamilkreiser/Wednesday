# KS-1229 R16B-SIDEEFFECTS - re-brief of the STALE READY at develop 3916eacd1 (written 08:51:24 AEST on 2026-09-22 by Wednesday's feed7 drafter from the file at the tip - 309 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`
Tip: `3916eacd12af23bfd464440b4c770f7da0f2dd96`
Runner: `jest`

## Premises (measured by the feed7 drafter in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1229_ornith35b-q4_TESTONLY-JEST-REFUSAL-SIDEEFFECTS-PASS-7of7-RECHECK_2026-09-18.diff.md` (Ornith PASS 7/7 by harness re-check at tip 3961c2add / 34cdcfb26; the census18 row reads `No valid patches in input` because the READY fence carries NO `---`/`+++` header and no `@@` line - the 43 `+` lines below are that fence's, verbatim, count asserted 43). The run dir is gone (`work/embeds/b7769c8bc9d8.diff` absent); the READY fence is the patch.
- The old READY's `+` lines at the tip: ABSENT (no `KS-1229 R1` / `KS-1229 R2` cell in the file; the issue describe.each at :249-:278 ends with the `without parentDocumentId` control at :273-:277). Content absent - un-merged.
- The test file at the tip: EXISTS (309 lines) - MODIFY IN PLACE. Mode: **MODIFY**. The block is inserted after :277 (`  });`, the close of the last control) and before :278 (`});`, the close of the issue describe.each), so it is the LAST member of that describe.each - the placement the old READY had (its context `describe('KS-1202 create guard ...` is :280 at the tip; the blank :279 is not a context line, a blank context line being refused in a modify fence).
- Tamper source: the old brief `night/briefs/KS-1229.md` (its `## Tamper` line/from/to, converted to the `### ID` shape). The one-line From occurs EXACTLY ONCE in `routes/certifications.ts` at the tip (`grep -c -F` = 1, at :201, the file 1426 lines; :202 is the `return res.status(400)` body, :203 closes the block).
- Ticket KS-1229: In Progress (started), not archived (board read at drafting time). File ownership: `services/originate/` is Seat B 18th's directory, but this test file and `routes/certifications.ts` are NOT on Seat B 18th's GROUPING list (its originate files: ks1058 / ks1103 / ks549 tests and `routes/documents.ts`) - a test-only pin in a file that is not theirs.
- Sibling: `KS-1229-R16B-LOOSE.md` (this feed) inserts two rows at :252 of the SAME file; the two hunks do not overlap (:252-:253 vs :276-:278). Queue them as separate rows; whichever lands second takes a +2 / +43 offset at the raise (the model is told nothing of the other).
- The names the block reads are all declared ABOVE it at the tip: `seed` (:98), `stub` (:106, the loopback express listener whose port is `process.env.AUTH_SERVICE_URL` from :112), `issue` (:250, the describe-local helper), `SOURCE_ID`, `mockSaveCertification` (:43). Nothing is imported.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1229 (TEST-ONLY, jest, originate: three cells in the ks1213 issue describe.each pin that a REFUSED derived issue sends nothing upstream — R1 no /api/users/stub call, R2 no anchoring job, plus a control that sees both calls; red under the tamper at routes/certifications.ts:201)
> # PR NOTES: Refs KS-1229 (NOT Closes: only rows X-ISSUE-AFTER-HOLDER + X-ISSUE-AFTER-ANCHOR are pinned). TIER 2 (test-only). R2 and the control set and delete ANCHORING_SERVICE_URL in finally (unset today).
`POST /api/certifications/issue` with `parentDocumentId` refuses a `data.documentType` that differs from the certification type (`routes/certifications.ts:201`, 400 BAD_REQUEST) BEFORE two external side effects: the holder stub (`:242`, `POST <AUTH_SERVICE_URL>/api/users/stub`, sent when the body carries `holderEmail`) and the anchoring submit (`:411`, `POST <ANCHORING_SERVICE_URL>/api/anchors`). The runtime is correct at the tip, but the issue cells read only the status, the code and the saved rows, so moving the guard below either call keeps the whole file green. This task asks for the SAME three cells, re-derived at develop `3916eacd1`, as the last members of the issue describe.each. Nothing in the product changes.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the ONE hunk below (context lines byte-for-byte from the tip; no blank context line; no blank + line; the insertion ends with a context line). No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`. Keep the indentation of the fence exactly (2 spaces for the `it(` lines and their closing `});`, 4 inside each `it(`, 6 inside `try` / `finally`).

## The exact change
```
@@ -276,3 +276,46 @@
     expect(mockSaveCertification).toHaveBeenCalledTimes(1);
   });
+  it('RED KS-1229 R1 - a refused issue with holderEmail sends nothing to the users/stub upstream', async () => {
+    // KS-1229 (X-ISSUE-AFTER-HOLDER): users/stub mints or resolves an INVITED user in auth, so the refusal must come first.
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    try {
+      const r = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' }, holderEmail: 'holder-ks1229@example.test', parentDocumentId: SOURCE_ID });
+      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
+    } finally {
+      stub.off('request', onUpstream);
+    }
+  }); // KS-1229 R1
+  it('RED KS-1229 R2 - a refused issue submits no anchoring job', async () => {
+    // KS-1229 (X-ISSUE-AFTER-ANCHOR): the anchoring base points at the loopback stub for this cell only.
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    process.env.ANCHORING_SERVICE_URL = process.env.AUTH_SERVICE_URL;
+    try {
+      const r = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' }, parentDocumentId: SOURCE_ID });
+      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
+    } finally {
+      stub.off('request', onUpstream);
+      delete process.env.ANCHORING_SERVICE_URL;
+    }
+  }); // KS-1229 R2
+  it('control - KS-1229 an accepted issue reaches /api/anchors and a holderEmail issue reaches /api/users/stub on the loopback stub', async () => {
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    process.env.ANCHORING_SERVICE_URL = process.env.AUTH_SERVICE_URL;
+    try {
+      const accepted = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'DOCUMENT' }, parentDocumentId: SOURCE_ID });
+      const invited = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'DOCUMENT' }, holderEmail: 'holder-ks1229@example.test', parentDocumentId: SOURCE_ID });
+      expect([accepted.status, invited.status, upstreamUrls]).toEqual([201, 404, ['/api/anchors', '/api/users/stub']]);
+    } finally {
+      stub.off('request', onUpstream);
+      delete process.env.ANCHORING_SERVICE_URL;
+    }
+  }); // KS-1229 control
 });
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles; each renders once per principal of the enclosing describe.each, three cells per name)
- `RED KS-1229 R1 - a refused issue with holderEmail sends nothing to the users/stub upstream`
- `RED KS-1229 R2 - a refused issue submits no anchoring job`
- `control - KS-1229 an accepted issue reaches /api/anchors and a holderEmail issue reaches /api/users/stub on the loopback stub`  (CONTROL - green on both trees)

## Tampers
### SIDEEFFECTS
File: `Blockchain/Dev/services/originate/src/routes/certifications.ts`
Line: 201
From:
```
      if (req.body.parentDocumentId && derivedDataDocumentType !== undefined && derivedDataDocumentType !== (type || 'verification_certificate')) {
```
To:
```
      if (req.body.parentDocumentId && derivedDataDocumentType !== undefined && derivedDataDocumentType !== (type || 'verification_certificate') && (await Promise.all([req.body.holderEmail ? fetch((process.env.AUTH_SERVICE_URL || 'http://localhost:6003') + '/api/users/stub', { method: 'POST' }).catch(() => null) : null, fetch((process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005') + '/api/anchors', { method: 'POST' }).catch(() => null)]).then(() => true))) { // TAMPER: KS-1229 red-proof, the refusal is decided only after the holder stub and the anchoring submit were sent (the gate rows X-ISSUE-AFTER-HOLDER and X-ISSUE-AFTER-ANCHOR, in one line)
```
Reds: `RED KS-1229 R1 - a refused issue with holderEmail sends nothing to the users/stub upstream`, `RED KS-1229 R2 - a refused issue submits no anchoring job`
(From located at the tip: 1 match, :201; statement_ok: the From line opens `if (...) {` whose body is :202 - `return res.status(400).json({ ... BAD_REQUEST ... })` - and whose block closes at :203; the tamper keeps the three original conditions first, so `&&` short-circuits on every accepted request and the added holder-stub + anchoring calls run ONLY on a request the guard refuses; `.catch(() => null)` swallows a refused connection and `.then(() => true)` keeps the operand true, so every refused request still answers 400 BAD_REQUEST and R1 / R2 fail at `.toEqual` on the upstream list; the handler is `async` (it awaits at :242), so `await` compiles there. The control's bodies carry an EQUAL type, so the guard - tampered or not - is false and never calls anything.)

## Controls
- `control - KS-1229 an accepted issue reaches /api/anchors and a holderEmail issue reaches /api/users/stub on the loopback stub`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`); the hunk header exactly `@@ -276,3 +276,46 @@`; no dollar sign / backslash / backtick / double-quote character in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
