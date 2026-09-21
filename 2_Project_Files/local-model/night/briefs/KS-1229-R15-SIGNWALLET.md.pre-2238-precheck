# KS-1229 R15-SIGNWALLET - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 226 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `jest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1229-SIGNWALLET_ornith35b-q4_TESTONLY-JEST-STORED-NOT-SERVED-PASS-7of7_2026-09-18.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 1573 B sha256[:16] `f755ba1e6ea29c89`, +13/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` at the tip: EXISTS (226 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/split_1229signwallet/KS-1229.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1229: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1229.md.
- Generator notes: dropped 1 blank + line(s) (a blank + is refused in a modify fence); RE-ANCHORED: the old hunk appended at EOF / before a blank line; the last leading context line '});' is now the TRAILING context, so the new block lands one line UP (inside the enclosing block) - a placement change from the old READY, said here; tamper SIGNWALLET: the one-line From occurs 3x at the tip; WIDENED to a 5-line block starting at :2878 (the occurrence nearest the old line 2859) - an INFERENCE by line proximity; Wednesday confirms the site.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1229 X-SIGNWALLET-SERVED (TEST-ONLY, jest, originate: sign-wallet compares with the STORED type, not the served label)
> # FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — INSERT the block after line 176 (the `});` closing describe.each(WRITERS)), before the blank line 177. Hunk `@@ -174,6 +174,19 @@`, strict apply, no fuzzy.
> # VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night5). A2 strict; A3c 12/12; A4 1 failed / 87 — the declared cell SW1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
> # Source read by Wednesday: the model's 13 `+` lines IDENTICAL in sequence to the brief fence (a mutated copy unequal); its three context lines equal tip lines 174-176 exactly.
> # TAMPER used to prove the red (NOT part of this diff): documents.ts:2859 — `source.type` -> `source.data?.documentType ?? source.type`, LINE-PINNED because that guard text also sits at :1980 (/version) and :2590 (/sign-cert).
> # WHY THE CONTROL IS SOUND: it uses an ordinary source with no `data.documentType`, so the tampered expression reduces to the tip's — green on BOTH trees by construction, which is what lets A4's "controls green" mean something here.
> # PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-SIGNWALLET-SERVED only). TIER 2 (test-only). Behaviour change: none.
> # RAISE WITH the three siblings as ONE PR: READY_KS-1229-SIGNWALLET (174-179) · READY_KS-1229-LOOSE (179-184) · READY_KS-1229_…-RECHECK (204-209) · READY_KS-1229-SIGNCERT (EOF) — `Refs KS-1229 (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR, X-ISSUE-LOOSE, X-SIGNCERT-AFTER-UPSTREAM, X-SIGNWALLET-SERVED)`. Apply lowest-line-first; later hunks take their offsets. NOTE: this hunk's lower context (177-179) is the LOOSE hunk's upper neighbourhood — apply this one FIRST, then LOOSE, and let patch offset.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`.

## The exact change
```
@@ -174,3 +174,15 @@
     });
   });
+describe('KS-1229 X-SIGNWALLET-SERVED - sign-wallet compares with the STORED type, not the served label', () => {
+  const signWallet = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata });
+  it('RED KS-1229 SW1 - a legacy source served as DEGREE still refuses metadata.documentType DEGREE', async () => {
+    // KS-1229 (X-SIGNWALLET-SERVED): the new row would be STORED CERTIFICATE and SERVED DEGREE - the relabel KS-1213 closed.
+    seed('CERTIFICATE', { documentType: 'DEGREE' });
+    expect(await signWallet({ documentType: 'DEGREE' })).toEqual(REFUSED);
+  }); // KS-1229 SW1
+  it('control - KS-1229 an ordinary source accepts a metadata.documentType equal to its stored type', async () => {
+    seed('DOCUMENT');
+    expect(await signWallet({ documentType: 'DOCUMENT' })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
+  }); // KS-1229 SW control
+});
 });
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1229 SW1 - a legacy source served as DEGREE still refuses metadata.documentType DEGREE`
- `control - KS-1229 an ordinary source accepts a metadata.documentType equal to its stored type`  (CONTROL - green on both trees)

## Tampers
### SIGNWALLET
File: `Blockchain/Dev/services/originate/src/routes/documents.ts`
Line: 2878
From:
```
      if (metadata.documentType !== undefined && metadata.documentType !== source.type) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      // 2. Verify the wallet signature SERVER-SIDE (KS-274): the wallet must
```
To:
```
      if (metadata.documentType !== undefined && metadata.documentType !== ((source.data as Record<string, unknown> | undefined)?.documentType ?? source.type)) { // TAMPER: KS-1229 red-proof, the guard compares with the SERVED label instead of the stored type (the gate row X-SIGNWALLET-SERVED)
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      // 2. Verify the wallet signature SERVER-SIDE (KS-274): the wallet must
```
Reds: `RED KS-1229 SW1 - a legacy source served as DEGREE still refuses metadata.documentType DEGREE`
(From located at the tip: 1 match(es); block tamper of 5 lines; the old brief/input said line 2859)

## Controls
- `control - KS-1229 an ordinary source accepts a metadata.documentType equal to its stored type`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
