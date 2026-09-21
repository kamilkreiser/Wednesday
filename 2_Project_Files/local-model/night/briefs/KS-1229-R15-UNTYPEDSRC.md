# KS-1229 R15-UNTYPEDSRC - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 226 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `jest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1229-UNTYPEDSRC_ornith35b-q4_TESTONLY-JEST-UNTYPED-SOURCE-STILL-REFUSED-PASS-7of7_2026-09-18.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 1348 B sha256[:16] `e563fc385ec414cc`, +13/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` at the tip: EXISTS (226 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/KS-1229.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1229: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1229.md.
- Generator notes: dropped 1 blank + line(s) (a blank + is refused in a modify fence).

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP (TEST-ONLY, jest, originate: a new top-level describe pins that /sign-cert still refuses a relabel when the source row has NO type — red under a line-pinned tamper at documents.ts:2590)
> # VERDICT: Ornith r2 RESULT: PASS (7/7), apply_mode=STRICT. r1 FAILED A4 (a BRIEF defect, not the model: the fence's leading context contained a BLANK line, the model substituted non-blank context, header and context disagreed, the harness reanchored one line early and the block landed inside the issue describe — 3 existing controls red). The ONE rebrief under Kam's counter (email 2026-09-16 07:57Z) was spent on it and PASSED.
> # Source read by Wednesday: the model's 13 `+` lines are IDENTICAL IN SEQUENCE to the brief fence, verified with a working mutated control (every single-character mutation of every non-blank line compares unequal — the first control written was a no-op on a line that did not contain the needle, and was re-run).
> # Checker detail: A2 strict; A3 touched set = the ks1213 test only; A3c 12/12, A3d clean; A4 under the tamper 1 failed / 87 — exactly the declared cell `RED KS-1229 U1`, by assertion, controls green; A5 87/87; A6 originate 741 -> 743, 0 new red; A7 tsc rc 0.
> # PLACEMENT: hunk at 209-211 (trailing, all-non-blank context). Disjoint from all six KS-1229 rows held earlier today (118-123, 145-150, 174-179, 179-184, 204-206, EOF 224-226) — all SEVEN can raise as ONE PR.
> # PR NOTES: Refs KS-1229 (NOT Closes — this is the ticket's Q-SIGNCERT-UNTYPED-SOURCE-SKIP row). TIER 2 (test-only). Behaviour change: none. In-memory only: `fromDbRow` gives `type = document_type || 'document'`, so an untyped source is unreachable through Postgres — this pins the handler's own guard. Written from develop 34cdcfb26; re-read the ks1213 test and documents.ts at raise.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`.

## The exact change
```
@@ -209,3 +209,15 @@
+describe('KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP - the sign-cert guard still refuses when the source has no type', () => {
+  const signCert = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-cert', { metadata });
+  it('RED KS-1229 U1 - an untyped source is refused a relabel, nothing saved', async () => {
+    // KS-1229 (Q-SIGNCERT-UNTYPED-SOURCE-SKIP): an untyped in-memory source must not skip the guard.
+    seed(undefined as unknown as string);
+    expect(await signCert({ documentType: 'DEGREE' })).toEqual(REFUSED);
+  }); // KS-1229 U1
+  it('control - KS-1229 a typed source is still refused a differing relabel', async () => {
+    seed('DOCUMENT');
+    expect(await signCert({ documentType: 'PROPERTY_DEED' })).toEqual(REFUSED);
+  }); // KS-1229 U control
+});
 describe('KS-1202 create guard - the properties its gate left unpinned (#1024 N-B)', () => {
   const create = async (b: Record<string, unknown>) => {
     const r = await write(ISSUER, '/api/documents', b);
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1229 U1 - an untyped source is refused a relabel, nothing saved`
- `control - KS-1229 a typed source is still refused a differing relabel`  (CONTROL - green on both trees)

## Tampers
### UNTYPEDSRC
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
Reds: `RED KS-1229 U1 - an untyped source is refused a relabel, nothing saved`
(From located at the tip: 1 match(es); the old brief/input said line 201)

## Controls
- `control - KS-1229 a typed source is still refused a differing relabel`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
