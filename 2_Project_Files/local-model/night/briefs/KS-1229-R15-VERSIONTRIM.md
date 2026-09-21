# KS-1229 R15-VERSIONTRIM - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 226 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `jest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1229-VERSIONTRIM_ornith35b-q4_TESTONLY-JEST-EXACT-NOT-TRIMMED-PASS-7of7_2026-09-18.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 1650 B sha256[:16] `7fe40223eaaa1ec5`, +13/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` at the tip: EXISTS (226 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/split_1229versiontrim/KS-1229.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1229: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1229.md.
- Generator notes: dropped 1 blank + line(s) (a blank + is refused in a modify fence); RE-ANCHORED: the old hunk appended at EOF / before a blank line; the last leading context line '];' is now the TRAILING context, so the new block lands one line UP (inside the enclosing block) - a placement change from the old READY, said here; tamper VERSIONTRIM: the one-line From occurs 3x at the tip; WIDENED to a 5-line block starting at :1993 (the occurrence nearest the old line 1980) - an INFERENCE by line proximity; Wednesday confirms the site.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1229 X-VERSION-TRIM (TEST-ONLY, jest, originate: /version compares EXACTLY, so a padded carrier is refused)
> # FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — INSERT the block after line 147 (the `];` closing the WRITERS table), before the blank line 148. Hunk `@@ -145,6 +145,19 @@`, strict apply, no fuzzy.
> # VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night6). A2 strict; A3c 12/12; A4 1 failed / 87 — the declared cell VT1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
> # Source read by Wednesday: the model's 13 `+` lines IDENTICAL in sequence to the brief fence; **the single TRAILING SPACE inside `version('DOCUMENT ')` survived** (it is the whole point of the cell, and a mutated control with the space removed is unequal); its three context lines equal tip 145-147 exactly, backticks and `${SOURCE_ID}` included.
> # TAMPER used to prove the red (NOT part of this diff): documents.ts:1980 — `!== source.type` -> `(typeof x !== 'string' || x.trim() !== source.type)`, LINE-PINNED because that guard text also sits at :2590 (/sign-cert) and :2859 (/sign-wallet).
> # PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-VERSION-TRIM only). TIER 2 (test-only). Behaviour change: none.
> # RAISE WITH the four siblings as ONE PR — this one (145-150) · SIGNWALLET (174-179) · LOOSE (179-184) · RECHECK (204-209) · SIGNCERT (EOF): `Refs KS-1229 (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR, X-ISSUE-LOOSE, X-SIGNCERT-AFTER-UPSTREAM, X-SIGNWALLET-SERVED, X-VERSION-TRIM)`. Apply lowest-line-first; later hunks take their offsets.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`.

## The exact change
```
@@ -145,3 +145,15 @@
   ['/sign-cert', `/api/documents/${SOURCE_ID}/sign-cert`, (metadata) => ({ ...(metadata ? { metadata } : {}) })],
   ['/sign-wallet', `/api/documents/${SOURCE_ID}/sign-wallet`, (metadata) => ({ walletAddress: 'addr_test1ks1213', signature: 'a1', key: 'a2', ...(metadata ? { metadata } : {}) })],
+describe('KS-1229 X-VERSION-TRIM - the /version guard compares EXACTLY, so a padded carrier is refused', () => {
+  const version = (documentType: string) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/version', { action: 'watermark', newContentHash: HASH, metadata: { documentType } });
+  it('RED KS-1229 VT1 - a trailing-space carrier is refused, never trimmed into a match', async () => {
+    // KS-1229 (X-VERSION-TRIM): trimming would store DOCUMENT and serve the padded label - a relabel by invisible whitespace.
+    seed('DOCUMENT');
+    expect(await version('DOCUMENT ')).toEqual(REFUSED);
+  }); // KS-1229 VT1
+  it('control - KS-1229 the exact carrier is accepted and served as that type', async () => {
+    seed('DOCUMENT');
+    expect(await version('DOCUMENT')).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
+  }); // KS-1229 VT control
+});
 ];
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1229 VT1 - a trailing-space carrier is refused, never trimmed into a match`
- `control - KS-1229 the exact carrier is accepted and served as that type`  (CONTROL - green on both trees)

## Tampers
### VERSIONTRIM
File: `Blockchain/Dev/services/originate/src/routes/documents.ts`
Line: 1993
From:
```
      if (metadata.documentType !== undefined && metadata.documentType !== source.type) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      const newExternalId = `doc-${Date.now()}-${uuidv4().slice(0, 8)}`;
```
To:
```
      if (metadata.documentType !== undefined && (typeof metadata.documentType !== 'string' || metadata.documentType.trim() !== source.type)) { // TAMPER: KS-1229 red-proof, the guard trims the carrier before comparing (the gate row X-VERSION-TRIM)
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      const newExternalId = `doc-${Date.now()}-${uuidv4().slice(0, 8)}`;
```
Reds: `RED KS-1229 VT1 - a trailing-space carrier is refused, never trimmed into a match`
(From located at the tip: 1 match(es); block tamper of 5 lines; the old brief/input said line 1980)

## Controls
- `control - KS-1229 the exact carrier is accepted and served as that type`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
