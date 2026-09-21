# KS-1229 R15-AFTERVERIFY - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 226 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `jest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1229-AFTERVERIFY_ornith35b-q4_TESTONLY-JEST-LABEL-REFUSAL-BEFORE-CIP8-PASS-7of7_2026-09-18.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 1815 B sha256[:16] `82de649e95f5ebd6`, +20/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` at the tip: EXISTS (226 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/split_1229afterverify/KS-1229.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1229: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1229.md.
- Generator notes: dropped 1 blank + line(s) (a blank + is refused in a modify fence); RE-ANCHORED: the old hunk appended at EOF / before a blank line; the last leading context line 'beforeEach(() => { store.clear' is now the TRAILING context, so the new block lands one line UP (inside the enclosing block) - a placement change from the old READY, said here; tamper AFTERVERIFY: the one-line From occurs 3x at the tip; WIDENED to a 5-line block starting at :2878 (the occurrence nearest the old line 2859) - an INFERENCE by line proximity; Wednesday confirms the site.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1229 Q-SIGNWALLET-AFTER-VERIFY (TEST-ONLY, jest, originate: the label refusal precedes the wallet-signature check)
> # FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — INSERT the block after line 120 (the `beforeEach(...)` one-liner), before the blank line 121. Hunk `@@ -118,6 +118,26 @@`, strict apply, no fuzzy.
> # VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night7). A2 strict; A3c 19/19; A4 1 failed / 87 — the declared cell AV1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
> # Source read by Wednesday: the model's 20 `+` lines IDENTICAL in sequence to the brief fence (a mutated copy unequal), including the `finally` restore line; its three context lines equal tip 118-120 exactly.
> # HOW THE RED IS PROVEN: tamper at documents.ts:2859 (LINE-PINNED; the same guard text sits at :1980 and :2590) replaces the guard line with TWO statements — an early CIP-8 check that returns INVALID_WALLET_SIGNATURE, then the original guard line unchanged. The cell makes the suite's shared `verifyMessageSignature` stub return false for its own duration and restores it in `finally`.
> # ⚠ READ BEFORE MOVING IT: the block sits ABOVE the declarations it uses (`write`, `seed`, `ISSUER`, `SOURCE_ID`). That is deliberate and measured — `write`/`seed` are hoisted function declarations and the consts are read only inside `it` bodies. A5 87/87 at the tip is the proof; do not "fix" it by relocating the block.
> # THE RESTORE is proven only INDIRECTLY (A5 87/87 in-file and A6 743 suite-wide, so no later cell inherited a false signature) — there is no separate assertion for it.
> # PR NOTES: Refs KS-1229 (NOT Closes: this is the row Q-SIGNWALLET-AFTER-VERIFY only). TIER 2 (test-only). Behaviour change: none.
> # RAISE WITH the five siblings as ONE PR — this one (118-123) · VERSIONTRIM (145-150) · SIGNWALLET (174-179) · LOOSE (179-184) · RECHECK (204-209) · SIGNCERT (EOF). Apply lowest-line-first; later hunks take their offsets.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`.

## The exact change
```
@@ -118,3 +118,22 @@
   server?.close(); stub?.close();
 });
+describe('KS-1229 Q-SIGNWALLET-AFTER-VERIFY - the label refusal comes BEFORE the wallet signature check', () => {
+  it('RED KS-1229 AV1 - a mislabelled request with a bad signature is refused BAD_REQUEST, not INVALID_WALLET_SIGNATURE', async () => {
+    // KS-1229 (Q-SIGNWALLET-AFTER-VERIFY): the cheap, caller-fixable refusal must precede the CIP-8 check.
+    const shared = jest.requireMock('@secuura/shared') as { verifyMessageSignature: jest.Mock };
+    seed('DOCUMENT');
+    shared.verifyMessageSignature.mockImplementation(() => false);
+    try {
+      const r = await write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata: { documentType: 'PROPERTY_DEED' } });
+      expect([r.status, r.code, r.saved]).toEqual([400, 'BAD_REQUEST', 0]);
+    } finally {
+      shared.verifyMessageSignature.mockImplementation(() => true);
+    }
+  }); // KS-1229 AV1
+  it('control - KS-1229 the same mislabelled request with a good signature is refused BAD_REQUEST', async () => {
+    seed('DOCUMENT');
+    const r = await write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata: { documentType: 'PROPERTY_DEED' } });
+    expect([r.status, r.code, r.saved]).toEqual([400, 'BAD_REQUEST', 0]);
+  }); // KS-1229 AV control
+});
 beforeEach(() => { store.clear(); saved.length = 0; mockSaveCertification.mockClear(); });
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1229 AV1 - a mislabelled request with a bad signature is refused BAD_REQUEST, not INVALID_WALLET_SIGNATURE`
- `control - KS-1229 the same mislabelled request with a good signature is refused BAD_REQUEST`  (CONTROL - green on both trees)

## Tampers
### AFTERVERIFY
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
      if (!verifyMessageSignature(walletAddress, source.contentHash, signature, key)) { return res.status(400).json({ success: false, error: { code: 'INVALID_WALLET_SIGNATURE', message: 'TAMPER: KS-1229 red-proof, the CIP-8 check now runs BEFORE the label refusal (the gate row Q-SIGNWALLET-AFTER-VERIFY)' } }); } if (metadata.documentType !== undefined && metadata.documentType !== source.type) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      // 2. Verify the wallet signature SERVER-SIDE (KS-274): the wallet must
```
Reds: `RED KS-1229 AV1 - a mislabelled request with a bad signature is refused BAD_REQUEST, not INVALID_WALLET_SIGNATURE`
(From located at the tip: 1 match(es); block tamper of 5 lines; the old brief/input said line 2859)

## Controls
- `control - KS-1229 the same mislabelled request with a good signature is refused BAD_REQUEST`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
